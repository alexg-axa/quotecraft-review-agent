from __future__ import annotations

import os
import re
import textwrap
from html import escape
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from pypdf import PdfReader
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer
from rich.console import Console


console = Console()

APP_TEXT_FILE_PATTERNS = [
    "README.md",
    "Dockerfile",
    ".github/workflows/*.yml",
    ".github/workflows/*.yaml",
    "docs/*.md",
    "docs/*.yaml",
    "deploy/openshift/*.yaml",
    "infra/**/*.tf",
    "src/**/*.py",
]

CASE_TEXT_FILE_PATTERNS = [
    "hackathon_task.md",
    "hackathon-assets/*.yaml",
]

CASE_PDF_FILE_PATTERNS = [
    "hackathon-assets/*.pdf",
]

POLICY_CLAUSE_ID_PATTERN = re.compile(r"\b(AHS|ARS|ASC|CKS|DCH|FIN)-\d{2}\b")

OUTPUT_DIR = Path("outputs")
MARKDOWN_REPORT_NAME = "review-report.md"
PDF_REPORT_NAME = "review-report.pdf"

SYSTEM_PROMPT = """
You are an AlphaInsure architecture review agent.

You are a LangChain tool-using agent. Before writing the report, call the tools
in this order:
1. list_evidence_sources
2. build_policy_clause_index
3. analyze_evidence_precedence
4. collect_review_evidence

Produce a findings report, not a summary.

Review QuoteCraft using only evidence returned by the tools. Do not make
generic cloud, OpenShift, Kubernetes, or security recommendations unless they
are tied to specific QuoteCraft evidence and a specific AlphaPaaS policy clause.

If evidence is missing or contradictory, report that as a finding and cite the
conflicting sources.

When sources disagree, apply this evidence precedence model:
1. Intake form = review contract and declared requirements.
2. AlphaPaaS policies = compliance standard.
3. Manifests, Terraform, source code, and CI = implementation reality.
4. Architecture docs, runbooks, and capacity plans = declared intent,
   operational notes, or planning evidence.

If implementation reality conflicts with a document claim, prefer
implementation reality for current-state findings and cite the conflict.

Return exactly this Markdown structure:

# QuoteCraft Architecture Review Findings

## Executive Summary
Write 3-5 bullets only. Do not stop here.

## Findings
Return 8-12 findings grouped by dimension in this exact order:

### Cost
List Cost findings here, sorted by severity in this order: Critical, High,
Medium, Low.

### Security
List Security findings here, sorted by severity in this order: Critical, High,
Medium, Low.

### Scalability
List Scalability findings here, sorted by severity in this order: Critical,
High, Medium, Low.

### Availability
List Availability findings here, sorted by severity in this order: Critical,
High, Medium, Low.

For each finding, use this exact structure under the relevant dimension heading:

#### F-01: <short title>
- Severity: Critical, High, Medium, or Low
- Dimension: Cost, Security, Scalability, or Availability
- Evidence:
  - Source: <file path or PDF name from the evidence header>
  - Quote: "<short exact quote or very close paraphrase from the evidence>"
- Policy reference: <policy clause ID, for example ARS-15, CKS-06, FIN-07>
- Why it matters: <business or operational impact>
- Remediation: <concrete next step suitable for a backlog ticket>
- Confidence: High, Medium, or Low

## Highest Priority Next Actions
Return the top 5 remediation actions in priority order.

Important rules:
- Every finding must cite at least one evidence source.
- Findings must be grouped in this exact dimension order: Cost, Security,
  Scalability, Availability.
- Within each dimension, findings must be sorted by this severity order:
  Critical, High, Medium, Low.
- Prefer exact policy clause IDs over policy document names.
- If a finding is based on conflicting documents, include both sources.
- Do not invent file names, line numbers, clauses, or implementation details.
- Do not include generic best-practice advice.
""".strip()

USER_PROMPT = """
Perform an architecture review of QuoteCraft across security, availability,
scalability, and cost. Use the available evidence tools first, then write the
final Markdown report.
""".strip()


def get_app_repo_path() -> Path:
    return Path(os.getenv("QUOTECRAFT_REPO_PATH", "..\\quotecraft")).resolve()


def get_case_materials_path() -> Path:
    return Path(os.getenv("CASE_MATERIALS_PATH", ".\\case-materials")).resolve()


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(f"--- page {page_number} ---\n{text}")
    return "\n".join(pages)


def clean_snippet(text: str, limit: int = 360) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3].rstrip() + "..."


def collect_matching_files(root: Path, patterns: list[str]) -> list[Path]:
    files: list[Path] = []
    for pattern in patterns:
        files.extend(path for path in root.glob(pattern) if path.is_file())
    return sorted(set(files))


def format_source_header(source_root: Path, path: Path, source_type: str) -> str:
    relative_name = path.relative_to(source_root).as_posix()
    return f"{source_type}:{relative_name}"


def build_evidence_inventory(app_repo_path: Path, case_materials_path: Path) -> str:
    lines = [
        f"Application repository: {app_repo_path}",
        f"Case materials: {case_materials_path}",
        "",
        "Application evidence files:",
    ]

    for path in collect_matching_files(app_repo_path, APP_TEXT_FILE_PATTERNS):
        lines.append(f"- {format_source_header(app_repo_path, path, 'app')}")

    lines.append("")
    lines.append("Case material text files:")
    for path in collect_matching_files(case_materials_path, CASE_TEXT_FILE_PATTERNS):
        lines.append(f"- {format_source_header(case_materials_path, path, 'case')}")

    lines.append("")
    lines.append("Case material PDF files:")
    for path in collect_matching_files(case_materials_path, CASE_PDF_FILE_PATTERNS):
        lines.append(f"- {format_source_header(case_materials_path, path, 'case')}")

    return "\n".join(lines)


def collect_review_evidence_text(app_repo_path: Path, case_materials_path: Path) -> str:
    sections: list[str] = []

    for path in collect_matching_files(case_materials_path, CASE_TEXT_FILE_PATTERNS):
        source = format_source_header(case_materials_path, path, "case")
        sections.append(f"===== {source} =====\n{read_text_file(path)}")

    for path in collect_matching_files(case_materials_path, CASE_PDF_FILE_PATTERNS):
        source = format_source_header(case_materials_path, path, "case")
        sections.append(f"===== {source} =====\n{read_pdf(path)}")

    for path in collect_matching_files(app_repo_path, APP_TEXT_FILE_PATTERNS):
        source = format_source_header(app_repo_path, path, "app")
        sections.append(f"===== {source} =====\n{read_text_file(path)}")

    return "\n\n".join(sections)


def extract_policy_clauses_from_text(source: str, text: str) -> list[tuple[str, str, str]]:
    clauses: list[tuple[str, str, str]] = []
    matches = list(POLICY_CLAUSE_ID_PATTERN.finditer(text))
    for index, match in enumerate(matches):
        clause_id = match.group(0)
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        clause_text = clean_snippet(text[start:end], limit=520)
        clauses.append((clause_id, source, clause_text))
    return clauses


def build_policy_clause_index_text(case_materials_path: Path) -> str:
    clauses: list[tuple[str, str, str]] = []
    for path in collect_matching_files(case_materials_path, CASE_PDF_FILE_PATTERNS):
        source = format_source_header(case_materials_path, path, "case")
        clauses.extend(extract_policy_clauses_from_text(source, read_pdf(path)))

    if not clauses:
        return "No policy clauses were extracted from case-material PDFs."

    lines = ["Policy clause index extracted from case-material PDFs:"]
    for clause_id, source, clause_text in clauses:
        lines.append(f"- {clause_id} | {source} | {clause_text}")
    return "\n".join(lines)


def read_app_file(app_repo_path: Path, relative_path: str) -> str:
    path = app_repo_path / relative_path
    if not path.exists():
        return ""
    return read_text_file(path)


def source_quote(source: str, quote: str) -> str:
    return f"  - Source: {source}\n    Quote: \"{clean_snippet(quote, limit=300)}\""


def analyze_evidence_precedence_text(app_repo_path: Path) -> str:
    architecture = read_app_file(app_repo_path, "docs/architecture.md")
    capacity = read_app_file(app_repo_path, "docs/capacity-plan.md")
    runbook = read_app_file(app_repo_path, "docs/runbook.md")
    deployment = read_app_file(app_repo_path, "deploy/openshift/deployment.yaml")
    route = read_app_file(app_repo_path, "deploy/openshift/route.yaml")

    lines = [
        "Evidence precedence model:",
        "1. Intake form = review contract and declared requirements.",
        "2. AlphaPaaS policies = compliance standard.",
        "3. Manifests, Terraform, source code, and CI = implementation reality.",
        "4. Architecture docs, runbooks, and capacity plans = declared intent, operational notes, or planning evidence.",
        "",
        "Deterministic contradiction and precedence analysis:",
    ]

    checks: list[str] = []

    if "zone-redundant high availability" in architecture and "High availability: single-zone" in capacity:
        checks.append(
            "\n[Availability] PostgreSQL HA conflict. Implementation/planning evidence should be verified against Terraform; capacity plan is weaker than architecture doc.\n"
            + source_quote("app:docs/architecture.md", "Configured with zone-redundant high availability.")
            + "\n"
            + source_quote("app:docs/capacity-plan.md", 'High availability: single-zone (see "Open items" below)')
            + "\n  Likely policy references: ARS-18, ASC-04."
        )

    if "Accessed via Private Endpoint through the vWAN Hub" in architecture and "Move of Postgres traffic to the Private Endpoint" in capacity:
        checks.append(
            "\n[Security] Cross-CSP private connectivity conflict. The architecture claims Private Endpoint use, but the capacity plan tracks the move as an open item.\n"
            + source_quote("app:docs/architecture.md", "Accessed via Private Endpoint through the vWAN Hub; no traffic leaves the AlphaInsure private network.")
            + "\n"
            + source_quote("app:docs/capacity-plan.md", "Move of Postgres traffic to the Private Endpoint (QC-168)")
            + "\n  Likely policy references: AHS-16, AHS-17, ASC-07."
        )

    if "replicas in 1b and 1c" in architecture and "Nodes: 1 (single-AZ)" in capacity:
        checks.append(
            "\n[Availability] Redis topology conflict. Architecture describes multi-AZ Redis replicas, while capacity plan says Redis is a single-AZ single-node service.\n"
            + source_quote("app:docs/architecture.md", "Deployed as a replication group with a primary node in zone 1a and replicas in 1b and 1c.")
            + "\n"
            + source_quote("app:docs/capacity-plan.md", "Nodes: 1 (single-AZ)")
            + "\n  Likely policy references: ARS-18, ASC approved service requirements for ElastiCache Redis."
        )

    if "Azure Key Vault" in architecture and "HashiCorp Vault" in runbook:
        checks.append(
            "\n[Security] Secrets manager conflict. Architecture names Azure Key Vault; runbook names HashiCorp Vault. Both may be approved, but the current source of truth is unclear.\n"
            + source_quote("app:docs/architecture.md", "Secrets are sourced from Azure Key Vault via the External Secrets Operator.")
            + "\n"
            + source_quote("app:docs/runbook.md", "Secrets are managed in HashiCorp Vault.")
            + "\n  Likely policy references: CKS-10, CKS-11, DCH-07."
        )

    if "replicas: 1" in deployment:
        checks.append(
            "\n[Availability] Manifest reality conflicts with Silver capacity expectations. Deployment manifest sets one replica, while Silver workloads require at least three replicas.\n"
            + source_quote("app:deploy/openshift/deployment.yaml", "replicas: 1")
            + "\n"
            + source_quote("app:docs/capacity-plan.md", "Expected baseline replica count: 6 (2 per AZ)")
            + "\n  Likely policy references: ARS-02, ARS criticality tier table."
        )

    if "failure-domain.alphapaas.com/zone" in deployment and "topologySpreadConstraints" not in deployment:
        checks.append(
            "\n[Availability] Manifest pins pods to one zone instead of declaring topology spread constraints.\n"
            + source_quote("app:deploy/openshift/deployment.yaml", 'failure-domain.alphapaas.com/zone: "1"')
            + "\n  Likely policy references: ARS-05."
        )

    if "quotecraft:latest" in deployment or "quotecraft:latest" in capacity:
        checks.append(
            "\n[Security] Image tag is not pinned. Evidence mentions `quotecraft:latest`, which is prohibited for production/pre-production manifests.\n"
            + source_quote("app:deploy/openshift/deployment.yaml", "image: quotecraft:latest")
            + "\n"
            + source_quote("app:docs/capacity-plan.md", "Container image: `quotecraft:latest`")
            + "\n  Likely policy references: CKS-06."
        )

    if "envFrom:" in deployment or "secretKeyRef:" in deployment:
        checks.append(
            "\n[Security] Manifest injects secrets through environment variables, conflicting with documentation that claims file-volume projection.\n"
            + source_quote("app:deploy/openshift/deployment.yaml", "envFrom: ... secretRef: name: quotecraft-secrets")
            + "\n"
            + source_quote("app:deploy/openshift/deployment.yaml", "valueFrom: secretKeyRef:")
            + "\n"
            + source_quote("app:docs/architecture.md", "Secrets are projected into pods as file volumes, not environment variables.")
            + "\n  Likely policy references: CKS-11, DCH-07."
        )

    if "/health/deep" in deployment or "Used as both the readiness and liveness probe" in runbook:
        checks.append(
            "\n[Availability] Deep database health check is used for liveness, which can restart healthy pods during downstream database incidents.\n"
            + source_quote("app:deploy/openshift/deployment.yaml", "livenessProbe: httpGet: path: /health/deep")
            + "\n"
            + source_quote("app:docs/runbook.md", "Used as both the readiness and liveness probe by Kubernetes.")
            + "\n  Likely policy references: ARS-07."
        )

    if "Backup retention: 7 days" in capacity:
        checks.append(
            "\n[Availability] PostgreSQL backup retention is below Silver requirement.\n"
            + source_quote("app:docs/capacity-plan.md", "Backup retention: 7 days")
            + "\n  Likely policy references: ARS-15."
        )

    if "DR exercise: **not yet performed.**" in capacity or "### Single-AZ loss\n\nTODO." in runbook:
        checks.append(
            "\n[Availability] DR testing and runbook procedures are incomplete for a Silver workload.\n"
            + source_quote("app:docs/capacity-plan.md", "DR exercise: **not yet performed.** Scheduled for Q3 2026.")
            + "\n"
            + source_quote("app:docs/runbook.md", "Single-AZ loss TODO. Full region loss TODO.")
            + "\n  Likely policy references: ARS-20, ARS-21, ARS-22."
        )

    if "in-memory rate limiter" in runbook:
        checks.append(
            "\n[Scalability] In-memory rate limiter is incompatible with horizontal scaling.\n"
            + source_quote("app:docs/runbook.md", "This is a known issue with the current in-memory rate limiter when the service is scaled to multiple pods.")
            + "\n  Likely policy references: ARS-14."
        )

    if "Throughput mode: provisioned, 200 MiB/s" in capacity:
        checks.append(
            "\n[Cost] EFS uses provisioned throughput; this requires documented IOPS/throughput justification.\n"
            + source_quote("app:docs/capacity-plan.md", "Throughput mode: provisioned, 200 MiB/s")
            + "\n  Likely policy references: FIN-06."
        )

    if route and "router=irp" not in route and "router:" not in route:
        checks.append(
            "\n[Security] Route manifest may not carry the required explicit router label; verify against AHS route-label requirements.\n"
            + source_quote("app:deploy/openshift/route.yaml", "No explicit router label found by deterministic scan.")
            + "\n  Likely policy references: AHS-04, AHS-05."
        )

    if not checks:
        lines.append("No deterministic contradictions were detected by the Day 3 scanner.")
    else:
        lines.extend(checks)

    return "\n".join(lines)


@tool
def list_evidence_sources() -> str:
    """List the QuoteCraft application and case-material files available for review."""
    return build_evidence_inventory(get_app_repo_path(), get_case_materials_path())


@tool
def collect_review_evidence() -> str:
    """Collect QuoteCraft policy, intake, documentation, manifest, Terraform, and source evidence."""
    evidence = collect_review_evidence_text(get_app_repo_path(), get_case_materials_path())
    if not evidence.strip():
        return "No evidence was collected. Check QUOTECRAFT_REPO_PATH and CASE_MATERIALS_PATH."
    return evidence


@tool
def build_policy_clause_index() -> str:
    """Extract AlphaPaaS policy clause IDs and short clause text from case-material PDFs."""
    return build_policy_clause_index_text(get_case_materials_path())


@tool
def analyze_evidence_precedence() -> str:
    """Analyze evidence precedence and known contradictions between docs, manifests, and policies."""
    return analyze_evidence_precedence_text(get_app_repo_path())


def save_markdown_report(report: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / MARKDOWN_REPORT_NAME
    path.write_text(report, encoding="utf-8")
    return path


def save_pdf_report(report: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / PDF_REPORT_NAME

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    subheading_style = styles["Heading3"]
    body_style = styles["BodyText"]
    body_style.leading = 14

    doc = SimpleDocTemplate(
        str(path),
        pagesize=LETTER,
        rightMargin=48,
        leftMargin=48,
        topMargin=48,
        bottomMargin=48,
        title="QuoteCraft Architecture Review",
    )

    story = [Paragraph("QuoteCraft Architecture Review", title_style), Spacer(1, 16)]
    for raw_line in report.splitlines():
        line = raw_line.strip()
        if not line:
            story.append(Spacer(1, 8))
            continue
        if line.startswith("# "):
            continue
        if line.startswith("## "):
            story.append(PageBreak() if line == "## Findings" else Spacer(1, 10))
            story.append(Paragraph(escape(line.removeprefix("## ")), heading_style))
            story.append(Spacer(1, 8))
            continue
        if line.startswith("### "):
            story.append(Spacer(1, 10))
            story.append(Paragraph(escape(line.removeprefix("### ")), subheading_style))
            story.append(Spacer(1, 4))
            continue
        if line.startswith("#### "):
            story.append(Spacer(1, 8))
            story.append(Paragraph(escape(line.removeprefix("#### ")), heading_style))
            story.append(Spacer(1, 4))
            continue

        for wrapped_line in textwrap.wrap(line, width=105) or [""]:
            story.append(Paragraph(escape(wrapped_line), body_style))

    doc.build(story)
    return path


def create_model() -> ChatOpenAI:
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    base_url = os.getenv("AZURE_OPENAI_BASE_URL")
    model_name = os.getenv("AZURE_OPENAI_MODEL")

    missing = [
        name
        for name, value in [
            ("AZURE_OPENAI_API_KEY", api_key),
            ("AZURE_OPENAI_BASE_URL", base_url),
            ("AZURE_OPENAI_MODEL", model_name),
        ]
        if not value
    ]
    if missing:
        raise RuntimeError(
            "Missing required environment variables: " + ", ".join(missing)
        )

    return ChatOpenAI(
        base_url=base_url,
        api_key=api_key,
        model=model_name,
        temperature=0.1,
        max_tokens=4000,
    )


def extract_final_content(agent_response: dict) -> str:
    messages = agent_response.get("messages", [])
    if not messages:
        return str(agent_response)

    final_message = messages[-1]
    content = getattr(final_message, "content", None)
    if content is None and isinstance(final_message, dict):
        content = final_message.get("content")

    if isinstance(content, list):
        return "\n".join(
            item.get("text", str(item)) if isinstance(item, dict) else str(item)
            for item in content
        )

    return str(content)


def validate_paths(app_repo_path: Path, case_materials_path: Path) -> None:
    if not app_repo_path.exists():
        raise RuntimeError(f"QuoteCraft repo path does not exist: {app_repo_path}")
    if not case_materials_path.exists():
        raise RuntimeError(f"Case materials path does not exist: {case_materials_path}")


def main() -> None:
    load_dotenv()

    app_repo_path = get_app_repo_path()
    case_materials_path = get_case_materials_path()
    validate_paths(app_repo_path, case_materials_path)

    console.print(f"[bold]Application repository:[/bold] {app_repo_path}")
    console.print(f"[bold]Case materials:[/bold] {case_materials_path}")
    console.print("[bold]Running LangChain architecture review agent...[/bold]")

    agent = create_agent(
        model=create_model(),
        tools=[
            list_evidence_sources,
            build_policy_clause_index,
            analyze_evidence_precedence,
            collect_review_evidence,
        ],
        system_prompt=SYSTEM_PROMPT,
    )
    response = agent.invoke({"messages": [{"role": "user", "content": USER_PROMPT}]})
    report = extract_final_content(response)

    console.print("\n[bold]QuoteCraft Architecture Review[/bold]\n")
    console.print(report)

    markdown_path = save_markdown_report(report, OUTPUT_DIR)
    pdf_path = save_pdf_report(report, OUTPUT_DIR)
    console.print(f"\n[bold]Saved Markdown:[/bold] {markdown_path.resolve()}")
    console.print(f"[bold]Saved PDF:[/bold] {pdf_path.resolve()}")


if __name__ == "__main__":
    main()

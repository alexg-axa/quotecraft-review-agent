from __future__ import annotations

import os
import textwrap
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from pypdf import PdfReader
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer
from rich.console import Console


console = Console()


TEXT_FILE_PATTERNS = [
    "docs/*.md",
    "docs/*.yaml",
    "deploy/openshift/*.yaml",
    "infra/**/*.tf",
]

PDF_FILE_NAMES = [
    "hackathon-assets/hackathon-quotecraft-intake-form.pdf",
    "hackathon-assets/AHS_Application_Hosting_Standard.pdf",
    "hackathon-assets/ARS_Availability_and_Resilience_Standard.pdf",
    "hackathon-assets/ASC_Approved_Services_Catalog.pdf",
    "hackathon-assets/CKS_Container_and_Kubernetes_Security_Standard.pdf",
    "hackathon-assets/DCH_Data_Classification_and_Handling_Standard.pdf",
    "hackathon-assets/FIN_FinOps_and_Cloud_Cost_Standard.pdf",
]

OUTPUT_DIR = Path("outputs")
MARKDOWN_REPORT_NAME = "review-report.md"
PDF_REPORT_NAME = "review-report.pdf"


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(f"--- page {page_number} ---\n{text}")
    return "\n".join(pages)


def collect_evidence(repo_path: Path) -> str:
    sections: list[str] = []

    for relative_name in PDF_FILE_NAMES:
        path = repo_path / relative_name
        if path.exists():
            sections.append(f"===== {relative_name} =====\n{read_pdf(path)}")

    for pattern in TEXT_FILE_PATTERNS:
        for path in sorted(repo_path.glob(pattern)):
            if path.is_file():
                relative_name = path.relative_to(repo_path).as_posix()
                sections.append(f"===== {relative_name} =====\n{read_text_file(path)}")

    return "\n\n".join(sections)


def build_prompt(evidence: str) -> str:
    return f"""
You are an AlphaInsure architecture review agent.

Your task is to produce a findings report, not a summary.

Review QuoteCraft using only the supplied evidence. Do not make generic cloud,
OpenShift, Kubernetes, or security recommendations unless they are tied to
specific QuoteCraft evidence and a specific AlphaPaaS policy clause.

If evidence is missing or contradictory, report that as a finding and cite the
conflicting sources.

Find the most important issues across:
- security
- availability
- scalability
- cost

Return exactly this Markdown structure:

# QuoteCraft Architecture Review Findings

## Executive Summary
Write 3-5 bullets only. Do not stop here.

## Findings
Return 8-12 findings. For each finding, use this exact structure:

### F-01: <short title>
- Severity: Critical, High, Medium, or Low
- Dimension: Security, Availability, Scalability, Cost, or Evidence Quality
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
- Prefer exact policy clause IDs over policy document names.
- If a finding is based on conflicting documents, include both sources.
- Do not invent file names, line numbers, clauses, or implementation details.
- Do not include generic best-practice advice.

Evidence:
{evidence}
""".strip()


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
            story.append(Paragraph(line.removeprefix("## "), heading_style))
            story.append(Spacer(1, 8))
            continue
        if line.startswith("### "):
            story.append(Spacer(1, 10))
            story.append(Paragraph(line.removeprefix("### "), heading_style))
            story.append(Spacer(1, 4))
            continue

        for wrapped_line in textwrap.wrap(line, width=105) or [""]:
            story.append(Paragraph(wrapped_line, body_style))

    doc.build(story)
    return path


def create_model() -> ChatOpenAI | AzureChatOpenAI:
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing required environment variable: AZURE_OPENAI_API_KEY")

    base_url = os.getenv("AZURE_OPENAI_BASE_URL")
    model_name = os.getenv("AZURE_OPENAI_MODEL")
    if base_url:
        if not model_name:
            raise RuntimeError(
                "Missing required environment variable: AZURE_OPENAI_MODEL"
            )
        return ChatOpenAI(
            base_url=base_url,
            api_key=api_key,
            model=model_name,
            temperature=0.1,
            max_tokens=4000,
        )

    required = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_DEPLOYMENT",
        "AZURE_OPENAI_API_VERSION",
    ]
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        raise RuntimeError(
            "Missing required environment variables: " + ", ".join(missing)
        )

    return AzureChatOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=api_key,
        azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        temperature=0.1,
        max_tokens=4000,
    )


def main() -> None:
    load_dotenv()

    repo_path = Path(os.getenv("QUOTECRAFT_REPO_PATH", "..\\quotecraft")).resolve()
    if not repo_path.exists():
        raise RuntimeError(f"QuoteCraft repo path does not exist: {repo_path}")

    console.print(f"[bold]Reading evidence from:[/bold] {repo_path}")
    evidence = collect_evidence(repo_path)
    if not evidence.strip():
        raise RuntimeError("No evidence was collected. Check QUOTECRAFT_REPO_PATH.")

    console.print("[bold]Running architecture review...[/bold]")
    model = create_model()
    response = model.invoke(build_prompt(evidence))
    report = str(response.content)

    console.print("\n[bold]QuoteCraft Architecture Review[/bold]\n")
    console.print(report)

    markdown_path = save_markdown_report(report, OUTPUT_DIR)
    pdf_path = save_pdf_report(report, OUTPUT_DIR)
    console.print(f"\n[bold]Saved Markdown:[/bold] {markdown_path.resolve()}")
    console.print(f"[bold]Saved PDF:[/bold] {pdf_path.resolve()}")


if __name__ == "__main__":
    main()

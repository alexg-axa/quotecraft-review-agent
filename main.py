from __future__ import annotations

import argparse
import os
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

OUTPUT_DIR = Path("outputs")
MARKDOWN_REPORT_NAME = "review-report.md"
PDF_REPORT_NAME = "review-report.pdf"
EVIDENCE_INVENTORY_NAME = "evidence-inventory.md"

SYSTEM_PROMPT = """
You are an AlphaInsure architecture review agent.

You are a LangChain tool-using agent. Before writing the report, call the
available tools to inspect the evidence inventory and collect the review
evidence. Produce a findings report, not a summary.

Review QuoteCraft using only evidence returned by the tools. Do not make
generic cloud, OpenShift, Kubernetes, or security recommendations unless they
are tied to specific QuoteCraft evidence and a specific AlphaPaaS policy clause.

If evidence is missing or contradictory, report that as a finding and cite the
conflicting sources.

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

## Report Quality Check
Return a short checklist with Pass/Fail for:
- Findings are grouped by Cost, Security, Scalability, Availability.
- Every finding cites at least one evidence source.
- Every finding cites at least one policy clause.
- Findings are specific to QuoteCraft, not generic cloud advice.
- Recommendations are concrete enough for backlog tickets.

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


def save_markdown_report(report: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / MARKDOWN_REPORT_NAME
    path.write_text(report, encoding="utf-8")
    return path


def save_evidence_inventory(inventory: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / EVIDENCE_INVENTORY_NAME
    path.write_text(inventory, encoding="utf-8")
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the QuoteCraft architecture review agent."
    )
    parser.add_argument(
        "--repo-path",
        type=Path,
        default=None,
        help="Path to the QuoteCraft application repository.",
    )
    parser.add_argument(
        "--case-materials",
        type=Path,
        default=None,
        help="Path to the safe shared hackathon case materials.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help="Directory where reports are written.",
    )
    parser.add_argument(
        "--no-pdf",
        action="store_true",
        help="Skip PDF generation and save only Markdown.",
    )
    parser.add_argument(
        "--list-evidence",
        action="store_true",
        help="Print and save the evidence inventory without calling the model.",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Ask what to run: full review, evidence inventory only, or Markdown only.",
    )
    return parser.parse_args()


def apply_interactive_choices(args: argparse.Namespace) -> None:
    if not args.interactive:
        return

    console.print("\n[bold]What would you like to do?[/bold]")
    console.print("1. Full review")
    console.print("2. List evidence only")
    console.print("3. Markdown only")

    choice = ""
    while choice not in {"1", "2", "3"}:
        choice = input("Select 1, 2, or 3: ").strip()

    if choice == "1":
        args.list_evidence = False
        args.no_pdf = False
    elif choice == "2":
        args.list_evidence = True
        args.no_pdf = True
    elif choice == "3":
        args.list_evidence = False
        args.no_pdf = True


def main() -> None:
    load_dotenv()
    args = parse_args()
    apply_interactive_choices(args)

    app_repo_path = (args.repo_path or get_app_repo_path()).resolve()
    case_materials_path = (args.case_materials or get_case_materials_path()).resolve()
    validate_paths(app_repo_path, case_materials_path)
    output_dir = args.output_dir.resolve()

    console.print(f"[bold]Application repository:[/bold] {app_repo_path}")
    console.print(f"[bold]Case materials:[/bold] {case_materials_path}")
    console.print(f"[bold]Output directory:[/bold] {output_dir}")

    inventory = build_evidence_inventory(app_repo_path, case_materials_path)
    inventory_path = save_evidence_inventory(inventory, output_dir)
    console.print(f"[bold]Evidence inventory saved:[/bold] {inventory_path.resolve()}")

    if args.list_evidence:
        console.print("\n[bold]Evidence Inventory[/bold]\n")
        console.print(inventory)
        console.print("\n[bold]Model call:[/bold] skipped (--list-evidence)")
        return

    console.print("[bold]Running LangChain architecture review agent...[/bold]")

    agent = create_agent(
        model=create_model(),
        tools=[list_evidence_sources, collect_review_evidence],
        system_prompt=SYSTEM_PROMPT,
    )
    response = agent.invoke({"messages": [{"role": "user", "content": USER_PROMPT}]})
    report = extract_final_content(response)

    console.print("\n[bold]QuoteCraft Architecture Review[/bold]\n")
    console.print(report)

    markdown_path = save_markdown_report(report, output_dir)
    console.print(f"\n[bold]Saved Markdown:[/bold] {markdown_path.resolve()}")
    if args.no_pdf:
        console.print("[bold]Saved PDF:[/bold] skipped (--no-pdf)")
    else:
        pdf_path = save_pdf_report(report, output_dir)
        console.print(f"[bold]Saved PDF:[/bold] {pdf_path.resolve()}")


if __name__ == "__main__":
    main()

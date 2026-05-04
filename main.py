from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from pypdf import PdfReader
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

Review QuoteCraft using only the supplied evidence. Do not make generic
recommendations. If evidence is missing or contradictory, say so clearly.

Find the most important issues across:
- security
- availability
- scalability
- cost

For each finding, include:
- title
- severity: Critical, High, Medium, or Low
- dimension
- evidence source
- policy reference
- impact
- recommended remediation

Keep the report concise and practical.

Evidence:
{evidence}
""".strip()


def create_model() -> AzureChatOpenAI:
    required = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
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
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        temperature=0.1,
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

    console.print("\n[bold]QuoteCraft Architecture Review[/bold]\n")
    console.print(response.content)


if __name__ == "__main__":
    main()

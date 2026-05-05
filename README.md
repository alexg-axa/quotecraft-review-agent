# QuoteCraft Review Agent

Local architecture-review agent for the QuoteCraft hackathon.

The current Day 2 version uses LangChain's `create_agent` API with local tools
for evidence discovery and collection. Azure AI Foundry supplies the OpenAI-
compatible chat model.

## Repository Layout

Clone the application repository and this review-agent repository side by side:

```text
workspace/
  quotecraft/                 # application under review
  quotecraft-review-agent/    # this agent project
```

The `quotecraft` repository should be cloned from the original shared source:

```powershell
git clone https://github.com/cloudofficer/quotecraft.git
```

Clone this repository next to it:

```powershell
git clone https://github.com/alexg-axa/quotecraft-review-agent
```

The review agent expects the application repository at `..\quotecraft` and case
materials at `.\case-materials` by default. If your local folders are different,
update `QUOTECRAFT_REPO_PATH` and `CASE_MATERIALS_PATH` in your `.env` file.

Shared hackathon assets that are safe for the team repository should live in
`case-materials/`. Do not commit proprietary meeting transcripts, personal
notes, credentials, generated reports, or other internal-only material.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Fill in `.env` with your Azure model details and confirm the QuoteCraft path.
For Azure AI Foundry `/openai/v1` endpoints, use:

```env
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_BASE_URL=https://<your-foundry-resource>.services.ai.azure.com/openai/v1
AZURE_OPENAI_MODEL=<your-deployment-name>
QUOTECRAFT_REPO_PATH=..\quotecraft
CASE_MATERIALS_PATH=.\case-materials
```

The `AZURE_OPENAI_MODEL` value should be the deployment name shown in Azure AI
Foundry, for example `gpt-4.1`.

## Agent Design

The app uses a small LangChain tool-using agent:

- `list_evidence_sources` lists the application and case-material files
  available for review.
- `collect_review_evidence` reads the policy PDFs, intake/task materials,
  application docs, manifests, Terraform, and Python source files.
- The agent uses those tool results to produce a policy-backed Markdown
  findings report.

## Run

```powershell
python main.py
```

The command prints a Markdown architecture-review report to the terminal and
saves two files:

```text
outputs/review-report.md
outputs/review-report.pdf
```

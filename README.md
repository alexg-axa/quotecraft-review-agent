# QuoteCraft Review Agent

Day 1 scaffold for a small local architecture-review agent.

The first version reads evidence from the neighboring QuoteCraft repository,
asks an Azure OpenAI / Azure Foundry model to review it, and prints a Markdown
findings report.

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

The review agent expects the application repository at `..\quotecraft` by
default. If your local folders are different, update `QUOTECRAFT_REPO_PATH` in
your `.env` file.

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
```

For classic Azure OpenAI resource endpoints, use these instead:

```env
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=<your-deployment-name>
AZURE_OPENAI_API_VERSION=2024-10-21
QUOTECRAFT_REPO_PATH=..\quotecraft
```

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

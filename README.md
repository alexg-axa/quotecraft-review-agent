# QuoteCraft Review Agent

Local architecture-review agent for the QuoteCraft hackathon.

The current Day 3 version keeps the recommended LangChain ReAct-style agent
approach from the hackathon sessions and improves the user experience around
it: a model-backed agent receives a system prompt, decides which tools to call,
observes the tool results, and then writes the final answer. Azure AI Foundry
supplies the OpenAI-compatible chat model.

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

### on local Windows computer

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

### in Azure Shell Powershell

```azure shell powershell
python3 -m venv .venv
.\.venv\bin\Activate.ps1
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

The app uses a small LangChain ReAct-style tool-using agent built with:

```python
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
```

This keeps the hackathon coding pattern aligned with the recommended LangChain
agent approach while using Azure AI Foundry instead of AWS Bedrock for the model.

The current agent has two tools:

- `list_evidence_sources` lists the application and case-material files
  available for review.
- `collect_review_evidence` reads the policy PDFs, intake/task materials,
  application docs, manifests, Terraform, and Python source files.
- The agent uses those tool results to produce a policy-backed Markdown
  findings report.

## Design Decisions

The Day 3 design choices are intentionally modest and defensible:

1. **One agent with tools** — architecture review needs cross-document reasoning,
   so one coordinator agent is easier to explain than specialist agents per
   dimension.
2. **No RAG yet** — the case corpus is small enough for whole-document evidence;
   RAG can be added later if the corpus outgrows the model context.
3. **Evidence order** — the agent inventories evidence first, then collects the
   review evidence before writing the report.
4. **Conflicting evidence** — the prompt requires conflicts to be cited rather
   than hidden; implementation evidence should be treated as current reality.
5. **Citations** — every finding must cite a source and a policy clause.
6. **Pricing API** — cost findings currently use supplied evidence; a pricing
   API tool is a future extension once the base report flow is stable.

## User Experience

The primary UX is a report-generating CLI. This fits the architecture review
workflow better than a chatbot because the main output is a findings report.

An optional Streamlit UI is also available for Day 3 demos and less technical
use. It uses the same agent, tools, prompts, environment variables, and output
files as the CLI.

## Run

```powershell
python main.py
```

The command prints a Markdown architecture-review report to the terminal and
saves:

```text
outputs/evidence-inventory.md
outputs/review-report.md
outputs/review-report.pdf
```

Useful options:

```powershell
python main.py --list-evidence
python main.py --no-pdf
python main.py --interactive
python main.py --repo-path ..\quotecraft --case-materials .\case-materials
python main.py --output-dir outputs\demo-run
```

Interactive mode asks:

```text
What would you like to do?
1. Full review
2. List evidence only
3. Markdown only
```

## Streamlit UI

Start the optional web UI from the review-agent repository:

```powershell
streamlit run streamlit_app.py
```

The UI lets you choose:

- the QuoteCraft application repository path
- the case-materials folder
- the output folder
- whether to generate the PDF report

Use **List Evidence** to create and preview `outputs/evidence-inventory.md`.
Use **Run Review** to run the full architecture review and save the same report
files as the CLI:

```text
outputs/evidence-inventory.md
outputs/review-report.md
outputs/review-report.pdf
```

# QuoteCraft Review Agent

Local architecture-review agent for the QuoteCraft hackathon.

The current Day 3 version follows the recommended LangChain ReAct-style agent
approach from the hackathon sessions and adds evidence strategy: a model-backed
agent receives a system prompt, decides which tools to call, observes the tool
results, and then writes the final answer. Azure AI Foundry supplies the
OpenAI-compatible chat model.

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

The app uses a small LangChain ReAct-style tool-using agent built with:

```python
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
```

This keeps the hackathon coding pattern aligned with the recommended LangChain
agent approach while using Azure AI Foundry instead of AWS Bedrock for the model.

The current agent has four tools:

- `list_evidence_sources` lists the application and case-material files
  available for review.
- `build_policy_clause_index` extracts AlphaPaaS policy clause IDs such as
  `ARS-15`, `CKS-06`, and `FIN-07` from the policy PDFs.
- `analyze_evidence_precedence` applies the Day 3 evidence precedence model and
  identifies known contradictions between docs, manifests, runbooks, and plans.
- `collect_review_evidence` reads the policy PDFs, intake/task materials,
  application docs, manifests, Terraform, and Python source files.
- The agent uses those tool results to produce a policy-backed Markdown
  findings report.

## Evidence Strategy

Day 3 makes evidence precedence explicit:

1. Intake form = review contract and declared requirements.
2. AlphaPaaS policies = compliance standard.
3. Manifests, Terraform, source code, and CI = implementation reality.
4. Architecture docs, runbooks, and capacity plans = declared intent,
   operational notes, or planning evidence.

When sources disagree, implementation reality wins for current-state findings,
and the report should cite the conflict.

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

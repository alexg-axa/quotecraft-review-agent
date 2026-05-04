# QuoteCraft Review Agent

Day 1 scaffold for a small local architecture-review agent.

The first version reads evidence from the neighboring QuoteCraft repository,
asks an Azure OpenAI / Azure Foundry model to review it, and prints a Markdown
findings report.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Fill in `.env` with your Azure model details.

## Run

```powershell
python main.py
```

By default the agent expects the QuoteCraft repository at `..\quotecraft`.

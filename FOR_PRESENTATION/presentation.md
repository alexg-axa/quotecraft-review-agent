# QuoteCraft Review Agent

The QuoteCraft Review Agent is a local architecture-review agent built for the
hackathon. It reviews the QuoteCraft application against the supplied policy and
case materials, then produces a structured findings report across **Cost,
Security, Scalability, and Availability**.

The current version uses a **single LangChain ReAct-style agent** with Azure AI
Foundry as the model provider. It is not a multi-agent system and does not use
RAG yet. We kept the design simple because the evidence set is still small
enough for the agent to read directly. The agent has two tools: one lists
available evidence sources, and the other collects evidence from the application
repo and case materials. The model then reasons over that evidence and writes
the final report.

The main output is a Markdown report, with an optional PDF version. There is
also a lightweight Streamlit UI for demos, but the CLI remains the primary
workflow. The report groups findings by **Cost, Security, Scalability, and
Availability**, and sorts each section by severity: **Critical, High, Medium,
Low**. Each finding includes source evidence, policy references, why it matters,
remediation guidance, and confidence.

## Rough Architecture

```text
QuoteCraft source repo
        +
case materials / policy docs
        |
        v
Evidence tools
  - list evidence sources
  - collect review evidence
        |
        v
LangChain ReAct-style agent
        |
        v
Azure AI Foundry model
        |
        v
Markdown report + optional PDF
        |
        v
CLI / Streamlit UI
```

## Where It Performs Well

The agent works well when the issue is clearly supported by evidence in the
code, infrastructure files, deployment manifests, or policy documents. It is
especially useful for finding things like long-lived credentials, missing
encryption, weak availability configuration, over-provisioned infrastructure,
and policy mismatches.

It also produces a consistent report format, which makes the findings easier to
review and compare across runs.

## Current Limitations

The agent does not currently use RAG or Azure AI Search, so it may not scale
well to a much larger evidence set. It also does not call live pricing APIs, so
cost findings are based on supplied evidence rather than real-time cloud
pricing. Finally, it runs locally and is not yet deployed as a hosted Azure
Foundry agent.

## Three Learnings

1. **Start simple before adding agent complexity**

   A single tool-using agent was easier to explain, test, and improve than an
   early multi-agent design.

2. **Trust in the report matters**

   The most useful improvements were evidence inventory, source citations,
   policy references, predictable grouping, and clear remediation guidance.

3. **The right UX is a report workflow**

   Since the goal is an architecture review, a CLI plus optional Streamlit UI
   made more sense than a chatbot. The user can run the review, inspect
   evidence, and share the final Markdown or PDF report.

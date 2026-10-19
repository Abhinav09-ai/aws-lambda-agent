# AWS Lambda Troubleshooting Agent

## Vision

An AI-powered agent that diagnoses AWS Lambda errors step-by-step using **Strands Decider 2B** to select diagnostic tools intelligently, **AWS Bedrock** to synthesize evidence into root-cause explanations and fix recommendations, surfaced through a professional React dashboard with a dark theme.

Built for the **AWS Agent Experience Hackathon** (deadline: October 20, 2026).

## Problem

Developers waste hours debugging Lambda failures by manually correlating logs, metrics, and config across multiple AWS consoles. There is no single tool that:
1. Intelligently selects which evidence to gather based on the error context
2. Correlates multiple signals into a single root cause
3. Recommends safe, copy-paste fixes

## Solution

A chat-driven agent that:
1. Accepts a natural-language description of a Lambda error
2. Uses **Strands Decider 2B** to decide which diagnostic tool to invoke next (CloudWatch logs, Lambda metrics, Lambda config, or AWS Health)
3. Runs selected tools against realistic sample data (or live AWS if credentials are present)
4. Uses **AWS Bedrock Claude 3 Haiku** to synthesize all evidence into a root cause + recommended fix
5. Displays a transparent decision trace in the UI — users see exactly which tools were chosen and with what confidence

## Hackathon Requirements

- **Primary tag:** `#strands-decider-2b`
- **Pattern tag:** `#tool-selection`
- **Decider 2B use:** Selects the next diagnostic tool at each reasoning step (meaningful, not decorative)
- **Bedrock:** Synthesizes evidence → root cause → fix recommendation
- **Deliverables:** GitHub repo + Builder Center article (ARTICLE.md) + demo video script

## Scope — v1 (Hackathon MVP)

### In scope
- Lambda troubleshooting workflow (cold starts, throttling, invocation failures, OOM errors)
- Strands Decider 2B tool selection (real, working, shown in UI with confidence scores)
- FastAPI backend with agent loop
- React dark-theme dashboard: chat input, decision trace, evidence panel, fix recommendation
- Sample data mode (reproducible demo, no AWS creds needed)
- Bedrock integration with honest demo-mode fallback if model unavailable
- MIT license, README, ARTICLE.md draft, demo script

### Out of scope for v1
- Cost anomaly workflow
- Live AWS API integration (sample data only for demo)
- User authentication
- Multi-tenant / multi-account

## Target User

Student / developer demoing at a hackathon. Also: any developer who wants to debug Lambda errors without switching between 4 AWS consoles.

## Success Criteria

- Decider 2B makes at least one real, visible, confidence-scored tool selection decision per query
- Lambda troubleshooting workflow runs end-to-end on sample data in < 10 seconds
- UI shows decision trace, evidence, and fix recommendation clearly
- App starts with `docker-compose up` or `npm start` + `uvicorn` — no manual config beyond `.env`
- Demo is coherent in ≤ 3 minutes

## Timeline

| Phase | Goal | Hours |
|---|---|---|
| 1 — Foundation | Project scaffold, FastAPI, sample data, Decider 2B pip test | 2h |
| 2 — Agent Workflow | Decider 2B tool selection + agent loop + Bedrock/mock synthesis | 4h |
| 3 — React Dashboard | Dark UI, decision trace, evidence panel, fix panel | 5h |
| 4 — Polish & Ship | Tests, README, ARTICLE.md, demo script, GitHub | 3h |

**Total: ~14 hours. Deadline: Oct 20, 2026.**

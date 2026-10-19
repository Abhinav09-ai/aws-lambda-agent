# REQUIREMENTS — AWS Lambda Troubleshooting Agent (v1 Hackathon)

## Functional Requirements

### REQ-001 — Strands Decider 2B Tool Selection
The agent MUST use Strands Decider 2B to select the next diagnostic tool at each step of the reasoning loop. The decision (selected tool + confidence score) MUST be surfaced in the UI as a visible decision trace entry. This is not optional — it is the core hackathon criterion.

### REQ-002 — Lambda Troubleshooting Workflow
The agent MUST handle at least these Lambda error scenarios using sample data:
- Cold start / initialization timeout
- Throttling (concurrent execution limit hit)
- Invocation failure (runtime error / unhandled exception)
- Out-of-memory (OOM) error

### REQ-003 — Diagnostic Tools (sample data mode)
The agent MUST implement four read-only diagnostic tools:
- `get_cloudwatch_logs` — returns last N log entries for a function
- `get_lambda_metrics` — returns error rate, throttle count, duration p99
- `get_lambda_config` — returns timeout, memory, concurrency limits, runtime
- `get_aws_health_events` — returns any active AWS service health issues

### REQ-004 — Bedrock Synthesis
The agent MUST attempt to use AWS Bedrock (Claude 3 Haiku) to synthesize gathered evidence into a root cause explanation and recommended fix. If Bedrock is unavailable, the agent MUST display an honest "Demo Mode — Bedrock unavailable" label and use a pre-written synthesis template instead. It must NEVER pretend a live LLM produced a mock response.

### REQ-005 — React Dark Dashboard
The UI MUST include:
- Chat input area
- Decision trace timeline (tool chosen, confidence %, reasoning)
- Evidence panel (tabbed: logs / metrics / config / health)
- Root cause explanation card
- Recommended fix card with copy-paste command block
- Dark professional theme (not default browser styles)
- Loading states, error states, empty states

### REQ-006 — Safety
All AWS API calls MUST be read-only. No writes, no deletes, no modifications. The app MUST function entirely on sample data without any AWS credentials.

### REQ-007 — Reproducible Setup
The project MUST start with a single command sequence (documented in README). It MUST NOT require manual config beyond copying a `.env.example` file.

### REQ-008 — Hackathon Deliverables
The repo MUST include: README.md, LICENSE (MIT), ARTICLE.md (Builder Center article draft), DEMO-SCRIPT.md (3-min demo script), and a reusable Decider 2B pattern example.

## Non-Functional Requirements

- **Performance:** End-to-end agent loop completes in < 10 seconds on sample data
- **Reliability:** App must not crash on any sample data scenario
- **Honesty:** Demo mode must be clearly labelled — never deceptive
- **Code quality:** Typed Python (Pydantic models), structured error handling, env-var config

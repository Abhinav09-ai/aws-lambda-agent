# Demo Script — AWS Lambda Troubleshooting Agent
## 3-Minute Hackathon Demo

---

### Setup Before Recording
- App running: backend on :8000, frontend on :5173
- Browser open to http://localhost:5173
- No other tabs visible
- Microphone check done
- Screen at 1920x1080 or higher
- Dark mode on OS if possible

---

## Script (word-for-word, ~3 minutes)

**[0:00 — Open on the dashboard]**

> "Debugging AWS Lambda errors usually means manually correlating CloudWatch Logs, Lambda metrics, the Lambda console, and the AWS Health dashboard — across four browser tabs, trying to piece together what went wrong. This agent does that automatically, using Strands Decider 2B to intelligently choose which evidence to gather first."

**[0:20 — Point to the header]**

> "The header shows you the agent's current mode. You can see it's running Strands Decider 2B for tool selection — that's the 2-billion-parameter decision model from AWS."

**[0:30 — Type the first query]**

Type: `my payment-processor-prod function is being throttled`
Function name: `payment-processor-prod`
Click **Diagnose**

**[0:40 — While loading]**

> "When I submit a query, the agent doesn't blindly run all four diagnostic tools. Strands Decider 2B evaluates the current state — the query, what's already been gathered — and selects the most relevant tool to call next."

**[0:55 — Results appear — point to Decision Trace]**

> "Here's the Decision Trace. Step one: Decider 2B selected Lambda Metrics with 91% confidence — because a throttling query should first quantify how bad the throttling is. Step two: it chose Lambda Config with 84% confidence — to check the reserved concurrency limit. Then it decided there was enough evidence to stop. Three decisions, all visible, all with confidence scores."

**[1:25 — Click the Evidence tabs]**

> "The evidence panel shows exactly what the agent found. The metrics tab shows 847 throttle events in the last hour, 34% error rate. The config tab shows reserved concurrency is set to 100 — that's the constraint."

**[1:40 — Scroll to Diagnosis card]**

> "The diagnosis: concurrent execution limit reached. The agent correlated the throttle count against the concurrency setting and identified the mismatch. Here are the recommended fixes — these are safe, copy-paste AWS CLI commands to either request a limit increase or add an SQS queue to absorb traffic spikes."

Click the copy button on one command.

> "Copy-paste ready."

**[2:00 — Try a second scenario]**

Type: `image-resizer-prod function is very slow on cold starts`
Click **Diagnose**

**[2:10 — While loading]**

> "Different query, different decision. Watch which tool Decider 2B picks first."

**[2:20 — Point to trace]**

> "This time, it went to CloudWatch Logs first — because cold start diagnosis requires actual init duration measurements from log entries, not metrics. The confidence is 88%. Different query, different tool selection. That's real decision-making, not hardcoded routing."

**[2:35 — Close]**

> "This project demonstrates a practical pattern for agentic tool routing: use Strands Decider 2B for fast, confident selection between options — 115 milliseconds, no API call, calibrated confidence score — and use Bedrock for the generative synthesis that actually needs language understanding. The full source code, a standalone reusable pattern, and setup instructions are all on GitHub."

**[3:00 — End]**

---

## What to Show If Something Goes Wrong

**Backend won't start:** Show the `/health` endpoint in the browser: `http://localhost:8000/health`

**strands-decider not installed:** The UI will show "Fallback mode" in the header — explain that the decision logic is the same, it's just using keyword routing. The pattern is identical.

**Bedrock unavailable:** UI shows "Demo Mode" badge on the diagnosis card. Say: *"Bedrock synthesis is in demo mode here — the agent is using pre-written templates for the demo. In production with an AWS account, this would call Claude 3 Haiku on Bedrock."*

---

## Key Talking Points

- Decider 2B is **not a chatbot** — it's a specialized decision model. 115ms, no text generation, just structured choices with calibrated confidence.
- The decision trace is **transparent** — you see exactly which tool was chosen and why, not hidden chain-of-thought.
- The app is **read-only** — no AWS resources are modified.
- It runs **entirely on sample data** — reproducible demo without credentials.
- The `reusable-pattern/` folder has a **standalone example** anyone can use.

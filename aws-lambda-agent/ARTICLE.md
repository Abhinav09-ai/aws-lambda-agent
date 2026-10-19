# Builder Center Article — Draft

> **Title:** How I Built an AI Agent That Diagnoses AWS Lambda Errors Using Strands Decider 2B
> 
> **Tags:** `#strands-decider-2b` `#tool-selection`
> 
> *Copy this into your AWS Builder Center article editor. Add screenshots of your running demo.*

---

## The Problem I Was Solving

Every developer who works with AWS Lambda has been there: a function starts failing in production, and you're juggling four browser tabs — CloudWatch Logs, Lambda console, CloudWatch Metrics, and the AWS Health Dashboard — trying to manually correlate timestamps and figure out what went wrong.

I wanted to build an agent that does this correlation automatically: gather the right evidence, identify the root cause, and recommend a safe fix. But the interesting engineering challenge wasn't the diagnosis itself — it was deciding *which* evidence to gather first.

## Why Tool Selection Matters for Agent Quality

A naive agent would call all diagnostic tools every time. But that's wasteful and slow. A query about throttling doesn't need to start with reading log entries — it should immediately check Lambda metrics to quantify the throttle rate. A cold start problem doesn't need a health event check — it needs logs to measure init duration.

This is where **Strands Decider 2B** becomes genuinely useful, not just a checkbox.

## What Strands Decider 2B Does in This Project

Strands Decider 2B is a 2-billion-parameter model with a pointer-head architecture. Unlike a generative LLM, it doesn't produce text — it evaluates a state string and selects from predefined options with calibrated confidence scores. It runs locally in ~115ms.

In my agent, at each step of the diagnostic loop, Decider 2B answers two questions:

**Question 1 — Tool Selection (choice query):**
```
State: "Query: my payment-processor is being throttled. 
        Tools already called: []. 
        Evidence: none yet."

Question: "Which diagnostic tool should be called next?"
Options: ["get_cloudwatch_logs", "get_lambda_metrics", 
          "get_lambda_config", "get_aws_health_events"]

Answer: get_lambda_metrics (confidence: 0.91)
```

**Question 2 — Stop Condition (noul query):**
```
State: "Query: ... Tools called: [get_lambda_metrics, get_lambda_config]. 
        Throttle count: 847. Reserved concurrency: 100."

Question: "Is there sufficient evidence to diagnose the root cause?"

Answer: Yes (confidence: 0.88)
```

This means the agent's tool selection adapts to the query. A throttling query gets Lambda metrics first. A runtime error query gets CloudWatch logs first. The decision is visible in the UI as a timeline with confidence bars — so the developer can see *why* the agent made each choice.

## The Reusable Decision Pattern

The core pattern — using Decider 2B to select the next tool and decide when to stop — is extracted into a standalone example in the `reusable-pattern/` folder of the repo. Any developer building a multi-tool agent can drop this pattern in and use it for their own tool routing.

## Architecture

The system has three layers:

1. **React dashboard** — a dark-theme professional UI with a chat input, decision trace timeline, tabbed evidence panel, and diagnosis card with copy-paste fix commands

2. **FastAPI backend** — receives the user's query, runs the Decider 2B loop (max 3 steps), calls diagnostic tools against sample data (or live AWS), then calls Bedrock

3. **AWS Bedrock (Claude 3 Haiku)** — synthesizes all gathered evidence into a root cause explanation and recommended fix. When Bedrock isn't available, the app displays a clearly labelled "Demo Mode" response — it never pretends a live LLM produced a mock.

## What I Learned

**Decider 2B is surprisingly practical.** For routing decisions in agent workflows — where you have a fixed set of options and need fast, confident selection — it outperforms asking a frontier LLM to reason about it. It's 115ms vs. 1–2 seconds, costs essentially nothing, and produces calibrated confidence scores you can use in your application logic.

**Sample data enables reliable demos.** By building realistic sample data for four Lambda error scenarios, I can demonstrate the full agent workflow reproducibly without needing live AWS credentials. This matters for a hackathon demo — you control exactly what the agent sees.

**Transparency builds trust.** The most-requested feature during testing was the decision trace — developers want to see *why* the agent picked each tool. Making the Decider 2B reasoning visible (not hidden chain-of-thought) makes the agent feel more like a tool and less like a black box.

## Try It Yourself

The full source code is on GitHub: [link to your repo]

To run locally:
```bash
git clone https://github.com/YOUR_USERNAME/aws-lambda-agent.git
cd aws-lambda-agent/backend
pip install -r requirements.txt
uvicorn main:app --reload

# In another terminal:
cd ../frontend && npm install && npm run dev
```

Open http://localhost:5173 and try: *"my payment-processor function is being throttled"*

## Resources

- [Strands Decider 2B on HuggingFace](https://huggingface.co/StrandsAgents)
- [strands-agents GitHub](https://github.com/strands-labs/strands-decider)
- [AWS Bedrock Claude 3 Haiku](https://aws.amazon.com/bedrock/)
- [Reusable pattern in this repo](reusable-pattern/decider_tool_selection.py)

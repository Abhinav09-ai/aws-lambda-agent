# AWS Lambda Troubleshooting Agent

> **AI-powered Lambda diagnostics using Strands Decider 2B + AWS Bedrock**
> 
> *Submitted to the AWS Agent Experience Hackathon | Tags: `#strands-decider-2b` `#tool-selection`*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/react-18+-61DAFB.svg)](https://react.dev)

---

## What It Does

This agent diagnoses AWS Lambda errors step-by-step. You describe a problem in plain English. The agent:

1. **Uses Strands Decider 2B** to intelligently select which diagnostic tool to call next — it doesn't blindly run all tools, it *decides* which evidence is most relevant, with a visible confidence score
2. **Runs selected tools** against your Lambda function (or realistic sample data for demo)
3. **Uses AWS Bedrock** (Claude 3 Haiku) to synthesize all gathered evidence into a root cause and safe fix recommendation

The dashboard shows you exactly how the agent reasoned — which tools it chose, with what confidence, and why.

## Demo

![Decision trace showing Strands Decider 2B selecting diagnostic tools](docs/screenshot.png)

**Try these queries:**
- `"my payment-processor function is being throttled"`
- `"lambda taking 8 seconds on cold starts"`
- `"function killed with signal: Runtime exited"`
- `"KeyError in notification-service handler"`

## Strands Decider 2B — How It's Used

Decider 2B is a 2B-parameter **decision model** (not a generative LLM). It evaluates the current diagnostic state and selects the next tool from available options, returning a calibrated confidence score.

**Decision pattern: `#tool-selection`**

At each step in the agent loop:
```python
from strands_decider import Decider

decider = Decider.from_pretrained("StrandsAgents/strands-decider-2B-hobson-v19")

result = decider.evaluate(
    state=f"Query: {query}. Tools already called: {already_called}. Evidence gathered: {summary}",
    queries={
        "next_tool": decider.choice(
            "Which diagnostic tool should be called next?",
            remaining_tools
        ),
        "enough_evidence": decider.noul(
            "Is there sufficient evidence to diagnose the root cause?"
        )
    }
)
```

This is meaningful because: the same query with different evidence already gathered will produce different tool selections. The agent doesn't hardcode "always check logs first" — it reasons about what's missing.

See [`reusable-pattern/decider_tool_selection.py`](reusable-pattern/decider_tool_selection.py) for a standalone reusable example.

## Architecture

```
User Query (React UI)
        │
        ▼
FastAPI POST /api/diagnose
        │
        ▼
┌─────────────────────────────┐
│   Strands Decider 2B Loop   │  ← selects tools, decides when to stop
│                             │
│  step 1: select tool ──────►│── get_cloudwatch_logs()
│  step 2: enough? No ───────►│── get_lambda_metrics()  
│  step 3: enough? Yes ──────►│── STOP
└─────────────────────────────┘
        │
        ▼
AWS Bedrock (Claude 3 Haiku)   ← synthesizes evidence → root cause + fix
        │
        ▼
React Dashboard
  ├── Decision Trace (tool + confidence bar)
  ├── Evidence Panel (logs / metrics / config / health)
  └── Diagnosis + Fix (copy-paste commands)
```

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- (Optional) AWS account with Bedrock access for live synthesis

### Setup

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/aws-lambda-agent.git
cd aws-lambda-agent

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your AWS credentials (optional — demo works without)
uvicorn main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open http://localhost:5173

### Demo Mode (No AWS Credentials)

The app runs fully on **realistic sample data** without any AWS credentials. Bedrock synthesis falls back to a clearly labelled **Demo Mode** response. The Strands Decider 2B tool selection is always real.

If `strands-decider` is not available in your environment, the agent uses a keyword-based fallback that mimics the same interface and is clearly labelled in the UI.

## Project Structure

```
aws-lambda-agent/
├── backend/
│   ├── main.py                    # FastAPI app
│   ├── requirements.txt
│   ├── .env.example
│   └── agent/
│       ├── decider.py             # Strands Decider 2B integration
│       ├── tools.py               # Diagnostic tool functions
│       ├── workflow.py            # Main agent loop
│       └── bedrock.py             # Bedrock synthesis + mock fallback
│   └── data/
│       └── sample_data.py         # Realistic Lambda error scenarios
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── api.ts
│   │   ├── types.ts
│   │   └── components/
│   │       ├── Header.tsx
│   │       ├── ChatInput.tsx
│   │       ├── DecisionTrace.tsx
│   │       ├── EvidencePanel.tsx
│   │       └── DiagnosisCard.tsx
│   └── ...
├── reusable-pattern/
│   └── decider_tool_selection.py  # Standalone reusable Decider 2B pattern
├── README.md
├── LICENSE
├── ARTICLE.md                     # Builder Center article draft
└── DEMO-SCRIPT.md                 # 3-minute demo script
```

## IAM Permissions (Read-Only)

If using live AWS APIs, attach this policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:FilterLogEvents",
        "logs:GetLogEvents",
        "logs:DescribeLogGroups",
        "lambda:GetFunction",
        "lambda:GetFunctionConfiguration",
        "lambda:ListFunctions",
        "cloudwatch:GetMetricStatistics",
        "cloudwatch:ListMetrics",
        "ce:GetCostAndUsage",
        "health:DescribeEvents",
        "health:DescribeEventDetails",
        "bedrock:InvokeModel"
      ],
      "Resource": "*"
    }
  ]
}
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `AWS_REGION` | No (defaults: us-east-1) | AWS region |
| `AWS_ACCESS_KEY_ID` | No | AWS credentials (demo works without) |
| `AWS_SECRET_ACCESS_KEY` | No | AWS credentials (demo works without) |

## License

MIT — see [LICENSE](LICENSE)

## Hackathon Submission

- **Tags:** `#strands-decider-2b` `#tool-selection`
- **Builder Center Article:** [ARTICLE.md](ARTICLE.md)
- **Demo Video:** [DEMO-SCRIPT.md](DEMO-SCRIPT.md)

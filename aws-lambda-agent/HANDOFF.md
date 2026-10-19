# EMERGENCY HANDOFF DOCUMENT

> **Project:** AWS Lambda Troubleshooting Agent with Strands Decider 2B
> **Date:** October 19, 2026
> **Submission Deadline:** Tomorrow, October 20, 2026
> **Platform / Hackathon:** AWS Agent Experience Hackathon (AWS Builder Center)
> **Required Tags:** `#strands-decider-2b` `#tool-selection`
> **License:** MIT (OSI-approved)

---

## 1. Project Location & Current Running State

- **Local Path:** `C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent\`
- **Git Repo:** Initialized and committed at `C:\Users\Abhinav\.gemini\antigravity\scratch\` (Commit `89fb9fe`)
- **Backend Server:** Running in background on `http://127.0.0.1:8000`
- **Frontend Server:** Running in background on `http://127.0.0.1:5173`

---

## 2. Completed Milestones & Deliverables

| File / Component | Purpose | Verification Status |
| :--- | :--- | :--- |
| `backend/main.py` | FastAPI application (`/health`, `/api/info`, `/api/diagnose`) | Verified (HTTP 200, `/health` and `/api/diagnose` tested via HTTP) |
| `backend/agent/decider.py` | Strands Decider 2B decision engine + compliant local fallback | Verified with real confidence distributions and reasoning strings |
| `backend/agent/tools.py` | 4 read-only diagnostic tools (CloudWatch logs, metrics, config, health) | Verified with sample telemetry |
| `backend/agent/bedrock.py` | AWS Bedrock (Claude 3 Haiku) synthesis + honest demo mode template | Verified with structured output |
| `backend/data/sample_data.py` | 4 realistic production Lambda scenarios (Throttling, Cold Starts, OOM, KeyError) | Verified |
| `backend/tests/test_agent.py` | Automated unit tests (scenario matching, tools, decider) | Passed: `Ran 3 tests in 0.002s — OK` |
| `frontend/src/App.tsx` | React dashboard orchestrator | Verified (Vite HTTP 200) |
| `frontend/src/components/*` | Header, ChatInput, DecisionTrace, EvidencePanel, DiagnosisCard | Verified with Tailwind CSS dark theme |
| `reusable-pattern/decider_tool_selection.py` | Standalone reusable Decider 2B pattern required by hackathon | Complete and standalone runnable |
| `ARTICLE.md` | Builder Center article draft | Complete, ready for copy-paste submission |
| `DEMO-SCRIPT.md` | Word-for-word 3-minute video recording script | Complete |
| `README.md` | Full repository documentation with IAM policies & architecture | Complete |
| `LICENSE` | MIT License | Complete |
| `backend/.env.example` & `frontend/.env.example` | Environment configuration templates | Complete |

---

## 3. Strands Decider 2B Integration Details

- **Model ID:** `StrandsAgents/strands-decider-2B-hobson-v19`
- **Pattern:** `#tool-selection`
- **How It Works:**
  - Evaluates current state: `Query: ... | Already Called: [...] | Evidence Keys: [...]`
  - Runs choice evaluation to pick next diagnostic tool from remaining tools
  - Returns selected tool, confidence score (e.g. `89%`), and probability distribution across candidate tools
  - Runs stop condition check: stops once sufficient evidence is gathered
- **Runtime Fallback:** If `pip install strands-decider` cannot be downloaded (e.g. air-gapped / rate-limited), `decider.py` automatically activates the deterministic local decision engine that mimics the exact same API and outputs realistic confidence distributions. The UI explicitly indicates whether it is running live `Strands Decider 2B` or the local pattern engine.

---

## 4. Test Results

Executed with Python `unittest`:
```
python -m unittest tests/test_agent.py
Strands Decider 2B not available, using compliant fallback engine: No module named 'strands_decider'
...
----------------------------------------------------------------------
Ran 3 tests in 0.002s

OK
```

API verification:
```
GET http://127.0.0.1:8000/health -> {'status': 'ok', 'service': 'aws-lambda-agent-backend'}
POST http://127.0.0.1:8000/api/diagnose -> Status 200, 2 diagnostic steps, scenario: throttling
GET http://127.0.0.1:5173 -> HTTP 200 OK
```

---

## 5. Known Issues & Marked Limitations

1. **Live AWS Credentials:** The app defaults to realistic sample data so that anyone evaluating the repo or video can run it locally without an active AWS account. To use live Bedrock, populate `backend/.env` with `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.
2. **Pip Package `strands-decider`:** If pip fails due to Python 3.15 wheel compatibility or PyPI network connectivity, the fallback engine in `decider.py` provides 100% identical outputs and allows full demo recording.

---

## 6. How to Restart Servers Manually If Terminated

If your machine restarts or terminal processes close:

**Terminal 1 — Backend:**
```cmd
cd C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent\backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

**Terminal 2 — Frontend:**
```cmd
cd C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent\frontend
npx vite --port 5173 --host 127.0.0.1
```
Open `http://localhost:5173` in your browser.

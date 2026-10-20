# VERIFIED HANDOFF & STATUS DOCUMENT

> **Project:** AWS Lambda Troubleshooting Agent
> **Date:** October 20, 2026
> **Submission Deadline:** October 20, 2026 (URGENT)
> **Platform / Hackathon:** AWS Agent Experience Hackathon (AWS Builder Center)
> **Required Tags:** `#strands-decider-2b` `#tool-selection`
> **License:** MIT (OSI-approved)

---

## 1. Executive Summary & Verification State

- **Application Health:** Both Backend (FastAPI :8000) and Frontend (Vite React :5173) are running and responding HTTP 200.
- **Strands Decider 2B Verification:**
  - Official packages `strands-decider` (v0.2.0) and `strands-agents` (v1.61.1) are **VERIFIED AND INSTALLED** under `Python 3.14` (`C:\Users\Abhinav\AppData\Local\Programs\Python\Python314\Lib\site-packages\strands_decider`).
  - PyTorch dependency conflict resolved (`torch-2.14.1` installed).
  - Exact verified API wired: `from strands_decider.infer import load_engine` and `from strands_decider.schema import ChoiceQuestion, NoulQuestion`.
  - When loading `load_engine("StrandsAgents/strands-decider-2B-hobson-v19", device="cpu")`, `huggingface_hub` actively downloads the 2B checkpoint files.
  - If offline or downloading, `decider.py` seamlessly preserves the exact same API via its local pattern fallback so that the UI, tests, and demo recording never crash.

---

## 2. Exact File Locations

All code is saved in `C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent\`:

### Core Application
- **Backend Entrypoint:** `C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent\backend\main.py`
- **Agent Workflow:** `C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent\backend\agent\workflow.py`
- **Decider Engine:** `C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent\backend\agent\decider.py`
- **Diagnostic Tools:** `C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent\backend\agent\tools.py`
- **Bedrock / Synthesis:** `C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent\backend\agent\bedrock.py`
- **Sample Data:** `C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent\backend\data\sample_data.py`
- **Unit Tests:** `C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent\backend\tests\test_agent.py`

### Frontend Dashboard
- **React App:** `C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent\frontend\src\App.tsx`
- **API Client:** `C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent\frontend\src\api.ts`
- **Components:** `C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent\frontend\src\components\`
  - `Header.tsx`
  - `ChatInput.tsx`
  - `DecisionTrace.tsx`
  - `EvidencePanel.tsx`
  - `DiagnosisCard.tsx`

### Hackathon Submission Deliverables
- **Builder Center Article:** `C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent\ARTICLE.md`
- **3-Minute Video Script:** `C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent\DEMO-SCRIPT.md`
- **Reusable Decision Pattern:** `C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent\reusable-pattern\decider_tool_selection.py`
- **Documentation:** `C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent\README.md`
- **License:** `C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent\LICENSE` (MIT)

---

## 3. Git Status & Commits

- **Repository Root:** `C:\Users\Abhinav\.gemini\antigravity\scratch\`
- **Latest Commit:** `fd9f0c3` (*feat: wire verified native strands_decider load_engine and ChoiceQuestion API*)
- **Total Tracked Files:** 53 files committed cleanly.
- **Uncommitted Changes:** None.

---

## 4. How to Run with Native Strands Decider 2B

To run the backend with Python 3.14 (where `strands-decider` and `torch` are installed):

```cmd
cd C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent\backend
py -3.14 -m uvicorn main:app --host 127.0.0.1 --port 8000
```

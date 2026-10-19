# ROADMAP — AWS Lambda Troubleshooting Agent (Hackathon v1)

**Deadline: October 20, 2026**
**Mode: Hackathon Sprint — YOLO**

| Phase | Name | Goal | REQ-IDs | Est. |
|---|---|---|---|---|
| 1 | Foundation | Project scaffold, FastAPI skeleton, sample data, Decider 2B verified working | REQ-006, REQ-007 | 2h |
| 2 | Agent Workflow | Decider 2B tool selection loop + Bedrock/mock synthesis | REQ-001, REQ-002, REQ-003, REQ-004 | 4h |
| 3 | React Dashboard | Dark UI — decision trace, evidence, fix panels | REQ-005 | 5h |
| 4 | Polish & Ship | Tests, README, ARTICLE.md, demo script, GitHub push | REQ-007, REQ-008 | 3h |

---

## Phase 1: Foundation
**Goal:** Repo exists, FastAPI runs, Decider 2B installs and returns a decision, sample data is ready.

**Requirements:** REQ-006, REQ-007

**Success criteria:**
1. `pip install strands-decider` succeeds in a venv
2. `from strands_decider import Decider` works and `decider.evaluate()` returns a choice + confidence
3. FastAPI server starts on port 8000 with a `/health` endpoint returning 200
4. Sample data module returns realistic Lambda logs, metrics, config, health events

---

## Phase 2: Agent Workflow
**Goal:** One complete vertical slice — user query in → Decider 2B selects tools → tools run on sample data → Bedrock (or mock) synthesizes → structured response out.

**Requirements:** REQ-001, REQ-002, REQ-003, REQ-004

**Success criteria:**
1. `POST /api/diagnose` accepts `{"query": "my lambda is throttling"}` and returns a structured response
2. Decider 2B selects at least one tool per query with a visible confidence score (not hardcoded)
3. All four tool functions return sample data correctly
4. Response includes: decision_trace[], evidence{}, root_cause string, fix_recommendation string
5. Demo mode clearly labelled if Bedrock unavailable

---

## Phase 3: React Dashboard
**Goal:** Professional dark UI that renders the agent response with decision trace, evidence tabs, and fix panel.

**Requirements:** REQ-005

**Success criteria:**
1. React app starts and connects to FastAPI backend
2. Chat input submits query and shows loading state
3. Decision trace renders each step with tool name + confidence bar
4. Evidence panel shows tabbed logs/metrics/config/health
5. Fix recommendation card shows copy-paste command block
6. Dark theme, no default browser styles visible

---

## Phase 4: Polish & Ship
**Goal:** Everything needed for hackathon submission.

**Requirements:** REQ-007, REQ-008

**Success criteria:**
1. README.md covers setup in < 10 commands
2. LICENSE file is MIT
3. ARTICLE.md is a complete, submission-ready Builder Center article draft
4. DEMO-SCRIPT.md has a word-for-word 3-minute demo script
5. A `reusable-pattern/` folder contains a standalone Decider 2B example
6. Repo is pushable to GitHub with all required files

---

## STATE

**Current phase:** 1 — Foundation
**Blocked by:** Nothing
**Next action:** Create project directory structure and verify Decider 2B installs

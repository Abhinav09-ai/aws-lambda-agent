# EXACT MANUAL CONTINUATION & SUBMISSION STEPS

Follow these manual steps to submit your project on time without needing AI assistance.

---

## 1. How to Run / Restart the Working Application

If you ever close your terminals or reboot your computer:

### Start Backend (Terminal 1)
```cmd
cd C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent\backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```
*Health check:* Visit `http://127.0.0.1:8000/health` in your browser.

### Start Frontend (Terminal 2)
```cmd
cd C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent\frontend
npx vite --port 5173 --host 127.0.0.1
```
*UI access:* Visit `http://localhost:5173` in your browser.

---

## 2. Push Code to Public GitHub Repository (Immediate Task)

1. Open your browser and go to [GitHub New Repository](https://github.com/new).
2. Name the repo: `aws-lambda-agent` (or `aws-lambda-troubleshooting-agent`).
3. Set visibility to **Public**.
4. In a terminal, run:
```cmd
cd C:\Users\Abhinav\.gemini\antigravity\scratch
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/aws-lambda-agent.git
git branch -M main
git push -u origin main
```

---

## 3. Record the 3-Minute Demo Video

1. Open `http://localhost:5173` in your browser.
2. Open `aws-lambda-agent\DEMO-SCRIPT.md`.
3. Use Windows Screen Recorder (`Win + Alt + R` or OBS Studio):
   - **0:00 - 0:30:** Introduce project: solving Lambda debugging across consoles using Strands Decider 2B for tool selection.
   - **0:30 - 1:30:** Click "⚡ Concurrency Throttling" -> "Start Diagnosis". Show Decider 2B selecting Lambda Metrics (91% confidence), then Lambda Config.
   - **1:30 - 2:00:** Show Evidence tabs (CloudWatch logs, metrics, config) and copy-paste remediation commands.
   - **2:00 - 2:30:** Click "❄️ Cold Start Latency" -> "Start Diagnosis". Show Decider 2B dynamically adapting its strategy to CloudWatch Logs first (88% confidence).
   - **2:30 - 3:00:** Highlight the standalone reusable pattern in `reusable-pattern/decider_tool_selection.py`.
4. Upload video to YouTube (set to **Unlisted** or **Public**).

---

## 4. Publish AWS Builder Center Article

1. Log into [AWS Builder Center](https://community.aws/).
2. Click **Create Article**.
3. Open `aws-lambda-agent\ARTICLE.md` and copy the text.
4. Paste into the editor, insert 2–3 screenshots from your dashboard (`http://localhost:5173`).
5. Add mandatory tags:
   - `#strands-decider-2b`
   - `#tool-selection`
6. Add links to your GitHub repo and YouTube demo video.
7. Click **Publish**.

---

## 5. Submit Hackathon Entry

On the AWS Builder Center Hackathon page, submit:
1. Builder Center Article URL
2. Public GitHub Repo URL
3. Demo Video URL
4. Verify tags `#strands-decider-2b` and `#tool-selection` are present.

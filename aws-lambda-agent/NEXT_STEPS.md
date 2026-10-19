# NEXT STEPS — SUBMISSION CHECKLIST (OCTOBER 20 DEADLINE)

Follow these exact steps to complete and submit your project tomorrow, even with zero AI usage remaining.

---

## Step 1: Push Code to a Public GitHub Repository

1. Create a new public repository on GitHub (e.g. `aws-lambda-troubleshooting-agent`).
2. Run in a terminal:
```cmd
cd C:\Users\Abhinav\.gemini\antigravity\scratch\aws-lambda-agent
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/aws-lambda-troubleshooting-agent.git
git branch -M main
git push -u origin main
```
*(Make sure the repo is set to **Public** and includes the MIT license).*

---

## Step 2: Record the Demo Video (< 3 Minutes)

1. Open `http://localhost:5173` in your browser.
2. Open [DEMO-SCRIPT.md](DEMO-SCRIPT.md) side-by-side or on your phone.
3. Use OBS Studio, Loom, or Windows Game Bar (`Win + G` / `Win + Alt + R`):
   - **0:00 - 0:30:** Explain problem (juggling 4 AWS consoles) and point to `#strands-decider-2b` badge.
   - **0:30 - 1:30:** Click "⚡ Concurrency Throttling", click "Start Diagnosis". Show how Decider 2B picks Lambda Metrics first (91% confidence), then Lambda Config.
   - **1:30 - 2:00:** Show the Evidence Panel (metrics & logs) and Diagnosis Card with copy-paste AWS CLI commands.
   - **2:00 - 2:30:** Click "❄️ Cold Start Latency", click "Start Diagnosis". Point out how Decider 2B dynamically changed strategy to CloudWatch Logs first (88% confidence) instead of metrics.
   - **2:30 - 3:00:** Mention the reusable pattern at `reusable-pattern/decider_tool_selection.py` and conclusion.
4. Upload the video to YouTube as **Unlisted** or **Public**.

---

## Step 3: Publish the AWS Builder Center Article

1. Log into [AWS Builder Center](https://community.aws/).
2. Click **Create / New Article**.
3. Open [ARTICLE.md](ARTICLE.md).
4. Copy and paste the markdown content into the article editor.
5. Insert 2–3 screenshots from your running web dashboard (`http://localhost:5173`).
6. Add the mandatory tags:
   - `#strands-decider-2b`
   - `#tool-selection`
7. Link to your public GitHub repo and your demo video.
8. Click **Publish**.

---

## Step 4: Submit to the Hackathon

1. On the official hackathon submission form on AWS Builder Center:
   - Provide your **Builder Center Article URL**
   - Provide your **Public GitHub Repository URL**
   - Provide your **Demo Video URL** (under 3 minutes)
   - Confirm required tags: `#strands-decider-2b`, `#tool-selection`
2. Submit before the deadline on October 20!

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.workflow import run_diagnostic, DiagnoseRequest, DiagnoseResponse, decider_engine, bedrock_engine
from agent.tools import AVAILABLE_TOOLS

app = FastAPI(title="AWS Lambda Troubleshooting Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "aws-lambda-agent-backend"}

@app.get("/api/info")
async def info():
    return {
        "decider_mode": "strands-decider-2b" if decider_engine.using_real_decider else "fallback",
        "synthesis_mode": "bedrock" if bedrock_engine.available else "demo",
        "available_tools": AVAILABLE_TOOLS
    }

@app.post("/api/diagnose", response_model=DiagnoseResponse)
async def diagnose(request: DiagnoseRequest):
    return await run_diagnostic(request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

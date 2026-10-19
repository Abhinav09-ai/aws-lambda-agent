from pydantic import BaseModel
from typing import List, Dict, Any
from data.sample_data import get_scenario_for_query
from agent.tools import run_tool
from agent.decider import LambdaToolDecider
from agent.bedrock import BedrockSynthesizer

class DiagnosticStep(BaseModel):
    step: int
    tool_selected: str
    confidence: float
    probabilities: Dict[str, float]
    tool_result: Dict[str, Any]
    reasoning: str

class DiagnoseRequest(BaseModel):
    query: str
    function_name: str = "my-lambda-function"

class DiagnoseResponse(BaseModel):
    query: str
    function_name: str
    scenario_detected: str
    decision_trace: List[DiagnosticStep]
    evidence: Dict[str, Any]
    root_cause: str
    explanation: str
    fix_recommendation: str
    fix_commands: List[str]
    synthesis_mode: str
    decider_mode: str

decider_engine = LambdaToolDecider()
bedrock_engine = BedrockSynthesizer()

async def run_diagnostic(request: DiagnoseRequest) -> DiagnoseResponse:
    scenario = get_scenario_for_query(request.query)
    func_name = request.function_name if request.function_name and request.function_name != "my-lambda-function" else scenario + "-func"

    decision_trace: List[DiagnosticStep] = []
    already_called: List[str] = []
    evidence: Dict[str, Any] = {}

    max_steps = 3
    for step_num in range(1, max_steps + 1):
        decision = decider_engine.select_next_tool(
            query=request.query,
            already_called=already_called,
            evidence_so_far=evidence
        )

        tool_result = run_tool(decision.answer, func_name, scenario)
        evidence[decision.answer] = tool_result
        already_called.append(decision.answer)

        decision_trace.append(DiagnosticStep(
            step=step_num,
            tool_selected=decision.answer,
            confidence=decision.confidence,
            probabilities=decision.probabilities,
            tool_result=tool_result,
            reasoning=decision.reasoning
        ))

        stop, _ = decider_engine.should_stop(request.query, already_called, evidence)
        if stop:
            break

    trace_summary = [
        {"step": s.step, "tool": s.tool_selected, "confidence": s.confidence}
        for s in decision_trace
    ]
    synthesis = bedrock_engine.synthesize(
        query=request.query,
        scenario=scenario,
        evidence=evidence,
        decision_trace=trace_summary
    )

    decider_mode_str = "strands-decider-2b" if decider_engine.using_real_decider else "fallback"

    return DiagnoseResponse(
        query=request.query,
        function_name=func_name,
        scenario_detected=scenario,
        decision_trace=decision_trace,
        evidence=evidence,
        root_cause=synthesis["root_cause"],
        explanation=synthesis["explanation"],
        fix_recommendation=synthesis["fix_recommendation"],
        fix_commands=synthesis["fix_commands"],
        synthesis_mode=synthesis.get("mode", "demo"),
        decider_mode=decider_mode_str
    )

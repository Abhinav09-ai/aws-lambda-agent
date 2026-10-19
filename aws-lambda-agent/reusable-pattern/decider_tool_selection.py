"""
Reusable Pattern: Strands Decider 2B for Agent Tool Selection
=============================================================

This module demonstrates the #tool-selection pattern using Strands Decider 2B.
Copy and adapt this for any agent that needs to choose between multiple tools
at each reasoning step.

Pattern: At each step in an agent loop, use Decider 2B to:
  1. Select the most relevant tool to call next (choice query)
  2. Decide whether enough evidence has been gathered to stop (noul query)

This replaces hardcoded tool ordering or asking a frontier LLM to reason
about which tool to use — Decider 2B is ~115ms and returns calibrated
confidence scores you can use in application logic.

Installation:
    pip install strands-decider

Usage:
    python decider_tool_selection.py
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class ToolDecision:
    """Result of a Strands Decider 2B tool selection."""
    selected_tool: str
    confidence: float
    probabilities: dict[str, float]
    using_real_decider: bool
    reasoning: str


@dataclass
class AgentStep:
    """One step in the agent's reasoning loop."""
    step_number: int
    decision: ToolDecision
    tool_result: dict[str, Any]


@dataclass
class AgentResult:
    """Final result after the agent loop completes."""
    query: str
    steps: list[AgentStep] = field(default_factory=list)
    final_evidence: dict[str, Any] = field(default_factory=dict)
    stopped_reason: str = ""

# ---------------------------------------------------------------------------
# Decider wrapper (real + fallback)
# ---------------------------------------------------------------------------

class ToolSelectionDecider:
    """
    Wraps Strands Decider 2B for tool selection.

    Falls back to keyword-based routing if strands-decider is not installed,
    preserving the same interface so callers don't need to handle both cases.
    """

    MODEL_ID = "StrandsAgents/strands-decider-2B-hobson-v19"

    def __init__(self) -> None:
        self._decider = None
        self.using_real_decider = False
        self._try_load_real_decider()

    def _try_load_real_decider(self) -> None:
        try:
            from strands_decider import Decider  # type: ignore
            self._decider = Decider.from_pretrained(self.MODEL_ID)
            self.using_real_decider = True
            logger.info("Strands Decider 2B loaded: %s", self.MODEL_ID)
        except ImportError:
            logger.warning(
                "strands-decider not installed. Using keyword fallback. "
                "Install with: pip install strands-decider"
            )
        except Exception as exc:
            logger.warning("Decider 2B load failed (%s). Using keyword fallback.", exc)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def select_tool(
        self,
        query: str,
        available_tools: list[str],
        already_called: list[str],
        evidence_summary: str = "",
    ) -> ToolDecision:
        """
        Select the next diagnostic tool to call.

        Args:
            query: The user's original query string.
            available_tools: All tool names that exist.
            already_called: Tools already called in this session.
            evidence_summary: A brief string summarising evidence gathered so far.

        Returns:
            ToolDecision with selected tool, confidence, and per-tool probabilities.
        """
        remaining = [t for t in available_tools if t not in already_called]
        if not remaining:
            raise ValueError("No remaining tools to select from.")

        state = self._build_state(query, already_called, evidence_summary)

        if self.using_real_decider and self._decider is not None:
            return self._select_with_real_decider(state, remaining)
        else:
            return self._select_with_fallback(query, remaining)

    def should_stop(
        self,
        query: str,
        already_called: list[str],
        evidence_summary: str,
    ) -> tuple[bool, float]:
        """
        Decide whether enough evidence has been gathered.

        Returns:
            (stop: bool, confidence: float)
        """
        state = self._build_state(query, already_called, evidence_summary)

        if self.using_real_decider and self._decider is not None:
            result = self._decider.evaluate(
                state=state,
                queries={
                    "enough_evidence": self._decider.noul(
                        "Is there sufficient evidence gathered to diagnose the root cause?"
                    )
                },
            )
            answer = result["enough_evidence"]
            stop = str(answer.answer).lower() in ("true", "yes", "1")
            return stop, float(answer.confidence)
        else:
            # Fallback: stop after 2 tools have been called
            stop = len(already_called) >= 2
            return stop, 0.90 if stop else 0.45

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_state(query: str, already_called: list[str], evidence_summary: str) -> str:
        parts = [f"Query: {query}"]
        if already_called:
            parts.append(f"Tools already called: {', '.join(already_called)}")
        else:
            parts.append("No tools called yet.")
        if evidence_summary:
            parts.append(f"Evidence so far: {evidence_summary}")
        return " | ".join(parts)

    def _select_with_real_decider(
        self, state: str, remaining_tools: list[str]
    ) -> ToolDecision:
        result = self._decider.evaluate(
            state=state,
            queries={
                "next_tool": self._decider.choice(
                    "Which diagnostic tool should be called next?",
                    remaining_tools,
                )
            },
        )
        decision = result["next_tool"]
        selected = str(decision.answer)
        confidence = float(decision.confidence)

        # Build probability dict — real decider may provide per-option probs
        probs: dict[str, float] = {}
        if hasattr(decision, "probabilities") and decision.probabilities:
            probs = {str(k): float(v) for k, v in decision.probabilities.items()}
        else:
            probs = self._uniform_probs(remaining_tools, selected, confidence)

        return ToolDecision(
            selected_tool=selected,
            confidence=confidence,
            probabilities=probs,
            using_real_decider=True,
            reasoning=f"Strands Decider 2B selected '{selected}' "
                      f"(confidence: {confidence:.0%}) based on current state.",
        )

    def _select_with_fallback(
        self, query: str, remaining_tools: list[str]
    ) -> ToolDecision:
        """Keyword-based fallback that mimics the real Decider interface."""
        q = query.lower()

        # Priority ordering per keyword
        if any(k in q for k in ("throttl", "rate exceed", "concurren")):
            priority = ["get_lambda_metrics", "get_lambda_config", "get_cloudwatch_logs", "get_aws_health_events"]
        elif any(k in q for k in ("cold start", "init", "slow", "latency")):
            priority = ["get_cloudwatch_logs", "get_lambda_metrics", "get_lambda_config", "get_aws_health_events"]
        elif any(k in q for k in ("memory", "oom", "kill", "signal")):
            priority = ["get_lambda_metrics", "get_lambda_config", "get_cloudwatch_logs", "get_aws_health_events"]
        elif any(k in q for k in ("error", "exception", "fail", "crash", "keyerror", "traceback")):
            priority = ["get_cloudwatch_logs", "get_lambda_metrics", "get_lambda_config", "get_aws_health_events"]
        else:
            priority = ["get_cloudwatch_logs", "get_lambda_metrics", "get_lambda_config", "get_aws_health_events"]

        # Pick highest-priority remaining tool
        selected = next((t for t in priority if t in remaining_tools), remaining_tools[0])
        confidence = 0.87
        probs = self._uniform_probs(remaining_tools, selected, confidence)

        return ToolDecision(
            selected_tool=selected,
            confidence=confidence,
            probabilities=probs,
            using_real_decider=False,
            reasoning=f"Keyword fallback selected '{selected}' "
                      f"(confidence: {confidence:.0%}) — install strands-decider for real decisions.",
        )

    @staticmethod
    def _uniform_probs(tools: list[str], selected: str, top_confidence: float) -> dict[str, float]:
        remaining_confidence = 1.0 - top_confidence
        other_count = len(tools) - 1
        per_other = remaining_confidence / other_count if other_count > 0 else 0.0
        return {t: (top_confidence if t == selected else per_other) for t in tools}


# ---------------------------------------------------------------------------
# Example agent loop (copy this pattern)
# ---------------------------------------------------------------------------

def run_agent_with_decider(
    query: str,
    available_tools: list[str],
    tool_runner: Any,  # callable: (tool_name: str, context: dict) -> dict
    max_steps: int = 3,
) -> AgentResult:
    """
    Generic agent loop using Strands Decider 2B for tool selection.

    This is the reusable pattern. Replace `tool_runner` with your own
    tool execution logic.

    Args:
        query: The user's query.
        available_tools: List of tool names the agent can use.
        tool_runner: A callable that runs a tool and returns its result dict.
        max_steps: Maximum number of tool calls before stopping.

    Returns:
        AgentResult with all steps, evidence, and stop reason.
    """
    decider = ToolSelectionDecider()
    result = AgentResult(query=query)
    already_called: list[str] = []
    evidence: dict[str, Any] = {}

    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print(f"Decider mode: {'Strands Decider 2B (real)' if decider.using_real_decider else 'Keyword fallback'}")
    print(f"{'='*60}\n")

    for step_num in range(1, max_steps + 1):
        remaining = [t for t in available_tools if t not in already_called]
        if not remaining:
            result.stopped_reason = "All tools exhausted"
            break

        # --- Decider 2B: select next tool ---
        evidence_summary = _summarise_evidence(evidence)
        decision = decider.select_tool(
            query=query,
            available_tools=available_tools,
            already_called=already_called,
            evidence_summary=evidence_summary,
        )

        print(f"Step {step_num}: {decision.selected_tool}")
        print(f"  Confidence: {decision.confidence:.0%}")
        print(f"  Probabilities: {json.dumps({k: f'{v:.0%}' for k, v in decision.probabilities.items()}, indent=2)}")
        print(f"  Reasoning: {decision.reasoning}")

        # --- Run the selected tool ---
        tool_result = tool_runner(decision.selected_tool, {"query": query})
        evidence[decision.selected_tool] = tool_result
        already_called.append(decision.selected_tool)

        step = AgentStep(
            step_number=step_num,
            decision=decision,
            tool_result=tool_result,
        )
        result.steps.append(step)
        print(f"  Result keys: {list(tool_result.keys())}\n")

        # --- Decider 2B: should we stop? ---
        updated_summary = _summarise_evidence(evidence)
        stop, stop_confidence = decider.should_stop(
            query=query,
            already_called=already_called,
            evidence_summary=updated_summary,
        )
        if stop:
            result.stopped_reason = f"Enough evidence (confidence: {stop_confidence:.0%})"
            print(f"Stopping: {result.stopped_reason}")
            break
    else:
        result.stopped_reason = f"Max steps ({max_steps}) reached"

    result.final_evidence = evidence
    return result


def _summarise_evidence(evidence: dict[str, Any]) -> str:
    if not evidence:
        return "none"
    parts = []
    for tool, data in evidence.items():
        keys = list(data.keys())[:3]
        parts.append(f"{tool}: {keys}")
    return "; ".join(parts)


# ---------------------------------------------------------------------------
# Demo / self-test
# ---------------------------------------------------------------------------

def _mock_tool_runner(tool_name: str, context: dict) -> dict:
    """Minimal mock tool runner for demonstration."""
    mock_results = {
        "get_lambda_metrics": {
            "error_rate": 0.34,
            "throttle_count": 847,
            "duration_p99_ms": 1200,
        },
        "get_cloudwatch_logs": {
            "log_entries": ["[ERROR] Rate exceeded", "[ERROR] Rate exceeded"],
            "period": "last 15 minutes",
        },
        "get_lambda_config": {
            "reserved_concurrency": 100,
            "memory_mb": 256,
            "timeout_seconds": 30,
        },
        "get_aws_health_events": {
            "events": [],
        },
    }
    return mock_results.get(tool_name, {"error": "unknown tool"})


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)

    tools = [
        "get_cloudwatch_logs",
        "get_lambda_metrics",
        "get_lambda_config",
        "get_aws_health_events",
    ]

    queries = [
        "my payment-processor function is being throttled",
        "lambda function is very slow on cold starts",
        "function exits with signal: killed — out of memory",
    ]

    for q in queries:
        agent_result = run_agent_with_decider(
            query=q,
            available_tools=tools,
            tool_runner=_mock_tool_runner,
            max_steps=3,
        )
        print(f"Stop reason: {agent_result.stopped_reason}")
        print(f"Tools called: {[s.decision.selected_tool for s in agent_result.steps]}")
        print()

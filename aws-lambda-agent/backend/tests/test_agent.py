import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data.sample_data import get_scenario_for_query, SAMPLE_SCENARIOS
from agent.tools import run_tool, AVAILABLE_TOOLS
from agent.decider import LambdaToolDecider

class TestLambdaAgent(unittest.TestCase):
    def test_scenario_matching(self):
        self.assertEqual(get_scenario_for_query("Function is being throttled under peak load"), "throttling")
        self.assertEqual(get_scenario_for_query("High cold start latency on lambda initialization"), "cold_start")
        self.assertEqual(get_scenario_for_query("Signal killed out of memory"), "oom")
        self.assertEqual(get_scenario_for_query("KeyError: user_id in handler"), "invocation_error")

    def test_diagnostic_tools(self):
        for tool in AVAILABLE_TOOLS:
            res = run_tool(tool, "test-func", "throttling")
            self.assertNotIn("error", res)
            self.assertIsInstance(res, dict)

    def test_decider_tool_selection(self):
        decider = LambdaToolDecider()
        res = decider.select_next_tool("Payment lambda throttled", [], {})
        self.assertIn(res.answer, AVAILABLE_TOOLS)
        self.assertGreater(res.confidence, 0.5)
        self.assertGreater(len(res.probabilities), 0)

        stop, conf = decider.should_stop("query", ["t1", "t2"], {})
        self.assertTrue(stop)
        self.assertGreaterEqual(conf, 0.85)

if __name__ == "__main__":
    unittest.main()

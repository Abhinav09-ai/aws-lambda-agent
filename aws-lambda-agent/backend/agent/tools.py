from typing import Dict, Any, List
from data.sample_data import SAMPLE_SCENARIOS

AVAILABLE_TOOLS: List[str] = [
    "get_cloudwatch_logs",
    "get_lambda_metrics",
    "get_lambda_config",
    "get_aws_health_events"
]

def get_cloudwatch_logs(function_name: str, scenario: str) -> Dict[str, Any]:
    data = SAMPLE_SCENARIOS.get(scenario, SAMPLE_SCENARIOS["invocation_error"])
    return {
        "function": function_name,
        "log_entries": data["logs"],
        "period": "last 15 minutes",
        "query_filter": "fields @timestamp, @message | sort @timestamp desc | limit 20"
    }

def get_lambda_metrics(function_name: str, scenario: str) -> Dict[str, Any]:
    data = SAMPLE_SCENARIOS.get(scenario, SAMPLE_SCENARIOS["invocation_error"])
    return {
        "function": function_name,
        "metrics": data["metrics"],
        "period": "last 1 hour",
        "sample_interval": "1 minute"
    }

def get_lambda_config(function_name: str, scenario: str) -> Dict[str, Any]:
    data = SAMPLE_SCENARIOS.get(scenario, SAMPLE_SCENARIOS["invocation_error"])
    return {
        "function": function_name,
        "config": data["config"]
    }

def get_aws_health_events(function_name: str, scenario: str) -> Dict[str, Any]:
    data = SAMPLE_SCENARIOS.get(scenario, SAMPLE_SCENARIOS["invocation_error"])
    return {
        "region": "us-east-1",
        "service": "AWS_LAMBDA",
        "events": data["health_events"]
    }

def run_tool(tool_name: str, function_name: str, scenario: str) -> Dict[str, Any]:
    if tool_name == "get_cloudwatch_logs":
        return get_cloudwatch_logs(function_name, scenario)
    elif tool_name == "get_lambda_metrics":
        return get_lambda_metrics(function_name, scenario)
    elif tool_name == "get_lambda_config":
        return get_lambda_config(function_name, scenario)
    elif tool_name == "get_aws_health_events":
        return get_aws_health_events(function_name, scenario)
    else:
        return {"error": f"Unknown tool: {tool_name}"}

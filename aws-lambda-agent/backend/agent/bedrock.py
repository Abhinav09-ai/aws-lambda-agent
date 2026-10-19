from typing import Dict, Any, List
import json
import os
import logging

logger = logging.getLogger(__name__)

class BedrockSynthesizer:
    def __init__(self):
        self.client = None
        self.available = False
        self.model_id = "anthropic.claude-3-haiku-20240307-v1:0"
        self._check_client()

    def _check_client(self):
        try:
            import boto3
            region = os.getenv("AWS_REGION", "us-east-1")
            self.client = boto3.client("bedrock-runtime", region_name=region)
            # Check credentials if present
            if os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY"):
                self.available = True
            else:
                self.available = False
        except Exception as e:
            logger.info("Bedrock client unavailable: %s", e)
            self.available = False

    def synthesize(
        self,
        query: str,
        scenario: str,
        evidence: Dict[str, Any],
        decision_trace: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        if self.available and self.client:
            try:
                prompt = f"""Human: You are an expert AWS Site Reliability Engineer.
Analyze this Lambda issue and gathered evidence.
User Query: {query}
Gathered Evidence: {json.dumps(evidence, default=str)}
Decision Trace: {json.dumps(decision_trace, default=str)}

Respond in valid JSON only with keys:
"root_cause": string (concise root cause summary),
"explanation": string (clear explanation of why this happened based on logs/metrics),
"fix_recommendation": string (actionable steps to resolve),
"fix_commands": array of strings (exact AWS CLI or shell commands to apply the fix)

Assistant:"""
                body = json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1000,
                    "temperature": 0.1,
                    "messages": [{"role": "user", "content": prompt}]
                })
                res = self.client.invoke_model(modelId=self.model_id, body=body)
                resp_json = json.loads(res["body"].read())
                content = resp_json["content"][0]["text"]
                parsed = json.loads(content)
                parsed["mode"] = "bedrock"
                return parsed
            except Exception as e:
                logger.warning("Bedrock invocation failed, falling back to verified synthesis template: %s", e)

        # Verified synthesis template per scenario
        templates = {
            "throttling": {
                "root_cause": "Lambda Concurrency Limit Exceeded (Throttling)",
                "explanation": "Evidence reveals 847 throttle events and a 34% error rate. The function has a reserved concurrency limit of 100 which is being saturated during traffic bursts.",
                "fix_recommendation": "Increase the function's reserved concurrency quota to handle peak bursts or place an Amazon SQS buffer queue in front of the Lambda.",
                "fix_commands": [
                    "aws lambda put-function-concurrency --function-name payment-processor-prod --reserved-concurrent-executions 250",
                    "aws cloudwatch put-metric-alarm --alarm-name 'Lambda-Throttles-Alert' --metric-name Throttles --namespace AWS/Lambda --statistic Sum --period 300 --threshold 10 --comparison-operator GreaterThanThreshold"
                ],
                "mode": "demo"
            },
            "cold_start": {
                "root_cause": "High Initialization Latency (Cold Starts)",
                "explanation": "CloudWatch Logs record an Init Duration of 4,532ms. Large unoptimized dependencies (torchvision, numpy) loaded synchronously during container bootstrap cause p99 latency to hit 8.2s.",
                "fix_recommendation": "Configure Provisioned Concurrency to keep warm container instances ready, or optimize the deployment bundle by tree-shaking unused ML dependencies.",
                "fix_commands": [
                    "aws lambda put-provisioned-concurrency-config --function-name image-resizer-prod --qualifier live --provisioned-concurrent-executions 5",
                    "aws lambda update-function-configuration --function-name image-resizer-prod --memory-size 2048"
                ],
                "mode": "demo"
            },
            "oom": {
                "root_cause": "Memory Limit Exceeded (OOM Crash)",
                "explanation": "Function terminated abruptly with 'Runtime exited with error: signal: killed'. Memory consumption peaked at 512 MB (100% of the allocated 512 MB memory limit) while buffering datasets.",
                "fix_recommendation": "Upgrade function memory allocation to 1024 MB or stream records in chunks rather than buffering the entire batch into memory.",
                "fix_commands": [
                    "aws lambda update-function-configuration --function-name data-etl-prod --memory-size 1024",
                    "aws cloudwatch put-metric-alarm --alarm-name 'Lambda-MaxMemory-Alert' --metric-name MemoryUtilization --namespace AWS/Lambda --statistic Maximum --threshold 90 --period 60"
                ],
                "mode": "demo"
            },
            "invocation_error": {
                "root_cause": "Unhandled KeyError in Handler Logic",
                "explanation": "CloudWatch Logs show an unhandled Python exception: KeyError: 'user_id' in handler.py line 28. Incoming invocations lack the required payload attribute.",
                "fix_recommendation": "Implement defensive schema validation using Pydantic or dict.get('user_id') with proper error handling and dead-letter queue (DLQ) routing.",
                "fix_commands": [
                    "aws lambda update-function-configuration --function-name notification-service-dev --dead-letter-config TargetArn=arn:aws:sqs:us-east-1:123456789012:lambda-dlq",
                    "aws logs filter-log-events --log-group-name /aws/lambda/notification-service-dev --filter-pattern 'Traceback'"
                ],
                "mode": "demo"
            }
        }
        res = templates.get(scenario, templates["invocation_error"])
        return res

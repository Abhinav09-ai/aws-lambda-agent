"""
Realistic sample data for AWS Lambda troubleshooting scenarios.
"""

SAMPLE_SCENARIOS = {
    "throttling": {
        "function_name": "payment-processor-prod",
        "error_type": "ThrottlingException",
        "logs": [
            "2026-10-19T10:14:02.100Z START RequestId: a91823-11ef-9321-411",
            "2026-10-19T10:14:02.112Z [ERROR] Rate exceeded: ConcurrencyLimitExceeded for account 123456789012",
            "2026-10-19T10:14:02.115Z [WARN] Client request throttled during peak payment checkout stream",
            "2026-10-19T10:14:02.118Z END RequestId: a91823-11ef-9321-411",
            "2026-10-19T10:14:02.120Z REPORT RequestId: a91823-11ef-9321-411 Duration: 18.2 ms Billed Duration: 19 ms Memory Size: 256 MB Max Memory Used: 78 MB"
        ],
        "metrics": {
            "error_rate": 0.34,
            "throttle_count": 847,
            "duration_p99_ms": 1420,
            "invocation_count": 12500,
            "memory_used_mb": 78,
            "memory_limit_mb": 256
        },
        "config": {
            "timeout_seconds": 30,
            "memory_mb": 256,
            "reserved_concurrency": 100,
            "provisioned_concurrency": 0,
            "runtime": "python3.11",
            "last_modified": "2026-10-01T08:30:00Z"
        },
        "health_events": []
    },
    "cold_start": {
        "function_name": "image-resizer-prod",
        "error_type": "HighLatencyWarning",
        "logs": [
            "2026-10-19T11:02:14.005Z START RequestId: b20194-43ea-8821-992",
            "2026-10-19T11:02:18.537Z [INFO] Loading heavy computer vision dependencies: torchvision, numpy, pillow",
            "2026-10-19T11:02:22.210Z [INFO] Finished initialization of weights and cache models",
            "2026-10-19T11:02:22.300Z END RequestId: b20194-43ea-8821-992",
            "2026-10-19T10:02:22.305Z REPORT RequestId: b20194-43ea-8821-992 Duration: 8200 ms Billed Duration: 8200 ms Memory Size: 1024 MB Max Memory Used: 640 MB Init Duration: 4532 ms"
        ],
        "metrics": {
            "error_rate": 0.02,
            "throttle_count": 0,
            "duration_p99_ms": 8200,
            "invocation_count": 3100,
            "memory_used_mb": 640,
            "memory_limit_mb": 1024
        },
        "config": {
            "timeout_seconds": 15,
            "memory_mb": 1024,
            "reserved_concurrency": 50,
            "provisioned_concurrency": 0,
            "runtime": "python3.11",
            "last_modified": "2026-10-12T14:15:00Z"
        },
        "health_events": []
    },
    "oom": {
        "function_name": "data-etl-prod",
        "error_type": "OutOfMemoryKilled",
        "logs": [
            "2026-10-19T09:45:10.120Z START RequestId: c31048-91ac-7744-123",
            "2026-10-19T09:45:12.800Z [INFO] Ingesting CSV chunk with 150,000 records into memory dataframe",
            "2026-10-19T09:45:14.990Z [WARN] Memory consumption at 98% (502 MB / 512 MB)",
            "2026-10-19T09:45:15.110Z Runtime exited with error: signal: killed",
            "2026-10-19T09:45:15.115Z REPORT RequestId: c31048-91ac-7744-123 Duration: 5010 ms Billed Duration: 5010 ms Memory Size: 512 MB Max Memory Used: 512 MB"
        ],
        "metrics": {
            "error_rate": 0.42,
            "throttle_count": 0,
            "duration_p99_ms": 5010,
            "invocation_count": 890,
            "memory_used_mb": 512,
            "memory_limit_mb": 512
        },
        "config": {
            "timeout_seconds": 60,
            "memory_mb": 512,
            "reserved_concurrency": 20,
            "provisioned_concurrency": 0,
            "runtime": "python3.11",
            "last_modified": "2026-09-20T11:00:00Z"
        },
        "health_events": []
    },
    "invocation_error": {
        "function_name": "notification-service-dev",
        "error_type": "UnhandledKeyError",
        "logs": [
            "2026-10-19T12:00:01.010Z START RequestId: d49201-11ab-3321-778",
            "2026-10-19T12:00:01.050Z [ERROR] Traceback (most recent call last):",
            "2026-10-19T12:00:01.051Z   File \"/var/task/handler.py\", line 28, in lambda_handler",
            "2026-10-19T12:00:01.052Z     recipient_id = event['user_id']",
            "2026-10-19T12:00:01.053Z KeyError: 'user_id'",
            "2026-10-19T12:00:01.060Z END RequestId: d49201-11ab-3321-778",
            "2026-10-19T12:00:01.065Z REPORT RequestId: d49201-11ab-3321-778 Duration: 55 ms Billed Duration: 56 ms Memory Size: 256 MB Max Memory Used: 82 MB"
        ],
        "metrics": {
            "error_rate": 0.18,
            "throttle_count": 0,
            "duration_p99_ms": 110,
            "invocation_count": 4200,
            "memory_used_mb": 82,
            "memory_limit_mb": 256
        },
        "config": {
            "timeout_seconds": 10,
            "memory_mb": 256,
            "reserved_concurrency": 10,
            "provisioned_concurrency": 0,
            "runtime": "python3.11",
            "last_modified": "2026-10-18T19:00:00Z"
        },
        "health_events": []
    }
}


def get_scenario_for_query(query: str) -> str:
    q = query.lower()
    if any(k in q for k in ["throttl", "rate exceed", "429", "concurren"]):
        return "throttling"
    if any(k in q for k in ["cold", "slow", "init", "latency", "startup"]):
        return "cold_start"
    if any(k in q for k in ["memory", "oom", "kill", "signal", "512mb"]):
        return "oom"
    return "invocation_error"

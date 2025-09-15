"""Validation checks for {{.project_name}} AI Tools.

- Functional test of the main tool function
- Latency measurement vs target
"""
import time
from typing import Any, Dict

from .generic_functions import {{.tool_name}}


def run(latency_target_ms: int = int("{{.latency_target_ms}}")) -> None:
    payload: Dict[str, Any] = {"text": "healthcheck"}

    t0 = time.time()
    out = {{.tool_name}}(payload)
    elapsed_ms = int((time.time() - t0) * 1000)

    print(f"Output: {out}")
    print(f"Latency: {elapsed_ms} ms; target: {latency_target_ms} ms")

    if elapsed_ms > latency_target_ms:
        raise RuntimeError(f"Latency {elapsed_ms} exceeds target {latency_target_ms} ms")


if __name__ == "__main__":
    run()

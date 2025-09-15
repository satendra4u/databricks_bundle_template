"""Synchronous inference client for {{.project_name}} AI Tools.

Calls the Model Serving endpoint and prints the response.
Env vars required:
- DATABRICKS_HOST
- DATABRICKS_TOKEN
"""
import os
import json
import requests
from typing import Any, Dict, List


def invoke(endpoint_name: str, inputs: List[Dict[str, Any]]) -> Dict[str, Any]:
    host = os.environ.get("DATABRICKS_HOST")
    token = os.environ.get("DATABRICKS_TOKEN")
    if not host or not token:
        raise RuntimeError("Set DATABRICKS_HOST and DATABRICKS_TOKEN environment variables")

    url = f"{host.rstrip('/')}/serving-endpoints/{endpoint_name}/invocations"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"inputs": inputs}

    r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
    r.raise_for_status()
    return r.json()


def run() -> None:
    endpoint_name = "{{.endpoint_name}}"
    inputs = [{"text": "hello tool"}]
    resp = invoke(endpoint_name, inputs)
    print(json.dumps(resp, indent=2))


if __name__ == "__main__":
    run()

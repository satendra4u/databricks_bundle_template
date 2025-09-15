"""Asynchronous inference processor for {{.project_name}}.

Reads requests from a Delta inbox table, calls the agent serving endpoint, and writes
responses to a Delta outbox table. This is intended to run as a scheduled/batch job.

Required environment variables for endpoint invocation:
- DATABRICKS_HOST
- DATABRICKS_TOKEN
"""
import os
import json
import requests
from typing import Any, Dict, List


def _invoke(endpoint_name: str, inputs: List[Dict[str, Any]]) -> Dict[str, Any]:
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


def run(catalog: str, schema: str,
        inbox_table: str = "agent_inbox",
        outbox_table: str = "agent_outbox",
        text_col: str = "text",
        id_col: str = "id",
        endpoint_name: str = "{{.agent_endpoint_name}}") -> None:
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col, struct, lit

    spark = SparkSession.builder.getOrCreate()

    inbox = f"{catalog}.{schema}.{inbox_table}"
    outbox = f"{catalog}.{schema}.{outbox_table}"

    try:
        reqs = spark.table(inbox)
    except Exception:
        # Create an empty inbox if it doesn't exist
        spark.createDataFrame([], schema=f"{id_col} STRING, {text_col} STRING").write.mode("overwrite").saveAsTable(inbox)
        reqs = spark.table(inbox)

    if reqs.rdd.isEmpty():
        print("No pending requests in inbox")
        return

    # Convert rows to list of payloads
    pdf = reqs.select(id_col, text_col).toPandas()
    inputs = [{"id": rid, "text": txt} for rid, txt in zip(pdf[id_col], pdf[text_col])]

    resp = _invoke(endpoint_name, inputs)

    # Expecting response to include outputs aligned with inputs; adapt as needed
    outputs = resp.get("outputs", []) if isinstance(resp, dict) else []
    # Build a simple mapping by id if available
    id_to_output = {}
    for out in outputs:
        oid = out.get("id") or out.get("request_id")
        id_to_output[oid] = out

    rows = []
    for item in inputs:
        rid = item.get("id")
        txt = item.get("text")
        out = id_to_output.get(rid, {})
        rows.append({id_col: rid, text_col: txt, "response": json.dumps(out)})

    out_df = spark.createDataFrame(rows)
    out_df.write.mode("append").saveAsTable(outbox)
    print(f"Wrote {len(rows)} responses to {outbox}")


if __name__ == "__main__":
    run(catalog="{{.uc_catalog}}", schema="{{.uc_schema}}")

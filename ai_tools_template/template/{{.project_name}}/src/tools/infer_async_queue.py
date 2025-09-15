"""Asynchronous inference queue processor for {{.project_name}} AI Tools.

Reads requests from a Delta inbox table, invokes the serving endpoint, and writes
responses to an outbox table. Intended to run as a scheduled job.

Env vars required:
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


def run(inbox_table: str = "tools_inbox", outbox_table: str = "tools_outbox", endpoint_name: str = "{{.endpoint_name}}",
        id_col: str = "id", text_col: str = "text") -> None:
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.getOrCreate()

    try:
        inbox_df = spark.table(inbox_table)
    except Exception:
        spark.createDataFrame([], schema=f"{id_col} STRING, {text_col} STRING").write.mode("overwrite").saveAsTable(inbox_table)
        inbox_df = spark.table(inbox_table)

    if inbox_df.rdd.isEmpty():
        print("No pending requests in inbox")
        return

    pdf = inbox_df.select(id_col, text_col).toPandas()
    inputs = [{"id": rid, "text": txt} for rid, txt in zip(pdf[id_col], pdf[text_col])]

    resp = _invoke(endpoint_name, inputs)
    outputs = resp.get("outputs", []) if isinstance(resp, dict) else []

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
    out_df.write.mode("append").saveAsTable(outbox_table)
    print(f"Wrote {len(rows)} responses to {outbox_table}")


if __name__ == "__main__":
    run()

"""Run the tool as a Databricks Job for batch processing.

Reads inputs from a Delta table and writes outputs to another Delta table.
"""
from typing import Any, Dict
from pyspark.sql import SparkSession
from .generic_functions import {{.tool_name}}


def run(input_table: str = "tools_inbox", output_table: str = "tools_outbox",
        id_col: str = "id", text_col: str = "text") -> None:
    spark = SparkSession.builder.getOrCreate()
    try:
        df = spark.table(input_table)
    except Exception:
        print(f"Input table {input_table} not found; creating empty table")
        spark.createDataFrame([], schema=f"{id_col} STRING, {text_col} STRING").write.mode("overwrite").saveAsTable(input_table)
        df = spark.table(input_table)

    if df.rdd.isEmpty():
        print("No inputs to process")
        return

    pdf = df.select(id_col, text_col).toPandas()
    rows = []
    for rid, txt in zip(pdf[id_col], pdf[text_col]):
        out = {{.tool_name}}({"id": rid, "text": txt})
        rows.append({id_col: rid, text_col: txt, "response": str(out)})

    out_df = spark.createDataFrame(rows)
    out_df.write.mode("append").saveAsTable(output_table)
    print(f"Wrote {len(rows)} outputs to {output_table}")


if __name__ == "__main__":
    run()

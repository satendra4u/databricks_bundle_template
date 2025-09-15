"""Bootstrap Delta tables used by the AI Agent async flow.

Creates inbox/outbox tables in the specified UC catalog/schema if they do not exist.
"""
from pyspark.sql import SparkSession


def run(catalog: str, schema: str, inbox: str = "agent_inbox", outbox: str = "agent_outbox") -> None:
    spark = SparkSession.builder.getOrCreate()

    inbox_fqn = f"{catalog}.{schema}.{inbox}"
    outbox_fqn = f"{catalog}.{schema}.{outbox}"

    # Create inbox if missing
    try:
        spark.table(inbox_fqn)
        print(f"Inbox exists: {inbox_fqn}")
    except Exception:
        spark.createDataFrame([], schema="id STRING, text STRING").write.mode("overwrite").saveAsTable(inbox_fqn)
        print(f"Created inbox: {inbox_fqn}")

    # Create outbox if missing
    try:
        spark.table(outbox_fqn)
        print(f"Outbox exists: {outbox_fqn}")
    except Exception:
        spark.createDataFrame([], schema="id STRING, text STRING, response STRING").write.mode("overwrite").saveAsTable(outbox_fqn)
        print(f"Created outbox: {outbox_fqn}")


if __name__ == "__main__":
    run(catalog="{{.uc_catalog}}", schema="{{.uc_schema}}")

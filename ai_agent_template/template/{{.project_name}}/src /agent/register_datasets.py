"""Register datasets to Unity Catalog for {{.project_name}}.

Steps:
1) Ingest or reference data from the configured source.
2) Create managed tables in UC catalog/schema.
"""
from typing import Optional


def run(source: str, catalog: str, schema: str, table_name: str = "agent_raw") -> None:
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.getOrCreate()

    # Example: if source is s3 path, read as files; if it's UC path, simply clone or CTAS.
    if source.startswith("s3://"):
        df = spark.read.format("parquet").load(source)
    elif "/" in source or "." in source:
        # Attempt to read from a table-like identifier
        df = spark.table(source)
    else:
        raise ValueError("Unsupported data_source format. Provide s3://... or a UC table path.")

    full_out = f"{catalog}.{schema}.{table_name}"
    df.write.mode("overwrite").saveAsTable(full_out)
    print(f"Registered dataset at {full_out}")


if __name__ == "__main__":
    run(source="{{.data_source}}", catalog="{{.uc_catalog}}", schema="{{.uc_schema}}")

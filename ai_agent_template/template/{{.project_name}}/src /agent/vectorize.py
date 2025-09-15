"""Vectorize data and create/refresh a Vector Search index for {{.project_name}}.

This script demonstrates how you might:
- Load text from a UC table
- Generate embeddings using a system model
- Write embeddings back to UC
- Ensure a Vector Search index exists and is synced

Note: Adjust to your org's preferred embedding model/workflow.
"""
from typing import Optional


def run(catalog: str, schema: str, source_table: str = "agent_raw", text_col: str = "text",
        embeddings_table: str = "agent_embeddings", index_name: str = "{{.vector_index_name}}",
        vs_endpoint: str = "{{.vector_endpoint_name}}", embedding_model: str = "databricks-bge-large-en") -> None:
    from pyspark.sql import SparkSession
    from databricks.sdk import WorkspaceClient

    spark = SparkSession.builder.getOrCreate()
    w = WorkspaceClient()

    src = f"{catalog}.{schema}.{source_table}"
    dst = f"{catalog}.{schema}.{embeddings_table}"

    # Example: simple UDF to call embeddings; replace with production-grade invocation
    # For Databricks Foundation Models, you can use AI functions or serving endpoints.
    df = spark.table(src)
    if text_col not in df.columns:
        raise ValueError(f"text column '{text_col}' not found in {src}")

    # Placeholder: copy text and add dummy vector (all zeros) to show schema
    # In production, call the embeddings model and populate 'embedding' column with a vector (array<float>)
    from pyspark.sql.functions import lit
    df_out = df.select(text_col).withColumn("embedding", lit([0.0]*3))
    df_out.write.mode("overwrite").saveAsTable(dst)
    print(f"Wrote embeddings to {dst}")

    # Ensure Vector Search endpoint exists (idempotent)
    try:
        w.vector_search.endpoints.get(name=vs_endpoint)
        print(f"Vector Search endpoint exists: {vs_endpoint}")
    except Exception:
        w.vector_search.endpoints.create(name=vs_endpoint)
        print(f"Created Vector Search endpoint: {vs_endpoint}")

    # Ensure Index exists (idempotent)
    full_index_name = f"{catalog}.{schema}.{index_name}"
    try:
        w.vector_search.indexes.get(name=full_index_name)
        print(f"Vector Search index exists: {full_index_name}")
    except Exception:
        # Create an embedding index over the table
        w.vector_search.indexes.create(
            name=full_index_name,
            endpoint_name=vs_endpoint,
            primary_key="id",  # Ensure your table has an 'id' column or adjust accordingly
            embedding_vector_column="embedding",
            embedding_source_columns=[text_col],
            schema_name=schema,
            catalog_name=catalog,
            index_type="EMBEDDING",
            input_table_name=dst,
        )
        print(f"Created Vector Search index: {full_index_name}")

    # Request a sync/refresh
    try:
        w.vector_search.indexes.sync(name=full_index_name)
        print(f"Triggered sync for index: {full_index_name}")
    except Exception as e:
        print(f"Index sync not supported or failed: {e}")


if __name__ == "__main__":
    run(catalog="{{.uc_catalog}}", schema="{{.uc_schema}}")

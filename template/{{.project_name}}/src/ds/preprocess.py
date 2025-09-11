"""Data preprocessing entrypoint for {{.project_name}}."""
from typing import Optional


def run(input_table: str, output_table: str, catalog: Optional[str] = None, schema: Optional[str] = None) -> None:
    """Example preprocess that copies data from input to output."""
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.getOrCreate()
    full_in = f"{catalog+'.' if catalog else ''}{schema+'.' if schema else ''}{input_table}"
    full_out = f"{catalog+'.' if catalog else ''}{schema+'.' if schema else ''}{output_table}"

    df = spark.table(full_in)
    # TODO: add real transforms
    df.write.mode("overwrite").saveAsTable(full_out)
    print(f"Wrote preprocessed data to {full_out}")


if __name__ == "__main__":
    # Example CLI usage; in Databricks jobs, configure via parameters
    run(input_table="raw.input", output_table="curated.output")

"""Batch inference entrypoint for {{.project_name}}."""
from typing import Optional

def run(input_table: str, output_table: str, model_name: str, catalog: Optional[str] = None, schema: Optional[str] = None) -> None:
    import mlflow
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.getOrCreate()
    full_in = f"{catalog+'.' if catalog else ''}{schema+'.' if schema else ''}{input_table}"
    full_out = f"{catalog+'.' if catalog else ''}{schema+'.' if schema else ''}{output_table}"

    df = spark.table(full_in)

    # Load latest model
    client = mlflow.tracking.MlflowClient()
    rm = client.get_registered_model(model_name)
    latest_version = max((int(v.version) for v in rm.latest_versions), default=None)
    if latest_version is None:
        raise RuntimeError(f"No versions found for model {model_name}")

    pyfunc = mlflow.pyfunc.load_model(model_uri=f"models:/{model_name}/{latest_version}")

    pdf = df.toPandas()
    preds = pyfunc.predict(pdf)
    out_pdf = pdf.copy()
    out_pdf["prediction"] = preds

    out_sdf = spark.createDataFrame(out_pdf)
    out_sdf.write.mode("overwrite").saveAsTable(full_out)
    print(f"Wrote batch inference results to {full_out}")


if __name__ == "__main__":
    run(input_table="curated.output", output_table="predictions.output", model_name="{{.project_name}}-model")

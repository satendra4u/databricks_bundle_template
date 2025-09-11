"""Model training entrypoint for {{.project_name}}."""
from typing import Optional


def run(training_table: str, experiment: str, model_name: str, catalog: Optional[str] = None, schema: Optional[str] = None) -> None:
    import mlflow
    import pandas as pd
    from pyspark.sql import SparkSession
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    spark = SparkSession.builder.getOrCreate()
    full_table = f"{catalog+'.' if catalog else ''}{schema+'.' if schema else ''}{training_table}"
    pdf = spark.table(full_table).toPandas()

    # Dummy example: assume label column 'y'
    X = pdf.drop(columns=[c for c in pdf.columns if c.lower() in ("label", "y")][0])
    y = pdf[[c for c in pdf.columns if c.lower() in ("label", "y")][0]]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    mlflow.set_experiment(experiment)
    with mlflow.start_run():
        model = LogisticRegression(max_iter=100)
        model.fit(X_train, y_train.values.ravel())
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        mlflow.log_metric("accuracy", float(acc))
        mlflow.sklearn.log_model(model, "model")
        mlflow.set_tag("model_name", model_name)
        print(f"Trained model {model_name} with accuracy={acc:.4f}")


if __name__ == "__main__":
    run(training_table="curated.output", experiment="/Shared/{{.project_name}}/experiments/train", model_name="{{.project_name}}-model")

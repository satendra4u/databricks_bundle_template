"""MLflow utility helpers."""
import mlflow


def latest_run_id(experiment: str) -> str:
    client = mlflow.tracking.MlflowClient()
    exp = mlflow.get_experiment_by_name(experiment)
    if not exp:
        raise RuntimeError(f"Experiment not found: {experiment}")
    runs = client.search_runs(experiment_ids=[exp.experiment_id], order_by=["attributes.start_time DESC"], max_results=1)
    if not runs:
        raise RuntimeError("No runs found")
    return runs[0].info.run_id

"""Model registration entrypoint for {{.project_name}}."""
from typing import Optional


def run(experiment: str, model_name: str) -> None:
    import mlflow

    client = mlflow.tracking.MlflowClient()
    runs = client.search_runs(experiment_ids=[mlflow.get_experiment_by_name(experiment).experiment_id], order_by=["attributes.start_time DESC"], max_results=1)
    if not runs:
        raise RuntimeError("No runs found to register")
    run_id = runs[0].info.run_id
    mv = mlflow.register_model(f"runs:/{run_id}/model", model_name)
    print(f"Registered model version: name={model_name}, version={mv.version}")


if __name__ == "__main__":
    run(experiment="/Shared/{{.project_name}}/experiments/train", model_name="{{.project_name}}-model")

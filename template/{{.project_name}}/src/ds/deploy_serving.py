"""Serving deployment entrypoint for {{.project_name}}."""

def run(model_name: str, target_endpoint: str) -> None:
    import mlflow
    from databricks.sdk import WorkspaceClient

    w = WorkspaceClient()
    client = mlflow.tracking.MlflowClient()
    latest = client.get_registered_model(model_name)
    # Choose latest version
    latest_version = max((int(v.version) for v in latest.latest_versions), default=None)
    if latest_version is None:
        raise RuntimeError(f"No versions found for model {model_name}")

    # Create or update serving endpoint (placeholder minimal example)
    try:
        w.serving_endpoints.get(name=target_endpoint)
        w.serving_endpoints.update_config(name=target_endpoint, served_models=[{"name": "prod", "model_name": model_name, "model_version": str(latest_version), "workload_size": "Small"}])
        print(f"Updated endpoint {target_endpoint} -> {model_name}:{latest_version}")
    except Exception:
        w.serving_endpoints.create(name=target_endpoint, config={"served_models": [{"name": "prod", "model_name": model_name, "model_version": str(latest_version), "workload_size": "Small"}]})
        print(f"Created endpoint {target_endpoint} -> {model_name}:{latest_version}")


if __name__ == "__main__":
    run(model_name="{{.project_name}}-model", target_endpoint="{{.project_name}}-endpoint")

"""Create or update a Serving endpoint for {{.project_name}} tools.

Note: In production, you should log an MLflow model (pyfunc) that wraps your tool(s) and
reference it below. This template provides a placeholder to show endpoint creation.
"""
from typing import Optional


def run(endpoint_name: str = "{{.endpoint_name}}", model_name: str = "", model_version: str = "") -> None:
    from databricks.sdk import WorkspaceClient

    w = WorkspaceClient()

    if not model_name:
        # Placeholder: Without a registered model, we can't attach a real served_model.
        # We still create an empty endpoint config to be updated later.
        cfg = {"served_models": []}
    else:
        cfg = {
            "served_models": [
                {
                    "name": "tool",
                    "model_name": model_name,
                    "model_version": model_version,
                    # Add workload size or scale settings as appropriate
                    "workload_size": "Small"
                }
            ]
        }

    try:
        w.serving_endpoints.get(name=endpoint_name)
        w.serving_endpoints.update_config(name=endpoint_name, **cfg)
        print(f"Updated serving endpoint: {endpoint_name}")
    except Exception:
        w.serving_endpoints.create(name=endpoint_name, config=cfg)
        print(f"Created serving endpoint: {endpoint_name}")


if __name__ == "__main__":
    run()

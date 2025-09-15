"""Create or update the AI Agent serving endpoint for {{.project_name}}.

This uses Databricks Model Serving to host a simple agent function.
In a production setup, package your agent logic as a model or handler and reference it here.
"""
from typing import Optional


def run(endpoint_name: str, llm_model: str) -> None:
    from databricks.sdk import WorkspaceClient

    w = WorkspaceClient()

    served_models = [
        {
            "name": "agent",
            # For demo: reference a foundation LLM directly via serverless routing
            # In production: reference a logged MLflow model or custom handler
            "model_name": llm_model,
            "model_version": ""
        }
    ]

    try:
        w.serving_endpoints.get(name=endpoint_name)
        w.serving_endpoints.update_config(name=endpoint_name, served_models=served_models)
        print(f"Updated serving endpoint: {endpoint_name}")
    except Exception:
        w.serving_endpoints.create(name=endpoint_name, config={"served_models": served_models})
        print(f"Created serving endpoint: {endpoint_name}")


if __name__ == "__main__":
    run(endpoint_name="{{.agent_endpoint_name}}", llm_model="{{.llm_model}}")

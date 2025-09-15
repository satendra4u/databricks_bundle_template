# Databricks AI Agent Bundle Template

This is an additional template in this repository focused on building AI Agents on Databricks.
It supports:
- Registering datasets to Unity Catalog
- Vectorizing data (embeddings) and creating a Vector Search index/endpoint
- Selecting an LLM
- Creating a Model Serving endpoint for the agent
- Sync (real-time) and async (batch) inference paths

## Use
```bash
# From this repo URL, specify the subdirectory containing the schema
# The schema file is at: ai_agent_template/databricks_template_schema.json

databricks bundle init https://github.com/<org>/<repo>.git --template-dir ai_agent_template
```

You will be prompted for:
- project_name
- data_source
- uc_catalog, uc_schema
- vector_index_name, vector_endpoint_name
- llm_model
- agent_endpoint_name

The generated project mirrors the AI model template structure but includes agent-specific jobs and code under `src/agent/`.

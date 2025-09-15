# Databricks AI Tools Bundle Template

A template for building and serving generic AI tools on Databricks with both low-latency (serverless) and job-based (batch) modes. Includes validation, serving, and sync/async flows.

## Use this template
From this repo via subdirectory:
```bash
databricks bundle init https://github.com/<org>/<repo>.git --template-dir ai_tools_template
```
Or from local path:
```bash
databricks bundle init /path/to/Databricks_template/ai_tools_template
```

## Prompts
- project_name
- uc_catalog, uc_schema
- tool_name
- endpoint_name
- latency_target_ms
- compute_mode (serverless|job)
- delivery_mode (sync|async|both)

## Generated project
- `databricks.yml` (includes `jobs/*.yml`)
- `src/tools/` with:
  - `generic_functions.py` (example tool functions)
  - `validate.py` (sanity checks, latency target placeholder)
  - `serve.py` (create/update serving endpoint for tool)
  - `infer_sync.py` (sync invocation)
  - `infer_async_queue.py` (queue processor)
  - `job_runner.py` (run tool as a Databricks job)
- `jobs/` with YAMLs for validate/deploy/sync/async/job

Adjust cluster sizes, serving config, and functions to your needs.

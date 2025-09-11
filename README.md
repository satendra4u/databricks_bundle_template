# Databricks Bundle Template

This repository contains a custom Databricks Asset Bundle template. It follows the official template schema and uses Go templating so you can initialize new projects with a consistent structure.

## Contents
- `databricks_template_schema.json`: Template schema defining prompts and messages.
- `template/{{.project_name}}/`: Folder that mirrors the structure of the generated bundle.
  - `databricks.yml.tmpl`: Main bundle config. Includes `jobs/*.yml`.
  - `requirements*.txt`: Python dependencies.
  - `src/ds/`: Project package with preprocessing, training, registration, serving, and utils.
  - `notebooks/`: Interactive notebooks.
  - `jobs/`: Job definitions.
  - `policies/`: Example cluster/serving policies.
  - `ci/`: Example GitHub Actions workflow.
  - `docs/`: Governance doc.

## Prerequisites
- Databricks CLI v0.240.0+
- An authenticated Databricks profile (`databricks auth login`)

## How to use this template (from Git)
1. Ensure this repo is accessible to your users (public or they have access).
2. Users run:
   ```bash
   databricks bundle init https://github.com/<org>/<repo>.git
   ```
   If the schema is in a subfolder, use `--template-dir`.

3. When prompted, enter the project name (e.g., `my_project`). The CLI will generate:
   ```
   my_project/
     databricks.yml
     requirements.txt
     src/
     notebooks/
     jobs/
     policies/
     ci/
     docs/
   ```

## Non-interactive init (optional)
Create `init.json`:
```json
{ "project_name": "my_project" }
```
Run:
```bash
databricks bundle init <git-url-or-path> --config-file init.json
```

## Validate and run
```bash
cd my_project
# Validate configuration
databricks bundle validate -t dev
# Deploy configuration
databricks bundle deploy -t dev
# Run a job (example)
databricks bundle run job_preprocess -t dev
```

## Local path usage (without Git)
If users have the template locally:
```bash
databricks bundle init /path/to/Databricks_template
```

## Notes
- You can add more prompts to `databricks_template_schema.json` (enums, patterns, ordering).
- `jobs/*.yml` reference notebooks and Python scripts in `notebooks/` and `src/`.
- Adjust cluster sizes, Spark versions, policies, and CI workflow to your org standards.

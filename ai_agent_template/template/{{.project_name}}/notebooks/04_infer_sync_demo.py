# Databricks notebook source
# COMMAND ----------
# Sync inference demo for {{.project_name}}

from agent.infer_sync import run

# Ensure DATABRICKS_HOST and DATABRICKS_TOKEN are configured in the job/cluster env
run()

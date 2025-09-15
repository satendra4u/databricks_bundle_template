# Databricks notebook source
# COMMAND ----------
# Deploy AI Tools serving endpoint for {{.project_name}}

from tools.serve import run

run(endpoint_name="{{.endpoint_name}}")

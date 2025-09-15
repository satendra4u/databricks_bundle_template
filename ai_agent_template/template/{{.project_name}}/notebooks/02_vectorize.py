# Databricks notebook source
# COMMAND ----------
# Vectorize data and manage Vector Search for {{.project_name}}

from agent.vectorize import run

run(catalog="{{.uc_catalog}}", schema="{{.uc_schema}}")

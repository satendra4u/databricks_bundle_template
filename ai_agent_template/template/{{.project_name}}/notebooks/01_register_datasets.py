# Databricks notebook source
# COMMAND ----------
# Register datasets to UC for {{.project_name}}

from agent.register_datasets import run

run(source="{{.data_source}}", catalog="{{.uc_catalog}}", schema="{{.uc_schema}}")

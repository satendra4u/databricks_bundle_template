# Databricks notebook source
# COMMAND ----------
# Create inbox/outbox tables for async processing for {{.project_name}}

from agent.bootstrap_tables import run

run(catalog="{{.uc_catalog}}", schema="{{.uc_schema}}")

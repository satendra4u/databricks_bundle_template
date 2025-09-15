# Databricks notebook source
# COMMAND ----------
# Deploy AI Agent serving endpoint for {{.project_name}}

from agent.serve import run

run(endpoint_name="{{.agent_endpoint_name}}", llm_model="{{.llm_model}}")

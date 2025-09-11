# Databricks notebook source
# COMMAND ----------
# Interactive model registration and validation for {{.project_name}}

from ds.register import run as register

experiment = "/Shared/{{.project_name}}/experiments/train"
model_name = "{{.project_name}}-model"

register(experiment=experiment, model_name=model_name)

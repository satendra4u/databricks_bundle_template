# Databricks notebook source
# COMMAND ----------
# Interactive training notebook for {{.project_name}}

from ds.train import run

training_table = "curated.output"
experiment = "/Shared/{{.project_name}}/experiments/train"
model_name = "{{.project_name}}-model"

run(training_table=training_table, experiment=experiment, model_name=model_name)

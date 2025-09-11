# Databricks notebook source
# COMMAND ----------
# Interactive preprocessing notebook for {{.project_name}}

from ds.preprocess import run

# Example parameters (replace or parameterize via widgets)
input_table = "raw.input"
output_table = "curated.output"
catalog = None
schema = None

run(input_table=input_table, output_table=output_table, catalog=catalog, schema=schema)

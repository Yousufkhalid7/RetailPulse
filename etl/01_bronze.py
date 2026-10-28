# Databricks notebook source
display(dbutils.fs.ls("/Volumes/workspace/retailpulse/raw/"))

#Reading data as raw texts
from pyspark.sql import functions as F
raw_path = "/Volumes/workspace/retailpulse/raw/Sales_Transactions.csv"

df_raw = (
    spark.read.option("header", True).option("inferSchema", False).csv(raw_path)
)

df_raw.printSchema()
print(df_raw.count())

df_bronze = (
    df_raw
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_source_file", F.col("_metadata.file_path"))
)

(df_bronze.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.retailpulse.bronze_sales_transactions"))

bronze = spark.table("workspace.retailpulse.bronze_sales_transactions")
print("Rows: ", bronze.count())

source_cols = [c for c in bronze.columns if not c.startswith("_")]
total = bronze.count()
distinct = bronze.select(source_cols).dropDuplicates().count()
print("duplicate rows kept:", total - distinct)

(bronze
 .filter(~F.col("CustomerNo").rlike("^[0-9]+$"))
 .groupBy("CustomerNo").count()
 .show())
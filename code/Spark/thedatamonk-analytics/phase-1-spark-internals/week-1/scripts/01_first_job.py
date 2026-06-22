#!/usr/bin/env python3
"""
Week 1 - First Spark Job
Demonstrates basic Spark initialization and data loading
"""

from pyspark.sql import SparkSession

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("FirstSparkJob") \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()

print("\n" + "="*60)
print("SPARK SESSION INITIALIZED")
print("="*60)
print(f"Spark Version: {spark.version}")
print(f"Master: {spark.sparkContext.master}")
print(f"App ID: {spark.sparkContext.applicationId}")

# Read CSV file
csv_path = "../data/sample.csv"
df = spark.read.csv(csv_path, header=True, inferSchema=True)

print("\n" + "="*60)
print("DATA LOADED")
print("="*60)
print(f"File: {csv_path}")
print(f"Rows: {df.count()}")
print(f"Columns: {len(df.columns)}")

# Display schema
print("\nSchema:")
df.printSchema()

# Display data
print("\nData Preview:")
df.show()

# Basic statistics
print("\nStatistics:")
df.describe().show()

# Calculate some metrics
print("\nAnalysis:")
print(f"Average Salary: ${df.agg({'salary': 'avg'}).collect()[0][0]:.2f}")
print(f"Max Salary: ${df.agg({'salary': 'max'}).collect()[0][0]:.2f}")
print(f"Min Salary: ${df.agg({'salary': 'min'}).collect()[0][0]:.2f}")

# Show execution plan (important for understanding DAG)
print("\n" + "="*60)
print("EXECUTION PLAN (Explains)")
print("="*60)
df.explain()

print("\n✅ Job completed successfully!")
print("="*60)
print("\nOpen Spark UI at: http://localhost:4040")
print("While this script is running or just after it finishes.\n")

spark.stop()

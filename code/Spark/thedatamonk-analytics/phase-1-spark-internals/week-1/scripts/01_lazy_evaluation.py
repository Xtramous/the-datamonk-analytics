#!/usr/bin/env python3
"""
Demonstrates Spark lazy evaluation
Transformations are lazy, actions trigger execution
"""

from pyspark.sql import SparkSession
import time

spark = SparkSession.builder \
    .appName("LazyEvaluation") \
    .getOrCreate()

df = spark.read.csv("../data/sample.csv", header=True, inferSchema=True)

print("\n" + "="*60)
print("LAZY EVALUATION DEMO")
print("="*60)

# Transformation 1 - LAZY (no output)
print("\n1. Applying transformation (LAZY)...")
print("   df.filter(df.age > 25)")
start = time.time()
filtered_df = df.filter(df.age > 25)
elapsed = time.time() - start
print(f"   ⚡ Execution time: {elapsed:.4f} seconds")
print("   ℹ️  No action triggered - just building DAG")

# Transformation 2 - LAZY (no output)
print("\n2. Applying another transformation (LAZY)...")
print("   filtered_df.select('name', 'salary')")
start = time.time()
selected_df = filtered_df.select("name", "salary")
elapsed = time.time() - start
print(f"   ⚡ Execution time: {elapsed:.4f} seconds")
print("   ℹ️  Still building DAG - no actual data processing")

# ACTION 1 - EAGER (output)
print("\n3. Triggering ACTION (.show())...")
start = time.time()
selected_df.show()
elapsed = time.time() - start
print(f"   ⚡ Execution time: {elapsed:.4f} seconds")
print("   ✅ NOW Spark executes all transformations!")

spark.stop()
print("\n" + "="*60)

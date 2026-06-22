#!/usr/bin/env python3
"""
Long-running Spark job to explore the Spark UI
"""

from pyspark.sql import SparkSession
import time

spark = SparkSession.builder \
    .appName("SparkUiDemo") \
    .getOrCreate()

print("\n" + "="*60)
print("🔥 SPARK UI AVAILABLE!")
print("="*60)
print("\n📊 Open Spark UI in your browser:")
print("   http://localhost:4040")
print("\nThe UI will be available for 120 seconds...")
print("="*60 + "\n")

# Read CSV
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "../data/sample.csv")
df = spark.read.csv(csv_path, header=True, inferSchema=True)

# Perform some operations (visible in Spark UI)
print("Running transformations...")
result = df.filter(df.salary > 75000).groupBy("city").count()
result.show()

print("\n✅ Check the Spark UI now at http://localhost:4040")
print("⏱️  The UI will stay active for 120 more seconds...\n")

# Keep the job alive so you can explore the UI
print("\n⏱️  Spark UI will be available for the next 180 seconds...")
print("📍 Check port 4040 or 4041 if 4040 is busy\n")
time.sleep(180)

spark.stop()
print("✅ Spark session stopped")

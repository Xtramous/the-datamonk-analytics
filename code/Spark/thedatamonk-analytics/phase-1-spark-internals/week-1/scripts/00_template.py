#!/usr/bin/env python3
"""
Template script for Spark learning
Copy this and modify for your exercises
"""

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MyApp") \
    .getOrCreate()

try:
    # Your code here
    print("Hello from Spark from nitin!")
    
finally:
    spark.stop()

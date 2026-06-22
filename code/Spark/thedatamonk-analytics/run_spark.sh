#!/bin/bash
# Wrapper script to run Spark with proper environment variables

# Set environment
export JAVA_HOME=/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home
export SPARK_HOME=/opt/homebrew/opt/apache-spark/libexec
export PATH=$JAVA_HOME/bin:$SPARK_HOME/bin:$PATH

# Handle arguments
if [ $# -eq 0 ]; then
  echo "Usage: ./run_spark.sh <script.py> [args...]"
  echo ""
  echo "Example:"
  echo "  ./run_spark.sh phase-1-spark-internals/week-1/scripts/01_first_job.py"
  exit 1
fi

# Run the Spark script
python3 "$@"

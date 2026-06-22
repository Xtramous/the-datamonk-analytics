#!/bin/bash
# Wrapper to run Jupyter with Spark environment

export JAVA_HOME=/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home
export SPARK_HOME=/opt/homebrew/opt/apache-spark/libexec
export PATH=$JAVA_HOME/bin:$SPARK_HOME/bin:$PATH

echo "🚀 Starting Jupyter Lab with Spark environment..."
echo "📊 Open your browser at: http://localhost:8888"
echo ""

jupyter lab

#!/bin/bash
# Verification script for Spark setup

echo "========================================"
echo "SPARK SETUP VERIFICATION"
echo "========================================"
echo ""

echo "✓ Checking Java..."
java -version 2>&1 | head -1
echo ""

echo "✓ Checking Spark..."
spark-shell --version 2>&1 | head -1
echo ""

echo "✓ Checking Python..."
python3 --version
echo ""

echo "✓ Checking PySpark..."
python3 -c "import pyspark; print(f'PySpark: {pyspark.__version__}')" 2>/dev/null || echo "PySpark: Not installed"

echo "✓ Checking Jupyter..."
python3 -c "import jupyter; print('Jupyter: Installed')" 2>/dev/null || echo "Jupyter: Not installed"

echo "✓ Checking Data..."
if [ -f ~/code/spark/phase-1-spark-internals/week-1/data/sample.csv ]; then
  echo "Sample data: ✅ Found"
else
  echo "Sample data: ❌ Missing"
fi

echo "✓ Checking Project Structure..."
total_dirs=$(find ~/code/spark -type d -name "week-*" | wc -l)
echo "Weeks created: $total_dirs"

echo ""
echo "========================================"
echo "TEST RUN"
echo "========================================"
echo ""
echo "To test your Spark setup, run:"
echo "  cd ~/code/spark/phase-1-spark-internals/week-1/scripts"
echo "  python3 01_first_job.py"
echo ""
echo "Then visit: http://localhost:4040"
echo ""

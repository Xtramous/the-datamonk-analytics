# 🔧 VS Code Quick Start Guide

## What You Should See in VS Code

When VS Code opens with the Spark folder, you'll see:

```
📁 spark (root folder)
├── 📁 phase-1-spark-internals
│   ├── 📁 week-1
│   │   ├── 📁 data
│   │   │   └── 📄 sample.csv
│   │   ├── 📁 scripts
│   │   │   ├── 📄 00_template.py          ← Copy this for new scripts
│   │   │   ├── 📄 01_first_job.py         ← Example #1 (READY TO RUN ✅)
│   │   │   └── 📄 01_lazy_evaluation.py   ← Example #2 (READY TO RUN ✅)
│   │   ├── 📁 notebooks
│   │   ├── 📁 output                      ← Results will save here
│   │   └── 📁 config
│   ├── 📁 week-2
│   ├── 📁 week-3
│   └── 📁 week-4
├── 📁 phase-2-streaming
├── 📁 phase-3-system-design
├── 📄 run_spark.sh                        ← Script runner
├── 📄 run_jupyter.sh                      ← Jupyter launcher
└── 📄 FOLDER_GUIDE.md                     ← Folder reference
```

---

## 3 Example Scripts Explained

### 1️⃣ **00_template.py** (COPY THIS FOR NEW SCRIPTS)
```python
#!/usr/bin/env python3
"""Template script for Spark learning"""

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MyApp") \
    .getOrCreate()

try:
    # Your code here
    print("Hello from Spark!")
    
finally:
    spark.stop()
```
✅ **Purpose:** Use as starting point for all new scripts
📋 **How to use:** `cp 00_template.py my_script.py` then edit

---

### 2️⃣ **01_first_job.py** (READY TO RUN)
```python
#!/usr/bin/env python3
"""Week 1 - First Spark Job"""

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("FirstSparkJob") \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()

# Read data
df = spark.read.csv("../data/sample.csv", header=True, inferSchema=True)

# Show results
print("Data loaded:")
df.show()

print("Schema:")
df.printSchema()

print("Statistics:")
df.describe().show()

print("Analysis:")
print(f"Average Salary: ${df.agg({'salary': 'avg'}).collect()[0][0]:.2f}")
print(f"Max Salary: ${df.agg({'salary': 'max'}).collect()[0][0]:.2f}")
print(f"Min Salary: ${df.agg({'salary': 'min'}).collect()[0][0]:.2f}")

print("Execution Plan:")
df.explain()

spark.stop()
```

✅ **What it does:**
- Loads sample.csv (10 rows, 5 columns)
- Shows data and schema
- Calculates statistics
- Displays execution plan

🚀 **Run it:**
```bash
cd ~/code/spark
./run_spark.sh phase-1-spark-internals/week-1/scripts/01_first_job.py
```

---

### 3️⃣ **01_lazy_evaluation.py** (DEMONSTRATES KEY CONCEPT)
```python
#!/usr/bin/env python3
"""Demonstrates Spark lazy evaluation"""

from pyspark.sql import SparkSession
import time

spark = SparkSession.builder \
    .appName("LazyEvaluation") \
    .getOrCreate()

df = spark.read.csv("../data/sample.csv", header=True, inferSchema=True)

# Transformation 1 - LAZY (no execution, just builds DAG)
print("1. df.filter(df.age > 25)")
start = time.time()
filtered_df = df.filter(df.age > 25)
print(f"   Time: {time.time() - start:.4f}s (NO EXECUTION)")

# Transformation 2 - LAZY (no execution, extends DAG)
print("2. filtered_df.select('name', 'salary')")
start = time.time()
selected_df = filtered_df.select("name", "salary")
print(f"   Time: {time.time() - start:.4f}s (NO EXECUTION)")

# ACTION - EAGER (NOW execution happens!)
print("3. selected_df.show()")
start = time.time()
selected_df.show()
print(f"   Time: {time.time() - start:.4f}s (EXECUTION HAPPENS HERE!)")

spark.stop()
```

✅ **What it demonstrates:**
- Transformations (filter, select) are lazy - instant!
- Actions (show()) trigger actual execution
- Build complex DAGs without running code

🚀 **Run it:**
```bash
cd ~/code/spark
./run_spark.sh phase-1-spark-internals/week-1/scripts/01_lazy_evaluation.py
```

---

## 🎯 Your First Task

1. **Open the folder** (already done - VS Code should be opening)

2. **Navigate to scripts folder:**
   - Click: `phase-1-spark-internals` → `week-1` → `scripts`

3. **Open the first example:**
   - Click: `01_first_job.py`
   - Read through the code

4. **Run it:**
   - Open Terminal in VS Code (Ctrl+`)
   - Run:
   ```bash
   cd ~/code/spark
   ./run_spark.sh phase-1-spark-internals/week-1/scripts/01_first_job.py
   ```

5. **Watch the output:**
   - See data loaded and displayed
   - See statistics calculated
   - See execution plan (DAG)

6. **Monitor the job:**
   - While it runs, open: http://localhost:4040
   - See the Spark UI with job details

---

## 📝 Create Your First Script

```bash
# 1. Copy the template
cd ~/code/spark/phase-1-spark-internals/week-1/scripts
cp 00_template.py 02_my_analysis.py

# 2. Edit the file in VS Code
# Replace the comment with:
df = spark.read.csv("../data/sample.csv", header=True, inferSchema=True)
df.filter(df.salary > 75000).show()

# 3. Save the file

# 4. Run it
cd ~/code/spark
./run_spark.sh phase-1-spark-internals/week-1/scripts/02_my_analysis.py
```

---

## 📊 Sample Data Structure

Your script reads from: `../data/sample.csv`

```
id,name,age,city,salary
1,Alice,28,New York,75000
2,Bob,34,San Francisco,95000
3,Charlie,25,Seattle,65000
4,Diana,31,Austin,85000
5,Eve,29,Boston,80000
6,Frank,36,Denver,90000
7,Grace,27,Chicago,70000
8,Henry,32,Portland,78000
9,Ivy,30,Austin,82000
10,Jack,28,Seattle,72000
```

---

## 🔍 Monitor Your Jobs

While your script runs (or just after):

**Open:** http://localhost:4040

You'll see:
- **Jobs** tab → see your job execution
- **Stages** tab → see execution stages
- **Tasks** tab → see individual tasks
- **Executors** tab → see worker processes
- **SQL** tab → see SQL queries (if using SQL)

---

## 🎓 Next Steps

1. ✅ Run `01_first_job.py` to understand data loading
2. ✅ Run `01_lazy_evaluation.py` to understand lazy execution
3. ✅ Create your first script using template
4. ✅ Read Week 1 theory: `week1_theory_spark_execution_model_dag_generation.html`
5. ✅ Complete the exercises in the theory document

---

## 💡 Tips

- **Always use relative paths:** `../data/` and `../output/`
- **Save results:** `df.write.csv("../output/results")`
- **Take screenshots** of Spark UI and save to `../output/`
- **Document your code:** Add comments explaining what you're doing
- **Keep it organized:** One script per concept/exercise

---

**Happy coding! 🚀**

# Spark Learning Project - Complete Structure & Setup

## 🎯 Overview

This document explains:
1. **What gets installed and where**
2. **How everything connects**
3. **Directory structure for 12-week program**
4. **File locations and purposes**

---

## 📦 Installation Flow (Step-by-Step)

```
STEP 1: Homebrew
   └─ Package manager for macOS
   └─ Installed to: /usr/local/Cellar/homebrew/

STEP 2: Java JDK 11
   └─ Required by Spark
   └─ Installed to: /usr/local/opt/openjdk@11/
   └─ Add to ~/.zprofile: export JAVA_HOME=$(/usr/libexec/java_home -v 11)

STEP 3: Apache Spark
   └─ Distributed compute engine
   └─ Installed to: /usr/local/opt/apache-spark/libexec/
   └─ Add to ~/.zprofile: export SPARK_HOME=/usr/local/opt/apache-spark/libexec

STEP 4: Python Packages
   └─ pyspark, jupyter, pandas, numpy, etc.
   └─ Installed to: ~/.local/lib/python3.X/site-packages/
   └─ Use: requirements.txt

STEP 5: Project Structure
   └─ Your learning materials
   └─ Location: ~/code/spark/
   └─ 12 weeks of organized content
```

---

## 🗂️ Directory Structure

```
~/code/spark/                          (Root project directory)
│
├── 📄 README.md                       (Project overview)
├── 📄 requirements.txt                (Python dependencies)
├── 📄 00_SPARK_COMPLETE_SETUP_GUIDE.html  (This setup guide)
├── 📄 PROJECT_STRUCTURE_REFERENCE.md (This file)
│
├── 📁 phase-1-spark-internals/       (Weeks 1-4: Spark fundamentals)
│   ├── 📁 week-1/                    (Spark Execution Model & DAG)
│   │   ├── 📁 data/                  (Input data: CSV, JSON)
│   │   │   └── sample.csv            (Sample dataset)
│   │   │
│   │   ├── 📁 scripts/               (Python scripts)
│   │   │   ├── 00_template.py        (Template for new scripts)
│   │   │   ├── 01_first_job.py       (First working example)
│   │   │   ├── 01_lazy_evaluation.py (Lazy evaluation demo)
│   │   │   └── 02_multi_stage_dag.py (DAG visualization)
│   │   │
│   │   ├── 📁 notebooks/             (Jupyter notebooks)
│   │   │   └── week1_exploration.ipynb
│   │   │
│   │   ├── 📁 output/                (Results, screenshots, logs)
│   │   │   ├── dag_screenshot.png
│   │   │   └── week1_analysis.md
│   │   │
│   │   └── 📁 config/                (Configuration files)
│   │       └── log4j.properties      (Logging configuration)
│   │
│   ├── 📁 week-2/                    (Catalyst Optimizer)
│   │   └── (Same structure: data/, scripts/, notebooks/, output/, config/)
│   │
│   ├── 📁 week-3/                    (Tungsten & Memory Management)
│   │   └── (Same structure)
│   │
│   └── 📁 week-4/                    (Shuffle & Broadcast)
│       └── (Same structure)
│
├── 📁 phase-2-streaming/              (Weeks 5-8: Streaming & Kafka)
│   ├── 📁 week-5/                    (CAP Theorem)
│   ├── 📁 week-6/                    (Replication & Consensus)
│   ├── 📁 week-7/                    (Kafka Internals)
│   └── 📁 week-8/                    (Spark Structured Streaming)
│
└── 📁 phase-3-system-design/         (Weeks 9-12: Architecture & Operations)
    ├── 📁 week-9/                    (System Design Framework)
    ├── 📁 week-10/                   (CDC & Data Modeling)
    ├── 📁 week-11/                   (Reliability & SLA/SLO)
    └── 📁 week-12/                   (Cost Optimization & Design Challenges)
```

---

## 🔌 How Everything Connects

### 1. **Environment Variables** (Stored in ~/.zprofile)

```bash
# ~/.zprofile (Shell configuration file)

# Java
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export PATH=$JAVA_HOME/bin:$PATH

# Spark
export SPARK_HOME=/usr/local/opt/apache-spark/libexec
export PATH=$SPARK_HOME/bin:$PATH

# When you open Terminal, these variables are loaded automatically
# Allows you to run: java, spark-shell, spark-submit from anywhere
```

### 2. **Spark Installation Locations** (macOS with Homebrew)

```
/usr/local/opt/apache-spark/libexec/
├── bin/                    ← Contains spark-shell, spark-submit, pyspark
├── conf/                   ← Default configuration
│   ├── log4j.properties    ← Logging config
│   └── spark-defaults.conf ← Default settings
├── jars/                   ← Spark Java libraries
└── python/                 ← PySpark implementation
```

### 3. **Python Packages** (installed via pip3)

```
~/.local/lib/python3.X/site-packages/
├── pyspark/                ← Spark Python API
├── jupyter/                ← Interactive notebooks
├── pandas/                 ← Data manipulation
├── numpy/                  ← Numerical computing
├── matplotlib/             ← Plotting
└── (other packages)
```

### 4. **Your Project** (~/code/spark/)

```
~/code/spark/
└── Contains:
    - Learning materials organized by week
    - Sample data
    - Scripts you write
    - Notebooks for exploration
    - Config files for Spark jobs
```

---

## ⚙️ How Spark Finds Everything

When you run a Spark job:

```
1. Terminal loads ~/.zprofile
   ├─ Sets JAVA_HOME → Spark knows where Java is
   └─ Sets SPARK_HOME → Spark knows where Spark is

2. You run: python3 script.py
   ├─ Python interpreter starts
   └─ Your script runs

3. Your script does: SparkSession.builder.getOrCreate()
   ├─ Spark creates a session
   ├─ Finds Java from JAVA_HOME
   ├─ Loads Spark from SPARK_HOME
   ├─ Creates Driver process
   └─ Starts Executor threads

4. You read data: spark.read.csv("../data/sample.csv")
   ├─ Spark finds file relative to script location
   └─ Creates RDD

5. You trigger action: df.show()
   ├─ Spark builds execution plan (DAG)
   ├─ Executors process data
   └─ Results display in console

6. Spark UI available at: http://localhost:4040
   └─ While job is running or just after
```

---

## 📝 File Purposes & What Goes Where

### **data/ folder**
- **Purpose:** Store input datasets
- **What goes here:** CSV, JSON, Parquet files
- **Examples:**
  - `sample.csv` - Test dataset
  - `users.csv` - User data
  - `transactions.json` - Event log

### **scripts/ folder**
- **Purpose:** Store Python/Scala Spark code
- **What goes here:** Runnable Spark jobs
- **Examples:**
  - `01_lazy_evaluation.py` - Learning code
  - `02_multi_stage_dag.py` - Hands-on lab
  - `03_shuffles_demo.py` - Concept demonstration

### **notebooks/ folder**
- **Purpose:** Interactive exploration
- **What goes here:** Jupyter notebooks (.ipynb)
- **Examples:**
  - `week1_exploration.ipynb` - Notes + analysis
  - `dag_analysis.ipynb` - Visual DAG study

### **output/ folder**
- **Purpose:** Store results and analysis
- **What goes here:** Screenshots, CSV results, analysis notes
- **Examples:**
  - `dag_screenshot.png` - DAG visualization
  - `week1_analysis.md` - Analysis notes
  - `results.csv` - Spark query output

### **config/ folder**
- **Purpose:** Store configuration files
- **What goes here:** log4j.properties, spark-defaults.conf
- **Examples:**
  - `log4j.properties` - Logging level settings
  - `spark-defaults.conf` - Default Spark config

---

## 🚀 How to Use This Setup

### **Writing Your First Spark Script**

```python
# File: ~/code/spark/phase-1-spark-internals/week-1/scripts/my_script.py

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MyJob") \
    .getOrCreate()

# Spark automatically finds:
# - Java from JAVA_HOME
# - Itself from SPARK_HOME
# - Libraries from ~/.local/lib/python3.X/site-packages/

df = spark.read.csv("../data/sample.csv", header=True)
df.show()

spark.stop()
```

### **Running Your Script**

```bash
cd ~/code/spark/phase-1-spark-internals/week-1/scripts
python3 my_script.py

# What happens:
# 1. Shell loads ~/.zprofile (JAVA_HOME, SPARK_HOME set)
# 2. Python starts your script
# 3. Script creates Spark session
# 4. Spark uses JAVA_HOME + SPARK_HOME to initialize
# 5. Job runs using sample.csv from ../data/
# 6. Results printed to console
```

### **Monitoring with Spark UI**

```bash
# While script is running (or right after):
# Open browser: http://localhost:4040
# View: DAG, stages, tasks, execution time
```

### **Using Jupyter Notebooks**

```bash
cd ~/code/spark
jupyter lab

# Opens http://localhost:8888
# Create new notebook
# Write PySpark code cell by cell
# See results immediately
```

---

## 🔍 Verification: How to Check Everything

```bash
# Check Java
java -version
echo $JAVA_HOME

# Check Spark
spark-shell --version
echo $SPARK_HOME

# Check Python
python3 --version

# Check PySpark
python3 -c "import pyspark; print(pyspark.__version__)"

# Check Jupyter
jupyter --version

# Check project structure
ls -la ~/code/spark/
```

---

## 📊 12-Week Program Organization

```
PHASE 1: Spark Fundamentals (Weeks 1-4)
├─ Week 1: Execution Model & DAG
├─ Week 2: Catalyst Optimizer
├─ Week 3: Tungsten & Memory
└─ Week 4: Shuffle & Broadcast

PHASE 2: Streaming & Distributed Systems (Weeks 5-8)
├─ Week 5: CAP Theorem
├─ Week 6: Replication & Consensus
├─ Week 7: Kafka Internals
└─ Week 8: Spark Structured Streaming

PHASE 3: System Design & Operations (Weeks 9-12)
├─ Week 9: System Design Framework
├─ Week 10: CDC & Data Modeling
├─ Week 11: Reliability Engineering
└─ Week 12: Cost Optimization

Each week has: data/, scripts/, notebooks/, output/, config/
```

---

## 💾 File Structure Summary

```
Installation:
├─ Homebrew       → /usr/local/
├─ Java          → /usr/local/opt/openjdk@11/
├─ Spark         → /usr/local/opt/apache-spark/
└─ Python packages → ~/.local/lib/python3.X/

Configuration:
└─ ~/.zprofile    ← JAVA_HOME, SPARK_HOME

Learning:
└─ ~/code/spark/  ← Your 12-week materials
   ├─ phase-1/ (weeks 1-4)
   ├─ phase-2/ (weeks 5-8)
   └─ phase-3/ (weeks 9-12)
```

---

## ✅ Ready to Start?

1. Run the setup guide: `00_SPARK_COMPLETE_SETUP_GUIDE.html`
2. Follow steps 1-10 to install everything
3. Verify with the checklist
4. Run your first job: `01_first_job.py`
5. Start Week 1 learning materials

**Total setup time: 15-25 minutes**

---

**Last Updated:** June 16, 2026  
**For:** 12-Week L5 Data Engineer Intensive Program

# 📁 Folder Structure Guide - Where to Write Code & Output

## Root: ~/code/spark/

```
~/code/spark/
│
├── 📄 README.md                              (Program overview)
├── 📄 INSTALLATION_COMPLETE.md              (Installation summary)
├── 📄 PROJECT_STRUCTURE_REFERENCE.md        (How everything connects)
├── 📄 requirements.txt                      (Python dependencies)
├── 🔧 run_spark.sh                         (Wrapper to run scripts)
├── 🔧 run_jupyter.sh                       (Wrapper for Jupyter)
├── 🔧 VERIFY_SETUP.sh                      (Verify installation)
│
├── 📁 phase-1-spark-internals/              (Weeks 1-4: Spark Fundamentals)
├── 📁 phase-2-streaming/                   (Weeks 5-8: Streaming & Distributed Systems)
└── 📁 phase-3-system-design/               (Weeks 9-12: System Design & Operations)
```

---

## Phase Structure (Example: Phase 1)

```
~/code/spark/phase-1-spark-internals/
│
├── 📁 week-1/                   (Spark Execution Model & DAG)
├── 📁 week-2/                   (Catalyst Optimizer)
├── 📁 week-3/                   (Tungsten & Memory Management)
└── 📁 week-4/                   (Shuffle & Broadcast)
```

---

## Week Structure (Each week has this layout)

```
~/code/spark/phase-1-spark-internals/week-1/
│
├── 📁 data/                     ← READ DATA FROM HERE
│   └── sample.csv              (Sample dataset - 10 rows)
│
├── 📁 scripts/                  ← WRITE YOUR CODE HERE ⭐
│   ├── 00_template.py           (Copy this for new scripts)
│   ├── 01_first_job.py          (Example script - tested ✅)
│   ├── 01_lazy_evaluation.py    (Example script)
│   ├── MY_SCRIPT_1.py           (Your script goes here)
│   ├── MY_SCRIPT_2.py           (Your script goes here)
│   └── ...
│
├── 📁 notebooks/                ← INTERACTIVE EXPLORATION
│   ├── week1_exploration.ipynb  (Jupyter notebook)
│   └── my_analysis.ipynb        (Your notebook goes here)
│
├── 📁 output/                   ← SAVE OUTPUT HERE ⭐
│   ├── results.csv              (CSV output from your scripts)
│   ├── analysis.txt             (Text results)
│   ├── dag_screenshot.png       (Screenshots from Spark UI)
│   ├── week1_summary.md         (Your analysis notes)
│   └── ...
│
└── 📁 config/
    └── log4j.properties         (Logging configuration)
```

---

## WHERE TO DO WHAT

### 📝 Write Spark Code
**Location:** `~/code/spark/phase-X-name/week-Y/scripts/`

**How to create a new script:**
1. Copy template: `cp 00_template.py my_first_analysis.py`
2. Edit in VS Code or text editor
3. Run it:
   ```bash
   cd ~/code/spark
   ./run_spark.sh phase-1-spark-internals/week-1/scripts/my_first_analysis.py
   ```

**Example script structure:**
```python
#!/usr/bin/env python3
"""Week 1 - My First Analysis"""

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MyAnalysis") \
    .getOrCreate()

# Read data from data/ folder
df = spark.read.csv("../data/sample.csv", header=True, inferSchema=True)

# Your analysis here
df.show()

# Save results to output/ folder (optional)
# df.coalesce(1).write.mode("overwrite").csv("../output/results")

spark.stop()
```

---

### 📊 Interactive Exploration (Jupyter)
**Location:** `~/code/spark/phase-X-name/week-Y/notebooks/`

**How to use:**
```bash
cd ~/code/spark
./run_jupyter.sh
# Opens http://localhost:8888
# Create new notebook or edit existing ones
```

**Inside Jupyter notebook:**
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("JupyterExploration") \
    .getOrCreate()

# Read from ../data/
df = spark.read.csv("../data/sample.csv", header=True, inferSchema=True)
df.show()
df.printSchema()
```

---

### 📁 Read Input Data
**Location:** `~/code/spark/phase-X-name/week-Y/data/`

**Available files:**
- `sample.csv` — 10 sample rows (id, name, age, city, salary)

**How to read in your script:**
```python
# Inside scripts/ folder:
df = spark.read.csv("../data/sample.csv", header=True, inferSchema=True)

# Or use absolute path:
df = spark.read.csv("/Users/nitinkamal/code/spark/phase-1-spark-internals/week-1/data/sample.csv", header=True)
```

---

### 💾 Save Output/Results
**Location:** `~/code/spark/phase-X-name/week-Y/output/`

**Save CSV results:**
```python
# Inside your script
df_results = df.filter(df.salary > 75000)

# Save to output folder
df_results.write.mode("overwrite").csv("../output/high_salary_results")
```

**Save as single file:**
```python
df_results.coalesce(1).write.mode("overwrite").csv("../output/single_file_result")
```

**Save summary text:**
```python
with open("../output/analysis_summary.txt", "w") as f:
    f.write("Analysis Results:\n")
    f.write(f"Total rows: {df.count()}\n")
    f.write(f"Avg salary: ${df.agg({'salary': 'avg'}).collect()[0][0]:.2f}\n")
```

**Save Spark UI screenshots:**
- While your script runs, Spark UI shows at: http://localhost:4040
- Take screenshots and save to `output/`

**Store analysis notes:**
```markdown
# Week 1 Analysis Notes

## Date
June 19, 2026

## What I Did
- Loaded sample.csv
- Filtered by salary > 75000
- Calculated statistics

## Key Findings
- Average salary: $79,200
- Highest paid: Bob ($95,000)
```

Save this as: `~/code/spark/phase-1-spark-internals/week-1/output/week1_summary.md`

---

## 📊 Data Flow Diagram

```
WEEK DIRECTORY
│
├─ data/               ← INPUT
│   └─ sample.csv     (Read data from here in your scripts)
│
├─ scripts/           ← YOUR CODE
│   ├─ 00_template.py (Copy this for new scripts)
│   └─ my_script.py   (Your code: reads from ../data/, writes to ../output/)
│
└─ output/            ← OUTPUT
    ├─ results.csv    (Spark DataFrame output)
    ├─ summary.txt    (Analysis results)
    └─ notes.md       (Your observations)
```

---

## Quick Reference Table

| Task | Location | Command |
|------|----------|---------|
| Write new Spark script | `scripts/` | `cp 00_template.py my_script.py` |
| Run your script | From `~/code/spark/` | `./run_spark.sh phase-1-spark-internals/week-1/scripts/my_script.py` |
| Read input data | `data/` | `spark.read.csv("../data/sample.csv", ...)` |
| Save results | `output/` | `df.write.csv("../output/results")` |
| Use Jupyter | `notebooks/` | `./run_jupyter.sh` then create `.ipynb` file |
| Save notes | `output/` | Save `.md` or `.txt` files there |
| Monitor job | Browser | http://localhost:4040 (while job runs) |

---

## Path Examples

### Absolute Paths
```python
# If you need absolute paths (not relative):
data_path = "/Users/nitinkamal/code/spark/phase-1-spark-internals/week-1/data/sample.csv"
output_path = "/Users/nitinkamal/code/spark/phase-1-spark-internals/week-1/output/results"

df = spark.read.csv(data_path, header=True)
df.write.csv(output_path)
```

### Relative Paths (Recommended)
```python
# Scripts are in: ~/code/spark/phase-1-spark-internals/week-1/scripts/
# So relative paths work perfectly:

df = spark.read.csv("../data/sample.csv", header=True)        # Read input
df.write.csv("../output/results")                              # Save output
```

---

## Organization Tips

**For each week:**

1. **Create your scripts in `scripts/` folder:**
   ```bash
   01_first_exploration.py        (Initial data exploration)
   02_transformations.py          (Data transformations)
   03_analysis.py                 (Statistical analysis)
   04_optimization.py             (Performance tuning)
   ```

2. **Create notebooks in `notebooks/` folder:**
   ```bash
   week1_exploration.ipynb        (Interactive exploration)
   week1_learning_notes.ipynb     (Study notes with code)
   ```

3. **Keep outputs in `output/` folder:**
   ```bash
   results_*.csv                  (Output data files)
   screenshots/                   (Spark UI screenshots)
   summary.txt                    (Results summary)
   notes.md                       (Your observations)
   ```

4. **Input data in `data/` folder:**
   ```bash
   sample.csv                     (Provided sample)
   custom_data.csv               (Your test data if needed)
   ```

---

## Complete 12-Week Layout

```
~/code/spark/
│
├── phase-1-spark-internals/
│   ├── week-1/
│   │   ├── data/
│   │   ├── scripts/         ← Write code here (Week 1)
│   │   ├── notebooks/       ← Jupyter exploration (Week 1)
│   │   └── output/          ← Save results here (Week 1)
│   ├── week-2/
│   │   ├── data/
│   │   ├── scripts/         ← Write code here (Week 2)
│   │   ├── notebooks/       ← Jupyter exploration (Week 2)
│   │   └── output/          ← Save results here (Week 2)
│   ├── week-3/ ... same pattern
│   └── week-4/ ... same pattern
│
├── phase-2-streaming/
│   ├── week-5/ ... same pattern
│   ├── week-6/ ... same pattern
│   ├── week-7/ ... same pattern
│   └── week-8/ ... same pattern
│
└── phase-3-system-design/
    ├── week-9/ ... same pattern
    ├── week-10/ ... same pattern
    ├── week-11/ ... same pattern
    └── week-12/ ... same pattern
```

---

## Example Workflow

### Week 1, Day 1: First Script

1. **Create your first script:**
   ```bash
   cd ~/code/spark/phase-1-spark-internals/week-1/scripts
   cp 00_template.py 01_my_first_script.py
   ```

2. **Edit the script** (add your code)

3. **Run it:**
   ```bash
   cd ~/code/spark
   ./run_spark.sh phase-1-spark-internals/week-1/scripts/01_my_first_script.py
   ```

4. **Check Spark UI:** http://localhost:4040

5. **Save outputs:**
   - Results go to: `phase-1-spark-internals/week-1/output/`
   - Screenshots go to: `phase-1-spark-internals/week-1/output/screenshots/`
   - Notes go to: `phase-1-spark-internals/week-1/output/notes.md`

---

**Key Takeaway:**
- ✍️ **Write code** in: `phase-X/week-Y/scripts/`
- 📖 **Explore interactively** in: `phase-X/week-Y/notebooks/`
- 📂 **Read input** from: `phase-X/week-Y/data/`
- 💾 **Save output** to: `phase-X/week-Y/output/`

That's the complete workflow for all 12 weeks!

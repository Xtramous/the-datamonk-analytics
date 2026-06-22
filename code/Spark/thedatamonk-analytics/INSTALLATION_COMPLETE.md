# ✅ Spark Installation Complete

**Date:** June 19, 2026  
**Status:** All 10 installation steps completed successfully

---

## 📋 Installation Summary

### What Was Installed

| Component | Version | Location | Status |
|-----------|---------|----------|--------|
| **Java JDK** | 21.0.11 | `/opt/homebrew/opt/openjdk@21/` | ✅ Verified |
| **Apache Spark** | 4.1.2 | `/opt/homebrew/opt/apache-spark/` | ✅ Verified |
| **Python** | 3.9.6 | System | ✅ Verified |
| **PySpark** | 4.0.3 | `~/.local/lib/python3.9/` | ✅ Verified |
| **Jupyter Lab** | Latest | `~/.local/lib/python3.9/` | ✅ Verified |
| **Pandas** | Latest | `~/.local/lib/python3.9/` | ✅ Verified |
| **NumPy** | Latest | `~/.local/lib/python3.9/` | ✅ Verified |
| **Matplotlib** | Latest | `~/.local/lib/python3.9/` | ✅ Verified |

---

## 📁 Project Structure Created

```
~/code/spark/
├── phase-1-spark-internals/         (Weeks 1-4)
│   ├── week-1/ → week-4/
│   │   ├── data/        (sample.csv ready)
│   │   ├── scripts/     (01_first_job.py tested ✅)
│   │   ├── notebooks/   (ready for Jupyter)
│   │   ├── output/      (for results)
│   │   └── config/      (log4j.properties)
├── phase-2-streaming/               (Weeks 5-8)
│   └── week-5/ → week-8/ (structure ready)
├── phase-3-system-design/          (Weeks 9-12)
│   └── week-9/ → week-12/ (structure ready)
└── Utilities:
    ├── run_spark.sh                 (Wrapper for Spark scripts)
    ├── run_jupyter.sh              (Wrapper for Jupyter)
    ├── VERIFY_SETUP.sh             (Verification script)
    └── requirements.txt             (Python dependencies)
```

---

## ✅ Verification Checklist

- [x] Homebrew installed and working
- [x] Java JDK 21 installed and verified
- [x] Apache Spark 4.1.2 installed and verified
- [x] Python 3.9+ with PySpark
- [x] Jupyter Lab installed
- [x] Pandas, NumPy, Matplotlib installed
- [x] Project directory structure (12 weeks × 3 phases)
- [x] Sample CSV data created
- [x] Spark configuration files (log4j.properties)
- [x] First Spark job runs successfully ✅

---

## 🚀 How to Use

### Run a Spark Script

```bash
cd ~/code/spark
./run_spark.sh phase-1-spark-internals/week-1/scripts/01_first_job.py
```

### Start Jupyter with Spark Environment

```bash
cd ~/code/spark
./run_jupyter.sh
# Opens http://localhost:8888
```

### Quick Verification

```bash
bash ~/code/spark/VERIFY_SETUP.sh
```

---

## 📊 Test Run Result

**First Job: 01_first_job.py** - ✅ SUCCESSFUL

```
✓ Spark Session initialized
✓ Loaded sample.csv (10 rows, 5 columns)
✓ Displayed schema and data preview
✓ Calculated statistics
✓ Generated execution plan (Physical Plan shown)
✓ Job completed in ~5 seconds
```

**Output Highlights:**
- Average Salary: $79,200
- Max Salary: $95,000 (Bob in San Francisco)
- Min Salary: $65,000 (Charlie in Seattle)
- Execution Plan: FileScan CSV format, data loaded from file

---

## 🎯 Next Steps

1. **Read Week 1 Theory:** `~/code/spark/week1_theory_spark_execution_model_dag_generation.html`
2. **Explore the scripts:**
   - `01_first_job.py` - Basic data loading and analysis
   - `01_lazy_evaluation.py` - Demonstrates lazy evaluation
   - Create your own scripts in `scripts/` folders
3. **Use Jupyter Lab** for interactive exploration:
   ```bash
   ./run_jupyter.sh
   ```
4. **Monitor Jobs** - Open Spark UI while jobs run: http://localhost:4040

---

## 🔧 Environment Variables

Your environment is configured in `~/.zprofile`:

```bash
export JAVA_HOME=/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home
export PATH=$JAVA_HOME/bin:$PATH
export SPARK_HOME=/opt/homebrew/opt/apache-spark/libexec
export PATH=$SPARK_HOME/bin:$PATH
```

**Note:** The `run_spark.sh` and `run_jupyter.sh` wrappers automatically set these for you.

---

## 📝 Key Files & Locations

| File | Purpose |
|------|---------|
| `~/code/spark/run_spark.sh` | Run Spark scripts with proper environment |
| `~/code/spark/run_jupyter.sh` | Start Jupyter Lab with Spark |
| `~/code/spark/VERIFY_SETUP.sh` | Verify all components |
| `~/code/spark/phase-1-spark-internals/week-1/scripts/01_first_job.py` | Example Spark job |
| `~/code/spark/phase-1-spark-internals/week-1/data/sample.csv` | Sample data |

---

## ⚠️ Notes

- **Java Version:** Uses OpenJDK 21 (installed as Spark dependency)
- **Spark Version:** 4.1.2 (latest from Homebrew)
- **Python Version:** 3.9.6 (system Python)
- **Installation Time:** ~45 minutes (including package downloads)
- **Network:** Uses pip for package installation (may need retry on network issues)

---

## 🎓 You're Ready!

The complete Spark learning environment is set up and tested. All 12 weeks of materials are organized and ready for learning.

**Estimated Time to Complete 12-Week Program:** 600 hours

---

**Last Updated:** June 19, 2026  
**Maintained by:** Nitin Kamal  
**Program:** L5 Data Engineer Intensive

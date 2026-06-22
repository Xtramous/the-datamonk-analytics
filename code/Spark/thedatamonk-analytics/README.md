# 12-Week Apache Spark Learning Program

## L5 Data Engineer Intensive

**Goal:** Reach Staff-level (L5) data engineer competency through deep mastery of Apache Spark, distributed systems, and data engineering patterns.

### 📊 Program Structure

**Phase 1: Spark Fundamentals (Weeks 1-4)**
- Week 1: Spark Execution Model & DAG Generation
- Week 2: Catalyst Optimizer
- Week 3: Tungsten & Memory Management  
- Week 4: Shuffle Operations & Broadcast

**Phase 2: Streaming & Distributed Systems (Weeks 5-8)**
- Week 5: CAP Theorem & Consistency
- Week 6: Replication & Consensus Algorithms
- Week 7: Kafka Internals
- Week 8: Spark Structured Streaming

**Phase 3: System Design & Operations (Weeks 9-12)**
- Week 9: System Design Framework
- Week 10: CDC & Data Modeling
- Week 11: Reliability Engineering & SLA/SLO
- Week 12: Cost Optimization & Design Challenges

### 🚀 Getting Started

1. **Environment Setup**
   - Spark: 4.1.2 (installed via Homebrew)
   - Java: 21 (OpenJDK)
   - Python: 3.9+
   - Jupyter Lab available

2. **Running Code**
   ```bash
   cd ~/code/spark/phase-1-spark-internals/week-1/scripts
   python3 01_first_job.py
   ```

3. **Monitor Jobs**
   - While job runs, visit: http://localhost:4040
   - View DAG, stages, tasks, executors

4. **Interactive Learning**
   ```bash
   jupyter lab
   # Opens http://localhost:8888
   ```

### 📁 Directory Structure

```
~/code/spark/
├── phase-1-spark-internals/
│   ├── week-1/ → week-4/
│   │   ├── data/       (CSV, JSON input files)
│   │   ├── scripts/    (Python Spark jobs)
│   │   ├── notebooks/  (Jupyter notebooks)
│   │   ├── output/     (Results, screenshots)
│   │   └── config/     (log4j.properties)
├── phase-2-streaming/
│   └── week-5/ → week-8/ (same structure)
├── phase-3-system-design/
│   └── week-9/ → week-12/ (same structure)
└── requirements.txt
```

### ✅ Installation Complete

Verify all components:
```bash
java -version          # Should show Java 21
spark-shell --version  # Should show Spark 4.1.2
python3 -c "import pyspark"
jupyter --version
```

### 📚 Learning Materials

Each week includes:
- **theory_*.html** - Comprehensive study material with diagrams
- **scripts/** - Runnable Spark code examples
- **notebooks/** - Interactive exploration
- **exercises/** - Hands-on practice problems

### 🎯 Success Criteria

- Deep understanding of Spark internals (execution, optimization, memory)
- Mastery of distributed systems concepts (CAP, replication, consensus)
- Experience with streaming platforms (Kafka, Spark Streaming)
- System design thinking (scalability, reliability, cost)
- Ready for L5/Staff-level technical interviews

---

**Last Updated:** June 19, 2026  
**Instructor:** Nitin Kamal  
**Program Duration:** 12 weeks (estimated 600 hours)

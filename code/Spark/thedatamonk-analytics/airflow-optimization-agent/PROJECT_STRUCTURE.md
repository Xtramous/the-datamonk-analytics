# Airflow Optimization Agent - Project Structure

## Complete Project Overview

```
airflow-optimization-agent/
│
├── 📋 Core Documentation (START HERE)
│   ├── README.md                          [700+ lines] Main documentation
│   ├── QUICKSTART.md                      [300 lines]  5-minute setup
│   ├── AGENTIFICATION_ARCHITECTURE.md     [1000+ lines] Technical deep dive
│   ├── IMPLEMENTATION_SUMMARY.md          [300 lines]  What was built
│   └── PROJECT_STRUCTURE.md               [This file]
│
├── ⚙️  Configuration
│   ├── requirements.txt                   [15 dependencies]
│   ├── .env.example                       [Configuration template]
│   └── main.py                            [Entry point]
│
└── 🤖 Source Code (2,500+ lines)
    │
    ├── src/__init__.py
    │
    ├── src/config.py [210 lines]
    │   └─ Configuration management
    │      • API endpoints (Airflow, Prometheus)
    │      • Thresholds (cost, duration, errors)
    │      • Agent settings
    │
    ├── src/api/
    │   ├── __init__.py
    │   ├── airflow_client.py [180 lines]
    │   │   └─ Airflow REST API integration
    │   │      • get_dags()
    │   │      • get_dag_runs()
    │   │      • get_dag_stats()
    │   │      • get_task_instances()
    │   │      • extract_dag_metrics()
    │   │
    │   └── prometheus_client.py [150 lines]
    │       └─ Prometheus metrics fetcher
    │          • query() - Execute PromQL
    │          • get_dag_execution_time()
    │          • get_task_failures()
    │          • get_resource_usage()
    │          • get_dag_metrics()
    │
    ├── src/agents/
    │   ├── __init__.py
    │   ├── analysis_agent.py [200 lines]
    │   │   └─ Claude-powered DAG analysis
    │   │      • analyze_dag_performance()
    │   │      • recommend_optimizations()
    │   │      • prioritize_dags()
    │   │
    │   ├── cost_calculator_agent.py [180 lines]
    │   │   └─ Cost & ROI calculations
    │   │      • estimate_dag_cost()
    │   │      • calculate_roi()
    │   │      • prioritize_by_savings()
    │   │
    │   └── orchestrator.py [250 lines]
    │       └─ Workflow coordination
    │          • run_full_analysis()
    │          • analyze_single_dag()
    │          • _generate_report()
    │          • _generate_next_actions()
    │
    ├── src/storage/
    │   ├── __init__.py
    │   └── pattern_store.py [200 lines]
    │       └─ Chroma vector DB integration
    │          • add_optimization_pattern()
    │          • find_similar_patterns()
    │          • get_patterns_for_technique()
    │          • get_statistics()
    │
    ├── src/tools/
    │   └── __init__.py [reserved for future tools]
    │
    └── src/cli.py [350 lines]
        └─ CLI interface (Typer)
           • analyze-all
           • analyze-dag
           • show-patterns
           • health
           • demo
```

## Component Interactions

### Data Flow Architecture

```
┌─────────────────────────────────────────────────────────┐
│  INPUT: One Command                                     │
│  python -m src.cli analyze-all                         │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  STAGE 1: Data Collection                              │
│                                                         │
│  airflow_client.py                                      │
│  └─ Fetch: DAG list, runs, stats, task instances      │
│                                                         │
│  prometheus_client.py                                   │
│  └─ Query: CPU, memory, execution time, failure rates  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  STAGE 2: Analysis                                      │
│                                                         │
│  analysis_agent.py (Claude)                             │
│  └─ Input: DAG metrics + performance data              │
│  └─ Process: "What are the issues?"                    │
│  └─ Output: Assessment, issues, techniques            │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  STAGE 3: Pattern Matching                              │
│                                                         │
│  pattern_store.py (Chroma)                              │
│  └─ Query: Similar past optimizations                 │
│  └─ Return: Patterns + results + confidence           │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  STAGE 4: Cost-Benefit Analysis                         │
│                                                         │
│  cost_calculator_agent.py (Claude)                      │
│  └─ Input: Resource usage + optimization technique    │
│  └─ Process: "What will this save?"                    │
│  └─ Output: Cost estimates, ROI, payback period       │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  STAGE 5: Recommendations                              │
│                                                         │
│  analysis_agent.py (Claude)                             │
│  └─ Input: Analysis + patterns + costs                │
│  └─ Process: "Generate implementation plan"           │
│  └─ Output: Steps, risks, mitigations                 │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  STAGE 6: Learning                                      │
│                                                         │
│  pattern_store.py (Chroma)                              │
│  └─ Store: Optimization results                       │
│  └─ For future: Pattern reuse + improvements          │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  OUTPUT: Comprehensive Report                           │
│  • Priority order of DAGs                              │
│  • Recommended techniques                              │
│  • Cost-benefit analysis                               │
│  • Implementation plans                                │
│  • Next action items                                   │
│  • JSON report saved: optimization_report.json         │
└─────────────────────────────────────────────────────────┘
```

## Tool Integration Map

```
                ┌─────────────────────┐
                │   Claude API        │
                │  (Analysis Brain)   │
                └──────────┬──────────┘
                           │
    ┌──────────────────────┼──────────────────────┐
    │                      │                      │
    ▼                      ▼                      ▼
┌────────────┐      ┌──────────────┐     ┌──────────────┐
│ Airflow    │      │ Prometheus   │     │  Chroma DB   │
│ REST API   │      │  Metrics     │     │  (Patterns)  │
│            │      │              │     │              │
│ • DAG runs │      │ • CPU usage  │     │ • Techniques │
│ • Duration │      │ • Memory     │     │ • Results    │
│ • Status   │      │ • Failures   │     │ • Confidence │
└────────────┘      └──────────────┘     └──────────────┘
    │                      │                      │
    └──────────────────────┼──────────────────────┘
                           │
                  ┌────────▼────────┐
                  │  Orchestrator   │
                  │  Coordinator    │
                  └────────────────┘
                           │
                  ┌────────▼────────┐
                  │  JSON Report    │
                  │  + Insights     │
                  └────────────────┘
```

## File Dependencies

```
cli.py (Entry point)
  │
  ├── src/agents/orchestrator.py
  │   ├── src/api/airflow_client.py
  │   │   └── src/config.py
  │   ├── src/api/prometheus_client.py
  │   │   └── src/config.py
  │   ├── src/agents/analysis_agent.py
  │   │   └── Uses Claude API
  │   ├── src/agents/cost_calculator_agent.py
  │   │   └── Uses Claude API
  │   └── src/storage/pattern_store.py
  │       └── Uses Chroma DB
  │
  └── src/config.py (Configuration)
```

## Code Statistics

| Component | Files | Lines | Purpose |
|-----------|-------|-------|---------|
| **APIs** | 2 | 330 | Airflow & Prometheus integration |
| **Agents** | 3 | 630 | Analysis, cost, orchestration |
| **Storage** | 1 | 200 | Pattern learning system |
| **CLI** | 1 | 350 | User interface |
| **Config** | 1 | 210 | Settings management |
| **Core** | 8 | 1,720 | Production code |
| **Docs** | 4 | 2,300+ | Complete documentation |
| **TOTAL** | 12 | 4,000+ | Complete system |

## Key Design Patterns

### 1. Client Pattern (Airflow, Prometheus)
```python
class AirflowClient:
    def get_dags(self):
        """Fetch all DAGs"""
        
    def get_dag_runs(self, dag_id):
        """Fetch DAG execution history"""
```

**Why:** Encapsulates API details, enables testing, handles errors gracefully.

### 2. Agent Pattern (Analysis, Cost, Orchestrator)
```python
class AnalysisAgent:
    def analyze_dag_performance(self, metrics):
        """Claude analyzes performance"""
        
    def recommend_optimizations(self, metrics, patterns):
        """Generate implementation plan"""
```

**Why:** Separates concerns, enables independent scaling, promotes reusability.

### 3. Vector DB Pattern (Chroma)
```python
class PatternStore:
    def add_optimization_pattern(self, dag_id, pattern):
        """Store successful optimization"""
        
    def find_similar_patterns(self, problem):
        """Semantic search for similar cases"""
```

**Why:** Enables learning, improves recommendations over time, semantic understanding.

### 4. Orchestrator Pattern
```python
class AgentOrchestrator:
    def run_full_analysis(self):
        """Coordinate all components"""
        # 1. Collect
        # 2. Analyze
        # 3. Prioritize
        # 4. Recommend
        # 5. Learn
        # 6. Report
```

**Why:** Single source of truth for workflows, ensures consistency, manages state.

## Extending the System

### Adding a New Tool (Example: dbt)

1. Create client
```python
# src/api/dbt_client.py
class dbtClient:
    def get_model_stats(self, project):
        """Fetch dbt model performance"""
```

2. Register in config
```python
# src/config.py
DBT_API_KEY = os.getenv("DBT_API_KEY")
DBT_PROJECT_ID = os.getenv("DBT_PROJECT_ID")
```

3. Use in agent
```python
# src/agents/analysis_agent.py
dbt_models = dbt_client.get_model_stats(...)
# Incorporate into analysis
```

### Adding a New Agent (Example: Auto-Implementer)

1. Create agent
```python
# src/agents/implementation_agent.py
class ImplementationAgent:
    def generate_dag_code(self, recommendation):
        """Generate optimized DAG code"""
```

2. Add to orchestrator
```python
# src/agents/orchestrator.py
impl_agent = ImplementationAgent()
generated_code = impl_agent.generate_dag_code(recommendation)
```

3. Add CLI command
```python
# src/cli.py
@app.command()
def generate_optimized_dag(dag_id: str):
    """Generate optimized DAG code"""
```

## Deployment Options

### Local Development
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m src.cli analyze-all
```

### Docker Container
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "-m", "src.cli"]
```

### Kubernetes Job
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: dag-optimization-analysis
spec:
  schedule: "0 2 * * SUN"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: agent
            image: airflow-agent:latest
            command: ["python", "-m", "src.cli", "analyze-all"]
```

### GitHub Actions
```yaml
name: Weekly DAG Analysis
on:
  schedule:
    - cron: '0 2 * * 0'
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: python -m src.cli analyze-all
      - run: git push
```

## Testing Strategy

```
src/
├── tests/
│   ├── test_airflow_client.py
│   │   └─ Mock Airflow API responses
│   │
│   ├── test_analysis_agent.py
│   │   └─ Test Claude integration
│   │
│   ├── test_pattern_store.py
│   │   └─ Test Chroma operations
│   │
│   ├── test_orchestrator.py
│   │   └─ Test full pipeline
│   │
│   └── test_integration.py
│       └─ End-to-end testing
```

## Monitoring & Observability

```python
# Logging
logging.info("Starting full DAG analysis")
logging.debug(f"Analyzed {dag_id}: {analysis}")
logging.error(f"Failed to fetch metrics: {e}")

# Metrics
├─ Analysis time per DAG
├─ Claude API calls & costs
├─ Pattern match accuracy
├─ Recommendation accuracy
└─ System health checks
```

## Next Steps

1. **Get Started**
   - Read: `QUICKSTART.md`
   - Run: `python -m src.cli demo`

2. **Configure**
   - Edit `.env` with your credentials
   - Test: `python -m src.cli health`

3. **Analyze**
   - Run: `python -m src.cli analyze-all`
   - Review: `optimization_report.json`

4. **Implement**
   - Pick top recommendation
   - Follow implementation plan
   - Monitor results

5. **Learn**
   - Agent stores successful patterns
   - Future recommendations improve
   - Confidence increases over time

## Related Documentation

- [README.md](README.md) - Complete usage guide
- [QUICKSTART.md](QUICKSTART.md) - 5-minute setup
- [AGENTIFICATION_ARCHITECTURE.md](AGENTIFICATION_ARCHITECTURE.md) - Technical deep dive
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - What was built
- [Airflow DAG Optimization Guide](../Airflow_DAG_Optimization_Guide.html) - Reference material

---

**Everything you need is in this directory. Start with README.md or QUICKSTART.md.**

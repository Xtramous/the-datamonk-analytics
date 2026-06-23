# Code Reading Order - Complete Flow Guide

## Overview: How to Read the Code

This guide shows you the **execution order** when running `python -m src.cli analyze-all`, so you understand the complete data flow.

## Phase 1: Entry Points (Start Here)

### 1. `main.py` (10 lines) - Application Entry Point
**What it does**: Sets up logging and launches CLI

**Key lines**:
```python
from src.cli import app

if __name__ == "__main__":
    app()  # Launches CLI with Typer
```

**Why read this first**: This is where execution begins. Very simple - just loads and runs the CLI.

**Time to understand**: 1 minute

---

## Phase 2: CLI Interface (User Commands)

### 2. `src/cli.py` (350 lines) - User Commands Entry Point
**What it does**: Provides command-line interface using Typer

**Read these functions in order**:

1. **`analyze_all()` command (lines ~20-80)**
   - This is what runs when you type: `python -m src.cli analyze-all`
   - Creates console output with Rich formatting
   - Calls orchestrator to run full analysis
   - **Key line**: `report = orchestrator.run_full_analysis()`
   - This is the main entry point for the whole system!

2. **`analyze_dag()` command (lines ~82-150)**
   - Single DAG deep dive
   - Uses same orchestrator but different method

3. **`show_patterns()` command (lines ~152-200)**
   - Displays learned patterns
   - Shows pattern store statistics

4. **`health()` command (lines ~202-260)**
   - Tests all tool connections
   - Useful for debugging

5. **`demo()` command (lines ~262-300)**
   - Shows capabilities with documentation
   - No real analysis, just info

**Why read this**: Understand what happens when user runs a command. The `analyze_all()` function calls the orchestrator, which is the heart of the system.

**Time to understand**: 10-15 minutes

**Key takeaway**: `analyze_all()` → `orchestrator.run_full_analysis()` is the main execution path.

---

## Phase 3: Configuration (Global Settings)

### 3. `src/config.py` (210 lines) - Configuration Management
**What it does**: Loads environment variables and sets defaults

**Read in order**:

```python
class Settings(BaseSettings):
    # Claude API
    ANTHROPIC_API_KEY: str          # Your API key
    CLAUDE_MODEL: str               # Which Claude model to use

    # Airflow
    AIRFLOW_BASE_URL: str           # Where Airflow runs
    AIRFLOW_USERNAME: str           # Airflow credentials
    AIRFLOW_PASSWORD: str

    # Prometheus (optional)
    PROMETHEUS_URL: str

    # Chroma Vector DB
    CHROMA_DB_PATH: str             # Where patterns are stored
    CHROMA_COLLECTION_NAME: str

    # Optimization thresholds
    COST_THRESHOLD_HIGH: float      # What's "high cost"
    DURATION_THRESHOLD_HOURS: float # What's "long duration"
    ERROR_RATE_THRESHOLD: float     # What's "high error rate"

    # Agent settings
    MAX_RETRIES: int                # Retry failed API calls
    TIMEOUT_SECONDS: int            # API timeout
```

**Why read this**: Understand what configuration is available. Every other module imports from here.

**Time to understand**: 5 minutes

**Key takeaway**: All configuration comes from .env file or defaults in this file.

---

## Phase 4: Core Orchestration (The Brain)

### 4. `src/agents/orchestrator.py` (250 lines) - Workflow Coordinator
**What it does**: Orchestrates all agents in the correct order. This is the **MAIN LOGIC**.

**Read in this exact order**:

#### 4.1 `__init__()` method (lines ~20-30)
**What it does**: Initializes all components
```python
def __init__(self):
    self.airflow_client = AirflowClient()      # Will read data
    self.prometheus_client = PrometheusClient()  # Will read metrics
    self.analysis_agent = DAGAnalysisAgent()    # Will analyze with Claude
    self.cost_agent = CostCalculatorAgent()     # Will calculate ROI
    self.pattern_store = PatternStore()         # Will learn patterns
```

**Why this**: See what components are created and in what order.

**Time to understand**: 2 minutes

#### 4.2 `run_full_analysis()` method (lines ~32-120) - **THE MAIN PIPELINE**
**This is the core flow!** Read this carefully.

```python
def run_full_analysis(self):
    # STEP 1: COLLECT METRICS
    logger.info("Step 1: Collecting DAG metrics...")
    dag_metrics = self.airflow_client.extract_dag_metrics()
    # Returns: {dag_id: {metrics}}
    
    # STEP 2: ANALYZE PERFORMANCE
    logger.info("Step 2: Analyzing DAG performance...")
    analyses = {}
    for dag_id, metrics in dag_metrics.items():
        analysis = self.analysis_agent.analyze_dag_performance(metrics)
        # analysis = {assessment, issues, techniques, expected_savings}
        analyses[dag_id] = analysis
    
    # STEP 3: PRIORITIZE DAGS
    logger.info("Step 3: Prioritizing DAGs...")
    priority_order = self.analysis_agent.prioritize_dags(dag_metrics)
    # priority_order = [dag_id_1, dag_id_2, dag_id_3, ...]
    
    # STEP 4: GENERATE RECOMMENDATIONS
    logger.info("Step 4: Generating optimization recommendations...")
    recommendations = {}
    for dag_id in priority_order[:5]:  # Top 5 DAGs
        # Find similar patterns from Chroma
        similar_patterns = self.pattern_store.find_similar_patterns(...)
        # Ask Claude for detailed recommendations
        recommendation = self.analysis_agent.recommend_optimizations(
            metrics, similar_patterns
        )
        # recommendation = {technique, steps, risks, ROI, implementation}
        recommendations[dag_id] = recommendation
    
    # STEP 5: CALCULATE COSTS
    logger.info("Step 5: Calculating costs and ROI...")
    cost_analyses = {}
    for dag_id in priority_order[:5]:
        cost_estimate = self.cost_agent.estimate_dag_cost({...})
        # cost_estimate = {monthly_cost, breakdown, drivers}
        cost_analyses[dag_id] = cost_estimate
    
    # STEP 6: STORE PATTERNS (LEARNING)
    logger.info("Step 6: Storing optimization patterns...")
    for dag_id in priority_order[:3]:
        pattern = {
            "optimization_technique": recommendation["technique"],
            "before_cost": cost_estimate["monthly_cost"],
            "after_cost": cost_estimate["monthly_cost"] * 0.5,
            "savings": calculated_savings,
            ...
        }
        self.pattern_store.add_optimization_pattern(dag_id, pattern)
    
    # STEP 7: GENERATE REPORT
    logger.info("Step 7: Generating optimization report...")
    report = self._generate_report(...)
    return report
```

**This is the complete flow!** Each step calls different components.

**Time to understand**: 15-20 minutes

**Key takeaway**: This is the **orchestration logic**. Every step is a method call to another component.

#### 4.3 `analyze_single_dag()` method (lines ~122-160)
**What it does**: Same as above but for one DAG
- Similar flow but focused on one dag_id
- Returns detailed analysis for that DAG

#### 4.4 `_generate_report()` method (lines ~162-185)
**What it does**: Format results into a nice report
- Gathers all analyses
- Calculates totals and statistics
- Returns JSON-serializable report

**Time to understand**: 5 minutes

---

## Phase 5: Data Collection Layer (Reading Real Data)

### 5. `src/api/airflow_client.py` (180 lines) - Airflow REST API Integration

**What it does**: Fetches real DAG metrics from Airflow

**Read in this order**:

#### 5.1 `__init__()` method (lines ~15-20)
```python
def __init__(self):
    self.base_url = settings.AIRFLOW_BASE_URL
    self.auth = HTTPBasicAuth(...)  # Credentials
    self.timeout = settings.TIMEOUT_SECONDS
```

#### 5.2 Low-level API methods
1. `get_dags()` - Fetch all DAGs
2. `get_dag_runs()` - Get execution history
3. `get_dag_stats()` - Get success/failure counts
4. `get_task_instances()` - Get individual task data

**These are simple HTTP GET requests**

#### 5.3 `extract_dag_metrics()` (lines ~75-105) - **HIGH-LEVEL METHOD**
**What it does**: Combine all low-level calls into unified metrics

```python
def extract_dag_metrics(self):
    dags = self.get_dags()  # Get list of all DAGs
    
    for dag in dags:
        dag_id = dag["dag_id"]
        
        # Get execution history
        runs = self.get_dag_runs(dag_id, limit=5)
        
        # Get statistics
        stats = self.get_dag_stats(dag_id)
        
        # Calculate metrics
        durations = [run["duration"] for run in runs]
        avg_duration = sum(durations) / len(durations)
        
        # Store aggregated metrics
        metrics[dag_id] = {
            "dag_id": dag_id,
            "avg_duration_seconds": avg_duration,
            "total_runs": len(runs),
            "stats": stats,
            ...
        }
    
    return metrics  # This goes to orchestrator
```

**Time to understand**: 10 minutes

**Key takeaway**: This fetches REAL data from Airflow. These metrics feed into all analysis agents.

---

### 6. `src/api/prometheus_client.py` (150 lines) - Prometheus Metrics

**What it does**: Fetches performance metrics from Prometheus

**Similar structure to AirflowClient**:

1. `__init__()` - Initialize connection
2. `query()` - Execute PromQL queries (lowest level)
3. `get_dag_execution_time()` - Get average DAG execution time
4. `get_task_failures()` - Get failure counts
5. `get_resource_usage()` - Get CPU and memory
6. `get_dag_metrics()` - Combine all into one object

**Key difference**: Uses PromQL queries instead of REST API

**Time to understand**: 10 minutes

**Key takeaway**: Provides detailed resource metrics that complement Airflow's execution metrics.

---

## Phase 6: Analysis Agents (Claude AI)

### 7. `src/agents/analysis_agent.py` (200 lines) - Performance Analysis

**What it does**: Uses Claude AI to analyze DAG performance and make intelligent decisions

**Read in this order**:

#### 7.1 Configuration (lines ~1-20)
```python
OPTIMIZATION_TECHNIQUES = [
    "Parallelization",
    "Incremental Loading",
    "Indexing & Caching",
    "Query Optimization",
    "Resource Right-Sizing",
    "DAG Parallelization",
    "Batch Processing",
    "Compression",
    "Monitoring & Alerting",
    "Incremental Updates"
]
```

These are the 10 techniques from your HTML guide - now part of agent knowledge!

#### 7.2 `__init__()` method
```python
def __init__(self):
    self.client = anthropic.Anthropic()  # Initialize Claude
    self.model = "claude-3-5-sonnet-20241022"
```

#### 7.3 `analyze_dag_performance()` method (lines ~30-90) - **KEY METHOD**

**What it does**: Ask Claude to analyze a DAG

```python
def analyze_dag_performance(self, dag_metrics: Dict[str, Any]):
    prompt = f"""
    Analyze this Airflow DAG's performance:
    
    DAG ID: {dag_metrics['dag_id']}
    Duration: {dag_metrics['avg_duration_seconds']} seconds
    Frequency: daily
    Stats: {dag_metrics['stats']}
    
    Recommend from: {', '.join(OPTIMIZATION_TECHNIQUES)}
    
    Respond with JSON:
    {{
        "assessment": "good|okay|poor",
        "issues": ["issue1", "issue2"],
        "recommended_techniques": ["tech1", "tech2"],
        "expected_savings": "low|medium|high"
    }}
    """
    
    # Send to Claude
    message = self.client.messages.create(
        model=self.model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Parse response
    response_text = message.content[0].text
    analysis = json.loads(response_text)  # Extract JSON
    
    return analysis
```

**This is how Claude gets used!** Observe the pattern:
1. Build a prompt with data
2. Send to Claude via API
3. Parse the response

#### 7.4 `recommend_optimizations()` method (lines ~92-160)

**What it does**: Generate detailed implementation recommendations

Uses Claude to answer: "How should we implement this optimization?"

Takes as input:
- DAG metrics
- Similar patterns from Chroma (for context)

Returns:
- Implementation steps
- Risk assessment
- Estimated savings

#### 7.5 `prioritize_dags()` method (lines ~162-200)

**What it does**: Ask Claude which DAGs matter most

"Given all these DAGs, which should we optimize first?"

**Time to understand**: 20-25 minutes (Claude integration is key concept)

**Key takeaway**: Analysis Agent = Pattern (data → Claude prompt → JSON response)

---

### 8. `src/agents/cost_calculator_agent.py` (180 lines) - Cost & ROI Analysis

**What it does**: Uses Claude to estimate costs and calculate ROI

**Similar pattern to Analysis Agent**:

1. `__init__()` - Initialize Claude client
2. `estimate_dag_cost()` - Ask Claude: "What's the cost?"
3. `calculate_roi()` - Ask Claude: "What's the payback period?"
4. `prioritize_by_savings()` - Ask Claude: "Which DAGs save most money?"

**Key difference**: Focuses on financial metrics instead of technical

**Time to understand**: 10 minutes

**Key takeaway**: Same Claude integration pattern, different prompts/outputs

---

## Phase 7: Learning System (Vector Database)

### 9. `src/storage/pattern_store.py` (200 lines) - Chroma Vector Database

**What it does**: Stores optimization patterns and enables semantic search

**Read in this order**:

#### 9.1 `__init__()` method
```python
def __init__(self):
    self.client = chromadb.Client()
    self.collection = self.client.get_or_create_collection(
        name=settings.CHROMA_COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}  # Similarity metric
    )
```

**Key concept**: Collection stores vectors for semantic search

#### 9.2 `add_optimization_pattern()` method
```python
def add_optimization_pattern(self, dag_id: str, pattern: Dict):
    pattern_text = f"""
    DAG: {dag_id}
    Problem: {pattern['problem']}
    Optimization: {pattern['optimization_technique']}
    Result: Saved ${pattern['savings']}/month
    Implementation: {pattern['implementation']}
    """
    
    self.collection.add(
        ids=[f"{dag_id}_{technique}"],
        documents=[pattern_text],
        metadatas=[{
            "dag_id": dag_id,
            "technique": technique,
            "savings_percent": savings
        }]
    )
```

**What it does**: Store a pattern for future learning

#### 9.3 `find_similar_patterns()` method (KEY METHOD)
```python
def find_similar_patterns(self, problem_description: str):
    results = self.collection.query(
        query_texts=[problem_description],
        n_results=3  # Get top 3 similar patterns
    )
    
    return results  # Similar patterns ranked by relevance
```

**This is semantic search!** 

Example:
- Query: "Our DAG has sequential tasks"
- Returns: [Pattern A (parallelization), Pattern B (async), Pattern C (batch)]

#### 9.4 `get_patterns_for_technique()` method
```python
def get_patterns_for_technique(self, technique: str):
    # Get all patterns using specific technique
    # Example: get_patterns_for_technique("Parallelization")
    # Returns: All DAGs that used parallelization
```

#### 9.5 `get_statistics()` method
```python
def get_statistics(self):
    # Count patterns, calculate avg savings
    # Returns stats like:
    # {
    #     "total_patterns": 8,
    #     "techniques": {
    #         "Parallelization": {"count": 5, "avg_savings": 45%},
    #         "Caching": {"count": 3, "avg_savings": 15%}
    #     }
    # }
```

**Time to understand**: 15-20 minutes

**Key takeaway**: Chroma = Memory for the agent. Stores learnings, enables future improvements.

---

## Complete Execution Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│ USER: python -m src.cli analyze-all                    │
└──────────────────┬──────────────────────────────────────┘
                   ↓
        ┌──────────────────────┐
        │ main.py              │
        │ Entry point          │
        └──────────┬───────────┘
                   ↓
        ┌──────────────────────┐
        │ src/cli.py           │
        │ analyze_all()        │
        │ Parse CLI options    │
        └──────────┬───────────┘
                   ↓
        ┌──────────────────────┐
        │ src/config.py        │
        │ Load settings        │
        └──────────┬───────────┘
                   ↓
   ┌───────────────────────────────────┐
   │ orchestrator.run_full_analysis()  │
   │ (This is the main logic!)         │
   └──────┬────────────────────────────┘
          │
   ┌──────┴──────────────────────────────────────────┐
   │              STEP 1: COLLECT DATA               │
   │                                                 │
   │  airflow_client.extract_dag_metrics()          │
   │  ├─ get_dags()                                 │
   │  ├─ get_dag_runs()                             │
   │  ├─ get_dag_stats()                            │
   │  └─ aggregate into metrics dict                │
   │                                                 │
   │  prometheus_client.get_dag_metrics()           │
   │  ├─ query CPU, memory, execution time          │
   │  └─ return resource metrics                    │
   │                                                 │
   │  Result: dag_metrics = {                        │
   │    "daily_etl": {duration, frequency, ...},   │
   │    "hourly_monitoring": {...},                 │
   │    ...                                          │
   │  }                                              │
   └──────┬──────────────────────────────────────────┘
          │
   ┌──────┴──────────────────────────────────────────┐
   │           STEP 2: ANALYZE EACH DAG              │
   │                                                 │
   │  for dag_id, metrics in dag_metrics.items():   │
   │    analysis = analysis_agent                   │
   │      .analyze_dag_performance(metrics)         │
   │      (Ask Claude: "What's wrong?")             │
   │    analyses[dag_id] = {                        │
   │      assessment: "poor",                       │
   │      issues: [...],                            │
   │      recommended_techniques: [...]             │
   │    }                                            │
   │                                                 │
   │  Result: analyses = {                          │
   │    "daily_etl": {assessment, issues, ...},    │
   │    ...                                          │
   │  }                                              │
   └──────┬──────────────────────────────────────────┘
          │
   ┌──────┴──────────────────────────────────────────┐
   │           STEP 3: PRIORITIZE DAGS               │
   │                                                 │
   │  priority_order =                              │
   │    analysis_agent.prioritize_dags(dag_metrics) │
   │    (Ask Claude: "Which DAGs matter most?")     │
   │                                                 │
   │  Result: priority_order = [                    │
   │    "daily_etl",                                │
   │    "hourly_monitoring",                        │
   │    "weekly_reporting"                          │
   │  ]                                              │
   └──────┬──────────────────────────────────────────┘
          │
   ┌──────┴──────────────────────────────────────────┐
   │      STEP 4: PATTERN SEARCH & RECOMMEND        │
   │                                                 │
   │  for dag_id in priority_order[:5]:             │
   │    # Search Chroma for similar cases           │
   │    similar_patterns =                          │
   │      pattern_store                             │
   │      .find_similar_patterns(problem_desc)      │
   │    (Semantic search: "sequential tasks")       │
   │                                                 │
   │    # Generate detailed recommendations         │
   │    recommendation =                            │
   │      analysis_agent                            │
   │      .recommend_optimizations(                 │
   │        metrics, similar_patterns)              │
   │      (Ask Claude: "How to implement?")         │
   │    recommendations[dag_id] = {                 │
   │      technique, steps, risks, roi, ...         │
   │    }                                            │
   │                                                 │
   │  Result: recommendations = {                   │
   │    "daily_etl": {steps, risks, ROI, ...},     │
   │    ...                                          │
   │  }                                              │
   └──────┬──────────────────────────────────────────┘
          │
   ┌──────┴──────────────────────────────────────────┐
   │          STEP 5: COST ANALYSIS                  │
   │                                                 │
   │  for dag_id in priority_order[:5]:             │
   │    cost_estimate =                             │
   │      cost_agent                                │
   │      .estimate_dag_cost(metrics)               │
   │      (Ask Claude: "What's the cost?")          │
   │                                                 │
   │    roi = cost_agent.calculate_roi(             │
   │      recommendation, before, after)            │
   │      (Ask Claude: "What's the payback?")       │
   │                                                 │
   │    cost_analyses[dag_id] = {                   │
   │      monthly_cost, breakdown, roi, ...         │
   │    }                                            │
   │                                                 │
   │  Result: cost_analyses = {                     │
   │    "daily_etl": {cost, savings, ROI, ...},    │
   │    ...                                          │
   │  }                                              │
   └──────┬──────────────────────────────────────────┘
          │
   ┌──────┴──────────────────────────────────────────┐
   │          STEP 6: LEARNING (Store)               │
   │                                                 │
   │  for dag_id in priority_order[:3]:             │
   │    pattern = {                                 │
   │      problem: analyses[dag_id]['issues'],      │
   │      technique: recommendations['technique'],  │
   │      before_cost: cost_analyses['before'],     │
   │      after_cost: cost_analyses['after'],       │
   │      savings: calculated_savings,              │
   │      confidence: 'high'                        │
   │    }                                            │
   │                                                 │
   │    pattern_store                               │
   │      .add_optimization_pattern(dag_id, pattern)│
   │      (Store for future use!)                   │
   │                                                 │
   │  Result: Patterns now in Chroma for next run   │
   └──────┬──────────────────────────────────────────┘
          │
   ┌──────┴──────────────────────────────────────────┐
   │          STEP 7: GENERATE REPORT                │
   │                                                 │
   │  report = _generate_report(                    │
   │    dag_metrics, analyses, priority_order,      │
   │    recommendations, cost_analyses              │
   │  )                                              │
   │                                                 │
   │  report = {                                    │
   │    timestamp: "2024-06-22T...",                │
   │    summary: {                                  │
   │      total_dags: 15,                           │
   │      current_cost: $20000,                     │
   │      potential_savings: $10000,                │
   │      ...                                       │
   │    },                                          │
   │    priority_order: [...],                      │
   │    analyses: {...},                            │
   │    recommendations: {...},                     │
   │    cost_analyses: {...},                       │
   │    pattern_statistics: {...}                   │
   │  }                                              │
   └──────┬──────────────────────────────────────────┘
          │
   ┌──────┴──────────────────────────────────────────┐
   │       RETURN TO CLI AND DISPLAY RESULTS         │
   │                                                 │
   │  cli.py prints:                                │
   │  - Summary table                               │
   │  - Priority order                              │
   │  - Next actions                                │
   │                                                 │
   │  Saves: optimization_report.json               │
   └──────────────────────────────────────────────────┘
```

---

## Reading Order Summary

**Follow this exact order to understand the complete flow:**

### Session 1: Entry Points & Flow (20 min)
1. `main.py` (1 min) - How it starts
2. `src/cli.py` (10 min) - User commands, focus on `analyze_all()`
3. `src/config.py` (5 min) - Configuration loaded
4. Check the "STEP 1-7" comments in `src/agents/orchestrator.py` (4 min)

### Session 2: Data Collection (20 min)
5. `src/api/airflow_client.py` (10 min) - How real DAG metrics are fetched
6. `src/api/prometheus_client.py` (10 min) - How performance metrics are fetched

### Session 3: Core Orchestration (25 min)
7. `src/agents/orchestrator.py` complete (25 min) - Read `run_full_analysis()` line by line

### Session 4: Analysis Agents (35 min)
8. `src/agents/analysis_agent.py` (20 min) - How Claude is used for analysis
9. `src/agents/cost_calculator_agent.py` (15 min) - How Claude is used for ROI

### Session 5: Learning System (20 min)
10. `src/storage/pattern_store.py` (20 min) - How patterns are stored & searched

---

## Key Concepts to Understand at Each Level

### Level 1: CLI Entry
- User runs command → CLI parses options → Calls orchestrator

### Level 2: Orchestration
- Orchestrator is the "conductor" - coordinates all other components
- Each STEP (1-7) calls different components in sequence
- Data flows from step to step (metrics → analysis → recommendations → report)

### Level 3: Data Collection
- AirflowClient = REST API wrapper
- PrometheusClient = Prometheus query wrapper
- Both return dictionaries of metrics

### Level 4: Analysis
- AnalysisAgent = Claude wrapper
- CostCalculatorAgent = Claude wrapper (same pattern, different purpose)
- Pattern: Build prompt → Send to Claude → Parse response

### Level 5: Learning
- PatternStore = Chroma vector DB wrapper
- Stores optimization patterns for future use
- Enables semantic search for similar cases

---

## Reading Tips

1. **Start with the execution flow diagram above** - Follow the arrows
2. **Read main methods first** - Ignore helper methods initially
3. **Look for the Claude.messages.create() calls** - This is where AI happens
4. **Follow the data types** - See what dict/object is returned at each step
5. **Note the orchestration pattern** - Each step inputs = previous step outputs

---

## Understanding Each File by Purpose

| File | Purpose | Key Method | Returns |
|------|---------|-----------|---------|
| `cli.py` | User commands | `analyze_all()` | None (prints) |
| `config.py` | Settings | `Settings()` | Config object |
| `orchestrator.py` | Main logic | `run_full_analysis()` | Report dict |
| `airflow_client.py` | Get DAG metrics | `extract_dag_metrics()` | {dag_id: metrics} |
| `prometheus_client.py` | Get perf metrics | `get_dag_metrics()` | {cpu, memory, ...} |
| `analysis_agent.py` | Analyze w/ Claude | `analyze_dag_performance()` | {assessment, issues, ...} |
| `cost_calculator_agent.py` | ROI w/ Claude | `estimate_dag_cost()` | {cost, breakdown, ...} |
| `pattern_store.py` | Store & search | `find_similar_patterns()` | [similar patterns] |

---

## Claude API Pattern (Used Everywhere)

This pattern is used in both agents:

```python
# 1. Build prompt with data
prompt = f"""
Analyze this: {data}
Return JSON with: {{...}}
"""

# 2. Send to Claude
message = self.client.messages.create(
    model=self.model,
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)

# 3. Parse response
response_text = message.content[0].text
start_idx = response_text.find('{')
end_idx = response_text.rfind('}') + 1
json_str = response_text[start_idx:end_idx]
result = json.loads(json_str)

# 4. Return to caller
return result
```

**Memorize this pattern!** It's used 10+ times throughout the codebase.

---

## Next Steps After Reading

1. **Read a function** from the code
2. **Trace it mentally** through the flow diagram
3. **Identify which files** get called
4. **Find the Claude prompt** if it's an agent
5. **Understand the input/output** types

This will cement your understanding of the complete system.

Happy reading! 🚀

# Code Flow Examples - Actual Code Snippets

This document shows the **actual code** from each file as the execution flows through the system.

## Example 1: User Runs analyze-all Command

### Step 1: User Types Command
```bash
python -m src.cli analyze-all
```

### Step 2: main.py Executes
```python
# main.py
if __name__ == "__main__":
    app()  # Launches the Typer CLI app
```

### Step 3: CLI Routes to analyze_all() Function
```python
# src/cli.py
@app.command()
def analyze_all():
    """Run comprehensive analysis on all DAGs"""
    console.print(Panel("🤖 Airflow Optimization Agent - Full Analysis", style="bold blue"))

    with console.status("[bold cyan]Analyzing DAGs...", spinner="dots"):
        report = orchestrator.run_full_analysis()  # <-- MAIN CALL
    
    # ... display results ...
```

**Key line**: `report = orchestrator.run_full_analysis()`

This calls the orchestrator's main method.

---

## Example 2: Complete Flow Through Orchestrator

### The complete run_full_analysis() method:

```python
# src/agents/orchestrator.py - Line 32
def run_full_analysis(self) -> Dict[str, Any]:
    """Run complete analysis pipeline"""
    logger.info("Starting full DAG optimization analysis...")

    # ========== STEP 1: COLLECT METRICS ==========
    logger.info("Step 1: Collecting DAG metrics...")
    
    # Call Airflow API to get DAG metrics
    dag_metrics = self.airflow_client.extract_dag_metrics()
    # Returns: {
    #   "daily_etl": {
    #     "dag_id": "daily_etl",
    #     "owner": "data_team",
    #     "avg_duration_seconds": 3600,
    #     "total_runs": 30,
    #     "last_run": "2024-06-22T15:30:00Z"
    #   },
    #   "hourly_monitoring": {...},
    #   ...
    # }
    
    if not dag_metrics:
        logger.warning("No DAG metrics collected")
        return {"error": "No DAGs found"}

    # ========== STEP 2: ANALYZE PERFORMANCE ==========
    logger.info("Step 2: Analyzing DAG performance...")
    
    analyses = {}
    for dag_id, metrics in dag_metrics.items():
        # Ask Claude to analyze this DAG
        analysis = self.analysis_agent.analyze_dag_performance(metrics)
        # Returns: {
        #   "assessment": "poor",
        #   "issues": [
        #     "Sequential tasks take 3600 seconds",
        #     "5% error rate",
        #     "No caching between runs"
        #   ],
        #   "recommended_techniques": [
        #     "Parallelization",
        #     "Caching",
        #     "Monitoring"
        #   ],
        #   "expected_savings": "high"
        # }
        analyses[dag_id] = analysis
        logger.debug(f"Analyzed {dag_id}: {analysis.get('assessment')}")

    # ========== STEP 3: PRIORITIZE DAGS ==========
    logger.info("Step 3: Prioritizing DAGs for optimization...")
    
    # Ask Claude which DAGs should be optimized first
    priority_order = self.analysis_agent.prioritize_dags(dag_metrics)
    # Returns: ["daily_etl", "hourly_monitoring", "weekly_reporting"]

    # ========== STEP 4: GENERATE RECOMMENDATIONS ==========
    logger.info("Step 4: Generating optimization recommendations...")
    
    recommendations = {}
    for dag_id in priority_order[:5]:  # Top 5 DAGs
        metrics = dag_metrics.get(dag_id, {})
        
        # Find similar patterns from Chroma
        problem_description = f"DAG {dag_id} has issues: {analyses[dag_id].get('issues', [])}"
        similar_patterns = self.pattern_store.find_similar_patterns(problem_description)
        # Returns: [{
        #   "pattern": "DAG with sequential tasks...",
        #   "metadata": {"technique": "Parallelization", "savings_percent": 50},
        #   "distance": 0.1234  # Similarity score
        # }, ...]

        # Ask Claude to generate detailed recommendations
        recommendation = self.analysis_agent.recommend_optimizations(
            metrics, similar_patterns
        )
        # Returns: {
        #   "primary_technique": "Parallelization",
        #   "implementation_steps": [
        #     "Step 1: Identify independent tasks",
        #     "Step 2: Use SubDagOperator",
        #     "Step 3: Set pool limits"
        #   ],
        #   "estimated_implementation_hours": 6,
        #   "expected_monthly_savings": "$8,600",
        #   "confidence_level": "high",
        #   "risks": ["Increased memory usage"],
        #   "mitigations": ["Monitor closely"]
        # }
        recommendations[dag_id] = recommendation

    # ========== STEP 5: CALCULATE COSTS ==========
    logger.info("Step 5: Calculating costs and ROI...")
    
    cost_analyses = {}
    for dag_id in priority_order[:5]:
        metrics = dag_metrics.get(dag_id, {})
        
        # Estimate current cost
        cost_estimate = self.cost_agent.estimate_dag_cost({
            **metrics,
            "frequency": "daily",
            "monthly_executions": 30,
            "instance_type": "t3.small"
        })
        # Returns: {
        #   "monthly_cost_usd": 1450,
        #   "breakdown": {
        #     "compute": 1000,
        #     "data_transfer": 300,
        #     "storage": 150
        #   },
        #   "cost_drivers": ["Compute dominates (70%)"],
        #   "optimization_opportunities": [...]
        # }
        
        # Calculate ROI
        roi = self.cost_agent.calculate_roi(
            recommendations[dag_id],
            cost_estimate.get('monthly_cost_usd', 0),
            cost_estimate.get('monthly_cost_usd', 0) * 0.5  # 50% savings
        )
        # Returns: {
        #   "monthly_savings": 725,
        #   "annual_savings": 8700,
        #   "payback_period_days": 14,
        #   "roi_percent": 285,
        #   "recommendation": "implement"
        # }
        
        cost_analyses[dag_id] = cost_estimate
        logger.debug(f"Cost for {dag_id}: ${cost_estimate.get('monthly_cost_usd', 0)}/month")

    # ========== STEP 6: STORE PATTERNS (LEARNING) ==========
    logger.info("Step 6: Storing optimization patterns...")
    
    for dag_id in priority_order[:3]:  # Top 3 DAGs
        if dag_id in recommendations:
            # Create pattern object
            pattern = {
                "problem": str(analyses[dag_id].get('issues', [])),
                "optimization_technique": recommendations[dag_id].get('primary_technique'),
                "before_cost": cost_analyses[dag_id].get('monthly_cost_usd', 0),
                "after_cost": cost_analyses[dag_id].get('monthly_cost_usd', 0) * 0.5,
                "savings": cost_analyses[dag_id].get('monthly_cost_usd', 0) * 0.5,
                "savings_percent": 50,
                "implementation": recommendations[dag_id].get('implementation_steps', [])
            }
            
            # Store in Chroma for future use
            self.pattern_store.add_optimization_pattern(dag_id, pattern)
            # Now this pattern can be found by future analyses!

    # ========== STEP 7: GENERATE REPORT ==========
    logger.info("Step 7: Generating optimization report...")
    
    report = self._generate_report(
        dag_metrics, analyses, priority_order,
        recommendations, cost_analyses
    )
    # Returns: {
    #   "timestamp": "2024-06-22T15:30:00Z",
    #   "summary": {
    #     "total_dags": 15,
    #     "current_monthly_cost": $20000,
    #     "potential_monthly_savings": $10000,
    #     "potential_annual_savings": $120000,
    #     "optimization_rate": "50%"
    #   },
    #   "priority_order": ["daily_etl", "hourly_monitoring", ...],
    #   "analyses": {...},
    #   "recommendations": {...},
    #   "cost_analyses": {...},
    #   "next_actions": [...]
    # }

    logger.info("Analysis complete!")
    return report
```

**This is the complete flow!** Each step has clear input/output.

---

## Example 3: Data Collection - Airflow API

### How Airflow metrics are fetched:

```python
# src/api/airflow_client.py

def get_dags(self) -> List[Dict[str, Any]]:
    """Fetch all DAGs from Airflow"""
    try:
        # Make HTTP request to Airflow REST API
        response = requests.get(
            f"{self.base_url}/api/v1/dags",
            auth=self.auth,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json().get("dags", [])
    except Exception as e:
        logger.error(f"Failed to fetch DAGs: {e}")
        return []


def extract_dag_metrics(self) -> Dict[str, Any]:
    """Extract key metrics from all DAGs"""
    
    # Get list of all DAGs
    dags = self.get_dags()
    # Returns: [
    #   {"dag_id": "daily_etl", "owner": "data_team", ...},
    #   {"dag_id": "hourly_monitoring", "owner": "monitoring", ...},
    #   ...
    # ]
    
    metrics = {}

    for dag in dags:
        dag_id = dag.get("dag_id")
        
        # Get execution history (last 5 runs)
        runs = self.get_dag_runs(dag_id, limit=5)
        # Returns: [
        #   {"execution_date": "2024-06-22T15:30:00Z", "duration": 3600, "state": "success"},
        #   {"execution_date": "2024-06-21T15:30:00Z", "duration": 3550, "state": "success"},
        #   ...
        # ]
        
        # Get DAG statistics
        stats = self.get_dag_stats(dag_id)
        # Returns: {"task_successes": 150, "task_failures": 2, ...}

        # Calculate average duration
        durations = []
        for run in runs:
            if run.get("duration"):
                durations.append(run["duration"])

        avg_duration = sum(durations) / len(durations) if durations else 0

        # Store aggregated metrics
        metrics[dag_id] = {
            "dag_id": dag_id,
            "owner": dag.get("owner"),
            "description": dag.get("description"),
            "is_paused": dag.get("is_paused", False),
            "total_runs": len(runs),
            "avg_duration_seconds": avg_duration,  # <-- Key metric
            "last_run": runs[0].get("execution_date") if runs else None,
            "stats": stats,
        }

    return metrics
```

**Output Example**:
```python
{
    "daily_etl": {
        "dag_id": "daily_etl",
        "owner": "data_team",
        "avg_duration_seconds": 3600,
        "total_runs": 30,
        "stats": {"task_successes": 150, "task_failures": 2}
    },
    "hourly_monitoring": {
        ...
    }
}
```

This gets passed to the Analysis Agent!

---

## Example 4: Using Claude AI in Analysis Agent

### How Claude is called:

```python
# src/agents/analysis_agent.py

def analyze_dag_performance(self, dag_metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze DAG performance and identify issues"""
    
    # STEP 1: Build the prompt
    prompt = f"""
    Analyze this Airflow DAG's performance and identify optimization opportunities:

    DAG Metrics:
    - DAG ID: {dag_metrics.get('dag_id')}
    - Owner: {dag_metrics.get('owner')}
    - Average Duration: {dag_metrics.get('avg_duration_seconds')} seconds
    - Total Runs (last 5): {dag_metrics.get('total_runs')}
    - Last Run: {dag_metrics.get('last_run')}
    - Status: {'Paused' if dag_metrics.get('is_paused') else 'Active'}
    - Stats: {json.dumps(dag_metrics.get('stats', {}), indent=2)}

    Based on this data, provide:
    1. Performance assessment (good/okay/poor)
    2. Top 3 performance issues
    3. Estimated current monthly cost impact
    4. Recommended optimization techniques from this list: {', '.join(OPTIMIZATION_TECHNIQUES)}
    5. Expected cost savings (low/medium/high)

    Format response as JSON with these exact fields:
    {{
        "assessment": "good|okay|poor",
        "issues": ["issue1", "issue2", "issue3"],
        "estimated_cost_impact": "number in dollars",
        "recommended_techniques": ["technique1", "technique2", "technique3"],
        "expected_savings": "low|medium|high",
        "reasoning": "brief explanation"
    }}
    """

    try:
        # STEP 2: Send to Claude
        message = self.client.messages.create(
            model=self.model,  # "claude-3-5-sonnet-20241022"
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        # STEP 3: Extract and parse response
        response_text = message.content[0].text
        # Example response:
        # {
        #   "assessment": "poor",
        #   "issues": ["Sequential tasks", "No caching", "High error rate"],
        #   ...
        # }
        
        # Find JSON in response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        json_str = response_text[start_idx:end_idx]
        
        # Parse JSON
        analysis = json.loads(json_str)
        
        # STEP 4: Return to caller
        return analysis
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return {"error": str(e), "assessment": "error"}
```

**Key Pattern**:
1. Build prompt with data
2. Call `self.client.messages.create()`
3. Extract text from response
4. Parse JSON
5. Return to orchestrator

**This same pattern is used 10+ times!**

---

## Example 5: Pattern Storage in Chroma

### How patterns are stored and retrieved:

```python
# src/storage/pattern_store.py

def add_optimization_pattern(self, dag_id: str, pattern: Dict[str, Any]) -> None:
    """Store a successful optimization pattern"""
    try:
        # Create a human-readable document
        pattern_text = f"""
        DAG: {dag_id}
        Problem: {pattern.get('problem', '')}
        Optimization: {pattern.get('optimization_technique', '')}
        Before Cost: ${pattern.get('before_cost', 0)}/month
        After Cost: ${pattern.get('after_cost', 0)}/month
        Savings: ${pattern.get('savings', 0)}/month ({pattern.get('savings_percent', 0)}%)
        Implementation Details: {pattern.get('implementation', '')}
        """

        # Store in Chroma vector database
        self.collection.add(
            ids=[f"{dag_id}_{pattern.get('optimization_technique', 'unknown')}"],
            documents=[pattern_text],  # Text for search
            metadatas=[{
                "dag_id": dag_id,
                "technique": pattern.get("optimization_technique", ""),
                "savings_percent": pattern.get("savings_percent", 0),
                "before_cost": pattern.get("before_cost", 0),
                "after_cost": pattern.get("after_cost", 0),
            }]
        )
        logger.info(f"Added optimization pattern for {dag_id}")
    except Exception as e:
        logger.error(f"Failed to add pattern: {e}")


def find_similar_patterns(self, problem_description: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """Find similar optimization patterns from past learnings"""
    try:
        # Query Chroma using semantic search
        # Input: "Our DAG has sequential tasks running one by one"
        # Chroma finds similar patterns using vector similarity
        results = self.collection.query(
            query_texts=[problem_description],
            n_results=top_k  # Get top 3 most similar
        )

        patterns = []
        for i, doc in enumerate(results.get("documents", [[]])[0]):
            patterns.append({
                "pattern": doc,
                "metadata": results.get("metadatas", [[]])[0][i] if results.get("metadatas") else {},
                "distance": results.get("distances", [[]])[0][i] if results.get("distances") else 0
            })

        return patterns
        # Returns: [
        #   {
        #     "pattern": "DAG with sequential tasks...",
        #     "metadata": {"technique": "Parallelization", "savings_percent": 50},
        #     "distance": 0.1234  # Similarity (lower is better)
        #   },
        #   {
        #     "pattern": "DAG with async operations...",
        #     "metadata": {"technique": "Async", "savings_percent": 35},
        #     "distance": 0.2456
        #   },
        #   ...
        # ]
        
    except Exception as e:
        logger.error(f"Failed to query patterns: {e}")
        return []
```

**Key Concept**: Chroma stores patterns as vectors, enabling semantic search.

Example query:
- Query: "Our DAG has sequential tasks"
- Chroma returns: Similar patterns ranked by relevance
- Analysis Agent uses these to inform recommendations

---

## Example 6: Complete CLI Output Generation

### How results are displayed to user:

```python
# src/cli.py

@app.command()
def analyze_all():
    """Run comprehensive analysis on all DAGs"""
    console.print(Panel("🤖 Airflow Optimization Agent - Full Analysis", style="bold blue"))

    # Run analysis
    with console.status("[bold cyan]Analyzing DAGs...", spinner="dots"):
        report = orchestrator.run_full_analysis()

    if "error" in report:
        console.print(f"[red]Error: {report['error']}[/red]")
        return

    # Display summary
    summary = report.get("summary", {})
    console.print("\n[bold green]📊 Optimization Summary[/bold green]")
    
    summary_table = Table(title="Cost Analysis")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="magenta")

    summary_table.add_row("Total DAGs", str(summary.get("total_dags")))
    summary_table.add_row("Current Monthly Cost", f"${summary.get('current_monthly_cost', 0):.2f}")
    summary_table.add_row("Potential Monthly Savings", f"${summary.get('potential_monthly_savings', 0):.2f}")
    summary_table.add_row("Potential Annual Savings", f"${summary.get('potential_annual_savings', 0):.2f}")
    summary_table.add_row("Optimization Rate", summary.get("optimization_rate"))

    console.print(summary_table)

    # Display priority order
    console.print("\n[bold green]🎯 DAG Optimization Priority[/bold green]")
    priority_table = Table(title="Recommended Order")
    priority_table.add_column("Priority", style="cyan")
    priority_table.add_column("DAG ID", style="magenta")

    for idx, dag_id in enumerate(report.get("priority_order", [])[:5], 1):
        priority_table.add_row(str(idx), dag_id)

    console.print(priority_table)

    # Display next actions
    console.print("\n[bold green]✅ Next Actions[/bold green]")
    for action in report.get("next_actions", []):
        console.print(f"  {action}")

    # Save report to JSON
    with open("optimization_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    console.print("\n[green]✓ Report saved to optimization_report.json[/green]")
```

**Output to User**:
```
🤖 Airflow Optimization Agent - Full Analysis

📊 Optimization Summary
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Metric                        ┃ Value           ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ Total DAGs                    │ 15              │
│ Current Monthly Cost          │ $20,000.00      │
│ Potential Monthly Savings     │ $10,000.00      │
│ Potential Annual Savings      │ $120,000.00     │
│ Optimization Rate             │ 50%             │
└───────────────────────────────┴─────────────────┘

🎯 DAG Optimization Priority
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ Priority ┃ DAG ID             ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ 1        │ daily_etl          │
│ 2        │ hourly_monitoring  │
│ 3        │ weekly_reporting   │
└──────────┴────────────────────┘

✅ Next Actions
  1. Review optimization plan for daily_etl
  2. Implement parallelization (estimated 4-8 hours)
  3. Schedule testing environment setup
  ...

✓ Report saved to optimization_report.json
```

---

## Example 7: Data Flowing Through the System

### Following one DAG from start to finish:

```
INPUT: daily_etl DAG

┌─────────────────────────────────────────────────────────┐
│ STEP 1: Airflow API                                    │
└────────────────────┬────────────────────────────────────┘
                     ↓
        dag_metrics["daily_etl"] = {
            "dag_id": "daily_etl",
            "avg_duration_seconds": 3600,
            "total_runs": 30,
            "stats": {"task_successes": 150, "task_failures": 2}
        }

┌─────────────────────────────────────────────────────────┐
│ STEP 2: Analysis Agent (Claude)                        │
│ Prompt: "Analyze: 3600 sec duration, daily frequency"  │
└────────────────────┬────────────────────────────────────┘
                     ↓
        analysis["daily_etl"] = {
            "assessment": "poor",
            "issues": [
                "Sequential tasks take 3600 seconds",
                "5% error rate suggests flaky dependencies",
                "No caching between daily runs"
            ],
            "recommended_techniques": [
                "Parallelization",
                "Caching",
                "Monitoring"
            ],
            "expected_savings": "high"
        }

┌─────────────────────────────────────────────────────────┐
│ STEP 3: Pattern Store (Chroma Search)                  │
│ Query: "Sequential tasks in DAG"                        │
└────────────────────┬────────────────────────────────────┘
                     ↓
        similar_patterns = [
            {
                "pattern": "Parallelization on etl_pipeline, saved 50%",
                "metadata": {"technique": "Parallelization", "savings": 50}
            },
            {
                "pattern": "Async on user_sync, saved 40%",
                "metadata": {"technique": "Async", "savings": 40}
            },
            ...
        ]

┌─────────────────────────────────────────────────────────┐
│ STEP 4: Recommendation Agent (Claude)                  │
│ Prompt: "Implement optimization using past patterns"   │
└────────────────────┬────────────────────────────────────┘
                     ↓
        recommendations["daily_etl"] = {
            "primary_technique": "Parallelization",
            "implementation_steps": [
                "1. Identify independent tasks",
                "2. Use SubDagOperator for grouping",
                "3. Set pool limits to avoid overload"
            ],
            "expected_monthly_savings": "$8,600",
            "confidence_level": "high"
        }

┌─────────────────────────────────────────────────────────┐
│ STEP 5: Cost Calculator Agent (Claude)                 │
│ Prompt: "Calculate ROI for parallelization"            │
└────────────────────┬────────────────────────────────────┘
                     ↓
        cost_analyses["daily_etl"] = {
            "monthly_cost_usd": 17400,
            "breakdown": {
                "compute": 17000,
                "data_transfer": 300,
                "storage": 100
            },
            "expected_savings": "$8,700",
            "roi_percent": "285%"
        }

┌─────────────────────────────────────────────────────────┐
│ STEP 6: Pattern Store (Save)                           │
│ Store: "Parallelization works for daily_etl"           │
└────────────────────┬────────────────────────────────────┘
                     ↓
        Added to Chroma for future use!
        Next run: Agent already knows parallelization
        works for similar DAGs

┌─────────────────────────────────────────────────────────┐
│ STEP 7: Report Generation                              │
└────────────────────┬────────────────────────────────────┘
                     ↓
        report["priority_order"][0] = "daily_etl"
        report["summary"]["current_cost"] = $20000
        report["summary"]["potential_savings"] = $10000

┌─────────────────────────────────────────────────────────┐
│ OUTPUT: User sees on screen                             │
└─────────────────────────────────────────────────────────┘

Priority 1: daily_etl
├─ Current cost: $17,400/year
├─ Optimization: Parallelization
├─ After optimization: $8,800/year
├─ Savings: $8,600/year (50%)
├─ Confidence: High (5 similar DAGs succeeded)
└─ Next: Implement parallelization
```

This shows how **one DAG flows through the entire system!**

---

## Quick Reference: Input/Output for Each Component

| Component | Input | Output | Time |
|-----------|-------|--------|------|
| `airflow_client` | None | {dag_id: metrics} | 30-60s |
| `analysis_agent` | dag_metrics | {assessment, issues, techniques} | 10-15s |
| `prioritizer` | all metrics | [dag_id_1, dag_id_2] | 10-15s |
| `pattern_store` | problem text | [similar patterns] | <100ms |
| `recommendation` | metrics + patterns | {steps, risks, ROI} | 15-20s |
| `cost_agent` | metrics | {cost, breakdown, savings} | 10-15s |
| `report_gen` | all data | JSON report | 5s |

---

## Common Claude Prompts

### Pattern 1: Analysis
```python
prompt = f"""
Analyze: {data}
What's wrong? Issues?
Recommend from: {techniques}
Return JSON: {{assessment, issues, techniques}}
"""
```

### Pattern 2: Recommendations
```python
prompt = f"""
Based on: {metrics}
And patterns: {similar_patterns}
How to implement?
Return JSON: {{steps, risks, ROI}}
"""
```

### Pattern 3: Prioritization
```python
prompt = f"""
Given: {all_dags}
Which to optimize first?
Consider: impact, cost, effort
Return JSON: {{priority_order, reasoning}}
"""
```

All three follow the same pattern:
1. Build prompt
2. Send to Claude
3. Parse JSON
4. Return

---

## Now You Can Read the Code!

Use these examples as a guide:
1. Start with Example 2 (complete flow) - Follow the STEP comments
2. Go to actual file and trace each step
3. Look for Claude calls (Example 4 pattern)
4. See how data transforms (Example 7)
5. Check input/output types using table above

Happy coding! 🚀

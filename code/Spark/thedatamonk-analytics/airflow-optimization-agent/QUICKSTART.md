# Airflow Optimization Agent - Quick Start (5 minutes)

Get the AI agent analyzing your DAGs in 5 minutes.

## Prerequisites
- Python 3.9+
- Airflow instance with REST API enabled
- Anthropic API key (from https://console.anthropic.com)

## Setup (2 minutes)

### 1. Clone and navigate
```bash
cd /Users/nitinkamal/code/Spark/thedatamonk-analytics/airflow-optimization-agent
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure credentials
```bash
cp .env.example .env
# Edit .env with your credentials:
# ANTHROPIC_API_KEY=your_key_here
# AIRFLOW_BASE_URL=http://localhost:8080
nano .env
```

## Run Analysis (3 minutes)

### Full Analysis (Recommended)
```bash
python -m src.cli analyze-all
```

This will:
- ✓ Connect to your Airflow cluster
- ✓ Fetch all DAG metrics
- ✓ Use Claude AI to analyze performance
- ✓ Query Prometheus for detailed metrics
- ✓ Search for similar past optimizations
- ✓ Prioritize DAGs by impact
- ✓ Generate cost-benefit analysis
- ✓ Save results to `optimization_report.json`

**Output Example:**
```
📊 Optimization Summary
Total DAGs: 15
Current Monthly Cost: $20,000.00
Potential Monthly Savings: $10,000.00
Potential Annual Savings: $120,000.00

🎯 DAG Optimization Priority
1. daily_etl
2. hourly_monitoring
3. weekly_reporting

✅ Next Actions
1. Review optimization plan for daily_etl
2. Implement parallelization (estimated 4-8 hours)
3. Schedule testing environment setup
...
```

### Single DAG Analysis
```bash
python -m src.cli analyze-dag daily_etl
```

Dive deep into one DAG with detailed recommendations.

### Check Agent Health
```bash
python -m src.cli health
```

Verify all tool connections (Airflow, Prometheus, Claude, Chroma).

### View Learned Patterns
```bash
python -m src.cli show-patterns
```

See optimization patterns the agent has learned.

## What Happens Next?

### Review Report
Open `optimization_report.json` to see:
- Which DAGs to optimize first
- Expected cost savings
- Implementation plans
- Risk assessments

### Pick Top DAG
The report prioritizes for you. Typically:
1. **Daily ETL** - Runs daily, 30+ times/month
2. **Hourly Monitoring** - Runs 24x/day
3. **Weekly Reporting** - Lower frequency, lower impact

### Implement
Agent provides step-by-step implementation guide. Most common optimization: **Parallelization**

**Example:**
```python
# Before: Sequential tasks
with DAG('daily_etl') as dag:
    task1 = PythonOperator(task_id='extract')
    task2 = PythonOperator(task_id='transform')  # Waits for task1
    task3 = PythonOperator(task_id='load')       # Waits for task2
    
    task1 >> task2 >> task3  # Sequential: 1 hour

# After: Parallel where possible
with DAG('daily_etl') as dag:
    extract = PythonOperator(task_id='extract')
    transform = [
        PythonOperator(task_id='transform_users'),
        PythonOperator(task_id='transform_orders'),  # Run together
        PythonOperator(task_id='transform_products'),
    ]
    load = PythonOperator(task_id='load')
    
    extract >> transform >> load  # Parallel: 20 minutes (80% savings)
```

### Monitor Results
After implementing, re-run analysis:
```bash
python -m src.cli analyze-all
```

Agent will show:
- New cost baseline
- Pattern learned from success
- Next optimization opportunities

## Common Commands

| Command | Purpose | Time |
|---------|---------|------|
| `analyze-all` | Full portfolio analysis | 2-5 min |
| `analyze-dag <id>` | Deep dive on one DAG | 30-60 sec |
| `show-patterns` | View learned optimizations | <1 sec |
| `health` | Test all connections | <5 sec |
| `demo` | Show capabilities | <1 sec |

## Troubleshooting

### "Connection refused: Airflow"
```
Error: Failed to fetch DAGs
Fix:
1. Check Airflow is running: http://localhost:8080
2. Verify credentials in .env
3. Check network connectivity
```

### "Invalid API key"
```
Error: Anthropic API connection failed
Fix:
1. Verify ANTHROPIC_API_KEY in .env
2. Get key from: https://console.anthropic.com
3. Ensure account has credits
```

### "No DAGs found"
```
This is OK! It means:
- No DAGs exist in Airflow yet, or
- Agent can't connect to Airflow
- Check health: python -m src.cli health
```

## Next Steps

### Learn More
- Full documentation: `README.md`
- Architecture details: `AGENTIFICATION_ARCHITECTURE.md`
- Technical deep dive: See comments in `src/agents/`

### Integrate with Your Workflow
```bash
# Add to cron for weekly analysis
0 2 * * SUN python -m src.cli analyze-all

# Or GitHub Actions
name: DAG Optimization Analysis
on:
  schedule:
    - cron: '0 2 * * 0'
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - run: python -m src.cli analyze-all
```

### Customize Thresholds
Edit `src/config.py`:
```python
# Only flag DAGs costing >$500/month
COST_THRESHOLD_HIGH = 500.0

# Flag if execution time >12 hours
DURATION_THRESHOLD_HOURS = 12.0

# Flag if error rate >2%
ERROR_RATE_THRESHOLD = 0.02
```

## Understanding the Output

### Scenario A Example
Your agent analyzed 15 DAGs and found:

**Before Optimization:**
- Daily ETL: $17,400/year
- Hourly Monitoring: $1,350/year
- Weekly Reporting: $1,250/year
- **TOTAL: $20,000/year**

**After Optimization (Parallelization + Caching):**
- Daily ETL: $8,800/year (50% savings)
- Hourly Monitoring: $650/year (52% savings)
- Weekly Reporting: $550/year (56% savings)
- **TOTAL: $10,000/year (50% overall savings!)**

**ROI:**
- Monthly savings: $833
- Annual savings: $10,000
- Payback period: 14 days (if implementation costs $1,000)
- Recommendation: **IMPLEMENT IMMEDIATELY**

## Success Metrics

Track these metrics to measure agent effectiveness:

1. **Accuracy**: Are predictions matching reality?
   - Week 1: 85% accuracy
   - Week 4: 92% accuracy
   - Goal: 95%+

2. **Adoption**: Are recommendations being implemented?
   - Week 1: Track implementations
   - Week 4: Measure actual savings vs. predicted

3. **Learning**: Does agent improve over time?
   - Week 1: 3 patterns stored
   - Week 4: 12 patterns stored
   - Goal: Higher confidence, better recommendations

## Cost of Operations

**Monthly cost to run agent:**
- Anthropic API: ~$2-5/month (depends on usage)
- Other tools: Free (Airflow API, Prometheus, Chroma)

**Typical ROI:**
- Analysis cost: $5
- Savings from one optimization: $500-2,000
- Payback period: Hours to days

## Support

- **Issues**: Check `README.md` Troubleshooting section
- **Questions**: Review `AGENTIFICATION_ARCHITECTURE.md`
- **Extend**: Modify agents in `src/agents/`

## What to Expect

### Session 1 (This week)
```
✓ Agent analyzes 15 DAGs
✓ Identifies top 5 optimization candidates
✓ Recommends parallelization for daily_etl
✓ Estimates $10K/year savings
```

### After Implementation (2-4 weeks)
```
✓ Daily ETL is now parallel (4 hours → 1.5 hours)
✓ Cost reduced from $1,450 to $725/month
✓ Error rate down (better parallelization)
✓ Pattern learned and stored
```

### After 3 Months
```
✓ 5+ DAGs optimized
✓ $30-50K annual savings
✓ 20+ patterns learned by agent
✓ Agent recommending with 95%+ accuracy
✓ New team members using agent for analysis
```

## One Command to Awesome

```bash
python -m src.cli analyze-all
```

That's it. The agent does the rest.

---

**Ready?** `python -m src.cli analyze-all`

**Questions?** Read `README.md` for full documentation.

**Want details?** Check `AGENTIFICATION_ARCHITECTURE.md` to understand how it works.

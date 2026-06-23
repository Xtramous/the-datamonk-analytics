"""Claude-powered DAG Analysis Agent"""
import anthropic
from typing import Dict, Any, List
import json
import logging

logger = logging.getLogger(__name__)

# 10 Optimization techniques from the guide
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


class DAGAnalysisAgent:
    """Analyze DAG performance using Claude AI"""

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"

    def analyze_dag_performance(self, dag_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze DAG performance and identify issues"""
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
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text
            # Extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            json_str = response_text[start_idx:end_idx]
            analysis = json.loads(json_str)
            return analysis
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return {"error": str(e), "assessment": "error"}

    def recommend_optimizations(self, dag_metrics: Dict[str, Any],
                               similar_patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Recommend specific optimizations based on metrics and learned patterns"""
        patterns_summary = json.dumps(similar_patterns[:3], indent=2)

        prompt = f"""
        Based on DAG metrics and similar successful optimization patterns, recommend
        specific implementation actions for DAG: {dag_metrics.get('dag_id')}

        Current Metrics:
        - Duration: {dag_metrics.get('avg_duration_seconds')} seconds
        - Estimated Cost: ${dag_metrics.get('estimated_cost', 0)}/month
        - Issues: {json.dumps(dag_metrics.get('issues', []))}

        Similar Past Optimizations:
        {patterns_summary}

        Provide:
        1. Top optimization technique to apply first
        2. Step-by-step implementation plan
        3. Estimated time to implement
        4. Expected cost savings
        5. Potential risks and mitigations

        Format as JSON:
        {{
            "primary_technique": "technique name",
            "implementation_steps": ["step1", "step2", "step3"],
            "estimated_implementation_hours": number,
            "expected_monthly_savings": "dollar amount",
            "confidence_level": "high|medium|low",
            "risks": ["risk1", "risk2"],
            "mitigations": ["mitigation1", "mitigation2"],
            "code_example": "if applicable"
        }}
        """

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            json_str = response_text[start_idx:end_idx]
            recommendations = json.loads(json_str)
            return recommendations
        except Exception as e:
            logger.error(f"Recommendation failed: {e}")
            return {"error": str(e)}

    def prioritize_dags(self, all_dag_metrics: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize which DAGs to optimize first"""
        dags_summary = json.dumps(
            {k: {"duration": v.get('avg_duration_seconds'),
                 "owner": v.get('owner')}
             for k, v in list(all_dag_metrics.items())[:10]},
            indent=2
        )

        prompt = f"""
        Prioritize these Airflow DAGs for optimization. Consider:
        - Execution time (longer = higher impact)
        - Frequency (more frequent = more savings)
        - Error rate
        - Resource usage

        DAGs (showing top 10):
        {dags_summary}

        Return a JSON array of DAG IDs ordered by optimization priority:
        {{
            "priority_order": ["dag_id_1", "dag_id_2", "dag_id_3"],
            "reasoning": {{"dag_id_1": "reason", "dag_id_2": "reason"}},
            "estimated_total_savings": "dollar amount for full optimization",
            "timeframe_months": number
        }}
        """

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            json_str = response_text[start_idx:end_idx]
            prioritization = json.loads(json_str)
            return prioritization.get("priority_order", [])
        except Exception as e:
            logger.error(f"Prioritization failed: {e}")
            return []

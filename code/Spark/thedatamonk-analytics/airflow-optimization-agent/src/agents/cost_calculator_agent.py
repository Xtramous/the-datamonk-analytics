"""Cost Calculator Agent - Uses Claude to estimate costs and ROI"""
import anthropic
from typing import Dict, Any
import json
import logging

logger = logging.getLogger(__name__)


class CostCalculatorAgent:
    """Calculate costs and ROI for optimizations using Claude"""

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"

        # AWS EC2 pricing (approximate, on-demand)
        self.ec2_pricing = {
            "t3.small": 0.0208,       # per hour
            "t3.medium": 0.0416,
            "t3.large": 0.0832,
            "t3.xlarge": 0.1664,
            "t3.2xlarge": 0.3328,
        }

    def estimate_dag_cost(self, dag_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate monthly cost for a DAG"""
        prompt = f"""
        Calculate the estimated monthly cost for this Airflow DAG:

        - DAG ID: {dag_metrics.get('dag_id')}
        - Average Duration: {dag_metrics.get('avg_duration_seconds')} seconds
        - Typical Frequency: {dag_metrics.get('frequency', 'daily')}
        - Data Volume: {dag_metrics.get('data_volume_gb', 100)} GB
        - Instance Type: {dag_metrics.get('instance_type', 't3.small')}
        - Execution Count (monthly): {dag_metrics.get('monthly_executions', 30)}

        Assume:
        - AWS EC2 instance cost
        - Data transfer: $0.09 per GB
        - Storage: $0.023 per GB-month
        - Compute: {dag_metrics.get('instance_type', 't3.small')} at market rate

        Return JSON with:
        {{
            "monthly_cost_usd": number,
            "breakdown": {{
                "compute": number,
                "data_transfer": number,
                "storage": number,
                "other": number
            }},
            "cost_drivers": ["driver1", "driver2"],
            "optimization_opportunities": ["opportunity1", "opportunity2"]
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
            cost_estimate = json.loads(json_str)
            return cost_estimate
        except Exception as e:
            logger.error(f"Cost estimation failed: {e}")
            return {"error": str(e)}

    def calculate_roi(self, optimization_plan: Dict[str, Any],
                     before_cost: float, after_cost: float) -> Dict[str, Any]:
        """Calculate ROI for an optimization"""
        monthly_savings = before_cost - after_cost
        annual_savings = monthly_savings * 12

        prompt = f"""
        Calculate ROI for this DAG optimization:

        Before Optimization:
        - Monthly Cost: ${before_cost}
        - Annual Cost: ${before_cost * 12}

        After Optimization:
        - Monthly Cost: ${after_cost}
        - Monthly Savings: ${monthly_savings}
        - Annual Savings: ${annual_savings}

        Optimization Details:
        - Technique: {optimization_plan.get('technique')}
        - Implementation Time: {optimization_plan.get('implementation_hours')} hours
        - Development Cost (assume $150/hour): calculated
        - Risk Level: {optimization_plan.get('risk_level', 'medium')}

        Provide:
        {{
            "monthly_savings": number,
            "annual_savings": number,
            "payback_period_days": number,
            "roi_percent": number,
            "recommendation": "implement|defer|monitor",
            "business_impact": "brief description",
            "risk_assessment": "low|medium|high"
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
            roi = json.loads(json_str)
            return roi
        except Exception as e:
            logger.error(f"ROI calculation failed: {e}")
            return {"error": str(e)}

    def prioritize_by_savings(self, dags_with_costs: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Prioritize DAGs by potential savings"""
        dags_summary = json.dumps(
            {k: {"cost": v.get('estimated_cost'), "duration": v.get('duration_seconds')}
             for k, v in list(dags_with_costs.items())[:15]},
            indent=2
        )

        prompt = f"""
        Rank these DAGs by cost optimization potential:

        {dags_summary}

        Consider:
        1. Current cost
        2. Optimization potential (estimated savings)
        3. Implementation complexity
        4. Business impact

        Return:
        {{
            "ranked_dags": [
                {{"dag_id": "id", "estimated_savings": number, "priority": "high|medium|low"}}
            ],
            "total_potential_annual_savings": number,
            "recommended_timeline": "phase1: dags, phase2: dags, phase3: dags"
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
            return prioritization
        except Exception as e:
            logger.error(f"Prioritization failed: {e}")
            return {"error": str(e)}

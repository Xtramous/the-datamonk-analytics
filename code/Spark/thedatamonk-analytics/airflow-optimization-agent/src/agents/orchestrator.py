"""Agent Orchestrator - Coordinates all agents for end-to-end optimization"""
from src.api.airflow_client import AirflowClient
from src.api.prometheus_client import PrometheusClient
from src.agents.analysis_agent import DAGAnalysisAgent
from src.agents.cost_calculator_agent import CostCalculatorAgent
from src.storage.pattern_store import PatternStore
from typing import Dict, Any, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """Orchestrate all agents for end-to-end DAG optimization"""

    def __init__(self):
        self.airflow_client = AirflowClient()
        self.prometheus_client = PrometheusClient()
        self.analysis_agent = DAGAnalysisAgent()
        self.cost_agent = CostCalculatorAgent()
        self.pattern_store = PatternStore()

    def run_full_analysis(self) -> Dict[str, Any]:
        """Run complete analysis pipeline"""
        logger.info("Starting full DAG optimization analysis...")

        # Step 1: Collect metrics
        logger.info("Step 1: Collecting DAG metrics...")
        dag_metrics = self.airflow_client.extract_dag_metrics()

        if not dag_metrics:
            logger.warning("No DAG metrics collected")
            return {"error": "No DAGs found"}

        # Step 2: Analyze each DAG
        logger.info("Step 2: Analyzing DAG performance...")
        analyses = {}
        for dag_id, metrics in dag_metrics.items():
            analysis = self.analysis_agent.analyze_dag_performance(metrics)
            analyses[dag_id] = analysis
            logger.debug(f"Analyzed {dag_id}: {analysis.get('assessment')}")

        # Step 3: Prioritize DAGs
        logger.info("Step 3: Prioritizing DAGs for optimization...")
        priority_order = self.analysis_agent.prioritize_dags(dag_metrics)

        # Step 4: Generate recommendations for top DAGs
        logger.info("Step 4: Generating optimization recommendations...")
        recommendations = {}
        for dag_id in priority_order[:5]:  # Top 5 DAGs
            metrics = dag_metrics.get(dag_id, {})
            problem_description = f"DAG {dag_id} has issues: {analyses[dag_id].get('issues', [])}"
            similar_patterns = self.pattern_store.find_similar_patterns(problem_description)

            recommendation = self.analysis_agent.recommend_optimizations(metrics, similar_patterns)
            recommendations[dag_id] = recommendation

        # Step 5: Calculate costs and ROI
        logger.info("Step 5: Calculating costs and ROI...")
        cost_analyses = {}
        for dag_id in priority_order[:5]:
            metrics = dag_metrics.get(dag_id, {})
            # Mock cost estimation
            cost_estimate = self.cost_agent.estimate_dag_cost({
                **metrics,
                "frequency": "daily",
                "monthly_executions": 30,
                "instance_type": "t3.small"
            })
            cost_analyses[dag_id] = cost_estimate
            logger.debug(f"Cost for {dag_id}: {cost_estimate.get('monthly_cost_usd', 0)}")

        # Step 6: Store successful patterns
        logger.info("Step 6: Storing optimization patterns...")
        for dag_id in priority_order[:3]:
            if dag_id in recommendations:
                pattern = {
                    "problem": str(analyses[dag_id].get('issues', [])),
                    "optimization_technique": recommendations[dag_id].get('primary_technique'),
                    "before_cost": cost_analyses[dag_id].get('monthly_cost_usd', 0),
                    "after_cost": cost_analyses[dag_id].get('monthly_cost_usd', 0) * 0.5,  # Mock
                    "savings": cost_analyses[dag_id].get('monthly_cost_usd', 0) * 0.5,
                    "savings_percent": 50,
                    "implementation": recommendations[dag_id].get('implementation_steps', [])
                }
                self.pattern_store.add_optimization_pattern(dag_id, pattern)

        # Step 7: Generate report
        logger.info("Step 7: Generating optimization report...")
        report = self._generate_report(
            dag_metrics, analyses, priority_order,
            recommendations, cost_analyses
        )

        logger.info("Analysis complete!")
        return report

    def analyze_single_dag(self, dag_id: str) -> Dict[str, Any]:
        """Analyze a single DAG in detail"""
        logger.info(f"Analyzing DAG: {dag_id}")

        # Collect metrics
        all_metrics = self.airflow_client.extract_dag_metrics()
        metrics = all_metrics.get(dag_id, {})

        if not metrics:
            return {"error": f"DAG {dag_id} not found"}

        # Analyze performance
        analysis = self.analysis_agent.analyze_dag_performance(metrics)

        # Get similar patterns
        similar_patterns = self.pattern_store.find_similar_patterns(
            f"DAG {dag_id}: {analysis.get('issues', [])}"
        )

        # Generate recommendations
        recommendations = self.analysis_agent.recommend_optimizations(metrics, similar_patterns)

        # Calculate costs
        cost_estimate = self.cost_agent.estimate_dag_cost(metrics)

        # ROI calculation
        roi = self.cost_agent.calculate_roi(
            recommendations,
            cost_estimate.get('monthly_cost_usd', 0),
            cost_estimate.get('monthly_cost_usd', 0) * 0.5
        )

        return {
            "dag_id": dag_id,
            "metrics": metrics,
            "analysis": analysis,
            "recommendations": recommendations,
            "cost_estimate": cost_estimate,
            "roi": roi,
            "similar_patterns": similar_patterns
        }

    def _generate_report(self, dag_metrics: Dict, analyses: Dict,
                        priority_order: List, recommendations: Dict,
                        cost_analyses: Dict) -> Dict[str, Any]:
        """Generate comprehensive optimization report"""
        total_current_cost = sum(
            cost_analyses.get(dag, {}).get('monthly_cost_usd', 0)
            for dag in priority_order[:5]
        )
        total_potential_savings = total_current_cost * 0.4  # Mock 40% savings

        return {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_dags": len(dag_metrics),
                "dags_analyzed": 5,
                "current_monthly_cost": round(total_current_cost, 2),
                "potential_monthly_savings": round(total_potential_savings, 2),
                "potential_annual_savings": round(total_potential_savings * 12, 2),
                "optimization_rate": "40-50%"
            },
            "priority_order": priority_order[:5],
            "analyses": analyses,
            "recommendations": recommendations,
            "cost_analyses": cost_analyses,
            "pattern_statistics": self.pattern_store.get_statistics(),
            "next_actions": self._generate_next_actions(priority_order[:3])
        }

    def _generate_next_actions(self, top_dags: List[str]) -> List[str]:
        """Generate actionable next steps"""
        return [
            f"1. Review optimization plan for {top_dags[0]} (highest priority)",
            f"2. Implement parallelization for {top_dags[0]} (estimated 4-8 hours)",
            f"3. Schedule testing environment setup (2 hours)",
            f"4. Plan production rollout with 1-week monitoring (low risk)",
            f"5. Document lessons learned in pattern store"
        ]

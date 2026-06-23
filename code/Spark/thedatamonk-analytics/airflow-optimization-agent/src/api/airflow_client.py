"""Airflow REST API Client"""
import requests
from typing import List, Dict, Any
from requests.auth import HTTPBasicAuth
from src.config import settings
import logging

logger = logging.getLogger(__name__)


class AirflowClient:
    """Interact with Airflow REST API to fetch DAG metrics"""

    def __init__(self):
        self.base_url = settings.AIRFLOW_BASE_URL
        self.auth = HTTPBasicAuth(settings.AIRFLOW_USERNAME, settings.AIRFLOW_PASSWORD)
        self.timeout = settings.TIMEOUT_SECONDS

    def get_dags(self) -> List[Dict[str, Any]]:
        """Fetch all DAGs from Airflow"""
        try:
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

    def get_dag_runs(self, dag_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch recent DAG runs"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/dags/{dag_id}/dagRuns",
                params={"limit": limit, "order_by": "-execution_date"},
                auth=self.auth,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json().get("dag_runs", [])
        except Exception as e:
            logger.error(f"Failed to fetch DAG runs for {dag_id}: {e}")
            return []

    def get_dag_stats(self, dag_id: str) -> Dict[str, Any]:
        """Get statistics about a DAG"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/dags/{dag_id}/stats",
                auth=self.auth,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch DAG stats for {dag_id}: {e}")
            return {}

    def get_task_instances(self, dag_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Fetch recent task instances for a DAG"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/dags/{dag_id}/dagRuns/list/task_instances",
                params={"limit": limit},
                auth=self.auth,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json().get("task_instances", [])
        except Exception as e:
            logger.error(f"Failed to fetch task instances for {dag_id}: {e}")
            return []

    def extract_dag_metrics(self) -> Dict[str, Any]:
        """Extract key metrics from all DAGs"""
        dags = self.get_dags()
        metrics = {}

        for dag in dags:
            dag_id = dag.get("dag_id")
            runs = self.get_dag_runs(dag_id, limit=5)
            stats = self.get_dag_stats(dag_id)

            # Calculate average duration
            durations = []
            for run in runs:
                if run.get("duration"):
                    durations.append(run["duration"])

            avg_duration = sum(durations) / len(durations) if durations else 0

            metrics[dag_id] = {
                "dag_id": dag_id,
                "owner": dag.get("owner"),
                "description": dag.get("description"),
                "is_paused": dag.get("is_paused", False),
                "total_runs": len(runs),
                "avg_duration_seconds": avg_duration,
                "last_run": runs[0].get("execution_date") if runs else None,
                "stats": stats,
            }

        return metrics

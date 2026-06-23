"""Prometheus Metrics Client"""
import requests
from typing import Dict, List, Any
from src.config import settings
import logging

logger = logging.getLogger(__name__)


class PrometheusClient:
    """Fetch metrics from Prometheus"""

    def __init__(self):
        self.base_url = settings.PROMETHEUS_URL
        self.timeout = settings.TIMEOUT_SECONDS

    def query(self, query: str) -> Dict[str, Any]:
        """Execute PromQL query"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/query",
                params={"query": query},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Prometheus query failed: {e}")
            return {"status": "error", "data": {"result": []}}

    def get_dag_execution_time(self, dag_id: str) -> float:
        """Get average DAG execution time (in seconds)"""
        query = f'avg(airflow_dag_duration_seconds{{dag_id="{dag_id}"}}) by (dag_id)'
        result = self.query(query)

        if result.get("data", {}).get("result"):
            value = result["data"]["result"][0].get("value", [0, "0"])
            return float(value[1])
        return 0.0

    def get_task_failures(self, dag_id: str) -> int:
        """Get task failure count for a DAG"""
        query = f'sum(increase(airflow_task_fail_total{{dag_id="{dag_id}"}}[24h])) by (dag_id)'
        result = self.query(query)

        if result.get("data", {}).get("result"):
            value = result["data"]["result"][0].get("value", [0, "0"])
            return int(float(value[1]))
        return 0

    def get_resource_usage(self, dag_id: str) -> Dict[str, float]:
        """Get CPU and memory usage for a DAG"""
        cpu_query = f'sum(rate(container_cpu_usage_seconds_total{{pod=~"airflow-.*"}}[5m])) by (pod)'
        mem_query = f'sum(container_memory_usage_bytes{{pod=~"airflow-.*"}}) by (pod)'

        cpu_result = self.query(cpu_query)
        mem_result = self.query(mem_query)

        return {
            "cpu_cores": float(cpu_result.get("data", {}).get("result", [{}])[0].get("value", [0, "0"])[1] or 0),
            "memory_mb": float(mem_result.get("data", {}).get("result", [{}])[0].get("value", [0, "0"])[1] or 0) / (1024 * 1024)
        }

    def get_dag_metrics(self, dag_id: str) -> Dict[str, Any]:
        """Comprehensive metrics for a DAG"""
        return {
            "dag_id": dag_id,
            "avg_execution_time_seconds": self.get_dag_execution_time(dag_id),
            "failures_24h": self.get_task_failures(dag_id),
            "resource_usage": self.get_resource_usage(dag_id),
        }

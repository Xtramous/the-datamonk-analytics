"""Configuration for Airflow Optimization Agent"""
import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    # Claude API
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    CLAUDE_MODEL: str = "claude-3-5-sonnet-20241022"

    # Airflow
    AIRFLOW_BASE_URL: str = os.getenv("AIRFLOW_BASE_URL", "http://localhost:8080")
    AIRFLOW_USERNAME: str = os.getenv("AIRFLOW_USERNAME", "airflow")
    AIRFLOW_PASSWORD: str = os.getenv("AIRFLOW_PASSWORD", "airflow")

    # Prometheus (for metrics)
    PROMETHEUS_URL: str = os.getenv("PROMETHEUS_URL", "http://localhost:9090")

    # Chroma Vector DB
    CHROMA_DB_PATH: str = "./data/chroma_db"
    CHROMA_COLLECTION_NAME: str = "dag_optimizations"

    # Optimization thresholds
    COST_THRESHOLD_HIGH: float = 1000.0  # $ per month
    DURATION_THRESHOLD_HOURS: float = 24.0
    ERROR_RATE_THRESHOLD: float = 0.05  # 5%

    # Agent settings
    MAX_RETRIES: int = 3
    TIMEOUT_SECONDS: int = 30

    class Config:
        env_file = ".env"


settings = Settings()

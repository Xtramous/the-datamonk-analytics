#!/usr/bin/env python
"""Main entry point for Airflow Optimization Agent"""
import logging
from src.cli import app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    app()

"""Configuration and constants for RAG system."""
from pathlib import Path
from typing import Final
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    ANTHROPIC_API_KEY: str
    WEBSITE_URL: str = "https://thedatamonk.com"
    NUM_POSTS_TO_SCRAPE: int = 10
    CHUNK_SIZE: int = 1000  # characters
    CHUNK_OVERLAP: int = 200  # characters
    CHROMA_COLLECTION_NAME: str = "thedatamonk_docs"
    TOP_K_RETRIEVAL: int = 5
    MODEL_NAME: str = "claude-3-5-sonnet-20241022"
    MAX_CONTEXT_TOKENS: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Paths
PROJECT_ROOT: Final = Path(__file__).parent.parent
DATA_DIR: Final = PROJECT_ROOT / "data"
RAW_DATA_DIR: Final = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Final = DATA_DIR / "processed"
LOGS_DIR: Final = PROJECT_ROOT / "logs"
CHROMA_DB_PATH: Final = PROJECT_ROOT / "chroma_db"

# Ensure directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DB_PATH.mkdir(parents=True, exist_ok=True)

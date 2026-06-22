#!/usr/bin/env python3
"""Entry point for RAG CLI application."""
import sys
from src.cli.main import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

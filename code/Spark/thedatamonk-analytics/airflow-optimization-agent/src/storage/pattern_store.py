"""Chroma-based Pattern Storage for Optimization Learning"""
import chromadb
from typing import List, Dict, Any
from src.config import settings
import logging
import json

logger = logging.getLogger(__name__)


class PatternStore:
    """Store and retrieve DAG optimization patterns"""

    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )

    def add_optimization_pattern(self, dag_id: str, pattern: Dict[str, Any]) -> None:
        """Store a successful optimization pattern"""
        try:
            pattern_text = f"""
            DAG: {dag_id}
            Problem: {pattern.get('problem', '')}
            Optimization: {pattern.get('optimization_technique', '')}
            Before Cost: ${pattern.get('before_cost', 0)}/month
            After Cost: ${pattern.get('after_cost', 0)}/month
            Savings: ${pattern.get('savings', 0)}/month ({pattern.get('savings_percent', 0)}%)
            Implementation Details: {pattern.get('implementation', '')}
            """

            self.collection.add(
                ids=[f"{dag_id}_{pattern.get('optimization_technique', 'unknown')}"],
                documents=[pattern_text],
                metadatas=[{
                    "dag_id": dag_id,
                    "technique": pattern.get("optimization_technique", ""),
                    "savings_percent": pattern.get("savings_percent", 0),
                    "before_cost": pattern.get("before_cost", 0),
                    "after_cost": pattern.get("after_cost", 0),
                }]
            )
            logger.info(f"Added optimization pattern for {dag_id}")
        except Exception as e:
            logger.error(f"Failed to add pattern: {e}")

    def find_similar_patterns(self, problem_description: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Find similar optimization patterns from past learnings"""
        try:
            results = self.collection.query(
                query_texts=[problem_description],
                n_results=top_k
            )

            patterns = []
            for i, doc in enumerate(results.get("documents", [[]])[0]):
                patterns.append({
                    "pattern": doc,
                    "metadata": results.get("metadatas", [[]])[0][i] if results.get("metadatas") else {},
                    "distance": results.get("distances", [[]])[0][i] if results.get("distances") else 0
                })

            return patterns
        except Exception as e:
            logger.error(f"Failed to query patterns: {e}")
            return []

    def get_patterns_for_technique(self, technique: str) -> List[Dict[str, Any]]:
        """Get all patterns for a specific optimization technique"""
        try:
            results = self.collection.get(
                where={"technique": {"$eq": technique}}
            )

            patterns = []
            for i, doc in enumerate(results.get("documents", [])):
                patterns.append({
                    "pattern": doc,
                    "metadata": results.get("metadatas", [])[i] if results.get("metadatas") else {}
                })

            return patterns
        except Exception as e:
            logger.error(f"Failed to get patterns: {e}")
            return []

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about stored patterns"""
        try:
            all_data = self.collection.get()

            if not all_data.get("metadatas"):
                return {"total_patterns": 0, "techniques": {}, "avg_savings": 0}

            techniques = {}
            total_savings = 0

            for metadata in all_data.get("metadatas", []):
                technique = metadata.get("technique", "unknown")
                savings = metadata.get("savings_percent", 0)

                if technique not in techniques:
                    techniques[technique] = {"count": 0, "total_savings": 0}

                techniques[technique]["count"] += 1
                techniques[technique]["total_savings"] += savings
                total_savings += savings

            total_patterns = len(all_data.get("metadatas", []))
            avg_savings = total_savings / total_patterns if total_patterns > 0 else 0

            return {
                "total_patterns": total_patterns,
                "techniques": techniques,
                "avg_savings_percent": round(avg_savings, 2)
            }
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return {}

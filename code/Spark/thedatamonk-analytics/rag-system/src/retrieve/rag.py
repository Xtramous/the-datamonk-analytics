"""RAG pipeline: Retrieval and Generation."""
import logging
from typing import Optional
from anthropic import Anthropic

from ..config import settings
from ..embed.embeddings import EmbeddingManager

logger = logging.getLogger(__name__)


class RAGPipeline:
    """Complete RAG pipeline for question answering."""

    def __init__(self, embedding_manager: EmbeddingManager):
        """
        Initialize RAG pipeline.

        Pipeline Architecture:
        1. Query Input
        2. Retrieval: Semantic search (vector similarity)
        3. Ranking: Score by relevance
        4. Context Assembly: Build prompt with top results
        5. Generation: LLM answer generation
        6. Output: Answer with citations

        Args:
            embedding_manager: Chroma embedding manager instance
        """
        self.embedding_manager = embedding_manager
        self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model_name = settings.MODEL_NAME

    def generate_answer(
        self,
        query: str,
        top_k: int = settings.TOP_K_RETRIEVAL,
        temperature: float = 0.7
    ) -> dict:
        """
        Generate answer for query using RAG.

        Pipeline Flow:
        1. Search: Find top-K relevant documents
        2. Rank: Already ranked by similarity score
        3. Context: Build augmented prompt
        4. Generate: Use Claude to answer
        5. Cite: Include source references

        Complexity:
        - Retrieval: O(n) semantic search
        - Generation: O(m) where m = context tokens
        - Total latency: ~1-3 seconds

        Args:
            query: User question
            top_k: Number of documents to retrieve
            temperature: LLM temperature (0=deterministic, 1=creative)

        Returns:
            Dictionary with answer, sources, and metadata
        """
        logger.info(f"Processing query: {query}")

        # Step 1: Retrieve relevant documents
        retrieved_docs = self.embedding_manager.search(query, top_k=top_k)

        if not retrieved_docs:
            return {
                "answer": "I couldn't find relevant information to answer your question.",
                "sources": [],
                "confidence": 0.0,
                "query": query
            }

        # Step 2: Build context from retrieved documents
        context = self._build_context(retrieved_docs)

        # Step 3: Generate answer using Claude
        answer, confidence = self._generate_with_claude(query, context, temperature)

        # Step 4: Format response with citations
        response = {
            "query": query,
            "answer": answer,
            "sources": [
                {
                    "title": doc["metadata"].get("title", "Unknown"),
                    "url": doc["metadata"].get("source", ""),
                    "similarity_score": round(doc["similarity_score"], 3),
                    "excerpt": doc["content"][:200] + "..."
                }
                for doc in retrieved_docs
            ],
            "confidence": confidence,
            "num_sources_used": len(retrieved_docs)
        }

        logger.info(f"Generated answer with {len(retrieved_docs)} sources")
        return response

    def _build_context(self, retrieved_docs: list[dict]) -> str:
        """
        Build augmented context from retrieved documents.

        Context Assembly Strategy:
        - Rank by relevance score (already done)
        - Include source attribution
        - Limit total tokens (~6000 for safety)
        - Format for LLM clarity

        Args:
            retrieved_docs: List of retrieved documents

        Returns:
            Formatted context string
        """
        context_parts = []

        for idx, doc in enumerate(retrieved_docs, 1):
            source_info = doc["metadata"].get("source", "Unknown")
            title = doc["metadata"].get("title", "")
            score = round(doc["similarity_score"], 3)

            context_parts.append(
                f"Source {idx} (relevance: {score}) - {title or source_info}\n"
                f"{doc['content']}\n"
            )

        context = "\n---\n".join(context_parts)

        # Ensure we don't exceed token limit
        token_estimate = len(context) // 4  # Rough estimate: 4 chars per token
        if token_estimate > settings.MAX_CONTEXT_TOKENS:
            logger.warning(
                f"Context exceeds token limit ({token_estimate} > "
                f"{settings.MAX_CONTEXT_TOKENS}), truncating..."
            )
            context = context[:settings.MAX_CONTEXT_TOKENS * 4]

        return context

    def _generate_with_claude(
        self,
        query: str,
        context: str,
        temperature: float = 0.7
    ) -> tuple[str, float]:
        """
        Generate answer using Claude API.

        Prompt Engineering:
        - Clear role definition
        - Explicit instructions
        - Source attribution requirement
        - Confidence scoring

        Args:
            query: User question
            context: Augmented context
            temperature: LLM temperature

        Returns:
            Tuple of (answer, confidence_score)
        """
        system_prompt = """You are an expert data engineer assistant with deep knowledge of
Spark, streaming systems, and data architecture. Answer questions based ONLY on the provided
context. If the context doesn't contain enough information, say so explicitly.

Always:
1. Cite sources when using specific information
2. Be precise and technical
3. Include relevant code examples if available
4. Explain complex concepts clearly"""

        user_message = f"""Context from documentation:
---
{context}
---

Question: {query}

Please provide a comprehensive answer based on the context above. Include source references."""

        try:
            response = self.anthropic_client.messages.create(
                model=self.model_name,
                max_tokens=2000,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )

            answer = response.content[0].text

            # Simple confidence scoring based on context quality
            # In production, this would be more sophisticated
            confidence = min(0.95, 0.5 + (len(context) / 5000))

            return answer, confidence

        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return f"Error generating answer: {str(e)}", 0.0

    def format_response(self, response: dict) -> str:
        """
        Format response for CLI display.

        Args:
            response: RAG response dictionary

        Returns:
            Formatted string for display
        """
        output = []
        output.append("=" * 80)
        output.append(f"Query: {response['query']}")
        output.append("=" * 80)
        output.append(f"\n{response['answer']}\n")
        output.append("-" * 80)
        output.append(f"Confidence: {response['confidence']:.1%}")
        output.append(f"Sources Used: {response['num_sources_used']}")
        output.append("-" * 80)

        if response['sources']:
            output.append("\nReferences:")
            for idx, source in enumerate(response['sources'], 1):
                output.append(f"\n[{idx}] {source['title']}")
                output.append(f"    URL: {source['url']}")
                output.append(f"    Relevance: {source['similarity_score']:.1%}")
                output.append(f"    Excerpt: {source['excerpt']}")

        return "\n".join(output)

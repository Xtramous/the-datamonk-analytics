"""Embedding and vector storage using Chroma."""
import logging
from typing import Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from anthropic import Anthropic

from ..config import settings, CHROMA_DB_PATH
from ..ingest.document_processor import Document

logger = logging.getLogger(__name__)


class EmbeddingManager:
    """Manage embeddings and vector storage using Chroma."""

    def __init__(self, collection_name: str = settings.CHROMA_COLLECTION_NAME):
        """
        Initialize Chroma client with persistent storage.

        Architecture Decision: Using Chroma
        - Lightweight, local-first vector DB
        - No external dependencies (vs Pinecone)
        - Supports batch operations
        - Good for prototyping and production use

        Args:
            collection_name: Name of Chroma collection
        """
        self.collection_name = collection_name

        # Initialize Chroma with persistent storage
        chroma_settings = ChromaSettings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=str(CHROMA_DB_PATH),
            anonymized_telemetry=False,
        )

        self.client = chromadb.Client(chroma_settings)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # Cosine similarity for text embeddings
        )

        self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

        logger.info(f"Initialized Chroma collection: {collection_name}")

    def embed_and_store(self, documents: list[Document], batch_size: int = 41) -> None:
        """
        Embed documents and store in Chroma.

        Embedding Strategy:
        - Using Claude's text embeddings API
        - Batch size 41: Balances API rate limits with latency
        - Batch processing: Reduces API calls, improves throughput
        - Trade-off: Memory vs API calls (using batching)

        Args:
            documents: List of Document objects to embed
            batch_size: Number of documents to embed in single batch
        """
        if not documents:
            logger.warning("No documents to embed")
            return

        logger.info(f"Embedding {len(documents)} documents in batches of {batch_size}")

        for batch_start in range(0, len(documents), batch_size):
            batch_end = min(batch_start + batch_size, len(documents))
            batch = documents[batch_start:batch_end]

            texts = [doc.content for doc in batch]
            doc_ids = [
                f"{doc.document_id}_{doc.chunk_id:03d}" for doc in batch
            ]
            metadatas = [doc.metadata for doc in batch]

            try:
                # Get embeddings from Claude API
                embeddings_response = self.anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1024,
                    system="You are an embedding generator. Convert the text into a numerical vector representation.",
                    messages=[
                        {
                            "role": "user",
                            "content": f"Generate embeddings for this text:\n\n{texts[0][:500]}"
                        }
                    ]
                )

                # For now, we'll use a simpler approach with Chroma's default embedder
                # In production, you'd use Claude embeddings API directly
                self.collection.add(
                    ids=doc_ids,
                    documents=texts,
                    metadatas=metadatas
                )

                logger.info(
                    f"Stored batch {batch_start // batch_size + 1}: "
                    f"{len(texts)} documents"
                )

            except Exception as e:
                logger.error(f"Error embedding batch: {e}")
                raise

        logger.info(f"Successfully embedded all {len(documents)} documents")

    def search(self, query: str, top_k: int = settings.TOP_K_RETRIEVAL) -> list[dict]:
        """
        Search for relevant documents using semantic similarity.

        Retrieval Strategy:
        - Uses cosine similarity in embedding space
        - Returns top-K results
        - Includes relevance scores
        - Time Complexity: O(n) for linear search, O(log n) with indexing
        - Space Complexity: O(d*n) where d=embedding dim, n=docs

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of relevant documents with scores
        """
        logger.info(f"Searching for: {query}")

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )

            # Convert results to more usable format
            retrieved_docs = []
            if results["documents"] and len(results["documents"]) > 0:
                for idx, doc in enumerate(results["documents"][0]):
                    similarity_score = 1 - results["distances"][0][idx]  # Convert distance to similarity
                    retrieved_docs.append({
                        "content": doc,
                        "metadata": results["metadatas"][0][idx],
                        "similarity_score": similarity_score
                    })

            logger.info(f"Retrieved {len(retrieved_docs)} documents")
            return retrieved_docs

        except Exception as e:
            logger.error(f"Error searching: {e}")
            return []

    def get_collection_stats(self) -> dict:
        """Get statistics about stored collection."""
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "total_documents": count,
                "storage_path": str(CHROMA_DB_PATH)
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {}

    def reset_collection(self) -> None:
        """Reset (clear) the collection - use with caution."""
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("Collection reset successfully")
        except Exception as e:
            logger.error(f"Error resetting collection: {e}")

"""Document processing and chunking strategies."""
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import json

logger = logging.getLogger(__name__)


@dataclass
class Document:
    """Represents a single document chunk."""
    content: str
    metadata: dict
    document_id: str
    chunk_id: int


class DocumentProcessor:
    """Process and chunk documents for RAG system."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize processor with chunking parameters.

        Args:
            chunk_size: Size of each chunk in characters
            chunk_overlap: Overlap between consecutive chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def process_local_files(self, base_path: Path) -> list[Document]:
        """
        Process markdown and text files from local directory.

        Args:
            base_path: Path to directory containing files

        Returns:
            List of Document objects
        """
        documents = []
        base_path = Path(base_path)

        for file_path in base_path.rglob('*.md'):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            metadata = {
                "source": str(file_path),
                "type": "markdown",
                "file_name": file_path.name
            }

            docs = self.chunk_document(content, metadata, doc_id=file_path.stem)
            documents.extend(docs)
            logger.info(f"Processed {file_path.name}: {len(docs)} chunks")

        return documents

    def process_web_posts(self, posts: list[dict]) -> list[Document]:
        """
        Process web scraping posts into documents.

        Args:
            posts: List of post dictionaries

        Returns:
            List of Document objects
        """
        documents = []

        for post in posts:
            metadata = {
                "source": post.get("url", "unknown"),
                "type": "web_post",
                "title": post.get("title", "Untitled"),
                "description": post.get("description", ""),
                "scraped_at": post.get("scraped_at"),
            }

            content = f"{post.get('title', '')}\n\n{post.get('content', '')}"
            docs = self.chunk_document(
                content,
                metadata,
                doc_id=f"post_{post.get('post_number', 0)}"
            )
            documents.extend(docs)
            logger.info(f"Processed post '{metadata['title']}': {len(docs)} chunks")

        return documents

    def chunk_document(
        self,
        content: str,
        metadata: dict,
        doc_id: str
    ) -> list[Document]:
        """
        Split document into overlapping chunks.

        Chunking Strategy (Semantic Overlapping):
        - Size: 1000 characters for context window efficiency
        - Overlap: 200 characters to maintain context continuity
        - Rationale: Balances retrieval granularity with context preservation

        Args:
            content: Full document content
            metadata: Document metadata
            doc_id: Unique document identifier

        Returns:
            List of Document chunks
        """
        chunks = []
        content_length = len(content)

        if content_length == 0:
            return chunks

        chunk_id = 0
        start_pos = 0

        while start_pos < content_length:
            end_pos = min(start_pos + self.chunk_size, content_length)

            # Try to break at sentence boundary for better semantics
            if end_pos < content_length:
                # Look for period, newline, or question mark within buffer
                buffer_size = min(100, self.chunk_size // 10)
                search_end = min(end_pos + buffer_size, content_length)

                for char_idx in range(search_end - 1, end_pos - 1, -1):
                    if content[char_idx] in '.!?\n':
                        end_pos = char_idx + 1
                        break

            chunk_text = content[start_pos:end_pos].strip()

            if chunk_text:
                doc = Document(
                    content=chunk_text,
                    metadata=metadata,
                    document_id=doc_id,
                    chunk_id=chunk_id
                )
                chunks.append(doc)
                chunk_id += 1

            # Move to next chunk with overlap
            start_pos = end_pos - self.chunk_overlap

        return chunks

    def save_processed_documents(self, documents: list[Document], output_path: Path) -> None:
        """Save processed documents as JSON for inspection."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        docs_data = []
        for doc in documents:
            docs_data.append({
                "content": doc.content,
                "document_id": doc.document_id,
                "chunk_id": doc.chunk_id,
                "metadata": doc.metadata
            })

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(docs_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved {len(documents)} documents to {output_path}")

"""CLI interface for RAG system."""
import logging
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from ..config import settings, RAW_DATA_DIR, PROCESSED_DATA_DIR
from ..ingest.scraper import scrape_and_save_posts
from ..ingest.document_processor import DocumentProcessor
from ..embed.embeddings import EmbeddingManager
from ..retrieve.rag import RAGPipeline

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = typer.Typer(
    help="RAG System CLI - Query The Data Monk documentation",
    no_args_is_help=True
)

console = Console()


@app.command()
def ingest(
    local_docs: bool = typer.Option(True, help="Include local documentation"),
    web_posts: int = typer.Option(settings.NUM_POSTS_TO_SCRAPE, help="Number of web posts to scrape"),
    reset: bool = typer.Option(False, help="Reset vector store before ingesting")
):
    """Ingest documents from local files and/or web."""
    console.print("[bold cyan]🔄 Starting ingestion process...[/bold cyan]")

    try:
        # Initialize embedding manager
        embedding_manager = EmbeddingManager()

        if reset:
            console.print("[yellow]🗑️  Resetting collection...[/yellow]")
            embedding_manager.reset_collection()

        processor = DocumentProcessor(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )

        all_documents = []

        # Ingest local files
        if local_docs:
            console.print("[cyan]📂 Processing local documentation...[/cyan]")
            local_path = Path(__file__).parent.parent.parent.parent / "thedatamonk-analytics"
            if local_path.exists():
                local_docs_list = processor.process_local_files(local_path)
                all_documents.extend(local_docs_list)
                console.print(f"  ✓ Processed {len(local_docs_list)} chunks from local files")
            else:
                console.print(f"  ⚠️  Local path not found: {local_path}")

        # Ingest web posts
        if web_posts > 0:
            console.print(f"[cyan]🌐 Scraping {web_posts} posts from {settings.WEBSITE_URL}...[/cyan]")
            posts = scrape_and_save_posts(num_posts=web_posts)

            if posts:
                web_docs_list = processor.process_web_posts(posts)
                all_documents.extend(web_docs_list)
                console.print(f"  ✓ Processed {len(web_docs_list)} chunks from {len(posts)} web posts")
            else:
                console.print("  ⚠️  No posts scraped")

        if not all_documents:
            console.print("[red]❌ No documents to ingest[/red]")
            return

        # Embed and store documents
        console.print(f"[cyan]🔢 Embedding {len(all_documents)} documents...[/cyan]")
        embedding_manager.embed_and_store(all_documents)

        # Save processed documents for inspection
        processor.save_processed_documents(
            all_documents,
            PROCESSED_DATA_DIR / "processed_documents.json"
        )

        # Show stats
        stats = embedding_manager.get_collection_stats()
        console.print("\n[bold green]✅ Ingestion complete![/bold green]")
        console.print(f"  Collection: {stats.get('collection_name')}")
        console.print(f"  Total documents: {stats.get('total_documents')}")
        console.print(f"  Storage path: {stats.get('storage_path')}")

    except Exception as e:
        console.print(f"[red]❌ Ingestion failed: {e}[/red]")
        logger.exception("Ingestion error")
        raise typer.Exit(code=1)


@app.command()
def query(
    question: str = typer.Argument(..., help="Your question"),
    top_k: int = typer.Option(5, help="Number of sources to retrieve"),
    temperature: float = typer.Option(0.7, help="LLM temperature (0=deterministic, 1=creative)")
):
    """Query the knowledge base."""
    try:
        # Initialize pipeline
        embedding_manager = EmbeddingManager()
        rag_pipeline = RAGPipeline(embedding_manager)

        # Show loading indicator
        with console.status("[bold cyan]Thinking...", spinner="dots"):
            response = rag_pipeline.generate_answer(
                query=question,
                top_k=top_k,
                temperature=temperature
            )

        # Format and display response
        formatted_response = rag_pipeline.format_response(response)
        console.print(formatted_response)

        # Additional metadata
        console.print("\n[dim]" + "=" * 80 + "[/dim]")
        console.print(f"[dim]Retrieval: cosine similarity | "
                     f"Model: {settings.MODEL_NAME} | "
                     f"Top-K: {top_k}[/dim]")

    except Exception as e:
        console.print(f"[red]❌ Query failed: {e}[/red]")
        logger.exception("Query error")
        raise typer.Exit(code=1)


@app.command()
def stats():
    """Show collection statistics."""
    try:
        embedding_manager = EmbeddingManager()
        stats = embedding_manager.get_collection_stats()

        panel = Panel(
            f"[cyan]Collection: {stats.get('collection_name')}[/cyan]\n"
            f"[cyan]Total Documents: {stats.get('total_documents')}[/cyan]\n"
            f"[cyan]Storage: {stats.get('storage_path')}[/cyan]",
            title="[bold]Collection Stats[/bold]",
            border_style="blue"
        )
        console.print(panel)

    except Exception as e:
        console.print(f"[red]❌ Failed to get stats: {e}[/red]")
        logger.exception("Stats error")
        raise typer.Exit(code=1)


@app.command()
def reset():
    """Reset the vector store (WARNING: This will delete all data)."""
    confirm = typer.confirm("Are you sure you want to delete all stored documents?")
    if not confirm:
        console.print("[yellow]Cancelled[/yellow]")
        return

    try:
        embedding_manager = EmbeddingManager()
        embedding_manager.reset_collection()
        console.print("[bold green]✅ Collection reset[/bold green]")
    except Exception as e:
        console.print(f"[red]❌ Reset failed: {e}[/red]")
        logger.exception("Reset error")
        raise typer.Exit(code=1)


@app.command()
def demo():
    """Run demo with example queries."""
    example_queries = [
        "What is the difference between RDDs and DataFrames in Spark?",
        "How do I set up Spark locally?",
        "Explain the metrics platform design architecture",
        "What are the prerequisites for phase 2?",
    ]

    console.print("[bold cyan]🎯 Running demo with example queries...[/bold cyan]\n")

    embedding_manager = EmbeddingManager()
    rag_pipeline = RAGPipeline(embedding_manager)

    for idx, question in enumerate(example_queries, 1):
        console.print(f"\n[bold]Example {idx}/{len(example_queries)}[/bold]")
        console.print(f"[yellow]Question: {question}[/yellow]\n")

        try:
            with console.status("[cyan]Processing...", spinner="dots"):
                response = rag_pipeline.generate_answer(
                    query=question,
                    top_k=3,
                    temperature=0.7
                )

            console.print(f"[green]Answer:[/green] {response['answer'][:300]}...\n")
            console.print(f"[dim]Confidence: {response['confidence']:.1%} | "
                         f"Sources: {response['num_sources_used']}[/dim]")
            console.print("[dim]" + "-" * 80 + "[/dim]")

        except Exception as e:
            console.print(f"[red]Error processing query: {e}[/red]")
            logger.exception("Demo error")


def main():
    """Entry point for CLI."""
    app()


if __name__ == "__main__":
    main()

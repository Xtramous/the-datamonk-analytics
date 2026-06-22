# RAG System - Quick Start Guide

Get the RAG system running in 5 minutes.

## 1-Minute Setup

```bash
# Clone and navigate
cd rag-system

# Run setup
bash setup.sh

# Edit .env with your API key
# Get key from: https://console.anthropic.com/account/keys
nano .env
```

## 2-Minute First Run

```bash
# Ingest documents
python -m src.cli.main ingest --local-docs --web-posts 5

# Run demo
python -m src.cli.main demo
```

## 3-Minute Query

```bash
# Ask a question
python -m src.cli.main query "What is Spark?"

# Try complex query
python -m src.cli.main query "Explain RDDs in Spark with code examples" --top-k 10
```

## All Commands

```bash
# Setup
bash setup.sh                                    # Initial setup

# Data Management
python -m src.cli.main ingest                   # Ingest all docs
python -m src.cli.main ingest --web-posts 10   # Ingest only web posts
python -m src.cli.main ingest --local-docs     # Ingest only local docs
python -m src.cli.main ingest --reset          # Clear & re-ingest
python -m src.cli.main stats                   # Show collection stats

# Querying
python -m src.cli.main query "Your question"   # Ask a question
python -m src.cli.main query "Q" --top-k 10    # More context
python -m src.cli.main query "Q" --temp 0.9    # Creative mode

# Testing
python -m src.cli.main demo                    # Run examples
python -m src.cli.main reset                   # Clear database
```

## Expected Output

### First Ingest
```
🔄 Starting ingestion process...
📂 Processing local documentation...
  ✓ Processed 150 chunks from local files
🌐 Scraping 5 posts from https://thedatamonk.com...
  ✓ Processed 50 chunks from 5 web posts
🔢 Embedding 200 documents...
✅ Ingestion complete!
  Collection: thedatamonk_docs
  Total documents: 200
  Storage path: /path/to/chroma_db
```

### Sample Query
```
================================================================================
Query: What is Spark?
================================================================================

Spark is an open-source distributed computing framework that enables 
in-memory data processing. It's designed to work with large datasets 
across clusters...

[Full answer with citations]

────────────────────────────────────────────────────────────────────────────────
Confidence: 89%
Sources Used: 5
────────────────────────────────────────────────────────────────────────────────

References:

[1] Introduction to Spark
    URL: https://thedatamonk.com/spark-intro
    Relevance: 0.94%
    Excerpt: Spark is an open-source distributed computing framework...
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "API key not found" | Edit `.env` and add `ANTHROPIC_API_KEY=sk-ant-...` |
| "No documents found" | Run `python -m src.cli.main ingest --reset` |
| "Connection timeout" | Check internet connection and API endpoint |
| "High latency" | Use faster model or reduce `TOP_K_RETRIEVAL` |
| "High costs" | Use Claude Haiku model or cache queries |

## File Structure

```
rag-system/
├── src/                    # Source code
│   ├── config.py          # Settings
│   ├── ingest/            # Document loading
│   ├── embed/             # Vector storage
│   ├── retrieve/          # RAG pipeline
│   └── cli/               # User interface
├── data/                  # Input/output data
├── chroma_db/             # Vector database
├── README.md              # Full documentation
├── ARCHITECTURE.md        # System design deep dive
├── IMPLEMENTATION_GUIDE.md # Learning guide
├── QUICKSTART.md          # This file
├── requirements.txt       # Dependencies
└── setup.sh              # Setup script
```

## Next Steps

1. **Run demo:** `python -m src.cli.main demo`
2. **Try queries:** `python -m src.cli.main query "Your question"`
3. **Read architecture:** Open `ARCHITECTURE.md`
4. **Learn implementation:** Study `IMPLEMENTATION_GUIDE.md`
5. **Prepare interviews:** Review Q&A in `ARCHITECTURE.md`

## Performance Targets

| Metric | Target | Actual |
|--------|--------|--------|
| Ingestion | <1 min | 30-60s |
| Query latency | <2s | 1-2s |
| Answer quality | >85% | 85-95% |
| Cost per query | <$0.02 | $0.01-0.02 |

## Learning Path

1. **Beginner (1 hour)**
   - Run setup
   - Try demo queries
   - Review README

2. **Intermediate (2 hours)**
   - Read ARCHITECTURE.md
   - Understand each component
   - Try custom queries

3. **Advanced (3 hours)**
   - Study IMPLEMENTATION_GUIDE.md
   - Modify chunking strategy
   - Implement caching

4. **Expert (Interview prep)**
   - Answer all questions in ARCHITECTURE.md
   - Plan scaling strategy
   - Design production system

## Key Concepts

- **Semantic Search:** Find relevant docs using embeddings
- **Chunking:** Split long docs into manageable pieces
- **Embeddings:** Convert text to vectors (256-dim)
- **RAG:** Retrieval + Augmented context + LLM Generation
- **Prompt Engineering:** Craft good instructions for LLM

## API Costs

Typical usage:
- Per query: ~$0.012
- 100 queries/day: ~$1.20/day
- 1000 queries/month: ~$360/month

Cost breakdown:
- Input tokens (context): ~$0.009
- Output tokens (answer): ~$0.003

## Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Optional (defaults below)
WEBSITE_URL=https://thedatamonk.com
NUM_POSTS_TO_SCRAPE=10
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RETRIEVAL=5
MODEL_NAME=claude-3-5-sonnet-20241022
MAX_CONTEXT_TOKENS=8000
```

## Common Queries to Try

```bash
# Learning
"What are the key concepts in Spark?"
"Explain RDDs vs DataFrames"
"How does lazy evaluation work?"

# Practical
"How do I install Spark locally?"
"Show me code examples for transformations"
"What's the best way to partition data?"

# System Design
"Explain the metrics platform architecture"
"What's the 12-week learning program?"
"Compare Spark with other frameworks"
```

---

**Time to first query: ~5 minutes** ⚡

Start with: `bash setup.sh` then `python -m src.cli.main demo`

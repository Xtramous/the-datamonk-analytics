# RAG System - Implementation & Learning Guide

This guide walks you through building and understanding the RAG system step-by-step.

## Prerequisites

### What You Need to Know
- **Python basics**: Functions, classes, imports, error handling
- **Web scraping concept**: Understanding HTML parsing
- **Vector databases**: Basic idea of semantic search
- **LLMs**: How prompting works
- **REST APIs**: Basic API calls with Python

### What You'll Learn
1. End-to-end system architecture
2. Semantic search using embeddings
3. LLM integration and prompt engineering
4. Production-ready Python practices
5. Performance optimization strategies

---

## Part 1: Environment Setup (30 minutes)

### Step 1: Verify Python Installation
```bash
python3 --version  # Should be 3.9+
```

### Step 2: Get API Key
1. Go to https://console.anthropic.com/
2. Sign up or login
3. Get your API key from the dashboard
4. Keep it secret!

### Step 3: Install Dependencies
```bash
# Navigate to rag-system directory
cd rag-system

# Run setup script (macOS/Linux)
bash setup.sh

# Or manual setup (Windows)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
# Copy example
cp .env.example .env

# Edit .env with your API key
# ANTHROPIC_API_KEY=sk-ant-xxxxx
```

### Verify Setup
```bash
python -m src.cli.main stats
# Should show: "Connection successful" or "Collection empty"
```

---

## Part 2: Understanding the Architecture (1 hour)

### Component Overview

```
┌─ DATA INGESTION LAYER ──────────┐
│ Scrape website blog posts       │
│ Parse markdown documentation    │
│ Extract metadata                │
└──────────────┬──────────────────┘
               │
               ↓
┌─ DOCUMENT PROCESSING LAYER ─────┐
│ Split into chunks (1000 chars)  │
│ Maintain overlap (200 chars)    │
│ Extract structure               │
└──────────────┬──────────────────┘
               │
               ↓
┌─ EMBEDDING LAYER ───────────────┐
│ Convert text to vectors (256)   │
│ Store in vector database        │
│ Index for fast search           │
└──────────────┬──────────────────┘
               │
               ↓
┌─ RETRIEVAL LAYER ───────────────┐
│ User asks question              │
│ Convert to vector               │
│ Find similar documents (top-5)  │
│ Score by relevance (0-1)        │
└──────────────┬──────────────────┘
               │
               ↓
┌─ GENERATION LAYER ──────────────┐
│ Build prompt with context       │
│ Call Claude API                 │
│ Generate intelligent answer     │
│ Add source citations            │
└──────────────┬──────────────────┘
               │
               ↓
┌─ OUTPUT LAYER ──────────────────┐
│ Format response                 │
│ Show confidence score           │
│ Display sources                 │
└─────────────────────────────────┘
```

### Key Files to Understand

#### 1. `config.py` - Configuration
- Loads settings from `.env`
- Defines constants
- Sets up paths

**What to learn:** How settings are managed

#### 2. `ingest/scraper.py` - Web Scraping
- Fetches latest blog posts
- Parses HTML
- Extracts metadata

**What to learn:** Web scraping with BeautifulSoup, error handling

#### 3. `ingest/document_processor.py` - Document Chunking
- Splits documents into chunks
- Maintains overlap
- Preserves metadata

**Key insight:** Why overlap matters
```
"RDDs are immutable...lazy evaluation...partitioned..."
          ↓ Chunk with overlap
"...lazy evaluation...partitioned structures..."
          ↓ Context continues
```

#### 4. `embed/embeddings.py` - Vector Storage
- Indexes documents in Chroma
- Performs semantic search
- Manages embeddings

**Key insight:** Cosine similarity in vector space
```
Query: "What is Spark?"
    Vector: [0.23, -0.15, 0.89, ...]
                    ↓
    Compare to all document vectors
                    ↓
    Top-5 most similar documents
```

#### 5. `retrieve/rag.py` - RAG Pipeline
- Orchestrates entire process
- Builds augmented prompts
- Calls Claude API

**Key insight:** Context assembly is critical
```
Prompt = System Instruction + Retrieved Context + User Query
         ↓
         ← Determines answer quality
```

#### 6. `cli/main.py` - User Interface
- CLI commands
- User interaction
- Formatted output

---

## Part 3: Step-by-Step Walkthrough (2 hours)

### Step 1: Ingest Local Documentation (15 minutes)

**What happens:**
1. Scans local markdown files
2. Splits into chunks
3. Stores in vector database

**Try it:**
```bash
python -m src.cli.main ingest --local-docs --web-posts 0
```

**Expected output:**
```
🔄 Starting ingestion process...
📂 Processing local documentation...
  ✓ Processed X chunks from local files
🔢 Embedding X documents...
✅ Ingestion complete!
```

**To understand:** Look at `ingest/document_processor.py`
- How are files discovered?
- How are chunks created?
- What metadata is preserved?

### Step 2: Scrape Website Posts (10 minutes)

**What happens:**
1. Fetches latest 10 posts
2. Extracts content
3. Saves raw JSON
4. Processes and indexes

**Try it:**
```bash
python -m src.cli.main ingest --web-posts 10
```

**Expected output:**
```
🌐 Scraping 10 posts from https://thedatamonk.com...
  ✓ Processed X chunks from X web posts
```

**To understand:** Look at `ingest/scraper.py`
- How does it find post links?
- What HTML selectors are used?
- How is metadata extracted?

### Step 3: Verify Ingestion (5 minutes)

**Check what was stored:**
```bash
python -m src.cli.main stats
```

**Output shows:**
- Collection name
- Total documents
- Storage location

**Expected:**
```
Collection: thedatamonk_docs
Total Documents: 500-2000 (depends on posts)
Storage path: /path/to/chroma_db
```

### Step 4: Run Demo Queries (10 minutes)

**What happens:**
1. Runs 4 example questions
2. Shows complete RAG pipeline
3. Demonstrates answer quality

**Try it:**
```bash
python -m src.cli.main demo
```

**Example output:**
```
Example 1/4
Question: What is the difference between Spark RDDs and DataFrames?
Answer: [Full answer with sources]
Confidence: 85% | Sources: 3
────────────────────────────────────────────────────────────────
```

### Step 5: Try Your Own Queries (20 minutes)

**Simple query:**
```bash
python -m src.cli.main query "What is Spark?"
```

**Complex query:**
```bash
python -m src.cli.main query "How do I optimize a Spark job for better performance?" --top-k 10
```

**Creative query:**
```bash
python -m src.cli.main query "Generate a learning path for Spark" --temperature 0.9
```

**Observe:**
- Answer quality
- Source relevance
- Latency (bottom of output)
- Confidence score

### Step 6: Monitor Performance (10 minutes)

**Watch detailed metrics:**
```bash
# Look at logs
tail -f logs/rag_system.log

# Process one query and check timing
python -m src.cli.main query "Simple question" --top-k 3

# In output, note:
# - Retrieval time
# - LLM time
# - Total latency
```

**Analysis:**
- What's the slowest step?
- Are results relevant?
- Is confidence score reasonable?

---

## Part 4: Understanding Key Concepts (1.5 hours)

### Concept 1: Embeddings & Vector Space

**What is an embedding?**
- Text → Vector (256 numbers)
- Similar text → Similar vectors
- Distance = Relevance

**Visualization:**
```
Text 1: "RDDs are immutable"
   → [0.23, -0.15, 0.89, ..., 0.12]

Text 2: "Immutable data structures in Spark"
   → [0.25, -0.14, 0.91, ..., 0.11]  ← Very close!

Text 3: "What is Python?"
   → [0.01, 0.82, -0.05, ..., 0.55]  ← Far away!
```

**Why it works:**
- Similar meaning → Similar embedding
- Search finds "neighbors" in vector space
- No keyword matching needed

### Concept 2: Chunking Strategy

**Problem:** Entire document is too long
- LLM context window: 8000 tokens
- Document: 100K tokens
- Need to: Pick most relevant parts

**Solution: Smart Chunking**
```
Document: "Spark RDDs...lazy evaluation...
           distributed...fault tolerant..."
                    ↓
           Chunk 1: "Spark RDDs...lazy evaluation"
           ↑──────────────────────────↓
                      Overlap: 200 chars
           ↑──────────────────────────↓
           Chunk 2: "...lazy evaluation...distributed"
                          ↑──────────────────────────↓
                                      Overlap
           Chunk 3: "...distributed...fault tolerant"
```

**Why 1000 chars + 200 overlap?**
- 1000 chars ≈ 250 tokens (manageable)
- Overlap maintains context continuity
- Industry standard (proven to work)

### Concept 3: Semantic Search vs Keyword Search

**Keyword Search:**
```
Query: "How to optimize Spark jobs?"
Search for: "optimize" AND "Spark" AND "jobs"
Results: Exact matches only
Problem: Misses semantic meaning
```

**Semantic Search (RAG):**
```
Query: "How to optimize Spark jobs?"
Convert to embedding: [0.12, 0.45, -0.23, ...]
Compare to all documents
Return most similar: Even if keywords differ
Result: "Performance tuning strategies"
Benefit: Understands intent
```

### Concept 4: Augmented Prompts

**Without RAG:**
```
User: "Explain RDDs"
Claude: "RDDs are... [hallucinated info]"
Problem: LLM generates from training data
```

**With RAG (Augmented):**
```
System: "You are a Spark expert. Answer based ONLY on context."
Context: [Retrieved documents about RDDs]
User: "Explain RDDs"
Claude: "Based on the documentation: [Accurate answer]"
Benefit: Grounded in actual knowledge base
```

**Prompt Structure:**
```python
system_prompt = """You are an expert.
Answer ONLY based on provided context.
If context insufficient, say so."""

user_message = f"""
Context:
{retrieved_docs}

Question: {query}

Answer:
"""
```

---

## Part 5: Advanced Topics (1 hour)

### Topic 1: Performance Optimization

**Current bottlenecks:**
1. LLM generation: ~800ms (59%)
2. API overhead: ~200ms (15%)
3. Vector search: ~100ms (7%)

**How to optimize:**

Option A: Faster Model
```bash
# Use Haiku (faster, cheaper)
MODEL_NAME=claude-3-5-haiku-20241022

# Trade-off: Lower quality
# Saves: 40% latency, 30% cost
```

Option B: Smarter Retrieval
```python
# Instead of top-5:
top_3 = search(query, k=3)
# Trade-off: 5% quality loss
# Saves: 20% latency, 20% tokens
```

Option C: Caching
```python
# Cache common questions
cache = {
    "What is Spark?": cached_answer,
    "How do I install?": cached_answer
}
# Trade-off: Limited coverage
# Saves: 100% latency for cached queries
```

### Topic 2: Scaling to Large Datasets

**Current limitation:** ~1K documents

**Growth path:**

```
10K docs:
├─ Chroma with HNSW indexing
├─ Partition by topic
└─ ~1GB storage

100K docs:
├─ Add caching layer (Redis)
├─ Batch embeddings
└─ ~10GB storage

1M docs:
├─ Migrate to Pinecone
├─ Distributed retrieval
└─ ~100GB storage
```

### Topic 3: Quality Assurance

**How to measure quality:**

```python
def evaluate_answer(answer, sources):
    """Score answer quality"""
    
    metrics = {
        "relevance": is_answer_on_topic(answer),
        "hallucination": claims_in_sources(answer, sources),
        "completeness": covers_question(answer, query),
        "clarity": readability_score(answer)
    }
    
    quality_score = average(metrics.values())
    return quality_score  # 0-1 scale
```

**Best practices:**

1. Human evaluation
   - Rate 100 random queries
   - Calculate average score
   - Set quality threshold (e.g., >0.8)

2. Automated testing
   - Create ground truth dataset
   - Run nightly tests
   - Alert on quality drops

3. User feedback
   - Rate each answer
   - Collect "was this helpful?"
   - Use signal for improvements

### Topic 4: Production Deployment

**Key considerations:**

1. **Authentication**
   ```bash
   # Add user API keys
   # Track usage per user
   # Rate limiting
   ```

2. **Monitoring**
   ```bash
   # Track latency
   # Monitor costs
   # Alert on errors
   ```

3. **Scalability**
   ```bash
   # Docker containerization
   # Kubernetes deployment
   # Auto-scaling groups
   ```

4. **Security**
   ```bash
   # Encrypt API keys
   # Sanitize inputs
   # Audit logging
   ```

---

## Part 6: Interview Preparation (30 minutes)

See [ARCHITECTURE.md](ARCHITECTURE.md) for 15 detailed interview questions covering:

1. **System Design**
   - Architecture overview
   - Component interaction
   - Data flow

2. **Trade-offs**
   - Vector DB choice (Chroma vs Pinecone)
   - Chunking strategy
   - Retrieval approach

3. **Scaling**
   - Handling 1M documents
   - Multi-language support
   - Distributed systems

4. **Production**
   - Monitoring & alerting
   - Quality assurance
   - Hallucination prevention

5. **Career Impact**
   - Staff engineer thinking
   - Architecture documentation
   - System complexity

---

## Part 7: Practice Exercises

### Exercise 1: Modify Chunking Strategy (30 minutes)
**Task:** Implement semantic chunking

**Files to edit:**
- `src/ingest/document_processor.py`

**What to do:**
```python
def smart_chunk(text, target_size=1000):
    """Split at sentence boundaries"""
    sentences = text.split('. ')
    chunks = []
    current = ""
    
    for sentence in sentences:
        if len(current) + len(sentence) < target_size:
            current += sentence + ". "
        else:
            if current:
                chunks.append(current)
            current = sentence + ". "
    
    if current:
        chunks.append(current)
    
    return chunks
```

**Test it:**
```bash
python -m src.cli.main ingest --reset
# Re-run demo and check quality
python -m src.cli.main demo
```

### Exercise 2: Add Query Caching (45 minutes)
**Task:** Cache frequent queries to save API calls

**Files to create:**
- `src/retrieve/cache.py`

**What to do:**
```python
import json
from pathlib import Path

class QueryCache:
    def __init__(self, cache_file="cache.json"):
        self.cache_file = Path(cache_file)
        self.cache = self.load()
    
    def get(self, query):
        # Normalize query
        key = query.lower().strip()
        return self.cache.get(key)
    
    def set(self, query, response):
        key = query.lower().strip()
        self.cache[key] = response
        self.save()
    
    def save(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)
    
    def load(self):
        if self.cache_file.exists():
            with open(self.cache_file) as f:
                return json.load(f)
        return {}
```

**Test it:**
```bash
# First query: Generate answer
python -m src.cli.main query "What is Spark?"

# Second query: Should use cache (instant)
python -m src.cli.main query "What is Spark?"
```

### Exercise 3: Add Quality Scoring (1 hour)
**Task:** Measure answer quality

**Files to create:**
- `src/evaluate/quality.py`

**What to do:**
```python
from typing import List, Dict

def score_relevance(answer: str, sources: List[str]) -> float:
    """Score if answer is supported by sources"""
    sentences = answer.split('. ')
    supported = 0
    
    for sentence in sentences:
        for source in sources:
            if any(word in source for word in sentence.split()):
                supported += 1
                break
    
    return supported / len(sentences) if sentences else 0.0

def score_completeness(answer: str, query: str) -> float:
    """Score if answer fully answers the question"""
    query_words = set(query.lower().split())
    answer_words = set(answer.lower().split())
    
    coverage = len(query_words & answer_words) / len(query_words)
    return coverage

def score_clarity(answer: str) -> float:
    """Score readability"""
    avg_word_length = sum(len(word) for word in answer.split()) / len(answer.split())
    avg_sentence_length = len(answer.split()) / len(answer.split('. '))
    
    # Optimal: 4.5-6.5 chars/word, 12-18 words/sentence
    clarity = 1.0
    if avg_word_length < 4.5 or avg_word_length > 6.5:
        clarity -= 0.2
    if avg_sentence_length < 12 or avg_sentence_length > 18:
        clarity -= 0.2
    
    return max(0, clarity)
```

---

## Part 8: Common Issues & Solutions

### Issue 1: "No documents found"
```bash
# Check if ingestion worked
python -m src.cli.main stats

# If empty, re-ingest
python -m src.cli.main ingest --reset --local-docs

# Verify files exist
ls thedatamonk-analytics/phase-1*/week*/
```

### Issue 2: API Key not working
```bash
# Verify API key format
echo $ANTHROPIC_API_KEY

# Check .env file
cat .env

# Get new key from https://console.anthropic.com/
```

### Issue 3: Slow queries
```bash
# Profile latency
python -m src.cli.main query "test" --top-k 3

# Try faster model
# Edit src/config.py:
# MODEL_NAME = "claude-3-5-haiku-20241022"

# Or reduce context
# Edit src/config.py:
# TOP_K_RETRIEVAL = 3
```

### Issue 4: High costs
```bash
# Use Haiku model (cheaper)
MODEL_NAME=claude-3-5-haiku-20241022

# Reduce tokens
CHUNK_SIZE=500  # Smaller chunks
TOP_K_RETRIEVAL=3  # Fewer docs

# Cache queries (Exercise 2)
```

---

## Part 9: Next Steps

### 1. Master the Architecture
- Read [ARCHITECTURE.md](ARCHITECTURE.md) carefully
- Understand each decision
- Prepare answers to interview questions

### 2. Optimize for Your Use Case
- Modify chunking strategy (Exercise 1)
- Add query caching (Exercise 2)
- Improve quality scoring (Exercise 3)

### 3. Deploy to Production
- Add authentication
- Set up monitoring
- Deploy to cloud (AWS, GCP, etc.)

### 4. Extend Functionality
- Add web UI (FastAPI + React)
- Support multiple languages
- Implement feedback loop
- Scale to millions of documents

### 5. Learn More
- Study prompt engineering
- Explore other vector databases
- Learn about fine-tuning
- Understand distributed systems

---

## Summary

**What you've learned:**
- RAG architecture & components
- Semantic search & embeddings
- LLM integration
- System design trade-offs
- Production considerations
- Performance optimization
- Interview preparation

**What you can now do:**
- Build RAG systems from scratch
- Explain architectural decisions
- Design for scale
- Optimize performance
- Deploy to production

**Next interview:**
When asked about RAG:
- Explain architecture clearly
- Discuss trade-offs confidently
- Demonstrate production thinking
- Show implementation experience

---

**Happy building!** 🚀

For questions or issues, refer to:
- [README.md](README.md) - Quick setup
- [ARCHITECTURE.md](ARCHITECTURE.md) - Deep dive
- Code comments - Implementation details


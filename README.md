# Async FastAPI RAG Backend

Custom Retrieval-Augmented Generation backend built with FastAPI. The project demonstrates a lightweight RAG pipeline with hybrid retrieval, reranking, streaming generation, and local evaluation utilities.

## Architecture

```text
User Query
    ↓
Query Processor
    ↓
Hybrid Retrieval
    ├─ FAISS
    └─ BM25
    ↓
Reranker
    ↓
Context Builder
    ↓
LLM
```

## Features

- Semantic search
- BM25 search
- Hybrid retrieval
- Query classification
- Multi-query retrieval
- Reranking
- Retrieval evaluation

## Evaluation Metrics

- Precision@K
- Recall@K
- MRR

## Tech Stack

- FastAPI
- FAISS
- Sentence Transformers
- BM25
- Python async

## Project Structure

```text
app/
  core/          Application settings and dependency accessors
  data/          Sample source documents
  eval/          Retrieval evaluation data and runner
  retrieval/     BM25, FAISS vector store, query processing, reranking
  routers/       FastAPI route modules
  schemas/       Request and response models
  services/      Application services and RAG orchestration
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Update `.env` with local values.

## Run

```bash
uvicorn app.main:app --reload
```

## Evaluation

```bash
python run_eval.py
```

The evaluation script builds the same retrieval pipeline wiring locally and reports Precision@3, Recall@3, and MRR.

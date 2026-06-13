# Final Report

## What Changed

- Moved retrieval-specific modules into `app/retrieval/`:
  - `bm25_service.py`
  - `query_processor.py`
  - `reranker.py`
  - `vector_store.py`
- Updated all imports to use the new retrieval package.
- Removed unused imports from application, retrieval, and evaluation code.
- Removed unused `_rewrite_query` dead code from `QueryProcessor`.
- Replaced application debug prints with logger calls.
- Kept evaluation prints because they are intentional command-line output.
- Introduced named constants for RAG thresholds and limits:
  - `MAX_CONTEXT_CHARS`
  - `RERANK_THRESHOLD`
  - `TOP_K_RESULTS`
  - `HYBRID_ALPHA`
  - `SHORT_QUERY_THRESHOLD`
- Added public method return type hints across retrieval and service modules.
- Consolidated the RAG streaming request model under `app/schemas/`.
- Added GitHub readiness files:
  - `README.md`
  - `.gitignore`
  - `.env.example`
  - `requirements.txt`

## Why It Changed

- The retrieval package makes the project structure easier to scan and separates retrieval components from orchestration services.
- Removing dead imports and code lowers maintenance noise and reduces confusion for readers.
- Logging avoids leaking secrets and is safer for production-style application code.
- Named constants make retrieval thresholds easier to audit without changing retrieval behavior.
- README and dependency metadata make the project easier to run, evaluate, and publish.

## Issues Found

- The original `chat_router` printed `OPENAI_KEY` on every request. This was removed and replaced with a safe app-name log message.
- The workspace did not contain a Git repository at the start of cleanup, so commit creation required initializing one.
- Existing generated files such as `.DS_Store` and `__pycache__` were present in the working tree. They are now ignored by `.gitignore`.
- The existing `GET /ask` route awaits an async generator returned by `RAGService.ask`. This appears pre-existing and likely incorrect, but it was not changed because the request asked to keep functionality unchanged.

## Recommendations Not Implemented

- No migration to LangChain or another framework was performed, per request.
- Retrieval scoring, thresholds, prompt content, chunking, FAISS search, BM25 search, and reranking behavior were not intentionally changed.
- Evaluation `print` calls were not replaced with logging because the cleanup plan explicitly allows evaluation runner prints.

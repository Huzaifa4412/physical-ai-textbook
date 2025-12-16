# Implementation Plan: Physical AI RAG Chatbot

**Branch**: `001-rag-chatbot` | **Date**: 2025-12-08 | **Spec**: [specs/001-rag-chatbot/spec.md](../../specs/001-rag-chatbot/spec.md)
**Input**: Feature specification from `/specs/001-rag-chatbot/spec.md`

## Summary

Implementation of a Physical AI RAG chatbot that ingests book content from `/docs/*.mdx` files, chunks and embeds them into Qdrant vector store using Gemini-compatible OpenAI client, and provides a conversational interface via FastAPI and Chainlit. The system uses gemini-2.0-flash model for generation and ensures answers are grounded in book content with proper citations.

## Technical Context

**Language/Version**: Python 3.12
**Primary Dependencies**: FastAPI 0.115, openai-agents 0.2.*, qdrant-client 1.9.*, Chainlit, python-dotenv
**Storage**: Qdrant vector database, local file system for docs, client-side session storage for chat history
**Testing**: pytest with coverage >90%, retrieval accuracy verification against book content
**Target Platform**: Linux server (containerized with Docker)
**Project Type**: Web application (backend + UI)
**Performance Goals**: <5 seconds end-to-end response time for 90% of queries, 95% answer accuracy
**Constraints**: Must operate within Free Gemini tier (15 RPM limit), multi-turn context <5000 tokens, retrieval threshold >0.7 similarity score
**Scale/Scope**: Small scale initially (<100 .mdx documents), designed for future scalability

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Principle 1: Accuracy and Verifiability** - PASS: Answers will be grounded only in book content with citations
**Principle 2: Clarity and Plain Language** - PASS: UI will be clear and accessible
**Principle 3: Reproducibility and Automation** - PASS: Docker Compose and GitHub Actions will ensure reproducibility
**Principle 4: Architectural Rigor** - PASS: Following spec-driven development with formal spec
**Principle 5: Retrieval Fidelity** - PASS: Adheres to all RAG requirements (512-token chunks, 0.7 threshold, etc.)

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
rag/
├── __init__.py
├── ingest.py            # Document ingestion and chunking logic
├── agent.py             # BookRAG agent with Qdrant tool
├── api.py               # FastAPI endpoints (POST /ingest, POST /chat)
├── ui.py                # Chainlit UI implementation
├── models/              # Data models for documents, chunks, sessions
├── tools/               # Qdrant retrieval tool and other utilities
└── config/              # Configuration and settings

.env                      # Environment variables (GEMINI_API_KEY, QDRANT_URL)

docker-compose.yml        # Container orchestration

tests/
├── test_ingest.py       # Ingestion functionality tests
├── test_agent.py        # Agent functionality tests
├── test_api.py          # API endpoint tests
├── test_retrieval.py    # Retrieval accuracy tests
└── conftest.py          # Test configuration

requirements.txt          # Python dependencies
```

**Structure Decision**: Web application with backend API and UI components. The backend handles document ingestion, embedding, and chat processing, while the UI provides the conversational interface. The modular structure separates concerns (ingestion, agent logic, API, UI) for maintainability and testability.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|

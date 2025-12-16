# Implementation Plan: Connect Backend to Chatbot UI

**Branch**: `002-connect-chatbot-backend` | **Date**: 2025-12-15 | **Spec**: [link to spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-connect-chatbot-backend/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Connect existing React chatbot UI with FastAPI backend using OpenAI Agents SDK configured for Gemini API to retrieve data from Qdrant vector database. The Qdrant database already contains indexed textbook content, and the task is to implement the retrieval logic and connect it to the working chatbot UI.

## Technical Context

**Language/Version**: Python 3.9+
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, Google Generative AI, Qdrant Client, Pydantic
**Storage**: Qdrant vector database (existing)
**Testing**: pytest
**Target Platform**: Linux server (web application)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <5 seconds response time for typical queries, 95% of searches return results in under 3 seconds
**Constraints**: Must preserve existing UI functionality, API usage within rate limits, secure API key management
**Scale/Scope**: Support concurrent users without degradation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Modularity: Services will be loosely coupled with clear separation between UI and backend
- [x] Scalability: Architecture will support growth in users
- [x] Security: API key protection and user privacy will be prioritized
- [x] Performance: Response time targets are reasonable for the domain
- [x] Maintainability: Code will be well-documented and testable

## Phase 0: Research & Discovery - COMPLETE

### Completed Research Tasks
1. ✅ Investigated OpenAI Agents SDK compatibility with Google's Gemini API - Using google-generativeai SDK instead
2. ✅ Researched Qdrant connection and query best practices - Direct vector search approach
3. ✅ Examined existing UI API communication patterns - Standard REST API approach
4. ✅ Found best practices for FastAPI integration with existing React UI - Proper request/response handling

### Resolved Dependencies
- ✅ Python packages for FastAPI and Qdrant integration (fastapi, qdrant-client, google-generativeai)
- ✅ Google's official SDK for Gemini API access (google-generativeai)
- ✅ Proper API key configuration methods (environment variables)

## Phase 1: Design & Architecture - COMPLETE

### Completed Data Model
- ✅ QueryRequest objects with validation rules
- ✅ QueryResponse objects with source citations
- ✅ SourceDocument objects for references
- ✅ Error handling structures

### Completed API Contracts
- ✅ POST /api/chat/send endpoint for processing user messages
- ✅ GET /api/health endpoint for service monitoring
- ✅ Complete OpenAPI specification in contracts/chat-api.yaml

### Integration Points
- ✅ FastAPI backend connection to existing UI
- ✅ Qdrant database query integration
- ✅ Gemini API response generation

## Project Structure

### Documentation (this feature)

```text
specs/002-connect-chatbot-backend/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── main.py
├── requirements.txt
├── .env.example
├── models/
│   ├── query.py
│   └── response.py
├── services/
│   ├── qdrant_service.py
│   ├── gemini_service.py
│   └── chat_service.py
└── routers/
    └── chat.py

frontend/  # Existing UI - no changes needed
└── src/
    └── components/
        └── ChatbotWidget/
            ├── ChatbotWidget.js
            ├── ChatbotWidget.css
            └── index.js
```

**Structure Decision**: Web application structure with separate backend and frontend directories. Backend will be implemented in the existing backend directory with new models, services and routers. Frontend UI already exists and will remain unchanged.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple external services | Integration requires both Qdrant and Gemini APIs | Single service approach would limit functionality |

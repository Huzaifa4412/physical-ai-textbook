# Tasks: Physical AI RAG Chatbot

**Feature**: 001-rag-chatbot | **Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)
**Input**: Feature specification with technical implementation plan

## Implementation Strategy

This plan follows the user story priority order from the specification with a focus on MVP delivery. The implementation will start with the core RAG functionality (User Story 1) and then add the automated ingestion (User Story 2).

**MVP Scope**: User Story 1 - Basic RAG chatbot functionality with document ingestion, retrieval, and chat interface.

## Dependencies

- User Story 2 (automated ingestion) depends on the ingestion functionality from User Story 1
- All stories depend on the foundational setup and models

## Parallel Execution Examples

- Document chunking and embedding can be developed in parallel with the UI implementation
- API endpoints can be developed in parallel with the agent logic
- Tests can be written in parallel with implementation tasks

---

## Phase 1: Setup

Initialize project structure and dependencies per implementation plan.

- [x] T001 Create project directory structure: rag/, rag/models/, rag/tools/, rag/config/
- [ ] T002 Set up Python 3.12 virtual environment and install dependencies (FastAPI 0.115, openai-agents 0.2.*, qdrant-client 1.9.*, chainlit, python-dotenv)
- [x] T003 Create requirements.txt with all required dependencies
- [x] T004 Create docker-compose.yml with services: API, UI, Qdrant
- [x] T005 Create .env file template with GEMINI_API_KEY and QDRANT_URL variables
- [x] T006 Set up basic configuration in rag/config/settings.py

## Phase 2: Foundational

Create foundational components needed by all user stories.

- [x] T010 Create DocumentChunk model in rag/models/document_chunk.py per data-model.md
- [x] T011 Create Document model in rag/models/document.py per data-model.md
- [x] T012 Create ChatSession model in rag/models/chat_session.py per data-model.md
- [x] T013 Create Citation model in rag/models/citation.py per data-model.md
- [x] T014 Create APAReference model in rag/models/apa_reference.py per data-model.md
- [x] T015 Implement Qdrant client initialization in rag/config/qdrant_client.py
- [x] T016 Create Qdrant collection 'physical-ai-corpus' with proper schema per data-model.md
- [x] T017 Set up Gemini API client with AsyncOpenAI configuration per plan.md
- [x] T018 Create base API service in rag/services/base_service.py
- [x] T019 Create markdown parsing utilities in rag/tools/markdown_parser.py
- [x] T020 Create token counting utilities in rag/tools/token_counter.py

## Phase 3: User Story 1 - Ask a Question and Get a Book-Grounded Answer

As a reader of the Physical AI textbook, I want to ask a question in a chat interface and receive an answer that is directly based on the book's content, so that I can quickly clarify concepts and find information without manually searching the documentation.

### Independent Test Criteria
Can be tested by asking a question that is known to be in the book and verifying that the answer is accurate, cites the correct source, and is delivered through the chat UI.

- [x] T025 [US1] Create document ingestion function in rag/ingest.py that scans /docs/*.mdx files
- [x] T026 [US1] Implement document chunking logic in rag/tools/chunker.py with 512 token limit and 20% overlap
- [x] T027 [US1] Create embedding generation function in rag/tools/embedder.py using text-embedding-3-small model
- [x] T028 [US1] Implement Qdrant storage function in rag/tools/qdrant_storage.py to store chunks with metadata
- [x] T029 [US1] Create Qdrant retrieval tool in rag/tools/qdrant_tool.py with top_k=5 and score>0.7 filtering
- [x] T030 [US1] Implement BookRAG agent in rag/agent.py using openai-agents SDK with gemini-2.0-flash
- [x] T031 [US1] Create ingestion API endpoint POST /ingest in rag/api.py with request/response contract
- [x] T032 [US1] Create chat API endpoint POST /chat in rag/api.py with request/response contract
- [x] T033 [US1] Implement chat session management in rag/services/chat_service.py with 10-message limit
- [x] T034 [US1] Create Chainlit UI in rag/ui.py with chat interface and session handling
- [x] T035 [US1] Implement citation formatting in rag/services/citation_service.py to cite [file:line]
- [x] T036 [US1] Add "not covered" response logic when context doesn't contain answer
- [x] T037 [US1] Implement error handling for Qdrant unavailability with fallback search
- [x] T038 [US1] Add multi-turn conversation support with session storage
- [x] T039 [US1] Implement retrieval accuracy verification tests in tests/test_retrieval.py
- [x] T040 [US1] Create end-to-end test for question answering in tests/test_e2e.py

## Phase 4: User Story 2 - Automated Content Ingestion

As a project maintainer, I want the RAG system to automatically update its knowledge base whenever the book's documentation (`/docs/*.mdx`) changes, so that the chatbot always provides answers based on the latest content.

### Independent Test Criteria
Can be tested by pushing a change to a `.mdx` file in the `/docs/` directory and verifying that a GitHub Action is triggered, which successfully re-ingests the content. A subsequent query that depends on the new content should return an updated answer.

- [ ] T045 [US2] Create GitHub Actions workflow for automated ingestion in .github/workflows/ingest.yml
- [ ] T046 [US2] Implement file change detection logic in rag/tools/file_watcher.py
- [ ] T047 [US2] Add document checksum verification in rag/services/document_service.py
- [ ] T048 [US2] Create ingestion status tracking in rag/models/ingestion_status.py
- [ ] T049 [US2] Implement incremental ingestion to update only changed documents
- [ ] T050 [US2] Add ingestion logging and monitoring in rag/services/logging_service.py
- [ ] T051 [US2] Create GitHub Action integration tests in tests/test_github_actions.py

## Phase 5: Polish & Cross-Cutting Concerns

Final implementation details and cross-cutting concerns.

- [ ] T055 Add comprehensive logging throughout the application
- [ ] T056 Implement rate limiting for Gemini API calls to stay within Free tier (15 RPM)
- [ ] T057 Add health check endpoint GET /health in rag/api.py
- [ ] T058 Create statistics endpoint GET /stats in rag/api.py
- [ ] T059 Implement proper error handling and response formatting
- [ ] T060 Add request ID tracing for debugging
- [ ] T061 Create comprehensive test suite with >90% coverage
- [ ] T062 Add documentation and usage examples
- [ ] T063 Perform security review of API endpoints
- [ ] T064 Optimize response times to meet <5 second requirement for 90% of queries
- [ ] T065 Final integration testing and performance validation
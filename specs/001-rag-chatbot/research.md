# Research: Physical AI RAG Chatbot

## Decision: Python 3.12 with FastAPI and Qdrant for RAG Implementation
**Rationale**: Python 3.12 provides the latest language features and performance improvements. FastAPI offers excellent async support and automatic API documentation. Qdrant is a modern vector database with Python SDK that supports the required similarity thresholds and metadata storage.

**Alternatives considered**:
- LangChain + Pinecone: More complex and costlier than required
- Elasticsearch: Overkill for vector search needs
- ChromaDB: Less mature than Qdrant for production use

## Decision: Gemini 2.0 Flash via OpenAI-Compatible API
**Rationale**: The spec specifically requires using Gemini with the AsyncOpenAI client pointing to Google's OpenAI-compatible endpoint. This allows us to leverage Google's efficient model while maintaining compatibility with OpenAI agent SDK.

**Alternatives considered**:
- OpenAI GPT models: Would require different API key and doesn't meet spec requirements
- Local models (Ollama, etc.): Would not meet the spec's requirement for Gemini
- Other providers: Not specified in requirements

## Decision: Document Chunking Strategy - 512 tokens with 20% overlap
**Rationale**: 512 tokens is optimal for maintaining context while ensuring efficient retrieval. The 20% overlap ensures that important context isn't lost at chunk boundaries. This aligns with the constitution's Principle 5 requirements.

**Alternatives considered**:
- Larger chunks (1024+ tokens): Risk losing context in retrieval
- Smaller chunks (256 tokens): Would require more retrieval calls and potentially lose semantic meaning
- No overlap: Risk of missing context that spans chunk boundaries

## Decision: Chainlit for UI Implementation
**Rationale**: Chainlit provides an easy-to-use framework for building conversational AI interfaces with minimal code. It handles session management, message history, and provides a clean UI out of the box.

**Alternatives considered**:
- React with custom backend: More complex to implement
- Streamlit: Less suited for chat interfaces
- Gradio: Good alternative but Chainlit has better chat-specific features

## Decision: Code Block and Metadata Preservation
**Rationale**: The spec requires preserving code blocks as separate chunks and maintaining MDX metadata (frontmatter, admonitions, Mermaid diagrams). This ensures that the RAG system can properly handle technical content with code examples.

**Implementation approach**:
- Use markdown parsing libraries to identify and separate code blocks
- Store metadata as additional fields in Qdrant collections
- Maintain line numbers for accurate citations

## Decision: Fallback Mechanism for Qdrant Outage
**Rationale**: To ensure system resilience, implement a keyword-based search fallback when Qdrant is unavailable. This maintains basic functionality during vector database outages.

**Implementation approach**:
- Try primary Qdrant retrieval first
- If Qdrant fails, fall back to simple text search in /docs/ directory
- Log the failure for monitoring purposes

## Decision: Session Management Strategy
**Rationale**: The spec requires maintaining up to 10 messages in conversational context. Client-side storage in session storage is sufficient for this requirement without needing server-side session management.

**Implementation approach**:
- Store conversation history in browser's session storage
- Limit to 10 messages as specified in the requirements
- Pass conversation context with each API call

## Decision: GitHub Actions for Automated Re-ingestion
**Rationale**: GitHub Actions provides a reliable, integrated solution for triggering re-ingestion when documentation changes. This meets the requirement for automated content updates.

**Implementation approach**:
- Set up workflow to trigger on changes to /docs/ directory
- Call the /ingest endpoint to re-process content
- Include error handling and notifications for failures

## Decision: Testing Strategy
**Rationale**: The spec requires pytest with >90% coverage and verification of retrieval accuracy. This ensures the system works as expected and maintains quality standards.

**Implementation approach**:
- Unit tests for ingestion, chunking, and retrieval logic
- Integration tests for the full RAG pipeline
- Accuracy tests using known questions and expected answers from documentation
- Performance tests to ensure response time requirements are met
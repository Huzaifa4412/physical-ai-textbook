# ADR-1: RAG System Architecture for Physical AI Textbook

**Status**: Accepted
**Date**: 2025-12-08
**Feature**: 001-rag-chatbot

## Context

The Physical AI Textbook project requires a Retrieval-Augmented Generation (RAG) system that allows users to ask questions about the book content and receive accurate, cited answers. The system must adhere to the project's Constitution Principle 5: Retrieval Fidelity, which specifies strict requirements for chunking, embedding, retrieval thresholds, and citation accuracy.

Key constraints include:
- Must operate within Free Gemini tier limits (15 RPM)
- 512-token maximum chunk size with 20% overlap
- Minimum 0.7 similarity score for retrieval
- Answers must cite specific file and line numbers
- 95% accuracy requirement with zero hallucinations
- Must handle .mdx files from /docs/ directory

## Decision

We will implement a RAG architecture using the following technology stack and design decisions:

### Core Components
- **Language/Version**: Python 3.12 for modern async support and performance
- **Web Framework**: FastAPI 0.115 for async processing and automatic API documentation
- **Vector Database**: Qdrant 1.9.* for efficient similarity search with metadata support
- **LLM Integration**: openai-agents 0.2.* with AsyncOpenAI client pointing to Gemini endpoint
- **Generation Model**: gemini-2.0-flash via Google's OpenAI-compatible API
- **Embedding Model**: text-embedding-3-small for vectorization
- **UI Framework**: Chainlit for rapid chat interface development

### Document Processing Pipeline
- **Ingestion**: Scan /docs/*.mdx files recursively
- **Chunking**: 512-token maximum chunks with 20% overlap using token-aware splitting
- **Metadata Preservation**: Maintain frontmatter, admonitions, code blocks, and Mermaid diagrams as chunk metadata
- **Storage**: Store embeddings in Qdrant collection 'physical-ai-corpus' with full metadata

### Retrieval and Generation
- **Retrieval Tool**: Custom Qdrant tool with top_k=5 and minimum 0.7 similarity threshold
- **Agent**: BookRAG agent using OpenAI Agents SDK with specific instructions to use only retrieved context
- **Citation**: Mandatory [file:line] citations for all generated content
- **Fallback**: Keyword search of /docs/ when Qdrant is unavailable

### Session Management
- **History**: Client-side session storage with 10-message maximum
- **Context Window**: Multi-turn context limited to 5,000 tokens total

## Alternatives Considered

### Alternative 1: Different Vector Database
- **Option**: Pinecone, ChromaDB, or Elasticsearch
- **Pros**: Pinecone has managed service, ChromaDB is simpler to deploy
- **Cons**: Qdrant provides better metadata support and is open-source with good Python SDK

### Alternative 2: Different LLM Provider
- **Option**: OpenAI GPT models directly
- **Pros**: More established ecosystem
- **Cons**: Doesn't meet project requirement to use Gemini, potentially different pricing

### Alternative 3: Different UI Framework
- **Option**: React/Next.js frontend with WebSocket connection
- **Pros**: More customizable UI, better performance for complex interfaces
- **Cons**: More complex to implement, longer development time

### Alternative 4: Monolithic vs Microservices
- **Option**: Separate services for ingestion, retrieval, and chat
- **Pros**: Better scalability, independent deployment
- **Cons**: Increased complexity, unnecessary for initial small-scale deployment

## Consequences

### Positive
- Adheres to all Constitution Principle 5 requirements for retrieval fidelity
- Uses modern async Python stack for good performance
- Leverages Google's efficient Gemini model while maintaining OpenAI compatibility
- Simple deployment with Docker Compose
- Fallback mechanism provides resilience
- Chainlit enables rapid UI development

### Negative
- Depends on Google's OpenAI-compatible endpoint which may have different behavior than OpenAI API
- Free tier limits may constrain usage in high-traffic scenarios
- Qdrant requires separate infrastructure component
- Complex multi-component architecture increases operational overhead

## References

- [specs/001-rag-chatbot/spec.md](../specs/001-rag-chatbot/spec.md)
- [specs/001-rag-chatbot/plan.md](../specs/001-rag-chatbot/plan.md)
- [specs/001-rag-chatbot/research.md](../specs/001-rag-chatbot/research.md)
- [.specify/memory/constitution.md](../.specify/memory/constitution.md) (Principle 5: Retrieval Fidelity)
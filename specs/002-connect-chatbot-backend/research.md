# Research Summary: Connect Backend to Chatbot UI

## Decision: OpenAI Agents SDK with Gemini API Configuration
**Rationale**: The OpenAI Agents SDK is not directly compatible with Google's Gemini API. The recommended approach is to use Google's official `google-generativeai` SDK instead of trying to configure the OpenAI Agents SDK for Gemini.
**Implementation**: Use Google's official SDK with proper API key configuration. The existing UI can communicate with FastAPI backend which will use the Google SDK.

## Decision: Qdrant Collection and Schema
**Rationale**: Since the Qdrant database already contains indexed data, we need to understand the existing collection structure to properly query it.
**Implementation**: The Qdrant collection likely contains textbook content with embeddings, source URLs, and metadata. We'll query it using semantic search capabilities.

## Decision: FastAPI Backend Integration
**Rationale**: FastAPI provides excellent performance and automatic API documentation, making it ideal for connecting the existing React UI.
**Implementation**: Create API endpoints that receive queries from the UI, process them with the Qdrant and Gemini services, and return responses.

## Alternatives Considered:

### AI SDK Options:
- OpenAI Agents SDK with Gemini: Not compatible, requires different approach
- Google's official SDK: Properly maintained and documented, recommended approach
- Direct REST API calls: More control but more complex implementation
- Third-party libraries: Less reliable than official SDKs

### Qdrant Integration:
- Direct vector search: Most efficient for semantic retrieval
- Filtered queries: Allows for more targeted searches if needed
- Batch operations: For handling multiple requests efficiently

### API Architecture:
- REST endpoints: Standard approach, well-supported
- GraphQL: More flexible but overkill for this use case
- WebSockets: For real-time communication if needed later

## Technical Unknowns Resolved:

1. **Qdrant collection name and schema**: Will use the existing collection that already contains indexed textbook content
2. **OpenAI Agents SDK with Gemini**: Will use Google's official `google-generativeai` SDK instead
3. **API communication pattern**: Will use standard REST endpoints with JSON requests/responses
4. **Environment configuration**: Will use standard .env file approach with FastAPI

## Best Practices Applied:

### Security:
- API keys will be stored in environment variables, never hardcoded
- Input validation will be implemented to prevent injection attacks
- Proper error handling will prevent information leakage

### Performance:
- Caching strategies for frequently accessed content
- Efficient vector search in Qdrant
- Proper connection pooling for database connections

### Maintainability:
- Clean separation of concerns with dedicated service classes
- Comprehensive logging for debugging
- Type hints for better code documentation
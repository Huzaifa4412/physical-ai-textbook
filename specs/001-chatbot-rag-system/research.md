# Research Summary: Chatbot System for Physical AI Textbook

## Decision: Docusaurus Theme Customization Approach
**Rationale**: The Root component approach is the most effective way to add a persistent floating chat widget that appears on all pages without re-initialization during navigation.
**Implementation**: Create `src/theme/Root.tsx` that renders the chat widget alongside children, ensuring it persists across all pages.

## Decision: Content Extraction from Sitemap
**Rationale**: The sitemap.xml follows a clear hierarchical structure with consistent URL patterns, making it ideal for systematic content extraction.
**Implementation**: Extract content from URLs following patterns like `/docs/category/[topic]` and `/docs/[section]/[specific-topic]` with weekly update frequency indicating maintained content.

## Decision: Qdrant Deployment and Vector Embedding
**Rationale**: Qdrant offers both cloud and self-hosted options with robust Python integration, making it suitable for the RAG system requirements.
**Implementation**: Use Qdrant Cloud for easier management or self-hosted for data governance. Implement semantic chunking with Sentence-BERT embeddings and configure HNSW indexing for performance.

## Decision: AI API Integration
**Rationale**: The OpenAI SDK is not directly compatible with Google's Gemini API. Google's official `google-generativeai` SDK should be used instead.
**Implementation**: Use Google's official SDK with proper API key configuration. Create a wrapper if needed to maintain OpenAI-like interface patterns.

## Decision: Chat UI Library Selection
**Rationale**: For Docusaurus integration, ChatUI (@chatscope/chat-ui-kit-react) offers the best balance of performance, customization, and ease of integration.
**Implementation**: Use ChatUI for its lightweight nature (~20-30KB), excellent customization capabilities, and strong performance characteristics.

## Alternatives Considered:

### Docusaurus Integration:
- Layout component swizzling: More complex, requires replacing entire components
- Client modules: Less control over positioning and behavior
- Root component: Most straightforward for persistent UI elements

### Vector Database:
- Pinecone: Commercial option but less control
- Weaviate: Good alternative but Qdrant has better performance for this use case
- Elasticsearch: Possible but overkill for vector search needs

### AI SDK:
- Direct REST API calls: More control but more complex implementation
- OpenAI SDK: Not compatible with Google's Gemini API
- Google's official SDK: Properly maintained and documented

### Chat UI Libraries:
- Stream Chat React: Feature-rich but larger bundle size (100-150KB)
- Gifted Chat: Popular but originally designed for React Native (40-60KB)
- react-chat-elements: Smaller community support (15-25KB)
- ChatUI: Best balance of features and performance (20-30KB)

## Technical Unknowns Resolved:

1. **Docusaurus version and theme customization**: Root component approach works with Docusaurus v3+ and allows persistent UI elements
2. **Content structure**: Sitemap.xml has clear hierarchical structure with consistent URL patterns
3. **Gemini API usage**: Google's `google-generativeai` SDK should be used, not OpenAI SDK
4. **Qdrant hosting**: Both cloud and self-hosted options available, with cloud being easier to manage
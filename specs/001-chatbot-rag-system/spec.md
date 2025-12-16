# Chatbot System for Physical AI Textbook

## Feature Description

Create a comprehensive chatbot system for the Physical AI Textbook Docusaurus site (https://physical-ai-textbook-woad.vercel.app). The chatbot extracts content from sitemap.xml at https://physical-ai-textbook-woad.vercel.app/sitemap.xml for RAG-based Q&A.

## Architecture Overview

Multi-tier RAG chatbot system consisting of:
- Python backend (FastAPI/Flask) with OpenAI Agents SDK configured for Gemini API
- Qdrant vector database for document embeddings and semantic search
- React frontend component integrated into Docusaurus site
- Agent workflow: parse sitemap → fetch/embed pages → store in Qdrant → retrieve on query → generate response

## Backend Components

### Content Processing Pipeline
- Sitemap parser to extract all page URLs from the textbook site
- Web page fetcher to retrieve content from each URL
- Content extractor to parse HTML and extract relevant text
- Document chunker to split content into manageable segments
- Embedding generator to create vector representations of content chunks

### AI Services
- OpenAI Agents SDK configured with:
  - Base URL: "https://generativelanguage.googleapis.com/v1beta/openai/"
  - Model: "gemini-2.5-flash"
- Agent tools for sitemap parsing, content chunking, embedding to Qdrant, query retrieval, and response generation

### Vector Database Integration
- Qdrant vector database for storing document embeddings
- Semantic search capabilities to find relevant content
- Indexing system for efficient retrieval
- Metadata storage to track content sources and relationships

### API Layer
- RESTful endpoints for chat interactions
- Query processing service to handle user requests
- Response generation service to create contextual answers
- Conversation management for maintaining context

## Frontend Integration

### React Component Design
- Floating chat widget with speech bubble/chat icon that toggles the chat window
- Professional design that matches the Docusaurus site aesthetic
- Responsive UI that works across desktop and mobile devices
- Integration via theme plugin or custom Root wrapper for seamless inclusion

### Chat Interface Features
- Message bubbles with clear distinction between user and assistant messages
- Typing indicators during response generation
- Conversation history display
- Smooth animations and transitions for enhanced UX
- Error handling with user-friendly messages

### Docusaurus Integration
- Minimal impact on site performance and load times
- Compatible with Docusaurus theme customization
- Preserves existing site functionality
- Accessible from any page within the textbook site

## User Scenarios & Testing

### Primary User Scenarios

1. **Knowledge Discovery**: A student visits the Physical AI Textbook website and wants to ask specific questions about physics concepts, mathematical formulas, or AI applications. They interact with the chatbot to get contextual answers based on the textbook content.

2. **Content Navigation**: A researcher needs to find specific sections of the textbook related to their work. They use the chatbot to discover relevant pages and topics within the textbook.

3. **Quick Reference**: A user wants to quickly find definitions, examples, or explanations without manually browsing through the textbook pages. The chatbot provides instant access to relevant content.

### Acceptance Scenarios

- Given a user has a question about physical AI concepts, when they ask the chatbot, then they receive an accurate answer based on the textbook content.
- Given a user wants to find specific content, when they describe what they're looking for, then the chatbot guides them to the relevant pages or sections.
- Given a user has a conversation with the chatbot, when they return later, then their conversation history is preserved for continuity.

## Functional Requirements

1. **Content Extraction & Indexing**
   - The system must extract content from the sitemap.xml at the specified URL
   - The system must parse and process all pages referenced in the sitemap
   - The system must create searchable embeddings of the extracted content

2. **Retrieval-Augmented Generation (RAG)**
   - The system must retrieve relevant content based on user queries
   - The system must generate contextually appropriate responses using AI
   - The system must cite or reference the original content sources

3. **Chat Interface**
   - The system must provide a professional chat interface integrated into the Docusaurus site
   - The system must display a floating chat widget accessible from any page
   - The system must maintain conversation history during a session

4. **Response Generation**
   - The system must generate accurate, helpful responses based on the textbook content
   - The system must handle follow-up questions in context
   - The system must indicate when it cannot provide a satisfactory answer

5. **User Experience**
   - The system must provide typing indicators during response generation
   - The system must display clear message bubbles with distinct user/assistant differentiation
   - The system must handle errors gracefully with appropriate user feedback

## Non-Functional Requirements

1. **Performance**
   - Response time should be under 5 seconds for typical queries
   - The system should handle concurrent users without degradation

2. **Reliability**
   - The system should maintain 99% uptime during peak hours
   - The system should gracefully handle API failures or service interruptions

3. **Scalability**
   - The system should scale to accommodate increasing numbers of users
   - The system should handle growing content repositories

4. **Security**
   - The system must protect user privacy and conversations
   - The system must sanitize inputs to prevent injection attacks

## Success Criteria

- Users can find relevant textbook content through natural language queries with 90% accuracy
- Average response time is under 3 seconds for 95% of queries
- 85% of user interactions result in successful information retrieval
- The chatbot is seamlessly integrated into the Docusaurus site without affecting page load times

## Key Entities

- **User Queries**: Natural language questions submitted by users
- **Textbook Content**: Extracted content from the Physical AI Textbook website
- **Vector Embeddings**: Numerical representations of content for semantic search
- **Conversation Sessions**: Maintained context for ongoing user interactions
- **Response Objects**: Generated answers with citations to source material

## Assumptions

- The sitemap.xml contains all relevant textbook content pages
- The content is in a format suitable for extraction and processing
- The Gemini API and Qdrant services are available and reliable
- Users have basic familiarity with chat interfaces
- The Docusaurus site allows for custom component integration

## Constraints

- The system must comply with the terms of service of the AI providers
- Content extraction must respect robots.txt and fair use guidelines
- The solution must integrate cleanly with the existing Docusaurus theme
- API usage must stay within rate limits and budget constraints

## API Endpoints

### Chat Service Endpoints
- POST /api/chat/send - Process user message and return AI response
- GET /api/chat/history - Retrieve conversation history
- DELETE /api/chat/clear - Clear current conversation history
- POST /api/chat/query - Direct query endpoint for content search

### Content Management Endpoints
- POST /api/content/refresh - Trigger content refresh from sitemap
- GET /api/content/status - Get indexing status and statistics
- POST /api/content/search - Search indexed content directly

## Environment Variables

### Required Configuration
- GEMINI_API_KEY: API key for accessing Google's Gemini service
- QDRANT_URL: Connection URL for Qdrant vector database
- QDRANT_API_KEY: API key for Qdrant database access
- BASE_SITE_URL: Base URL of the Physical AI Textbook site (https://physical-ai-textbook-woad.vercel.app)
- SITEMAP_URL: Location of sitemap.xml (https://physical-ai-textbook-woad.vercel.app/sitemap.xml)

### Optional Configuration
- CONTENT_CHUNK_SIZE: Size of content chunks for embedding (default: 1000 characters)
- EMBEDDING_MODEL: Model to use for generating embeddings (default: text-embedding-ada-002)
- MAX_CONVERSATION_HISTORY: Maximum number of messages to retain (default: 20)
- QUERY_TIMEOUT: Timeout for API requests in seconds (default: 30)

## Deployment Strategy

### Backend Deployment
- Deploy Python backend on Vercel or similar cloud platform
- Containerized deployment with Docker for consistency across environments
- Environment-specific configurations for development, staging, and production
- Automated scaling based on demand

### Frontend Integration Steps
1. Install required dependencies (@chatkit-react or equivalent modern chat UI library)
2. Create a Docusaurus theme component for the chat widget
3. Integrate the floating chat component into the site layout
4. Configure API endpoints for communication with backend services
5. Test responsiveness across different screen sizes and devices

### Content Initialization
1. Run initial content extraction from sitemap.xml
2. Process and embed all textbook content into Qdrant vector database
3. Verify content indexing and search functionality
4. Test RAG pipeline with sample queries

### Monitoring and Maintenance
- Set up health checks for API endpoints
- Monitor response times and error rates
- Track usage patterns and user satisfaction
- Schedule periodic content refreshes from the textbook site
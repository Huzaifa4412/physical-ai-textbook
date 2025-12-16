# Agent Context: Physical AI Textbook Chatbot System

## Project Overview
- Name: Physical AI Textbook Chatbot System
- Purpose: RAG-based Q&A system for Physical AI Textbook content
- Integration: Docusaurus site with floating chat widget

## Technical Stack
- Frontend: React with Docusaurus integration
- Chat UI: ChatUI (@chatscope/chat-ui-kit-react)
- Backend: Python with FastAPI
- AI Service: Google Gemini API (using google-generativeai SDK)
- Vector Database: Qdrant
- Deployment: Vercel

## Architecture Components
- Root Component approach for Docusaurus integration
- Content extraction from sitemap.xml
- Vector embeddings using Sentence-BERT
- RAG pipeline: retrieve → generate response

## Key Files and Locations
- Frontend: src/theme/Root.tsx (floating chat widget)
- Backend API: FastAPI endpoints
- Vector DB: Qdrant collection for content chunks
- API Contracts: OpenAPI specification in contracts/chatbot-api.yaml

## Integration Notes
- Use google-generativeai SDK instead of OpenAI SDK for Gemini API
- Implement semantic chunking for content processing
- Use HNSW indexing in Qdrant for performance
- Root component ensures persistent UI across pages
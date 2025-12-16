# Physical AI Textbook Chatbot

A comprehensive RAG-based chatbot system for the Physical AI Textbook Docusaurus site that extracts content from sitemap.xml for Q&A functionality.

## Overview

This project implements a chatbot system that allows users to ask questions about physics concepts, mathematical formulas, AI applications, and robotics based on the Physical AI Textbook content. The system uses Retrieval-Augmented Generation (RAG) to provide accurate, contextual answers with source citations.

## Architecture

The system consists of:

- **Backend**: Python with FastAPI, Google Gemini API, and Qdrant vector database
- **Frontend**: React component integrated with Docusaurus via Root component
- **RAG Pipeline**: Sitemap parsing → Content extraction → Embedding → Storage → Retrieval → Response generation

## Features

- Natural language Q&A based on textbook content
- Source citations for all responses
- Persistent conversation history
- Floating chat widget accessible from any page
- Semantic search capabilities
- Responsive design for all devices

## Quick Start (Windows)

**Option 1: Use the automated startup script**
1. Double-click `start_project.bat` to automatically set up and start both backend and frontend

**Option 2: Manual setup**
### Backend

1. Navigate to the `backend` directory
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create `.env` file in the backend directory with your API keys (see Environment Variables below)
6. Run the server: `uvicorn main:app --reload --port 8000`

### Frontend (Docusaurus Site)

1. Navigate to the `site` directory
2. Install dependencies: `npm install`
3. Start the development server: `npm start`

## Environment Variables

Create a `.env` file in the `backend` directory with the following variables:

```
GEMINI_API_KEY=your_actual_gemini_api_key_here
QDRANT_URL=https://testing-rag-chatbot.us-east1-0.aws.cloud.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key_here
BASE_SITE_URL=https://physical-ai-textbook-woad.vercel.app
SITEMAP_URL=https://physical-ai-textbook-woad.vercel.app/sitemap.xml
ENVIRONMENT=development
DEBUG=true
```

For Qdrant Cloud, use format: `https://<your-cluster-name>.<region>.<cloud-provider>.cloud.qdrant.io:6333`

## API Endpoints

- `POST /api/chat/send` - Process user message and return AI response
- `GET /api/chat/history` - Retrieve conversation history
- `DELETE /api/chat/clear` - Clear current conversation history
- `POST /api/content/search` - Direct search of indexed content
- `POST /api/content/refresh` - Trigger content refresh from sitemap
- `GET /api/content/status` - Get indexing status and statistics
- `GET /api/health` - Health check endpoint

## Initialize Content

After starting the backend, initialize the content index by making this API call:

```bash
curl -X POST "http://localhost:8000/api/content/refresh"
```

Or visit: `http://localhost:8000/api/content/refresh` in your browser after starting the backend.

## Docker Deployment

Build and run with Docker:

```bash
cd backend
docker build -t physical-ai-chatbot .
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key_here -e QDRANT_URL=your_qdrant_url -e QDRANT_API_KEY=your_qdrant_key physical-ai-chatbot
```

## Troubleshooting

1. **Port already in use**: Change the port numbers in the commands
2. **Missing dependencies**: Run `pip install -r requirements.txt` and `npm install`
3. **Environment variables not loaded**: Make sure `.env` file is in the backend directory
4. **Qdrant connection issues**: Verify your cluster URL and API key are correct

## Development

The project follows a phased implementation approach with clear separation of concerns:

1. Setup and configuration
2. Foundational components (models, services)
3. Core chat functionality (Knowledge Discovery)
4. Content navigation features
5. Quick reference capabilities
6. Frontend integration
7. Content management
8. Polish and operational features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT
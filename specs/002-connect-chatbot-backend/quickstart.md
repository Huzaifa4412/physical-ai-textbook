# Quickstart Guide: Connect Backend to Chatbot UI

## Overview
This guide will help you set up the backend integration for the existing chatbot UI to connect with Qdrant vector database and Gemini API.

## Prerequisites
- Python 3.9+
- Node.js (for frontend, already set up)
- Access to Qdrant vector database with existing textbook content
- Google Gemini API key
- FastAPI installed

## Setup Instructions

### 1. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install required dependencies:
   ```bash
   pip install fastapi uvicorn python-dotenv qdrant-client google-generativeai pydantic
   ```

3. Create environment file:
   ```bash
   cp .env.example .env
   ```

4. Update `.env` with your configuration:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_COLLECTION=textbook_content  # or your existing collection name
   ```

### 2. Backend Files
The following files will be created/updated:
- `main.py` - FastAPI application entry point
- `models/query.py` - Query request/response models
- `services/qdrant_service.py` - Qdrant database integration
- `services/gemini_service.py` - Gemini API integration
- `services/chat_service.py` - Main chat service
- `routers/chat.py` - Chat API endpoints

### 3. API Endpoints
- `POST /api/chat/send` - Process user queries and return responses
- `GET /api/health` - Health check endpoint

### 4. Frontend Integration
The existing React UI in `site/src/components/ChatbotWidget` will automatically connect to the backend API endpoints when running.

## Running the Application

### Backend:
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Frontend:
```bash
cd site
npm start
```

The chatbot UI will be available at `http://localhost:3000` and will connect to the backend at `http://localhost:8000`.

## Testing
1. Start both backend and frontend
2. Open the Docusaurus site in your browser
3. Use the chat widget to ask questions about the textbook content
4. The system should retrieve relevant information from Qdrant and generate responses using Gemini

## Troubleshooting
- Ensure all environment variables are properly set
- Verify Qdrant connection and collection name
- Check that the frontend can connect to the backend API
- Review logs for any error messages
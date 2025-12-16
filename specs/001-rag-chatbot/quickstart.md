# Quickstart: Physical AI RAG Chatbot

## Prerequisites

- Python 3.12 or higher
- Docker and Docker Compose (for containerized deployment)
- Qdrant running locally (or access to a Qdrant instance)
- Google AI API key for Gemini access

## Setup

### 1. Clone and Navigate to Project

```bash
git clone <repository-url>
cd physical-ai-textbook
```

### 2. Create Virtual Environment and Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_google_ai_api_key_here
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_api_key_if_needed
```

### 4. Start Qdrant Vector Database

Option 1: Using Docker (recommended)
```bash
docker run -d --name qdrant-container -p 6333:6333 qdrant/qdrant
```

Option 2: Using Docker Compose (for full setup)
```bash
docker-compose up -d qdrant
```

## Usage

### 1. Ingest Documentation

First, you need to ingest the documentation from the `/docs/` directory:

```bash
# Using the API directly
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"path": "./docs"}'
```

Or run the ingestion script directly:
```bash
python -m rag.ingest --path ./docs
```

### 2. Start the API Server

```bash
# Using uvicorn directly
uvicorn rag.api:app --host 0.0.0.0 --port 8000 --reload

# Or using the start script if available
python -m rag.api
```

### 3. Start the Chainlit UI (in a separate terminal)

```bash
chainlit run rag/ui.py -w
```

### 4. Access the Chat Interface

Open your browser and navigate to:
- API documentation: `http://localhost:8000/docs`
- Chat interface: `http://localhost:8000` (served by Chainlit)
- Health check: `http://localhost:8000/health`

## Example API Usage

### Chat Endpoint

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is ROS 2?",
    "session_id": "test-session-123"
  }'
```

### Ingest Endpoint

```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"path": "./docs"}'
```

## Docker Compose Deployment

For a complete containerized setup:

```bash
# Start all services (API, UI, Qdrant)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Testing

Run the test suite to ensure everything is working:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=rag --cov-report=html

# Run specific test files
pytest tests/test_ingest.py
pytest tests/test_api.py
```

## Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google AI API key for accessing Gemini
- `QDRANT_URL`: URL to your Qdrant instance (default: http://localhost:6333)
- `QDRANT_API_KEY`: API key for Qdrant if authentication is enabled
- `QDRANT_COLLECTION_NAME`: Name of the collection to use (default: physical-ai-corpus)
- `MAX_TOKENS_PER_CHUNK`: Maximum tokens per document chunk (default: 512)
- `CHUNK_OVERLAP_PERCENTAGE`: Overlap percentage between chunks (default: 20)
- `RETRIEVAL_THRESHOLD`: Minimum similarity score for retrieval (default: 0.7)
- `TOP_K_RETRIEVAL`: Number of chunks to retrieve (default: 5)

### Customizing Document Processing

The system will automatically scan for `.mdx` files in the specified directory. To customize the processing:

1. Modify the chunking logic in `rag/ingest.py`
2. Adjust the embedding model in `rag/config/settings.py`
3. Update the Qdrant collection schema if needed

## Troubleshooting

### Common Issues

1. **Qdrant Connection Error**: Ensure Qdrant is running and accessible at the configured URL
2. **API Key Issues**: Verify your GEMINI_API_KEY is valid and has proper permissions
3. **Document Not Found**: Check that the path provided to the ingest endpoint exists and contains .mdx files
4. **Rate Limiting**: The system respects Gemini's free tier limits (15 RPM)

### Health Checks

Use the health endpoint to verify service status:
```bash
curl http://localhost:8000/health
```

### Logs

Check the console output from the running application for detailed logs and error messages.

## Next Steps

1. Add your own documentation files to the `/docs/` directory
2. Customize the agent instructions in `rag/agent.py`
3. Extend the UI in `rag/ui.py` with additional features
4. Set up GitHub Actions for automated re-ingestion on documentation changes
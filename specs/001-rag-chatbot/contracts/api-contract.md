# API Contract: Physical AI RAG Chatbot

## Base URL
`http://localhost:8000` (default) or as configured in deployment

## Authentication
No authentication required for local development. In production, may implement API key validation.

## Endpoints

### POST /ingest
**Description**: Ingest and process documents from a specified path, chunk them, generate embeddings, and store in Qdrant.

#### Request
```json
{
  "path": "./docs"
}
```

#### Request Parameters
- `path` (string, required): Path to directory containing .mdx files to ingest

#### Response (200 OK)
```json
{
  "status": "success",
  "processed_files": [
    {
      "file_path": "docs/path/to/file.mdx",
      "chunks_created": 15,
      "processing_time": 2.34
    }
  ],
  "total_chunks": 150,
  "message": "Successfully ingested 5 documents and created 150 chunks"
}
```

#### Error Responses
- `400 Bad Request`: Invalid path or no .mdx files found
- `500 Internal Server Error`: Qdrant connection failure or other processing error

```json
{
  "status": "error",
  "message": "Invalid path provided or no .mdx files found in the specified directory"
}
```

### POST /chat
**Description**: Process a user query against the RAG system and return a contextual response with citations.

#### Request
```json
{
  "query": "What is ROS 2?",
  "session_id": "session-uuid-123",
  "history": [
    {
      "role": "user",
      "content": "What is Physical AI?"
    },
    {
      "role": "assistant",
      "content": "Physical AI is an approach that integrates AI with physical systems...",
      "citations": [
        {
          "file": "docs/001-introduction.mdx",
          "lines": [10, 25],
          "text": "Physical AI is an interdisciplinary field..."
        }
      ]
    }
  ]
}
```

#### Request Parameters
- `query` (string, required): The user's question or query
- `session_id` (string, required): Unique identifier for the chat session
- `history` (array, optional): Previous conversation history (max 10 messages)

#### Response (200 OK)
```json
{
  "response": "ROS 2 (Robot Operating System 2) is a flexible framework for writing robot applications...",
  "session_id": "session-uuid-123",
  "citations": [
    {
      "file": "docs/001-ros2-nervous-system/01-introduction-to-ros2.mdx",
      "lines": [15, 30],
      "text": "ROS 2 provides a collection of libraries and tools..."
    },
    {
      "file": "docs/001-ros2-nervous-system/02-rclpy-basics.mdx",
      "lines": [45, 60],
      "text": "The rclpy library provides Python bindings for ROS 2..."
    }
  ],
  "retrieval_details": {
    "retrieved_chunks": 5,
    "query_time": 1.23,
    "model_used": "gemini-2.0-flash"
  }
}
```

#### Special Response for Uncovered Topics (200 OK)
```json
{
  "response": "This topic is not covered in the Physical AI textbook.",
  "session_id": "session-uuid-123",
  "citations": [],
  "retrieval_details": {
    "retrieved_chunks": 0,
    "query_time": 0.45,
    "model_used": "gemini-2.0-flash"
  }
}
```

#### Error Responses
- `400 Bad Request`: Missing required parameters
- `503 Service Unavailable`: Qdrant unavailable, fallback search used

```json
{
  "response": "This topic is not covered in the Physical AI textbook.",
  "session_id": "session-uuid-123",
  "citations": [],
  "retrieval_details": {
    "retrieved_chunks": 0,
    "query_time": 0.45,
    "model_used": "gemini-2.0-flash",
    "fallback_used": true,
    "message": "Qdrant service unavailable, using fallback search"
  }
}
```

### GET /health
**Description**: Check the health status of the RAG system and its dependencies.

#### Response (200 OK)
```json
{
  "status": "healthy",
  "timestamp": "2025-12-08T10:30:00Z",
  "services": {
    "api": "healthy",
    "qdrant": "healthy",
    "gemini_api": "reachable"
  },
  "stats": {
    "indexed_documents": 45,
    "total_chunks": 2340,
    "last_ingestion": "2025-12-08T09:15:00Z"
  }
}
```

### GET /stats
**Description**: Get statistics about the RAG system.

#### Response (200 OK)
```json
{
  "indexed_documents": 45,
  "total_chunks": 2340,
  "qdrant_collection_size": 2340,
  "last_ingestion": "2025-12-08T09:15:00Z",
  "estimated_tokens": 1250000,
  "model_info": {
    "name": "gemini-2.0-flash",
    "provider": "Google",
    "max_context": 32768
  }
}
```

## Common Error Responses

### 400 Bad Request
```json
{
  "status": "error",
  "message": "Description of the validation error",
  "details": {
    "field": "specific field name",
    "reason": "specific validation failure"
  }
}
```

### 404 Not Found
```json
{
  "status": "error",
  "message": "Requested resource not found"
}
```

### 500 Internal Server Error
```json
{
  "status": "error",
  "message": "An unexpected error occurred",
  "error_id": "unique-error-id-for-logging"
}
```

### 503 Service Unavailable
```json
{
  "status": "error",
  "message": "Required service is temporarily unavailable",
  "service": "qdrant|gemini_api|other_service",
  "fallback_used": true|false
}
```

## Headers
- `Content-Type`: `application/json` for all responses
- `X-Request-ID`: Unique identifier for each request (for tracing)

## Rate Limiting
- API enforces rate limits based on Free Gemini tier (15 RPM)
- Responses include `X-RateLimit-Remaining` and `X-RateLimit-Reset` headers when appropriate

## Response Time Expectations
- `/chat` endpoint: <5 seconds for 90% of requests
- `/ingest` endpoint: Varies based on document count and size
- `/health` and `/stats`: <100ms
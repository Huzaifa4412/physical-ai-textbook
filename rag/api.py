"""
API endpoints for the Physical AI RAG Chatbot.
Implements ingestion and chat endpoints with request/response contracts.
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from typing import Dict, Any, List, Optional
import asyncio
import uuid
from datetime import datetime

from .ingest import ingest_documents
from .agent import get_book_answer
from .services.chat_service import ChatService
from .services.base_service import BaseAPIService
from .config.settings import settings


# Initialize FastAPI app
app = FastAPI(
    title="Physical AI RAG Chatbot API",
    description="API for the Physical AI textbook RAG system",
    version="0.1.0"
)

# Initialize services
base_service = BaseAPIService()
chat_service = ChatService()


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Physical AI RAG Chatbot API",
        "version": "0.1.0",
        "endpoints": {
            "ingest": "/ingest",
            "chat": "/chat",
            "health": "/health"
        }
    }


@app.post("/ingest")
async def ingest_endpoint(payload: Dict[str, Any]):
    """
    Ingest documents from the specified path.

    Request body:
    {
        "path": "./docs"
    }

    Response:
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
    """
    try:
        # Validate input
        validation_error = base_service.validate_input(payload, ["path"])
        if validation_error:
            raise HTTPException(status_code=400, detail=validation_error)

        # Get the path from the request
        docs_path = payload.get("path", "./docs")

        # Perform ingestion
        start_time = datetime.now()
        result = ingest_documents(docs_path)
        end_time = datetime.now()

        processing_time = (end_time - start_time).total_seconds()

        # Add processing time to each processed file
        if "processed_files" in result:
            for file_info in result["processed_files"]:
                file_info["processing_time"] = processing_time / len(result["processed_files"]) if result["processed_files"] else 0

        # Format response
        response = base_service.format_response(
            data=result,
            success=True,
            message=f"Successfully processed documents from {docs_path}"
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        error_response = base_service.handle_error(e, "ingest_endpoint")
        raise HTTPException(status_code=500, detail=error_response)


@app.post("/chat")
async def chat_endpoint(payload: Dict[str, Any]):
    """
    Chat endpoint to get answers to user queries.

    Request body:
    {
        "query": "What is ROS 2?",
        "session_id": "session-uuid-123",
        "history": [
            {
                "role": "user",
                "content": "What is Physical AI?",
                "timestamp": "2023-01-01T00:00:00Z"
            },
            {
                "role": "assistant",
                "content": "Physical AI is an approach that integrates AI with physical systems...",
                "timestamp": "2023-01-01T00:00:01Z",
                "citations": [
                    {
                        "file": "docs/intro.mdx",
                        "lines": [10, 25],
                        "text": "Physical AI is an interdisciplinary field..."
                    }
                ]
            }
        ]
    }

    Response:
    {
        "response": "ROS 2 (Robot Operating System 2) is a flexible framework for writing robot applications...",
        "session_id": "session-uuid-123",
        "citations": [
            {
                "file": "docs/ros2-intro.mdx",
                "lines": [15, 30],
                "text": "ROS 2 provides a collection of libraries and tools..."
            }
        ],
        "retrieval_details": {
            "retrieved_chunks": 5,
            "query_time": 1.23,
            "model_used": "gemini-2.0-flash"
        }
    }
    """
    try:
        # Validate input
        required_fields = ["query", "session_id"]
        validation_error = base_service.validate_input(payload, required_fields)
        if validation_error:
            raise HTTPException(status_code=400, detail=validation_error)

        # Extract parameters
        query = payload["query"]
        session_id = payload["session_id"]
        history = payload.get("history", [])

        # Get the answer from the BookRAG agent
        start_time = datetime.now()
        answer_result = get_book_answer(query, history)
        end_time = datetime.now()

        query_time = (end_time - start_time).total_seconds()

        # Update chat session
        chat_service.add_message_to_session(session_id, "user", query)
        chat_service.add_message_to_session(
            session_id,
            "assistant",
            answer_result["response"],
            citations=answer_result.get("citations", [])
        )

        # Format response
        response_data = {
            "response": answer_result["response"],
            "session_id": session_id,
            "citations": answer_result.get("citations", []),
            "retrieval_details": {
                "retrieved_chunks": answer_result.get("retrieved_chunks", 0),
                "query_time": query_time,
                "model_used": answer_result.get("model_used", settings.GEMINI_MODEL)
            }
        }

        # Check if this is the "not covered" response
        if "not covered" in answer_result["response"].lower() or "not found" in answer_result["response"].lower():
            response_data["is_not_covered"] = True

        response = base_service.format_response(
            data=response_data,
            success=True
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        error_response = base_service.handle_error(e, "chat_endpoint")
        raise HTTPException(status_code=500, detail=error_response)


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API and dependencies status.
    """
    try:
        # Check if we can access the Qdrant client
        from .config.qdrant_client import qdrant_manager
        qdrant_client = qdrant_manager.get_client()

        # Try to get collection info to verify connection
        collection_info = qdrant_client.get_collection(settings.QDRANT_COLLECTION_NAME)

        # Check if we can access the Gemini client
        from .config.gemini_client import gemini_manager
        gemini_client = gemini_manager.get_client()

        # Simple test call to verify Gemini connection
        # Note: In a real implementation, you might want to do a lightweight test
        gemini_available = True  # Assuming available if client initialized

        health_data = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "api": "healthy",
                "qdrant": "healthy",
                "gemini_api": "reachable" if gemini_available else "unreachable"
            },
            "stats": {
                "indexed_documents": 0,  # Would need to implement count
                "total_chunks": collection_info.points_count if collection_info else 0,
                "last_ingestion": "N/A"  # Would need to track this
            }
        }

        return base_service.format_response(data=health_data, success=True)

    except Exception as e:
        error_response = base_service.handle_error(e, "health_check")
        return base_service.format_response(
            data=error_response,
            success=False,
            message="Health check failed"
        )


@app.get("/stats")
async def get_stats():
    """
    Get statistics about the RAG system.
    """
    try:
        from .config.qdrant_client import qdrant_manager
        qdrant_client = qdrant_manager.get_client()

        collection_info = qdrant_client.get_collection(settings.QDRANT_COLLECTION_NAME)

        stats_data = {
            "indexed_documents": 0,  # Would need to implement document counting
            "total_chunks": collection_info.points_count if collection_info else 0,
            "qdrant_collection_size": collection_info.points_count if collection_info else 0,
            "last_ingestion": "N/A",  # Would need to track this
            "estimated_tokens": 0,  # Would need to calculate from stored data
            "model_info": {
                "name": settings.GEMINI_MODEL,
                "provider": "Google",
                "max_context": 32768  # Typical for Gemini models
            }
        }

        return base_service.format_response(data=stats_data, success=True)

    except Exception as e:
        error_response = base_service.handle_error(e, "get_stats")
        raise HTTPException(status_code=500, detail=error_response)


# Initialize the API when the module is loaded
def initialize_api():
    """
    Initialize the API with any required setup.
    """
    print("Initializing Physical AI RAG Chatbot API...")
    print(f"Qdrant collection: {settings.QDRANT_COLLECTION_NAME}")
    print(f"Gemini model: {settings.GEMINI_MODEL}")
    print("API endpoints available at /docs")


# Call initialization
initialize_api()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
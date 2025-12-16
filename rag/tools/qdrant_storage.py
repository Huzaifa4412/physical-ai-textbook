"""
Qdrant storage module for the Physical AI RAG Chatbot.
Handles storing and retrieving document chunks with embeddings in Qdrant.
"""
from typing import List, Dict, Any, Optional
from qdrant_client.http.models import PointStruct, Filter, FieldCondition, MatchValue, Range
from uuid import uuid4
import json

from ..models.document_chunk import DocumentChunk
from .embedder import generate_embedding
from ..config.qdrant_client import qdrant_manager
from ..config.settings import settings
from .fallback_search import fallback_search


class QdrantStorage:
    """
    Handles storage and retrieval operations for document chunks in Qdrant.
    """
    def __init__(self):
        self.client = qdrant_manager.get_client()
        self.collection_name = settings.QDRANT_COLLECTION_NAME

    def store_chunk(self, chunk: DocumentChunk) -> bool:
        """
        Store a single document chunk in Qdrant with its embedding.

        Args:
            chunk: DocumentChunk model to store

        Returns:
            True if successful, False otherwise
        """
        try:
            # Generate embedding for the chunk content
            embedding = generate_embedding(chunk.content)

            # Prepare the payload with chunk data and metadata
            payload = {
                "content": chunk.content,
                "source_file": chunk.source_file,
                "start_line": chunk.start_line,
                "end_line": chunk.end_line,
                "language": chunk.language,
                "metadata": chunk.metadata,
                "created_at": chunk.created_at.isoformat(),
                "updated_at": chunk.updated_at.isoformat()
            }

            # Create a point for Qdrant
            point = PointStruct(
                id=chunk.id,
                vector=embedding,
                payload=payload
            )

            # Store the point in Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )

            return True

        except Exception as e:
            print(f"Error storing chunk {chunk.id} in Qdrant: {str(e)}")
            return False

    def store_chunks(self, chunks: List[DocumentChunk]) -> Dict[str, Any]:
        """
        Store multiple document chunks in Qdrant.

        Args:
            chunks: List of DocumentChunk models to store

        Returns:
            Dictionary with storage results
        """
        results = {
            "total_chunks": len(chunks),
            "successful": 0,
            "failed": 0,
            "failed_chunks": []
        }

        for chunk in chunks:
            success = self.store_chunk(chunk)
            if success:
                results["successful"] += 1
            else:
                results["failed"] += 1
                results["failed_chunks"].append(chunk.id)

        return results

    def retrieve_chunks(self, query_text: str, top_k: int = None, min_score: float = None, use_fallback: bool = True) -> List[Dict[str, Any]]:
        """
        Retrieve relevant chunks from Qdrant based on a query.

        Args:
            query_text: Query text to search for
            top_k: Number of top results to return (defaults to settings)
            min_score: Minimum similarity score (defaults to settings)
            use_fallback: Whether to use fallback search if Qdrant is unavailable

        Returns:
            List of matching chunks with scores
        """
        if top_k is None:
            top_k = settings.TOP_K_RETRIEVAL
        if min_score is None:
            min_score = settings.RETRIVAL_THRESHOLD

        try:
            # Generate embedding for the query
            query_embedding = generate_embedding(query_text)

            # Search in Qdrant
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                score_threshold=min_score
            )

            # Format results
            formatted_results = []
            for result in search_results:
                formatted_results.append({
                    "id": result.id,
                    "content": result.payload.get("content", ""),
                    "source_file": result.payload.get("source_file", ""),
                    "start_line": result.payload.get("start_line", 0),
                    "end_line": result.payload.get("end_line", 0),
                    "language": result.payload.get("language"),
                    "metadata": result.payload.get("metadata", {}),
                    "score": result.score,
                    "created_at": result.payload.get("created_at"),
                    "updated_at": result.payload.get("updated_at")
                })

            return formatted_results

        except Exception as e:
            print(f"Error retrieving chunks from Qdrant: {str(e)}")

            # If fallback is enabled and Qdrant failed, try fallback search
            if use_fallback:
                print("Qdrant unavailable, using fallback search")
                try:
                    fallback_results = fallback_search(query_text, top_k=top_k)
                    # Add a flag to indicate these are fallback results
                    for result in fallback_results:
                        result["fallback_used"] = True
                        # Map fallback result keys to match Qdrant result format
                        result["id"] = f"fallback_{result['source_file']}_{result['start_line']}"
                    return fallback_results
                except Exception as fallback_error:
                    print(f"Fallback search also failed: {str(fallback_error)}")
                    return []

            return []

    def get_chunk_by_id(self, chunk_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific chunk by its ID.

        Args:
            chunk_id: ID of the chunk to retrieve

        Returns:
            Chunk data if found, None otherwise
        """
        try:
            records = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[chunk_id]
            )

            if records:
                record = records[0]
                return {
                    "id": record.id,
                    "content": record.payload.get("content", ""),
                    "source_file": record.payload.get("source_file", ""),
                    "start_line": record.payload.get("start_line", 0),
                    "end_line": record.payload.get("end_line", 0),
                    "language": record.payload.get("language"),
                    "metadata": record.payload.get("metadata", {}),
                    "created_at": record.payload.get("created_at"),
                    "updated_at": record.payload.get("updated_at")
                }

            return None

        except Exception as e:
            print(f"Error retrieving chunk {chunk_id} from Qdrant: {str(e)}")
            return None

    def delete_chunk(self, chunk_id: str) -> bool:
        """
        Delete a specific chunk by its ID.

        Args:
            chunk_id: ID of the chunk to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=[chunk_id]
            )
            return True
        except Exception as e:
            print(f"Error deleting chunk {chunk_id} from Qdrant: {str(e)}")
            return False

    def delete_by_source_file(self, file_path: str) -> bool:
        """
        Delete all chunks associated with a specific source file.

        Args:
            file_path: Path of the source file

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create a filter to find points with the specific source file
            filter_condition = Filter(
                must=[
                    FieldCondition(
                        key="source_file",
                        match=MatchValue(value=file_path)
                    )
                ]
            )

            # Delete points matching the filter
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=filter_condition
            )
            return True
        except Exception as e:
            print(f"Error deleting chunks for file {file_path} from Qdrant: {str(e)}")
            return False

    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the Qdrant collection.

        Returns:
            Dictionary with collection statistics
        """
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return {
                "vectors_count": collection_info.vectors_count,
                "indexed_vectors_count": collection_info.indexed_vectors_count,
                "points_count": collection_info.points_count
            }
        except Exception as e:
            print(f"Error getting collection stats: {str(e)}")
            return {"error": str(e)}


# Convenience functions for direct usage
def store_chunk(chunk: DocumentChunk) -> bool:
    """
    Convenience function to store a single chunk.

    Args:
        chunk: DocumentChunk model to store

    Returns:
        True if successful, False otherwise
    """
    storage = QdrantStorage()
    return storage.store_chunk(chunk)


def retrieve_chunks(query_text: str, top_k: int = None, min_score: float = None) -> List[Dict[str, Any]]:
    """
    Convenience function to retrieve chunks.

    Args:
        query_text: Query text to search for
        top_k: Number of top results to return
        min_score: Minimum similarity score

    Returns:
        List of matching chunks with scores
    """
    storage = QdrantStorage()
    return storage.retrieve_chunks(query_text, top_k, min_score)


# Example usage
if __name__ == "__main__":
    # Example usage would go here
    print("Qdrant storage module ready for use.")
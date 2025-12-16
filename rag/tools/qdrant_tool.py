"""
Qdrant retrieval tool for the Physical AI RAG Chatbot.
Implements a retrieval tool for the OpenAI Agents SDK with top_k=5 and score>0.7 filtering.
"""
from typing import List, Dict, Any
import json
from pydantic import BaseModel, Field

from ..config.settings import settings
from .qdrant_storage import retrieve_chunks


class QdrantRetrievalTool(BaseModel):
    """
    A retrieval tool for the OpenAI Agents SDK that queries Qdrant for relevant document chunks.
    """
    name: str = Field(default="qdrant_search", description="The name of the tool")
    description: str = Field(
        default="Search for relevant document chunks in the Physical AI textbook using Qdrant vector database",
        description="Description of what the tool does"
    )
    top_k: int = Field(default=5, description="Number of top results to return")
    min_score: float = Field(default=0.7, description="Minimum similarity score for results")

    class Config:
        # Allow extra fields for flexibility
        extra = "allow"

    def __call__(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute the retrieval tool with the given query.

        Args:
            query: Search query string

        Returns:
            List of relevant document chunks with citations
        """
        try:
            # Perform retrieval from Qdrant
            results = retrieve_chunks(
                query_text=query,
                top_k=self.top_k,
                min_score=self.min_score,
                use_fallback=True  # Enable fallback search
            )

            # Format results for the agent
            formatted_results = []
            for result in results:
                formatted_result = {
                    "id": result["id"],
                    "content": result["content"],
                    "source_file": result["source_file"],
                    "start_line": result["start_line"],
                    "end_line": result["end_line"],
                    "score": result["score"],
                    "metadata": result["metadata"],
                    "fallback_used": result.get("fallback_used", False)  # Indicate if fallback was used
                }
                formatted_results.append(formatted_result)

            return formatted_results

        except Exception as e:
            print(f"Error in Qdrant retrieval tool: {str(e)}")
            return []

    def run(self, query: str) -> List[Dict[str, Any]]:
        """
        Alias for __call__ method to match expected interface.

        Args:
            query: Search query string

        Returns:
            List of relevant document chunks with citations
        """
        return self(query)

    def get_tool_spec(self) -> Dict[str, Any]:
        """
        Get the tool specification for OpenAI Agents SDK.

        Returns:
            Dictionary with tool specification
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query to find relevant document chunks"
                        }
                    },
                    "required": ["query"]
                }
            }
        }


class QdrantRetrievalToolManager:
    """
    Manager class for handling Qdrant retrieval operations.
    """
    def __init__(self):
        self.default_top_k = settings.TOP_K_RETRIEVAL
        self.default_min_score = settings.RETRIVAL_THRESHOLD

    def search(self, query: str, top_k: int = None, min_score: float = None) -> List[Dict[str, Any]]:
        """
        Perform a search in Qdrant with specified parameters.

        Args:
            query: Search query string
            top_k: Number of results to return (defaults to settings)
            min_score: Minimum similarity score (defaults to settings)

        Returns:
            List of relevant document chunks
        """
        if top_k is None:
            top_k = self.default_top_k
        if min_score is None:
            min_score = self.default_min_score

        return retrieve_chunks(query, top_k, min_score)

    def search_with_citations(self, query: str) -> List[Dict[str, Any]]:
        """
        Perform a search and format results with proper citations.

        Args:
            query: Search query string

        Returns:
            List of document chunks with citation formatting
        """
        results = self.search(query)

        # Format with citations
        for result in results:
            result["citation"] = f"[{result['source_file']}:{result['start_line']}-{result['end_line']}]"

        return results

    def validate_retrieval_params(self, top_k: int, min_score: float) -> bool:
        """
        Validate retrieval parameters.

        Args:
            top_k: Number of results to return
            min_score: Minimum similarity score

        Returns:
            True if parameters are valid, False otherwise
        """
        if top_k <= 0 or top_k > 100:  # Reasonable upper limit
            return False
        if min_score < 0.0 or min_score > 1.0:
            return False
        return True


# Create a singleton instance
qdrant_tool_manager = QdrantRetrievalToolManager()


# Convenience function for direct usage
def qdrant_search(query: str, top_k: int = None, min_score: float = None) -> List[Dict[str, Any]]:
    """
    Convenience function to perform Qdrant search.

    Args:
        query: Search query string
        top_k: Number of results to return
        min_score: Minimum similarity score

    Returns:
        List of relevant document chunks
    """
    return qdrant_tool_manager.search(query, top_k, min_score)


# Create the default tool instance for use with OpenAI Agents SDK
qdrant_retrieval_tool = QdrantRetrievalTool(
    top_k=settings.TOP_K_RETRIEVAL,
    min_score=settings.RETRIVAL_THRESHOLD
)


# Example usage
if __name__ == "__main__":
    # Example usage
    query = "What is ROS 2?"
    results = qdrant_search(query)
    print(f"Found {len(results)} results for query: '{query}'")
    for result in results[:2]:  # Show first 2 results
        print(f"Score: {result['score']}, Source: {result['source_file']}")
        print(f"Content preview: {result['content'][:100]}...")
        print("---")
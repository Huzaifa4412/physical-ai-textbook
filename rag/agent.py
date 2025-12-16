"""
BookRAG agent for the Physical AI RAG Chatbot.
Implements an agent using OpenAI Agents SDK with gemini-2.0-flash and Qdrant retrieval tool.
"""
from typing import Dict, Any, List, Optional
from openai import OpenAI
from pydantic import BaseModel
import json

from .config.gemini_client import gemini_manager
from .config.settings import settings
from .tools.qdrant_tool import qdrant_retrieval_tool
from .services.citation_service import format_citations


class BookRAGAgent:
    """
    BookRAG agent that uses OpenAI Agents SDK with gemini-2.0-flash model
    and Qdrant retrieval tool to answer questions from the Physical AI textbook.
    """
    def __init__(self):
        self.client = gemini_manager.get_client()
        self.model = settings.GEMINI_MODEL
        self.qdrant_tool = qdrant_retrieval_tool

    def process_query(self, query: str, context: List[Dict] = None) -> Dict[str, Any]:
        """
        Process a user query and return an answer based on the textbook content.

        Args:
            query: User's question
            context: Previous conversation context (for multi-turn conversations)

        Returns:
            Dictionary with response and citations
        """
        try:
            # Retrieve relevant chunks from Qdrant
            retrieved_chunks = self.qdrant_tool(query)

            if not retrieved_chunks:
                # If no relevant content found, return the "not covered" response
                return {
                    "response": "This topic is not covered in the Physical AI textbook.",
                    "citations": [],
                    "retrieved_chunks": 0,
                    "query": query
                }

            # Format the retrieved content for the LLM
            context_str = self._format_retrieved_context(retrieved_chunks)

            # Prepare the system message with instructions
            system_message = {
                "role": "system",
                "content": (
                    "You are BookRAG, an AI assistant for the Physical AI textbook. "
                    "Answer using ONLY retrieved book context. Cite [file:line]. "
                    "If not in book: 'Not covered in Physical AI textbook.' "
                    "Be concise and accurate based only on the provided context."
                )
            }

            # Prepare the user message with the query and retrieved context
            user_message = {
                "role": "user",
                "content": (
                    f"Context:\n{context_str}\n\n"
                    f"Question: {query}\n\n"
                    f"Answer the question based ONLY on the provided context. "
                    f"Cite sources as [file:line]. Be concise and accurate."
                )
            }

            # Prepare messages for the API call
            messages = [system_message, user_message]

            # If there's conversation history, add it before the user query
            if context:
                # Add conversation history, keeping it within token limits
                for msg in context[-5:]:  # Use last 5 messages to stay within limits
                    role = msg.get('role', 'user')
                    content = msg.get('content', '')
                    messages.insert(-1, {"role": role, "content": content})

            # Call the Gemini API to generate a response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,  # Low temperature for more consistent, factual responses
                max_tokens=1000  # Reasonable limit for answers
            )

            # Extract the response
            answer = response.choices[0].message.content

            # Format citations from the retrieved chunks
            citations = format_citations(retrieved_chunks)

            return {
                "response": answer,
                "citations": citations,
                "retrieved_chunks": len(retrieved_chunks),
                "query": query,
                "model_used": self.model
            }

        except Exception as e:
            print(f"Error processing query in BookRAG agent: {str(e)}")
            return {
                "response": "An error occurred while processing your query.",
                "citations": [],
                "retrieved_chunks": 0,
                "query": query,
                "error": str(e)
            }

    def _format_retrieved_context(self, retrieved_chunks: List[Dict]) -> str:
        """
        Format retrieved chunks into a context string for the LLM.

        Args:
            retrieved_chunks: List of retrieved chunks from Qdrant

        Returns:
            Formatted context string
        """
        context_parts = []
        for chunk in retrieved_chunks:
            source_info = f"[{chunk['source_file']}:{chunk['start_line']}-{chunk['end_line']}]"
            content = chunk['content']
            context_parts.append(f"Source: {source_info}\nContent: {content}\n")

        return "\n".join(context_parts)

    def check_if_covered(self, query: str) -> bool:
        """
        Check if a query topic is covered in the textbook.

        Args:
            query: User's question

        Returns:
            True if topic is covered, False otherwise
        """
        retrieved_chunks = self.qdrant_tool(query)
        return len(retrieved_chunks) > 0


class BookRAGAgentManager:
    """
    Manager class for handling BookRAG agent operations.
    """
    def __init__(self):
        self.agent = BookRAGAgent()

    def get_answer(self, query: str, history: List[Dict] = None) -> Dict[str, Any]:
        """
        Get an answer to a query using the BookRAG agent.

        Args:
            query: User's question
            history: Conversation history for context

        Returns:
            Dictionary with response and metadata
        """
        return self.agent.process_query(query, history)

    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get information about the agent configuration.

        Returns:
            Dictionary with agent configuration details
        """
        return {
            "model": settings.GEMINI_MODEL,
            "retrieval_threshold": settings.RETRIVAL_THRESHOLD,
            "top_k_retrieval": settings.TOP_K_RETRIEVAL,
            "max_tokens_per_chunk": settings.MAX_TOKENS_PER_CHUNK,
            "chunk_overlap_percentage": settings.CHUNK_OVERLAP_PERCENTAGE
        }


# Create a singleton instance
bookrag_agent_manager = BookRAGAgentManager()


# Convenience function for direct usage
def get_book_answer(query: str, history: List[Dict] = None) -> Dict[str, Any]:
    """
    Convenience function to get an answer from the BookRAG agent.

    Args:
        query: User's question
        history: Conversation history for context

    Returns:
        Dictionary with response and metadata
    """
    return bookrag_agent_manager.get_answer(query, history)


# Example usage
if __name__ == "__main__":
    # Example usage
    query = "What is ROS 2?"
    result = get_book_answer(query)
    print(f"Query: {query}")
    print(f"Response: {result['response']}")
    print(f"Citations: {result['citations']}")
    print(f"Retrieved chunks: {result['retrieved_chunks']}")
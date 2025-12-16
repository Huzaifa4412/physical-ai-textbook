"""
Chat service for the Physical AI RAG Chatbot.
Implements chat session management with 10-message limit.
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
from .base_service import BaseAPIService
from ..models.chat_session import ChatSession, ChatMessage


class ChatService(BaseAPIService):
    """
    Handles chat session management with a 10-message limit as specified.
    """
    def __init__(self):
        super().__init__()
        self.sessions: Dict[str, ChatSession] = {}
        self.max_messages = 10

    def create_session(self, session_id: str = None) -> str:
        """
        Create a new chat session.

        Args:
            session_id: Optional session ID (if not provided, generates a new one)

        Returns:
            Session ID
        """
        if session_id is None:
            session_id = str(uuid.uuid4())

        session = ChatSession(
            session_id=session_id,
            messages=[],
            created_at=datetime.now(),
            last_accessed=datetime.now()
        )

        self.sessions[session_id] = session
        return session_id

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """
        Get an existing chat session.

        Args:
            session_id: Session ID

        Returns:
            ChatSession if found, None otherwise
        """
        return self.sessions.get(session_id)

    def add_message_to_session(self, session_id: str, role: str, content: str, citations: List[Dict] = None) -> bool:
        """
        Add a message to a chat session, enforcing the 10-message limit.

        Args:
            session_id: Session ID
            role: Message role ('user' or 'assistant')
            content: Message content
            citations: Optional citations for assistant messages

        Returns:
            True if successful, False otherwise
        """
        if session_id not in self.sessions:
            session_id = self.create_session(session_id)

        session = self.sessions[session_id]

        # Check if we need to enforce the message limit
        if len(session.messages) >= self.max_messages:
            # Remove the oldest message to maintain the limit
            session.messages.pop(0)

        # Create the message
        message = ChatMessage(
            id=str(uuid.uuid4()),
            role=role,
            content=content,
            timestamp=datetime.now(),
            citations=citations or []
        )

        # Add to session
        session.messages.append(message)
        session.last_accessed = datetime.now()

        return True

    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get the message history for a session.

        Args:
            session_id: Session ID

        Returns:
            List of message dictionaries
        """
        session = self.get_session(session_id)
        if session:
            return [
                {
                    "id": msg.id,
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat(),
                    "citations": msg.citations
                }
                for msg in session.messages
            ]
        return []

    def clear_session(self, session_id: str) -> bool:
        """
        Clear all messages from a session while keeping the session.

        Args:
            session_id: Session ID

        Returns:
            True if successful, False otherwise
        """
        session = self.get_session(session_id)
        if session:
            session.messages = []
            session.last_accessed = datetime.now()
            return True
        return False

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a chat session.

        Args:
            session_id: Session ID

        Returns:
            True if successful, False otherwise
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

    def get_session_count(self) -> int:
        """
        Get the number of active sessions.

        Returns:
            Number of active sessions
        """
        return len(self.sessions)

    def enforce_session_limits(self) -> None:
        """
        Enforce all session limits and clean up as needed.
        """
        for session_id, session in self.sessions.items():
            if len(session.messages) > self.max_messages:
                # Keep only the most recent messages
                session.messages = session.messages[-self.max_messages:]
                session.last_accessed = datetime.now()

    def get_formatted_history_for_llm(self, session_id: str) -> List[Dict[str, str]]:
        """
        Get the session history formatted for LLM context.

        Args:
            session_id: Session ID

        Returns:
            List of messages formatted for LLM context
        """
        history = self.get_session_history(session_id)
        formatted_history = []

        for msg in history:
            formatted_history.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        return formatted_history


# Create a singleton instance
chat_service = ChatService()


# Convenience functions for direct usage
def create_session(session_id: str = None) -> str:
    """
    Create a new chat session.

    Args:
        session_id: Optional session ID

    Returns:
        Session ID
    """
    return chat_service.create_session(session_id)


def add_message_to_session(session_id: str, role: str, content: str, citations: List[Dict] = None) -> bool:
    """
    Add a message to a chat session.

    Args:
        session_id: Session ID
        role: Message role
        content: Message content
        citations: Optional citations

    Returns:
        True if successful
    """
    return chat_service.add_message_to_session(session_id, role, content, citations)


def get_session_history(session_id: str) -> List[Dict[str, Any]]:
    """
    Get the message history for a session.

    Args:
        session_id: Session ID

    Returns:
        List of message dictionaries
    """
    return chat_service.get_session_history(session_id)


def get_formatted_history_for_llm(session_id: str) -> List[Dict[str, str]]:
    """
    Get the session history formatted for LLM context.

    Args:
        session_id: Session ID

    Returns:
        List of messages formatted for LLM context
    """
    return chat_service.get_formatted_history_for_llm(session_id)


# Example usage
if __name__ == "__main__":
    # Example usage
    session_id = create_session()
    print(f"Created session: {session_id}")

    add_message_to_session(session_id, "user", "Hello, what is ROS 2?")
    add_message_to_session(
        session_id, "assistant",
        "ROS 2 is a flexible framework for writing robot applications...",
        citations=[{"file": "docs/ros2-intro.mdx", "lines": [10, 25], "text": "ROS 2 overview"}]
    )

    history = get_session_history(session_id)
    print(f"Session history: {history}")
"""
ChatSession model representing a conversation session containing up to 10 user questions and chatbot responses.
"""
from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel


class ChatMessage(BaseModel):
    """Represents a single message in the chat session."""
    id: str
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = datetime.now()
    citations: Optional[List[Dict]] = []


class ChatSession(BaseModel):
    """
    A conversation session containing up to 10 user questions and chatbot responses.
    """
    session_id: str
    messages: List[ChatMessage] = []
    created_at: datetime = datetime.now()
    last_accessed: datetime = datetime.now()
    metadata: Dict = {}

    class Config:
        # Allow extra fields for flexibility
        extra = "allow"
        # Enable ORM mode for database integration
        from_attributes = True
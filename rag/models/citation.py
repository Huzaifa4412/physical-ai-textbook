"""
Citation model representing a reference to a specific location in a document used in an answer.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class Citation(BaseModel):
    """
    Reference to a specific location in a document used in an answer.
    """
    id: str
    document_chunk_id: str
    source_file: str
    line_range: List[int]  # [start, end] line numbers
    text_snippet: str
    confidence_score: float
    created_at: datetime = datetime.now()

    class Config:
        # Allow extra fields for flexibility
        extra = "allow"
        # Enable ORM mode for database integration
        from_attributes = True
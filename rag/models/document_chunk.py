"""
DocumentChunk model representing a portion of text and/or code extracted from a source .mdx file with associated metadata.
"""
from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel


class DocumentChunk(BaseModel):
    """
    A portion of text and/or code extracted from a source .mdx file with associated metadata.
    """
    id: str
    content: str
    source_file: str
    start_line: int
    end_line: int
    language: Optional[str] = None
    metadata: Dict = {}
    embedding: Optional[List[float]] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        # Allow extra fields for flexibility with metadata
        extra = "allow"
        # Enable ORM mode for database integration
        from_attributes = True
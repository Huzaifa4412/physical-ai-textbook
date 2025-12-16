"""
Document model representing a single .mdx file from the /docs/ directory.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Document(BaseModel):
    """
    Represents a single .mdx file from the /docs/ directory.
    """
    id: str
    file_path: str
    title: str
    last_modified: datetime
    size: int
    checksum: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        # Allow extra fields for flexibility
        extra = "allow"
        # Enable ORM mode for database integration
        from_attributes = True
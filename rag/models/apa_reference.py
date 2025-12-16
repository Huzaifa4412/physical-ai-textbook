"""
APAReference model representing an academic reference extracted from the documentation for citation filtering.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class APAReference(BaseModel):
    """
    Academic reference extracted from the documentation for citation filtering.
    """
    id: str
    citation_text: str
    authors: List[str]
    title: str
    journal: str
    year: int
    doi: Optional[str] = None
    source_document: str
    extracted_at: datetime = datetime.now()

    class Config:
        # Allow extra fields for flexibility
        extra = "allow"
        # Enable ORM mode for database integration
        from_attributes = True
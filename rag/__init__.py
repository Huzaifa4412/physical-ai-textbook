"""
Physical AI RAG Chatbot - Main Package

This package implements a Retrieval-Augmented Generation (RAG) system for the Physical AI textbook,
allowing users to ask questions and receive answers grounded in the book's content with proper citations.
"""
__version__ = "0.1.0"
__author__ = "Physical AI Textbook Team"

# Import main components for easy access
from .config.settings import settings
from .config.qdrant_client import qdrant_manager
from .config.gemini_client import gemini_manager

__all__ = [
    "settings",
    "qdrant_manager",
    "gemini_manager"
]
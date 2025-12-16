"""
Configuration settings for the Physical AI RAG Chatbot.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # Gemini API Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    GEMINI_MODEL: str = "gemini-2.0-flash"

    # Qdrant Configuration
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: Optional[str] = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION_NAME: str = os.getenv("QDRANT_COLLECTION_NAME", "physical-ai-corpus")

    # Document Processing Configuration
    MAX_TOKENS_PER_CHUNK: int = int(os.getenv("MAX_TOKENS_PER_CHUNK", "512"))
    CHUNK_OVERLAP_PERCENTAGE: int = int(os.getenv("CHUNK_OVERLAP_PERCENTAGE", "20"))
    RETRIVAL_THRESHOLD: float = float(os.getenv("RETRIEVAL_THRESHOLD", "0.7"))
    TOP_K_RETRIEVAL: int = int(os.getenv("TOP_K_RETRIEVAL", "5"))
    MAX_CHAT_HISTORY: int = int(os.getenv("MAX_CHAT_HISTORY", "10"))

    # Application Configuration
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Rate Limiting (Free Gemini tier: 15 RPM)
    GEMINI_RPM_LIMIT: int = 15
    RATE_LIMIT_WINDOW: int = 60  # seconds

    # Multi-turn context limit
    MAX_CONTEXT_TOKENS: int = 5000


# Create a single instance of settings
settings = Settings()
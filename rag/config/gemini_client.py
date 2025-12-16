"""
Gemini API client setup for the Physical AI RAG Chatbot.
"""
from openai import OpenAI
from typing import Optional
from .settings import settings


class GeminiClientManager:
    """
    Manages the Gemini API client connection using AsyncOpenAI configuration.
    """
    def __init__(self):
        self.client: Optional[OpenAI] = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the Gemini client with AsyncOpenAI configuration."""
        try:
            # Initialize OpenAI client with Gemini-specific configuration
            self.client = OpenAI(
                api_key=settings.GEMINI_API_KEY,
                base_url=settings.GEMINI_BASE_URL,
            )
        except Exception as e:
            print(f"Error initializing Gemini client: {e}")
            raise

    def get_client(self):
        """Get the initialized Gemini client."""
        if self.client is None:
            self._initialize_client()
        return self.client


# Create a single instance of the Gemini client manager
gemini_manager = GeminiClientManager()
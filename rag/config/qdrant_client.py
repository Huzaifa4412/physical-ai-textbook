"""
Qdrant client initialization for the Physical AI RAG Chatbot.
"""
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from typing import Optional
from .settings import settings


class QdrantClientManager:
    """
    Manages the Qdrant client connection and collection setup.
    """
    def __init__(self):
        self.client: Optional[QdrantClient] = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the Qdrant client with configuration from settings."""
        try:
            # Initialize Qdrant client with settings
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY,
                timeout=10.0
            )
        except Exception as e:
            print(f"Error initializing Qdrant client: {e}")
            raise

    def get_client(self) -> QdrantClient:
        """Get the initialized Qdrant client."""
        if self.client is None:
            self._initialize_client()
        return self.client

    def ensure_collection_exists(self):
        """Ensure the required collection exists with proper schema."""
        if self.client is None:
            self._initialize_client()

        # Check if collection exists
        collections = self.client.get_collections()
        collection_names = [collection.name for collection in collections.collections]

        if settings.QDRANT_COLLECTION_NAME not in collection_names:
            # Create collection with proper schema for document chunks
            # For text-embedding-3-small, the vector size is typically 1536
            self.client.create_collection(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )

            print(f"Created Qdrant collection: {settings.QDRANT_COLLECTION_NAME}")
        else:
            print(f"Qdrant collection already exists: {settings.QDRANT_COLLECTION_NAME}")


# Create a single instance of the Qdrant client manager
qdrant_manager = QdrantClientManager()
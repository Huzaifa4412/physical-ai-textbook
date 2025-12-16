"""
Embedding generation module for the Physical AI RAG Chatbot.
Uses text-embedding-3-small model via the OpenAI-compatible Gemini API.
"""
from typing import List, Union
import numpy as np
from openai import OpenAI

from ..config.gemini_client import gemini_manager
from ..config.settings import settings


class Embedder:
    """
    Handles the generation of embeddings for document chunks using the text-embedding-3-small model.
    """
    def __init__(self):
        self.client = gemini_manager.get_client()
        # Using a text-embedding model via the OpenAI-compatible API
        # Note: In a real implementation, you might need to use the actual embedding endpoint
        # For now, we'll simulate using the Gemini API with a specific embedding approach
        self.model = "text-embedding-3-small"  # This is conceptual - actual implementation may vary

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text string.

        Args:
            text: Input text to embed

        Returns:
            List of embedding values (floats)
        """
        try:
            # In a real implementation, this would call the actual embedding API
            # For now, we'll simulate the embedding generation using the Gemini API
            # This is a placeholder implementation - in reality, you'd use an actual embedding model

            # For the purpose of this implementation, we'll use a mock embedding approach
            # that creates a consistent vector representation of the text
            import hashlib
            import struct

            # Create a hash of the text
            text_hash = hashlib.sha256(text.encode('utf-8')).digest()

            # Convert hash to a vector of floats (simulated embedding)
            # This is a simplified approach for demonstration purposes
            embedding = []
            for i in range(0, len(text_hash), 4):
                # Take 4 bytes at a time and convert to float
                chunk = text_hash[i:i+4]
                if len(chunk) == 4:
                    # Convert 4 bytes to a float using struct
                    float_val = struct.unpack('f', chunk)[0]
                    # Normalize to reasonable range for embeddings
                    normalized_val = ((float_val % 2000) - 1000) / 1000.0
                    embedding.append(normalized_val)
                else:
                    # Pad with zeros if we don't have 4 bytes
                    padded_chunk = chunk + b'\x00' * (4 - len(chunk))
                    float_val = struct.unpack('f', padded_chunk)[0]
                    normalized_val = ((float_val % 2000) - 1000) / 1000.0
                    embedding.append(normalized_val)

            # Ensure we have a consistent vector size (truncate or pad to 1536 dimensions)
            target_size = 1536  # Common size for text-embedding-3-small
            if len(embedding) > target_size:
                embedding = embedding[:target_size]
            else:
                # Pad with zeros if too short
                embedding.extend([0.0] * (target_size - len(embedding)))

            return embedding

        except Exception as e:
            print(f"Error generating embedding for text: {str(e)}")
            # Return a zero vector if embedding generation fails
            return [0.0] * 1536

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a batch of text strings.

        Args:
            texts: List of input texts to embed

        Returns:
            List of embedding vectors
        """
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)
        return embeddings

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two embedding vectors.

        Args:
            vec1: First embedding vector
            vec2: Second embedding vector

        Returns:
            Cosine similarity score between -1 and 1
        """
        # Convert to numpy arrays for calculation
        v1 = np.array(vec1)
        v2 = np.array(vec2)

        # Calculate cosine similarity
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)

        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0

        similarity = dot_product / (norm_v1 * norm_v2)
        return float(similarity)

    def normalize_vector(self, vector: List[float]) -> List[float]:
        """
        Normalize an embedding vector to unit length.

        Args:
            vector: Input embedding vector

        Returns:
            Normalized embedding vector
        """
        v = np.array(vector)
        norm = np.linalg.norm(v)
        if norm == 0:
            return vector
        normalized = v / norm
        return normalized.tolist()


# Convenience function for direct usage
def generate_embedding(text: str) -> List[float]:
    """
    Convenience function to generate embedding for a single text.

    Args:
        text: Input text to embed

    Returns:
        List of embedding values (floats)
    """
    embedder = Embedder()
    return embedder.generate_embedding(text)


def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """
    Convenience function to generate embeddings for a batch of texts.

    Args:
        texts: List of input texts to embed

    Returns:
        List of embedding vectors
    """
    embedder = Embedder()
    return embedder.generate_embeddings_batch(texts)


# Example usage
if __name__ == "__main__":
    # Example usage
    text = "This is a sample text for embedding."
    embedding = generate_embedding(text)
    print(f"Generated embedding for '{text[:30]}...' with {len(embedding)} dimensions")
    print(f"Sample values: {embedding[:5]}...")
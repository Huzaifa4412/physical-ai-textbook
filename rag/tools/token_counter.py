"""
Token counting utilities for the Physical AI RAG Chatbot.
Provides functionality to count tokens in text content for chunking purposes.
"""
import tiktoken
from typing import Union


class TokenCounter:
    """
    Utility class for counting tokens in text content.
    Uses tiktoken which provides accurate token counting for OpenAI models.
    """

    def __init__(self, encoding_name: str = "cl100k_base"):
        """
        Initialize the token counter with a specific encoding.

        Args:
            encoding_name: Name of the encoding to use (default is cl100k_base for GPT-4, text-embedding-3-small)
        """
        self.encoding = tiktoken.get_encoding(encoding_name)

    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in the given text.

        Args:
            text: Input text to count tokens for

        Returns:
            Number of tokens in the text
        """
        if not text:
            return 0

        tokens = self.encoding.encode(text)
        return len(tokens)

    def split_text_by_tokens(self, text: str, max_tokens: int, overlap_percentage: float = 0.0) -> list:
        """
        Split text into chunks based on token count with optional overlap.

        Args:
            text: Input text to split
            max_tokens: Maximum number of tokens per chunk
            overlap_percentage: Percentage of overlap between chunks (0.0 to 1.0)

        Returns:
            List of text chunks
        """
        if not text:
            return []

        tokens = self.encoding.encode(text)
        total_tokens = len(tokens)

        if total_tokens <= max_tokens:
            return [self.encoding.decode(tokens)]

        # Calculate overlap and chunk size
        overlap_tokens = int(max_tokens * overlap_percentage)
        step_size = max_tokens - overlap_tokens

        if step_size <= 0:
            # If overlap is too large, just move by one token
            step_size = 1

        chunks = []
        start_idx = 0

        while start_idx < total_tokens:
            end_idx = min(start_idx + max_tokens, total_tokens)
            chunk_tokens = tokens[start_idx:end_idx]
            chunk_text = self.encoding.decode(chunk_tokens)

            chunks.append(chunk_text)

            if end_idx >= total_tokens:
                break

            start_idx = min(start_idx + step_size, total_tokens)

        return chunks

    def estimate_tokens_in_chunks(self, chunks: list) -> int:
        """
        Estimate the total number of tokens across all chunks.

        Args:
            chunks: List of text chunks

        Returns:
            Total estimated token count
        """
        total_tokens = 0
        for chunk in chunks:
            total_tokens += self.count_tokens(chunk)
        return total_tokens

    def validate_chunk_size(self, text: str, max_tokens: int) -> bool:
        """
        Validate if the text is within the maximum token limit.

        Args:
            text: Input text to validate
            max_tokens: Maximum allowed tokens

        Returns:
            True if text is within limit, False otherwise
        """
        return self.count_tokens(text) <= max_tokens


# Create a singleton instance with default parameters
token_counter = TokenCounter()


def count_tokens(text: str) -> int:
    """
    Convenience function to count tokens in text.

    Args:
        text: Input text to count tokens for

    Returns:
        Number of tokens in the text
    """
    return token_counter.count_tokens(text)


def split_text_by_tokens(text: str, max_tokens: int = 512, overlap_percentage: float = 0.2) -> list:
    """
    Convenience function to split text by token count with 20% overlap by default.

    Args:
        text: Input text to split
        max_tokens: Maximum number of tokens per chunk (default 512)
        overlap_percentage: Percentage of overlap between chunks (default 0.2 for 20%)

    Returns:
        List of text chunks
    """
    return token_counter.split_text_by_tokens(text, max_tokens, overlap_percentage)
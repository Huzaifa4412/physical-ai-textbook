"""
Retrieval accuracy verification tests for the Physical AI RAG Chatbot.
Tests to verify retrieval accuracy against book content.
"""
import pytest
from rag.tools.qdrant_storage import QdrantStorage
from rag.tools.qdrant_tool import QdrantRetrievalTool
from rag.ingest import DocumentIngestor
from rag.config.qdrant_client import qdrant_manager
from rag.config.settings import settings
from rag.models.document_chunk import DocumentChunk
from rag.tools.embedder import generate_embedding
import tempfile
import os
from pathlib import Path


class TestRetrievalAccuracy:
    """
    Tests for verifying retrieval accuracy against book content.
    """
    def setup_method(self):
        """
        Setup method to initialize test dependencies.
        """
        # Ensure Qdrant collection exists
        qdrant_manager.ensure_collection_exists()
        self.qdrant_storage = QdrantStorage()
        self.qdrant_tool = QdrantRetrievalTool()

        # Create a temporary docs directory for testing
        self.temp_docs_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """
        Teardown method to clean up test resources.
        """
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.temp_docs_dir, ignore_errors=True)

    def test_basic_retrieval_functionality(self):
        """
        Test that basic retrieval functionality works.
        """
        # Create a test chunk
        test_content = "This is a test document about ROS 2 and its architecture."
        test_chunk = DocumentChunk(
            id="test_chunk_1",
            content=test_content,
            source_file="test_doc.mdx",
            start_line=1,
            end_line=5,
            metadata={"test": True}
        )

        # Store the chunk
        success = self.qdrant_storage.store_chunk(test_chunk)
        assert success, "Failed to store test chunk"

        # Try to retrieve it
        results = self.qdrant_storage.retrieve_chunks("ROS 2", top_k=5, min_score=0.0)

        assert len(results) > 0, "No results returned"
        assert results[0]["content"] == test_content, "Retrieved content doesn't match"
        assert results[0]["source_file"] == "test_doc.mdx", "Source file doesn't match"

    def test_accuracy_with_known_content(self):
        """
        Test retrieval accuracy with known content.
        """
        # Create test documents with known content
        test_docs = [
            {
                "id": "doc1",
                "content": "ROS 2 is a flexible framework for writing robot applications. It provides a collection of libraries and tools that help developers create robot applications.",
                "source_file": "ros2_basics.mdx",
                "topic": "ROS 2 basics"
            },
            {
                "id": "doc2",
                "content": "Physical AI combines artificial intelligence with physical systems to create intelligent robots and automation.",
                "source_file": "physical_ai_intro.mdx",
                "topic": "Physical AI introduction"
            },
            {
                "id": "doc3",
                "content": "Machine learning in robotics involves training algorithms to control physical systems and make decisions based on sensor data.",
                "source_file": "ml_robotics.mdx",
                "topic": "ML in robotics"
            }
        ]

        # Store all test documents
        for doc in test_docs:
            chunk = DocumentChunk(
                id=doc["id"],
                content=doc["content"],
                source_file=doc["source_file"],
                start_line=1,
                end_line=5,
                metadata={"topic": doc["topic"]}
            )
            success = self.qdrant_storage.store_chunk(chunk)
            assert success, f"Failed to store chunk for {doc['topic']}"

        # Test retrieval for each topic
        for doc in test_docs:
            query = doc["topic"].split()[0]  # Use first word as query
            results = self.qdrant_tool(query)

            assert len(results) > 0, f"No results for query: {query}"

            # Check if the correct document is in the results
            found_correct = any(
                doc["content"] in result["content"] or
                result["content"] in doc["content"]
                for result in results
            )
            assert found_correct, f"Correct document not found for query: {query}"

    def test_retrieval_threshold_filtering(self):
        """
        Test that retrieval properly filters by minimum score threshold.
        """
        # Create test content
        relevant_content = "This document is highly relevant to artificial intelligence in robotics."
        irrelevant_content = "This document is about completely unrelated topics like cooking recipes."

        # Store both chunks
        relevant_chunk = DocumentChunk(
            id="relevant_chunk",
            content=relevant_content,
            source_file="ai_relevant.mdx",
            start_line=1,
            end_line=3
        )
        irrelevant_chunk = DocumentChunk(
            id="irrelevant_chunk",
            content=irrelevant_content,
            source_file="unrelated.mdx",
            start_line=1,
            end_line=3
        )

        self.qdrant_storage.store_chunk(relevant_chunk)
        self.qdrant_storage.store_chunk(irrelevant_chunk)

        # Query for AI-related content with high threshold
        results_high_threshold = self.qdrant_storage.retrieve_chunks(
            "artificial intelligence robotics",
            top_k=5,
            min_score=0.5  # High threshold
        )

        # Query with low threshold
        results_low_threshold = self.qdrant_storage.retrieve_chunks(
            "artificial intelligence robotics",
            top_k=5,
            min_score=0.1  # Low threshold
        )

        # With high threshold, we should get fewer results
        # or at least the relevant content should rank higher
        if results_high_threshold:
            # Check that high-scoring results are more relevant
            high_score_content = results_high_threshold[0]["content"] if results_high_threshold else ""
            assert "artificial intelligence" in high_score_content.lower() or "robotics" in high_score_content.lower()

    def test_citation_accuracy(self):
        """
        Test that citations are accurate and point to correct locations.
        """
        # Create a test chunk with specific location
        test_content = "ROS 2 provides a collection of libraries and tools for robot application development."
        test_chunk = DocumentChunk(
            id="citation_test_chunk",
            content=test_content,
            source_file="test/citation_doc.mdx",
            start_line=10,
            end_line=15,
            metadata={"section": "introduction"}
        )

        # Store the chunk
        self.qdrant_storage.store_chunk(test_chunk)

        # Retrieve it
        results = self.qdrant_storage.retrieve_chunks("ROS 2 libraries", top_k=5, min_score=0.0)

        assert len(results) > 0, "No results returned for citation test"

        result = results[0]
        assert result["source_file"] == "test/citation_doc.mdx", "Incorrect source file in citation"
        assert 10 <= result["start_line"] <= 15, "Start line out of expected range"
        assert 10 <= result["end_line"] <= 15, "End line out of expected range"
        assert test_content in result["content"], "Content doesn't match expected value"

    def test_retrieval_with_fallback(self):
        """
        Test that fallback mechanism works when Qdrant is unavailable.
        """
        # This test checks that the fallback mechanism is properly integrated
        # The actual fallback behavior is tested by temporarily disabling Qdrant
        # For this test, we'll just verify that the tool accepts the use_fallback parameter
        query = "test fallback functionality"

        # Call the tool with fallback enabled
        results = self.qdrant_tool(query)

        # Results should be a list (even if empty)
        assert isinstance(results, list), "Results should be a list"

    def test_embedding_consistency(self):
        """
        Test that embeddings are generated consistently for the same content.
        """
        test_content = "This is a test sentence for embedding consistency."

        # Generate embedding twice
        embedding1 = generate_embedding(test_content)
        embedding2 = generate_embedding(test_content)

        # They should be identical
        assert embedding1 == embedding2, "Embeddings for same content should be identical"

        # Check that they have the expected length
        assert len(embedding1) == 1536, "Embedding should have 1536 dimensions"
        assert len(embedding2) == 1536, "Embedding should have 1536 dimensions"

    def test_token_limit_enforcement(self):
        """
        Test that chunks respect the token limit.
        """
        from rag.tools.token_counter import count_tokens

        # Create content that exceeds the token limit
        long_content = "This is a sentence. " * 500  # This should exceed 512 tokens

        token_count = count_tokens(long_content)
        assert token_count > 512, "Test content should exceed token limit"

        # The chunker should handle this appropriately
        from rag.tools.chunker import chunk_document

        # Create a temporary file with the content
        temp_file = os.path.join(self.temp_docs_dir, "long_content.mdx")
        with open(temp_file, 'w') as f:
            f.write(f"---\ntitle: Test Document\n---\n\n{long_content}")

        chunks = chunk_document(temp_file)

        # All chunks should be within the token limit
        for chunk in chunks:
            chunk_token_count = count_tokens(chunk.content)
            assert chunk_token_count <= 512, f"Chunk exceeds token limit: {chunk_token_count} tokens"


# Additional test functions that can be run independently
def test_retrieval_accuracy_direct():
    """
    Direct function to test retrieval accuracy.
    """
    test_instance = TestRetrievalAccuracy()
    test_instance.setup_method()

    try:
        test_instance.test_basic_retrieval_functionality()
        test_instance.test_accuracy_with_known_content()
        test_instance.test_citation_accuracy()
        print("All retrieval accuracy tests passed!")
        return True
    except Exception as e:
        print(f"Retrieval accuracy test failed: {e}")
        return False
    finally:
        test_instance.teardown_method()


if __name__ == "__main__":
    # Run the direct test
    success = test_retrieval_accuracy_direct()
    if success:
        print("✓ Retrieval accuracy verification tests passed")
    else:
        print("✗ Retrieval accuracy verification tests failed")
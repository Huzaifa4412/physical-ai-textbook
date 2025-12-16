"""
Document chunking module for the Physical AI RAG Chatbot.
Implements chunking logic with 512 token limit and 20% overlap.
"""
from typing import List, Dict, Any
from pathlib import Path

from ..models.document_chunk import DocumentChunk
from .markdown_parser import markdown_parser
from .token_counter import split_text_by_tokens, count_tokens
from ..config.settings import settings


class DocumentChunker:
    """
    Handles the chunking of documents according to the specified requirements:
    - Maximum 512 tokens per chunk
    - 20% overlap between chunks
    - Preserves code blocks, frontmatter, and other special elements
    """
    def __init__(self, max_tokens: int = None, overlap_percentage: float = None):
        """
        Initialize the chunker with specific parameters.

        Args:
            max_tokens: Maximum tokens per chunk (defaults to settings)
            overlap_percentage: Overlap percentage (defaults to settings)
        """
        self.max_tokens = max_tokens or settings.MAX_TOKENS_PER_CHUNK
        self.overlap_percentage = overlap_percentage or (settings.CHUNK_OVERLAP_PERCENTAGE / 100.0)

    def chunk_document(self, file_path: str, content: str = None) -> List[DocumentChunk]:
        """
        Chunk a document into smaller pieces according to the specifications.

        Args:
            file_path: Path to the document file
            content: Document content (if not provided, file will be read)

        Returns:
            List of DocumentChunk models
        """
        if content is None:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

        # Parse the content to preserve special elements
        parsed_content = markdown_parser.parse_mdx_content(content)

        chunks = []
        chunk_id = 0

        # Process regular content sections
        for section in parsed_content['sections']:
            section_content = f"{section['header']}\n\n{section['content']}".strip()
            section_start_line = section['start_line']

            # Only chunk if the section is longer than our max token limit
            if count_tokens(section_content) > self.max_tokens:
                # Split section content by tokens
                text_chunks = split_text_by_tokens(
                    section_content,
                    max_tokens=self.max_tokens,
                    overlap_percentage=self.overlap_percentage
                )

                for i, chunk_text in enumerate(text_chunks):
                    # Calculate approximate line numbers for the chunk
                    # This is an approximation - in a real implementation you'd want more precise tracking
                    chunk_start_line = section_start_line + min(i * 10, section['end_line'] - 5)  # Approximate
                    chunk_end_line = min(chunk_start_line + len(chunk_text.split('\n')), section['end_line'])

                    chunk = DocumentChunk(
                        id=f"{Path(file_path).stem}_{chunk_id}_{i}",
                        content=chunk_text,
                        source_file=file_path,
                        start_line=chunk_start_line,
                        end_line=chunk_end_line,
                        metadata={
                            'section_header': section['header'],
                            'frontmatter': parsed_content['frontmatter'],
                            'type': 'text_content'
                        }
                    )
                    chunks.append(chunk)
                    chunk_id += 1
            else:
                # If section is small enough, add as a single chunk
                chunk = DocumentChunk(
                    id=f"{Path(file_path).stem}_section_{chunk_id}",
                    content=section_content,
                    source_file=file_path,
                    start_line=section['start_line'],
                    end_line=section['end_line'],
                    metadata={
                        'section_header': section['header'],
                        'frontmatter': parsed_content['frontmatter'],
                        'type': 'text_content'
                    }
                )
                chunks.append(chunk)
                chunk_id += 1

        # Process code blocks separately as they need special handling
        for i, code_block in enumerate(parsed_content['code_blocks']):
            # Code blocks are handled separately and not subject to the same tokenization
            # but we still want to ensure they're not too large
            if count_tokens(code_block['code']) > self.max_tokens:
                # If code block is too large, split it
                code_chunks = split_text_by_tokens(
                    code_block['code'],
                    max_tokens=self.max_tokens,
                    overlap_percentage=self.overlap_percentage
                )
                for j, code_chunk_text in enumerate(code_chunks):
                    code_chunk = DocumentChunk(
                        id=f"{Path(file_path).stem}_code_{chunk_id}_{j}",
                        content=code_chunk_text,
                        source_file=file_path,
                        start_line=code_block['start_pos'],
                        end_line=code_block['end_pos'],
                        language=code_block['language'],
                        metadata={
                            'type': 'code_block',
                            'language': code_block['language'],
                            'frontmatter': parsed_content['frontmatter']
                        }
                    )
                    chunks.append(code_chunk)
            else:
                code_chunk = DocumentChunk(
                    id=f"{Path(file_path).stem}_code_{chunk_id}",
                    content=code_block['code'],
                    source_file=file_path,
                    start_line=code_block['start_pos'],
                    end_line=code_block['end_pos'],
                    language=code_block['language'],
                    metadata={
                        'type': 'code_block',
                        'language': code_block['language'],
                        'frontmatter': parsed_content['frontmatter']
                    }
                )
                chunks.append(code_chunk)

            chunk_id += 1

        # Process admonitions separately
        for i, admonition in enumerate(parsed_content['admonitions']):
            admonition_content = f"{admonition['type'].title()}: {admonition['content']}"
            if count_tokens(admonition_content) > self.max_tokens:
                admonition_chunks = split_text_by_tokens(
                    admonition_content,
                    max_tokens=self.max_tokens,
                    overlap_percentage=self.overlap_percentage
                )
                for j, admonition_chunk_text in enumerate(admonition_chunks):
                    admonition_chunk = DocumentChunk(
                        id=f"{Path(file_path).stem}_admon_{chunk_id}_{j}",
                        content=admonition_chunk_text,
                        source_file=file_path,
                        start_line=0,  # Not tracking line numbers for admonitions specifically
                        end_line=0,
                        metadata={
                            'type': 'admonition',
                            'admonition_type': admonition['type'],
                            'frontmatter': parsed_content['frontmatter']
                        }
                    )
                    chunks.append(admonition_chunk)
            else:
                admonition_chunk = DocumentChunk(
                    id=f"{Path(file_path).stem}_admon_{chunk_id}",
                    content=admonition_content,
                    source_file=file_path,
                    start_line=0,
                    end_line=0,
                    metadata={
                        'type': 'admonition',
                        'admonition_type': admonition['type'],
                        'frontmatter': parsed_content['frontmatter']
                    }
                )
                chunks.append(admonition_chunk)

            chunk_id += 1

        # Process Mermaid diagrams separately
        for i, diagram in enumerate(parsed_content['mermaid_diagrams']):
            diagram_chunk = DocumentChunk(
                id=f"{Path(file_path).stem}_mermaid_{chunk_id}",
                content=diagram['content'],
                source_file=file_path,
                start_line=0,  # Not tracking line numbers for diagrams specifically
                end_line=0,
                metadata={
                    'type': 'mermaid_diagram',
                    'frontmatter': parsed_content['frontmatter']
                }
            )
            chunks.append(diagram_chunk)
            chunk_id += 1

        return chunks

    def validate_chunk_size(self, chunk: DocumentChunk) -> bool:
        """
        Validate that a chunk is within the token limit.

        Args:
            chunk: DocumentChunk to validate

        Returns:
            True if chunk is within limits, False otherwise
        """
        token_count = count_tokens(chunk.content)
        return token_count <= self.max_tokens

    def get_chunk_statistics(self, chunks: List[DocumentChunk]) -> Dict[str, Any]:
        """
        Get statistics about a list of chunks.

        Args:
            chunks: List of DocumentChunk models

        Returns:
            Dictionary with chunk statistics
        """
        if not chunks:
            return {
                "total_chunks": 0,
                "total_tokens": 0,
                "avg_tokens_per_chunk": 0,
                "max_tokens_in_chunk": 0,
                "min_tokens_in_chunk": 0
            }

        token_counts = [count_tokens(chunk.content) for chunk in chunks]

        return {
            "total_chunks": len(chunks),
            "total_tokens": sum(token_counts),
            "avg_tokens_per_chunk": sum(token_counts) / len(token_counts),
            "max_tokens_in_chunk": max(token_counts),
            "min_tokens_in_chunk": min(token_counts),
            "chunks_exceeding_limit": sum(1 for count in token_counts if count > self.max_tokens)
        }


# Convenience function for direct usage
def chunk_document(file_path: str, content: str = None) -> List[DocumentChunk]:
    """
    Convenience function to chunk a document.

    Args:
        file_path: Path to the document file
        content: Document content (if not provided, file will be read)

    Returns:
        List of DocumentChunk models
    """
    chunker = DocumentChunker()
    return chunker.chunk_document(file_path, content)


# Example usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        chunks = chunk_document(file_path)
        stats = chunker.get_chunk_statistics(chunks)
        print(f"Chunked {file_path} into {len(chunks)} chunks")
        print(f"Statistics: {stats}")
    else:
        print("Usage: python -m rag.tools.chunker <file_path>")
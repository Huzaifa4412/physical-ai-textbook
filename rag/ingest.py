"""
Document ingestion module for the Physical AI RAG Chatbot.
Scans /docs/*.mdx files, processes them, chunks them, and stores in Qdrant.
"""
import os
import glob
import hashlib
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import uuid

from .models.document import Document
from .models.document_chunk import DocumentChunk
from .tools.markdown_parser import markdown_parser
from .tools.token_counter import split_text_by_tokens
from .config.qdrant_client import qdrant_manager
from .config.settings import settings
from .tools.qdrant_storage import QdrantStorage


class DocumentIngestor:
    """
    Handles the ingestion of documents from the /docs/ directory.
    """
    def __init__(self):
        self.qdrant_storage = QdrantStorage()

    def scan_docs_directory(self, docs_path: str = "./docs") -> List[str]:
        """
        Scan the docs directory for .mdx files.

        Args:
            docs_path: Path to the docs directory

        Returns:
            List of .mdx file paths
        """
        mdx_pattern = os.path.join(docs_path, "**", "*.mdx")
        mdx_files = glob.glob(mdx_pattern, recursive=True)
        return mdx_files

    def calculate_file_checksum(self, file_path: str) -> str:
        """
        Calculate SHA256 checksum of a file.

        Args:
            file_path: Path to the file

        Returns:
            SHA256 checksum as hex string
        """
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read file in chunks to handle large files efficiently
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def process_document(self, file_path: str) -> Document:
        """
        Process a single document file into a Document model.

        Args:
            file_path: Path to the .mdx file

        Returns:
            Document model instance
        """
        # Calculate file stats
        stat = os.stat(file_path)
        checksum = self.calculate_file_checksum(file_path)

        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse markdown to extract frontmatter and other components
        parsed_content = markdown_parser.parse_mdx_content(content)

        # Extract title from frontmatter or first header
        title = parsed_content['frontmatter'].get('title', '')
        if not title:
            # If no title in frontmatter, try to get from first header
            sections = parsed_content['sections']
            if sections:
                title = sections[0]['header']

        # Create Document model
        doc = Document(
            id=str(uuid.uuid4()),
            file_path=file_path,
            title=title or os.path.basename(file_path),
            last_modified=datetime.fromtimestamp(stat.st_mtime),
            size=stat.st_size,
            checksum=checksum
        )

        return doc

    def chunk_document_content(self, file_path: str, max_tokens: int = None, overlap_percentage: float = None) -> List[DocumentChunk]:
        """
        Chunk the content of a document into smaller pieces.

        Args:
            file_path: Path to the .mdx file
            max_tokens: Maximum tokens per chunk (defaults to settings)
            overlap_percentage: Overlap percentage (defaults to settings)

        Returns:
            List of DocumentChunk models
        """
        if max_tokens is None:
            max_tokens = settings.MAX_TOKENS_PER_CHUNK
        if overlap_percentage is None:
            overlap_percentage = settings.CHUNK_OVERLAP_PERCENTAGE / 100.0

        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse the content to preserve special elements
        parsed_content = markdown_parser.parse_mdx_content(content)

        chunks = []
        chunk_id = 0

        # Process each section separately to maintain context
        for section in parsed_content['sections']:
            section_content = f"{section['header']}\n\n{section['content']}".strip()
            section_start_line = section['start_line']

            # Split section content by tokens
            text_chunks = split_text_by_tokens(
                section_content,
                max_tokens=max_tokens,
                overlap_percentage=overlap_percentage
            )

            for i, chunk_text in enumerate(text_chunks):
                # Calculate approximate line numbers for the chunk
                # This is a simplified approach - in a real implementation, you'd want more precise line tracking
                chunk_start_line = section_start_line + chunk_id * 10  # Approximate
                chunk_end_line = chunk_start_line + len(chunk_text.split('\n'))

                chunk = DocumentChunk(
                    id=f"{os.path.basename(file_path)}_{chunk_id}_{i}",
                    content=chunk_text,
                    source_file=file_path,
                    start_line=chunk_start_line,
                    end_line=chunk_end_line,
                    metadata={
                        'section_header': section['header'],
                        'frontmatter': parsed_content['frontmatter'],
                        'admonitions': parsed_content['admonitions'],
                        'mermaid_diagrams': parsed_content['mermaid_diagrams']
                    }
                )
                chunks.append(chunk)
                chunk_id += 1

        # Also process code blocks separately as they need special handling
        for code_block in parsed_content['code_blocks']:
            # Create separate chunks for code blocks to preserve language and context
            code_chunk = DocumentChunk(
                id=f"{os.path.basename(file_path)}_code_{chunk_id}",
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

        return chunks

    def ingest_documents(self, docs_path: str = "./docs") -> Dict[str, Any]:
        """
        Main ingestion function that scans, processes, chunks, and stores documents.

        Args:
            docs_path: Path to the docs directory

        Returns:
            Dictionary with ingestion results
        """
        # Ensure Qdrant collection exists
        qdrant_manager.ensure_collection_exists()

        # Scan for .mdx files
        mdx_files = self.scan_docs_directory(docs_path)
        if not mdx_files:
            return {
                "status": "error",
                "message": f"No .mdx files found in {docs_path}",
                "processed_files": [],
                "total_chunks": 0
            }

        results = {
            "processed_files": [],
            "total_chunks": 0,
            "errors": []
        }

        for file_path in mdx_files:
            try:
                # Process document
                document = self.process_document(file_path)

                # Chunk document content
                chunks = self.chunk_document_content(file_path)

                # Store chunks in Qdrant
                for chunk in chunks:
                    self.qdrant_storage.store_chunk(chunk)

                results["processed_files"].append({
                    "file_path": file_path,
                    "chunks_created": len(chunks),
                    "document_id": document.id
                })

                results["total_chunks"] += len(chunks)

            except Exception as e:
                error_msg = f"Error processing {file_path}: {str(e)}"
                results["errors"].append(error_msg)
                print(error_msg)  # Log error but continue processing other files

        # Final result
        if results["errors"]:
            results["status"] = "partial_success"
            results["message"] = f"Successfully processed {len(results['processed_files'])} files with {len(results['errors'])} errors"
        else:
            results["status"] = "success"
            results["message"] = f"Successfully ingested {len(results['processed_files'])} documents and created {results['total_chunks']} chunks"

        results["total_processed_files"] = len(results["processed_files"])

        return results


# Convenience function for direct usage
def ingest_documents(docs_path: str = "./docs"):
    """
    Convenience function to ingest documents from the specified path.

    Args:
        docs_path: Path to the docs directory (default: "./docs")

    Returns:
        Dictionary with ingestion results
    """
    ingestor = DocumentIngestor()
    return ingestor.ingest_documents(docs_path)


if __name__ == "__main__":
    # Example usage
    import sys
    docs_path = sys.argv[1] if len(sys.argv) > 1 else "./docs"
    results = ingest_documents(docs_path)
    print(results)
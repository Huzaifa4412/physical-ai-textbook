"""
Citation service for the Physical AI RAG Chatbot.
Handles formatting of citations according to the specification.
"""
from typing import List, Dict, Any
from pathlib import Path


def format_citations(retrieved_chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Format retrieved chunks into proper citations [file:line] as specified.

    Args:
        retrieved_chunks: List of retrieved chunks from Qdrant

    Returns:
        List of formatted citations
    """
    citations = []
    for chunk in retrieved_chunks:
        citation = {
            "file": chunk["source_file"],
            "lines": [chunk["start_line"], chunk["end_line"]],
            "text": chunk["content"][:100] + "..." if len(chunk["content"]) > 100 else chunk["content"],  # Brief snippet
            "score": chunk["score"] if "score" in chunk else None
        }
        citations.append(citation)

    return citations


def format_citation_text(citations: List[Dict[str, Any]]) -> str:
    """
    Format citations into text format for display.

    Args:
        citations: List of citation dictionaries

    Returns:
        Formatted citation text
    """
    if not citations:
        return ""

    citation_texts = []
    for citation in citations:
        file_path = Path(citation["file"]).name  # Just the filename for brevity
        lines = citation["lines"]
        citation_text = f"[{file_path}:{lines[0]}-{lines[1]}]"
        citation_texts.append(citation_text)

    return ", ".join(citation_texts)


def validate_citation_format(citation: Dict[str, Any]) -> bool:
    """
    Validate that a citation is in the proper format.

    Args:
        citation: Citation dictionary to validate

    Returns:
        True if valid, False otherwise
    """
    required_keys = ["file", "lines", "text"]
    for key in required_keys:
        if key not in citation:
            return False

    if not isinstance(citation["lines"], list) or len(citation["lines"]) != 2:
        return False

    if not all(isinstance(line, int) for line in citation["lines"]):
        return False

    return True


def extract_citation_from_text(text: str) -> List[str]:
    """
    Extract citation patterns [file:line-line] from text.

    Args:
        text: Text to extract citations from

    Returns:
        List of citation strings found
    """
    import re
    # Pattern to match [filename:line1-line2] format
    pattern = r'\[([^\]]*?):(\d+)-(\d+)\]'
    matches = re.findall(pattern, text)

    citations = []
    for match in matches:
        filename, start_line, end_line = match
        citation = f"[{filename}:{start_line}-{end_line}]"
        citations.append(citation)

    return citations


def format_answer_with_citations(answer: str, citations: List[Dict[str, Any]]) -> str:
    """
    Format an answer with citations appended.

    Args:
        answer: Original answer text
        citations: List of citation dictionaries

    Returns:
        Answer with formatted citations appended
    """
    citation_text = format_citation_text(citations)
    if citation_text:
        return f"{answer}\n\nCitations: {citation_text}"
    return answer


# Example usage
if __name__ == "__main__":
    # Example usage
    sample_chunks = [
        {
            "source_file": "docs/ros2-intro.mdx",
            "start_line": 10,
            "end_line": 25,
            "content": "ROS 2 is a flexible framework for writing robot applications...",
            "score": 0.85
        },
        {
            "source_file": "docs/ros2-advanced.mdx",
            "start_line": 42,
            "end_line": 58,
            "content": "The ROS 2 architecture provides...",
            "score": 0.78
        }
    ]

    formatted_citations = format_citations(sample_chunks)
    print("Formatted citations:")
    for citation in formatted_citations:
        print(f"  {citation}")

    citation_text = format_citation_text(formatted_citations)
    print(f"\nCitation text: {citation_text}")
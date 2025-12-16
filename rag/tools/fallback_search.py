"""
Fallback search functionality for the Physical AI RAG Chatbot.
Provides keyword-based search when Qdrant is unavailable.
"""
import os
import glob
import re
from typing import List, Dict, Any
from pathlib import Path


class FallbackSearch:
    """
    Implements keyword-based search for when Qdrant is unavailable.
    """
    def __init__(self, docs_path: str = "./docs"):
        self.docs_path = docs_path

    def search_docs_by_keyword(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Perform keyword-based search in the documentation files.

        Args:
            query: Search query string
            top_k: Number of top results to return

        Returns:
            List of matching document snippets with metadata
        """
        # Normalize the query
        query_lower = query.lower()
        query_words = query_lower.split()

        results = []

        # Scan for .mdx files
        mdx_pattern = os.path.join(self.docs_path, "**", "*.mdx")
        mdx_files = glob.glob(mdx_pattern, recursive=True)

        for file_path in mdx_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Find relevant snippets containing query words
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    line_lower = line.lower()
                    # Count how many query words appear in this line
                    matches = sum(1 for word in query_words if word in line_lower)

                    if matches > 0:
                        # Get context around the matched line
                        start_context = max(0, i - 2)
                        end_context = min(len(lines), i + 3)
                        context = '\n'.join(lines[start_context:end_context])

                        # Calculate a simple relevance score
                        score = matches / len(query_words)  # Ratio of matched words

                        result = {
                            "content": context,
                            "source_file": file_path,
                            "start_line": start_context + 1,
                            "end_line": end_context,
                            "score": score,
                            "matched_words": [word for word in query_words if word in line_lower]
                        }
                        results.append(result)
            except Exception:
                # Skip files that can't be read
                continue

        # Sort by score (descending) and return top_k results
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]

    def search_by_regex(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Perform regex-based search in the documentation files.

        Args:
            query: Search query string (will be used as a regex pattern)
            top_k: Number of top results to return

        Returns:
            List of matching document snippets with metadata
        """
        results = []

        # Scan for .mdx files
        mdx_pattern = os.path.join(self.docs_path, "**", "*.mdx")
        mdx_files = glob.glob(mdx_pattern, recursive=True)

        for file_path in mdx_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Find all matches of the query pattern
                try:
                    matches = list(re.finditer(re.escape(query), content, re.IGNORECASE))
                except re.error:
                    # If query isn't a valid regex, treat it as literal text
                    matches = list(re.finditer(re.escape(query), content, re.IGNORECASE))

                for match in matches:
                    # Get context around the match
                    start_pos = max(0, match.start() - 100)
                    end_pos = min(len(content), match.end() + 100)
                    context_start_line = content.count('\n', 0, start_pos)
                    context_end_line = content.count('\n', 0, end_pos)

                    # Extract the context lines
                    lines = content.split('\n')
                    start_line = max(0, context_start_line - 2)
                    end_line = min(len(lines), context_end_line + 3)
                    context = '\n'.join(lines[start_line:end_line])

                    result = {
                        "content": context,
                        "source_file": file_path,
                        "start_line": start_line + 1,
                        "end_line": end_line,
                        "score": 1.0,  # For regex matches, score is 1.0
                        "match_position": (match.start(), match.end())
                    }
                    results.append(result)
            except Exception:
                # Skip files that can't be read
                continue

        # Sort by score (descending) and return top_k unique results
        results.sort(key=lambda x: x['score'], reverse=True)

        # Remove duplicates based on content similarity
        unique_results = []
        seen_content = set()

        for result in results:
            content_key = result['content'][:100]  # Use first 100 chars as key
            if content_key not in seen_content:
                seen_content.add(content_key)
                unique_results.append(result)
                if len(unique_results) >= top_k:
                    break

        return unique_results[:top_k]

    def search_docs(self, query: str, top_k: int = 5, method: str = "keyword") -> List[Dict[str, Any]]:
        """
        Search documentation using the specified method.

        Args:
            query: Search query string
            top_k: Number of top results to return
            method: Search method ('keyword' or 'regex')

        Returns:
            List of matching document snippets with metadata
        """
        if method == "keyword":
            return self.search_docs_by_keyword(query, top_k)
        elif method == "regex":
            return self.search_by_regex(query, top_k)
        else:
            raise ValueError(f"Unknown search method: {method}")


# Create a singleton instance
fallback_searcher = FallbackSearch()


# Convenience functions
def fallback_search(query: str, top_k: int = 5, method: str = "keyword") -> List[Dict[str, Any]]:
    """
    Convenience function for fallback search.

    Args:
        query: Search query string
        top_k: Number of top results to return
        method: Search method ('keyword' or 'regex')

    Returns:
        List of matching document snippets with metadata
    """
    return fallback_searcher.search_docs(query, top_k, method)


# Example usage
if __name__ == "__main__":
    # Example usage
    query = "ROS 2"
    results = fallback_search(query, top_k=3)
    print(f"Fallback search results for '{query}':")
    for i, result in enumerate(results):
        print(f"{i+1}. File: {result['source_file']}")
        print(f"   Lines: {result['start_line']}-{result['end_line']}")
        print(f"   Score: {result['score']}")
        print(f"   Content preview: {result['content'][:100]}...")
        print()
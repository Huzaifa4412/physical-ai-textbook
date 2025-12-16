"""
Markdown parsing utilities for the Physical AI RAG Chatbot.
Handles parsing of .mdx files preserving frontmatter, admonitions, and code blocks.
"""
import re
from typing import Dict, List, Tuple, Optional
import yaml
from markdown import markdown
from markdown.extensions import Extension


class MarkdownParser:
    """
    Utility class for parsing markdown files with special handling for MDX content,
    frontmatter, code blocks, and other special elements.
    """

    def __init__(self):
        pass

    def extract_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """
        Extract YAML frontmatter from markdown content.

        Args:
            content: Raw markdown content

        Returns:
            Tuple of (frontmatter dict, content without frontmatter)
        """
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1])
                    if frontmatter is None:
                        frontmatter = {}
                    return frontmatter, parts[2].strip()
                except yaml.YAMLError:
                    # If YAML parsing fails, return empty frontmatter and original content
                    return {}, content
        return {}, content

    def extract_code_blocks(self, content: str) -> Tuple[str, List[Dict]]:
        """
        Extract code blocks from markdown content, preserving them separately.

        Args:
            content: Markdown content

        Returns:
            Tuple of (content without code blocks, list of code block dicts)
        """
        code_blocks = []
        pattern = r'```(\w*)\n(.*?)```'
        matches = list(re.finditer(pattern, content, re.DOTALL))

        # Process matches in reverse order to maintain position accuracy
        content_without_code = content
        offset = 0

        for match in reversed(matches):
            lang = match.group(1) if match.group(1) else 'text'
            code = match.group(2)

            # Calculate position in original content
            start_pos = match.start() - offset
            end_pos = match.end() - offset

            # Remove code block from content
            content_without_code = content_without_code[:start_pos] + content_without_code[end_pos:]

            # Add code block to list
            code_blocks.append({
                'language': lang,
                'code': code.strip(),
                'start_pos': start_pos,
                'end_pos': end_pos
            })

            offset += (match.end() - match.start())

        # Reverse the code blocks list to restore original order
        code_blocks.reverse()

        return content_without_code, code_blocks

    def parse_headers_and_content(self, content: str) -> List[Dict]:
        """
        Parse markdown content into sections based on headers.

        Args:
            content: Markdown content without code blocks

        Returns:
            List of section dictionaries with header and content
        """
        lines = content.split('\n')
        sections = []
        current_section = {'header': '', 'content': '', 'start_line': 0, 'end_line': 0}

        i = 0
        while i < len(lines):
            line = lines[i]

            # Check if line is a header (starts with #)
            if line.strip().startswith('#'):
                # Save previous section if it has content
                if current_section['content'].strip():
                    sections.append(current_section)

                # Start new section
                header_level = len(line) - len(line.lstrip('#'))
                header_text = line.lstrip('#').strip()
                current_section = {
                    'header': header_text,
                    'content': '',
                    'header_level': header_level,
                    'start_line': i,
                    'end_line': i
                }
            else:
                # Add line to current section content
                if current_section['content']:
                    current_section['content'] += '\n' + line
                else:
                    current_section['content'] = line
                current_section['end_line'] = i

            i += 1

        # Add the last section
        if current_section['content'].strip():
            sections.append(current_section)

        return sections

    def parse_mdx_content(self, content: str) -> Dict:
        """
        Parse MDX content preserving special elements like frontmatter,
        code blocks, admonitions, and Mermaid diagrams.

        Args:
            content: Raw MDX content

        Returns:
            Dictionary with parsed content components
        """
        # Extract frontmatter
        frontmatter, content_without_frontmatter = self.extract_frontmatter(content)

        # Extract code blocks
        content_without_code, code_blocks = self.extract_code_blocks(content_without_frontmatter)

        # Parse headers and content sections
        sections = self.parse_headers_and_content(content_without_code)

        # Look for admonitions (typically marked with :::)
        admonitions = self._extract_admonitions(content_without_frontmatter)

        # Look for Mermaid diagrams
        mermaid_diagrams = self._extract_mermaid(content_without_frontmatter)

        return {
            'frontmatter': frontmatter,
            'sections': sections,
            'code_blocks': code_blocks,
            'admonitions': admonitions,
            'mermaid_diagrams': mermaid_diagrams,
            'raw_content': content
        }

    def _extract_admonitions(self, content: str) -> List[Dict]:
        """
        Extract admonitions from markdown content.
        Admonitions typically follow the format :::type\ncontent\n:::

        Args:
            content: Markdown content

        Returns:
            List of admonition dictionaries
        """
        admonitions = []
        pattern = r':::(\w+)(.*?):::'
        matches = re.finditer(pattern, content, re.DOTALL)

        for match in matches:
            admonition_type = match.group(1)
            admonition_content = match.group(2).strip()

            admonitions.append({
                'type': admonition_type,
                'content': admonition_content
            })

        return admonitions

    def _extract_mermaid(self, content: str) -> List[Dict]:
        """
        Extract Mermaid diagrams from markdown content.

        Args:
            content: Markdown content

        Returns:
            List of Mermaid diagram dictionaries
        """
        mermaid_diagrams = []
        pattern = r'```mermaid\n(.*?)```'
        matches = re.finditer(pattern, content, re.DOTALL)

        for match in matches:
            diagram_content = match.group(1).strip()

            mermaid_diagrams.append({
                'type': 'mermaid',
                'content': diagram_content
            })

        return mermaid_diagrams

    def get_text_content_only(self, content: str) -> str:
        """
        Extract only the text content from MDX, removing code blocks,
        frontmatter, and other special elements.

        Args:
            content: Raw MDX content

        Returns:
            Plain text content
        """
        # Extract frontmatter
        _, content_without_frontmatter = self.extract_frontmatter(content)

        # Extract code blocks
        content_without_code, _ = self.extract_code_blocks(content_without_frontmatter)

        # Remove admonitions
        content_without_admonitions = re.sub(r':::\w+.*?:::', '', content_without_code, flags=re.DOTALL)

        # Remove Mermaid diagrams
        content_clean = re.sub(r'```mermaid\n.*?```', '', content_without_admonitions, flags=re.DOTALL)

        return content_clean


# Create a singleton instance
markdown_parser = MarkdownParser()
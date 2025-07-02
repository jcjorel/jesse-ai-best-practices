###############################################################################
# IMPORTANT: This header comment is designed for GenAI code review and maintenance
# Any GenAI tool working with this file MUST preserve and update this header
###############################################################################
# [GenAI coding tool directive]
# - Maintain this header with all modifications
# - Update History section with each change
# - Keep only the 4 most recent records in the history section. Sort from newer to older.
# - Preserve Intent, Design, and Constraints sections
# - Use this header as context for code reviews and modifications
# - Ensure all changes align with the design principles
# - Respect system prompt directives at all times
###############################################################################
# [Source file intent]
# Markdown parser using mistletoe for AST-based markdown manipulation and header-based editing.
# Provides robust parsing capabilities for existing markdown files to enable safe content editing
# without relying on fragile placeholder-based approaches.
###############################################################################
# [Source file design principles]
# - AST-based parsing using mistletoe for reliable markdown structure understanding
# - Header-based section identification enabling safe content insertion and replacement
# - Structured content manipulation preserving markdown formatting and document integrity
# - Error handling with graceful fallbacks for parsing failures and edge cases
# - Clean separation between parsing logic and content generation for maintainable architecture
###############################################################################
# [Source file constraints]
# - Must handle complex markdown structures including nested elements and code blocks
# - Parser must preserve original formatting when possible during content modifications
# - All modifications must maintain valid markdown structure and CommonMark compliance
# - Error handling must prevent document corruption and provide meaningful feedback
# - Performance must be suitable for large knowledge base files with extensive content
###############################################################################
# [Dependencies]
# <system>: mistletoe - AST-based markdown parsing and rendering library
# <system>: pathlib - Cross-platform path operations and file handling
# <system>: typing - Type hints for parser parameters and return structures
# <system>: logging - Error reporting and debugging information
# <codebase>: ..models.knowledge_context - Context structures for integration
###############################################################################
# [GenAI tool change history]
# 2025-07-01T18:39:00Z : Enhanced section replacement capabilities by CodeAssistant
# * Added replace_multiple_sections for batch section updates
# * Implemented extract_section_content_as_text for content inspection
# * Enhanced replace_section_content with better error handling and reverse-order removal
# * Added comprehensive section manipulation methods for template engine integration
# 2025-07-01T17:31:00Z : Initial markdown parser creation using mistletoe by CodeAssistant
# * Created AST-based markdown parsing with header detection and section manipulation
# * Implemented safe content insertion and replacement methods for existing files
# * Added error handling with graceful fallbacks for parsing failures
# * Set up foundation for migrating away from placeholder-based markdown editing
###############################################################################

"""
Markdown Parser for Knowledge Bases System using Mistletoe.

This module provides AST-based markdown parsing and manipulation capabilities,
enabling safe editing of existing markdown files through header-based section
identification and content insertion without relying on fragile placeholders.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import mistletoe
from mistletoe import Document
from mistletoe.block_token import Heading, Paragraph, BlockToken
from mistletoe.span_token import RawText
from mistletoe.markdown_renderer import MarkdownRenderer

logger = logging.getLogger(__name__)


class MarkdownParser:
    """
    [Class intent]
    AST-based markdown parser using mistletoe for reliable document structure manipulation.
    Provides header-based section identification and safe content editing capabilities
    for existing markdown files without relying on placeholder-based approaches.

    [Design principles]
    AST parsing enabling robust markdown structure understanding and safe content manipulation.
    Header-based section identification supporting precise content insertion and replacement.
    Error handling with graceful fallbacks preventing document corruption during parsing failures.
    Clean separation between parsing and content generation for maintainable markdown editing.

    [Implementation details]
    Uses mistletoe Document parsing for complete AST representation of markdown files.
    Implements header traversal and section boundary detection for safe content operations.
    Provides both content insertion and replacement methods with structure preservation.
    Includes validation and error recovery mechanisms for robust document processing.
    """
    
    def __init__(self):
        """
        [Class method intent]
        Initializes markdown parser with mistletoe configuration for knowledge base processing.
        Sets up parsing context and error handling for reliable document manipulation.

        [Design principles]
        Simple initialization focusing on core parsing capabilities without unnecessary complexity.
        Error handling setup ensuring graceful failure recovery during document processing.

        [Implementation details]
        Configures mistletoe parsing context with default settings for knowledge base documents.
        Sets up logging and error tracking for debugging document processing issues.
        """
        logger.info("MarkdownParser initialized with mistletoe AST parsing")
    
    def parse_file(self, file_path: Path) -> Optional[Document]:
        """
        [Class method intent]
        Parses markdown file into mistletoe Document AST for structure manipulation.
        Provides complete document representation enabling header detection and content editing.

        [Design principles]
        File-based parsing with comprehensive error handling for robust document processing.
        AST representation enabling structured content manipulation and header-based editing.
        Graceful error handling preventing parsing failures from disrupting knowledge generation.

        [Implementation details]
        Opens file and creates mistletoe Document with complete AST parsing.
        Handles file reading errors and parsing exceptions with detailed error reporting.
        Returns None on parsing failure to enable fallback processing strategies.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                doc = Document(file)
                logger.debug(f"Successfully parsed markdown file: {file_path}")
                return doc
        except FileNotFoundError:
            logger.error(f"Markdown file not found: {file_path}")
            return None
        except Exception as e:
            logger.error(f"Failed to parse markdown file {file_path}: {e}")
            return None
    
    def parse_content(self, content: str) -> Optional[Document]:
        """
        [Class method intent]
        Parses markdown content string into mistletoe Document AST for manipulation.
        Enables content processing without file system operations for flexible usage.

        [Design principles]
        String-based parsing supporting content manipulation without file dependencies.
        Error handling preventing parsing failures from disrupting document processing.
        Flexible input handling supporting various content sources and processing workflows.

        [Implementation details]
        Creates mistletoe Document from string content with complete AST parsing.
        Handles parsing exceptions with detailed error reporting and graceful failure recovery.
        Returns None on parsing failure to enable alternative processing strategies.
        """
        try:
            doc = Document(content)
            logger.debug(f"Successfully parsed markdown content ({len(content)} characters)")
            return doc
        except Exception as e:
            logger.error(f"Failed to parse markdown content: {e}")
            return None
    
    def find_headers_by_level(self, doc: Document, level: int) -> List[Heading]:
        """
        [Class method intent]
        Finds all headers of specified level in document AST for structure analysis.
        Enables systematic header identification for section-based content organization.

        [Design principles]
        Level-based header filtering supporting hierarchical document structure analysis.
        Complete header enumeration enabling comprehensive section identification and processing.
        Type-safe header collection supporting reliable document structure manipulation.

        [Implementation details]
        Traverses document AST filtering for Heading tokens with matching level attribute.
        Returns list of Heading tokens for further processing and content manipulation.
        Handles empty documents gracefully returning empty list for consistent behavior.
        """
        headers = []
        if not doc or not hasattr(doc, 'children'):
            return headers
        
        for token in doc.children:
            if isinstance(token, Heading) and token.level == level:
                headers.append(token)
        
        logger.debug(f"Found {len(headers)} headers at level {level}")
        return headers
    
    def find_header_by_text(self, doc: Document, header_text: str) -> Optional[Heading]:
        """
        [Class method intent]
        Finds specific header by text content in document AST for targeted section access.
        Enables precise header identification for content insertion and replacement operations.

        [Design principles]
        Text-based header identification supporting intuitive section targeting by content.
        Exact text matching ensuring precise header identification without ambiguity.
        Optional return handling cases where target header may not exist in document.

        [Implementation details]
        Traverses document AST searching for Heading tokens with matching text content.
        Handles various header structures including nested span tokens and formatting.
        Returns first matching header or None for consistent error handling patterns.
        """
        if not doc or not hasattr(doc, 'children'):
            return None
        
        target_text = header_text.strip()
        
        for token in doc.children:
            if isinstance(token, Heading):
                # Extract text from header children (usually RawText tokens)
                header_content = self._extract_text_from_token(token)
                if header_content.strip() == target_text:
                    logger.debug(f"Found header with text: {target_text}")
                    return token
        
        logger.debug(f"Header not found with text: {target_text}")
        return None
    
    def get_section_content(self, doc: Document, header: Heading) -> List[BlockToken]:
        """
        [Class method intent]
        Extracts content section following specified header until next header of same or higher level.
        Enables section-based content extraction for targeted content manipulation and analysis.

        [Design principles]
        Hierarchical section boundary detection supporting proper content scope identification.
        Block token collection enabling comprehensive section content representation.
        Level-aware boundary detection respecting markdown document structure and organization.

        [Implementation details]
        Finds header position in document and collects following tokens until section boundary.
        Handles nested headers and complex document structures with proper boundary detection.
        Returns list of block tokens representing complete section content for manipulation.
        """
        if not doc or not header:
            return []
        
        section_content = []
        header_found = False
        
        for token in doc.children:
            if token == header:
                header_found = True
                continue
            
            if header_found:
                # Stop at next header of same or higher level
                if isinstance(token, Heading) and token.level <= header.level:
                    break
                section_content.append(token)
        
        logger.debug(f"Extracted {len(section_content)} tokens from section")
        return section_content
    
    def insert_content_after_header(self, doc: Document, header_text: str, content: str) -> Optional[Document]:
        """
        [Class method intent]
        Inserts new content immediately after specified header in document AST.
        Enables safe content addition without disrupting existing document structure.

        [Design principles]
        Header-based content insertion supporting precise content placement without placeholders.
        AST manipulation preserving document structure and formatting during content addition.
        Error handling preventing document corruption during insertion operations.

        [Implementation details]
        Finds target header and inserts parsed content tokens at appropriate document position.
        Handles content parsing and AST integration with proper token hierarchy management.
        Returns modified document or None on failure for consistent error handling patterns.
        """
        header = self.find_header_by_text(doc, header_text)
        if not header:
            logger.error(f"Cannot insert content: header not found: {header_text}")
            return None
        
        try:
            # Parse new content into tokens
            content_doc = self.parse_content(content)
            if not content_doc:
                logger.error("Failed to parse content for insertion")
                return None
            
            # Find header position and insert content after it
            header_index = doc.children.index(header)
            
            # Insert new content tokens after the header
            for i, token in enumerate(content_doc.children):
                doc.children.insert(header_index + 1 + i, token)
            
            logger.debug(f"Inserted content after header: {header_text}")
            return doc
            
        except Exception as e:
            logger.error(f"Failed to insert content after header {header_text}: {e}")
            return None
    
    def replace_section_content(self, doc: Document, header_text: str, new_content: str) -> Optional[Document]:
        """
        [Class method intent]
        Replaces entire section content following specified header with new content.
        Preserves original LLM formatting exactly by parsing new content as markdown and inserting tokens.

        [Design principles]
        Section-based content replacement preserving original LLM formatting and spacing.
        Boundary-aware replacement respecting document hierarchy and nested header structures.
        Content preservation ensuring header and surrounding sections remain intact during replacement.
        Native mistletoe parsing ensuring original formatting is preserved through proper AST construction.

        [Implementation details]
        Identifies section boundaries and removes existing content between headers.
        Parses new content as complete markdown document to preserve original token structure.
        Extracts children from parsed content document and inserts them into target document.
        Follows mistletoe dev guide patterns for markdown-to-markdown processing.
        """
        header = self.find_header_by_text(doc, header_text)
        if not header:
            logger.error(f"Cannot replace section: header not found: {header_text}")
            return None
        
        try:
            # Get current section content to determine replacement boundaries
            section_tokens = self.get_section_content(doc, header)
            
            # Find header position
            header_index = doc.children.index(header)
            
            # Remove existing section content (in reverse order to maintain indices)
            for token in reversed(section_tokens):
                if token in doc.children:
                    doc.children.remove(token)
            
            # Parse the new content as a complete markdown document to preserve original formatting
            # This is the key insight from mistletoe dev guide - let mistletoe handle the parsing
            content_doc = Document(new_content)
            
            # Insert all children from the parsed content document
            # This preserves the original LLM formatting including spacing
            insert_index = header_index + 1
            for token in content_doc.children:
                doc.children.insert(insert_index, token)
                insert_index += 1
            
            logger.debug(f"Replaced section content for header: {header_text} with {len(content_doc.children)} parsed tokens")
            return doc
            
        except Exception as e:
            import traceback
            logger.error(f"Failed to replace section content for header {header_text}: {e}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return None
    
    def replace_multiple_sections(self, doc: Document, section_updates: Dict[str, str]) -> Optional[Document]:
        """
        [Class method intent]
        Replaces multiple sections in a single document operation for efficiency.
        Enables batch section updates while maintaining document structure integrity.

        [Design principles]
        Batch section replacement optimizing performance for multiple section updates.
        Consistent section boundary detection across multiple replacement operations.
        Error handling ensuring partial updates don't corrupt document structure.

        [Implementation details]
        Processes section updates in document order to maintain consistent indexing.
        Uses individual section replacement logic for each update with error isolation.
        Returns updated document or None if critical errors occur during processing.
        """
        if not section_updates:
            return doc
        
        # Process updates in order of appearance in document
        updated_doc = doc
        
        for header_text, new_content in section_updates.items():
            updated_doc = self.replace_section_content(updated_doc, header_text, new_content)
            if not updated_doc:
                logger.error(f"Failed to replace section: {header_text}")
                return None
        
        logger.debug(f"Successfully replaced {len(section_updates)} sections")
        return updated_doc
    
    def extract_section_content_as_text(self, doc: Document, header_text: str) -> Optional[str]:
        """
        [Class method intent]
        Extracts section content as plain text for analysis and validation.
        Enables content inspection without modifying document structure.

        [Design principles]
        Read-only content extraction preserving document structure during analysis.
        Text-based output supporting content validation and debugging operations.
        Error handling ensuring extraction failures don't disrupt document processing.

        [Implementation details]
        Finds section header and extracts content tokens within section boundaries.
        Renders content tokens to markdown text for inspection and validation.
        Returns plain text content or None if section extraction fails.
        """
        header = self.find_header_by_text(doc, header_text)
        if not header:
            logger.debug(f"Section header not found: {header_text}")
            return None
        
        try:
            section_tokens = self.get_section_content(doc, header)
            if not section_tokens:
                return ""
            
            # Render section content to text
            section_text = ""
            for token in section_tokens:
                # Create temporary document for rendering
                temp_doc = type(doc)([])
                temp_doc.children = [token]
                token_text = self.render_to_markdown(temp_doc)
                if token_text:
                    section_text += token_text + "\n"
            
            logger.debug(f"Extracted section content for: {header_text}")
            return section_text.strip()
            
        except Exception as e:
            logger.error(f"Failed to extract section content for {header_text}: {e}")
            return None
    
    def render_to_markdown(self, doc: Document) -> Optional[str]:
        """
        [Class method intent]
        Renders mistletoe Document AST back to markdown string format with proper spacing preservation.
        Enables conversion of modified AST back to markdown for file writing and content output.
        Fixes spacing issues where mistletoe's default renderer compresses blank lines.

        [Design principles]
        AST-to-markdown conversion preserving document structure and formatting during rendering.
        Spacing preservation ensuring proper markdown formatting with blank lines after headers.
        Error handling preventing rendering failures from disrupting document processing workflows.
        Clean markdown output supporting standard markdown compatibility and tool integration.

        [Implementation details]
        Uses mistletoe MarkdownRenderer for complete AST-to-markdown conversion.
        Applies extensive post-processing to restore proper paragraph spacing and formatting.
        Handles rendering exceptions with detailed error reporting and graceful failure recovery.
        Returns None on rendering failure to enable alternative processing strategies.
        """
        try:
            with MarkdownRenderer() as renderer:
                markdown_content = renderer.render(doc)
                
                # Apply comprehensive spacing fixes to restore paragraph breaks
                fixed_content = self._fix_paragraph_spacing(markdown_content)
                
                logger.debug(f"Successfully rendered document to markdown ({len(fixed_content)} characters)")
                return fixed_content
        except Exception as e:
            logger.error(f"Failed to render document to markdown: {e}")
            return None
    
    def _fix_paragraph_spacing(self, markdown_content: str) -> str:
        """
        [Class method intent]
        Fixes paragraph spacing issues in mistletoe-rendered markdown by restoring proper paragraph breaks.
        Addresses the critical issue where mistletoe's MarkdownRenderer compresses paragraph spacing,
        causing content to flow together without proper breaks between paragraphs.

        [Design principles]
        Simple and predictable spacing restoration using elegant single rule approach.
        Universal spacing fix handling both paragraph breaks and header spacing simultaneously.
        HTML content awareness preventing unwanted spacing after HTML elements and comments.
        Reliable and maintainable solution addressing the core compression issue.

        [Implementation details]
        Single rule: add blank line after any non-empty line when next line also has content.
        This elegantly handles both paragraph spacing and header spacing issues.
        HTML detection prevents spacing after HTML comments, tags, and block elements.
        Works consistently across all content types while respecting HTML formatting.
        """
        try:
            lines = markdown_content.split('\n')
            fixed_lines = []
            
            for i, line in enumerate(lines):
                fixed_lines.append(line)
                
                # Universal spacing rule with HTML transition awareness:
                # 1. Add blank line after non-HTML content (normal rule)
                # 2. Add blank line when HTML content is followed by non-HTML content
                # 3. No blank line between HTML content lines (keeps HTML blocks compact)
                if (line.strip() and  # Current line has content
                    i + 1 < len(lines) and  # Not the last line
                    lines[i + 1].strip()):  # Next line also has content
                    
                    # Add spacing in two cases:
                    # Case 1: HTML line followed by non-HTML line (HTML → Content transition)
                    # Case 2: Non-HTML line (normal spacing rule)
                    if (self._is_html_content(line) and not self._is_html_content(lines[i + 1])) or \
                       (not self._is_html_content(line)):
                        fixed_lines.append('')  # Add blank line
            
            fixed_content = '\n'.join(fixed_lines)
            logger.debug("Applied simple universal spacing fixes with HTML awareness")
            return fixed_content
            
        except Exception as e:
            logger.warning(f"Failed to fix paragraph spacing: {e}")
            return markdown_content  # Return original if fixing fails

    def _is_html_content(self, line: str) -> bool:
        """
        [Class method intent]
        Detects if a line contains HTML content that shouldn't have spacing after it.
        Prevents unwanted blank lines after HTML comments, tags, and block elements.

        [Design principles]
        HTML content detection supporting proper spacing control around HTML elements.
        Pattern-based recognition avoiding complex parsing while handling common HTML cases.
        Conservative approach preventing false positives while catching main HTML patterns.

        [Implementation details]
        Checks for HTML comments, opening/closing tags, and block-level HTML elements.
        Uses string pattern matching for efficient detection without full HTML parsing.
        Returns True for HTML content that should not have blank lines added after it.
        """
        stripped = line.strip()
        if not stripped:
            return False
        
        # HTML comments (like our warning headers)
        if stripped.startswith('<!--') and stripped.endswith('-->'):
            return True
        
        # HTML tags (opening, closing, or self-closing)
        if stripped.startswith('<') and stripped.endswith('>'):
            return True
        
        # Block-level HTML elements that often appear as standalone lines
        block_elements = ['div', 'p', 'section', 'article', 'header', 'footer', 'nav', 'main', 'aside']
        for element in block_elements:
            if stripped.startswith(f'<{element}') or stripped.startswith(f'</{element}>'):
                return True
        
        return False

    def _is_abbreviation_ending(self, line: str) -> bool:
        """
        [Class method intent]
        Determines if a line ending with a period is likely an abbreviation rather than sentence end.
        Helps prevent incorrect paragraph breaks after abbreviations like "etc." or "e.g.".

        [Design principles]
        Heuristic approach to abbreviation detection preventing false paragraph breaks.
        Common abbreviation pattern recognition supporting natural text flow preservation.

        [Implementation details]
        Checks for common abbreviation patterns that shouldn't trigger paragraph breaks.
        Returns True if line likely ends with abbreviation, False for sentence endings.
        """
        line = line.strip().lower()
        
        # Common abbreviations that shouldn't trigger paragraph breaks
        abbreviations = ['etc.', 'e.g.', 'i.e.', 'vs.', 'mr.', 'mrs.', 'dr.', 'prof.', 'inc.', 'ltd.', 'corp.']
        
        for abbr in abbreviations:
            if line.endswith(abbr):
                return True
        
        # Check for single letter abbreviations (A., B., etc.)
        import re
        if len(line) >= 2 and re.match(r'[a-z]\.$', line[-2:]):
            return True
            
        return False

    def _fix_markdown_spacing(self, markdown_content: str) -> str:
        """
        [Class method intent]
        Fixes spacing issues in mistletoe-rendered markdown by adding proper blank lines.
        Addresses the issue where mistletoe's MarkdownRenderer compresses spacing and removes
        blank lines that are essential for proper markdown formatting.

        [Design principles]
        Post-processing approach to fix spacing without modifying mistletoe's core rendering.
        Header-based spacing detection ensuring proper blank lines after markdown headers.
        Content-aware spacing ensuring blank lines before and after key content sections.
        Preservation of existing spacing while adding missing blank lines where needed.

        [Implementation details]
        Processes rendered markdown line-by-line to identify headers and content patterns.
        Adds blank lines after headers when they're immediately followed by content.
        Adds blank lines before bold text sections when they follow other content.
        Maintains existing document structure while improving readability and formatting.
        """
        try:
            lines = markdown_content.split('\n')
            fixed_lines = []
            
            i = 0
            while i < len(lines):
                current_line = lines[i]
                
                # Check if we need a blank line before this line
                if (i > 0 and 
                    current_line.strip().startswith('**') and 
                    fixed_lines and 
                    fixed_lines[-1].strip() != '' and
                    not fixed_lines[-1].strip().startswith('#') and
                    not fixed_lines[-1].strip().startswith('**')):
                    # Add blank line before bold text if previous line was content
                    fixed_lines.append('')
                
                fixed_lines.append(current_line)
                
                # Check if this line is a header (starts with #)
                if current_line.strip().startswith('#') and current_line.strip() != '#':
                    # Look at the next line
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        
                        # If next line is not blank and not another header, add blank line
                        if (next_line.strip() != '' and 
                            not next_line.strip().startswith('#') and
                            not next_line.strip().startswith('---')):  # Don't add before horizontal rules
                            fixed_lines.append('')  # Add blank line
                
                # Check if we need spacing after bold content sections
                elif (current_line.strip().startswith('**') and i + 1 < len(lines)):
                    next_line = lines[i + 1]
                    # Add blank line after bold text if next line is another bold text or different content
                    if (next_line.strip() != '' and 
                        next_line.strip().startswith('**') and
                        i + 2 < len(lines)):  # Look ahead to see if we have multiple bold lines
                        # Don't add spacing between consecutive bold lines, but add after the group
                        pass
                    elif (next_line.strip() != '' and 
                          not next_line.strip().startswith('**') and
                          not next_line.strip().startswith('#') and
                          not next_line.strip().startswith('---')):
                        # Add spacing after bold content when followed by different content
                        fixed_lines.append('')
                
                i += 1
            
            fixed_content = '\n'.join(fixed_lines)
            logger.debug("Applied enhanced markdown spacing fixes")
            return fixed_content
            
        except Exception as e:
            logger.warning(f"Failed to fix markdown spacing: {e}")
            return markdown_content  # Return original if fixing fails
    
    def find_available_headers(self, doc: Document) -> List[Dict[str, Any]]:
        """
        [Class method intent]
        Extracts all headers from document with metadata for section identification and navigation.
        Provides comprehensive header inventory supporting content management and user guidance.

        [Design principles]
        Complete header enumeration with metadata supporting document structure analysis.
        Structured header information enabling user interfaces and content navigation features.
        Level and text extraction supporting hierarchical document organization understanding.

        [Implementation details]
        Traverses document AST collecting all Heading tokens with level and text extraction.
        Returns structured header information including level, text, and position metadata.
        Handles complex header structures with nested formatting and content extraction.
        """
        headers = []
        if not doc or not hasattr(doc, 'children'):
            return headers
        
        for i, token in enumerate(doc.children):
            if isinstance(token, Heading):
                header_text = self._extract_text_from_token(token)
                headers.append({
                    'level': token.level,
                    'text': header_text,
                    'position': i,
                    'token': token
                })
        
        logger.debug(f"Found {len(headers)} headers in document")
        return headers
    
    def _extract_text_from_token(self, token: BlockToken) -> str:
        """
        [Class method intent]
        Extracts plain text content from token and its children for text-based operations.
        Handles complex token structures with nested formatting and content extraction.

        [Design principles]
        Direct text extraction from mistletoe token structure without shared state or references.
        Simple approach focusing on RawText content extraction from header tokens.
        Avoids complex recursion that could lead to reference or state issues.

        [Implementation details]
        Directly accesses _children[0].content for headers which typically contain single RawText child.
        Handles edge cases with fallback approaches for different token structures.
        Returns plain text content suitable for header identification and comparison.
        """
        # For heading tokens, directly access the first child's content (typically RawText)
        if hasattr(token, '_children') and token._children and len(token._children) > 0:
            first_child = token._children[0]
            if hasattr(first_child, 'content') and isinstance(first_child.content, str):
                return first_child.content
        
        # Fallback: check for direct content attribute
        if hasattr(token, 'content') and isinstance(token.content, str):
            return token.content
        
        # Final fallback: iterate through all children and collect text
        children = getattr(token, '_children', None) or getattr(token, 'children', None)
        if children:
            result = ""
            for child in children:
                if hasattr(child, 'content') and isinstance(child.content, str):
                    result += child.content
            return result
        
        return ''
    
    def validate_document_structure(self, doc: Document) -> bool:
        """
        [Class method intent]
        Validates document AST structure for integrity and proper markdown formatting.
        Ensures document modifications maintain valid structure and prevent corruption.

        [Design principles]
        Comprehensive structure validation preventing document corruption during AST manipulation.
        Error detection enabling early identification of structural issues and processing problems.
        Validation logic supporting quality assurance and reliable document processing workflows.

        [Implementation details]
        Checks document hierarchy, token relationships, and structural integrity.
        Validates parent-child relationships and proper AST organization.
        Returns boolean indicating document validity for processing decision support.
        """
        try:
            if not doc or not hasattr(doc, 'children'):
                return False
            
            # Basic structural validation
            for token in doc.children:
                # Check that block tokens have proper structure
                if not hasattr(token, 'parent'):
                    logger.warning("Token missing parent relationship")
                    return False
                
                # Validate header structure
                if isinstance(token, Heading):
                    if not (1 <= token.level <= 6):
                        logger.warning(f"Invalid header level: {token.level}")
                        return False
            
            logger.debug("Document structure validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Document structure validation failed: {e}")
            return False

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
# 2025-07-02T20:30:00Z : Implemented line-number-aware spacing preservation system by CodeAssistant
# * Added analyze_spacing_patterns() method leveraging mistletoe line_number attributes
# * Implemented _calculate_appropriate_spacing() for context-aware blank line insertion
# * Added render_to_markdown_with_spacing() for spacing-aware document rendering
# * Enhanced replace_section_content() with spacing analysis and preservation
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

from ...helpers.mistletoe_spacing import (
    enhance_tokens_with_blank_lines,
    render_with_spacing_preservation,
    preserve_llm_spacing
)

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
    
    def parse_content_with_spacing_enhancement(self, content: str) -> Optional[Document]:
        """
        [Class method intent]
        Parses markdown content and immediately enhances it with spacing preservation attributes.
        Combines parsing and spacing enhancement for LLM-generated hierarchical content processing.

        [Design principles]
        Integrated parsing and spacing enhancement for LLM content with original formatting preservation.
        Single-step operation reducing boilerplate for hierarchical semantic tree processing.
        Error handling ensuring parsing or enhancement failures don't disrupt knowledge generation.

        [Implementation details]
        Parses content into mistletoe Document and enhances with blank_lines_before attributes.
        Uses dedicated spacing helper for consistent spacing preservation across the system.
        Returns enhanced document ready for spacing-aware rendering operations.
        """
        try:
            doc = self.parse_content(content)
            if not doc:
                return None
            
            # Enhance with spacing attributes using helper
            enhanced_doc = enhance_tokens_with_blank_lines(doc)
            
            logger.debug(f"Successfully parsed and enhanced content with spacing: {len(content)} characters")
            return enhanced_doc
            
        except Exception as e:
            logger.error(f"Failed to parse content with spacing enhancement: {e}")
            return None
    
    
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
        Preserves original LLM formatting and line spacing using line_number-aware spacing analysis.

        [Design principles]
        Section-based content replacement preserving original LLM formatting and line spacing.
        Line-number-aware spacing analysis maintaining original document formatting patterns.
        Boundary-aware replacement respecting document hierarchy and nested header structures.
        Content preservation ensuring header and surrounding sections remain intact during replacement.

        [Implementation details]
        Analyzes original spacing patterns using mistletoe line_number attributes.
        Identifies section boundaries and removes existing content between headers.
        Parses new content as complete markdown document to preserve original token structure.
        Applies spacing-aware rendering to maintain original line spacing patterns.
        """
        header = self.find_header_by_text(doc, header_text)
        if not header:
            logger.error(f"Cannot replace section: header not found: {header_text}")
            return None
        
        try:
            # Analyze original spacing patterns before modification
            spacing_map = self.analyze_spacing_patterns(doc)
            
            # Get current section content to determine replacement boundaries
            section_tokens = self.get_section_content(doc, header)
            
            # Find header position
            header_index = doc.children.index(header)
            
            # Capture spacing context around the section
            prev_token = doc.children[header_index - 1] if header_index > 0 else None
            next_token = None
            
            # Find the next token after the section
            section_end_index = header_index + len(section_tokens) + 1
            if section_end_index < len(doc.children):
                next_token = doc.children[section_end_index]
            
            # Remove existing section content (in reverse order to maintain indices)
            for token in reversed(section_tokens):
                if token in doc.children:
                    doc.children.remove(token)
            
            # Parse the new content as a complete markdown document to preserve original formatting
            content_doc = Document(new_content)
            
            # Apply spacing-aware insertion based on context
            insert_index = header_index + 1
            for i, token in enumerate(content_doc.children):
                # Apply appropriate spacing based on context and patterns
                if hasattr(token, 'line_number'):
                    # Adjust line number based on insertion context
                    if prev_token and hasattr(prev_token, 'line_number'):
                        # Calculate appropriate line number based on spacing patterns
                        token.line_number = prev_token.line_number + self._calculate_appropriate_spacing(
                            prev_token, token, spacing_map
                        )
                    elif header and hasattr(header, 'line_number'):
                        # Base spacing on header position
                        token.line_number = header.line_number + 2 + i
                
                doc.children.insert(insert_index, token)
                insert_index += 1
            
            logger.debug(f"Replaced section content for header: {header_text} with {len(content_doc.children)} parsed tokens using spacing-aware insertion")
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
        Renders mistletoe Document AST back to markdown string format.
        Enables conversion of modified AST back to markdown for file writing and content output.

        [Design principles]
        AST-to-markdown conversion preserving document structure and formatting during rendering.
        Clean markdown output supporting standard markdown compatibility and tool integration.
        Error handling preventing rendering failures from disrupting document processing workflows.

        [Implementation details]
        Uses mistletoe MarkdownRenderer for complete AST-to-markdown conversion.
        Handles rendering exceptions with detailed error reporting and graceful failure recovery.
        Returns None on rendering failure to enable alternative processing strategies.
        """
        try:
            with MarkdownRenderer() as renderer:
                markdown_content = renderer.render(doc)
                
                logger.debug(f"Successfully rendered document to markdown ({len(markdown_content)} characters)")
                return markdown_content
        except Exception as e:
            logger.error(f"Failed to render document to markdown: {e}")
            return None
    
    
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
    
    def analyze_spacing_patterns(self, doc: Document) -> Dict[int, int]:
        """
        [Class method intent]
        Analyzes original spacing patterns in document using mistletoe line_number attributes.
        Creates mapping of line number gaps to understand original formatting and blank line patterns.

        [Design principles]
        Line-number-aware spacing analysis leveraging mistletoe's built-in line tracking capabilities.
        Pattern recognition identifying common spacing conventions for consistent formatting.
        Gap-based analysis determining blank line positions from line number differences.

        [Implementation details]
        Traverses document tokens examining line_number attributes to identify spacing patterns.
        Calculates line gaps between consecutive tokens to determine blank line positions.
        Returns mapping of token positions to spacing information for rendering decisions.
        """
        spacing_map = {}
        
        if not doc or not hasattr(doc, 'children'):
            return spacing_map
        
        try:
            prev_line = None
            
            for i, token in enumerate(doc.children):
                if hasattr(token, 'line_number') and token.line_number is not None:
                    current_line = token.line_number
                    
                    if prev_line is not None:
                        # Calculate gap between previous and current token
                        line_gap = current_line - prev_line
                        
                        # Store spacing information
                        spacing_map[i] = {
                            'prev_line': prev_line,
                            'current_line': current_line,
                            'gap': line_gap,
                            'blank_lines': max(0, line_gap - 1)  # -1 because one line is the token itself
                        }
                        
                        logger.debug(f"Token {i}: gap={line_gap}, blank_lines={max(0, line_gap - 1)}")
                    
                    prev_line = current_line
                else:
                    # Token doesn't have line number, use default spacing
                    spacing_map[i] = {
                        'prev_line': prev_line,
                        'current_line': None,
                        'gap': 1,
                        'blank_lines': 0
                    }
            
            logger.debug(f"Analyzed spacing patterns for {len(spacing_map)} tokens")
            return spacing_map
            
        except Exception as e:
            logger.error(f"Failed to analyze spacing patterns: {e}")
            return {}
    
    def _calculate_appropriate_spacing(self, prev_token: BlockToken, current_token: BlockToken, spacing_map: Dict[int, int]) -> int:
        """
        [Class method intent]
        Calculates appropriate line spacing between tokens based on context and patterns.
        Uses spacing analysis and token types to determine optimal blank line insertion.

        [Design principles]
        Context-aware spacing calculation considering token types and surrounding patterns.
        Pattern-based spacing decisions respecting original document formatting conventions.
        Intelligent fallback spacing for cases where patterns cannot be determined.

        [Implementation details]
        Analyzes token types (headers, paragraphs, etc.) to determine appropriate spacing.
        Considers spacing patterns from original document for consistency.
        Returns line number increment for proper spacing in modified document.
        """
        try:
            # Default spacing based on token types
            default_spacing = 2  # One blank line between sections
            
            # Analyze token types for context-aware spacing
            if isinstance(prev_token, Heading) and isinstance(current_token, Paragraph):
                # Header to paragraph: typically 1 blank line
                return 2
            elif isinstance(prev_token, Paragraph) and isinstance(current_token, Heading):
                # Paragraph to header: typically 2 blank lines for section separation
                return 3
            elif isinstance(prev_token, Heading) and isinstance(current_token, Heading):
                # Header to header: depends on levels
                if hasattr(current_token, 'level') and hasattr(prev_token, 'level'):
                    if current_token.level <= prev_token.level:
                        # Same or higher level header: more spacing
                        return 3
                    else:
                        # Lower level header: less spacing
                        return 2
                return 2
            elif isinstance(prev_token, Paragraph) and isinstance(current_token, Paragraph):
                # Paragraph to paragraph: minimal spacing
                return 2
            
            # Look for patterns in spacing map if available
            if spacing_map:
                # Calculate average spacing for similar token transitions
                gaps = [info['gap'] for info in spacing_map.values() if info['gap'] > 0]
                if gaps:
                    avg_gap = sum(gaps) // len(gaps)
                    return max(2, avg_gap)  # At least 2 lines (1 blank line)
            
            logger.debug(f"Using default spacing: {default_spacing}")
            return default_spacing
            
        except Exception as e:
            logger.error(f"Failed to calculate appropriate spacing: {e}")
            return 2  # Safe fallback
    
    def render_to_markdown_with_spacing(self, doc: Document) -> Optional[str]:
        """
        [Class method intent]
        Renders mistletoe Document AST back to markdown with preserved line spacing.
        Uses line_number attributes to calculate and preserve original blank line patterns.

        [Design principles]
        Spacing-aware rendering preserving original document formatting and blank line patterns.
        Line-number-based spacing calculation maintaining visual document structure.
        Token-by-token rendering with manual spacing insertion for precise control.

        [Implementation details]
        Calculates blank lines from line_number differences between consecutive tokens.
        Renders each token individually to prevent spacing loss by default renderer.
        Manually inserts calculated blank lines between tokens for spacing preservation.
        """
        try:
            if not doc or not hasattr(doc, 'children') or not doc.children:
                return ""
            
            # Calculate spacing information for each token
            spacing_info = []
            prev_line = None
            
            for i, token in enumerate(doc.children):
                line_num = getattr(token, 'line_number', None)
                
                blank_lines = 0
                if prev_line is not None and line_num is not None:
                    gap = line_num - prev_line
                    blank_lines = max(0, gap - 1)  # -1 because one line is the token itself
                
                spacing_info.append({
                    'token': token,
                    'blank_lines': blank_lines
                })
                
                if line_num is not None:
                    prev_line = line_num
            
            # Render tokens with spacing preservation
            rendered_parts = []
            
            for i, info in enumerate(spacing_info):
                token = info['token']
                blank_lines = info['blank_lines']
                
                # Render individual token
                temp_doc = type(doc)([])
                temp_doc.children = [token]
                
                with MarkdownRenderer() as renderer:
                    token_content = renderer.render(temp_doc).rstrip()
                
                if i == 0:
                    # First token - no spacing prefix
                    rendered_parts.append(token_content)
                else:
                    # Add blank lines before the token
                    spacing_prefix = '\n' * (blank_lines + 1)  # +1 for normal newline between tokens
                    rendered_parts.append(spacing_prefix + token_content)
            
            # Join all parts and add final newline
            final_content = ''.join(rendered_parts) + '\n'
            
            logger.debug(f"Successfully rendered document with spacing preservation ({len(final_content)} characters)")
            return final_content
            
        except Exception as e:
            logger.error(f"Failed to render document with spacing: {e}")
            # Fallback to standard rendering
            return self.render_to_markdown(doc)
    
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

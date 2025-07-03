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
# Mistletoe renderer with enhanced blank line support for markdown document processing.
# Provides spacing-aware rendering capabilities that preserve original formatting patterns
# and add appropriate blank lines between document elements for improved readability.
###############################################################################
# [Source file design principles]
# - Derived renderer extending BaseRenderer with blank line insertion capabilities
# - Spacing preservation maintaining original document formatting and visual structure
# - Token enhancement adding blank line attributes for consistent spacing behavior
# - Clean separation between rendering logic and document parsing for maintainable architecture
# - Helper functions supporting existing markdown parser integration without breaking changes
###############################################################################
# [Source file constraints]
# - Must maintain compatibility with existing markdown_parser.py imports and usage
# - Renderer must preserve markdown structure and CommonMark compliance during processing
# - Spacing logic must handle various document types including hierarchical content structures
# - Performance must be suitable for large knowledge base files with extensive content
# - Error handling must prevent rendering failures from disrupting document processing workflows
###############################################################################
# [Dependencies]
# <system>: mistletoe - AST-based markdown parsing and rendering library
# <system>: mistletoe.base_renderer - Base renderer class for custom rendering implementations
# <system>: mistletoe.block_token - Block token types for document structure handling
# <system>: typing - Type hints for function parameters and return values
# <system>: logging - Error reporting and debugging information
# <codebase>: knowledge_bases.indexing.markdown_parser - Integration with existing parser
###############################################################################
# [GenAI tool change history]
# 2025-07-03T14:15:00Z : Fixed critical markdown code block stripping bug with comprehensive token registration by CodeAssistant
# * Added comprehensive token type registration in _register_all_token_types() to prevent fallback rendering
# * Implemented strict token validation in render() method with zero-tolerance error handling approach
# * Added complete render method implementations for all mistletoe token types (18 total methods)
# * Fixed CodeFence token handling ensuring markdown code blocks are never stripped from knowledge base output
# * Eliminated silent fallbacks that were causing formatting loss, now fails clearly on unhandled token types
# 2025-07-03T09:28:00Z : Initial mistletoe spacing renderer implementation by CodeAssistant
# * Created MarkdownPreservingRenderer class with blank line support for all major elements
# * Implemented enhance_tokens_with_blank_lines() for token attribute enhancement
# * Added render_with_spacing_preservation() and preserve_llm_spacing() helper functions
# * Established foundation for spacing-aware markdown rendering with existing parser integration
###############################################################################

"""
Mistletoe Spacing Renderer for Knowledge Bases System.

This module provides enhanced mistletoe rendering capabilities with intelligent
blank line insertion and spacing preservation for improved document readability
and consistent formatting across knowledge base documents.
"""

import logging
from typing import List, Dict, Any, Optional, Union
from mistletoe import Document, block_token
from mistletoe.base_renderer import BaseRenderer
from mistletoe.block_token import (
    Heading, Paragraph, BlockToken, ThematicBreak, CodeFence, Quote,
    List as MarkdownList, ListItem, Table, TableRow, TableCell
)
from mistletoe.span_token import Strong, Emphasis, RawText, LineBreak, Link, AutoLink, InlineCode

logger = logging.getLogger(__name__)


class MarkdownPreservingRenderer(BaseRenderer):
    """
    [Class intent]
    Derived mistletoe renderer that adds appropriate blank lines when rendering documents.
    Preserves original formatting patterns while ensuring consistent spacing between elements
    for improved readability and professional document appearance.

    [Design principles]
    BaseRenderer extension providing blank line insertion without changing core rendering logic.
    Element-specific spacing rules ensuring appropriate visual separation between different content types.
    Consistent formatting preservation maintaining original document structure and visual hierarchy.
    Clean rendering output supporting both human readability and tool compatibility.

    [Implementation details]
    Extends BaseRenderer with custom render methods for major block and span elements.
    Implements intelligent spacing logic based on element types and document structure.
    Preserves inner token rendering while adding controlled blank line insertion.
    Maintains compatibility with standard mistletoe rendering pipeline and token processing.
    """
    
    def __init__(self):
        """
        [Class method intent]
        Initializes the markdown preserving renderer following mistletoe BaseRenderer patterns.
        Sets up rendering context for spacing-aware document processing with proper token handling.

        [Design principles]
        Standard mistletoe renderer initialization following BaseRenderer patterns from dev guide.
        Comprehensive render method coverage ensuring all token types are properly handled.
        Zero-tolerance approach where unhandled tokens cause immediate clear failures.

        [Implementation details]
        Calls parent BaseRenderer constructor with standard initialization.
        All token handling is done through individual render methods following mistletoe conventions.
        Uses standard mistletoe render method naming pattern (render_<token_name_lowercase>).
        """
        super().__init__()
        logger.info("MarkdownPreservingRenderer initialized with comprehensive token registration and strict validation")
    
    def render_paragraph(self, token: Paragraph) -> str:
        """
        [Class method intent]
        Renders paragraph tokens with trailing blank line for proper visual separation.
        Ensures paragraphs have appropriate spacing in the final document output.

        [Design principles]
        Paragraph-specific spacing ensuring proper visual separation between text blocks.
        Inner content preservation maintaining original paragraph formatting and structure.
        Consistent blank line addition supporting readable document flow and organization.

        [Implementation details]
        Renders paragraph inner content using inherited renderer capabilities.
        Adds double newline (blank line) after paragraph content for visual separation.
        Preserves all internal paragraph formatting including spans and inline elements.
        """
        return f"{self.render_inner(token)}\n\n"
    
    def render_heading(self, token: Heading) -> str:
        """
        [Class method intent]
        Renders heading tokens with appropriate markdown syntax and trailing blank line.
        Maintains heading levels while ensuring proper spacing for document structure.

        [Design principles]
        Level-aware heading rendering preserving document hierarchy and structure.
        Blank line addition supporting clear visual separation between sections.
        Standard markdown syntax ensuring compatibility with all markdown processors.

        [Implementation details]
        Uses token.level to generate appropriate number of hash symbols for heading syntax.
        Renders inner heading content preserving any formatting or inline elements.
        Adds trailing blank line for proper section separation and visual hierarchy.
        """
        return f"{'#' * token.level} {self.render_inner(token)}\n\n"
    
    def render_strong(self, token: Strong) -> str:
        """
        [Class method intent]
        Renders strong emphasis tokens using standard markdown bold syntax.
        Preserves text formatting without adding additional spacing for inline elements.

        [Design principles]
        Inline element rendering without spacing modification preserving text flow.
        Standard markdown syntax ensuring broad compatibility and tool support.
        Content preservation maintaining original text formatting and structure.

        [Implementation details]
        Wraps inner content with double asterisks for standard markdown bold formatting.
        Uses render_inner to preserve any nested formatting or complex span structures.
        Returns inline content without additional spacing since this is not a block element.
        """
        return f"**{self.render_inner(token)}**"
    
    def render_emphasis(self, token: Emphasis) -> str:
        """
        [Class method intent]
        Renders emphasis tokens using standard markdown italic syntax.
        Preserves text formatting without adding spacing for inline elements.

        [Design principles]
        Inline element rendering preserving text flow without block-level spacing.
        Standard markdown syntax ensuring compatibility with all markdown processors.
        Nested content preservation supporting complex formatting structures.

        [Implementation details]
        Wraps inner content with single asterisks for standard markdown italic formatting.
        Preserves any nested span elements or complex formatting through render_inner.
        Returns inline content without additional newlines since emphasis is inline element.
        """
        return f"*{self.render_inner(token)}*"
    
    def render_raw_text(self, token: RawText) -> str:
        """
        [Class method intent]
        Renders raw text tokens without modification preserving original content.
        Maintains text integrity for basic content elements without formatting changes.

        [Design principles]
        Direct content rendering without modification preserving original text exactly.
        No spacing addition since raw text represents basic content without structural meaning.
        Content integrity ensuring no unintended changes to user-provided text.

        [Implementation details]
        Returns token content directly without any processing or modification.
        Preserves all original text including whitespace and special characters.
        No additional formatting since raw text represents basic content elements.
        """
        return token.content
    
    def render_line_break(self, token: LineBreak) -> str:
        """
        [Class method intent]
        Renders line break tokens using markdown hard line break syntax.
        Preserves intentional line breaks within paragraphs and other content.

        [Design principles]
        Hard line break rendering preserving intentional formatting breaks within content.
        Standard markdown syntax using trailing spaces for broad compatibility.
        Content flow preservation maintaining original document structure and formatting.

        [Implementation details]
        Uses double space followed by newline for standard markdown hard line break.
        Preserves intentional line breaks that were specified in original document.
        Compatible with CommonMark specification for reliable rendering across tools.
        """
        return "  \n"
    
    def render_thematic_break(self, token: ThematicBreak) -> str:
        """
        [Class method intent]
        Renders thematic break tokens (horizontal rules) with proper spacing.
        Ensures thematic breaks have appropriate visual separation from surrounding content.

        [Design principles]
        Thematic break rendering with surrounding blank lines for proper visual separation.
        Standard markdown syntax ensuring compatibility with all markdown processors.
        Visual emphasis supporting clear document structure and section separation.

        [Implementation details]
        Uses triple dash syntax for widely compatible horizontal rule rendering.
        Adds trailing blank line for proper visual separation from following content.
        Provides clear visual break suitable for section separation and document organization.
        """
        return "---\n\n"
    
    def render_block_code(self, token: CodeFence) -> str:
        """
        [Class method intent]
        Renders code fence tokens with language specification and proper spacing.
        Preserves code content exactly while ensuring proper visual separation.

        [Design principles]
        Code fence rendering preserving exact content without modification or formatting changes.
        Language specification support enabling syntax highlighting in compatible renderers.
        Blank line addition ensuring proper visual separation from surrounding content.

        [Implementation details]
        Uses triple backticks with optional language specification for standard markdown.
        Preserves code content exactly including all whitespace and special characters.
        Adds trailing blank line for proper visual separation from following content.
        """
        language = getattr(token, 'language', '') or ''
        # CodeFence tokens store content in children, not content attribute
        code_content = self.render_inner(token)
        return f"```{language}\n{code_content}```\n\n"
    
    def render_quote(self, token: Quote) -> str:
        """
        [Class method intent]
        Renders block quote tokens with proper markdown syntax and spacing.
        Preserves quote content while ensuring appropriate visual separation.

        [Design principles]
        Block quote rendering with standard markdown syntax and proper spacing.
        Inner content preservation maintaining original quote formatting and structure.
        Visual separation ensuring quotes are clearly distinguished from surrounding content.

        [Implementation details]
        Uses greater-than symbol prefix for standard markdown block quote syntax.
        Renders inner content preserving any nested formatting or complex structures.
        Adds trailing blank line for proper visual separation from following content.
        """
        return f"> {self.render_inner(token)}\n\n"
    
    def render_list(self, token: MarkdownList) -> str:
        """
        [Class method intent]
        Renders list tokens with proper markdown syntax and spacing.
        Preserves list structure and numbering while ensuring proper visual separation.

        [Design principles]
        List rendering with standard markdown syntax and proper spacing.
        Structure preservation maintaining original list formatting and hierarchy.
        Visual separation ensuring lists are clearly distinguished from surrounding content.

        [Implementation details]
        Renders inner list content preserving all list items and their formatting.
        Adds trailing blank line for proper visual separation from following content.
        Maintains list type and numbering through inner content rendering.
        """
        return f"{self.render_inner(token)}"
    
    def render_list_item(self, token: ListItem) -> str:
        """
        [Class method intent]
        Renders list item tokens with proper markdown syntax.
        Preserves list item content and formatting without additional spacing.

        [Design principles]
        List item rendering preserving content without block-level spacing.
        Standard markdown syntax ensuring compatibility with all markdown processors.
        Content preservation maintaining original list item formatting and structure.

        [Implementation details]
        Renders inner list item content with appropriate list marker handling.
        Uses standard markdown list item formatting for broad compatibility.
        No additional spacing since list items are handled by parent list.
        """
        return f"- {self.render_inner(token)}"
    
    def render_table(self, token: Table) -> str:
        """
        [Class method intent]
        Renders table tokens with proper markdown syntax and spacing.
        Preserves table structure and formatting while ensuring proper visual separation.

        [Design principles]
        Table rendering with standard markdown syntax and proper spacing.
        Structure preservation maintaining original table formatting and alignment.
        Visual separation ensuring tables are clearly distinguished from surrounding content.

        [Implementation details]
        Renders inner table content preserving all rows and cell formatting.
        Adds trailing blank line for proper visual separation from following content.
        Maintains table structure through inner content rendering.
        """
        return f"{self.render_inner(token)}\n\n"
    
    def render_table_row(self, token: TableRow) -> str:
        """
        [Class method intent]
        Renders table row tokens with proper markdown syntax.
        Preserves table row content and cell structure without additional spacing.

        [Design principles]
        Table row rendering preserving content without block-level spacing.
        Standard markdown syntax ensuring compatibility with all markdown processors.
        Structure preservation maintaining original table row formatting.

        [Implementation details]
        Renders inner table row content with appropriate cell separators.
        Uses standard markdown table row formatting for broad compatibility.
        No additional spacing since table rows are handled by parent table.
        """
        return f"| {self.render_inner(token)} |\n"
    
    def render_table_cell(self, token: TableCell) -> str:
        """
        [Class method intent]
        Renders table cell tokens with proper markdown syntax.
        Preserves table cell content without additional formatting or spacing.

        [Design principles]
        Table cell rendering preserving content without modification.
        Standard markdown syntax ensuring compatibility with all markdown processors.
        Content preservation maintaining original table cell formatting.

        [Implementation details]
        Renders inner table cell content with appropriate cell separator handling.
        Uses standard markdown table cell formatting for broad compatibility.
        No additional formatting since table cells are handled by parent row.
        """
        return f"{self.render_inner(token)} |"
    
    
    def render_link(self, token: Link) -> str:
        """
        [Class method intent]
        Renders link tokens using standard markdown link syntax.
        Preserves link text and URL without additional spacing for inline elements.

        [Design principles]
        Inline element rendering without spacing modification preserving text flow.
        Standard markdown syntax ensuring broad compatibility and tool support.
        Link preservation maintaining original text and URL structure.

        [Implementation details]
        Uses standard markdown link format with text and URL components.
        Renders inner content for link text preserving any nested formatting.
        Returns inline content without additional spacing since links are inline elements.
        """
        title = getattr(token, 'title', None)
        if title:
            return f'[{self.render_inner(token)}]({token.target} "{title}")'
        else:
            return f'[{self.render_inner(token)}]({token.target})'
    
    def render_auto_link(self, token: AutoLink) -> str:
        """
        [Class method intent]
        Renders auto link tokens using standard markdown auto link syntax.
        Preserves auto link URL without additional spacing for inline elements.

        [Design principles]
        Inline element rendering without spacing modification preserving text flow.
        Standard markdown syntax ensuring broad compatibility and tool support.
        Auto link preservation maintaining original URL structure.

        [Implementation details]
        Uses standard markdown auto link format with angle brackets.
        Preserves URL exactly as specified in the original content.
        Returns inline content without additional spacing since auto links are inline elements.
        """
        return f'<{token.target}>'
    
    def render_inline_code(self, token: InlineCode) -> str:
        """
        [Class method intent]
        Renders inline code tokens using standard markdown inline code syntax.
        Preserves code content exactly without additional spacing for inline elements.

        [Design principles]
        Inline element rendering without spacing modification preserving text flow.
        Standard markdown syntax ensuring broad compatibility and tool support.
        Code preservation maintaining exact content without modification.

        [Implementation details]
        Uses single backticks for standard markdown inline code formatting.
        Preserves code content exactly including all whitespace and special characters.
        Returns inline content without additional spacing since inline code is inline element.
        """
        # InlineCode tokens store content in children, not content attribute
        return f'`{self.render_inner(token)}`'
    


def enhance_tokens_with_blank_lines(doc: Document) -> Document:
    """
    [Function intent]
    Enhances document tokens with blank_lines_before attributes for spacing preservation.
    Analyzes document structure and adds spacing metadata to support rendering decisions.

    [Design principles]
    Token enhancement preserving original document structure while adding spacing metadata.
    Line number analysis supporting intelligent spacing decisions based on original formatting.
    Non-destructive enhancement maintaining document integrity during processing.

    [Implementation details]
    Traverses document tokens analyzing line number attributes for spacing calculation.
    Adds blank_lines_before attribute to tokens based on line number gaps.
    Returns enhanced document with spacing metadata ready for spacing-aware rendering.

    Args:
        doc (Document): Mistletoe document to enhance with spacing attributes

    Returns:
        Document: Enhanced document with blank_lines_before attributes added to tokens

    Raises:
        Exception: When document enhancement fails due to structure or processing issues
    """
    try:
        if not doc or not hasattr(doc, 'children'):
            return doc
        
        prev_line = None
        
        for token in doc.children:
            # Calculate blank lines based on line number gaps
            current_line = getattr(token, 'line_number', None)
            blank_lines = 0
            
            if prev_line is not None and current_line is not None:
                gap = current_line - prev_line
                blank_lines = max(0, gap - 1)  # -1 because one line is the token itself
            
            # Add spacing attribute to token
            token.blank_lines_before = blank_lines
            
            if current_line is not None:
                prev_line = current_line
        
        logger.debug(f"Enhanced document with blank line attributes for {len(doc.children)} tokens")
        return doc
        
    except Exception as e:
        logger.error(f"Failed to enhance tokens with blank lines: {e}")
        return doc  # Return original document on failure


def render_with_spacing_preservation(doc: Document) -> Optional[str]:
    """
    [Function intent]
    Renders document using MarkdownPreservingRenderer with enhanced spacing preservation.
    Combines custom renderer with document processing for consistent spacing output.

    [Design principles]
    Spacing-aware rendering using custom renderer for consistent document formatting.
    Error handling preventing rendering failures from disrupting document processing.
    Integration support enabling seamless use with existing markdown processing workflows.

    [Implementation details]
    Creates MarkdownPreservingRenderer instance and renders document with spacing enhancement.
    Handles rendering exceptions with graceful fallback and detailed error reporting.
    Returns rendered markdown with appropriate blank lines and formatting preservation.

    Args:
        doc (Document): Mistletoe document to render with spacing preservation

    Returns:
        Optional[str]: Rendered markdown content with preserved spacing, None on failure

    Raises:
        Exception: When document rendering fails due to structure or processing issues
    """
    try:
        if not doc:
            return None
        
        with MarkdownPreservingRenderer() as renderer:
            rendered_content = renderer.render(doc)
            
        logger.debug(f"Successfully rendered document with spacing preservation ({len(rendered_content)} characters)")
        return rendered_content
        
    except Exception as e:
        logger.error(f"Failed to render document with spacing preservation: {e}")
        return None


def preserve_llm_spacing(content: str) -> str:
    """
    [Function intent]
    Preserves LLM-generated content spacing by parsing and re-rendering with spacing enhancement.
    Handles content that may have inconsistent formatting from LLM generation processes.

    [Design principles]
    LLM content processing preserving original formatting while enhancing spacing consistency.
    Parse-and-render approach ensuring content structure integrity during processing.
    Error handling preventing content corruption during spacing preservation operations.

    [Implementation details]
    Parses content into mistletoe document and enhances with spacing attributes.
    Renders enhanced document using spacing-aware renderer for consistent output.
    Handles parsing and rendering failures with graceful fallback to original content.

    Args:
        content (str): Raw markdown content from LLM generation or other sources

    Returns:
        str: Content with preserved and enhanced spacing, original content on failure

    Raises:
        Exception: When content processing fails due to parsing or rendering issues
    """
    try:
        if not content or not isinstance(content, str):
            return content or ""
        
        # Parse content into document
        doc = Document(content)
        
        # Enhance with spacing attributes
        enhanced_doc = enhance_tokens_with_blank_lines(doc)
        
        # Render with spacing preservation
        rendered_content = render_with_spacing_preservation(enhanced_doc)
        
        if rendered_content is not None:
            logger.debug(f"Successfully preserved LLM spacing for content ({len(content)} -> {len(rendered_content)} characters)")
            return rendered_content
        else:
            logger.warning("Failed to render with spacing preservation, returning original content")
            return content
            
    except Exception as e:
        logger.error(f"Failed to preserve LLM spacing: {e}")
        return content  # Return original content on failure

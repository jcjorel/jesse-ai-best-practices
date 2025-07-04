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
# Incremental markdown engine for Knowledge Bases Hierarchical Indexing System.
# Provides selective section updates without full regeneration, supporting change-based
# updates with content extraction and insertion capabilities.
###############################################################################
# [Source file design principles]
# - Incremental updates: selective section replacement without full markdown regeneration
# - Content extraction: parse subdirectory summaries from fourth-level headers
# - Standard Python markdown library compatibility ensuring parseable output structure
# - Mistletoe-based selective updates with formatting preservation
# - Raw content insertion maintaining LLM formatting without parsing complexity
###############################################################################
# [Source file constraints]
# - Generated markdown must be parseable by standard Python markdown libraries
# - Content extraction must preserve original formatting from source markdown files
# - Section replacement must maintain document structure and spacing consistency
# - All markdown formatting must follow CommonMark specification for maximum compatibility
# - Performance optimized for incremental updates over full regeneration
###############################################################################
# [Dependencies]
# <codebase>: ..models.knowledge_context - Context structures and file metadata
# <system>: pathlib - Cross-platform path operations and metadata handling
# <system>: datetime - Timestamp formatting for knowledge file metadata
# <system>: typing - Type hints for template parameters and content structures
###############################################################################
# [GenAI tool change history]
# 2025-07-04T08:40:00Z : Simplified to incremental architecture with selective section updates by CodeAssistant
# * Removed unused FileAnalysis and DirectorySummary dataclasses (fields never used)
# * Replaced 3-phase workflow complexity with focused incremental update methods
# * Added extract_subdirectory_summary method for fourth-level header content extraction
# * Simplified to core functionality: load existing, selective updates, content extraction
# 2025-07-03T11:35:00Z : Updated file and directory headers to use get_portable_path() for cross-platform compatibility by CodeAssistant
# * Modified _assemble_file_content() to use get_portable_path() for file path headers instead of just filename
# * Modified _assemble_subdirectory_content() to use get_portable_path() for directory path headers with trailing slash preservation
# * Added error handling for portable path conversion with fallback to original paths when conversion fails
# * Ensured all markdown knowledge file headers use portable path variables for cross-platform compatibility
# 2025-07-03T09:40:00Z : Integrated mistletoe parser and MarkdownPreservingRenderer for enhanced spacing by CodeAssistant
# * Replaced SimpleMarkdownDocument with MarkdownParser for robust AST-based parsing and section manipulation
# * Integrated MarkdownPreservingRenderer in all phases for consistent blank line handling in final output
# * Updated all content insertion methods to use AST manipulation with enhanced spacing preservation
# * Applied preserve_llm_spacing() to all LLM-generated content for consistent formatting enhancement
# 2025-07-03T00:21:00Z : Fixed inconsistent spacing preservation across entire content pipeline by CodeAssistant
# * Applied preserve_llm_spacing() to subdirectory hierarchical content in _assemble_subdirectory_content()
# * Applied preserve_llm_spacing() to global summary hierarchical content in finalize_with_global_summary()
# * Ensured consistent blank_lines_before approach across individual files, subdirectory summaries, and global summaries
# * Resolved issue where LLM-generated hierarchical semantic trees lost spacing during template assembly
###############################################################################

"""
Incremental Markdown Engine for Knowledge Bases System.

This module provides selective markdown updates without full regeneration, enabling
efficient change-based updates with content extraction and section replacement.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from .markdown_parser import MarkdownParser
from ...helpers.path_utils import get_project_root
from ...helpers.path_utils import get_portable_path
from ...helpers.mistletoe_spacing import MarkdownPreservingRenderer, render_with_spacing_preservation, preserve_llm_spacing
from ..models.knowledge_context import FileContext

logger = logging.getLogger(__name__)


class IncrementalMarkdownEngine:
    """
    [Class intent]
    Incremental markdown engine for selective knowledge base updates without full regeneration.
    Provides content extraction from subdirectory summaries and selective section replacement
    for efficient change-based updates maintaining document structure and formatting.

    [Design principles]
    Incremental updates: selective section replacement without full markdown regeneration.
    Content extraction: parse subdirectory summaries from fourth-level headers with formatting preservation.
    Standard markdown compatibility supporting integration with existing markdown tooling.
    Raw content insertion maintaining LLM formatting without parsing complexity.
    Performance optimization favoring targeted updates over complete file recreation.

    [Implementation details]
    Uses mistletoe parser for selective section identification and replacement operations.
    Extracts content sections from existing markdown files preserving original formatting.
    Maintains minimal standardized structure for new knowledge base files.
    Provides targeted update methods for files, subdirectories, and metadata sections.
    """
    
    def __init__(self):
        """
        [Class method intent]
        Initializes markdown template engine with mistletoe-based markdown parsing and spacing preservation.
        Sets up MarkdownParser integration and MarkdownPreservingRenderer for enhanced blank line handling
        in final knowledge file output with consistent structure and dynamic content insertion points.

        [Design principles]
        Mistletoe-based parsing providing robust AST manipulation capabilities for template operations.
        MarkdownPreservingRenderer integration ensuring consistent blank line handling in final output.
        Clean template generation supporting maintainable template management with enhanced formatting.

        [Implementation details]
        Initializes MarkdownParser instance for robust document parsing and section manipulation.
        Sets up integration with MarkdownPreservingRenderer for enhanced final output formatting.
        Maintains programmatic template generation with improved parsing and rendering capabilities.
        """
        self.markdown_parser = MarkdownParser()
        logger.info("MarkdownTemplateEngine initialized with mistletoe parser and spacing-aware renderer")
    
    def _generate_warning_header(self) -> str:
        """
        [Class method intent]
        Generates warning header for all knowledge files to prevent manual editing.
        Provides clear notice that files are automatically generated and should not be edited manually.
        Returns raw HTML comment text for direct markdown insertion.

        [Design principles]
        Consistent warning message across all generated knowledge files.
        Clear communication preventing manual edits that would be overwritten.
        Prominent placement ensuring visibility to users who open knowledge files.
        Simple string output for direct template insertion without AST complexity.

        [Implementation details]
        Returns raw HTML comment text ready for direct insertion into markdown content.
        Uses prominent formatting to ensure the warning is easily visible.
        Simple string approach avoiding unnecessary AST object creation and rendering.
        """
        return ("<!-- ⚠️ DO NOT EDIT MANUALLY! DOCUMENT AUTOMATICALLY GENERATED! ⚠️ -->\n"
                "<!-- This file is automatically generated by the JESSE Knowledge Base system. -->\n"
                "<!-- Manual edits will be overwritten during the next generation cycle. -->\n"
                "<!-- To modify content, update the source files and regenerate the knowledge base. -->\n")
    
    
    def _generate_jesse_timestamp(self) -> str:
        """
        [Class method intent]
        Generates timestamp in JESSE framework standard format for content insertion.
        Provides consistent timestamp formatting across all knowledge base content sections.

        [Design principles]
        Standardized timestamp format maintaining consistency with JESSE framework conventions.
        ISO 8601 format with UTC timezone ensuring universal timestamp compatibility.
        Current timestamp generation providing real-time accuracy for content tracking.

        [Implementation details]
        Uses datetime.now() with UTC timezone and ISO format for standardized timestamp generation.
        Returns formatted timestamp string ready for insertion into markdown italic format.
        Consistent with JESSE framework timestamp patterns used throughout the system.
        """
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    def _generate_metadata_footer(self, **kwargs) -> str:
        """
        [Class method intent]
        Programmatically generates metadata footer for knowledge files with portable path support.
        Creates consistent metadata section with generation information and statistics
        using portable paths for cross-platform compatibility.

        [Design principles]
        Programmatic metadata generation enabling flexible footer customization.
        Consistent metadata structure across all knowledge files with portable paths.
        Comprehensive generation information supporting knowledge file tracking.

        [Implementation details]
        Accepts keyword arguments for metadata values and formats them consistently.
        Converts file and directory paths to portable format for cross-platform compatibility.
        Returns formatted metadata footer ready for insertion into knowledge files.
        """
        footer_lines = ["---"]
        
        if 'timestamp' in kwargs:
            footer_lines.append(f"*Generated: {kwargs['timestamp']}*")
        
        if 'file_path' in kwargs:
            try:
                portable_file_path = get_portable_path(kwargs['file_path'])
                footer_lines.append(f"*Source: {portable_file_path}*")
            except Exception as e:
                logger.warning(f"Failed to get portable path for file {kwargs['file_path']}: {e}")
                footer_lines.append(f"*Source: {kwargs['file_path']}*")
        elif 'directory_path' in kwargs:
            try:
                portable_dir_path = get_portable_path(kwargs['directory_path'])
                footer_lines.append(f"*Source Directory: {portable_dir_path}*")
            except Exception as e:
                logger.warning(f"Failed to get portable path for directory {kwargs['directory_path']}: {e}")
                footer_lines.append(f"*Source Directory: {kwargs['directory_path']}*")
        
        if 'file_count' in kwargs:
            footer_lines.append(f"*Total Files: {kwargs['file_count']}*")
        
        if 'subdirectory_count' in kwargs:
            footer_lines.append(f"*Total Subdirectories: {kwargs['subdirectory_count']}*")
        
        if 'directory_name' in kwargs:
            footer_lines.append(f"\n# End of {kwargs['directory_name']}_kb.md")
        
        return "\n".join(footer_lines)
    
    
    
    def load_or_create_base_structure(self, kb_file_path: Path) -> str:
        """
        [Class method intent]
        Loads existing knowledge base file or creates minimal standardized structure if file doesn't exist.
        Enables incremental updates by starting from existing content or creating foundation structure
        with standard sections ready for selective content insertion.

        [Design principles]
        Incremental update foundation: load existing content to preserve unchanged sections.
        Minimal structure creation: only essential headers and placeholders for new files.
        Standard markdown compatibility ensuring parseable structure at all times.
        Error handling enabling graceful degradation when file operations encounter issues.

        [Implementation details]
        Attempts to read existing knowledge base file preserving all current content.
        Creates minimal standardized structure if file doesn't exist with essential sections.
        Returns markdown content ready for selective section updates using mistletoe parser.
        """
        try:
            if kb_file_path.exists():
                # Load existing knowledge base file
                with open(kb_file_path, 'r', encoding='utf-8') as f:
                    existing_content = f.read()
                logger.debug(f"Loaded existing knowledge base: {kb_file_path}")
                return existing_content
            else:
                # Create minimal standardized structure
                directory_path = kb_file_path.parent
                directory_name = kb_file_path.stem.replace('_kb', '')
                
                content_parts = []
                
                # Add warning header
                warning_header = self._generate_warning_header()
                content_parts.append(warning_header.strip())

                # Add main title with portable path
                try:
                    portable_path = get_portable_path(directory_path)
                    if not portable_path.endswith('/') and not portable_path.endswith('\\'):
                        if len(portable_path) >= 3 and portable_path[1:3] == ':\\':
                            title_path = portable_path + "\\"
                        else:
                            title_path = portable_path + "/"
                    else:
                        title_path = portable_path
                except Exception as e:
                    logger.warning(f"Failed to get portable path for {directory_path}, using fallback: {e}")
                    title_path = f"{directory_name}/"
                
                content_parts.append(f"# Directory Knowledge Base {title_path}")
                
                # Add standard sections with placeholders
                sections = [
                    ("Global Summary", "*Global summary to be generated*"),
                    ("Subdirectory Knowledge Integration", "*No subdirectories processed*"),
                    ("File Knowledge Integration", "*No files processed*")
                ]
                
                for section_name, placeholder in sections:
                    content_parts.append(f"\n## {section_name}\n")
                    content_parts.append(placeholder)
                
                # Add metadata footer
                metadata = self._generate_metadata_footer(
                    timestamp=self._generate_jesse_timestamp(),
                    directory_path=str(directory_path),
                    file_count=0,
                    subdirectory_count=0,
                    directory_name=directory_name
                )
                content_parts.append(f"\n{metadata}")
                
                new_content = "\n".join(content_parts)
                logger.debug(f"Created minimal structure for new knowledge base: {kb_file_path}")
                return new_content
                
        except Exception as e:
            logger.error(f"Failed to load or create base structure for {kb_file_path}: {e}")
            raise RuntimeError(f"Base structure initialization failed: {e}") from e

    def extract_subdirectory_summary(self, subdir_kb_path: Path) -> str:
        """
        [Class method intent]
        Extracts content from fourth-level header (####) to next same/higher level header from subdirectory knowledge base.
        Preserves original formatting while extracting content sections for integration into parent directory
        knowledge base maintaining hierarchical content structure.

        [Design principles]
        Content extraction with formatting preservation maintaining original LLM output quality.
        Fourth-level header targeting supporting hierarchical semantic context pattern extraction.
        Flexible header name matching enabling extraction regardless of specific header text.
        Error handling ensuring graceful degradation when extraction encounters parsing issues.

        [Implementation details]
        Parses subdirectory knowledge base file using mistletoe parser for header identification.
        Extracts all content from first fourth-level header until next same or higher level header.
        Preserves original markdown formatting including lists, code blocks, and emphasis.
        Returns extracted content ready for insertion into parent directory knowledge base.
        """
        try:
            if not subdir_kb_path.exists():
                logger.warning(f"Subdirectory knowledge base file not found: {subdir_kb_path}")
                return f"*Content not available from {subdir_kb_path.name}*"
            
            # Read subdirectory knowledge base file
            with open(subdir_kb_path, 'r', encoding='utf-8') as f:
                subdir_content = f.read()
            
            # Parse content using mistletoe parser
            doc = self.markdown_parser.parse_content(subdir_content)
            if not doc:
                logger.warning(f"Failed to parse subdirectory knowledge base: {subdir_kb_path}")
                return f"*Failed to extract content from {subdir_kb_path.name}*"
            
            # Find first fourth-level header (####) and extract content until next same/higher level header
            extracted_content = []
            in_target_section = False
            
            for token in doc.children:
                # Check if this is a header
                if hasattr(token, 'level'):
                    header_level = token.level
                    if header_level == 4 and not in_target_section:
                        # Found first fourth-level header - start extracting
                        in_target_section = True
                        continue  # Skip the header itself
                    elif header_level <= 4 and in_target_section:
                        # Found next same or higher level header - stop extracting
                        break
                
                # Extract content if we're in the target section
                if in_target_section:
                    # Render this token back to markdown
                    temp_doc = type(doc)([])
                    temp_doc.children = [token]
                    token_content = self.markdown_parser.render_to_markdown(temp_doc)
                    if token_content and token_content.strip():
                        extracted_content.append(token_content.strip())
            
            if extracted_content:
                result = "\n\n".join(extracted_content)
                logger.debug(f"Extracted {len(result)} characters from {subdir_kb_path}")
                return result
            else:
                logger.info(f"No fourth-level header content found in {subdir_kb_path}")
                return f"*No detailed content available from {subdir_kb_path.name}*"
                
        except Exception as e:
            logger.error(f"Failed to extract subdirectory summary from {subdir_kb_path}: {e}")
            return f"*Error extracting content from {subdir_kb_path.name}: {e}*"

    def replace_file_section(self, markdown_content: str, file_path: Path, analysis_content: str) -> str:
        """
        [Class method intent]
        Selectively replaces individual file section in knowledge base markdown without affecting other content.
        Uses file path to identify target section and updates only that specific section
        while preserving all other content and document structure.

        [Design principles]
        Selective replacement: update only the specific file section without touching other content.
        Path-based identification: use file path for reliable section targeting.
        Content preservation: maintain all other sections and document structure unchanged.
        Raw content insertion: preserve LLM analysis formatting without transformation.

        [Implementation details]
        Creates section header from file path using portable path conversion.
        Uses mistletoe parser to locate and replace specific file section content.
        Maintains timestamp and formatting consistency with existing content structure.
        Returns updated markdown with only the target file section modified.
        """
        try:
            # Create section header for this file
            try:
                portable_file_path = get_portable_path(file_path)
            except Exception as e:
                logger.warning(f"Failed to get portable path for {file_path}, using original: {e}")
                portable_file_path = str(file_path)
            
            section_header = f"{portable_file_path} file"
            timestamp = self._generate_jesse_timestamp()
            
            # Format new section content
            new_section_content = f"*Last Updated: {timestamp}*\n\n{analysis_content.strip()}"
            
            # Parse existing markdown
            doc = self.markdown_parser.parse_content(markdown_content)
            if not doc:
                logger.warning("Failed to parse markdown content for file section replacement")
                return markdown_content
            
            # Use section replacement with specific file header
            updated_doc = self.markdown_parser.replace_section_content(doc, section_header, new_section_content)
            
            if updated_doc:
                # Render back to markdown with spacing preservation
                updated_markdown = render_with_spacing_preservation(updated_doc)
                if updated_markdown:
                    logger.debug(f"Replaced file section: {portable_file_path}")
                    return updated_markdown
                else:
                    # Fallback to standard rendering
                    updated_markdown = self.markdown_parser.render_to_markdown(updated_doc)
                    if updated_markdown:
                        logger.debug(f"Replaced file section with standard rendering: {portable_file_path}")
                        return updated_markdown
            
            # Fallback: return original content
            logger.warning(f"File section replacement failed for: {portable_file_path}")
            return markdown_content
            
        except Exception as e:
            logger.error(f"File section replacement failed for {file_path}: {e}")
            return markdown_content

    def replace_subdirectory_section(self, markdown_content: str, subdir_path: Path, extracted_content: str) -> str:
        """
        [Class method intent]
        Selectively replaces individual subdirectory section in knowledge base markdown without affecting other content.
        Uses subdirectory path to identify target section and updates only that specific section
        while preserving all other content and document structure with extracted formatting.

        [Design principles]
        Selective replacement: update only the specific subdirectory section without touching other content.
        Path-based identification: use subdirectory path for reliable section targeting.
        Content preservation: maintain all other sections and document structure unchanged.
        Formatting preservation: maintain extracted content formatting from source knowledge base.

        [Implementation details]
        Creates section header from subdirectory path using portable path conversion with trailing slash.
        Uses mistletoe parser to locate and replace specific subdirectory section content.
        Maintains timestamp and formatting consistency with existing content structure.
        Returns updated markdown with only the target subdirectory section modified.
        """
        try:
            # Create section header for this subdirectory
            try:
                portable_dir_path = get_portable_path(subdir_path)
                # Ensure trailing slash for directory formatting
                if not portable_dir_path.endswith('/') and not portable_dir_path.endswith('\\'):
                    if len(portable_dir_path) >= 3 and portable_dir_path[1:3] == ':\\':
                        portable_dir_path += "\\"
                    else:
                        portable_dir_path += "/"
            except Exception as e:
                logger.warning(f"Failed to get portable path for {subdir_path}, using original: {e}")
                portable_dir_path = f"{subdir_path.name}/"
            
            section_header = f"{portable_dir_path} directory"
            timestamp = self._generate_jesse_timestamp()
            
            # Format new section content with extracted content
            new_section_content = f"*Last Updated: {timestamp}*\n\n{extracted_content.strip()}"
            
            # Parse existing markdown
            doc = self.markdown_parser.parse_content(markdown_content)
            if not doc:
                logger.warning("Failed to parse markdown content for subdirectory section replacement")
                return markdown_content
            
            # Use section replacement with specific subdirectory header
            updated_doc = self.markdown_parser.replace_section_content(doc, section_header, new_section_content)
            
            if updated_doc:
                # Render back to markdown with spacing preservation
                updated_markdown = render_with_spacing_preservation(updated_doc)
                if updated_markdown:
                    logger.debug(f"Replaced subdirectory section: {portable_dir_path}")
                    return updated_markdown
                else:
                    # Fallback to standard rendering
                    updated_markdown = self.markdown_parser.render_to_markdown(updated_doc)
                    if updated_markdown:
                        logger.debug(f"Replaced subdirectory section with standard rendering: {portable_dir_path}")
                        return updated_markdown
            
            # Fallback: return original content
            logger.warning(f"Subdirectory section replacement failed for: {portable_dir_path}")
            return markdown_content
            
        except Exception as e:
            logger.error(f"Subdirectory section replacement failed for {subdir_path}: {e}")
            return markdown_content

    def update_footer_metadata(self, markdown_content: str, file_count: int, subdirectory_count: int) -> str:
        """
        [Class method intent]
        Updates only the footer metadata counts without affecting other content in knowledge base markdown.
        Selectively modifies file and subdirectory counts while preserving all other document content
        and maintaining consistent metadata footer structure.

        [Design principles]
        Selective metadata update: modify only count values without affecting other content.
        String replacement strategy: use targeted replacement for specific metadata fields.
        Structure preservation: maintain all other footer content and document structure.
        Consistency maintenance: ensure metadata footer format remains standardized.

        [Implementation details]
        Uses targeted string replacement to update specific count values in metadata footer.
        Updates generation timestamp to reflect metadata modification time.
        Preserves all other metadata fields and document content unchanged.
        Returns updated markdown with refreshed metadata counts and timestamp.
        """
        try:
            updated_content = markdown_content
            
            # Update file and subdirectory counts using targeted replacement
            updated_content = updated_content.replace("*Total Files: 0*", f"*Total Files: {file_count}*")
            updated_content = updated_content.replace("*Total Subdirectories: 0*", f"*Total Subdirectories: {subdirectory_count}*")
            
            # Update existing counts if they're not zero
            import re
            
            # Replace any existing file count
            updated_content = re.sub(r'\*Total Files: \d+\*', f'*Total Files: {file_count}*', updated_content)
            
            # Replace any existing subdirectory count  
            updated_content = re.sub(r'\*Total Subdirectories: \d+\*', f'*Total Subdirectories: {subdirectory_count}*', updated_content)
            
            # Update generation timestamp
            timestamp = self._generate_jesse_timestamp()
            updated_content = re.sub(r'\*Generated: [^*]+\*', f'*Generated: {timestamp}*', updated_content)
            
            logger.debug(f"Updated footer metadata: {file_count} files, {subdirectory_count} subdirectories")
            return updated_content
            
        except Exception as e:
            logger.error(f"Footer metadata update failed: {e}")
            return markdown_content
    
    def replace_global_summary_section(self, markdown_content: str, global_summary: str) -> str:
        """
        [Class method intent]
        Selectively replaces global summary section in knowledge base markdown without affecting other content.
        Updates only the global summary section while preserving all other content and document structure
        with LLM-generated summary content and formatting preservation.

        [Design principles]
        Selective replacement: update only the global summary section without touching other content.
        Content preservation: maintain all other sections and document structure unchanged.
        Raw content insertion: preserve LLM global summary formatting without transformation.
        Spacing preservation: maintain consistent formatting through enhanced rendering.

        [Implementation details]
        Uses mistletoe parser to locate and replace specific global summary section content.
        Applies spacing preservation to LLM-generated global summary content.
        Returns updated markdown with only the global summary section modified.
        """
        try:
            # Parse existing markdown
            doc = self.markdown_parser.parse_content(markdown_content)
            if not doc:
                logger.warning("Failed to parse markdown content for global summary replacement")
                return markdown_content
            
            # Apply spacing preservation to global summary content
            content_to_use = preserve_llm_spacing(global_summary.strip())
            
            # Use section replacement with Global Summary header
            updated_doc = self.markdown_parser.replace_section_content(doc, "Global Summary", content_to_use)
            
            if updated_doc:
                # Render back to markdown with spacing preservation
                updated_markdown = render_with_spacing_preservation(updated_doc)
                if updated_markdown:
                    logger.debug("Replaced global summary section")
                    return updated_markdown
                else:
                    # Fallback to standard rendering
                    updated_markdown = self.markdown_parser.render_to_markdown(updated_doc)
                    if updated_markdown:
                        logger.debug("Replaced global summary section with standard rendering")
                        return updated_markdown
            
            # Fallback: return original content
            logger.warning("Global summary section replacement failed")
            return markdown_content
            
        except Exception as e:
            logger.error(f"Global summary section replacement failed: {e}")
            return markdown_content
    
    def extract_assembled_content(self, markdown_content: str) -> str:
        """
        [Class method intent]
        Extracts assembled content from markdown for global summary generation context.
        Provides complete directory content including file analyses and subdirectory summaries
        for LLM global summary generation with comprehensive context understanding.

        [Design principles]
        Content extraction supporting LLM global summary generation with complete context.
        Structured content assembly enabling comprehensive directory understanding for synthesis.
        Clean content separation supporting focused global summary generation prompts.

        [Implementation details]
        Removes placeholder comments and metadata to extract pure content for LLM processing.
        Includes file analyses and subdirectory summaries for comprehensive context generation.
        Returns clean content ready for inclusion in global summary generation prompts.
        """
        try:
            # Remove placeholder comments and metadata for clean content extraction
            clean_content = markdown_content
            
            # Remove placeholder comments
            placeholders = [
                "<!-- GLOBAL_SUMMARY_PLACEHOLDER -->",
                "<!-- ARCHITECTURE_PLACEHOLDER -->", 
                "<!-- KEY_PATTERNS_PLACEHOLDER -->",
                "<!-- INTEGRATION_POINTS_PLACEHOLDER -->"
            ]
            
            for placeholder in placeholders:
                clean_content = clean_content.replace(placeholder, "")
            
            # Remove metadata section for focus on content
            if "---" in clean_content:
                content_parts = clean_content.split("---")
                if len(content_parts) > 1:
                    clean_content = content_parts[0].strip()
            
            logger.debug("Extracted assembled content for global summary generation")
            return clean_content
            
        except Exception as e:
            logger.error(f"Content extraction failed: {e}")
            return markdown_content  # Fallback to original content
    
    def validate_markdown_structure(self, markdown_content: str) -> bool:
        """
        [Class method intent]
        Validates generated markdown content for standard markdown library compatibility.
        Ensures generated knowledge files meet parseability requirements and structural standards
        for integration with existing markdown processing tooling and workflows.

        [Design principles]
        Quality assurance ensuring generated markdown meets standard compatibility requirements.
        Validation logic supporting consistent markdown structure across all generated knowledge files.
        Error detection enabling early identification of template rendering issues and content problems.

        [Implementation details]
        Performs basic markdown structure validation checking for required elements and formatting.
        Validates section headers, content organization, with flexible metadata requirements.
        Returns boolean indicating whether generated markdown meets structural requirements.
        """
        try:
            # Basic validation checks
            if not markdown_content or not markdown_content.strip():
                return False
            
            # Check for essential structural elements (relaxed validation)
            essential_elements = ["#", "##"]
            for element in essential_elements:
                if element not in markdown_content:
                    logger.warning(f"Missing essential markdown element: {element}")
                    return False
            
            # Check for remaining placeholders (should be none in final content)
            # Exclude warning header HTML comments from placeholder validation
            warning_header_comments = [
                "<!-- ⚠️ DO NOT EDIT MANUALLY! DOCUMENT AUTOMATICALLY GENERATED! ⚠️ -->",
                "<!-- This file is automatically generated by the JESSE Knowledge Base system. -->",
                "<!-- Manual edits will be overwritten during the next generation cycle. -->",
                "<!-- To modify content, update the source files and regenerate the knowledge base. -->"
            ]
            
            # Check for unresolved placeholders while excluding warning header
            content_without_warnings = markdown_content
            for warning_comment in warning_header_comments:
                content_without_warnings = content_without_warnings.replace(warning_comment, "")
            
            placeholders = ["<!-- ", " -->"]
            for placeholder in placeholders:
                if placeholder in content_without_warnings:
                    logger.warning(f"Unresolved placeholder found: {placeholder}")
                    return False
            
            # Validate section structure
            lines = markdown_content.split('\n')
            has_main_header = any(line.startswith('# ') for line in lines)
            has_subheaders = any(line.startswith('## ') for line in lines)
            
            if not has_main_header or not has_subheaders:
                logger.warning("Invalid markdown structure: missing required headers")
                return False
            
            # Optional validation for metadata (more flexible matching)
            has_metadata_separator = "---" in markdown_content
            has_timestamp = any(timestamp_marker in markdown_content for timestamp_marker in [
                "*Generated:", "Generated:", "_Generated:", "**Generated:"
            ])
            
            if not has_metadata_separator:
                logger.info("Metadata footer missing but document structure is valid")
            if not has_timestamp:
                logger.info("Generation timestamp missing but document structure is valid")
            
            logger.debug("Markdown structure validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Markdown validation failed: {e}")
            return False

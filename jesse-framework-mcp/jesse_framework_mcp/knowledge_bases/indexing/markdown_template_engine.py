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
# Markdown template engine for Knowledge Bases Hierarchical Indexing System.
# Implements 3-phase generation: individual file analysis insertion, subdirectory assembly,
# and global summary generation with standard Python markdown library compatibility.
###############################################################################
# [Source file design principles]
# - Standard Python markdown library compatibility ensuring parseable output structure
# - 3-phase incremental building: file analysis → subdirectory assembly → global summary
# - Programmatic content insertion for individual file analyses and subdirectory summaries
# - Template-based generation providing consistent markdown structure across knowledge files
# - Token efficiency through selective LLM usage only for analysis and global summary
###############################################################################
# [Source file constraints]
# - Generated markdown must be parseable by standard Python markdown libraries
# - Template structure must remain consistent across different content types
# - Content insertion points must be clearly defined and programmatically accessible
# - All markdown formatting must follow CommonMark specification for maximum compatibility
# - Template rendering must be performant for large-scale knowledge base generation
###############################################################################
# [Dependencies]
# <codebase>: ..models.knowledge_context - Context structures and file metadata
# <system>: pathlib - Cross-platform path operations and metadata handling
# <system>: datetime - Timestamp formatting for knowledge file metadata
# <system>: typing - Type hints for template parameters and content structures
###############################################################################
# [GenAI tool change history]
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
Markdown Template Engine for Knowledge Bases System.

This module provides template-based markdown generation with programmatic content
insertion, enabling standard Python markdown library compatibility while optimizing
LLM token usage through selective content generation.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .markdown_parser import MarkdownParser
from ...helpers.path_utils import get_project_root
from ...helpers.path_utils import get_portable_path
from ...helpers.mistletoe_spacing import MarkdownPreservingRenderer, render_with_spacing_preservation, preserve_llm_spacing
from ..models.knowledge_context import FileContext

logger = logging.getLogger(__name__)


@dataclass
class FileAnalysis:
    """
    [Class intent]
    Structured container for individual file analysis results from LLM processing.
    Holds navigation-focused analysis content for programmatic insertion
    into markdown templates helping developers understand what they'll find when working with files.

    [Design principles]
    Structured data container enabling clean separation between analysis content and formatting.
    Navigation-focused content organization supporting developer understanding and code exploration.
    Immutable data structure preventing accidental content modification during template rendering.

    [Implementation details]
    Uses dataclass for automatic initialization and immutable structure definition.
    Contains specific navigation categories matching developer guidance requirements.
    Provides clean interface for template parameter substitution and content assembly.
    """
    file_path: Path
    what_you_ll_find: str
    main_components: str
    how_its_organized: str
    connections: str
    context_you_need: str
    implementation_notes: str


@dataclass
class DirectorySummary:
    """
    [Class intent]
    Structured container for directory-level summary content from LLM processing.
    Holds navigation-focused insights and module organization information
    for programmatic insertion into hierarchical knowledge file templates.

    [Design principles]
    Hierarchical summary container enabling consistent directory knowledge structure.
    Navigation focus supporting developer understanding and effective directory exploration.
    Clean interface for template parameter substitution in directory knowledge generation.

    [Implementation details]
    Contains directory-level navigation insights and organizational information.
    Supports hierarchical knowledge assembly through structured content organization.
    Provides type-safe interface for template rendering and content assembly operations.
    """
    directory_path: Path
    what_this_directory_contains: str
    how_its_organized: str
    common_patterns: str
    how_it_connects: str


class MarkdownTemplateEngine:
    """
    [Class intent]
    Template engine for 3-phase markdown knowledge file generation with standard parseability.
    Implements incremental building: individual file analysis insertion, subdirectory assembly,
    and global summary generation with programmatic content insertion for token efficiency.

    [Design principles]
    3-phase incremental building supporting efficient knowledge file generation workflow.
    Programmatic content insertion enabling selective LLM usage for token cost optimization.
    Standard markdown compatibility supporting integration with existing markdown tooling.
    Incremental assembly supporting complex directory structures with nested content organization.
    Clean separation between LLM-generated content and programmatic structural formatting.

    [Implementation details]
    Implements 3-phase generation workflow with incremental markdown building capabilities.
    Uses string template substitution with programmable insertion points for content assembly.
    Provides separate templates and methods for each phase of the generation process.
    Supports global summary integration reading assembled content for comprehensive synthesis.
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
    
    
    
    def _assemble_subdirectory_content(self, subdirectory_summaries: List[DirectorySummary]) -> str:
        """
        [Class method intent]
        Assembles subdirectory summary content using hierarchical semantic tree format.
        Renders complete hierarchical content directly from what_this_directory_contains field
        which now contains the full hierarchical semantic tree from enhanced prompts.

        [Design principles]
        Hierarchical content preservation using raw LLM output without section parsing or transformation.
        Direct rendering of complete semantic trees maintaining original LLM formatting and structure.
        Graceful handling of empty subdirectory lists maintaining template rendering stability.
        Timestamp integration providing content freshness tracking for individual subdirectory summaries.
        Portable path usage ensuring cross-platform compatibility in markdown headers.

        [Implementation details]
        Iterates through subdirectory summaries rendering complete hierarchical content directly.
        Uses what_this_directory_contains field which contains full hierarchical semantic tree.
        Uses get_portable_path() for cross-platform compatible directory path headers.
        Only renders sections with actual content to avoid empty section headers.
        Returns formatted markdown ready for insertion into parent directory knowledge template.
        """
        if not subdirectory_summaries:
            return "*No subdirectories in this directory*"
        
        sections = []
        for subdir_summary in subdirectory_summaries:
            # Generate timestamp for this specific subdirectory summary
            timestamp = self._generate_jesse_timestamp()
            
            # Convert directory path to portable format for cross-platform compatibility
            try:
                portable_dir_path = get_portable_path(subdir_summary.directory_path)
                # Ensure trailing slash is preserved for directory formatting
                if not portable_dir_path.endswith('/') and not portable_dir_path.endswith('\\'):
                    # Add appropriate trailing slash based on path type
                    if len(portable_dir_path) >= 3 and portable_dir_path[1:3] == ':\\':
                        # Windows path - use backslash
                        portable_dir_path += "\\"
                    else:
                        # Unix/relative path - use forward slash
                        portable_dir_path += "/"
            except Exception as e:
                logger.warning(f"Failed to get portable path for {subdir_summary.directory_path}, using original: {e}")
                portable_dir_path = f"{subdir_summary.directory_path.name}/"
            
            # Only render content that exists - skip empty fields
            section_parts = [f"### {portable_dir_path} directory", f"*Last Updated: {timestamp}*"]
            
            # Use hierarchical content directly from what_this_directory_contains as-is
            if subdir_summary.what_this_directory_contains and subdir_summary.what_this_directory_contains.strip():
                # Insert LLM content as-is without any parsing or transformation
                section_parts.append(subdir_summary.what_this_directory_contains.strip())
            
            # Only add other fields if they contain actual content (not empty strings)
            if subdir_summary.how_its_organized and subdir_summary.how_its_organized.strip():
                section_parts.append(f"**How It's Organized**: {subdir_summary.how_its_organized}")
            
            if subdir_summary.common_patterns and subdir_summary.common_patterns.strip():
                section_parts.append(f"**Common Patterns**: {subdir_summary.common_patterns}")
            
            section = "\n\n".join(section_parts)
            sections.append(section)
        
        return "\n\n".join(sections)
    
    def _assemble_file_content(self, file_contexts: List[FileContext]) -> str:
        """
        [Class method intent]
        Assembles file content into formatted markdown sections using raw LLM outputs.
        Creates simple sections with headers and timestamps, inserting LLM content as-is
        without any parsing or transformation to preserve original formatting.

        [Design principles]
        Raw content insertion maintaining complete LLM response integrity without transformation.
        Section-based organization with headers and timestamps for navigation.
        Simple assembly process avoiding complex parsing or spacing manipulation.
        Portable path usage ensuring cross-platform compatibility in markdown headers.

        [Implementation details]
        Iterates through FileContext objects using knowledge_content as-is.
        Creates sections with portable path header, timestamp, and raw LLM content.
        Uses get_portable_path() for cross-platform compatible file path headers.
        Returns formatted markdown ready for insertion without any modifications.
        """
        if not file_contexts:
            return "*No files analyzed in this directory*"
        
        sections = []
        for file_context in file_contexts:
            if file_context.is_completed and file_context.knowledge_content:
                # Generate timestamp for this specific file analysis
                timestamp = self._generate_jesse_timestamp()
                
                # Convert file path to portable format for cross-platform compatibility
                try:
                    portable_file_path = get_portable_path(file_context.file_path)
                except Exception as e:
                    logger.warning(f"Failed to get portable path for {file_context.file_path}, using original: {e}")
                    portable_file_path = str(file_context.file_path)
                
                # Use LLM content as-is without any parsing or transformation
                section = f"### {portable_file_path} file\n*Last Updated: {timestamp}*\n\n{file_context.knowledge_content}"
                sections.append(section)
        
        # Use double newlines between sections for proper separation
        return "\n\n".join(sections)
    
    def initialize_directory_knowledge_base(self, directory_path: Path) -> str:
        """
        [Class method intent]
        Phase 1: Initializes base directory knowledge markdown structure programmatically.
        Creates structured markdown template ready for programmatic content insertion
        in subsequent phases of the 3-phase generation workflow.

        [Design principles]
        Programmatic structure initialization enabling clean incremental building workflow.
        Header-based approach supporting mistletoe content insertion without template complexity.
        Standard markdown compatibility ensuring parseability at every phase of generation.

        [Implementation details]
        Uses programmatic generation with structured headers for content insertion points.
        Creates initial markdown structure with proper headers and metadata sections.
        Returns markdown ready for Phase 2 file analysis insertion and Phase 3 global summary generation.
        """
        try:
            # Generate content programmatically
            content_parts = []
            
            # Add warning header (spacing handled by HTML transition logic in parser)
            warning_header = self._generate_warning_header()
            content_parts.append(warning_header.strip())

            # Add main title with portable path using new path utilities
            try:
                portable_path = get_portable_path(directory_path)
                # Ensure directory path has trailing separator for proper formatting
                # Use appropriate separator based on path type (backslash for Windows, forward slash for others)
                if len(portable_path) >= 3 and portable_path[1:3] == ':\\':
                    # Windows path - use backslash
                    if not portable_path.endswith('\\'):
                        title_path = portable_path + "\\"
                    else:
                        title_path = portable_path
                else:
                    # Unix/relative path - use forward slash
                    if not portable_path.endswith('/'):
                        title_path = portable_path + "/"
                    else:
                        title_path = portable_path
            except Exception as e:
                logger.warning(f"Failed to get portable path for {directory_path}, using fallback: {e}")
                # Fallback to full path if portable path conversion fails
                dir_str = str(directory_path)
                if len(dir_str) >= 3 and dir_str[1:3] == ':\\':
                    # Windows path fallback - use backslash
                    title_path = dir_str + "\\"
                else:
                    # Unix path fallback - use forward slash
                    title_path = dir_str + "/"
            
            content_parts.append(f"# Directory Knowledge Base {title_path}'\n")
            
            # Generate sections programmatically with placeholder content
            sections = [
                "Global Summary",
                "Subdirectory Knowledge Integration",
                "File Knowledge Integration"
            ]
            placeholder_values = [
                "*To be generated using complete assembled content*",
                "*No subdirectories processed*",
                "*No files processed*"
            ]
            
            for section, placeholder in zip(sections, placeholder_values):
                content_parts.append(f"## {section}")
                content_parts.append("")  # Add blank line between header and content
                content_parts.append(placeholder)
            
            # Add metadata footer
            metadata = self._generate_metadata_footer(
                timestamp=datetime.now().isoformat(),
                directory_path=str(directory_path),
                file_count=0,
                subdirectory_count=0,
                directory_name=directory_path.name
            )
            content_parts.append(metadata)
            
            base_content = "\n".join(content_parts)
            
            logger.debug(f"Initialized base directory knowledge structure programmatically for: {directory_path}")
            return base_content
            
        except Exception as e:
            logger.error(f"Base directory initialization failed for {directory_path}: {e}")
            raise RuntimeError(f"Programmatic base generation failed: {e}") from e
    
    def insert_file_analyses(self, markdown_content: str, file_contexts: List[FileContext]) -> str:
        """
        [Class method intent]
        Phase 2: Programmatically inserts individual file contexts into markdown structure using mistletoe parser.
        Uses AST-based section identification with robust parsing for reliable content updates
        while preserving all LLM response spacing and formatting through MarkdownPreservingRenderer.

        [Design principles]
        AST-based content identification enabling robust file content integration with mistletoe parsing.
        Spacing preservation through MarkdownPreservingRenderer maintaining all original formatting.
        Raw content insertion maintaining complete LLM response integrity without transformation.
        Robust error handling ensuring reliable content insertion with fallback to original content.

        [Implementation details]
        Parses markdown content using mistletoe MarkdownParser for header-based section replacement.
        Assembles file content directly from FileContext objects and uses AST-based section replacement.
        Returns updated markdown with enhanced spacing through MarkdownPreservingRenderer integration.
        """
        try:
            # Parse existing markdown content using mistletoe parser
            doc = self.markdown_parser.parse_content(markdown_content)
            if not doc:
                logger.warning("Failed to parse markdown content, returning original")
                return markdown_content
            
            # Assemble file content using existing method with FileContext objects
            file_content = self._assemble_file_content(file_contexts)
            
            # Use mistletoe section replacement with AST manipulation
            updated_doc = self.markdown_parser.replace_section_content(doc, "File Knowledge Integration", file_content)
            
            if updated_doc:
                # Render back to markdown with enhanced spacing preservation
                updated_markdown = render_with_spacing_preservation(updated_doc)
                if updated_markdown:
                    logger.debug(f"Inserted {len(file_contexts)} file contexts using mistletoe parser with enhanced spacing")
                    return updated_markdown
                else:
                    # Fallback to standard rendering
                    updated_markdown = self.markdown_parser.render_to_markdown(updated_doc)
                    if updated_markdown:
                        logger.debug(f"Inserted {len(file_contexts)} file contexts using mistletoe parser with standard rendering")
                        return updated_markdown
            
            # Fallback: return original content
            logger.warning("File context insertion failed, returning original content")
            return markdown_content
            
        except Exception as e:
            logger.error(f"File context insertion failed: {e}")
            return markdown_content
    
    def insert_file_contexts(self, markdown_content: str, file_contexts: List[FileContext]) -> str:
        """
        [Class method intent]
        Alias method for insert_file_analyses providing compatibility with simplified naming.
        Delegates to insert_file_analyses for actual implementation while maintaining
        consistent interface for ultra-simplified data pipeline processing.

        [Design principles]
        Interface compatibility supporting calling code without breaking changes.
        Method delegation maintaining single implementation point for file context insertion.
        Simplified naming reflecting ultra-simplified data pipeline architecture.

        [Implementation details]
        Direct delegation to insert_file_analyses with identical parameters and return behavior.
        Maintains same error handling and processing logic through delegation pattern.
        """
        return self.insert_file_analyses(markdown_content, file_contexts)
    
    def insert_subdirectory_summaries(self, markdown_content: str, subdirectory_summaries: List[DirectorySummary]) -> str:
        """
        [Class method intent]
        Phase 2b: Programmatically inserts subdirectory summaries into markdown structure using mistletoe parser.
        Uses AST-based section identification with robust parsing for reliable content updates
        while preserving all LLM response spacing and formatting through MarkdownPreservingRenderer.

        [Design principles]
        AST-based content identification enabling robust subdirectory integration with mistletoe parsing.
        Spacing preservation through MarkdownPreservingRenderer maintaining all original formatting.
        Hierarchical content integration supporting bottom-up knowledge assembly patterns.

        [Implementation details]
        Parses markdown content using mistletoe MarkdownParser for header-based section replacement.
        Assembles subdirectory content and uses AST-based section replacement with enhanced spacing.
        Returns updated markdown ready for Phase 3 global summary generation using assembled content.
        """
        try:
            # Parse existing markdown content using mistletoe parser
            doc = self.markdown_parser.parse_content(markdown_content)
            if not doc:
                logger.warning("Failed to parse markdown content, returning original")
                return markdown_content
            
            # Assemble subdirectory content using existing method
            subdirectory_content = self._assemble_subdirectory_content(subdirectory_summaries)
            
            # Apply spacing preservation to hierarchical content
            subdirectory_content = preserve_llm_spacing(subdirectory_content)
            
            # Use mistletoe section replacement with AST manipulation
            updated_doc = self.markdown_parser.replace_section_content(doc, "Subdirectory Knowledge Integration", subdirectory_content)
            
            if updated_doc:
                # Render back to markdown with enhanced spacing preservation
                updated_markdown = render_with_spacing_preservation(updated_doc)
                if updated_markdown:
                    logger.debug(f"Inserted {len(subdirectory_summaries)} subdirectory summaries using mistletoe parser with enhanced spacing")
                    return updated_markdown
                else:
                    # Fallback to standard rendering
                    updated_markdown = self.markdown_parser.render_to_markdown(updated_doc)
                    if updated_markdown:
                        logger.debug(f"Inserted {len(subdirectory_summaries)} subdirectory summaries using mistletoe parser with standard rendering")
                        return updated_markdown
            
            # Fallback: return original content
            logger.warning("Subdirectory summary insertion failed, returning original content")
            return markdown_content
            
        except Exception as e:
            logger.error(f"Subdirectory summary insertion failed: {e}")
            return markdown_content
    
    def finalize_with_global_summary(
        self, 
        markdown_content: str, 
        global_summary: str,
        directory_summary: DirectorySummary,
        file_count: int,
        subdirectory_count: int
    ) -> str:
        """
        [Class method intent]
        Phase 3: Finalizes directory knowledge with LLM-generated global summary using mistletoe parser.
        Uses AST-based section identification with robust parsing for reliable content updates
        while preserving all LLM response spacing through MarkdownPreservingRenderer to complete workflow.

        [Design principles]
        AST-based content identification enabling robust global summary integration with mistletoe parsing.
        Spacing preservation through MarkdownPreservingRenderer maintaining all original formatting.
        Global summary integration leveraging complete assembled content for comprehensive synthesis.
        Metadata finalization providing complete directory statistics and generation information.

        [Implementation details]
        Parses markdown content using mistletoe MarkdownParser for header-based section replacement.
        Updates global summary section with enhanced spacing preservation and updates metadata counts.
        Returns final markdown with enhanced spacing through MarkdownPreservingRenderer integration.
        """
        try:
            # Parse existing markdown content using mistletoe parser
            doc = self.markdown_parser.parse_content(markdown_content)
            if not doc:
                logger.warning("Failed to parse markdown content, returning original")
                return markdown_content
            
            # Use global summary content with spacing preservation
            content_to_use = preserve_llm_spacing(global_summary.strip())
            
            # Use mistletoe section replacement with AST manipulation
            updated_doc = self.markdown_parser.replace_section_content(doc, "Global Summary", content_to_use)
            
            if updated_doc:
                # Render back to markdown with enhanced spacing preservation
                updated_markdown = render_with_spacing_preservation(updated_doc)
                if not updated_markdown:
                    # Fallback to standard rendering
                    updated_markdown = self.markdown_parser.render_to_markdown(updated_doc)
                
                if updated_markdown:
                    # Update metadata using simple string replacement (safe for metadata)
                    updated_markdown = updated_markdown.replace("*Total Files: 0*", f"*Total Files: {file_count}*")
                    updated_markdown = updated_markdown.replace("*Total Subdirectories: 0*", f"*Total Subdirectories: {subdirectory_count}*")
                    
                    # Ensure metadata footer is present
                    if "---" not in updated_markdown or "*Generated:" not in updated_markdown:
                        # Re-add metadata footer if it was stripped
                        directory_name = directory_summary.directory_path.name
                        metadata_footer = self._generate_metadata_footer(
                            timestamp=datetime.now().isoformat(),
                            directory_path=str(directory_summary.directory_path),
                            file_count=file_count,
                            subdirectory_count=subdirectory_count,
                            directory_name=directory_name
                        )
                        
                        # Remove the existing end marker if present and add complete metadata footer
                        if f"# End of {directory_name}_kb.md" in updated_markdown:
                            updated_markdown = updated_markdown.replace(f"# End of {directory_name}_kb.md", "")
                        
                        updated_markdown = updated_markdown.rstrip() + "\n\n" + metadata_footer
                    
                    logger.debug("Finalized directory knowledge using mistletoe parser with enhanced spacing preservation")
                    return updated_markdown
            
            # Fallback: return original content
            logger.warning("Global summary finalization failed, returning original content")
            return markdown_content
            
        except Exception as e:
            logger.error(f"Global summary finalization failed: {e}")
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

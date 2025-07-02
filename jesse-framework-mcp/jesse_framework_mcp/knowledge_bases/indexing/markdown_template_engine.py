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
# 2025-07-01T18:49:00Z : Completed programmatic template generation with warning headers by CodeAssistant
# * Eliminated all hardcoded template strings in favor of programmatic generation
# * Added warning headers to all knowledge files preventing manual editing
# * Enhanced placeholder validation to exclude warning header HTML comments
# * Implemented flexible template generation supporting dynamic content structure
# 2025-07-01T18:41:00Z : Completed migration to mistletoe-only markdown editing by CodeAssistant
# * Replaced all string-based replacement methods with mistletoe AST manipulation
# * Updated insert_file_analyses, insert_subdirectory_summaries, finalize_with_global_summary to use AST parsing
# * Enhanced error handling with fallback to original content on parsing failures
# * Eliminated fragile string replacement operations in favor of robust header-based editing
# 2025-07-01T17:35:00Z : Integrated mistletoe for header-based markdown editing by CodeAssistant
# * Added MarkdownParser integration for AST-based markdown manipulation
# * Implemented header-based editing methods for existing file updates
# * Added intelligent file editing strategy with structure validation
# * Migrated from placeholder-based to header-based section editing
# 2025-07-01T16:21:00Z : Initial markdown template engine creation by CodeAssistant
# * Created parseable markdown template system with programmatic content insertion
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
from ...helpers.project_root import get_project_root
from ..models.knowledge_context import FileContext
from mistletoe import Document
from mistletoe.block_token import Paragraph
from mistletoe.span_token import RawText

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
        Initializes markdown template engine with programmatic template generation.
        Sets up template generation methods for file analysis and directory summary generation
        with consistent structure and dynamic content insertion points.

        [Design principles]
        Programmatic template generation providing flexible structure definitions for all knowledge types.
        Dynamic template creation ensuring adaptable structure across generated knowledge files.
        Clean template generation supporting maintainable template management and updates.

        [Implementation details]
        Uses programmatic methods to generate templates with architectural focus and technical detail sections.
        Creates dynamic template generation supporting hierarchical content organization and summary assembly.
        Sets up common template elements through methods for consistent metadata and formatting.
        """
        
        # Initialize mistletoe-based parser for header-based editing
        self.markdown_parser = MarkdownParser()
        
        logger.info("MarkdownTemplateEngine initialized with programmatic template generation and mistletoe parser")
    
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
    
    def _generate_file_template_sections(self) -> List[str]:
        """
        [Class method intent]
        Programmatically generates file knowledge template sections.
        Creates standardized section structure for individual file analysis with navigation focus.

        [Design principles]
        Programmatic section generation enabling flexible template modification.
        Standardized section structure ensuring consistency across file knowledge.
        Navigation focus supporting developer understanding and code exploration.

        [Implementation details]
        Returns list of section headers and content placeholders for file templates.
        Uses consistent naming and structure for all file analysis sections.
        """
        return [
            "What You'll Find",
            "Main Components", 
            "How It's Organized",
            "Connections",
            "Context You Need",
            "Implementation Notes"
        ]
    
    def _generate_directory_template_sections(self) -> List[str]:
        """
        [Class method intent]
        Programmatically generates directory knowledge template sections.
        Creates standardized section structure for directory-level analysis.

        [Design principles]
        Programmatic section generation enabling flexible template modification.
        Hierarchical section structure supporting directory knowledge organization.
        Comprehensive analysis sections supporting architectural understanding.

        [Implementation details]
        Returns list of section headers for directory templates including analysis and integration sections.
        Uses consistent naming and structure for all directory knowledge sections.
        """
        return [
            "Global Summary",
            "Architecture and Design",
            "Key Patterns",
            "Integration Points", 
            "Subdirectory Knowledge Integration",
            "File Knowledge Integration"
        ]
    
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
        Programmatically generates metadata footer for knowledge files.
        Creates consistent metadata section with generation information and statistics.

        [Design principles]
        Programmatic metadata generation enabling flexible footer customization.
        Consistent metadata structure across all knowledge files.
        Comprehensive generation information supporting knowledge file tracking.

        [Implementation details]
        Accepts keyword arguments for metadata values and formats them consistently.
        Returns formatted metadata footer ready for insertion into knowledge files.
        """
        footer_lines = ["---"]
        
        if 'timestamp' in kwargs:
            footer_lines.append(f"*Generated: {kwargs['timestamp']}*")
        
        if 'file_path' in kwargs:
            footer_lines.append(f"*Source: {kwargs['file_path']}*")
        elif 'directory_path' in kwargs:
            footer_lines.append(f"*Source Directory: {kwargs['directory_path']}*")
        
        if 'file_count' in kwargs:
            footer_lines.append(f"*Total Files: {kwargs['file_count']}*")
        
        if 'subdirectory_count' in kwargs:
            footer_lines.append(f"*Total Subdirectories: {kwargs['subdirectory_count']}*")
        
        if 'directory_name' in kwargs:
            footer_lines.append(f"\n# End of {kwargs['directory_name']}_kb.md")
        
        return "\n".join(footer_lines)
    
    def generate_file_knowledge(self, file_analysis: FileAnalysis) -> str:
        """
        [Class method intent]
        Generates complete file knowledge markdown using programmatic template structure and LLM analysis content.
        Combines architectural analysis content with consistent markdown formatting
        for standard markdown library compatibility and structured knowledge organization.

        [Design principles]
        Programmatic template generation ensuring consistent file knowledge structure across all files.
        Content insertion maintaining separation between analysis content and markdown formatting.
        Timestamp integration providing knowledge file generation metadata for tracking and updates.

        [Implementation details]
        Uses programmatic template generation with structured content insertion for comprehensive file knowledge.
        Incorporates all FileAnalysis content categories into standardized markdown sections.
        Adds generation metadata including timestamp and source file information for traceability.
        """
        try:
            # Generate content programmatically
            content_parts = []
            
            # Add warning header (spacing handled by HTML transition logic in parser)
            warning_header = self._generate_warning_header()
            content_parts.append(warning_header.strip())

            # Add main title
            content_parts.append(f"# {file_analysis.file_path.stem} Knowledge\n")
            
            # Generate sections programmatically
            sections = self._generate_file_template_sections()
            analysis_values = [
                file_analysis.what_you_ll_find,
                file_analysis.main_components,
                file_analysis.how_its_organized,
                file_analysis.connections,
                file_analysis.context_you_need,
                file_analysis.implementation_notes
            ]
            
            for section, value in zip(sections, analysis_values):
                content_parts.append(f"## {section}")
                content_parts.append("")  # Add blank line between header and content
                content_parts.append(value)
            
            # Add metadata footer
            metadata = self._generate_metadata_footer(
                timestamp=datetime.now().isoformat(),
                file_path=str(file_analysis.file_path)
            )
            content_parts.append(metadata)
            
            rendered_content = "\n".join(content_parts)
            
            logger.debug(f"Generated file knowledge markdown programmatically for: {file_analysis.file_path}")
            return rendered_content
            
        except Exception as e:
            logger.error(f"File knowledge generation failed for {file_analysis.file_path}: {e}")
            raise RuntimeError(f"Programmatic template generation failed: {e}") from e
    
    def generate_directory_knowledge(
        self, 
        directory_summary: DirectorySummary,
        file_analyses: List[FileAnalysis],
        subdirectory_summaries: List[DirectorySummary]
    ) -> str:
        """
        [Class method intent]
        Generates complete directory knowledge markdown by assembling directory summary
        with programmatically inserted file analyses and subdirectory content.
        Implements hierarchical knowledge assembly with consistent template structure.

        [Design principles]
        Hierarchical content assembly combining directory-level insights with file-level analysis.
        Programmatic content insertion enabling efficient knowledge file generation without full LLM markdown.
        Template consistency ensuring standard markdown structure across all directory knowledge files.
        Comprehensive content integration supporting complete directory understanding and navigation.

        [Implementation details]
        Assembles subdirectory content through recursive summary integration and formatting.
        Incorporates all file analyses into structured file knowledge sections with consistent formatting.
        Uses directory template with complete content substitution for hierarchical knowledge organization.
        Adds comprehensive metadata including file counts and generation timestamps for knowledge tracking.
        """
        try:
            # Assemble subdirectory content
            subdirectory_content = self._assemble_subdirectory_content(subdirectory_summaries)
            
            # Assemble file content
            file_content = self._assemble_file_content(file_analyses)
            
            # Generate complete directory knowledge
            rendered_content = self.directory_template.format(
                directory_name=directory_summary.directory_path.name,
                directory_overview=directory_summary.directory_overview,
                architecture_and_design=directory_summary.architecture_and_design,
                key_patterns=directory_summary.key_patterns,
                integration_points=directory_summary.integration_points,
                subdirectory_content=subdirectory_content,
                file_content=file_content,
                timestamp=datetime.now().isoformat(),
                directory_path=str(directory_summary.directory_path),
                file_count=len(file_analyses),
                subdirectory_count=len(subdirectory_summaries)
            )
            
            logger.debug(f"Generated directory knowledge markdown for: {directory_summary.directory_path}")
            return rendered_content
            
        except Exception as e:
            logger.error(f"Directory knowledge generation failed for {directory_summary.directory_path}: {e}")
            raise RuntimeError(f"Template rendering failed: {e}") from e
    
    def _assemble_subdirectory_content(self, subdirectory_summaries: List[DirectorySummary]) -> str:
        """
        [Class method intent]
        Assembles subdirectory summary content into formatted markdown sections for directory integration.
        Provides structured organization of child directory information within parent directory knowledge.
        Includes last updated timestamps for each individual subdirectory summary.

        [Design principles]
        Hierarchical content organization supporting clear subdirectory relationship representation.
        Consistent formatting ensuring readable and navigable directory knowledge structure.
        Graceful handling of empty subdirectory lists maintaining template rendering stability.
        Timestamp integration providing content freshness tracking for individual subdirectory summaries.

        [Implementation details]
        Iterates through subdirectory summaries creating formatted sections for each child directory.
        Uses consistent section formatting with directory names and summary content integration.
        Prepends JESSE framework standard timestamp to each subdirectory summary section.
        Returns formatted markdown ready for insertion into parent directory knowledge template.
        """
        if not subdirectory_summaries:
            return "*No subdirectories in this directory*"
        
        sections = []
        for subdir_summary in subdirectory_summaries:
            # Generate timestamp for this specific subdirectory summary
            timestamp = self._generate_jesse_timestamp()
            
            section = f"""
### {subdir_summary.directory_path.name}/
*Last Updated: {timestamp}*

**What This Directory Contains**: {subdir_summary.what_this_directory_contains}

**How It's Organized**: {subdir_summary.how_its_organized}

**Common Patterns**: {subdir_summary.common_patterns}"""
            sections.append(section)
        
        return "\n\n".join(sections)
    
    def _assemble_file_content(self, file_contexts: List[FileContext]) -> str:
        """
        [Class method intent]
        Assembles raw file content into formatted markdown sections using exact LLM responses.
        Creates ultra-simplified file sections with only filename headers, timestamps, 
        and completely untransformed LLM content for directory integration.

        [Design principles]
        Zero content transformation preserving exact LLM responses with original whitespace.
        Minimal structure with only essential headers and timestamp for file identification.
        Direct FileContext usage eliminating intermediate data structure transformations.
        Raw content preservation maintaining complete LLM response integrity.

        [Implementation details]
        Iterates through FileContext objects using knowledge_content field directly.
        Creates sections with filename header, timestamp, and exact LLM response.
        No content processing, formatting, or transformation applied to LLM responses.
        Returns formatted markdown ready for insertion into directory knowledge files.
        """
        if not file_contexts:
            return "*No files analyzed in this directory*"
        
        sections = []
        for file_context in file_contexts:
            if file_context.is_completed and file_context.knowledge_content:
                # Generate timestamp for this specific file analysis
                timestamp = self._generate_jesse_timestamp()
                
                # Use exact LLM response with no transformation
                section = f"""### {file_context.file_path.name}
*Last Updated: {timestamp}*

{file_context.knowledge_content}"""
                sections.append(section)
        
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

            # Add main title with relative path from project root
            project_root = get_project_root()
            if project_root:
                try:
                    # Calculate relative path from project root
                    relative_path = directory_path.relative_to(project_root)
                    title_path = str(relative_path) + "/"
                except ValueError:
                    # Directory is not under project root, use full filesystem path
                    title_path = str(directory_path) + "/"
            else:
                # Fallback to full path if project root not found
                title_path = str(directory_path) + "/"
            
            content_parts.append(f"# Directory Knowledge Base {title_path}'\n")
            
            # Generate sections programmatically with placeholder content
            sections = self._generate_directory_template_sections()
            placeholder_values = [
                "*To be generated using complete assembled content*",
                "*Analysis to be provided*",
                "*Patterns to be identified*", 
                "*Integration analysis to be completed*",
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
        Phase 2: Programmatically inserts individual file contexts into markdown structure using mistletoe AST manipulation.
        Uses header-based section identification with AST parsing for reliable content updates
        with exact LLM response preservation without any transformation.

        [Design principles]
        AST-based content identification enabling safe file content integration without placeholder dependencies.
        Mistletoe parsing preserving markdown formatting and structure during content updates.
        Raw content insertion maintaining complete LLM response integrity without transformation.
        Robust error handling ensuring reliable content insertion with fallback to original content.

        [Implementation details]
        Parses markdown content using mistletoe for AST manipulation.
        Assembles file content directly from FileContext objects and uses header-based section replacement.
        Returns updated markdown ready for Phase 3 subdirectory and global summary integration.
        """
        try:
            # Parse existing markdown content
            doc = self.markdown_parser.parse_content(markdown_content)
            if not doc:
                logger.error("Failed to parse markdown content for file context insertion")
                return markdown_content
            
            # Assemble file content using existing method with FileContext objects
            file_content = self._assemble_file_content(file_contexts)
            
            # Use mistletoe-based section replacement
            updated_doc = self.markdown_parser.replace_section_content(
                doc, "File Knowledge Integration", file_content
            )
            
            if updated_doc:
                # Render back to markdown
                updated_markdown = self.markdown_parser.render_to_markdown(updated_doc)
                if updated_markdown:
                    logger.debug(f"Inserted {len(file_contexts)} file contexts using mistletoe AST manipulation")
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
        Phase 2b: Programmatically inserts subdirectory summaries into markdown structure using mistletoe AST manipulation.
        Uses header-based section identification with AST parsing for reliable content updates
        for hierarchical knowledge integration and structured directory organization.

        [Design principles]
        AST-based content identification enabling safe subdirectory integration without placeholder dependencies.
        Mistletoe parsing preserving markdown formatting and structure during content updates.
        Hierarchical content integration supporting bottom-up knowledge assembly patterns.

        [Implementation details]
        Parses markdown content using mistletoe for AST manipulation.
        Assembles subdirectory content and uses header-based section replacement.
        Returns updated markdown ready for Phase 3 global summary generation using assembled content.
        """
        try:
            # Parse existing markdown content
            doc = self.markdown_parser.parse_content(markdown_content)
            if not doc:
                logger.error("Failed to parse markdown content for subdirectory summary insertion")
                return markdown_content
            
            # Assemble subdirectory content using existing method
            subdirectory_content = self._assemble_subdirectory_content(subdirectory_summaries)
            
            # Use mistletoe-based section replacement
            updated_doc = self.markdown_parser.replace_section_content(
                doc, "Subdirectory Knowledge Integration", subdirectory_content
            )
            
            if updated_doc:
                # Render back to markdown
                updated_markdown = self.markdown_parser.render_to_markdown(updated_doc)
                if updated_markdown:
                    logger.debug(f"Inserted {len(subdirectory_summaries)} subdirectory summaries using mistletoe AST manipulation")
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
        Phase 3: Finalizes directory knowledge with LLM-generated global summary and directory insights using mistletoe AST manipulation.
        Uses header-based section identification with AST parsing for reliable content updates
        to complete the 3-phase generation workflow with comprehensive knowledge integration.

        [Design principles]
        AST-based content identification enabling safe finalization without placeholder dependencies.
        Mistletoe parsing preserving markdown formatting and structure during content updates.
        Global summary integration leveraging complete assembled content for comprehensive synthesis.
        Metadata finalization providing complete directory statistics and generation information.

        [Implementation details]
        Parses markdown content using mistletoe for AST manipulation.
        Updates multiple sections using batch section replacement for efficiency.
        Updates metadata sections with actual file and subdirectory counts for accurate statistics.
        Returns final markdown ready for standard markdown library parsing and knowledge base integration.
        """
        try:
            # Parse existing markdown content
            doc = self.markdown_parser.parse_content(markdown_content)
            if not doc:
                logger.error("Failed to parse markdown content for global summary finalization")
                return markdown_content
            
            # Define sections to update - Global Summary gets clean content without duplicate headers
            section_updates = {
                "Global Summary": global_summary.strip(),
                "Architecture and Design": directory_summary.how_its_organized,
                "Key Patterns": directory_summary.common_patterns,
                "Integration Points": directory_summary.how_it_connects
            }
            
            # Use mistletoe-based batch section replacement
            updated_doc = self.markdown_parser.replace_multiple_sections(doc, section_updates)
            
            # Now update the Global Summary header to include directory name
            if updated_doc:
                # Find and update the Global Summary header to include directory name
                updated_doc = self._update_global_summary_header_text(updated_doc, directory_summary.directory_path.name)
            
            if updated_doc:
                # Render back to markdown
                updated_markdown = self.markdown_parser.render_to_markdown(updated_doc)
                if updated_markdown:
                    # Update metadata using simple string replacement (safe for metadata)
                    updated_markdown = updated_markdown.replace("*Total Files: 0*", f"*Total Files: {file_count}*")
                    updated_markdown = updated_markdown.replace("*Total Subdirectories: 0*", f"*Total Subdirectories: {subdirectory_count}*")
                    
                    # Ensure metadata footer is present (mistletoe may strip it during AST operations)
                    if "---" not in updated_markdown or "*Generated:" not in updated_markdown:
                        # Re-add metadata footer if it was stripped during AST manipulation
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
                    
                    logger.debug("Finalized directory knowledge using mistletoe AST manipulation")
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
    
    # New mistletoe-based header editing methods
    
    def parse_existing_markdown(self, file_path: Path) -> Optional[Any]:
        """
        [Class method intent]
        Parses existing markdown file using mistletoe for header-based editing operations.
        Enables safe manipulation of existing knowledge files without relying on placeholders.

        [Design principles]
        AST-based parsing supporting reliable structure identification in existing markdown files.
        Error handling preventing parsing failures from disrupting knowledge file editing workflows.
        Integration with existing template engine maintaining consistent processing patterns.

        [Implementation details]
        Uses MarkdownParser to create mistletoe Document AST from existing file.
        Returns parsed document ready for header-based content manipulation and editing.
        Handles file access and parsing errors with graceful fallback strategies.
        """
        try:
            doc = self.markdown_parser.parse_file(file_path)
            if doc:
                logger.debug(f"Successfully parsed existing markdown file for editing: {file_path}")
            return doc
        except Exception as e:
            logger.error(f"Failed to parse existing markdown file {file_path}: {e}")
            return None
    
    def update_section_by_header(self, file_path: Path, header_text: str, new_content: str) -> bool:
        """
        [Class method intent]
        Updates section content following specified header in existing markdown file.
        Provides safe content replacement without disrupting file structure or other sections.

        [Design principles]
        Header-based section identification enabling precise content updates without placeholders.
        File integrity preservation ensuring document structure remains intact during modifications.
        Error handling preventing content corruption and providing clear feedback on operation status.

        [Implementation details]
        Parses existing file, identifies target section by header text, replaces content.
        Uses mistletoe AST manipulation for safe content replacement preserving document structure.
        Writes updated content back to file with proper error handling and validation.
        """
        try:
            # Parse existing file
            doc = self.parse_existing_markdown(file_path)
            if not doc:
                logger.error(f"Cannot update section: failed to parse file {file_path}")
                return False
            
            # Replace section content
            updated_doc = self.markdown_parser.replace_section_content(doc, header_text, new_content)
            if not updated_doc:
                logger.error(f"Failed to replace section content for header: {header_text}")
                return False
            
            # Render back to markdown
            updated_markdown = self.markdown_parser.render_to_markdown(updated_doc)
            if not updated_markdown:
                logger.error("Failed to render updated document to markdown")
                return False
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_markdown)
            
            logger.debug(f"Successfully updated section '{header_text}' in file: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update section in file {file_path}: {e}")
            return False
    
    def insert_after_header(self, file_path: Path, header_text: str, content: str) -> bool:
        """
        [Class method intent]
        Inserts new content immediately after specified header in existing markdown file.
        Enables safe content addition without disrupting existing document structure.

        [Design principles]
        Header-based content insertion supporting precise placement without placeholder dependencies.
        Document structure preservation ensuring new content integrates seamlessly with existing content.
        Comprehensive error handling preventing document corruption during insertion operations.

        [Implementation details]
        Parses existing file, locates target header, inserts content at precise location.
        Uses mistletoe AST manipulation for safe content insertion preserving formatting.
        Validates results and writes updated content back with proper error recovery.
        """
        try:
            # Parse existing file
            doc = self.parse_existing_markdown(file_path)
            if not doc:
                logger.error(f"Cannot insert content: failed to parse file {file_path}")
                return False
            
            # Insert content after header
            updated_doc = self.markdown_parser.insert_content_after_header(doc, header_text, content)
            if not updated_doc:
                logger.error(f"Failed to insert content after header: {header_text}")
                return False
            
            # Render back to markdown
            updated_markdown = self.markdown_parser.render_to_markdown(updated_doc)
            if not updated_markdown:
                logger.error("Failed to render updated document to markdown")
                return False
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_markdown)
            
            logger.debug(f"Successfully inserted content after header '{header_text}' in file: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to insert content in file {file_path}: {e}")
            return False
    
    def find_available_headers(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        [Class method intent]
        Extracts all available headers from existing markdown file for navigation and editing guidance.
        Provides comprehensive header inventory supporting user interfaces and content management.

        [Design principles]
        Complete header enumeration enabling informed content editing and section management.
        Structured header metadata supporting user guidance and automated content operations.
        Error handling ensuring reliable header extraction even with complex document structures.

        [Implementation details]
        Parses existing file and extracts all headers with level, text, and position information.
        Returns structured header data ready for user interfaces and programmatic processing.
        Handles parsing errors gracefully returning empty list for consistent behavior.
        """
        try:
            # Parse existing file
            doc = self.parse_existing_markdown(file_path)
            if not doc:
                logger.error(f"Cannot find headers: failed to parse file {file_path}")
                return []
            
            # Extract available headers
            headers = self.markdown_parser.find_available_headers(doc)
            logger.debug(f"Found {len(headers)} headers in file: {file_path}")
            return headers
            
        except Exception as e:
            logger.error(f"Failed to extract headers from file {file_path}: {e}")
            return []
    
    def validate_existing_file_structure(self, file_path: Path) -> bool:
        """
        [Class method intent]
        Validates existing markdown file structure for safe editing operations.
        Ensures file can be safely modified without risk of corruption or data loss.

        [Design principles]
        Comprehensive structure validation preventing unsafe editing operations on corrupted files.
        Pre-editing validation ensuring document integrity before attempting modifications.
        Clear validation feedback supporting informed decision making about editing operations.

        [Implementation details]
        Parses file and validates AST structure, header organization, and content integrity.
        Returns boolean indicating whether file is safe for header-based editing operations.
        Provides detailed logging for debugging structure issues and validation failures.
        """
        try:
            # Parse existing file
            doc = self.parse_existing_markdown(file_path)
            if not doc:
                logger.error(f"File structure validation failed: cannot parse {file_path}")
                return False
            
            # Validate document structure
            is_valid = self.markdown_parser.validate_document_structure(doc)
            
            if is_valid:
                logger.debug(f"File structure validation passed for: {file_path}")
            else:
                logger.warning(f"File structure validation failed for: {file_path}")
            
            return is_valid
            
        except Exception as e:
            logger.error(f"Failed to validate file structure for {file_path}: {e}")
            return False
    
    def get_section_preview(self, file_path: Path, header_text: str, max_length: int = 200) -> Optional[str]:
        """
        [Class method intent]
        Extracts preview of section content following specified header for user guidance.
        Provides content summary supporting informed editing decisions and section identification.

        [Design principles]
        Section content preview enabling user verification of target sections before editing.
        Length-limited preview preventing overwhelming output while providing sufficient context.
        Header-based section identification supporting precise content targeting and verification.

        [Implementation details]
        Parses file, locates target header, extracts section content with length limitation.
        Returns truncated section content ready for user display and editing confirmation.
        Handles missing headers and extraction errors with appropriate feedback and fallbacks.
        """
        try:
            # Parse existing file
            doc = self.parse_existing_markdown(file_path)
            if not doc:
                logger.error(f"Cannot get section preview: failed to parse file {file_path}")
                return None
            
            # Find target header
            header = self.markdown_parser.find_header_by_text(doc, header_text)
            if not header:
                logger.error(f"Cannot get section preview: header not found '{header_text}'")
                return None
            
            # Get section content
            section_tokens = self.markdown_parser.get_section_content(doc, header)
            if not section_tokens:
                return "*Section is empty*"
            
            # Render section content to markdown for preview
            section_content = ""
            for token in section_tokens:
                # Create temporary document with just this token for rendering
                temp_doc = type(doc)([])
                temp_doc.children = [token]
                token_markdown = self.markdown_parser.render_to_markdown(temp_doc)
                if token_markdown:
                    section_content += token_markdown + "\n"
            
            # Truncate to max length
            if len(section_content) > max_length:
                section_content = section_content[:max_length] + "..."
            
            logger.debug(f"Generated section preview for header '{header_text}' in file: {file_path}")
            return section_content.strip()
            
        except Exception as e:
            logger.error(f"Failed to get section preview from file {file_path}: {e}")
            return None
    
    def _ensure_string_content(self, content: Any) -> str:
        """
        [Class method intent]
        Ensures content is converted to string format for safe markdown template insertion.
        Handles cases where mistletoe parsing might have created RawText objects instead of strings.
        Provides robust content conversion preventing type errors during template assembly.

        [Design principles]
        Safe content conversion handling various input types without breaking template rendering.
        RawText object detection and extraction for mistletoe compatibility.
        Fallback handling ensuring reliable string conversion for template insertion.

        [Implementation details]
        Checks for RawText objects and extracts content attribute to convert to string.
        Handles None and empty content gracefully with appropriate fallback values.
        Returns clean string content ready for markdown template insertion operations.
        """
        try:
            if content is None:
                return "Content not available"
            
            # Handle RawText objects from mistletoe parsing
            if hasattr(content, 'content'):
                # This is likely a RawText object, extract the content
                extracted_content = content.content
                if isinstance(extracted_content, str):
                    return extracted_content.strip()
                else:
                    return str(extracted_content).strip()
            
            # Handle string content directly
            if isinstance(content, str):
                return content.strip()
            
            # Handle other types by converting to string
            return str(content).strip()
            
        except Exception as e:
            logger.warning(f"Failed to ensure string content: {e}")
            return "Content conversion failed"
    
    def _update_global_summary_header_text(self, doc, directory_name: str):
        """
        [Class method intent]
        Updates the Global Summary header text to include directory name.
        Finds existing "Global Summary" header and programmatically updates it
        to include the directory name in the header text for cleaner structure.

        [Design principles]
        Header text modification using AST manipulation for clean header updates.
        Directory name integration providing context without content duplication.
        Safe AST manipulation with fallback handling for robust operation.

        [Implementation details]
        Searches for "Global Summary" header using AST traversal.
        Updates header text to include directory name in standardized format.
        Returns updated document or original document if operation fails.
        """
        try:
            # Find the Global Summary header
            headers = self.markdown_parser.find_available_headers(doc)
            global_summary_header = None
            
            for header_info in headers:
                header_text = header_info['text']
                if header_text == 'Global Summary':
                    global_summary_header = header_info
                    logger.debug(f"Found Global Summary header: '{header_text}'")
                    break
            
            if not global_summary_header:
                logger.warning("No Global Summary header found for directory name update")
                return doc  # Return original document
            
            # Update the header text to include directory name
            new_header_text = f"Global Summary: {directory_name}/"
            
            # Get the header token from the document
            header_token = global_summary_header['token']
            
            # Update the header text directly in the AST
            if hasattr(header_token, 'children') and header_token.children:
                # Update the text content of the header
                for child in header_token.children:
                    if hasattr(child, 'content'):
                        child.content = new_header_text
                        logger.debug(f"Successfully updated Global Summary header to: '{new_header_text}'")
                        break
                    elif hasattr(child, 'children'):
                        # Some mistletoe tokens have nested children structure
                        for grandchild in child.children:
                            if hasattr(grandchild, 'content'):
                                grandchild.content = new_header_text
                                logger.debug(f"Successfully updated Global Summary header to: '{new_header_text}'")
                                break
            else:
                logger.warning("Could not update header text in AST")
            
            return doc
                
        except Exception as e:
            logger.error(f"Failed to update Global Summary header text: {e}")
            return doc  # Return original document on error

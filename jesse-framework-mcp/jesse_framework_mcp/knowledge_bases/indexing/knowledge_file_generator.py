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
# Knowledge file generator for Knowledge Bases Hierarchical Indexing System.
# Provides full rebuild approach with alphabetical sorting, replacing complex incremental
# updates with straightforward template generation from complete content.
###############################################################################
# [Source file design principles]
# - Full rebuild: generate complete knowledge files from template on every change
# - Alphabetical sorting: sort files and subdirectories consistently across all knowledge files
# - Template-based generation: use string templates for predictable, debuggable output
# - Timestamp-based change detection: use three-trigger system for comprehensive change detection
# - Performance through simplicity: eliminate complex incremental update logic
###############################################################################
# [Source file constraints]
# - Generated markdown must be parseable by standard Python markdown libraries
# - Content insertion must preserve LLM formatting without transformation
# - All markdown formatting must follow CommonMark specification for maximum compatibility
# - Template generation must be deterministic and reproducible
# - Alphabetical sorting must be case-insensitive and consistent across platforms
###############################################################################
# [Dependencies]
# <codebase>: ..models.knowledge_context - Context structures and file metadata
# <codebase>: ...helpers.path_utils - Cross-platform path operations and portable paths
# <system>: pathlib - Cross-platform path operations and metadata handling
# <system>: datetime - Timestamp formatting for knowledge file metadata
# <system>: typing - Type hints for template parameters and content structures
###############################################################################
# [GenAI tool change history]
# 2025-07-04T15:27:00Z : Initial implementation of simple template generator by CodeAssistant
# * Created complete replacement for complex incremental markdown engine
# * Implemented three-trigger timestamp-based change detection system
# * Added alphabetical sorting for files and subdirectories in all templates
# * Implemented full rebuild approach with string-based template generation
###############################################################################

"""
Knowledge File Generator for Knowledge Bases System.

This module provides straightforward template-based knowledge file generation using
full rebuild approach with alphabetical sorting and timestamp-based change detection.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from ..models.knowledge_context import FileContext, DirectoryContext
from ...helpers.path_utils import get_portable_path

logger = logging.getLogger(__name__)


class KnowledgeFileGenerator:
    """
    [Class intent]
    Knowledge file generator for complete knowledge base file generation using full rebuild approach.
    Replaces complex incremental updates with straightforward template generation, alphabetical sorting,
    and comprehensive timestamp-based change detection for reliable and maintainable knowledge file creation.

    [Design principles]
    Full rebuild approach: generate complete knowledge files from template on every change.
    Alphabetical sorting: consistent file and subdirectory ordering across all knowledge files.
    Template-based generation: predictable, debuggable output using string templates.
    Timestamp-based change detection: three-trigger system for comprehensive change detection.
    Performance through simplicity: eliminate complex parsing and section replacement logic.

    [Implementation details]
    Uses string templates for complete knowledge file generation with deterministic output.
    Implements three-trigger timestamp comparison for change detection and rebuild decisions.
    Sorts all content alphabetically before template generation for consistent output.
    Preserves LLM formatting through direct content insertion without transformation.
    Provides clear logging and error handling for debugging and maintenance.
    """
    
    def __init__(self):
        """
        [Class method intent]
        Initializes simple template generator with logging and configuration setup.
        Sets up template generation capabilities without complex parsing dependencies.

        [Design principles]
        Minimal initialization focusing on template generation rather than parsing complexity.
        Clear logging setup for debugging template generation and change detection operations.
        No complex dependencies or initialization requirements for maximum reliability.

        [Implementation details]
        Sets up logging for template generation operations and change detection.
        No parser initialization or complex configuration required.
        Ready for immediate template generation operations.
        """
        logger.info("KnowledgeFileGenerator initialized with full rebuild approach")
    
    def directory_needs_rebuild(self, directory_path: Path, kb_file_path: Path) -> Tuple[bool, str]:
        """
        [Class method intent]
        Implements three-trigger timestamp-based change detection for comprehensive rebuild decisions.
        Checks directory structure changes, individual file changes, and subdirectory KB changes
        to determine if directory knowledge base file needs complete rebuild.

        [Design principles]
        Three-trigger system: directory mtime, source file mtime, subdirectory KB mtime comparisons.
        Comprehensive change detection: catch all possible change scenarios with simple timestamp logic.
        Fast filesystem operations: use stat() calls for efficient change detection.
        Clear reasoning: return specific reason for rebuild decision to aid debugging.

        [Implementation details]
        Compares directory, source files, and subdirectory KB timestamps against KB file timestamp.
        Returns tuple with rebuild decision and human-readable reason for logging.
        Handles missing KB files, filesystem errors, and edge cases gracefully.
        Uses case-insensitive file extension filtering for cross-platform compatibility.
        """
        try:
            if not kb_file_path.exists():
                return True, "KB file doesn't exist"
            
            kb_timestamp = kb_file_path.stat().st_mtime
            
            # TRIGGER 1: Directory structure changed (files added/deleted/renamed)
            dir_timestamp = directory_path.stat().st_mtime
            if dir_timestamp > kb_timestamp:
                return True, f"Directory structure changed (dir: {dir_timestamp:.2f} > kb: {kb_timestamp:.2f})"
            
            # TRIGGER 2: Source file content changed
            for source_file in directory_path.iterdir():
                if self._should_process_file(source_file):
                    file_timestamp = source_file.stat().st_mtime
                    if file_timestamp > kb_timestamp:
                        return True, f"Source file changed: {source_file.name} ({file_timestamp:.2f} > {kb_timestamp:.2f})"
            
            # TRIGGER 3: Subdirectory KB changed
            for subdir in directory_path.iterdir():
                if subdir.is_dir():
                    subdir_kb = self._get_kb_path(subdir)
                    if subdir_kb.exists():
                        subdir_kb_timestamp = subdir_kb.stat().st_mtime
                        if subdir_kb_timestamp > kb_timestamp:
                            return True, f"Subdirectory KB changed: {subdir.name} ({subdir_kb_timestamp:.2f} > {kb_timestamp:.2f})"
            
            return False, "No changes detected"
            
        except Exception as e:
            logger.error(f"Change detection failed for {directory_path}: {e}")
            return True, f"Change detection error: {e}"
    
    def generate_complete_knowledge_file(
        self,
        directory_path: Path,
        global_summary: str,
        file_contexts: List[FileContext],
        subdirectory_summaries: List[Tuple[Path, str]],
        kb_file_path: Path
    ) -> str:
        """
        [Class method intent]
        Generates complete knowledge base file using template approach with alphabetical sorting.
        Creates entire knowledge file content from components with consistent structure,
        sorted content, and proper metadata for reliable knowledge base generation.

        [Design principles]
        Complete template generation: create entire file content in single operation.
        Alphabetical sorting: consistent ordering of files and subdirectories.
        Template-based structure: predictable, maintainable knowledge file format.
        Content preservation: maintain LLM formatting without transformation.

        [Implementation details]
        Sorts file contexts and subdirectory summaries alphabetically before template generation.
        Uses string template approach for predictable output structure.
        Preserves LLM content formatting through direct insertion without parsing.
        Generates complete metadata footer with accurate counts and timestamps.
        Returns complete knowledge file content ready for writing to filesystem.
        """
        try:
            # Sort content alphabetically for consistent output
            sorted_files = sorted(file_contexts, key=lambda f: f.file_path.name.lower())
            sorted_subdirs = sorted(subdirectory_summaries, key=lambda s: s[0].name.lower())
            
            # Generate template content
            content_parts = []
            
            # Warning header
            content_parts.append(self._generate_warning_header())
            
            # Main title with portable path
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
                title_path = f"{directory_path.name}/"
            
            content_parts.append(f"# Directory Knowledge Base {title_path}")
            
            # Global Summary section
            content_parts.append("\n## Global Summary")
            if global_summary and global_summary.strip():
                content_parts.append(f"\n{global_summary.strip()}")
            else:
                content_parts.append("\n*Global summary not available*")
            
            # Subdirectory Knowledge Integration section
            content_parts.append("\n## Subdirectory Knowledge Integration")
            if sorted_subdirs:
                for subdir_path, subdir_summary in sorted_subdirs:
                    content_parts.append(self._generate_subdirectory_section(subdir_path, subdir_summary))
            else:
                content_parts.append("\n*No subdirectories processed*")
            
            # File Knowledge Integration section
            content_parts.append("\n## File Knowledge Integration")
            if sorted_files:
                for file_context in sorted_files:
                    if file_context.knowledge_content:
                        content_parts.append(self._generate_file_section(file_context))
            else:
                content_parts.append("\n*No files processed*")
            
            # Metadata footer
            content_parts.append(self._generate_metadata_footer(
                directory_path=directory_path,
                file_count=len(sorted_files),
                subdirectory_count=len(sorted_subdirs),
                kb_file_path=kb_file_path
            ))
            
            complete_content = "\n".join(content_parts)
            logger.debug(f"Generated complete knowledge file: {len(complete_content)} characters")
            return complete_content
            
        except Exception as e:
            logger.error(f"Complete knowledge file generation failed for {directory_path}: {e}")
            raise RuntimeError(f"Template generation failed: {e}") from e
    
    def _generate_warning_header(self) -> str:
        """
        [Class method intent]
        Generates consistent warning header for all knowledge files to prevent manual editing.
        Provides clear notice that files are automatically generated and manual edits will be overwritten.

        [Design principles]
        Consistent warning across all generated files for user clarity.
        Prominent formatting to ensure visibility and understanding.
        Clear instructions on proper modification procedures.

        [Implementation details]
        Returns raw HTML comment text for direct insertion into markdown content.
        Uses prominent emoji and formatting for maximum visibility.
        Simple string approach avoiding unnecessary complexity.
        """
        return ("<!-- ⚠️ DO NOT EDIT MANUALLY! DOCUMENT AUTOMATICALLY GENERATED! ⚠️ -->\n"
                "<!-- This file is automatically generated by the JESSE Knowledge Base system. -->\n"
                "<!-- Manual edits will be overwritten during the next generation cycle. -->\n"
                "<!-- To modify content, update the source files and regenerate the knowledge base. -->")
    
    def _generate_subdirectory_section(self, subdir_path: Path, subdir_summary: str) -> str:
        """
        [Class method intent]
        Generates formatted subdirectory section with portable path header and timestamp.
        Creates consistent subdirectory section format with extracted content from subdirectory KB.

        [Design principles]
        Consistent section formatting across all subdirectory entries.
        Portable path headers for cross-platform compatibility.
        Timestamp tracking for content freshness indication.
        Content preservation maintaining original formatting from source KB.

        [Implementation details]
        Uses portable path conversion with trailing slash for directory indication.
        Adds timestamp for content tracking and freshness indication.
        Preserves subdirectory summary content without transformation.
        Returns formatted section ready for template insertion.
        """
        try:
            # Create portable path with trailing slash
            try:
                portable_path = get_portable_path(subdir_path)
                if not portable_path.endswith('/') and not portable_path.endswith('\\'):
                    if len(portable_path) >= 3 and portable_path[1:3] == ':\\':
                        portable_path += "\\"
                    else:
                        portable_path += "/"
            except Exception as e:
                logger.warning(f"Failed to get portable path for {subdir_path}: {e}")
                portable_path = f"{subdir_path.name}/"
            
            timestamp = self._generate_timestamp()
            
            section_content = [
                f"\n### {portable_path}",
                f"\n*Last Updated: {timestamp}*",
                f"\n\n{subdir_summary.strip()}" if subdir_summary.strip() else "\n\n*No content available*"
            ]
            
            return "".join(section_content)
            
        except Exception as e:
            logger.error(f"Subdirectory section generation failed for {subdir_path}: {e}")
            return f"\n### {subdir_path.name}/\n\n*Error generating section: {e}*"
    
    def _generate_file_section(self, file_context: FileContext) -> str:
        """
        [Class method intent]
        Generates formatted file section with portable path header and analysis content.
        Creates consistent file section format with LLM-generated analysis content preservation.

        [Design principles]
        Consistent section formatting across all file entries.
        Portable path headers for cross-platform compatibility.
        Timestamp tracking for analysis freshness indication.
        Content preservation maintaining LLM analysis formatting without transformation.

        [Implementation details]
        Uses portable path conversion for file path headers.
        Adds timestamp for analysis tracking and freshness indication.
        Preserves file analysis content without transformation or parsing.
        Returns formatted section ready for template insertion.
        """
        try:
            # Create portable path for file
            try:
                portable_path = get_portable_path(file_context.file_path)
            except Exception as e:
                logger.warning(f"Failed to get portable path for {file_context.file_path}: {e}")
                portable_path = str(file_context.file_path)
            
            timestamp = self._generate_timestamp()
            
            section_content = [
                f"\n### {portable_path}",
                f"\n\n*Last Updated: {timestamp}*",
                f"\n\n{file_context.knowledge_content.strip()}" if file_context.knowledge_content else "\n\n*No analysis available*"
            ]
            
            return "".join(section_content)
            
        except Exception as e:
            logger.error(f"File section generation failed for {file_context.file_path}: {e}")
            return f"\n### {file_context.file_path.name}\n\n*Error generating section: {e}*"
    
    def _generate_metadata_footer(self, directory_path: Path, file_count: int, subdirectory_count: int, kb_file_path: Path) -> str:
        """
        [Class method intent]
        Generates complete metadata footer with generation timestamp, counts, and file identification.
        Creates consistent footer format with portable paths and accurate statistics.

        [Design principles]
        Comprehensive metadata tracking for knowledge file management.
        Portable path usage for cross-platform compatibility.
        Accurate count reporting for content verification.
        Consistent footer format across all knowledge files.

        [Implementation details]
        Includes generation timestamp, source directory, file counts, and subdirectory counts.
        Uses portable path conversion for source directory identification.
        Adds knowledge file name indication for easy identification.
        Returns formatted footer ready for template insertion.
        """
        try:
            timestamp = self._generate_timestamp()
            
            footer_lines = [
                "\n---",
                f"*Generated: {timestamp}*"
            ]
            
            # Add source directory with portable path
            try:
                portable_dir_path = get_portable_path(directory_path)
            except Exception as e:
                logger.warning(f"Failed to get portable path for directory {directory_path}: {e}")
                portable_dir_path = str(directory_path)
            
            footer_lines.append(f"*Source Directory: {portable_dir_path}*")
            footer_lines.append(f"*Total Files: {file_count}*")
            footer_lines.append(f"*Total Subdirectories: {subdirectory_count}*")
            
            # Add knowledge file identifier
            kb_filename = kb_file_path.name
            footer_lines.append(f"\n# End of {kb_filename}")
            
            return "\n".join(footer_lines)
            
        except Exception as e:
            logger.error(f"Metadata footer generation failed: {e}")
            return f"\n---\n*Generated: {self._generate_timestamp()}*\n*Error generating metadata: {e}*"
    
    def _generate_timestamp(self) -> str:
        """
        [Class method intent]
        Generates timestamp in JESSE framework standard format for content tracking.
        Provides consistent timestamp formatting across all knowledge base content.

        [Design principles]
        Standardized timestamp format for consistency across framework.
        UTC timezone usage for universal compatibility.
        ISO 8601 format for maximum interoperability.

        [Implementation details]
        Uses datetime.utcnow() with ISO format for standardized timestamp generation.
        Returns formatted timestamp string ready for insertion into content.
        """
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    def _should_process_file(self, file_path: Path) -> bool:
        """
        [Class method intent]
        Determines if file should be processed based on extension and characteristics.
        Filters out binary files, system files, and other non-processable content.

        [Design principles]
        Selective file processing to focus on relevant source code and documentation.
        Extension-based filtering for reliable file type detection.
        Cross-platform compatibility with case-insensitive extension checking.

        [Implementation details]
        Checks file extensions against processable types (source code, documentation).
        Excludes binary files, system files, and temporary files.
        Uses case-insensitive comparison for cross-platform compatibility.
        """
        if not file_path.is_file():
            return False
        
        # Get file extension in lowercase for comparison
        ext = file_path.suffix.lower()
        
        # Processable file extensions
        processable_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h',
            '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.scala',
            '.md', '.txt', '.json', '.yaml', '.yml', '.xml', '.toml', '.cfg',
            '.ini', '.conf', '.sh', '.bat', '.ps1', '.sql', '.html', '.css',
            '.scss', '.less', '.vue', '.svelte', '.r', '.m', '.mm', '.pl',
            '.lua', '.dart', '.elm', '.fs', '.clj', '.hs', '.ex', '.exs'
        }
        
        return ext in processable_extensions
    
    def _get_kb_path(self, directory_path: Path) -> Path:
        """
        [Class method intent]
        Generates knowledge base file path for given directory following naming conventions.
        Creates consistent KB file naming and location patterns.

        [Design principles]
        Consistent KB file naming across all directories.
        Standard naming convention with _kb.md suffix.
        Directory-adjacent placement for easy discovery.

        [Implementation details]
        Creates KB filename using directory name with _kb.md suffix.
        Places KB file in same parent directory as source directory.
        Returns Path object ready for filesystem operations.
        """
        kb_filename = f"{directory_path.name}_kb.md"
        return directory_path.parent / kb_filename

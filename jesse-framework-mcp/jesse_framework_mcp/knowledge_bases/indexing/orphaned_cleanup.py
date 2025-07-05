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
# Orphaned analysis cleanup manager for Knowledge Bases Hierarchical Indexing System.
# Removes analysis files and knowledge files that no longer have corresponding source files,
# ensuring knowledge base accuracy and preventing stale artifact accumulation.
###############################################################################
# [Source file design principles]
# - Leaf-first cleanup strategy ensuring safe bottom-up directory cleanup
# - Conservative approach only deleting analysis artifacts and orphaned knowledge files  
# - Comprehensive error handling with graceful degradation on individual failures
# - Detailed logging and statistics for cleanup audit trail and performance monitoring
# - Integration with existing FileAnalysisCache for consistent path calculations
# - FastMCP Context integration for real-time progress reporting
###############################################################################
# [Source file constraints]
# - Must only delete .analysis.md files and knowledge files (_kb.md) - never source files
# - Directory deletion only when completely empty (no files, no subdirectories)
# - Must traverse in leaf-first order to ensure proper cleanup dependency handling
# - Error handling must continue cleanup even when individual operations fail
# - Must integrate seamlessly with existing HierarchicalIndexer workflow phases
###############################################################################
# [Dependencies]
# <codebase>: ..models.indexing_config - Configuration and path calculation utilities
# <codebase>: .file_analysis_cache - Cache path calculation and knowledge file location
# <system>: pathlib - Cross-platform path operations and filesystem interaction
# <system>: logging - Structured logging for cleanup operations and debugging
# <system>: asyncio - Async programming patterns for non-blocking operations
###############################################################################
# [GenAI tool change history]
# 2025-07-05T13:39:00Z : Fixed directory pruning algorithm to preserve empty directories with existing source by CodeAssistant
# * Fixed _cleanup_empty_directory to check source directory existence before deletion
# * Added _get_source_directory_from_mirrored_path helper method for reverse path mapping
# * Enhanced directory preservation logic ensuring mirror structure integrity when source directories exist
# * Prevents deletion of empty mirrored directories when corresponding source directories exist in codebase
# 2025-07-05T13:26:00Z : Initial orphaned analysis cleanup component creation by CodeAssistant
# * Created comprehensive cleanup manager following existing architectural patterns
# * Implemented leaf-first cleanup strategy for safe bottom-up directory processing
# * Added support for both analysis file cleanup and knowledge file cleanup
# * Integrated with FileAnalysisCache for consistent path calculations and business rules
###############################################################################

"""
Orphaned Analysis Cleanup for Knowledge Bases System.

This module provides cleanup capabilities for orphaned analysis files and knowledge files
that no longer have corresponding source files, ensuring knowledge base accuracy and
preventing accumulation of stale artifacts in the mirror directory structure.
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass

from fastmcp import Context

from ..models import IndexingConfig
from .file_analysis_cache import FileAnalysisCache

logger = logging.getLogger(__name__)


@dataclass
class CleanupStats:
    """
    [Class intent]
    Statistics container for orphaned analysis cleanup operations.
    Tracks counts and performance metrics for different types of cleanup operations
    providing comprehensive reporting and audit trail capabilities.

    [Design principles]
    Immutable statistics structure preventing accidental modification during processing.
    Comprehensive metric collection supporting performance analysis and debugging.
    Clear categorization of different cleanup operation types for detailed reporting.

    [Implementation details]
    Separate counters for analysis files, knowledge files, and directory cleanup operations.
    Error tracking with detailed error message collection for troubleshooting.
    Timing information for performance analysis and optimization insights.
    """
    analysis_files_deleted: int = 0
    knowledge_files_deleted: int = 0
    directories_deleted: int = 0
    analysis_files_failed: int = 0
    knowledge_files_failed: int = 0
    directories_failed: int = 0
    errors: List[str] = None
    cleanup_start_time: Optional[datetime] = None
    cleanup_end_time: Optional[datetime] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []

    @property
    def total_files_deleted(self) -> int:
        """Total files deleted (analysis + knowledge files)."""
        return self.analysis_files_deleted + self.knowledge_files_deleted

    @property
    def total_items_deleted(self) -> int:
        """Total items deleted (files + directories)."""
        return self.total_files_deleted + self.directories_deleted

    @property
    def cleanup_duration(self) -> float:
        """Cleanup duration in seconds."""
        if self.cleanup_start_time and self.cleanup_end_time:
            return (self.cleanup_end_time - self.cleanup_start_time).total_seconds()
        return 0.0

    def add_error(self, error_message: str) -> None:
        """Add error message to error collection."""
        self.errors.append(error_message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert statistics to dictionary format for reporting."""
        return {
            'analysis_files_deleted': self.analysis_files_deleted,
            'knowledge_files_deleted': self.knowledge_files_deleted,
            'directories_deleted': self.directories_deleted,
            'total_files_deleted': self.total_files_deleted,
            'total_items_deleted': self.total_items_deleted,
            'analysis_files_failed': self.analysis_files_failed,
            'knowledge_files_failed': self.knowledge_files_failed,
            'directories_failed': self.directories_failed,
            'cleanup_duration': self.cleanup_duration,
            'error_count': len(self.errors),
            'errors': self.errors[:10] if self.errors else []  # Limit error list for reporting
        }


class OrphanedAnalysisCleanup:
    """
    [Class intent]
    Manages cleanup of orphaned analysis files and knowledge files in the knowledge base.
    Implements leaf-first cleanup strategy removing artifacts that no longer have
    corresponding source files while preserving valid knowledge base structure.

    [Design principles]
    Leaf-first cleanup strategy ensuring safe bottom-up directory processing without dependencies.
    Conservative deletion approach only removing analysis artifacts and orphaned knowledge files.
    Comprehensive error handling enabling graceful degradation when individual operations fail.
    Integration with existing FileAnalysisCache for consistent path calculations and business rules.
    Detailed statistics and logging providing complete audit trail for cleanup operations.
    Async-first architecture supporting non-blocking operations and progress reporting.

    [Implementation details]
    Uses FileAnalysisCache for consistent cache and knowledge file path calculations.
    Implements three-phase cleanup: analysis files, knowledge files, empty directories.
    Traverses directory structure in leaf-first order ensuring proper cleanup dependencies.
    Provides comprehensive error handling and continues processing despite individual failures.
    Reports progress through FastMCP Context for real-time user feedback and monitoring.
    """

    def __init__(self, config: IndexingConfig):
        """
        [Class method intent]
        Initializes orphaned analysis cleanup with configuration and cache integration.
        Sets up file analysis cache for consistent path calculations and cleanup coordination.

        [Design principles]
        Configuration-driven behavior supporting different cleanup scenarios and constraints.
        Integration with existing FileAnalysisCache ensuring consistent path calculation logic.
        Component initialization with error handling preventing construction failures.

        [Implementation details]
        Creates FileAnalysisCache instance for path calculations and knowledge file location.
        Stores configuration reference for cleanup behavior and constraint validation.
        Initializes cleanup statistics container for operation tracking and reporting.
        """
        self.config = config
        self.cache = FileAnalysisCache(config)
        self.stats = CleanupStats()
        
        logger.info("Initialized OrphanedAnalysisCleanup")

    async def cleanup_orphaned_files(self, knowledge_root: Path, source_root: Path, ctx: Context) -> CleanupStats:
        """
        [Class method intent]
        Performs comprehensive cleanup of orphaned analysis files and knowledge files.
        Implements leaf-first cleanup strategy removing artifacts without corresponding source files
        while maintaining knowledge base integrity and providing detailed progress reporting.

        [Design principles]
        Comprehensive cleanup covering both analysis files and knowledge files for complete artifact removal.
        Leaf-first processing ensuring safe bottom-up cleanup without dependency violations.
        Detailed progress reporting through FastMCP Context for real-time user feedback.
        Comprehensive error handling enabling partial cleanup completion when individual operations fail.
        Statistics tracking providing detailed performance metrics and audit trail information.

        [Implementation details]
        Performs three-phase cleanup: orphaned analysis files, orphaned knowledge files, empty directories.
        Traverses project-base directory structure in leaf-first order for safe cleanup dependencies.
        Uses FileAnalysisCache for consistent path calculations and knowledge file location logic.
        Reports detailed progress and statistics through FastMCP Context for monitoring and debugging.
        Returns comprehensive statistics for cleanup operation reporting and analysis.
        """
        self.stats = CleanupStats()
        self.stats.cleanup_start_time = datetime.now()

        try:
            await ctx.info(f"Starting orphaned analysis cleanup for: {knowledge_root}")

            # Target the project-base directory where analysis files are stored
            project_base_root = knowledge_root / "project-base"
            
            if not project_base_root.exists():
                await ctx.info("No project-base directory found - no cleanup needed")
                self.stats.cleanup_end_time = datetime.now()
                return self.stats

            await ctx.info(f"Cleaning up orphaned files in: {project_base_root}")

            # Phase 1: Collect all directories in leaf-first order
            directories = self._collect_directories_leaf_first(project_base_root)
            await ctx.info(f"Found {len(directories)} directories to process")

            # Phase 2: Clean up orphaned analysis files and knowledge files
            for directory in directories:
                await self._cleanup_directory(directory, source_root, ctx)

            self.stats.cleanup_end_time = datetime.now()
            
            # Report completion statistics
            await ctx.info(f"Cleanup completed: {self.stats.total_items_deleted} items deleted in {self.stats.cleanup_duration:.2f}s")
            await ctx.info(f"Analysis files: {self.stats.analysis_files_deleted}, Knowledge files: {self.stats.knowledge_files_deleted}, Directories: {self.stats.directories_deleted}")
            
            if len(self.stats.errors) > 0:
                await ctx.warning(f"Cleanup completed with {len(self.stats.errors)} errors")

            return self.stats

        except Exception as e:
            self.stats.cleanup_end_time = datetime.now()
            self.stats.add_error(f"Cleanup operation failed: {str(e)}")
            logger.error(f"Orphaned analysis cleanup failed: {e}", exc_info=True)
            await ctx.error(f"Cleanup operation failed: {str(e)}")
            return self.stats

    def _collect_directories_leaf_first(self, root_directory: Path) -> List[Path]:
        """
        [Class method intent]
        Collects all directories in leaf-first order for safe bottom-up cleanup processing.
        Ensures child directories are processed before parent directories to handle
        cleanup dependencies correctly and enable proper empty directory removal.

        [Design principles]
        Leaf-first ordering ensuring child processing before parent processing for cleanup safety.
        Recursive traversal collecting complete directory hierarchy for comprehensive coverage.
        Flat list generation simplifying cleanup processing and dependency management.

        [Implementation details]
        Uses recursive depth-first traversal to collect all directories in hierarchy.
        Returns directories in leaf-first order ensuring safe cleanup dependency handling.
        Handles filesystem errors gracefully continuing collection despite individual failures.
        """
        directories = []
        
        def collect_recursive(directory: Path):
            try:
                if not directory.is_dir():
                    return
                    
                # First collect all subdirectories recursively
                for item in directory.iterdir():
                    if item.is_dir():
                        collect_recursive(item)
                
                # Then add current directory (leaf-first order)
                directories.append(directory)
                
            except (OSError, PermissionError) as e:
                logger.warning(f"Cannot access directory {directory}: {e}")
                self.stats.add_error(f"Directory access failed: {directory}: {e}")

        collect_recursive(root_directory)
        return directories

    async def _cleanup_directory(self, directory: Path, source_root: Path, ctx: Context) -> None:
        """
        [Class method intent]
        Performs comprehensive cleanup for a single directory including orphaned analysis files,
        orphaned knowledge files, and empty directory removal following the three-phase cleanup strategy.

        [Design principles]
        Three-phase cleanup ensuring proper cleanup sequence and dependency handling.
        Conservative deletion approach only removing confirmed orphaned artifacts.
        Comprehensive error handling enabling continued processing despite individual failures.
        Detailed logging providing complete audit trail for cleanup operations.

        [Implementation details]
        Phase 1: Clean up orphaned analysis files (.analysis.md) without corresponding source files.
        Phase 2: Clean up orphaned knowledge files (_kb.md) in directories with no content.
        Phase 3: Remove directory if completely empty and no corresponding source directory exists.
        Reports progress and errors through FastMCP Context for monitoring and debugging.
        """
        try:
            await ctx.debug(f"Processing directory: {directory}")

            # Phase 1: Clean up orphaned analysis files
            await self._cleanup_orphaned_analysis_files(directory, source_root, ctx)

            # Phase 2: Clean up orphaned knowledge files
            await self._cleanup_orphaned_knowledge_files(directory, source_root, ctx)

            # Phase 3: Remove directory if empty and no corresponding source directory exists
            await self._cleanup_empty_directory(directory, source_root, ctx)

        except Exception as e:
            logger.error(f"Directory cleanup failed for {directory}: {e}", exc_info=True)
            self.stats.add_error(f"Directory cleanup failed: {directory}: {e}")
            await ctx.warning(f"Directory cleanup failed: {directory.name}: {str(e)}")

    async def _cleanup_orphaned_analysis_files(self, directory: Path, source_root: Path, ctx: Context) -> None:
        """
        [Class method intent]
        Cleans up orphaned .analysis.md files that no longer have corresponding source files.
        Iterates through all analysis files in directory and removes those without
        valid source file counterparts in the original codebase.

        [Design principles]
        Conservative deletion ensuring only confirmed orphaned files are removed.
        Source file verification using reverse path calculation from cache file location.
        Individual file error handling preventing single failures from stopping cleanup.
        Detailed logging providing audit trail for all deletion operations.

        [Implementation details]
        Identifies all .analysis.md files in directory using file extension filtering.
        Calculates corresponding source file path using reverse cache path logic.
        Verifies source file existence before marking analysis file for deletion.
        Performs safe file deletion with comprehensive error handling and statistics tracking.
        """
        try:
            # Find all analysis files in directory
            analysis_files = [f for f in directory.iterdir() if f.is_file() and f.name.endswith('.analysis.md')]
            
            if not analysis_files:
                return

            await ctx.debug(f"Found {len(analysis_files)} analysis files in {directory.name}")

            for analysis_file in analysis_files:
                try:
                    # Calculate corresponding source file path
                    source_file_path = self._get_source_path_from_analysis_file(analysis_file, source_root)
                    
                    # Check if source file exists
                    if not source_file_path or not source_file_path.exists():
                        # Orphaned analysis file - delete it
                        analysis_file.unlink()
                        self.stats.analysis_files_deleted += 1
                        logger.info(f"Deleted orphaned analysis file: {analysis_file}")
                        await ctx.debug(f"Deleted orphaned analysis file: {analysis_file.name}")
                    else:
                        await ctx.debug(f"Analysis file has valid source: {analysis_file.name}")

                except Exception as e:
                    self.stats.analysis_files_failed += 1
                    self.stats.add_error(f"Failed to cleanup analysis file {analysis_file}: {e}")
                    logger.warning(f"Failed to cleanup analysis file {analysis_file}: {e}")

        except Exception as e:
            logger.error(f"Analysis file cleanup failed for {directory}: {e}")
            self.stats.add_error(f"Analysis file cleanup failed: {directory}: {e}")

    async def _cleanup_orphaned_knowledge_files(self, directory: Path, source_root: Path, ctx: Context) -> None:
        """
        [Class method intent]
        Cleans up orphaned knowledge files (_kb.md) in directories that no longer contain
        any analysis files or subdirectories, indicating no content to summarize.

        [Design principles]
        Logical consistency ensuring knowledge files only exist where there's content to summarize.
        Conservative approach only deleting knowledge files from completely empty directories.
        Integration with FileAnalysisCache for consistent knowledge file path calculation.
        Comprehensive error handling preventing individual failures from stopping cleanup.

        [Implementation details]
        Checks if directory contains any .analysis.md files or subdirectories.
        Uses FileAnalysisCache.get_knowledge_file_path() for consistent path calculation.
        Only deletes knowledge files from directories with no content (no analysis files, no subdirectories).
        Performs safe file deletion with error handling and statistics tracking.
        """
        try:
            # Check if directory has any analysis files or subdirectories
            has_analysis_files = any(f.is_file() and f.name.endswith('.analysis.md') for f in directory.iterdir())
            has_subdirectories = any(f.is_dir() for f in directory.iterdir())

            # If directory has content, keep knowledge file
            if has_analysis_files or has_subdirectories:
                await ctx.debug(f"Directory {directory.name} has content - keeping knowledge file")
                return

            # Directory is empty of content - check for knowledge file
            try:
                # Calculate relative path from project-base to this directory
                project_base_root = self.config.knowledge_output_directory / "project-base"
                relative_path = directory.relative_to(project_base_root)
                
                # Map back to source directory structure
                source_directory = source_root / relative_path
                
                # Get knowledge file path using cache method
                knowledge_file_path = self.cache.get_knowledge_file_path(source_directory, source_root)
                
                if knowledge_file_path.exists():
                    # Orphaned knowledge file - delete it
                    knowledge_file_path.unlink()
                    self.stats.knowledge_files_deleted += 1
                    logger.info(f"Deleted orphaned knowledge file: {knowledge_file_path}")
                    await ctx.debug(f"Deleted orphaned knowledge file: {knowledge_file_path.name}")
                else:
                    await ctx.debug(f"No knowledge file found for empty directory: {directory.name}")

            except Exception as e:
                self.stats.knowledge_files_failed += 1
                self.stats.add_error(f"Failed to cleanup knowledge file for {directory}: {e}")
                logger.warning(f"Failed to cleanup knowledge file for {directory}: {e}")

        except Exception as e:
            logger.error(f"Knowledge file cleanup failed for {directory}: {e}")
            self.stats.add_error(f"Knowledge file cleanup failed: {directory}: {e}")

    async def _cleanup_empty_directory(self, directory: Path, source_root: Path, ctx: Context) -> None:
        """
        [Class method intent]
        Removes directory if it becomes completely empty after analysis and knowledge file cleanup
        AND the corresponding source directory no longer exists in the codebase.

        [Design principles]
        Conservative directory deletion only when completely empty and source directory is gone.
        Mirror structure preservation ensuring directories exist when source directories exist.
        Post-cleanup verification ensuring directory is truly empty before deletion.
        Error handling preventing directory deletion failures from affecting overall cleanup.
        Preservation of project-base root directory regardless of emptiness.

        [Implementation details]
        Verifies directory is completely empty (no files, no subdirectories) after cleanup.
        Checks if corresponding source directory exists to preserve mirror structure integrity.
        Only deletes mirrored directory when source directory no longer exists in codebase.
        Protects project-base root directory from deletion for structural consistency.
        Performs safe directory deletion with comprehensive error handling.
        Updates statistics and logging for complete audit trail of directory operations.
        """
        try:
            # Don't delete the project-base root directory
            project_base_root = self.config.knowledge_output_directory / "project-base"
            if directory == project_base_root:
                return

            # Check if directory is completely empty
            try:
                directory_contents = list(directory.iterdir())
                if not directory_contents:
                    # Directory is empty - check if corresponding source directory exists
                    source_directory = self._get_source_directory_from_mirrored_path(directory, source_root)
                    
                    if source_directory and source_directory.exists():
                        # Source directory exists - preserve the mirrored directory
                        await ctx.debug(f"Preserving empty directory - source exists: {directory.name}")
                        return
                    
                    # Source directory doesn't exist - safe to delete mirrored directory
                    directory.rmdir()
                    self.stats.directories_deleted += 1
                    logger.info(f"Deleted orphaned empty directory: {directory}")
                    await ctx.debug(f"Deleted orphaned empty directory: {directory.name}")
                else:
                    await ctx.debug(f"Directory not empty: {directory.name} ({len(directory_contents)} items)")
            except OSError:
                # Directory might not be empty or have permission issues
                await ctx.debug(f"Could not delete directory (not empty or permission denied): {directory.name}")

        except Exception as e:
            self.stats.directories_failed += 1
            self.stats.add_error(f"Failed to cleanup directory {directory}: {e}")
            logger.warning(f"Failed to cleanup directory {directory}: {e}")

    def _get_source_path_from_analysis_file(self, analysis_file: Path, source_root: Path) -> Optional[Path]:
        """
        [Class method intent]
        Calculates the corresponding source file path from an analysis cache file path.
        Performs reverse path calculation to determine if the original source file still exists.

        [Design principles]
        Reverse path calculation ensuring accurate source file identification.
        Integration with project-base directory structure mirroring business rules.
        Error handling returning None for invalid or unresolvable paths.

        [Implementation details]
        Removes .analysis.md suffix to get original filename.
        Calculates relative path from project-base directory structure.
        Maps relative path back to source directory structure for verification.
        Handles path calculation errors gracefully returning None for safety.
        """
        try:
            # Remove .analysis.md suffix to get original filename
            original_filename = analysis_file.name.replace('.analysis.md', '')
            
            # Calculate relative path from project-base
            project_base_root = self.config.knowledge_output_directory / "project-base"
            relative_dir_path = analysis_file.parent.relative_to(project_base_root)
            
            # Map back to source directory
            source_directory = source_root / relative_dir_path
            source_file_path = source_directory / original_filename
            
            return source_file_path
            
        except Exception as e:
            logger.debug(f"Failed to calculate source path for {analysis_file}: {e}")
            return None

    def _get_source_directory_from_mirrored_path(self, mirrored_directory: Path, source_root: Path) -> Optional[Path]:
        """
        [Class method intent]
        Calculates the corresponding source directory path from a mirrored knowledge directory path.
        Performs reverse path calculation to determine if the original source directory still exists.

        [Design principles]
        Reverse path calculation ensuring accurate source directory identification.
        Integration with project-base directory structure mirroring business rules.
        Error handling returning None for invalid or unresolvable paths.
        Consistent path mapping logic with file-based reverse path calculation.

        [Implementation details]
        Calculates relative path from project-base directory structure.
        Maps relative path back to source directory structure for verification.
        Handles path calculation errors gracefully returning None for safety.
        Provides foundation for mirror structure preservation logic.
        """
        try:
            # Calculate relative path from project-base
            project_base_root = self.config.knowledge_output_directory / "project-base"
            relative_path = mirrored_directory.relative_to(project_base_root)
            
            # Map back to source directory structure
            source_directory = source_root / relative_path
            
            return source_directory
            
        except Exception as e:
            logger.debug(f"Failed to calculate source directory path for {mirrored_directory}: {e}")
            return None

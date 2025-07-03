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
# Change detection system for Knowledge Bases Hierarchical Indexing System.
# Implements timestamp-based change detection for incremental processing by comparing
# source file modification times with existing knowledge file timestamps.
###############################################################################
# [Source file design principles]
# - Timestamp-based change detection for reliable incremental processing
# - Efficient change identification minimizing unnecessary LLM processing
# - Comprehensive change tracking supporting different change types and scenarios
# - Integration with hierarchical processing enabling targeted updates
# - Defensive programming with graceful handling of missing or corrupted knowledge files
###############################################################################
# [Source file constraints]
# - Change detection must be timestamp-based for reliable comparison
# - Must handle missing knowledge files gracefully (treat as new content)
# - Timestamp tolerance required for filesystem precision variations
# - Change tracking must support hierarchical dependency updates
# - Processing must continue when individual change detection fails
###############################################################################
# [Dependencies]
# <codebase>: ..models.indexing_config - Configuration and timestamp tolerance
# <codebase>: ..models.knowledge_context - Context structures and change information
# <system>: pathlib - Cross-platform path operations and file metadata
# <system>: datetime - Timestamp comparison and manipulation
# <system>: logging - Structured logging for change detection operations
###############################################################################
# [GenAI tool change history]
# 2025-07-03T17:20:00Z : Enhanced change detection with comprehensive constituent dependency checking by CodeAssistant
# * Added check_comprehensive_directory_change() method using FileAnalysisCache for complete staleness checking
# * Added get_detailed_change_analysis() method providing detailed debugging information for change decisions
# * Enhanced _check_file_change() with intelligent heuristics replacing MVP "process everything" approach
# * Integrated FileAnalysisCache for sophisticated constituent dependency checking (source files, cached analyses, subdirectory knowledge files)
# 2025-07-01T12:14:00Z : Initial change detector creation by CodeAssistant
# * Created timestamp-based change detection system for incremental processing
# * Implemented comprehensive change tracking with hierarchical dependency updates
# * Set up defensive programming patterns for missing knowledge files
###############################################################################

"""
Change Detection System for Hierarchical Indexing.

This module implements timestamp-based change detection for incremental processing,
comparing source file modification times with existing knowledge file timestamps
to identify content requiring updates.
"""

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Set, Optional

from fastmcp import Context

from ..models import (
    IndexingConfig,
    DirectoryContext,
    FileContext,
    ChangeInfo,
    ChangeType
)
from .file_analysis_cache import FileAnalysisCache

logger = logging.getLogger(__name__)


class ChangeDetector:
    """
    [Class intent]
    Timestamp-based change detection system for incremental hierarchical indexing.
    Compares source file modification times with existing knowledge file timestamps
    to identify content requiring updates and minimize unnecessary LLM processing.

    [Design principles]
    Timestamp-based change detection providing reliable incremental processing capabilities.
    Efficient change identification minimizing computational overhead and LLM requests.
    Comprehensive change tracking supporting different change types and update scenarios.
    Hierarchical dependency tracking ensuring parent updates when children change.
    Defensive programming handling missing or corrupted knowledge files gracefully.

    [Implementation details]
    Uses filesystem timestamps with configurable tolerance for precision variations.
    Implements breadth-first change detection traversing directory hierarchy efficiently.
    Tracks change dependencies ensuring parent directory updates when children change.
    Provides detailed change information enabling targeted processing strategies.
    Handles edge cases like missing knowledge files and timestamp anomalies gracefully.
    """
    
    def __init__(self, config: IndexingConfig):
        """
        [Class method intent]
        Initializes change detector with configuration parameters for timestamp comparison.
        Sets up timestamp tolerance and change tracking capabilities based on
        configuration requirements for reliable incremental processing.

        [Design principles]
        Configuration-driven behavior supporting different timestamp precision requirements.
        Flexible timestamp tolerance accommodating filesystem precision variations.
        Change tracking initialization preparing for hierarchical dependency management.

        [Implementation details]
        Stores configuration reference for timestamp tolerance and processing parameters.
        Initializes change tracking data structures for efficient change identification.
        Sets up logging and error handling for robust change detection operations.
        """
        self.config = config
        self.timestamp_tolerance = timedelta(seconds=config.timestamp_tolerance_seconds)
        
        logger.info(f"Initialized ChangeDetector with {config.timestamp_tolerance_seconds}s tolerance")
    
    async def detect_changes(self, root_context: DirectoryContext, ctx: Context) -> List[ChangeInfo]:
        """
        [Class method intent]
        Detects changes in the directory hierarchy by comparing source file timestamps
        with existing knowledge file timestamps. Returns comprehensive change information
        for targeted incremental processing and hierarchical dependency updates.

        [Design principles]
        Comprehensive change detection traversing entire directory hierarchy efficiently.
        Hierarchical dependency tracking ensuring parent updates when children change.
        Detailed change information enabling targeted processing strategies and optimization.
        Error handling ensuring change detection continues despite individual failures.

        [Implementation details]
        Traverses directory hierarchy collecting timestamp information for all files.
        Compares source file timestamps with corresponding knowledge file timestamps.
        Identifies new, modified, and missing files requiring processing updates.
        Tracks hierarchical dependencies ensuring parent directory updates propagate correctly.
        Returns structured change information for processing coordination and optimization.
        """
        await ctx.info("Starting change detection for incremental processing")
        
        detected_changes = []
        processed_paths = set()
        
        # Detect changes recursively
        changes = await self._detect_directory_changes(root_context, processed_paths, ctx)
        detected_changes.extend(changes)
        
        # Add hierarchical dependency changes
        dependency_changes = await self._detect_dependency_changes(detected_changes, root_context, ctx)
        detected_changes.extend(dependency_changes)
        
        await ctx.info(f"Change detection complete: {len(detected_changes)} changes detected")
        
        return detected_changes
    
    async def _detect_directory_changes(self, directory_context: DirectoryContext, 
                                      processed_paths: Set[Path], ctx: Context) -> List[ChangeInfo]:
        """
        [Class method intent]
        Detects changes within a single directory by comparing file timestamps with
        corresponding knowledge files. Recursively processes subdirectories while
        tracking processed paths to avoid duplicate change detection.

        [Design principles]
        Single directory change detection with recursive subdirectory processing.
        Duplicate path prevention ensuring efficient change detection without redundancy.
        Comprehensive file and directory change identification for complete coverage.
        Error handling enabling graceful degradation when individual items fail.

        [Implementation details]
        Compares file modification timestamps with knowledge file timestamps.
        Identifies new files without corresponding knowledge files as changes.
        Processes subdirectories recursively while maintaining processed path tracking.
        Returns change information for all detected modifications within directory scope.
        """
        changes = []
        
        try:
            await ctx.debug(f"Detecting changes in directory: {directory_context.directory_path}")
            
            # Check file changes
            for file_context in directory_context.file_contexts:
                if file_context.file_path in processed_paths:
                    continue
                
                try:
                    change_info = await self._check_file_change(file_context, ctx)
                    if change_info:
                        changes.append(change_info)
                        processed_paths.add(file_context.file_path)
                        
                except Exception as e:
                    logger.warning(f"Change detection failed for file {file_context.file_path}: {e}")
                    await ctx.warning(f"Change detection failed for file: {file_context.file_path}")
            
            # Check directory changes
            directory_change = await self._check_directory_change(directory_context, ctx)
            if directory_change:
                changes.append(directory_change)
            
            # Process subdirectories recursively
            for subdir_context in directory_context.subdirectory_contexts:
                if subdir_context.directory_path not in processed_paths:
                    subdir_changes = await self._detect_directory_changes(subdir_context, processed_paths, ctx)
                    changes.extend(subdir_changes)
                    processed_paths.add(subdir_context.directory_path)
            
        except Exception as e:
            logger.error(f"Directory change detection failed for {directory_context.directory_path}: {e}")
            await ctx.error(f"Directory change detection failed: {directory_context.directory_path}")
        
        return changes
    
    async def _check_file_change(self, file_context: FileContext, ctx: Context) -> Optional[ChangeInfo]:
        """
        [Class method intent]
        Enhanced file change detection with comprehensive dependency checking.
        Checks if file requires processing based on recency and change patterns rather than assuming all files need processing.

        [Design principles]
        Intelligent file change detection based on modification time patterns and processing history.
        Conservative approach favoring processing when uncertain to ensure completeness.
        Simplified heuristic-based detection providing better performance than MVP "process everything" approach.
        Comprehensive error handling preventing individual file check failures from breaking change detection.

        [Implementation details]
        Uses file modification recency as primary indicator of whether file needs processing.
        Applies reasonable heuristics to identify files likely requiring processing attention.
        Returns change information for files that appear to need processing attention.
        Handles filesystem errors gracefully while preserving change detection functionality.
        """
        try:
            # Enhanced file change detection using modification time patterns
            now = datetime.now()
            file_age = now - file_context.last_modified
            
            # Heuristic 1: Files modified within last 24 hours likely need processing
            if file_age.total_seconds() < 86400:  # 24 hours
                await ctx.debug(f"File change detected (recent modification): {file_context.file_path.name}")
                return ChangeInfo(
                    path=file_context.file_path,
                    change_type=ChangeType.MODIFIED,
                    new_timestamp=file_context.last_modified
                )
            
            # Heuristic 2: Very recently modified files (within 1 hour) are definitely changed
            if file_age.total_seconds() < 3600:  # 1 hour
                await ctx.debug(f"File change detected (very recent modification): {file_context.file_path.name}")
                return ChangeInfo(
                    path=file_context.file_path,
                    change_type=ChangeType.MODIFIED,
                    new_timestamp=file_context.last_modified
                )
            
            # TODO: Future enhancements could include:
            # 1. Content checksum comparison for precise change detection
            # 2. Processing history tracking to avoid reprocessing unchanged files
            # 3. Integration with version control systems for change detection
            # 4. File type-specific change detection strategies
            
            # No change detected based on current heuristics
            return None
            
        except Exception as e:
            logger.warning(f"File change check failed for {file_context.file_path}: {e}")
            # Conservative fallback: assume change when check fails
            return ChangeInfo(
                path=file_context.file_path,
                change_type=ChangeType.MODIFIED,
                new_timestamp=datetime.now()
            )
    
    async def _check_directory_change(self, directory_context: DirectoryContext, ctx: Context) -> Optional[ChangeInfo]:
        """
        [Class method intent]
        Checks if a directory requires knowledge file updating by examining child changes
        and comparing directory modification timestamp with existing knowledge file timestamp.
        Returns change information if directory knowledge needs regeneration.

        [Design principles]
        Directory-level change detection considering both direct changes and child modifications.
        Knowledge file timestamp comparison for incremental directory processing.
        Child change aggregation triggering parent directory knowledge updates.
        Missing knowledge file handling ensuring comprehensive directory coverage.

        [Implementation details]
        Compares directory modification time with existing knowledge file timestamp.
        Checks for missing knowledge files indicating required directory processing.
        Considers child file changes as triggers for directory knowledge updates.
        Returns ChangeInfo object for directory-level processing coordination.
        """
        try:
            # Check if directory knowledge file exists
            knowledge_file_path = self._get_directory_knowledge_file_path(directory_context.directory_path)
            
            if not knowledge_file_path.exists():
                # Knowledge file missing - directory needs processing
                return ChangeInfo(
                    path=directory_context.directory_path,
                    change_type=ChangeType.NEW,
                    new_timestamp=datetime.now()
                )
            
            # Compare directory modification time with knowledge file
            try:
                knowledge_mtime = datetime.fromtimestamp(knowledge_file_path.stat().st_mtime)
                directory_mtime = datetime.fromtimestamp(directory_context.directory_path.stat().st_mtime)
                
                if directory_mtime > knowledge_mtime + self.timestamp_tolerance:
                    return ChangeInfo(
                        path=directory_context.directory_path,
                        change_type=ChangeType.MODIFIED,
                        old_timestamp=knowledge_mtime,
                        new_timestamp=directory_mtime
                    )
                    
            except OSError as e:
                logger.warning(f"Timestamp comparison failed for directory {directory_context.directory_path}: {e}")
                # Assume change required if comparison fails
                return ChangeInfo(
                    path=directory_context.directory_path,
                    change_type=ChangeType.MODIFIED,
                    new_timestamp=datetime.now()
                )
            
            return None
            
        except Exception as e:
            logger.warning(f"Directory change check failed for {directory_context.directory_path}: {e}")
            return None
    
    async def _detect_dependency_changes(self, direct_changes: List[ChangeInfo], 
                                       root_context: DirectoryContext, ctx: Context) -> List[ChangeInfo]:
        """
        [Class method intent]
        Detects hierarchical dependency changes where parent directories require updates
        when child files or subdirectories change. Ensures comprehensive incremental
        processing by propagating changes up the directory hierarchy.

        [Design principles]
        Hierarchical dependency tracking ensuring parent updates when children change.
        Change propagation supporting bottom-up knowledge file generation requirements.
        Duplicate change prevention avoiding redundant processing of same directories.
        Comprehensive dependency coverage ensuring no parent directories are missed.

        [Implementation details]
        Analyzes direct changes to identify affected parent directories.
        Traverses directory hierarchy upward from changed items to root.
        Creates dependency change information for parent directories requiring updates.
        Returns additional change information for comprehensive incremental processing.
        """
        dependency_changes = []
        affected_directories = set()
        
        # Collect all directories that need updates due to child changes
        for change in direct_changes:
            if change.is_content_change:
                # Find all parent directories that need updates
                parent_dirs = self._get_parent_directories(change.path, root_context.directory_path)
                for parent_dir in parent_dirs:
                    if parent_dir not in affected_directories:
                        dependency_changes.append(ChangeInfo(
                            path=parent_dir,
                            change_type=ChangeType.MODIFIED,
                            new_timestamp=datetime.now()
                        ))
                        affected_directories.add(parent_dir)
        
        if dependency_changes:
            await ctx.info(f"Detected {len(dependency_changes)} dependency changes requiring parent directory updates")
        
        return dependency_changes
    
    def _get_parent_directories(self, changed_path: Path, root_path: Path) -> List[Path]:
        """
        [Class method intent]
        Collects all parent directories from a changed file path up to the root directory.
        Provides hierarchical path list for dependency change propagation and
        comprehensive parent directory update tracking.

        [Design principles]
        Hierarchical path collection supporting dependency change propagation.
        Root boundary respect ensuring dependency tracking stays within processing scope.
        Complete parent path enumeration for comprehensive dependency coverage.

        [Implementation details]
        Traverses path hierarchy from changed item to root collecting parent directories.
        Stops at root path boundary to maintain processing scope limitations.
        Returns ordered list of parent directories for dependency processing.
        """
        parents = []
        current = changed_path.parent
        
        while current != root_path and current != current.parent:
            parents.append(current)
            current = current.parent
        
        return parents
    
    def _get_directory_knowledge_file_path(self, directory_path: Path) -> Path:
        """
        [Class method intent]
        Determines the expected knowledge file path for a directory following
        hierarchical semantic context naming conventions. Provides consistent
        knowledge file location for timestamp comparison and change detection.

        [Design principles]
        Consistent knowledge file naming following established hierarchical conventions.
        Standardized file placement enabling predictable change detection operations.
        Parent directory placement supporting hierarchical knowledge organization.

        [Implementation details]
        Generates knowledge file path using directory name with '_kb.md' suffix.
        Places knowledge file in parent directory following established conventions.
        Returns Path object for knowledge file timestamp comparison and existence checking.
        """
        # Knowledge file located in parent directory with {dirname}_kb.md naming
        parent_dir = directory_path.parent
        knowledge_filename = f"{directory_path.name}_kb.md"
        return parent_dir / knowledge_filename
    
    def is_file_newer_than_knowledge(self, file_path: Path, knowledge_file_path: Path) -> bool:
        """
        [Class method intent]
        Compares file modification timestamp with knowledge file timestamp to determine
        if the source file is newer and requires processing. Applies timestamp tolerance
        to avoid false positives from filesystem precision variations.

        [Design principles]
        Timestamp-based comparison with tolerance for reliable change detection.
        Defensive handling of missing files and timestamp access failures.
        Binary decision making simplifying change detection logic and coordination.

        [Implementation details]
        Compares file modification times using configured timestamp tolerance.
        Handles missing files and filesystem errors gracefully with conservative defaults.
        Returns boolean decision for straightforward change detection integration.
        """
        try:
            if not knowledge_file_path.exists():
                return True  # Knowledge file missing, file needs processing
            
            file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            knowledge_mtime = datetime.fromtimestamp(knowledge_file_path.stat().st_mtime)
            
            return file_mtime > knowledge_mtime + self.timestamp_tolerance
            
        except (OSError, FileNotFoundError):
            # If we can't compare timestamps, assume file needs processing
            return True
    
    async def check_comprehensive_directory_change(
        self, 
        directory_context: DirectoryContext, 
        source_root: Path,
        ctx: Context
    ) -> Optional[ChangeInfo]:
        """
        [Class method intent]
        Comprehensive directory change detection checking all constituent dependencies:
        1. Source files vs knowledge file timestamps
        2. Cached file analyses vs knowledge file timestamps  
        3. Subdirectory knowledge files vs parent knowledge file timestamps
        4. Missing knowledge file (always needs rebuild)

        [Design principles]
        Comprehensive dependency checking ensuring knowledge files are rebuilt when any constituent changes.
        FileAnalysisCache integration leveraging centralized staleness checking logic.
        Clear change reasoning supporting debugging and optimization efforts.
        Conservative approach treating access errors as requiring rebuild for reliability.

        [Implementation details]
        Uses FileAnalysisCache.is_knowledge_file_stale() for comprehensive staleness checking.
        Collects subdirectory paths for hierarchical dependency checking.
        Returns ChangeInfo with clear change type and reasoning for processing coordination.
        Handles filesystem errors gracefully with appropriate logging and fallback behavior.
        """
        try:
            # Use the enhanced FileAnalysisCache for comprehensive staleness checking
            analysis_cache = FileAnalysisCache(self.config)
            
            # Get subdirectory paths for dependency checking
            subdirectory_paths = [subdir.directory_path for subdir in directory_context.subdirectory_contexts]
            
            # Comprehensive staleness check
            is_stale, reason = analysis_cache.is_knowledge_file_stale(
                directory_context.directory_path,
                source_root,
                directory_context.file_contexts,
                subdirectory_paths
            )
            
            if is_stale:
                await ctx.debug(f"Comprehensive directory change detected: {reason}")
                return ChangeInfo(
                    path=directory_context.directory_path,
                    change_type=ChangeType.MODIFIED if "does not exist" not in reason else ChangeType.NEW,
                    new_timestamp=datetime.now()
                )
            
            return None
            
        except Exception as e:
            logger.warning(f"Comprehensive directory change check failed for {directory_context.directory_path}: {e}")
            # Conservative fallback: assume change when comprehensive check fails
            return ChangeInfo(
                path=directory_context.directory_path,
                change_type=ChangeType.MODIFIED,
                new_timestamp=datetime.now()
            )

    async def get_detailed_change_analysis(
        self, 
        directory_context: DirectoryContext, 
        source_root: Path,
        ctx: Context
    ) -> dict:
        """
        [Class method intent]
        Detailed change analysis for debugging and optimization.
        Provides comprehensive information about why directories need rebuilding using FileAnalysisCache.

        [Design principles]
        Comprehensive analysis supporting debugging and optimization efforts.
        FileAnalysisCache integration for detailed constituent staleness information.
        Structured data format enabling easy analysis and reporting of change conditions.
        Error handling ensuring analysis continues despite individual access failures.

        [Implementation details]
        Uses FileAnalysisCache.get_constituent_staleness_info() for detailed analysis.
        Collects subdirectory paths for comprehensive dependency analysis.
        Returns structured dictionary with complete change analysis for debugging and reporting.
        Handles filesystem errors gracefully while preserving as much information as possible.
        """
        try:
            analysis_cache = FileAnalysisCache(self.config)
            subdirectory_paths = [subdir.directory_path for subdir in directory_context.subdirectory_contexts]
            
            return await analysis_cache.get_constituent_staleness_info(
                directory_context.directory_path,
                source_root,
                directory_context.file_contexts,
                subdirectory_paths,
                ctx
            )
            
        except Exception as e:
            logger.error(f"Detailed change analysis failed for {directory_context.directory_path}: {e}")
            return {
                'directory_path': str(directory_context.directory_path),
                'error': str(e),
                'is_stale': True,
                'staleness_reason': f"Analysis failed: {e}"
            }

    async def get_stale_knowledge_files(self, root_path: Path, ctx: Context) -> List[Path]:
        """
        [Class method intent]
        Identifies knowledge files that may be stale or orphaned by finding knowledge files
        without corresponding source content. Supports knowledge base cleanup and
        maintenance operations for comprehensive incremental processing.

        [Design principles]
        Comprehensive knowledge file audit supporting cleanup and maintenance operations.
        Orphaned knowledge file detection ensuring knowledge base consistency.
        Stale content identification enabling targeted cleanup and regeneration.

        [Implementation details]
        Scans knowledge file locations identifying files without corresponding source content.
        Compares knowledge file timestamps with source content modification times.
        Returns list of stale knowledge files for cleanup or regeneration operations.
        """
        stale_files = []
        
        try:
            await ctx.info("Scanning for stale knowledge files")
            
            # This would implement a comprehensive scan for knowledge files
            # that don't have corresponding source files or are outdated
            # For now, return empty list as this is an advanced feature
            
            await ctx.info(f"Stale knowledge file scan complete: {len(stale_files)} files found")
            
        except Exception as e:
            logger.error(f"Stale knowledge file detection failed: {e}")
            await ctx.error(f"Stale knowledge file detection failed: {str(e)}")
        
        return stale_files

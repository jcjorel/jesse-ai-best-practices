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
# Core hierarchical indexing orchestrator for Knowledge Bases Hierarchical Indexing System.
# Implements leaf-first processing strategy for building hierarchical knowledge files
# throughout the .knowledge/ directory structure using bottom-up assembly approach.
###############################################################################
# [Source file design principles]
# - Leaf-first hierarchical processing without parent-to-child context dependencies
# - Bottom-up assembly pattern aggregating child summaries into parent knowledge files
# - Async-first architecture supporting concurrent processing and progress reporting
# - Integration with ChangeDetector and KnowledgeBuilder for modular processing
# - Defensive programming with comprehensive error handling and recovery mechanisms
###############################################################################
# [Source file constraints]
# - Must process directories in leaf-first order ensuring child completion before parent processing
# - All operations must be async and use FastMCP Context for progress reporting
# - Integration with strands_agent_driver required for LLM-powered summarization
# - Error handling must continue processing when individual files fail (configurable)
# - Processing statistics must be accurately maintained throughout the workflow
###############################################################################
# [Dependencies]
# <codebase>: ..models.indexing_config - Configuration and filtering logic
# <codebase>: ..models.knowledge_context - Context structures and processing state
# <codebase>: .change_detector - Change detection and timestamp comparison
# <codebase>: .knowledge_builder - LLM-powered content summarization
# <codebase>: .special_handlers - Git-clone and project-base special handling
# <system>: asyncio - Async programming patterns and concurrency control
# <system>: pathlib - Cross-platform path operations
# <system>: logging - Structured logging and error reporting
###############################################################################
# [GenAI tool change history]
# 2025-07-05T13:29:00Z : Integrated orphaned analysis cleanup component by CodeAssistant
# * Added OrphanedAnalysisCleanup integration for comprehensive knowledge base maintenance
# * Implemented Phase 1.7 orphaned file cleanup after cache structure preparation
# * Added support for cleaning up orphaned analysis files (.analysis.md) and knowledge files (_kb.md)
# * Integrated leaf-first cleanup strategy ensuring safe bottom-up directory processing
# 2025-07-04T16:49:00Z : Implemented complete truncation artifact prevention system by CodeAssistant
# * Updated _process_single_file() to handle None return from KnowledgeBuilder indicating truncated files
# * Modified _process_directory_files() to completely omit truncated files from DirectoryContext file_contexts
# * Added proper logging and statistics tracking for truncated files with no artifact creation
# * Enhanced type hints to Optional[FileContext] reflecting truncation handling behavior
# 2025-07-03T17:57:00Z : Fixed systematic knowledge file rebuilding by integrating comprehensive change detection by CodeAssistant
# * Replaced old _detect_changes() with comprehensive change detection using check_comprehensive_directory_change()
# * Added _apply_comprehensive_change_detection() method for recursive directory evaluation with proper constituent dependency checking
# * Updated directory processing to skip knowledge file generation when processing_status is SKIPPED (up-to-date directories)
# * Integrated enhanced FileAnalysisCache logic eliminating systematic rebuilds when only source files change without cached analysis updates
# 2025-07-01T13:25:00Z : Fixed semaphore deadlock issue by CodeAssistant
# * Moved semaphore usage from directory processing to file processing level
# * Prevented recursive deadlocks in leaf-first directory processing
# * Ensured concurrent file processing without blocking directory traversal
###############################################################################

"""
Hierarchical Indexer for Knowledge Bases System.

This module implements the core orchestrator for hierarchical knowledge base indexing,
coordinating between change detection, content building, and special handling to
maintain structured knowledge files throughout the .knowledge/ directory hierarchy.
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

from fastmcp import Context

from ..models import (
    IndexingConfig, 
    DirectoryContext, 
    FileContext, 
    ProcessingStatus,
    ProcessingStats,
    IndexingStatus
)
from .change_detector import ChangeDetector
from .knowledge_builder import KnowledgeBuilder
from .orphaned_cleanup import OrphanedAnalysisCleanup

logger = logging.getLogger(__name__)


class HierarchicalIndexer:
    """
    [Class intent]
    Core orchestrator for hierarchical knowledge base indexing implementing leaf-first
    processing strategy. Coordinates change detection, content building, and special
    handling to maintain structured knowledge files throughout directory hierarchies.

    [Design principles]
    Leaf-first processing ensuring child contexts are complete before parent processing.
    Bottom-up assembly aggregating child summaries into parent knowledge files.
    Modular architecture delegating specialized tasks to dedicated components.
    Async-first design supporting concurrent operations and real-time progress reporting.
    Defensive error handling enabling graceful degradation and partial processing recovery.

    [Implementation details]
    Uses ChangeDetector for incremental processing and timestamp-based change detection.
    Delegates content summarization to KnowledgeBuilder with strands_agent_driver integration.
    Handles special cases through GitCloneHandler and ProjectBaseHandler components.
    Implements concurrent processing with configurable concurrency limits for performance.
    Provides comprehensive progress reporting through FastMCP Context integration.
    """
    
    def __init__(self, config: IndexingConfig):
        """
        [Class method intent]
        Initializes hierarchical indexer with configuration and component dependencies.
        Sets up change detection, knowledge building, and special handling components
        for coordinated hierarchical processing operations.

        [Design principles]
        Dependency injection pattern enabling testability and component modularity.
        Configuration-driven behavior supporting different processing scenarios.
        Component initialization with error handling preventing construction failures.

        [Implementation details]
        Creates ChangeDetector, KnowledgeBuilder, and special handler components.
        Initializes processing statistics and status tracking structures.
        Sets up concurrency semaphore based on configuration limits.
        """
        self.config = config
        self.change_detector = ChangeDetector(config)
        self.knowledge_builder = KnowledgeBuilder(config)
        self.orphaned_cleanup = OrphanedAnalysisCleanup(config)
        
        # Processing coordination
        self._processing_semaphore = asyncio.Semaphore(config.max_concurrent_operations)
        self._current_status = IndexingStatus()
        
        logger.info(f"Initialized HierarchicalIndexer with config: {config.to_dict()}")
    
    async def index_hierarchy(self, root_path: Path, ctx: Context) -> IndexingStatus:
        """
        [Class method intent]
        Performs complete hierarchical indexing of the specified root directory using
        leaf-first processing strategy. Coordinates change detection, content building,
        and knowledge file generation for the entire directory hierarchy.

        [Design principles]
        Comprehensive hierarchy processing with accurate progress reporting through FastMCP Context.
        Leaf-first processing ensuring bottom-up assembly of hierarchical knowledge files.
        Error recovery enabling partial processing completion when individual components fail.
        Statistics tracking providing detailed performance metrics and operation insights.

        [Implementation details]
        Implements discovery phase for directory structure analysis and file enumeration.
        Uses change detection for incremental processing when configured for efficiency.
        Processes directories in leaf-first order ensuring child completion before parents.
        Integrates special handling for git-clones and project-base scenarios.
        Reports progress through FastMCP Context for real-time user feedback.
        """
        self._current_status = IndexingStatus(
            overall_status=ProcessingStatus.PROCESSING,
            current_operation="Starting hierarchical indexing",
            processing_stats=ProcessingStats()
        )
        
        # Store source root for knowledge file path calculations
        self._source_root = root_path
        
        try:
            # Start timing
            self._current_status.processing_stats.processing_start_time = datetime.now()
            
            await ctx.info(f"Starting hierarchical indexing of: {root_path}")
            
            # Phase 1: Discovery - Build directory structure
            await ctx.info("Phase 1: Discovering directory structure")
            self._current_status.current_operation = "Discovering directory structure"
            
            root_context = await self._discover_directory_structure(root_path, ctx)
            self._current_status.root_directory_context = root_context
            
            # Phase 1.5: Cache Structure Preparation
            await ctx.info("Phase 1.5: Preparing cache directory structure")
            self._current_status.current_operation = "Preparing cache structure"
            await self.knowledge_builder.analysis_cache.prepare_cache_structure(root_context, root_path, ctx)
            
            # Phase 1.7: Orphaned Analysis Cleanup
            await ctx.info("Phase 1.7: Cleaning up orphaned analysis files")
            self._current_status.current_operation = "Cleaning up orphaned files"
            cleanup_stats = await self.orphaned_cleanup.cleanup_orphaned_files(
                self.config.knowledge_output_directory, root_path, ctx
            )
            await ctx.info(f"Cleanup completed: {cleanup_stats.total_items_deleted} items removed")
            
            # Phase 2: Change Detection (conditional based on mode)
            if self.config.indexing_mode.value == "incremental":
                await ctx.info("Phase 2: Detecting changes for incremental processing")
                self._current_status.current_operation = "Detecting changes"
                root_context = await self._detect_changes(root_context, ctx)
                self._current_status.root_directory_context = root_context
            elif self.config.indexing_mode.value == "full_kb_rebuild":
                await ctx.info("Phase 2: Skipping change detection - rebuilding all KB files (with file analysis cache)")
                # No change detection, but individual file analysis still uses cache
            else:  # self.config.indexing_mode.value == "full"
                await ctx.info("Phase 2: Skipping change detection - nuclear rebuild of everything from scratch")
                # No change detection, and file analysis cache will be bypassed
            
            # Phase 3: Leaf-First Processing
            await ctx.info("Phase 3: Processing files and directories (leaf-first)")
            self._current_status.current_operation = "Processing files (leaf-first)"
            
            await self._process_directory_hierarchy(root_context, ctx)
            
            # Complete processing
            self._current_status.processing_stats.processing_end_time = datetime.now()
            self._current_status.overall_status = ProcessingStatus.COMPLETED
            self._current_status.current_operation = "Indexing completed successfully"
            
            duration = self._current_status.processing_stats.processing_duration
            await ctx.info(f"Hierarchical indexing completed in {duration:.2f} seconds")
            
            return self._current_status
            
        except Exception as e:
            self._current_status.overall_status = ProcessingStatus.FAILED
            self._current_status.current_operation = f"Indexing failed: {str(e)}"
            self._current_status.processing_stats.add_error(f"Hierarchy indexing failed: {str(e)}")
            
            logger.error(f"Hierarchical indexing failed: {e}", exc_info=True)
            await ctx.error(f"Hierarchical indexing failed: {str(e)}")
            
            if not self.config.continue_on_file_errors:
                raise
            
            return self._current_status
    
    async def _discover_directory_structure(self, root_path: Path, ctx: Context) -> DirectoryContext:
        """
        [Class method intent]
        Recursively discovers and builds directory structure context for the entire hierarchy.
        Creates DirectoryContext and FileContext objects for all discoverable files and directories
        while respecting configuration filtering rules.

        [Design principles]
        Recursive discovery building complete hierarchy context before processing begins.
        Configuration-driven filtering preventing processing of excluded files and directories.
        Accurate statistics collection enabling progress calculation and performance monitoring.
        Error handling ensuring discovery continues despite individual file access failures.

        [Implementation details]
        Uses configuration filtering methods to exclude unwanted files and directories.
        Builds FileContext objects with metadata for all discoverable files.
        Creates nested DirectoryContext structure mirroring filesystem hierarchy.
        Updates processing statistics for accurate progress reporting and metrics.
        """
        if not root_path.exists():
            raise FileNotFoundError(f"Root path does not exist: {root_path}")
        
        if not root_path.is_dir():
            raise ValueError(f"Root path is not a directory: {root_path}")
        
        await ctx.info(f"Discovering structure for: {root_path}")
        
        # Build directory context recursively
        directory_context = await self._build_directory_context(root_path, ctx)
        
        # Update statistics
        stats = self._current_status.processing_stats
        stats.total_files_discovered = directory_context.total_files
        stats.total_directories_discovered = len(list(self._get_all_directories(directory_context)))
        
        await ctx.info(f"Discovery complete: {stats.total_files_discovered} files, {stats.total_directories_discovered} directories")
        
        return directory_context
    
    async def _build_directory_context(self, directory_path: Path, ctx: Context) -> DirectoryContext:
        """
        [Class method intent]
        Builds DirectoryContext for a single directory including all child files and subdirectories.
        Recursively processes subdirectories while applying configuration filtering rules
        and handling special cases for git-clones and project-base scenarios.

        [Design principles]
        Single directory context building with recursive subdirectory processing.
        Configuration filtering applied consistently across all discovery operations.
        Special handling integration for git-clones and project-base scenarios.
        Error handling enabling graceful degradation when individual items are inaccessible.

        [Implementation details]
        Iterates through directory contents applying should_process filters from configuration.
        Creates FileContext objects for all processable files with metadata extraction.
        Recursively builds DirectoryContext objects for processable subdirectories.
        Handles filesystem errors gracefully with logging and continued processing.
        """
        file_contexts = []
        subdirectory_contexts = []
        
        try:
            # Process files in current directory
            for item in directory_path.iterdir():
                try:
                    if item.is_file() and self.config.should_process_file(item):
                        file_context = FileContext(
                            file_path=item,
                            file_size=item.stat().st_size,
                            last_modified=datetime.fromtimestamp(item.stat().st_mtime)
                        )
                        file_contexts.append(file_context)
                        
                    elif item.is_dir() and self.config.should_process_directory(item):
                        # Recursive directory processing
                        subdir_context = await self._build_directory_context(item, ctx)
                        subdirectory_contexts.append(subdir_context)
                        
                except (OSError, PermissionError) as e:
                    logger.warning(f"Skipping inaccessible item {item}: {e}")
                    continue
        
        except (OSError, PermissionError) as e:
            logger.error(f"Cannot access directory {directory_path}: {e}")
            self._current_status.processing_stats.add_error(f"Directory access failed: {directory_path}: {e}")
        
        return DirectoryContext(
            directory_path=directory_path,
            file_contexts=file_contexts,
            subdirectory_contexts=subdirectory_contexts
        )
    
    async def _detect_changes(self, root_context: DirectoryContext, ctx: Context) -> DirectoryContext:
        """
        [Class method intent]
        Detects changes in the directory hierarchy using comprehensive change detection.
        Updates DirectoryContext objects to mark which directories need processing
        based on comprehensive constituent dependency checking.

        [Design principles]
        Comprehensive change detection using enhanced FileAnalysisCache integration.
        DirectoryContext status updates enabling targeted processing of only changed directories.
        Recursive change detection ensuring all directories are evaluated for staleness.

        [Implementation details]
        Uses enhanced check_comprehensive_directory_change() for each directory.
        Updates DirectoryContext processing_status to PENDING only for directories requiring rebuild.
        Returns updated DirectoryContext hierarchy with proper change detection status.
        """
        await ctx.info("Detecting changes using comprehensive change detection")
        
        # Apply comprehensive change detection recursively
        updated_root_context = await self._apply_comprehensive_change_detection(root_context, ctx)
        
        # Count directories that need processing
        all_directories = self._get_all_directories(updated_root_context)
        directories_needing_processing = [d for d in all_directories if d.processing_status == ProcessingStatus.PENDING]
        
        await ctx.info(f"Comprehensive change detection complete: {len(directories_needing_processing)}/{len(all_directories)} directories need processing")
        
        return updated_root_context
    
    async def _apply_comprehensive_change_detection(self, directory_context: DirectoryContext, ctx: Context) -> DirectoryContext:
        """
        [Class method intent]
        Recursively applies comprehensive change detection to directory hierarchy.
        Updates DirectoryContext processing_status to PENDING only for directories requiring rebuild.
        
        [Design principles]
        Recursive change detection ensuring all directories are evaluated for staleness.
        Status updates enabling targeted processing of only changed directories.
        Bottom-up evaluation ensuring child changes propagate to parent directories.
        
        [Implementation details]
        Uses ChangeDetector.check_comprehensive_directory_change() for each directory.
        Recursively processes subdirectories first, then evaluates current directory.
        Updates processing_status to PENDING only for directories that need rebuilding.
        """
        try:
            # Step 1: Recursively process subdirectories first
            updated_subdirectory_contexts = []
            for subdir_context in directory_context.subdirectory_contexts:
                updated_subdir_context = await self._apply_comprehensive_change_detection(subdir_context, ctx)
                updated_subdirectory_contexts.append(updated_subdir_context)
            
            # Step 2: Create updated context with processed subdirectories
            directory_context_with_updated_children = DirectoryContext(
                directory_path=directory_context.directory_path,
                file_contexts=directory_context.file_contexts,
                subdirectory_contexts=updated_subdirectory_contexts,
                processing_status=directory_context.processing_status,
                knowledge_file_path=directory_context.knowledge_file_path,
                directory_summary=directory_context.directory_summary,
                error_message=directory_context.error_message,
                processing_start_time=directory_context.processing_start_time,
                processing_end_time=directory_context.processing_end_time
            )
            
            # Step 3: Apply comprehensive change detection to current directory
            change_info = await self.change_detector.check_comprehensive_directory_change(
                directory_context_with_updated_children, self._source_root, ctx
            )
            
            # Step 4: Update processing status based on change detection result
            if change_info is not None:
                # Changes detected - mark for processing
                await ctx.debug(f"Directory needs processing: {directory_context.directory_path.name} - {change_info.change_type.value}")
                processing_status = ProcessingStatus.PENDING
            else:
                # No changes detected - skip processing
                await ctx.debug(f"Directory up to date: {directory_context.directory_path.name}")
                processing_status = ProcessingStatus.SKIPPED
            
            # Step 5: Return updated context with change detection status
            return DirectoryContext(
                directory_path=directory_context_with_updated_children.directory_path,
                file_contexts=directory_context_with_updated_children.file_contexts,
                subdirectory_contexts=directory_context_with_updated_children.subdirectory_contexts,
                processing_status=processing_status,
                knowledge_file_path=directory_context_with_updated_children.knowledge_file_path,
                directory_summary=directory_context_with_updated_children.directory_summary,
                error_message=directory_context_with_updated_children.error_message,
                processing_start_time=directory_context_with_updated_children.processing_start_time,
                processing_end_time=directory_context_with_updated_children.processing_end_time
            )
            
        except Exception as e:
            logger.error(f"Comprehensive change detection failed for {directory_context.directory_path}: {e}")
            # Conservative fallback: mark for processing if change detection fails
            await ctx.warning(f"Change detection failed for {directory_context.directory_path.name}, marking for processing")
            return DirectoryContext(
                directory_path=directory_context.directory_path,
                file_contexts=directory_context.file_contexts,
                subdirectory_contexts=directory_context.subdirectory_contexts,
                processing_status=ProcessingStatus.PENDING,  # Process when detection fails
                knowledge_file_path=directory_context.knowledge_file_path,
                directory_summary=directory_context.directory_summary,
                error_message=directory_context.error_message,
                processing_start_time=directory_context.processing_start_time,
                processing_end_time=directory_context.processing_end_time
            )
    
    async def _process_directory_hierarchy(self, root_context: DirectoryContext, ctx: Context) -> None:
        """
        [Class method intent]
        Processes the directory hierarchy using leaf-first strategy ensuring child contexts
        are completely processed before parent directory knowledge file generation.
        Coordinates concurrent processing while maintaining dependency order.

        [Design principles]
        Leaf-first processing ensuring bottom-up assembly without parent-to-child dependencies.
        Concurrent processing within dependency constraints for optimal performance.
        Progress reporting providing real-time feedback throughout hierarchical processing.
        Error handling enabling graceful degradation and partial processing completion.

        [Implementation details]
        Implements depth-first traversal identifying leaf directories for initial processing.
        Uses async semaphore for concurrency control respecting configuration limits.
        Processes all child files before attempting parent directory knowledge generation.
        Reports progress through FastMCP Context with detailed operation status.
        Captures and uses updated root context to ensure root-level knowledge file generation.
        """
        await ctx.info("Starting leaf-first hierarchical processing")
        
        # Process in leaf-first order and capture the updated root context
        updated_root_context = await self._process_directory_leaf_first(root_context, ctx)
        
        # Update the status with the processed root context
        self._current_status.root_directory_context = updated_root_context
        
        await ctx.info("Leaf-first processing completed")
    
    async def _process_directory_leaf_first(self, directory_context: DirectoryContext, ctx: Context) -> DirectoryContext:
        """
        [Class method intent]
        Processes a single directory using leaf-first strategy by first processing all
        subdirectories recursively, then processing files in current directory,
        and finally generating directory knowledge file from child summaries.
        Returns updated DirectoryContext with processed subdirectory and file contexts.

        [Design principles]
        Recursive leaf-first processing ensuring child completion before parent processing.
        Bottom-up assembly aggregating child summaries into parent knowledge files.
        Concurrent file processing for performance optimization within single directory.
        Comprehensive error handling enabling graceful degradation on individual failures.
        Immutable context management ensuring proper state updates throughout processing.

        [Implementation details]
        First recursively processes all subdirectories ensuring child context completion.
        Then processes all files in current directory using concurrent batch processing.
        Finally generates directory knowledge file using KnowledgeBuilder with child summaries.
        Updates processing statistics and status throughout the processing workflow.
        Returns updated DirectoryContext with all processed children for parent context updates.
        """
        try:
            await ctx.info(f"Processing directory: {directory_context.directory_path}")
            
            # Step 1: Process all subdirectories first (leaf-first) and collect updated contexts
            updated_subdirectory_contexts = []
            for subdir_context in directory_context.subdirectory_contexts:
                updated_subdir_context = await self._process_directory_leaf_first(subdir_context, ctx)
                updated_subdirectory_contexts.append(updated_subdir_context)
            
            # Step 2: Process all files in current directory
            updated_directory_context = directory_context
            if directory_context.file_contexts:
                await ctx.info(f"Processing {len(directory_context.file_contexts)} files in {directory_context.directory_path}")
                updated_directory_context = await self._process_directory_files(directory_context, ctx)
            
            # Step 3: Create directory context with updated subdirectory contexts
            complete_directory_context = DirectoryContext(
                directory_path=updated_directory_context.directory_path,
                file_contexts=updated_directory_context.file_contexts,
                subdirectory_contexts=updated_subdirectory_contexts,  # Use updated subdirectory contexts
                processing_status=updated_directory_context.processing_status,
                knowledge_file_path=updated_directory_context.knowledge_file_path,
                directory_summary=updated_directory_context.directory_summary,
                error_message=updated_directory_context.error_message,
                processing_start_time=datetime.now(),
                processing_end_time=None
            )
            
            # Step 4: Generate directory knowledge file from child summaries (only if needed)
            if complete_directory_context.processing_status == ProcessingStatus.SKIPPED:
                # Directory is up to date - skip knowledge file generation
                await ctx.info(f"Directory up to date, skipping knowledge file generation: {directory_context.directory_path}")
                
                # Update statistics
                self._current_status.processing_stats.directories_completed += 1
                
                return DirectoryContext(
                    directory_path=complete_directory_context.directory_path,
                    file_contexts=complete_directory_context.file_contexts,
                    subdirectory_contexts=complete_directory_context.subdirectory_contexts,
                    processing_status=ProcessingStatus.COMPLETED,  # Mark as completed (skipped but successful)
                    knowledge_file_path=complete_directory_context.knowledge_file_path,
                    directory_summary=complete_directory_context.directory_summary,
                    error_message=complete_directory_context.error_message,
                    processing_start_time=complete_directory_context.processing_start_time,
                    processing_end_time=datetime.now()
                )
            elif complete_directory_context.is_ready_for_summary:
                # Directory needs processing - generate knowledge file
                await ctx.info(f"Generating knowledge file for: {directory_context.directory_path}")
                final_directory_context = await self._generate_directory_knowledge_file(complete_directory_context, ctx)
                
                # Update statistics
                self._current_status.processing_stats.directories_completed += 1
                
                return final_directory_context
            else:
                await ctx.warning(f"Directory not ready for summary generation: {directory_context.directory_path}")
                
                # Update statistics
                self._current_status.processing_stats.directories_completed += 1
                
                return complete_directory_context
            
        except Exception as e:
            logger.error(f"Directory processing failed for {directory_context.directory_path}: {e}", exc_info=True)
            self._current_status.processing_stats.directories_failed += 1
            self._current_status.processing_stats.add_error(f"Directory processing failed: {directory_context.directory_path}: {e}")
            
            if not self.config.continue_on_file_errors:
                raise
            
            # Return failed context
            return DirectoryContext(
                directory_path=directory_context.directory_path,
                file_contexts=directory_context.file_contexts,
                subdirectory_contexts=directory_context.subdirectory_contexts,
                processing_status=ProcessingStatus.FAILED,
                error_message=str(e),
                processing_start_time=datetime.now(),
                processing_end_time=datetime.now()
            )
    
    async def _process_directory_files(self, directory_context: DirectoryContext, ctx: Context) -> DirectoryContext:
        """
        [Class method intent]
        Processes all files in a directory using concurrent batch processing for performance.
        Delegates individual file processing to KnowledgeBuilder while maintaining
        processing statistics and error handling throughout the operation.
        Returns updated DirectoryContext with processed file contexts.

        [Design principles]
        Concurrent file processing for performance optimization using configured batch sizes.
        Individual file processing delegation to specialized KnowledgeBuilder component.
        Comprehensive error handling enabling graceful degradation on individual file failures.
        Accurate statistics tracking for progress reporting and performance monitoring.
        Immutable context management ensuring proper state updates throughout processing.

        [Implementation details]
        Groups files into batches based on configuration batch size for concurrent processing.
        Uses asyncio.gather for concurrent processing within each batch for performance.
        Delegates individual file content analysis to KnowledgeBuilder component.
        Updates processing statistics for each file including success, failure, and error tracking.
        Creates new DirectoryContext with updated file contexts maintaining immutability.
        """
        files_to_process = [fc for fc in directory_context.file_contexts 
                           if fc.processing_status == ProcessingStatus.PENDING]
        
        if not files_to_process:
            return directory_context
        
        updated_file_contexts = list(directory_context.file_contexts)  # Copy the list
        
        # Process files in batches for performance
        batch_size = self.config.batch_size
        for i in range(0, len(files_to_process), batch_size):
            batch = files_to_process[i:i + batch_size]
            
            # Process batch concurrently
            tasks = [self._process_single_file(file_context, ctx) for file_context in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Update file contexts and statistics based on results
            for file_context, result in zip(batch, results):
                if isinstance(result, Exception):
                    self._current_status.processing_stats.files_failed += 1
                    self._current_status.processing_stats.add_error(f"File processing failed: {result}")
                    # Keep original context for failed files
                elif result is None:
                    # Truncation detected - completely omit this file from processing
                    self._current_status.processing_stats.files_completed += 1  # Count as completed (omitted)
                    # Remove the original file context from the list
                    updated_file_contexts = [fc for fc in updated_file_contexts if fc.file_path != file_context.file_path]
                    await ctx.info(f"🚨 TRUNCATION: File {file_context.file_path.name} omitted from processing - no artifacts created")
                else:
                    self._current_status.processing_stats.files_completed += 1
                    # Update the file context in the list
                    for j, fc in enumerate(updated_file_contexts):
                        if fc.file_path == file_context.file_path:
                            updated_file_contexts[j] = result
                            break
                
                self._current_status.processing_stats.files_processed += 1
        
        # Return updated directory context with processed file contexts
        return DirectoryContext(
            directory_path=directory_context.directory_path,
            file_contexts=updated_file_contexts,
            subdirectory_contexts=directory_context.subdirectory_contexts,
            processing_status=directory_context.processing_status,
            knowledge_file_path=directory_context.knowledge_file_path,
            directory_summary=directory_context.directory_summary,
            error_message=directory_context.error_message,
            processing_start_time=directory_context.processing_start_time,
            processing_end_time=directory_context.processing_end_time
        )
    
    async def _process_single_file(self, file_context: FileContext, ctx: Context) -> Optional[FileContext]:
        """
        [Class method intent]
        Processes a single file by delegating content analysis to KnowledgeBuilder with cache support.
        Passes source_root parameter enabling high-performance file analysis caching
        for significant performance improvements on unchanged files.
        Handles truncation detection by returning None to completely omit files from processing.

        [Design principles]
        Single file processing delegation to specialized KnowledgeBuilder component.
        Cache-enabled processing for performance optimization on unchanged files.
        Comprehensive error handling enabling graceful degradation on individual file failures.
        Truncation detection handling completely omitting files when LLM output is incomplete.
        Timing statistics collection for performance analysis and optimization.
        Processing status updates for accurate progress reporting and coordination.
        Semaphore usage for concurrency control without recursive deadlocks.

        [Implementation details]
        Uses semaphore to control concurrent file processing operations.
        Delegates content analysis to KnowledgeBuilder.build_file_knowledge method with source_root.
        Passes source_root parameter enabling FileAnalysisCache for performance optimization.
        Handles None return from KnowledgeBuilder indicating truncated files should be omitted.
        Tracks processing timing for performance analysis and optimization insights.
        Handles errors gracefully with detailed logging and statistics updates.
        Returns updated FileContext with processing results or None for omitted files.
        """
        async with self._processing_semaphore:
            try:
                await ctx.debug(f"Processing file: {file_context.file_path}")
                
                # Delegate to knowledge builder with source_root for cache support
                updated_context = await self.knowledge_builder.build_file_knowledge(
                    file_context, ctx, source_root=getattr(self, '_source_root', None)
                )
                
                # Handle truncation detection - None means file should be completely omitted
                if updated_context is None:
                    await ctx.debug(f"File omitted due to truncation: {file_context.file_path}")
                    return None
                
                return updated_context
                
            except Exception as e:
                logger.error(f"File processing failed for {file_context.file_path}: {e}", exc_info=True)
                
                # Return failed context
                return FileContext(
                    file_path=file_context.file_path,
                    file_size=file_context.file_size,
                    last_modified=file_context.last_modified,
                    processing_status=ProcessingStatus.FAILED,
                    error_message=str(e),
                    processing_start_time=file_context.processing_start_time,
                    processing_end_time=datetime.now()
                )
    
    async def _generate_directory_knowledge_file(self, directory_context: DirectoryContext, ctx: Context) -> DirectoryContext:
        """
        [Class method intent]
        Generates knowledge file for directory by aggregating child file summaries and
        subdirectory knowledge files into hierarchical directory summary.
        Delegates content generation to KnowledgeBuilder for consistent LLM integration.

        [Design principles]
        Bottom-up assembly aggregating child summaries into parent directory knowledge files.
        Hierarchical knowledge file generation following standard knowledge file format.
        Content generation delegation to specialized KnowledgeBuilder component.
        Error handling enabling graceful degradation when knowledge generation fails.

        [Implementation details]
        Collects all child file summaries and subdirectory knowledge content.
        Delegates hierarchical summary generation to KnowledgeBuilder component.
        Writes generated knowledge file to appropriate location in filesystem.
        Updates DirectoryContext with processing results and knowledge file path.
        """
        try:
            await ctx.debug(f"Generating knowledge file for directory: {directory_context.directory_path}")
            
            # Delegate to knowledge builder for directory summary generation
            # Pass source root for proper hierarchical structure preservation
            updated_context = await self.knowledge_builder.build_directory_summary(
                directory_context, ctx, source_root=getattr(self, '_source_root', None)
            )
            
            return updated_context
            
        except Exception as e:
            logger.error(f"Directory knowledge generation failed for {directory_context.directory_path}: {e}", exc_info=True)
            self._current_status.processing_stats.add_error(f"Directory knowledge generation failed: {directory_context.directory_path}: {e}")
            
            if not self.config.continue_on_file_errors:
                # Return failed context
                return DirectoryContext(
                    directory_path=directory_context.directory_path,
                    file_contexts=directory_context.file_contexts,
                    subdirectory_contexts=directory_context.subdirectory_contexts,
                    processing_status=ProcessingStatus.FAILED,
                    error_message=str(e),
                    processing_start_time=directory_context.processing_start_time,
                    processing_end_time=datetime.now()
                )
            else:
                raise
    
    def _get_all_directories(self, directory_context: DirectoryContext) -> List[DirectoryContext]:
        """
        [Class method intent]
        Recursively collects all DirectoryContext objects in the hierarchy for statistics
        calculation and processing coordination. Provides comprehensive directory inventory
        for accurate progress reporting and processing planning.

        [Design principles]
        Recursive directory collection enabling comprehensive hierarchy analysis.
        Flat list generation simplifying statistics calculation and processing coordination.
        Complete hierarchy traversal ensuring accurate directory count and inventory.

        [Implementation details]
        Uses recursive traversal collecting all DirectoryContext objects in hierarchy.
        Returns flat list of all directories for easy iteration and statistics calculation.
        Includes root directory context in results for complete hierarchy representation.
        """
        directories = [directory_context]
        for subdir in directory_context.subdirectory_contexts:
            directories.extend(self._get_all_directories(subdir))
        return directories
    
    @property
    def current_status(self) -> IndexingStatus:
        """
        [Class method intent]
        Returns current indexing operation status for external monitoring and coordination.
        Provides real-time access to processing state, progress, and statistics
        for user interfaces and system integration.

        [Design principles]
        Real-time status access enabling external monitoring and user feedback.
        Immutable status access preventing external modification of internal state.
        Comprehensive status information supporting detailed progress reporting.

        [Implementation details]
        Returns current IndexingStatus object with complete operation state.
        Status object includes processing statistics, progress percentage, and current operation.
        Thread-safe access to status information for concurrent monitoring scenarios.
        """
        return self._current_status
    
    async def cleanup(self) -> None:
        """
        [Class method intent]
        Cleans up hierarchical indexer resources including knowledge builder and handler components.
        Ensures proper resource cleanup and connection closure for all component dependencies.

        [Design principles]
        Comprehensive resource cleanup ensuring no resource leaks or connection issues.
        Component cleanup delegation enabling proper resource management across dependencies.
        Error handling preventing cleanup failures from cascading to calling code.

        [Implementation details]
        Delegates cleanup to KnowledgeBuilder and handler components for proper resource management.
        Handles cleanup errors gracefully with appropriate logging and error reporting.
        """
        try:
            if hasattr(self, 'knowledge_builder') and self.knowledge_builder:
                await self.knowledge_builder.cleanup()
            
            logger.info("HierarchicalIndexer cleanup completed")
        except Exception as e:
            logger.warning(f"HierarchicalIndexer cleanup error: {e}")

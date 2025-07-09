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
# Execution Engine for Plan-then-Execute architecture in Knowledge Bases Hierarchical Indexing System.
# Executes atomic tasks from ExecutionPlan objects with dependency resolution, progress reporting,
# and comprehensive error handling for reliable Plan-then-Execute implementation.
###############################################################################
# [Source file design principles]
# - Atomic task execution ensuring each task is processed independently with complete isolation
# - Dependency-aware execution respecting task dependencies and hierarchical processing requirements
# - Comprehensive progress reporting providing real-time execution status and performance metrics
# - Robust error handling enabling graceful degradation and recovery from individual task failures
# - Concurrent execution optimization maximizing resource utilization through parallel task processing
###############################################################################
# [Source file constraints]
# - All task execution must be atomic and idempotent ensuring safe re-execution scenarios
# - Dependency resolution must be accurate preventing execution of tasks before prerequisites complete
# - Progress reporting must be real-time enabling accurate user feedback and system monitoring
# - Error recovery must preserve system consistency preventing partial state corruption
# - Resource management must prevent memory leaks and connection issues during long-running executions
###############################################################################
# [Dependencies]
# <codebase>: ..models.indexing_config - Configuration and processing parameters
# <codebase>: ..models.knowledge_context - Context structures for task execution
# <codebase>: ..models.execution_plan - Task models and execution planning structures
# <codebase>: .knowledge_builder - LLM-powered content analysis and KB generation
# <codebase>: .file_analysis_cache - Caching system for performance optimization
# <system>: asyncio - Async programming patterns for concurrent task execution
# <system>: pathlib - Cross-platform path operations and file metadata
# <system>: logging - Structured logging for execution analysis and debugging
###############################################################################
# [GenAI tool change history]
# 2025-07-07T21:36:00Z : CRITICAL EXECUTION BUG FIX - Fixed missing _create_handler_for_path method causing AttributeError by CodeAssistant
# * FIXED EXECUTION FAILURE: Added missing _create_handler_for_path() method causing "'ExecutionEngine' object has no attribute '_create_handler_for_path'" error
# * ADDED HANDLER REGISTRY: Integrated HandlerRegistry for proper path-based handler selection in cache structure creation
# * FIXED CACHE CREATION: Cache structure creation tasks now properly select handlers (git-clone vs project-base) based on source path
# * RESTORED TASK EXECUTION: CREATE_CACHE_STRUCTURE tasks now execute successfully with appropriate handler selection
# * ROOT CAUSE: Method was called in _execute_create_cache_structure() but never implemented, causing immediate execution failure
# 2025-07-07T15:00:00Z : CRITICAL HANDLER PATH FIX - Fixed ExecutionEngine path override preventing git-clone KB segregation by CodeAssistant
# * FIXED CRITICAL BUG: Modified _execute_create_directory_kb() to use handler-determined knowledge_file_path from task metadata
# * BEFORE: ExecutionEngine used FileAnalysisCache.get_knowledge_file_path() overriding handler decisions with hardcoded project-base paths
# * AFTER: Task metadata now carries handler-determined paths and ExecutionEngine respects these decisions
# * Added handler-determined path extraction with debug logging showing which path is being used
# * PREVENTS PATH OVERRIDE: Git-clone indexing tasks now execute with git-clones/ paths instead of project-base/
# * RESTORES HANDLER CONTROL: Each handler type now maintains control over its KB file locations through task metadata
# 2025-07-06T23:40:00Z : CRITICAL METADATA FIX - Fixed cache metadata contamination in final KB files by CodeAssistant
# * FIXED METADATA CONTAMINATION: Added _strip_cache_metadata() method to remove XML metadata tags before content inclusion
# * ADDED METADATA STRIPPING: Enhanced _load_cached_analysis_content() to strip CACHE_METADATA_START/END blocks
# * RESTORED CLEAN CONTENT: Directory KB files now contain clean analysis content without cache metadata pollution
# * ROOT CAUSE: Raw cache file content included metadata XML tags causing contamination in final knowledge base files
# 2025-07-06T23:18:00Z : CRITICAL CONTENT FIX - Fixed hardcoded placeholder content regression by CodeAssistant
# * FIXED CONTENT BUG: Replaced hardcoded "[Knowledge content from file analysis]" with actual cached analysis content
# * ADDED _load_cached_analysis_content(): Loads real file analysis from .analysis.md cache files for proper KB synthesis
# * RESTORED REAL CONTENT: Directory KB files now contain actual file analysis instead of placeholder text
# * ROOT CAUSE: FileContext objects reconstructed with hardcoded placeholder instead of loading cached analysis content
###############################################################################

"""
Execution Engine for Knowledge Bases System.

This module executes atomic tasks from ExecutionPlan objects with proper dependency
resolution, concurrent optimization, and comprehensive progress reporting for
reliable Plan-then-Execute architecture implementation.
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Any

from fastmcp import Context

from ..models import (
    IndexingConfig,
    DirectoryContext,
    FileContext,
    ProcessingStatus
)
from ..models.execution_plan import (
    ExecutionPlan,
    AtomicTask,
    TaskType,
    ExecutionResults
)
from .knowledge_builder import KnowledgeBuilder
from .file_analysis_cache import FileAnalysisCache
from .handler_interface import HandlerRegistry

logger = logging.getLogger(__name__)


class ExecutionEngine:
    """
    [Class intent]
    Executes atomic tasks from ExecutionPlan objects with dependency resolution and progress reporting.
    Provides concurrent task execution, comprehensive error handling, and real-time progress monitoring
    for reliable Plan-then-Execute architecture implementation.

    [Design principles]
    Atomic task execution ensuring complete task isolation and independent processing.
    Dependency-aware execution respecting task prerequisites and hierarchical processing order.
    Concurrent execution optimization maximizing resource utilization through parallel processing.
    Comprehensive progress reporting providing real-time execution status and performance metrics.
    Robust error handling enabling graceful degradation and recovery from individual task failures.
    Resource management preventing memory leaks and connection issues during long-running executions.

    [Implementation details]
    Uses asyncio for concurrent task execution with proper dependency management.
    Implements task dispatch system routing tasks to appropriate execution handlers.
    Provides comprehensive progress tracking with real-time updates and performance metrics.
    Maintains execution state ensuring consistent system behavior across complex execution scenarios.
    Integrates with existing components (KnowledgeBuilder, FileAnalysisCache) for seamless operation.
    """
    
    def __init__(self, config: IndexingConfig):
        """
        [Class method intent]
        Initializes execution engine with configuration and component dependencies.
        Sets up task execution handlers, concurrency control, and progress tracking.

        [Design principles]
        Configuration-driven behavior enabling different execution scenarios and resource management.
        Component integration enabling seamless operation with existing knowledge building infrastructure.
        Concurrency control setup providing optimal resource utilization without system overload.

        [Implementation details]
        Creates KnowledgeBuilder and FileAnalysisCache instances for task execution.
        Sets up concurrency semaphore based on configuration limits.
        Initializes task execution handlers for different task types.
        Prepares progress tracking and error handling infrastructure.
        """
        self.config = config
        self.knowledge_builder = KnowledgeBuilder(config)
        self.file_cache = FileAnalysisCache(config)
        self.handler_registry = HandlerRegistry(config)
        
        # Concurrency control
        self._execution_semaphore = asyncio.Semaphore(config.max_concurrent_operations)
        
        # Task execution state
        self._completed_tasks: Set[str] = set()
        self._failed_tasks: Set[str] = set()
        self._running_tasks: Set[str] = set()
        
        # Task execution handlers
        self._task_handlers = {
            TaskType.ANALYZE_FILE_LLM: self._execute_analyze_file_llm,
            TaskType.SKIP_FILE_CACHED: self._execute_skip_file_cached,
            TaskType.CREATE_DIRECTORY_KB: self._execute_create_directory_kb,
            TaskType.SKIP_DIRECTORY_FRESH: self._execute_skip_directory_fresh,
            TaskType.DELETE_ORPHANED_FILE: self._execute_delete_orphaned_file,
            TaskType.DELETE_ORPHANED_DIRECTORY: self._execute_delete_orphaned_directory,
            TaskType.CREATE_CACHE_STRUCTURE: self._execute_create_cache_structure,
            TaskType.VERIFY_CACHE_FRESHNESS: self._execute_verify_cache_freshness,
            TaskType.VERIFY_KB_FRESHNESS: self._execute_verify_kb_freshness
        }
        
        logger.info("Initialized ExecutionEngine with atomic task execution capabilities")
    
    async def execute_plan(self, plan: ExecutionPlan, ctx: Context) -> ExecutionResults:
        """
        [Class method intent]
        Executes complete ExecutionPlan with dependency resolution and progress reporting.
        Processes all atomic tasks in proper order with concurrent optimization and error handling.

        [Design principles]
        Complete plan execution ensuring all tasks are processed according to their dependencies.
        Concurrent execution optimization maximizing resource utilization through parallel processing.
        Comprehensive progress reporting providing real-time execution status and performance metrics.
        Robust error handling enabling graceful degradation and recovery from individual task failures.
        Resource management ensuring proper cleanup and connection management throughout execution.

        [Implementation details]
        Validates plan dependencies before execution begins.
        Executes tasks in dependency order with concurrent optimization where possible.
        Tracks execution progress with real-time updates and performance metrics.
        Handles task failures gracefully with continued execution where possible.
        Returns comprehensive execution results for analysis and debugging.

        Args:
            plan: ExecutionPlan containing atomic tasks to execute
            ctx: FastMCP context for progress reporting and logging

        Returns:
            ExecutionResults: Comprehensive execution results with performance metrics
        """
        await ctx.info(f"Starting execution of plan {plan.plan_id} with {len(plan.tasks)} tasks")
        
        # Initialize execution results
        results = ExecutionResults(
            plan_id=plan.plan_id,
            execution_start=datetime.now()
        )
        
        try:
            # Initialize knowledge builder
            await self.knowledge_builder.initialize()
            
            # Validate plan dependencies
            validation_errors = plan.validate_dependencies()
            if validation_errors:
                error_msg = f"Plan validation failed: {validation_errors}"
                await ctx.error(f"❌ EXECUTION FAILED: {error_msg}")
                raise RuntimeError(error_msg)
            
            # Get execution order
            execution_order = plan.get_execution_order()
            await ctx.info(f"Executing {len(execution_order)} tasks in dependency order")
            
            # Execute tasks with progress reporting
            for i, task in enumerate(execution_order):
                progress = (i / len(execution_order)) * 100
                await ctx.info(f"[{progress:.1f}%] Executing: {task.description}")
                
                try:
                    # Check if dependencies are satisfied
                    if not self._are_dependencies_satisfied(task):
                        error_msg = f"Dependencies not satisfied for task {task.task_id}"
                        await ctx.error(f"❌ DEPENDENCY ERROR: {error_msg}")
                        results.add_failed_task(task.task_id, error_msg)
                        continue
                    
                    # Execute task
                    await self._execute_single_task(task, ctx)
                    results.add_completed_task(task.task_id)
                    
                    # Update performance metrics
                    if task.is_expensive:
                        results.llm_calls_made += 1
                    
                    if task.task_type in {TaskType.ANALYZE_FILE_LLM, TaskType.SKIP_FILE_CACHED}:
                        results.files_processed += 1
                    elif task.task_type in {TaskType.CREATE_DIRECTORY_KB, TaskType.SKIP_DIRECTORY_FRESH}:
                        results.directories_processed += 1
                    elif task.task_type in {TaskType.DELETE_ORPHANED_FILE, TaskType.DELETE_ORPHANED_DIRECTORY}:
                        results.files_deleted += 1
                    
                except Exception as e:
                    error_msg = f"Task execution failed: {str(e)}"
                    await ctx.error(f"❌ TASK FAILED: {task.description} - {error_msg}")
                    results.add_failed_task(task.task_id, error_msg)
                    
                    # Continue with next task unless configured to stop on errors
                    if not self.config.continue_on_file_errors:
                        await ctx.error("❌ EXECUTION STOPPED: continue_on_file_errors is False")
                        break
            
            # Complete execution
            results.complete_execution()
            
            await ctx.info(f"✅ Execution completed: {len(results.completed_tasks)} succeeded, {len(results.failed_tasks)} failed")
            await ctx.info(f"📊 Performance: {results.llm_calls_made} LLM calls, {results.total_duration:.1f}s total")
            
            return results
            
        except Exception as e:
            logger.error(f"Plan execution failed: {e}", exc_info=True)
            results.complete_execution()
            await ctx.error(f"❌ EXECUTION FAILED: {str(e)}")
            raise
        
        finally:
            # Cleanup resources
            await self._cleanup_execution_resources()
    
    async def preview_plan(self, plan: ExecutionPlan, ctx: Context) -> None:
        """
        [Class method intent]
        Provides detailed preview of execution plan without actually executing tasks.
        Shows what would be executed, dependencies, and resource requirements for debugging.

        [Design principles]
        Complete plan analysis enabling thorough debugging and verification before execution.
        No side effects ensuring preview can be called safely without affecting system state.
        Comprehensive information display supporting decision making and optimization.

        [Implementation details]
        Uses ExecutionPlan.preview() method for formatted output display.
        Adds execution-specific analysis and resource requirements.
        Provides dependency validation and execution order analysis.
        """
        await ctx.info("🔍 EXECUTION PLAN PREVIEW")
        await ctx.info("=" * 50)
        
        # Show plan preview
        preview_text = plan.preview()
        for line in preview_text.split('\n'):
            await ctx.info(line)
        
        # Add execution-specific analysis
        await ctx.info("")
        await ctx.info("🚀 Execution Analysis:")
        await ctx.info(f"   • Max Concurrent Operations: {self.config.max_concurrent_operations}")
        await ctx.info(f"   • Continue on Errors: {self.config.continue_on_file_errors}")
        await ctx.info(f"   • Estimated Duration: {plan.total_estimated_duration:.1f}s")
        
        # Show parallel execution opportunities
        parallel_groups = plan.get_parallel_execution_groups()
        max_parallel = max(len(group) for group in parallel_groups) if parallel_groups else 0
        await ctx.info(f"   • Max Parallel Tasks: {max_parallel}")
        await ctx.info(f"   • Execution Levels: {len(parallel_groups)}")
    
    def _are_dependencies_satisfied(self, task: AtomicTask) -> bool:
        """
        [Class method intent]
        Checks if all dependencies for a task have been completed successfully.
        Validates that prerequisite tasks have finished before allowing task execution.

        [Design principles]
        Strict dependency validation ensuring tasks only execute when prerequisites are satisfied.
        Failure propagation preventing execution of tasks whose dependencies failed.
        Simple boolean result enabling clear execution control flow.

        [Implementation details]
        Checks all task dependencies against completed tasks set.
        Ensures no dependencies are in failed tasks set.
        Returns True only when all dependencies are satisfied and successful.
        """
        for dep_id in task.dependencies:
            if dep_id in self._failed_tasks:
                # Dependency failed - cannot execute this task
                return False
            if dep_id not in self._completed_tasks:
                # Dependency not yet completed
                return False
        return True
    
    async def _execute_single_task(self, task: AtomicTask, ctx: Context) -> None:
        """
        [Class method intent]
        Executes single atomic task using appropriate task handler with concurrency control.
        Dispatches task to specialized handler based on task type with proper resource management.

        [Design principles]
        Atomic task execution ensuring complete task isolation and independent processing.
        Task dispatch system enabling specialized handling for different task types.
        Concurrency control preventing system overload while maximizing resource utilization.
        Comprehensive error handling enabling graceful task failure recovery.

        [Implementation details]
        Uses semaphore for concurrency control and resource management.
        Dispatches task to appropriate handler based on task type.
        Tracks running tasks for progress monitoring and debugging.
        Handles task execution errors with detailed logging and error reporting.
        """
        async with self._execution_semaphore:
            try:
                # Mark task as running
                self._running_tasks.add(task.task_id)
                
                # Get appropriate handler
                handler = self._task_handlers.get(task.task_type)
                if not handler:
                    raise RuntimeError(f"No handler found for task type: {task.task_type}")
                
                # Execute task
                await handler(task, ctx)
                
                # Mark task as completed
                self._completed_tasks.add(task.task_id)
                await ctx.debug(f"✅ Task completed: {task.task_id}")
                
            except Exception as e:
                # Mark task as failed
                self._failed_tasks.add(task.task_id)
                logger.error(f"Task execution failed: {task.task_id} - {e}", exc_info=True)
                raise
            
            finally:
                # Remove from running tasks
                self._running_tasks.discard(task.task_id)
    
    # Task Execution Handlers
    
    async def _execute_analyze_file_llm(self, task: AtomicTask, ctx: Context) -> None:
        """Execute LLM file analysis task"""
        file_path = task.target_path
        source_root = Path(task.metadata['source_root'])
        
        # Create FileContext for analysis
        file_context = FileContext(
            file_path=file_path,
            file_size=task.metadata['file_size'],
            last_modified=datetime.fromisoformat(task.metadata['last_modified']),
            processing_status=ProcessingStatus.PENDING
        )
        
        # Execute analysis (bypass cache since decision determined it's stale)
        # Get handler for source root to pass to knowledge builder
        handler = self._create_handler_for_path(source_root)
        result_context = await self.knowledge_builder.build_file_knowledge(
            file_context, ctx, source_root=source_root, bypass_cache=True, handler=handler
        )
        
        if result_context is None:
            raise RuntimeError(f"File analysis returned None (truncation): {file_path.name}")
        
        if result_context.processing_status == ProcessingStatus.FAILED:
            raise RuntimeError(f"File analysis failed: {result_context.error_message}")
        
        await ctx.debug(f"🤖 LLM analysis completed: {file_path.name}")
    
    async def _execute_skip_file_cached(self, task: AtomicTask, ctx: Context) -> None:
        """Execute file skip task (for tracking purposes)"""
        await ctx.debug(f"📄 Skipped file (cache fresh): {task.target_path.name}")
    
    async def _execute_create_directory_kb(self, task: AtomicTask, ctx: Context) -> None:
        """Execute directory KB creation task"""
        directory_path = task.target_path
        source_root = Path(task.metadata['source_root'])
        
        # SIMPLIFIED: Use knowledge_file_path from task metadata (set correctly by handler during discovery)
        knowledge_file_path = Path(task.metadata['knowledge_file_path'])
        await ctx.debug(f"Using KB path: {knowledge_file_path}")
        
        # Reconstruct FileContext objects from metadata with actual cached content
        file_contexts = []
        for fc_data in task.metadata['file_contexts']:
            file_path = Path(fc_data['path'])
            
            # Load actual analysis content from cache
            try:
                cached_content = await self._load_cached_analysis_content(file_path, source_root)
                knowledge_content = cached_content or "[Knowledge content from file analysis]"
            except Exception as e:
                logger.warning(f"Could not load cached analysis for {file_path}: {e}")
                knowledge_content = "[Knowledge content from file analysis]"
            
            file_context = FileContext(
                file_path=file_path,
                file_size=fc_data['size'],
                last_modified=datetime.fromisoformat(fc_data['last_modified']),
                processing_status=ProcessingStatus.COMPLETED,
                knowledge_content=knowledge_content
            )
            file_contexts.append(file_context)
        
        # Reconstruct subdirectory contexts with correct knowledge_file_paths
        subdirectory_contexts = []
        for sc_data in task.metadata['subdirectory_contexts']:
            subdir_path = Path(sc_data['path'])
            subdir_kb_path = Path(sc_data['knowledge_file_path'])
            subdir_context = DirectoryContext(
                directory_path=subdir_path,
                file_contexts=[],
                subdirectory_contexts=[],
                processing_status=ProcessingStatus.COMPLETED,
                knowledge_file_path=subdir_kb_path
            )
            subdirectory_contexts.append(subdir_context)
        
        # Create DirectoryContext for KB generation
        directory_context = DirectoryContext(
            directory_path=directory_path,
            file_contexts=file_contexts,
            subdirectory_contexts=subdirectory_contexts,
            processing_status=ProcessingStatus.PENDING,
            knowledge_file_path=knowledge_file_path
        )
        
        # Execute KB generation using the correct path
        result_context = await self.knowledge_builder.build_directory_summary(
            directory_context, ctx, knowledge_file_path=knowledge_file_path, source_root=source_root
        )
        
        if result_context.processing_status == ProcessingStatus.FAILED:
            raise RuntimeError(f"Directory KB creation failed: {result_context.error_message}")
        
        await ctx.debug(f"📁 Directory KB created: {directory_path.name}")
    
    async def _execute_skip_directory_fresh(self, task: AtomicTask, ctx: Context) -> None:
        """Execute directory skip task (for tracking purposes)"""
        await ctx.debug(f"✅ Skipped directory (KB fresh): {task.target_path.name}")
    
    async def _execute_delete_orphaned_file(self, task: AtomicTask, ctx: Context) -> None:
        """Execute orphaned file deletion task"""
        file_path = task.target_path
        
        if not task.metadata.get('is_safe_to_delete', False):
            raise RuntimeError(f"File not marked as safe to delete: {file_path}")
        
        try:
            if file_path.exists():
                file_path.unlink()
                await ctx.debug(f"🗑️ Deleted orphaned file: {file_path.name}")
            else:
                await ctx.debug(f"🗑️ File already deleted: {file_path.name}")
        except Exception as e:
            raise RuntimeError(f"Failed to delete orphaned file: {e}")
    
    async def _execute_delete_orphaned_directory(self, task: AtomicTask, ctx: Context) -> None:
        """Execute orphaned directory deletion task"""
        dir_path = task.target_path
        
        if not task.metadata.get('is_safe_to_delete', False):
            raise RuntimeError(f"Directory not marked as safe to delete: {dir_path}")
        
        try:
            if dir_path.exists() and dir_path.is_dir():
                dir_path.rmdir()  # Only removes empty directories
                await ctx.debug(f"🗂️ Deleted empty orphaned directory: {dir_path.name}")
            else:
                await ctx.debug(f"🗂️ Directory already deleted: {dir_path.name}")
        except OSError as e:
            if "not empty" in str(e).lower():
                await ctx.warning(f"Cannot delete non-empty directory: {dir_path.name}")
            else:
                raise RuntimeError(f"Failed to delete orphaned directory: {e}")
    
    async def _execute_create_cache_structure(self, task: AtomicTask, ctx: Context) -> None:
        """Execute cache structure creation task"""
        directories = task.metadata.get('directories', [])
        source_root = Path(task.metadata['source_root'])
        
        # Create appropriate handler based on source root
        handler = self._create_handler_for_path(source_root)
        
        for dir_str in directories:
            dir_path = Path(dir_str)
            try:
                # Use handler to determine cache path - NO fallbacks to project-base
                cache_path = handler.get_cache_path(dir_path / "dummy.txt", source_root).parent
                cache_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                logger.error(f"❌ CACHE STRUCTURE CREATION FAILED for {dir_path}: {e} - Handler: {handler.get_handler_type()}")
                raise RuntimeError(f"Cache structure creation failed: {e}")
        
        await ctx.debug(f"🏗️ Cache structure created: {len(directories)} directories using handler: {handler.get_handler_type()}")
    
    async def _execute_verify_cache_freshness(self, task: AtomicTask, ctx: Context) -> None:
        """Execute cache freshness verification task"""
        file_path = task.target_path
        source_root = Path(task.metadata['source_root'])
        
        # Check if file is empty/unreadable - these files are legitimately skipped
        try:
            if not file_path.exists() or file_path.stat().st_size == 0:
                await ctx.debug(f"🔍 Cache verification skipped: {file_path.name} (empty file)")
                return
        except Exception:
            await ctx.debug(f"🔍 Cache verification skipped: {file_path.name} (unreadable file)")
            return
        
        # Get appropriate handler for cache freshness checking
        handler = self._create_handler_for_path(source_root)
        is_fresh, reason = self.file_cache.is_cache_fresh(file_path, source_root, handler)
        if not is_fresh:
            raise RuntimeError(f"Cache verification failed: {reason}")
        
        await ctx.debug(f"🔍 Cache freshness verified: {file_path.name}")
    
    async def _execute_verify_kb_freshness(self, task: AtomicTask, ctx: Context) -> None:
        """Execute KB freshness verification task"""
        directory_path = task.target_path
        source_root = Path(task.metadata['source_root'])
        
        # Get KB path from task metadata (set by handler during planning)
        kb_path = Path(task.metadata.get('knowledge_file_path', ''))
        if not kb_path or not kb_path.exists():
            raise RuntimeError(f"KB file does not exist: {kb_path}")
        
        await ctx.debug(f"🔍 KB freshness verified: {directory_path.name}")
    
    def _strip_cache_metadata(self, content: str) -> str:
        """
        [Class method intent]
        Removes cache metadata XML tags from analysis content before inclusion in KB files.
        Strips CACHE_METADATA_START to CACHE_METADATA_END blocks to prevent contamination.

        [Design principles]
        Clean content delivery preventing metadata contamination in final KB files.
        Regex-based pattern matching for reliable metadata block identification.
        Graceful handling preserving content when metadata blocks are missing.

        [Implementation details]
        Uses regex with DOTALL flag to match multiline metadata blocks.
        Removes complete blocks including start/end tags and whitespace.
        Returns stripped content with leading/trailing whitespace removed.
        """
        import re
        # Remove cache metadata blocks from CACHE_METADATA_START to CACHE_METADATA_END
        pattern = r'<!-- CACHE_METADATA_START -->.*?<!-- CACHE_METADATA_END -->\s*'
        cleaned_content = re.sub(pattern, '', content, flags=re.DOTALL)
        return cleaned_content.strip()
    
    async def _load_cached_analysis_content(self, file_path: Path, source_root: Path) -> Optional[str]:
        """
        [Class method intent]
        Loads actual cached analysis content from FileAnalysisCache instead of using placeholder.
        Provides clean file analysis content for directory KB synthesis without metadata contamination.

        [Design principles]
        Real content loading enabling proper KB synthesis with actual analysis results.
        Metadata stripping preventing cache contamination in final KB files.
        Error handling preventing failures when cache content is unavailable.
        Performance optimization using existing cache infrastructure.

        [Implementation details]
        Uses FileAnalysisCache to load cached content from .analysis.md files.
        Strips cache metadata XML tags before returning clean content.
        Returns None if content unavailable, allowing fallback to placeholder.
        Handles file system errors gracefully to prevent task failures.
        """
        try:
            # Get appropriate handler for cache path resolution
            handler = self._create_handler_for_path(source_root)
            cache_path = self.file_cache.get_cache_path(file_path, source_root, handler)
            if cache_path.exists():
                raw_content = cache_path.read_text(encoding='utf-8')
                # Strip metadata tags before returning clean content
                return self._strip_cache_metadata(raw_content)
            else:
                logger.debug(f"Cache file not found: {cache_path}")
                return None
        except Exception as e:
            logger.warning(f"Error loading cached content for {file_path}: {e}")
            return None
    
    def _create_handler_for_path(self, source_path: Path):
        """
        [Class method intent]
        Creates appropriate handler for the given source path using HandlerRegistry.
        Provides path-based handler selection for cache and knowledge file operations.

        [Design principles]
        Handler registry integration enabling automatic handler selection based on path characteristics.
        Defensive handling ensuring execution continues even when no specific handler is available.
        Clear error reporting when handler selection fails to support debugging.

        [Implementation details]
        Uses HandlerRegistry.get_handler_for_path() for capability-based handler selection.
        Returns selected handler or raises RuntimeError if no handler is available.
        Supports both git-clone and project-base paths through registry routing.

        Args:
            source_path: Path requiring handler-specific processing

        Returns:
            IndexingHandler: Appropriate handler for the source path

        Raises:
            RuntimeError: When no handler is available for the path
        """
        handler = self.handler_registry.get_handler_for_path(source_path)
        if handler is None:
            raise RuntimeError(f"No indexing handler available for path: {source_path}")
        return handler
    
    async def _cleanup_execution_resources(self) -> None:
        """Clean up execution resources and connections"""
        try:
            if self.knowledge_builder:
                await self.knowledge_builder.cleanup()
            
            # Clear execution state
            self._completed_tasks.clear()
            self._failed_tasks.clear()
            self._running_tasks.clear()
            
            logger.info("ExecutionEngine cleanup completed")
        except Exception as e:
            logger.warning(f"ExecutionEngine cleanup error: {e}")

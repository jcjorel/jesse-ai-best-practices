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
# - Integration with RebuildDecisionEngine and KnowledgeBuilder for modular processing
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
# <codebase>: .knowledge_builder - LLM-powered content summarization
# <codebase>: .special_handlers - Git-clone and project-base special handling
# <system>: asyncio - Async programming patterns and concurrency control
# <system>: pathlib - Cross-platform path operations
# <system>: logging - Structured logging and error reporting
###############################################################################
# [GenAI tool change history]
# 2025-07-06T17:12:00Z : CRITICAL EXECUTION ORDER FIX - Fixed file-first processing to prevent stale KB generation by CodeAssistant
# * FIXED FUNDAMENTAL LOGICAL BUG: Corrected execution order in _process_directory_leaf_first to implement true file-first optimization
# * BEFORE: Generated directory KB files FIRST using stale analysis cache, then processed individual files (defeating optimization)
# * AFTER: Process individual stale files FIRST to refresh analysis cache, THEN generate directory KB files using fresh cache
# * Added explicit file-first messaging: "🔄 FILE-FIRST: Processing X stale files to refresh analysis cache"
# * PREVENTS STALE KB GENERATION: Directory knowledge files now always use fresh individual file analysis data
# 2025-07-06T16:32:00Z : CRITICAL WORKFLOW FIX - Added Phase 1.8 cleanup execution preventing cache inconsistencies by CodeAssistant
# * FIXED CRITICAL ISSUE: Added _execute_cleanup_decisions() method to actually delete orphaned files before rebuild processing
# * Added Phase 1.8 "Execute Cleanup Decisions" between decision analysis and change detection phases
# * Implemented concurrent deletion with safety validation and comprehensive error handling
# * PREVENTS CACHE INCONSISTENCIES: Orphaned cache files now removed before rebuild processing begins
# 2025-07-06T14:25:00Z : Integrated centralized RebuildDecisionEngine replacing scattered decision logic by CodeAssistant
# * Added RebuildDecisionEngine integration consolidating decision logic from HierarchicalIndexer, ChangeDetector, and FileAnalysisCache
# * Replaced scattered change detection and rebuild logic with unified decision engine providing comprehensive audit trails
# * Simplified indexing workflow by delegating all decision-making to centralized engine with clear reasoning
# 2025-07-06T14:09:00Z : Fixed empty directory rebuild loops and missing project root summary by CodeAssistant
# * Enhanced empty directory detection with improved logging (📁 EMPTY message) to prevent infinite rebuild cycles
# * Added project root forced processing (🏗️ PROJECT ROOT message) ensuring root_kb.md generation in incremental mode
# * Integrated FileAnalysisCache._is_directory_empty_of_processable_content() to skip knowledge file generation for empty directories
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
    IndexingStatus,
    DecisionReport,
    DecisionOutcome,
    ExecutionPlan,
    ExecutionResults
)
from .rebuild_decision_engine import RebuildDecisionEngine
from .knowledge_builder import KnowledgeBuilder
from .special_handlers import ProjectBaseHandler, GitCloneHandler
from .plan_generator import PlanGenerator
from .execution_engine import ExecutionEngine

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
    Uses RebuildDecisionEngine for centralized decision-making and comprehensive change detection.
    Delegates content summarization to KnowledgeBuilder with strands_agent_driver integration.
    Handles special cases through GitCloneHandler and ProjectBaseHandler components.
    Implements concurrent processing with configurable concurrency limits for performance.
    Provides comprehensive progress reporting through FastMCP Context integration.
    """
    
    def __init__(self, config: IndexingConfig):
        """
        [Class method intent]
        Initializes hierarchical indexer with Plan-then-Execute architecture components.
        Sets up decision engine, plan generator, and execution engine for coordinated processing.

        [Design principles]
        Plan-then-Execute architecture separating decision-making from execution for perfect debuggability.
        Component dependency injection enabling testability and modularity.
        Configuration-driven behavior supporting different processing scenarios.

        [Implementation details]
        Creates RebuildDecisionEngine for centralized decision-making.
        Creates PlanGenerator for converting decisions into atomic tasks.
        Creates ExecutionEngine for executing atomic tasks with dependency resolution.
        Initializes processing statistics and status tracking structures.
        """
        self.config = config
        
        # Plan-then-Execute architecture components
        self.rebuild_decision_engine = RebuildDecisionEngine(config)
        self.plan_generator = PlanGenerator(config)
        self.execution_engine = ExecutionEngine(config)
        
        # Processing coordination
        self._current_status = IndexingStatus()
        
        logger.info(f"Initialized HierarchicalIndexer with Plan-then-Execute architecture: {config.to_dict()}")
    
    async def index_hierarchy(self, root_path: Path, ctx: Context) -> IndexingStatus:
        """
        [Class method intent]
        Performs complete hierarchical indexing using Plan-then-Execute architecture.
        Separates decision-making from execution for perfect debuggability and atomic task processing.

        [Design principles]
        Plan-then-Execute architecture providing perfect execution plan visibility before expensive operations.
        Atomic task execution with dependency resolution ensuring proper hierarchical processing order.
        Comprehensive progress reporting with real-time status updates and performance metrics.
        Error recovery enabling graceful degradation and recovery from individual task failures.

        [Implementation details]
        Phase 1: Discovery - Build complete directory structure context
        Phase 2: Decision Analysis - Generate comprehensive DecisionReport with change detection
        Phase 3: Plan Generation - Convert decisions into atomic ExecutionPlan with dependencies
        Phase 4: Plan Preview - Show detailed execution plan for perfect debuggability
        Phase 5: Atomic Execution - Execute tasks with dependency resolution and progress reporting
        """
        self._current_status = IndexingStatus(
            overall_status=ProcessingStatus.PROCESSING,
            current_operation="Starting Plan-then-Execute hierarchical indexing",
            processing_stats=ProcessingStats()
        )
        
        # Store source root for knowledge file path calculations
        self._source_root = root_path
        
        try:
            # Start timing
            self._current_status.processing_stats.processing_start_time = datetime.now()
            
            await ctx.info(f"🚀 Starting Plan-then-Execute hierarchical indexing of: {root_path}")
            
            # Phase 1: Discovery (KEEP - build DirectoryContext hierarchy)
            await ctx.info("Phase 1: Discovering directory structure")
            self._current_status.current_operation = "Discovering directory structure"
            
            root_context = await self._discover_directory_structure(root_path, ctx)
            self._current_status.root_directory_context = root_context
            
            # Phase 2: Decision Analysis (KEEP - generate comprehensive DecisionReport)
            await ctx.info("Phase 2: Analyzing hierarchy for comprehensive decision-making")
            self._current_status.current_operation = "Analyzing hierarchy decisions"
            
            decision_report = await self.rebuild_decision_engine.analyze_hierarchy(root_context, root_path, ctx)
            await ctx.info(f"Decision analysis completed: {decision_report.total_decisions} decisions, {len(decision_report.files_to_delete)} deletions")
            
            # Phase 3: Plan Generation (NEW - convert decisions to atomic tasks)
            self._current_status.current_operation = "Generating atomic execution plan"
            execution_plan = await self._generate_execution_plan(root_context, decision_report, root_path, ctx)
            
            # Phase 4: Plan Preview (NEW - perfect debuggability)
            self._current_status.current_operation = "Previewing execution plan"
            await self._preview_execution_plan(execution_plan, ctx)
            
            # Phase 5: Atomic Execution (NEW - dependency-aware task execution)
            self._current_status.current_operation = "Executing atomic tasks"
            execution_results = await self._execute_plan_with_progress(execution_plan, ctx)
            
            # Create final status from execution results
            final_status = self._create_final_status(execution_results)
            
            duration = final_status.processing_stats.processing_duration
            await ctx.info(f"🎯 Plan-then-Execute indexing completed in {duration:.2f} seconds")
            
            return final_status
            
        except Exception as e:
            self._current_status.overall_status = ProcessingStatus.FAILED
            self._current_status.current_operation = f"Indexing failed: {str(e)}"
            self._current_status.processing_stats.add_error(f"Plan-then-Execute indexing failed: {str(e)}")
            self._current_status.processing_stats.processing_end_time = datetime.now()
            
            logger.error(f"Plan-then-Execute indexing failed: {e}", exc_info=True)
            await ctx.error(f"Plan-then-Execute indexing failed: {str(e)}")
            
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
        Uses RebuildDecisionEngine.should_rebuild_directory() for centralized decision-making.
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
        Uses RebuildDecisionEngine.should_rebuild_directory() for each directory.
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
            
            # Step 3: Apply centralized decision engine to current directory (handles project root and other special cases)
            decision = await self.rebuild_decision_engine.should_rebuild_directory(
                directory_context_with_updated_children, self._source_root, ctx
            )
            
            # Step 4: Update processing status based on decision result
            if decision.outcome == DecisionOutcome.REBUILD:
                # Changes detected - mark for processing
                await ctx.debug(f"Directory needs processing: {directory_context.directory_path.name} - {decision.reason.value}")
                processing_status = ProcessingStatus.PENDING
            else:
                # No changes detected - skip processing
                await ctx.debug(f"Directory up to date: {directory_context.directory_path.name} - {decision.reasoning_text}")
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
    
    # Plan-then-Execute Architecture Methods
    
    async def _generate_execution_plan(
        self, 
        root_context: DirectoryContext, 
        decision_report: DecisionReport, 
        root_path: Path, 
        ctx: Context
    ) -> ExecutionPlan:
        """
        [Class method intent]
        Converts DecisionReport into atomic ExecutionPlan using PlanGenerator.
        Creates comprehensive execution plan with proper task dependencies and resource estimation.

        [Design principles]
        Decision-to-plan translation delegating to specialized PlanGenerator component.
        Comprehensive execution planning with dependency resolution and resource estimation.
        Clear progress reporting for plan generation phase with detailed statistics.

        [Implementation details]
        Delegates plan generation to PlanGenerator.create_execution_plan() method.
        Reports plan generation results with task count and LLM call estimation.
        Returns validated ExecutionPlan ready for preview and execution.
        """
        await ctx.info("Phase 3: Generating atomic execution plan from decisions")
        
        execution_plan = await self.plan_generator.create_execution_plan(
            root_context, decision_report, root_path, ctx
        )
        
        await ctx.info(f"✅ Execution plan generated: {len(execution_plan.tasks)} tasks, {execution_plan.expensive_task_count} LLM calls")
        return execution_plan
    
    async def _preview_execution_plan(self, plan: ExecutionPlan, ctx: Context) -> None:
        """
        [Class method intent]
        Shows detailed execution plan preview before expensive operations for perfect debuggability.
        Provides comprehensive task breakdown, dependency analysis, and resource estimation.

        [Design principles]
        Perfect debuggability enabling complete execution plan understanding before expensive operations.
        Comprehensive preview with task categorization and resource estimation for informed decisions.
        No side effects ensuring preview can be called safely without affecting system state.

        [Implementation details]
        Delegates to ExecutionEngine.preview_plan() for detailed formatted output.
        Provides task breakdown, dependency validation, and execution analysis.
        Reports estimated duration and parallel execution opportunities.
        """
        await ctx.info("Phase 4: Previewing execution plan for debuggability")
        
        # Use ExecutionEngine preview capability for detailed analysis
        await self.execution_engine.preview_plan(plan, ctx)
    
    async def _execute_plan_with_progress(self, plan: ExecutionPlan, ctx: Context) -> ExecutionResults:
        """
        [Class method intent]
        Executes atomic tasks with dependency resolution and comprehensive progress reporting.
        Delegates to ExecutionEngine for atomic task execution with real-time progress updates.

        [Design principles]
        Atomic task execution with dependency resolution ensuring proper execution ordering.
        Comprehensive progress reporting providing real-time execution status and performance metrics.
        Error handling enabling graceful degradation and recovery from individual task failures.

        [Implementation details]
        Delegates to ExecutionEngine.execute_plan() for atomic task execution.
        Reports execution completion with success rate and performance metrics.
        Returns comprehensive ExecutionResults for final status creation.
        """
        await ctx.info("Phase 5: Executing atomic tasks with dependency resolution")
        
        execution_results = await self.execution_engine.execute_plan(plan, ctx)
        
        await ctx.info(f"🎯 Execution completed: {execution_results.success_rate:.1%} success rate")
        await ctx.info(f"📊 Performance: {execution_results.llm_calls_made} LLM calls, {execution_results.total_duration:.1f}s total")
        
        return execution_results
    
    def _create_final_status(self, execution_results: ExecutionResults) -> IndexingStatus:
        """
        [Class method intent]
        Converts ExecutionResults to IndexingStatus format for consistent API compatibility.
        Maps execution metrics to processing statistics and status information.

        [Design principles]
        Result mapping ensuring consistent API compatibility with existing IndexingStatus format.
        Comprehensive statistics mapping preserving all performance metrics and error information.
        Status determination based on execution results and success rates.

        [Implementation details]
        Maps ExecutionResults performance metrics to ProcessingStats format.
        Determines overall processing status based on execution success rates and error counts.
        Preserves all error information and performance metrics for comprehensive reporting.
        """
        # Update current status with execution results
        self._current_status.processing_stats.processing_end_time = execution_results.execution_end or datetime.now()
        
        # Map execution results to processing statistics
        stats = self._current_status.processing_stats
        stats.files_processed = execution_results.files_processed
        stats.files_completed = execution_results.files_processed
        stats.files_failed = len(execution_results.failed_tasks)
        stats.directories_processed = execution_results.directories_processed
        stats.directories_completed = execution_results.directories_processed
        
        # Add any execution errors to statistics
        for task_id, error in execution_results.failed_tasks:
            stats.add_error(f"Task {task_id} failed: {error}")
        
        # Determine overall status
        if execution_results.success_rate >= 0.9:  # 90% success rate threshold
            self._current_status.overall_status = ProcessingStatus.COMPLETED
            self._current_status.current_operation = "Indexing completed successfully"
        elif execution_results.success_rate >= 0.5:  # 50% success rate threshold
            self._current_status.overall_status = ProcessingStatus.COMPLETED  # Partial success
            self._current_status.current_operation = f"Indexing completed with {len(execution_results.failed_tasks)} failures"
        else:
            self._current_status.overall_status = ProcessingStatus.FAILED
            self._current_status.current_operation = f"Indexing failed: {execution_results.success_rate:.1%} success rate"
        
        return self._current_status

    async def cleanup(self) -> None:
        """
        [Class method intent]
        Cleans up hierarchical indexer resources including execution engine and plan generator components.
        Ensures proper resource cleanup and connection closure for all Plan-then-Execute dependencies.

        [Design principles]
        Comprehensive resource cleanup ensuring no resource leaks or connection issues.
        Component cleanup delegation enabling proper resource management across Plan-then-Execute architecture.
        Error handling preventing cleanup failures from cascading to calling code.

        [Implementation details]
        Delegates cleanup to ExecutionEngine for proper resource management.
        Handles cleanup errors gracefully with appropriate logging and error reporting.
        """
        try:
            if hasattr(self, 'execution_engine') and self.execution_engine:
                await self.execution_engine._cleanup_execution_resources()
            
            logger.info("HierarchicalIndexer cleanup completed")
        except Exception as e:
            logger.warning(f"HierarchicalIndexer cleanup error: {e}")

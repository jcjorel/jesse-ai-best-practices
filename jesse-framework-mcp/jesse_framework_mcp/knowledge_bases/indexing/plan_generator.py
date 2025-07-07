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
# Plan Generator for converting RebuildDecisionEngine decisions into atomic task execution plans.
# Implements decision-to-plan translation creating comprehensive ExecutionPlan objects with proper
# task dependencies and resource estimation for Plan-then-Execute architecture.
###############################################################################
# [Source file design principles]
# - Decision-to-Plan translation converting RebuildDecisionEngine outputs into atomic executable tasks
# - Dependency-aware task creation ensuring proper execution ordering for hierarchical processing
# - Comprehensive task metadata embedding all execution parameters for independent task execution
# - Resource estimation providing accurate duration and complexity assessment for execution planning
# - Atomic task decomposition ensuring each task represents single idempotent operation
###############################################################################
# [Source file constraints]
# - All generated tasks must be atomic and idempotent ensuring safe re-execution scenarios
# - Task dependencies must correctly represent hierarchical processing requirements
# - Generated plans must contain all information needed for execution without external state
# - Performance estimates must be realistic for meaningful progress reporting
# - Plan generation must be fast enabling quick debugging and verification workflows
###############################################################################
# [Dependencies]
# <codebase>: ..models.indexing_config - Configuration and processing parameters
# <codebase>: ..models.knowledge_context - Context structures for task creation
# <codebase>: ..models.rebuild_decisions - Decision inputs for plan generation
# <codebase>: ..models.execution_plan - Task models and execution planning structures
# <system>: pathlib - Cross-platform path operations and file metadata
# <system>: logging - Structured logging for plan generation analysis
###############################################################################
# [GenAI tool change history]
# 2025-07-07T15:02:00Z : CRITICAL HANDLER PATH FIX - Fixed task metadata to include handler-determined KB paths by CodeAssistant
# * FIXED CRITICAL BUG: Modified _generate_directory_tasks_recursive() to include knowledge_file_path in task metadata
# * BEFORE: Task metadata contained only paths but not handler-determined KB file paths causing ExecutionEngine to use cache defaults
# * AFTER: Task metadata now includes both main directory KB path and subdirectory KB paths from DirectoryContext
# * Added knowledge_file_path extraction from DirectoryContext.knowledge_file_path for main directory tasks
# * Added knowledge_file_path extraction for each subdirectory context in metadata
# * ENABLES HANDLER CONTROL: ExecutionEngine can now access handler-determined paths from task metadata instead of computing its own
# 2025-07-06T20:10:00Z : Initial implementation of Plan Generator for Plan-then-Execute architecture by CodeAssistant
# * Created comprehensive decision-to-plan translation converting RebuildDecisionEngine decisions into atomic tasks
# * Implemented dependency-aware task creation ensuring proper execution ordering for hierarchical knowledge building
# * Added resource estimation and task metadata embedding for independent task execution without external state
# * Designed atomic task decomposition with comprehensive validation and debugging capabilities
###############################################################################

"""
Plan Generator for Knowledge Bases Execution Planning.

This module converts RebuildDecisionEngine decisions into comprehensive ExecutionPlan
objects containing atomic tasks with proper dependencies and resource estimation
for reliable Plan-then-Execute architecture implementation.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

from fastmcp import Context

from ..models import (
    IndexingConfig,
    DirectoryContext,
    FileContext
)
from ..models.rebuild_decisions import (
    DecisionReport,
    RebuildDecision,
    DeletionDecision,
    DecisionOutcome,
    DecisionReason
)
from ..models.execution_plan import (
    ExecutionPlan,
    AtomicTask,
    TaskType,
    ExecutionResults
)

logger = logging.getLogger(__name__)


class PlanGenerator:
    """
    [Class intent]
    Converts RebuildDecisionEngine decisions into comprehensive atomic task execution plans.
    Transforms decision reports into ExecutionPlan objects with proper task dependencies,
    resource estimation, and complete execution metadata for Plan-then-Execute architecture.

    [Design principles]
    Decision-to-plan translation creating atomic executable tasks from high-level decisions.
    Dependency-aware task generation ensuring proper hierarchical processing order.
    Comprehensive metadata embedding eliminating external state dependencies during execution.
    Resource estimation providing accurate planning information for execution optimization.
    Fast plan generation enabling quick debugging and verification without expensive operations.

    [Implementation details]
    Processes DecisionReport objects creating corresponding atomic tasks for each decision.
    Generates proper task dependencies ensuring files are processed before directories.
    Embeds all execution parameters in task metadata for independent execution.
    Provides performance estimation based on task type and file characteristics.
    Creates complete ExecutionPlan objects ready for validation and execution.
    """
    
    def __init__(self, config: IndexingConfig):
        """
        [Class method intent]
        Initializes plan generator with configuration for task estimation and metadata generation.
        Sets up performance estimation parameters and task creation templates.

        [Design principles]
        Configuration-driven behavior enabling accurate task estimation and metadata generation.
        Performance estimation setup providing realistic duration and complexity assessment.
        Task template preparation enabling consistent atomic task creation across all operations.

        [Implementation details]
        Stores configuration for task estimation and metadata embedding.
        Initializes performance estimation parameters based on system characteristics.
        Sets up task creation templates for consistent atomic task generation.
        """
        self.config = config
        
        # Performance estimation parameters
        self.llm_analysis_duration = 30.0  # Average seconds per LLM file analysis
        self.kb_generation_duration = 15.0  # Average seconds per directory KB generation
        self.file_operation_duration = 0.1   # Average seconds per file operation
        self.cleanup_operation_duration = 0.05  # Average seconds per cleanup operation
        
        logger.info("Initialized PlanGenerator with performance estimation parameters")
    
    async def create_execution_plan(
        self,
        root_context: DirectoryContext,
        decision_report: DecisionReport,
        source_root: Path,
        ctx: Context
    ) -> ExecutionPlan:
        """
        [Class method intent]
        Creates comprehensive ExecutionPlan from RebuildDecisionEngine decisions and directory context.
        Converts high-level decisions into atomic tasks with proper dependencies and resource estimation.

        [Design principles]
        Complete decision-to-plan translation ensuring all decisions are represented as executable tasks.
        Dependency-aware task creation ensuring proper execution ordering for hierarchical processing.
        Comprehensive task validation ensuring generated plan is executable and consistent.
        Resource estimation providing accurate execution planning information.

        [Implementation details]
        Processes cleanup decisions first to create deletion tasks.
        Processes file decisions to create analysis or skip tasks with proper dependencies.
        Processes directory decisions to create KB generation tasks depending on file tasks.
        Adds cache structure creation and verification tasks for complete execution coverage.
        Validates generated plan ensuring all dependencies are resolvable and execution is feasible.

        Args:
            root_context: Root directory context containing complete hierarchy information
            decision_report: Decisions from RebuildDecisionEngine for all operations
            source_root: Source root path for relative path calculation and metadata embedding
            ctx: FastMCP context for progress reporting during plan generation

        Returns:
            ExecutionPlan: Complete execution plan with atomic tasks and dependencies
        """
        await ctx.info(f"Generating execution plan from {decision_report.total_decisions} decisions")
        
        # Create execution plan
        plan = ExecutionPlan(
            source_root=source_root,
            plan_id=f"plan_{int(datetime.now().timestamp())}"
        )
        
        # Phase 1: Generate cleanup tasks (no dependencies, execute first)
        await self._generate_cleanup_tasks(decision_report, plan, ctx)
        
        # Phase 2: Generate cache structure task (no dependencies, execute early)
        await self._generate_cache_structure_task(root_context, source_root, plan, ctx)
        
        # Phase 3: Generate file tasks (depend on cleanup and cache structure)
        await self._generate_file_tasks(root_context, decision_report, source_root, plan, ctx)
        
        # Phase 4: Generate directory tasks (depend on file tasks)
        await self._generate_directory_tasks(root_context, decision_report, source_root, plan, ctx)
        
        # Phase 5: Generate verification tasks (depend on all processing tasks)
        await self._generate_verification_tasks(root_context, decision_report, source_root, plan, ctx)
        
        # Validate generated plan
        validation_errors = plan.validate_dependencies()
        if validation_errors:
            error_msg = f"Generated plan has validation errors: {validation_errors}"
            await ctx.error(f"❌ PLAN VALIDATION FAILED: {error_msg}")
            raise RuntimeError(error_msg)
        
        await ctx.info(f"✅ Execution plan generated: {len(plan.tasks)} tasks, {plan.expensive_task_count} LLM calls")
        return plan
    
    async def _generate_cleanup_tasks(
        self,
        decision_report: DecisionReport,
        plan: ExecutionPlan,
        ctx: Context
    ) -> None:
        """
        [Class method intent]
        Generates cleanup tasks for orphaned file and directory deletion.
        Creates atomic deletion tasks with safety validation and proper metadata.

        [Design principles]
        Safety-first deletion task generation ensuring only safe deletions are performed.
        Atomic deletion operations enabling individual task success/failure tracking.
        Complete metadata embedding including deletion reasoning and safety validation.

        [Implementation details]
        Processes all deletion decisions from decision report.
        Creates DELETE_ORPHANED_FILE or DELETE_ORPHANED_DIRECTORY tasks as appropriate.
        Embeds safety validation and deletion reasoning in task metadata.
        Sets no dependencies enabling cleanup tasks to execute first.
        """
        cleanup_tasks_created = 0
        
        for file_path in decision_report.files_to_delete:
            deletion_decision = decision_report.get_decision_for_path(file_path)
            
            if not deletion_decision or not deletion_decision.is_safe_to_delete:
                await ctx.warning(f"Skipping unsafe deletion: {file_path}")
                continue
            
            # Determine task type based on path type
            if file_path.is_dir() or file_path.name.endswith('/'):
                task_type = TaskType.DELETE_ORPHANED_DIRECTORY
            else:
                task_type = TaskType.DELETE_ORPHANED_FILE
            
            task = AtomicTask(
                task_id=f"cleanup_{file_path.name}_{int(datetime.now().timestamp())}",
                task_type=task_type,
                target_path=file_path,
                dependencies=[],  # Cleanup tasks have no dependencies
                estimated_duration=self.cleanup_operation_duration,
                priority=100,  # High priority - execute first
                metadata={
                    'deletion_reason': deletion_decision.reasoning_text,
                    'is_safe_to_delete': deletion_decision.is_safe_to_delete,
                    'decision_outcome': deletion_decision.outcome.value,
                    'decision_reason': deletion_decision.reason.value
                }
            )
            
            plan.add_task(task)
            cleanup_tasks_created += 1
        
        await ctx.debug(f"Generated {cleanup_tasks_created} cleanup tasks")
    
    async def _generate_cache_structure_task(
        self,
        root_context: DirectoryContext,
        source_root: Path,
        plan: ExecutionPlan,
        ctx: Context
    ) -> None:
        """
        [Class method intent]
        Generates cache structure creation task for upfront directory preparation.
        Creates single atomic task to pre-create all necessary cache directories.

        [Design principles]
        Single cache structure task eliminating race conditions during concurrent processing.
        Complete directory inventory embedding all cache directories needed for processing.
        Early execution priority ensuring cache structure exists before file processing begins.

        [Implementation details]
        Analyzes root context to identify all directories requiring cache structure creation.
        Creates single CREATE_CACHE_STRUCTURE task with complete directory inventory.
        Sets high priority and no dependencies enabling early execution.
        Embeds complete directory list in metadata for independent execution.
        """
        # Collect all directories that will need cache structure
        cache_directories = []
        self._collect_cache_directories(root_context, source_root, cache_directories)
        
        if cache_directories:
            task = AtomicTask(
                task_id="create_cache_structure",
                task_type=TaskType.CREATE_CACHE_STRUCTURE,
                target_path=source_root,
                dependencies=[],  # No dependencies - execute early
                estimated_duration=len(cache_directories) * 0.01,  # Fast directory creation
                priority=90,  # High priority - execute early
                metadata={
                    'directories': cache_directories,
                    'source_root': str(source_root),
                    'total_directories': len(cache_directories)
                }
            )
            
            plan.add_task(task)
            await ctx.debug(f"Generated cache structure task for {len(cache_directories)} directories")
    
    def _collect_cache_directories(
        self,
        directory_context: DirectoryContext,
        source_root: Path,
        cache_directories: List[str]
    ) -> None:
        """
        [Class method intent]
        Recursively collects all directories requiring cache structure creation.
        Traverses directory hierarchy identifying all directories with processable files.

        [Design principles]
        Complete directory inventory ensuring no cache directories are missed during structure creation.
        Recursive traversal maintaining consistency with hierarchical processing approach.
        Path string collection enabling serializable metadata embedding in cache structure task.

        [Implementation details]
        Recursively traverses directory context collecting directories with files requiring cache.
        Converts directory paths to strings for metadata embedding and serialization.
        Builds comprehensive list covering entire hierarchy for complete cache structure creation.
        """
        # Add current directory if it has processable files
        if directory_context.file_contexts:
            cache_directories.append(str(directory_context.directory_path))
        
        # Recursively collect from subdirectories
        for subdir_context in directory_context.subdirectory_contexts:
            self._collect_cache_directories(subdir_context, source_root, cache_directories)
    
    async def _generate_file_tasks(
        self,
        root_context: DirectoryContext,
        decision_report: DecisionReport,
        source_root: Path,
        plan: ExecutionPlan,
        ctx: Context
    ) -> None:
        """
        [Class method intent]
        Generates file processing tasks based on RebuildDecisionEngine file decisions.
        Creates atomic tasks for LLM analysis or cache skip operations with proper dependencies.

        [Design principles]
        Decision-driven task generation ensuring tasks match RebuildDecisionEngine decisions exactly.
        Atomic file operations enabling individual file success/failure tracking and debugging.
        Complete metadata embedding including file characteristics and processing parameters.
        Dependency creation ensuring file tasks execute after cleanup and cache structure creation.

        [Implementation details]
        Recursively processes directory hierarchy collecting all file contexts.
        Matches file decisions from decision report to create appropriate task types.
        Creates ANALYZE_FILE_LLM tasks for files requiring processing.
        Creates SKIP_FILE_CACHED tasks for files with fresh cache (for tracking and debugging).
        Embeds complete file metadata enabling independent task execution.
        """
        file_tasks_created = 0
        
        # Get dependencies that file tasks should wait for
        base_dependencies = self._get_base_dependencies(plan)
        
        # Recursively generate file tasks
        await self._generate_file_tasks_recursive(
            root_context, decision_report, source_root, plan, base_dependencies, ctx
        )
        
        # Count file tasks created
        file_tasks_created = len([t for t in plan.tasks if t.task_type in {TaskType.ANALYZE_FILE_LLM, TaskType.SKIP_FILE_CACHED}])
        await ctx.debug(f"Generated {file_tasks_created} file tasks")
    
    async def _generate_file_tasks_recursive(
        self,
        directory_context: DirectoryContext,
        decision_report: DecisionReport,
        source_root: Path,
        plan: ExecutionPlan,
        base_dependencies: List[str],
        ctx: Context
    ) -> None:
        """
        [Class method intent]
        Recursively generates file tasks for entire directory hierarchy.
        Processes each directory's files and recurses into subdirectories for complete coverage.

        [Design principles]
        Comprehensive file task generation ensuring no files are missed during plan creation.
        Recursive traversal maintaining consistency with hierarchical processing approach.
        Decision matching ensuring generated tasks exactly reflect RebuildDecisionEngine decisions.

        [Implementation details]
        Processes all files in current directory creating appropriate tasks based on decisions.
        Recursively processes subdirectories ensuring complete hierarchy coverage.
        Maintains consistent task ID generation and dependency management across hierarchy.
        """
        # Process files in current directory
        for file_context in directory_context.file_contexts:
            # Find corresponding decision for this file
            rebuild_decision = decision_report.get_decision_for_path(file_context.file_path)
            
            if not rebuild_decision:
                await ctx.warning(f"No decision found for file: {file_context.file_path}")
                continue
            
            # Create appropriate task based on decision
            if rebuild_decision.outcome == DecisionOutcome.REBUILD:
                task_type = TaskType.ANALYZE_FILE_LLM
                estimated_duration = self.llm_analysis_duration
                priority = 50  # Medium priority
            else:  # SKIP
                task_type = TaskType.SKIP_FILE_CACHED
                estimated_duration = self.file_operation_duration
                priority = 40  # Lower priority
            
            task = AtomicTask(
                task_id=f"file_{self._sanitize_path_for_id(file_context.file_path)}",
                task_type=task_type,
                target_path=file_context.file_path,
                dependencies=base_dependencies.copy(),
                estimated_duration=estimated_duration,
                priority=priority,
                metadata={
                    'file_size': file_context.file_size,
                    'last_modified': file_context.last_modified.isoformat(),
                    'source_root': str(source_root),
                    'decision_outcome': rebuild_decision.outcome.value,
                    'decision_reason': rebuild_decision.reason.value,
                    'decision_reasoning': rebuild_decision.reasoning_text
                }
            )
            
            plan.add_task(task)
        
        # Recursively process subdirectories
        for subdir_context in directory_context.subdirectory_contexts:
            await self._generate_file_tasks_recursive(
                subdir_context, decision_report, source_root, plan, base_dependencies, ctx
            )
    
    async def _generate_directory_tasks(
        self,
        root_context: DirectoryContext,
        decision_report: DecisionReport,
        source_root: Path,
        plan: ExecutionPlan,
        ctx: Context
    ) -> None:
        """
        [Class method intent]
        Generates directory knowledge building tasks based on RebuildDecisionEngine directory decisions.
        Creates atomic tasks for KB generation or skip operations with proper file task dependencies.

        [Design principles]
        Decision-driven task generation ensuring tasks match RebuildDecisionEngine directory decisions.
        Hierarchical dependency creation ensuring directories depend on their constituent files.
        Complete context embedding including file and subdirectory contexts for KB generation.
        Atomic directory operations enabling individual directory success/failure tracking.

        [Implementation details]
        Recursively processes directory hierarchy in leaf-first order for proper dependency management.
        Matches directory decisions from decision report to create appropriate task types.
        Creates CREATE_DIRECTORY_KB tasks for directories requiring knowledge file generation.
        Creates SKIP_DIRECTORY_FRESH tasks for directories with fresh KB files.
        Establishes dependencies ensuring directory tasks execute after their constituent file tasks.
        """
        directory_tasks_created = 0
        
        # Generate directory tasks recursively (leaf-first for proper dependencies)
        await self._generate_directory_tasks_recursive(
            root_context, decision_report, source_root, plan, ctx
        )
        
        # Count directory tasks created
        directory_tasks_created = len([t for t in plan.tasks if t.task_type in {TaskType.CREATE_DIRECTORY_KB, TaskType.SKIP_DIRECTORY_FRESH}])
        await ctx.debug(f"Generated {directory_tasks_created} directory tasks")
    
    async def _generate_directory_tasks_recursive(
        self,
        directory_context: DirectoryContext,
        decision_report: DecisionReport,
        source_root: Path,
        plan: ExecutionPlan,
        ctx: Context
    ) -> str:
        """
        [Class method intent]
        Recursively generates directory tasks in leaf-first order with proper horizontal dependencies.
        Processes subdirectories first, then creates task for current directory depending on children AND siblings.
        Implements horizontal dependency management ensuring parent directories wait for ALL sibling completion.

        [Design principles]
        Leaf-first processing ensuring proper dependency order for hierarchical knowledge building.
        Horizontal dependency tracking ensuring parent directories wait for ALL sibling directories.
        Task ID return enabling parent directories to depend on child directory tasks.
        Comprehensive dependency management supporting selective cascading architecture.

        [Implementation details]
        Recursively processes subdirectories first collecting their task IDs.
        Collects sibling directory task IDs to establish horizontal dependencies.
        Creates directory task depending on all file tasks, subdirectory tasks, AND sibling tasks.
        Returns task ID enabling parent directories to establish proper dependencies.
        Handles both knowledge generation and skip scenarios based on decisions.

        Args:
            directory_context: Directory context for current directory
            decision_report: Decisions from RebuildDecisionEngine
            source_root: Source root path for metadata embedding
            plan: ExecutionPlan to add tasks to
            ctx: FastMCP context for progress reporting

        Returns:
            str: Task ID of created directory task for dependency tracking
        """
        # First, recursively process subdirectories (leaf-first)
        subdirectory_task_ids = []
        for subdir_context in directory_context.subdirectory_contexts:
            subdir_task_id = await self._generate_directory_tasks_recursive(
                subdir_context, decision_report, source_root, plan, ctx
            )
            if subdir_task_id:
                subdirectory_task_ids.append(subdir_task_id)
        
        # Find corresponding decision for this directory
        rebuild_decision = decision_report.get_decision_for_path(directory_context.directory_path)
        
        if not rebuild_decision:
            await ctx.warning(f"No decision found for directory: {directory_context.directory_path}")
            return None
        
        # Collect dependencies: file tasks + subdirectory tasks (no sibling dependencies to avoid circular deps)
        dependencies = []
        
        # Add file task dependencies (files in this directory)
        for file_context in directory_context.file_contexts:
            file_task_id = f"file_{self._sanitize_path_for_id(file_context.file_path)}"
            dependencies.append(file_task_id)
        
        # Add subdirectory task dependencies (direct children)
        # This naturally ensures horizontal synchronization: parent waits for ALL its children
        dependencies.extend(subdirectory_task_ids)
        
        if subdirectory_task_ids:
            await ctx.debug(f"🔗 PARENT DEPS: {directory_context.directory_path.name} waits for {len(subdirectory_task_ids)} child directories")
        
        # Create appropriate task based on decision
        if rebuild_decision.outcome == DecisionOutcome.REBUILD:
            task_type = TaskType.CREATE_DIRECTORY_KB
            estimated_duration = self.kb_generation_duration
            priority = 30  # Lower priority - execute after files
        else:  # SKIP
            task_type = TaskType.SKIP_DIRECTORY_FRESH
            estimated_duration = self.file_operation_duration
            priority = 20  # Lower priority
        
        task_id = f"dir_{self._sanitize_path_for_id(directory_context.directory_path)}"
        
        task = AtomicTask(
            task_id=task_id,
            task_type=task_type,
            target_path=directory_context.directory_path,
            dependencies=dependencies,
            estimated_duration=estimated_duration,
            priority=priority,
            metadata={
                'source_root': str(source_root),
                # SIMPLIFIED: knowledge_file_path is now correctly set by handler during discovery
                'knowledge_file_path': str(directory_context.knowledge_file_path),
                'file_contexts': [
                    {
                        'path': str(fc.file_path),
                        'size': fc.file_size,
                        'last_modified': fc.last_modified.isoformat()
                    }
                    for fc in directory_context.file_contexts
                ],
                'subdirectory_contexts': [
                    {
                        'path': str(sc.directory_path),
                        # SIMPLIFIED: knowledge_file_path is now correctly set by handler
                        'knowledge_file_path': str(sc.knowledge_file_path)
                    }
                    for sc in directory_context.subdirectory_contexts
                ],
                'child_dependencies': len(subdirectory_task_ids),
                'decision_outcome': rebuild_decision.outcome.value,
                'decision_reason': rebuild_decision.reason.value,
                'decision_reasoning': rebuild_decision.reasoning_text
            }
        )
        
        plan.add_task(task)
        return task_id
    
    async def _generate_verification_tasks(
        self,
        root_context: DirectoryContext,
        decision_report: DecisionReport,
        source_root: Path,
        plan: ExecutionPlan,
        ctx: Context
    ) -> None:
        """
        [Class method intent]
        Generates verification tasks to validate execution results and ensure system consistency.
        Creates atomic tasks for cache freshness and KB freshness verification after processing.

        [Design principles]
        Post-execution verification ensuring system consistency after all processing tasks complete.
        Atomic verification operations enabling individual verification success/failure tracking.
        Complete dependency setup ensuring verification only occurs after all processing is complete.

        [Implementation details]
        Creates verification tasks that depend on all processing tasks.
        Generates VERIFY_CACHE_FRESHNESS tasks for files that were processed.
        Generates VERIFY_KB_FRESHNESS tasks for directories that had KB files created.
        Sets lowest priority ensuring verification occurs last in execution order.
        """
        verification_tasks_created = 0
        
        # Get all processing task IDs for dependencies
        processing_task_ids = [
            t.task_id for t in plan.tasks 
            if t.task_type in {TaskType.ANALYZE_FILE_LLM, TaskType.CREATE_DIRECTORY_KB}
        ]
        
        # Create cache verification tasks for processed files
        for task in plan.tasks:
            if task.task_type == TaskType.ANALYZE_FILE_LLM:
                verify_task = AtomicTask(
                    task_id=f"verify_cache_{self._sanitize_path_for_id(task.target_path)}",
                    task_type=TaskType.VERIFY_CACHE_FRESHNESS,
                    target_path=task.target_path,
                    dependencies=[task.task_id],  # Depend on the analysis task
                    estimated_duration=0.01,  # Very fast verification
                    priority=10,  # Low priority - execute last
                    metadata={
                        'source_root': str(source_root),
                        'analysis_task_id': task.task_id
                    }
                )
                
                plan.add_task(verify_task)
                verification_tasks_created += 1
        
        # Create KB verification tasks for created directories
        for task in plan.tasks:
            if task.task_type == TaskType.CREATE_DIRECTORY_KB:
                verify_task = AtomicTask(
                    task_id=f"verify_kb_{self._sanitize_path_for_id(task.target_path)}",
                    task_type=TaskType.VERIFY_KB_FRESHNESS,
                    target_path=task.target_path,
                    dependencies=[task.task_id],  # Depend on the KB creation task
                    estimated_duration=0.01,  # Very fast verification
                    priority=10,  # Low priority - execute last
                    metadata={
                        'source_root': str(source_root),
                        'kb_task_id': task.task_id
                    }
                )
                
                plan.add_task(verify_task)
                verification_tasks_created += 1
        
        await ctx.debug(f"Generated {verification_tasks_created} verification tasks")
    
    def _get_base_dependencies(self, plan: ExecutionPlan) -> List[str]:
        """
        [Class method intent]
        Gets base dependencies that file and directory tasks should depend on.
        Returns list of task IDs for cleanup and structure tasks that should execute first.

        [Design principles]
        Consistent base dependency setup ensuring all processing tasks wait for preparation tasks.
        Simple dependency management avoiding complex dependency graph calculations.
        Clear execution ordering ensuring cleanup and structure creation occur before processing.

        [Implementation details]
        Identifies cleanup and structure creation tasks from current plan.
        Returns their task IDs for use as base dependencies in file and directory tasks.
        Enables simple dependency management ensuring proper execution ordering.
        """
        base_deps = []
        
        for task in plan.tasks:
            if task.task_type in {
                TaskType.DELETE_ORPHANED_FILE,
                TaskType.DELETE_ORPHANED_DIRECTORY,
                TaskType.CREATE_CACHE_STRUCTURE
            }:
                base_deps.append(task.task_id)
        
        return base_deps
    
    def _collect_sibling_directory_tasks(
        self,
        directory_context: DirectoryContext,
        decision_report: DecisionReport,
        source_root: Path,
        plan: ExecutionPlan,
        ctx: Context
    ) -> List[str]:
        """
        [Class method intent]
        Collects task IDs for sibling directories at the same hierarchical level that require rebuilding.
        Implements horizontal dependency management ensuring parent directories wait for ALL sibling completion.

        [Design principles]
        Horizontal dependency collection ensuring proper sibling synchronization before parent processing.
        Decision-based filtering ensuring only rebuilding siblings create dependencies.
        Task ID matching enabling reliable dependency resolution during execution.
        Performance optimization through early filtering and efficient sibling identification.

        [Implementation details]
        Identifies parent directory context to find sibling directories at same level.
        Filters sibling directories based on rebuild decisions from RebuildDecisionEngine.
        Generates task IDs for rebuilding siblings using consistent ID generation patterns.
        Returns list of sibling task IDs for horizontal dependency establishment.

        Args:
            directory_context: Current directory context for sibling identification
            decision_report: Decisions from RebuildDecisionEngine for filtering siblings
            source_root: Source root path for context calculations
            plan: ExecutionPlan for task ID verification (future enhancement)
            ctx: FastMCP context for progress reporting

        Returns:
            List[str]: Task IDs of sibling directories that require rebuilding
        """
        sibling_task_ids = []
        
        try:
            # Find parent directory path to identify siblings
            parent_path = directory_context.directory_path.parent
            
            # For root directory, no siblings exist
            if directory_context.directory_path == source_root:
                return sibling_task_ids
            
            # Scan decision report for directories at same level (siblings)
            for rebuild_decision in decision_report.rebuild_decisions.values():
                candidate_path = rebuild_decision.path
                
                # Check if this is a sibling directory (same parent, different from current)
                if (candidate_path != directory_context.directory_path and  # Not current directory
                    candidate_path.parent == parent_path and               # Same parent (sibling)
                    rebuild_decision.should_rebuild):                      # Requires rebuilding
                    
                    # Generate task ID for sibling directory
                    sibling_task_id = f"dir_{self._sanitize_path_for_id(candidate_path)}"
                    sibling_task_ids.append(sibling_task_id)
                    
                    logger.debug(f"Found sibling dependency: {directory_context.directory_path.name} waits for {candidate_path.name}")
            
            return sibling_task_ids
            
        except Exception as e:
            logger.warning(f"Failed to collect sibling directory tasks for {directory_context.directory_path}: {e}")
            return []

    def _sanitize_path_for_id(self, path: Path) -> str:
        """
        [Class method intent]
        Sanitizes file paths for use in task IDs ensuring valid identifier generation.
        Converts path separators and special characters to underscores for safe task ID creation.

        [Design principles]
        Safe task ID generation preventing invalid characters in task identifiers.
        Consistent ID format enabling reliable task identification and dependency resolution.
        Path-based ID generation ensuring unique task IDs for different files and directories.

        [Implementation details]
        Replaces path separators and special characters with underscores.
        Handles both forward and backward slashes for cross-platform compatibility.
        Returns sanitized string suitable for use as task ID component.
        """
        # Convert path to string and replace problematic characters
        path_str = str(path).replace('/', '_').replace('\\', '_').replace('.', '_').replace(' ', '_')
        
        # Remove multiple consecutive underscores
        while '__' in path_str:
            path_str = path_str.replace('__', '_')
        
        # Remove leading/trailing underscores
        return path_str.strip('_')

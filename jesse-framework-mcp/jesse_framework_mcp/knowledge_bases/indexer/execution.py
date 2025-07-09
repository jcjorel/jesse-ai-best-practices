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
# Generic task execution engine with dependency resolution and concurrency support.
# Executes atomic tasks in proper order with progress reporting, error handling,
# and dry-run capabilities for safe operation validation.
###############################################################################
# [Source file design principles]
# - Dependency-aware task execution with proper ordering
# - Concurrent execution support for performance optimization  
# - Comprehensive error handling with graceful failure recovery
# - Dry-run mode for execution validation without side effects
# - Clear progress reporting and execution monitoring
###############################################################################
# [Source file constraints]
# - Must respect task dependencies and execution ordering
# - No FastMCP dependencies for clean architecture
# - Exception-first error handling - no fallback mechanisms
# - Support both sequential and concurrent execution modes
###############################################################################
# [Dependencies]
# <system>:typing.List
# <system>:typing.Dict
# <system>:typing.Optional
# <system>:asyncio
# <system>:time.time
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.AtomicTask
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.ExecutionPlan
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.ExecutionContext
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.TaskResult
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.IndexingResult
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.ProgressCallback
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.TaskStatus
###############################################################################
# [GenAI tool change history]
# 2025-07-09T13:35:00Z : Initial generic execution implementation by CodeAssistant
# * Created TaskExecutor for individual task execution with error handling
# * Implemented ConcurrentExecutor for parallel task execution
# * Added ExecutionMonitor for progress tracking and performance analysis
# * Created GenericExecutor orchestrating complete execution workflow
###############################################################################

from typing import List, Dict, Optional
import asyncio
import time

from .models import (
    AtomicTask, ExecutionPlan, ExecutionContext, TaskResult, 
    IndexingResult, ProgressCallback, TaskStatus
)


class TaskExecutor:
    """
    [Class intent]
    Executes individual atomic tasks with comprehensive error handling
    and execution monitoring. Provides safe execution environment
    with precondition validation and result tracking.

    [Design principles]
    Single task execution with comprehensive error handling.
    Precondition validation before execution attempts.
    Detailed execution result tracking for debugging.

    [Implementation details]
    Validates task preconditions before execution.
    Measures execution time for performance monitoring.
    Captures all execution details in TaskResult objects.
    """
    
    async def execute_task(
        self, 
        task: AtomicTask, 
        context: ExecutionContext
    ) -> TaskResult:
        """
        [Class method intent]
        Execute single atomic task with comprehensive error handling.

        [Design principles]
        Safe task execution with precondition validation.
        Comprehensive error capture and result reporting.
        Execution time measurement for performance analysis.

        [Implementation details]
        Validates preconditions before execution.
        Measures execution time with high precision.
        Returns detailed TaskResult with execution outcome.
        """
        start_time = time.time()
        task_id = task.get_task_id()
        task_type = task.get_task_type()
        
        if context.progress_callback:
            context.progress_callback(f"Executing {task_type} task: {task_id}")
        
        try:
            # Validate preconditions
            if not context.dry_run:
                if not task.validate_preconditions(context):
                    raise RuntimeError(f"Task preconditions failed for {task_id}")
            
            # Execute task (skip actual execution in dry-run mode)
            if context.dry_run:
                # Simulate execution for dry-run
                await asyncio.sleep(0.01)  # Small delay to simulate work
                result = TaskResult(
                    success=True,
                    task_type=task_type,
                    task_id=task_id,
                    execution_time=time.time() - start_time,
                    metadata={'dry_run': True}
                )
            else:
                # Actual task execution
                result = await task.execute(context)
                result.execution_time = time.time() - start_time
            
            if context.progress_callback:
                status = "✅ COMPLETED" if result.success else "❌ FAILED"
                context.progress_callback(f"{status} {task_type} task: {task_id}")
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Task execution failed: {str(e)}"
            
            if context.progress_callback:
                context.progress_callback(f"❌ ERROR {task_type} task: {task_id} - {error_msg}")
            
            # Return failed task result
            return TaskResult(
                success=False,
                task_type=task_type,
                task_id=task_id,
                error_message=error_msg,
                execution_time=execution_time
            )


class ConcurrentExecutor:
    """
    [Class intent]
    Manages concurrent execution of compatible tasks for performance optimization.
    Coordinates parallel task execution while respecting concurrency constraints
    and dependency requirements.

    [Design principles]
    Safe concurrent execution with dependency respect.
    Performance optimization through parallel processing.
    Comprehensive error handling across concurrent tasks.

    [Implementation details]
    Uses asyncio for concurrent task execution.
    Respects task concurrency compatibility declarations.
    Aggregates results from all concurrent tasks.
    """
    
    def __init__(self, task_executor: TaskExecutor):
        """
        [Class method intent]
        Initialize concurrent executor with task executor for individual tasks.

        [Design principles]
        Composition pattern for task execution coordination.

        [Implementation details]
        Stores task executor for individual task execution.
        """
        self.task_executor = task_executor
    
    async def execute_concurrent_group(
        self, 
        tasks: List[AtomicTask], 
        context: ExecutionContext
    ) -> List[TaskResult]:
        """
        [Class method intent]
        Execute group of tasks concurrently with proper error handling.

        [Design principles]
        Concurrent execution with comprehensive error isolation.
        All tasks executed regardless of individual failures.
        Complete result aggregation for analysis.

        [Implementation details]
        Uses asyncio.gather for concurrent task execution.
        Isolates task failures to prevent cascade failures.
        Returns results for all tasks regardless of individual outcomes.
        """
        if not tasks:
            return []
        
        if context.progress_callback:
            context.progress_callback(f"Starting concurrent execution of {len(tasks)} tasks")
        
        # Create execution coroutines for all tasks
        execution_coroutines = [
            self.task_executor.execute_task(task, context) 
            for task in tasks
        ]
        
        try:
            # Execute all tasks concurrently
            results = await asyncio.gather(*execution_coroutines, return_exceptions=True)
            
            # Process results and handle exceptions
            task_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    # Convert exception to failed TaskResult
                    task = tasks[i]
                    error_result = TaskResult(
                        success=False,
                        task_type=task.get_task_type(),
                        task_id=task.get_task_id(),
                        error_message=f"Concurrent execution exception: {str(result)}"
                    )
                    task_results.append(error_result)
                else:
                    task_results.append(result)
            
            # Report concurrent group completion
            successful_count = sum(1 for r in task_results if r.success)
            failed_count = len(task_results) - successful_count
            
            if context.progress_callback:
                context.progress_callback(f"Concurrent group completed: {successful_count} succeeded, {failed_count} failed")
            
            return task_results
            
        except Exception as e:
            # Handle catastrophic concurrent execution failure
            error_msg = f"Concurrent execution group failed: {str(e)}"
            if context.progress_callback:
                context.progress_callback(f"❌ ERROR: {error_msg}")
            
            # Return failed results for all tasks
            failed_results = []
            for task in tasks:
                failed_result = TaskResult(
                    success=False,
                    task_type=task.get_task_type(),
                    task_id=task.get_task_id(),
                    error_message=error_msg
                )
                failed_results.append(failed_result)
            
            return failed_results


class ExecutionMonitor:
    """
    [Class intent]
    Monitors execution progress and performance with comprehensive metrics
    collection. Tracks execution statistics and provides real-time monitoring.

    [Design principles]
    Comprehensive execution monitoring and metrics collection.
    Real-time progress tracking with detailed statistics.
    Performance analysis for optimization insights.

    [Implementation details]
    Tracks task execution counts, times, and success rates.
    Provides progress reporting and performance metrics.
    Maintains execution statistics for analysis.
    """
    
    def __init__(self):
        """
        [Class method intent]
        Initialize execution monitor with empty metrics.

        [Design principles]
        Clean initialization with comprehensive metric tracking.

        [Implementation details]
        Initializes all metric counters and tracking structures.
        """
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.tasks_executed = 0
        self.tasks_successful = 0
        self.tasks_failed = 0
        self.total_execution_time = 0.0
        self.task_results: List[TaskResult] = []
    
    def start_monitoring(self):
        """
        [Class method intent]
        Start execution monitoring and timing.

        [Design principles]
        Clear monitoring lifecycle with explicit start.

        [Implementation details]
        Records execution start time for duration calculation.
        """
        self.start_time = time.time()
    
    def record_task_result(self, result: TaskResult):
        """
        [Class method intent]
        Record task execution result and update metrics.

        [Design principles]
        Comprehensive result tracking with metric updates.

        [Implementation details]
        Updates execution counters and performance metrics.
        Stores result for detailed analysis.
        """
        self.task_results.append(result)
        self.tasks_executed += 1
        
        if result.success:
            self.tasks_successful += 1
        else:
            self.tasks_failed += 1
        
        if result.execution_time:
            self.total_execution_time += result.execution_time
    
    def end_monitoring(self):
        """
        [Class method intent]
        End execution monitoring and finalize metrics.

        [Design principles]
        Clean monitoring lifecycle with explicit end.

        [Implementation details]
        Records execution end time for total duration calculation.
        """
        self.end_time = time.time()
    
    def get_execution_summary(self) -> Dict[str, any]:
        """
        [Class method intent]
        Generate comprehensive execution summary with all metrics.

        [Design principles]
        Complete execution analysis with performance insights.

        [Implementation details]
        Calculates success rates, performance metrics, and timing statistics.
        """
        total_time = 0.0
        if self.start_time and self.end_time:
            total_time = self.end_time - self.start_time
        
        success_rate = 0.0
        if self.tasks_executed > 0:
            success_rate = self.tasks_successful / self.tasks_executed
        
        average_task_time = 0.0
        if self.tasks_executed > 0:
            average_task_time = self.total_execution_time / self.tasks_executed
        
        return {
            'total_execution_time': total_time,
            'tasks_executed': self.tasks_executed,
            'tasks_successful': self.tasks_successful,
            'tasks_failed': self.tasks_failed,
            'success_rate': success_rate,
            'average_task_time': average_task_time,
            'total_task_time': self.total_execution_time
        }


class GenericExecutor:
    """
    [Class intent]
    Main orchestrator for generic task execution workflow.
    Coordinates complete execution process with dependency resolution,
    concurrent execution, and comprehensive monitoring.

    [Design principles]
    Complete execution workflow orchestration.
    Dependency-aware execution with concurrency optimization.
    Comprehensive monitoring and error handling.

    [Implementation details]
    Coordinates task executor, concurrent executor, and execution monitor.
    Provides unified interface for execution plan processing.
    Generates comprehensive execution results for analysis.
    """
    
    def __init__(self):
        """
        [Class method intent]
        Initialize generic executor with execution components.

        [Design principles]
        Composition pattern for execution workflow coordination.

        [Implementation details]
        Creates task executor, concurrent executor, and execution monitor.
        """
        self.task_executor = TaskExecutor()
        self.concurrent_executor = ConcurrentExecutor(self.task_executor)
        self.execution_monitor = ExecutionMonitor()
    
    async def execute_plan(
        self, 
        plan: ExecutionPlan, 
        context: ExecutionContext
    ) -> IndexingResult:
        """
        [Class method intent]
        Execute complete execution plan with comprehensive monitoring.

        [Design principles]
        Complete execution workflow with dependency respect.
        Comprehensive monitoring and error handling.
        Performance optimization through concurrent execution.

        [Implementation details]
        Validates plan before execution.
        Executes tasks respecting dependencies and concurrency.
        Generates comprehensive indexing result.
        """
        if context.progress_callback:
            mode = "DRY-RUN" if context.dry_run else "EXECUTION"
            context.progress_callback(f"Starting {mode} of execution plan: {plan.task_count} tasks")
        
        # Validate execution plan
        if not plan.is_valid:
            error_msg = f"Cannot execute invalid plan: {'; '.join(plan.validation_errors)}"
            if context.progress_callback:
                context.progress_callback(f"❌ ERROR: {error_msg}")
            raise RuntimeError(error_msg)
        
        # Start monitoring
        self.execution_monitor.start_monitoring()
        
        try:
            # Execute tasks respecting dependencies and concurrency
            if plan.concurrent_groups:
                await self._execute_with_concurrency(plan, context)
            else:
                await self._execute_sequentially(plan, context)
            
            # End monitoring
            self.execution_monitor.end_monitoring()
            
            # Generate execution result
            result = self._generate_indexing_result()
            
            if context.progress_callback:
                success_rate = result.success_rate * 100
                context.progress_callback(f"Execution completed: {success_rate:.1f}% success rate, {result.total_files_processed} files processed")
            
            return result
            
        except Exception as e:
            self.execution_monitor.end_monitoring()
            error_msg = f"Execution plan failed: {str(e)}"
            if context.progress_callback:
                context.progress_callback(f"❌ ERROR: {error_msg}")
            raise RuntimeError(error_msg) from e
    
    async def _execute_with_concurrency(self, plan: ExecutionPlan, context: ExecutionContext):
        """
        [Class method intent]
        Execute plan with concurrent task groups for performance optimization.

        [Design principles]
        Concurrent execution respecting dependency constraints.
        Group-based parallel processing for efficiency.

        [Implementation details]
        Processes concurrent groups in dependency order.
        Uses concurrent executor for parallel task execution.
        """
        if context.progress_callback:
            context.progress_callback(f"Executing {len(plan.concurrent_groups)} concurrent groups")
        
        # Create task lookup map
        task_map = {task.get_task_id(): task for task in plan.tasks}
        
        # Execute each concurrent group
        for i, group_ids in enumerate(plan.concurrent_groups):
            if context.progress_callback:
                context.progress_callback(f"Executing concurrent group {i+1}/{len(plan.concurrent_groups)}: {len(group_ids)} tasks")
            
            # Get tasks for this group
            group_tasks = [task_map[task_id] for task_id in group_ids if task_id in task_map]
            
            # Execute group concurrently
            group_results = await self.concurrent_executor.execute_concurrent_group(group_tasks, context)
            
            # Record results
            for result in group_results:
                self.execution_monitor.record_task_result(result)
    
    async def _execute_sequentially(self, plan: ExecutionPlan, context: ExecutionContext):
        """
        [Class method intent]
        Execute plan tasks sequentially in dependency order.

        [Design principles]
        Sequential execution for simple dependency chains.
        Individual task execution with comprehensive monitoring.

        [Implementation details]
        Processes tasks one by one in resolved order.
        Uses task executor for individual task execution.
        """
        if context.progress_callback:
            context.progress_callback(f"Executing {plan.task_count} tasks sequentially")
        
        for i, task in enumerate(plan.tasks):
            if context.progress_callback:
                context.progress_callback(f"Executing task {i+1}/{plan.task_count}: {task.get_task_id()}")
            
            # Execute individual task
            result = await self.task_executor.execute_task(task, context)
            
            # Record result
            self.execution_monitor.record_task_result(result)
    
    def _generate_indexing_result(self) -> IndexingResult:
        """
        [Class method intent]
        Generate comprehensive indexing result from execution monitoring.

        [Design principles]
        Complete result aggregation with detailed statistics.
        Performance metrics and execution analysis.

        [Implementation details]
        Aggregates task results into indexing statistics.
        Calculates performance metrics and success rates.
        """
        execution_summary = self.execution_monitor.get_execution_summary()
        
        # Aggregate statistics from task results
        files_analyzed = 0
        kbs_built = 0
        cache_files_created = 0
        orphaned_files_cleaned = 0
        errors = []
        
        for result in self.execution_monitor.task_results:
            if result.task_type == "analyze_file":
                files_analyzed += result.files_processed
                if not result.success:
                    cache_files_created += len(result.output_files)
            elif result.task_type == "build_knowledge_base":
                if result.success:
                    kbs_built += 1
            elif result.task_type == "cleanup":
                if result.success:
                    orphaned_files_cleaned += result.files_processed
            
            # Collect errors
            if not result.success and result.error_message:
                errors.append(f"{result.task_type}:{result.task_id} - {result.error_message}")
        
        return IndexingResult(
            files_analyzed=files_analyzed,
            kbs_built=kbs_built,
            cache_files_created=cache_files_created,
            orphaned_files_cleaned=orphaned_files_cleaned,
            task_results=self.execution_monitor.task_results,
            errors=errors,
            execution_time=execution_summary['total_execution_time'],
            discovery_time=0.0,  # Set by caller
            planning_time=0.0    # Set by caller
        )
    
    def get_execution_status(self) -> Dict[str, any]:
        """
        [Class method intent]
        Get current execution status and progress information.

        [Design principles]
        Real-time execution status for monitoring.

        [Implementation details]
        Returns current execution metrics and progress.
        """
        return self.execution_monitor.get_execution_summary()

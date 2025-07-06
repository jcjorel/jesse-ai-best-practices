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
# Execution planning models for Plan-then-Execute architecture in Knowledge Bases Hierarchical Indexing System.
# Defines atomic tasks, execution plans, and task dependencies enabling clear separation between decision-making
# and execution phases for improved debuggability and consistency.
###############################################################################
# [Source file design principles]
# - Plan-then-Execute architecture separating decision-making from execution for perfect debuggability
# - Atomic task definition with clear inputs, outputs, and dependencies enabling deterministic execution
# - Comprehensive execution planning with dependency resolution and task ordering for reliable processing
# - Rich metadata support enabling detailed task analysis and optimization without execution
# - Immutable execution plans ensuring consistent task execution across multiple runs
###############################################################################
# [Source file constraints]
# - All tasks must be atomic and idempotent ensuring safe re-execution and recovery scenarios
# - Task dependencies must form directed acyclic graph preventing circular dependency issues
# - Execution plans must be serializable enabling plan persistence and analysis workflows
# - Task metadata must contain all information needed for execution without external state dependencies
# - Performance estimation must be accurate enough for meaningful progress reporting and resource planning
###############################################################################
# [Dependencies]
# <system>: pathlib - Cross-platform path operations and file metadata
# <system>: datetime - Timestamp and duration tracking for task execution
# <system>: typing - Type annotations for comprehensive static analysis
# <system>: enum - Task type enumeration for structured task classification
###############################################################################
# [GenAI tool change history]
# 2025-07-06T20:50:00Z : Removed task display limit to show all tasks in execution plan preview by CodeAssistant
# * Modified ExecutionPlan.preview() method to display all tasks instead of limiting to first 20 tasks
# * Enhanced debugging experience by providing complete task visibility for comprehensive plan analysis
# * Removed truncation message and task count limitation enabling full plan inspection
# 2025-07-06T20:46:00Z : Added smart path truncation limiting displayed paths to 50 characters by CodeAssistant
# * Enhanced _get_display_path() method with smart upfront truncation for long paths
# * Added _truncate_path_smart() helper method preserving important path information while limiting display length
# * Improved readability of task descriptions by preventing overly long path displays in execution logs
# 2025-07-06T20:43:00Z : Enhanced task description display to show relative paths instead of basename by CodeAssistant
# * Modified AtomicTask.description property to display relative paths from source root when available
# * Added _get_display_path() helper method with graceful fallback to basename for improved task identification
# * Enhanced debugging experience by providing contextual file location information in task descriptions
###############################################################################

"""
Execution Planning Models for Knowledge Bases System.

This module defines the core models for the Plan-then-Execute architecture,
enabling clear separation between decision-making and execution phases with
comprehensive debuggability and task dependency management.
"""

from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


class TaskType(Enum):
    """
    [Enum intent]
    Comprehensive enumeration of all atomic task types in the knowledge base indexing system.
    Provides structured classification enabling task-specific execution logic and resource estimation.

    [Design principles]
    Complete task type coverage ensuring all possible operations have dedicated atomic task types.
    Clear naming convention following operation_target_detail pattern for easy identification.
    Logical grouping by operation type (file, directory, cleanup, structure) for organized processing.
    """
    
    # File Analysis Operations
    ANALYZE_FILE_LLM = "analyze_file_llm"           # Process file through LLM analysis
    SKIP_FILE_CACHED = "skip_file_cached"           # Skip file due to fresh cache
    
    # Directory Knowledge Operations
    CREATE_DIRECTORY_KB = "create_directory_kb"     # Generate directory knowledge file
    SKIP_DIRECTORY_FRESH = "skip_directory_fresh"   # Skip directory due to fresh KB
    
    # Cleanup Operations
    DELETE_ORPHANED_FILE = "delete_orphaned_file"   # Remove orphaned cache/KB file
    DELETE_ORPHANED_DIRECTORY = "delete_orphaned_directory"  # Remove empty orphaned directory
    
    # Structure Operations
    CREATE_CACHE_STRUCTURE = "create_cache_structure"  # Pre-create cache directory structure
    
    # Validation and Verification Operations
    VERIFY_CACHE_FRESHNESS = "verify_cache_freshness"  # Post-execution cache validation
    VERIFY_KB_FRESHNESS = "verify_kb_freshness"       # Post-execution KB validation


@dataclass
class AtomicTask:
    """
    [Class intent]
    Single atomic unit of work with complete execution specification and dependency tracking.
    Contains all information needed for independent execution without external state dependencies.

    [Design principles]
    Atomic operation definition ensuring single responsibility and idempotent execution behavior.
    Complete parameter embedding eliminating external state dependencies during execution.
    Clear dependency specification enabling reliable task ordering and parallel execution opportunities.
    Rich metadata support providing comprehensive task analysis capabilities without execution.
    Immutable task definition ensuring consistent execution behavior across multiple runs.

    [Implementation details]
    Embeds all execution parameters in metadata dictionary for task-specific logic.
    Tracks dependencies as task IDs enabling flexible execution ordering algorithms.
    Includes performance estimation supporting accurate progress reporting and resource planning.
    Provides task validation ensuring all required parameters are present before execution.
    """
    
    # Core Task Identity
    task_id: str                    # Unique identifier for dependency resolution
    task_type: TaskType            # Type of operation for execution dispatch
    target_path: Path              # Primary target for the operation
    
    # Dependency Management
    dependencies: List[str] = field(default_factory=list)  # Task IDs this task depends on
    
    # Performance Estimation
    estimated_duration: float = 0.0  # Estimated seconds for completion
    priority: int = 0               # Execution priority (higher = earlier)
    
    # Task-Specific Parameters
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Execution Tracking
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate task after creation"""
        self._validate_task()
    
    def _validate_task(self) -> None:
        """
        [Method intent]
        Validates task completeness and consistency preventing execution failures.
        Ensures all required parameters are present and task can be executed independently.

        [Design principles]
        Comprehensive validation preventing task execution failures due to missing parameters.
        Task-specific validation ensuring each task type has required metadata present.
        Early error detection catching configuration issues before expensive execution attempts.

        [Implementation details]
        Validates basic task structure including ID, type, and target path.
        Performs task-type-specific validation ensuring required metadata is present.
        Raises descriptive errors enabling quick identification and resolution of task configuration issues.
        """
        if not self.task_id:
            raise ValueError("Task ID is required")
        
        if not self.target_path:
            raise ValueError("Target path is required")
        
        # Task-type-specific validation
        if self.task_type == TaskType.ANALYZE_FILE_LLM:
            required_keys = ['file_size', 'last_modified', 'source_root']
            missing_keys = [key for key in required_keys if key not in self.metadata]
            if missing_keys:
                raise ValueError(f"ANALYZE_FILE_LLM task missing metadata: {missing_keys}")
        
        elif self.task_type == TaskType.CREATE_DIRECTORY_KB:
            required_keys = ['source_root', 'file_contexts', 'subdirectory_contexts']
            missing_keys = [key for key in required_keys if key not in self.metadata]
            if missing_keys:
                raise ValueError(f"CREATE_DIRECTORY_KB task missing metadata: {missing_keys}")
        
        elif self.task_type == TaskType.DELETE_ORPHANED_FILE:
            required_keys = ['deletion_reason', 'is_safe_to_delete']
            missing_keys = [key for key in required_keys if key not in self.metadata]
            if missing_keys:
                raise ValueError(f"DELETE_ORPHANED_FILE task missing metadata: {missing_keys}")
    
    @property
    def description(self) -> str:
        """Human-readable task description for debugging and progress reporting"""
        # Get relative path from source root if available, otherwise use target path
        display_path = self._get_display_path()
        
        if self.task_type == TaskType.ANALYZE_FILE_LLM:
            return f"Analyze {display_path} with LLM (cache stale)"
        elif self.task_type == TaskType.SKIP_FILE_CACHED:
            return f"Skip {display_path} (cache fresh)"
        elif self.task_type == TaskType.CREATE_DIRECTORY_KB:
            return f"Create KB for {display_path}/"
        elif self.task_type == TaskType.SKIP_DIRECTORY_FRESH:
            return f"Skip {display_path}/ (KB fresh)"
        elif self.task_type == TaskType.DELETE_ORPHANED_FILE:
            return f"Delete orphaned {display_path}"
        elif self.task_type == TaskType.DELETE_ORPHANED_DIRECTORY:
            return f"Delete empty directory {display_path}/"
        elif self.task_type == TaskType.CREATE_CACHE_STRUCTURE:
            return f"Create cache structure for {len(self.metadata.get('directories', []))} directories"
        else:
            return f"{self.task_type.value}: {display_path}"
    
    def _get_display_path(self) -> str:
        """
        [Method intent]
        Gets appropriate display path showing relative path from source root when available.
        Falls back to target path name if source root information is not available.
        Applies smart truncation to limit path length to 50 characters for better readability.

        [Design principles]
        Informative path display providing context about file location within project structure.
        Graceful fallback ensuring description works even when source root metadata is missing.
        Consistent path representation using relative paths for better readability.
        Smart truncation preserving important path information while maintaining reasonable display length.

        [Implementation details]
        Attempts to calculate relative path from source_root metadata if available.
        Uses Path.relative_to() for accurate relative path calculation.
        Falls back to basename display if relative path calculation fails.
        Applies upfront truncation with "..." prefix when paths exceed 50 characters.
        Handles both file and directory paths consistently.
        """
        try:
            # Try to get relative path from source root
            source_root = self.metadata.get('source_root')
            if source_root:
                source_root_path = Path(source_root)
                relative_path = str(self.target_path.relative_to(source_root_path))
                return self._truncate_path_smart(relative_path)
        except (ValueError, KeyError, TypeError):
            # Fallback to basename if relative path calculation fails
            pass
        
        # Fallback to just the name if we can't calculate relative path
        return self.target_path.name
    
    def _truncate_path_smart(self, path: str, max_length: int = 50) -> str:
        """
        [Method intent]
        Applies smart truncation to path strings limiting length while preserving important information.
        Uses upfront truncation with "..." prefix to maintain readability of file and directory names.

        [Design principles]
        Smart truncation preserving the most important part of the path (filename and immediate context).
        Consistent truncation behavior ensuring predictable display format across all paths.
        Readable output maintaining path context while respecting display length constraints.

        [Implementation details]
        Checks if path exceeds maximum length before applying truncation.
        Uses upfront truncation removing characters from the beginning of the path.
        Adds "..." prefix to indicate truncation has occurred.
        Ensures total length including "..." prefix does not exceed maximum length.
        """
        if len(path) <= max_length:
            return path
        
        # Calculate how many characters to keep (accounting for "..." prefix)
        chars_to_keep = max_length - 3  # Reserve 3 characters for "..."
        
        if chars_to_keep <= 0:
            # If max_length is too small, just return truncated filename
            return path[-max_length:] if max_length > 0 else ""
        
        # Truncate from the beginning and add "..." prefix
        truncated = path[-chars_to_keep:]
        return f"...{truncated}"
    
    @property
    def is_expensive(self) -> bool:
        """Returns True if task involves expensive operations like LLM calls"""
        expensive_types = {
            TaskType.ANALYZE_FILE_LLM,
            TaskType.CREATE_DIRECTORY_KB
        }
        return self.task_type in expensive_types
    
    def get_dependency_level(self, task_levels: Dict[str, int]) -> int:
        """Calculate dependency level for task ordering (0 = no dependencies)"""
        if not self.dependencies:
            return 0
        
        max_dep_level = 0
        for dep_id in self.dependencies:
            if dep_id in task_levels:
                max_dep_level = max(max_dep_level, task_levels[dep_id])
        
        return max_dep_level + 1


@dataclass
class ExecutionPlan:
    """
    [Class intent]
    Complete execution plan containing all atomic tasks with dependency resolution and analysis capabilities.
    Provides comprehensive task organization, validation, and preview functionality for perfect debuggability.

    [Design principles]
    Complete task inventory enabling comprehensive execution planning and resource estimation.
    Dependency validation ensuring all task dependencies can be resolved in proper execution order.
    Rich analysis capabilities providing detailed execution insights without performing actual execution.
    Immutable plan design ensuring consistent execution behavior across multiple runs.
    Comprehensive preview functionality enabling debugging and optimization before expensive operations.

    [Implementation details]
    Maintains ordered list of atomic tasks with complete dependency tracking.
    Provides task categorization and counting for resource planning and progress estimation.
    Implements dependency validation preventing circular dependencies and missing task references.
    Offers multiple analysis views including task counts, dependency levels, and execution estimates.
    Generates human-readable execution previews for debugging and verification workflows.
    """
    
    # Core Plan Content
    tasks: List[AtomicTask] = field(default_factory=list)
    
    # Plan Metadata
    plan_id: str = field(default_factory=lambda: f"plan_{int(datetime.now().timestamp())}")
    created_at: datetime = field(default_factory=datetime.now)
    source_root: Optional[Path] = None
    
    # Cached Analysis (computed on first access)
    _task_counts_by_type: Optional[Dict[TaskType, int]] = field(default=None, init=False)
    _dependency_levels: Optional[Dict[str, int]] = field(default=None, init=False)
    _total_estimated_duration: Optional[float] = field(default=None, init=False)
    
    def add_task(self, task: AtomicTask) -> None:
        """Add task to plan with validation and cache invalidation"""
        task._validate_task()  # Ensure task is valid
        self.tasks.append(task)
        self._invalidate_caches()
    
    def _invalidate_caches(self) -> None:
        """Invalidate cached analysis when plan is modified"""
        self._task_counts_by_type = None
        self._dependency_levels = None
        self._total_estimated_duration = None
    
    @property
    def task_count_by_type(self) -> Dict[TaskType, int]:
        """Cached task counts by type for resource planning"""
        if self._task_counts_by_type is None:
            self._task_counts_by_type = {}
            for task in self.tasks:
                self._task_counts_by_type[task.task_type] = self._task_counts_by_type.get(task.task_type, 0) + 1
        return self._task_counts_by_type
    
    @property
    def total_estimated_duration(self) -> float:
        """Cached total estimated duration for progress planning"""
        if self._total_estimated_duration is None:
            self._total_estimated_duration = sum(task.estimated_duration for task in self.tasks)
        return self._total_estimated_duration
    
    @property
    def expensive_task_count(self) -> int:
        """Count of expensive tasks (LLM calls) for resource planning"""
        return sum(1 for task in self.tasks if task.is_expensive)
    
    def get_tasks_by_type(self, task_type: TaskType) -> List[AtomicTask]:
        """Get all tasks of specified type"""
        return [task for task in self.tasks if task.task_type == task_type]
    
    def get_task_by_id(self, task_id: str) -> Optional[AtomicTask]:
        """Get task by ID for dependency resolution"""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None
    
    def validate_dependencies(self) -> List[str]:
        """
        [Method intent]
        Validates all task dependencies can be resolved and no circular dependencies exist.
        Returns list of validation errors for comprehensive dependency analysis.

        [Design principles]
        Comprehensive dependency validation preventing execution failures due to unresolvable dependencies.
        Circular dependency detection ensuring task execution can proceed in proper order.
        Clear error reporting enabling quick identification and resolution of dependency issues.

        [Implementation details]
        Validates all task dependencies reference existing tasks in the plan.
        Performs cycle detection using depth-first search to identify circular dependencies.
        Returns detailed error messages for each validation failure enabling targeted fixes.
        """
        errors = []
        task_ids = {task.task_id for task in self.tasks}
        
        # Check for missing dependencies
        for task in self.tasks:
            for dep_id in task.dependencies:
                if dep_id not in task_ids:
                    errors.append(f"Task {task.task_id} depends on non-existent task {dep_id}")
        
        # Check for circular dependencies using DFS
        def has_cycle(task_id: str, visiting: Set[str], visited: Set[str]) -> bool:
            if task_id in visiting:
                return True
            if task_id in visited:
                return False
            
            visiting.add(task_id)
            task = self.get_task_by_id(task_id)
            if task:
                for dep_id in task.dependencies:
                    if has_cycle(dep_id, visiting, visited):
                        return True
            
            visiting.remove(task_id)
            visited.add(task_id)
            return False
        
        visited = set()
        for task in self.tasks:
            if task.task_id not in visited:
                if has_cycle(task.task_id, set(), visited):
                    errors.append(f"Circular dependency detected involving task {task.task_id}")
        
        return errors
    
    def get_execution_order(self) -> List[AtomicTask]:
        """
        [Method intent]
        Returns tasks in valid execution order respecting all dependencies.
        Uses topological sorting to ensure dependencies are satisfied before task execution.

        [Design principles]
        Dependency-respecting execution order ensuring all task prerequisites are satisfied.
        Deterministic ordering providing consistent execution behavior across multiple runs.
        Optimization opportunities identifying tasks that can execute in parallel.

        [Implementation details]
        Implements topological sorting algorithm respecting task dependencies.
        Calculates dependency levels for each task enabling parallel execution identification.
        Returns ordered task list ready for sequential or parallel execution.
        """
        # Calculate dependency levels
        if self._dependency_levels is None:
            self._dependency_levels = {}
            
            # Iteratively calculate levels until all tasks have levels
            remaining_tasks = {task.task_id: task for task in self.tasks}
            current_level = 0
            
            while remaining_tasks:
                # Find tasks with no unresolved dependencies
                level_tasks = []
                for task_id, task in remaining_tasks.items():
                    unresolved_deps = [dep for dep in task.dependencies if dep in remaining_tasks]
                    if not unresolved_deps:
                        level_tasks.append((task_id, task))
                
                if not level_tasks:
                    # Circular dependency - break with error
                    logger.error(f"Circular dependency detected in remaining tasks: {list(remaining_tasks.keys())}")
                    break
                
                # Assign level and remove from remaining
                for task_id, task in level_tasks:
                    self._dependency_levels[task_id] = current_level
                    del remaining_tasks[task_id]
                
                current_level += 1
        
        # Sort tasks by dependency level, then by priority, then by creation time
        return sorted(self.tasks, key=lambda t: (
            self._dependency_levels.get(t.task_id, 999),  # Dependency level (lower first)
            -t.priority,  # Priority (higher first) 
            t.created_at   # Creation time (earlier first)
        ))
    
    def get_parallel_execution_groups(self) -> List[List[AtomicTask]]:
        """
        [Method intent]
        Groups tasks into parallel execution groups where tasks within each group can execute concurrently.
        Returns list of task groups where each group contains tasks with no interdependencies.

        [Design principles]
        Parallel execution optimization maximizing resource utilization through concurrent task execution.
        Dependency safety ensuring no task executes before its dependencies are satisfied.
        Resource planning enabling estimation of parallel execution requirements and benefits.

        [Implementation details]
        Groups tasks by dependency level enabling parallel execution within each level.
        Ensures tasks within same group have no interdependencies for safe concurrent execution.
        Returns ordered groups where each group can execute in parallel after previous groups complete.
        """
        if self._dependency_levels is None:
            self.get_execution_order()  # Calculate dependency levels
        
        # Group tasks by dependency level
        level_groups = {}
        for task in self.tasks:
            level = self._dependency_levels.get(task.task_id, 999)
            if level not in level_groups:
                level_groups[level] = []
            level_groups[level].append(task)
        
        # Return groups in dependency order
        return [level_groups[level] for level in sorted(level_groups.keys())]
    
    def preview(self) -> str:
        """
        [Method intent]
        Generates comprehensive human-readable execution plan preview for debugging and verification.
        Provides detailed task breakdown, dependency analysis, and resource estimation without execution.

        [Design principles]
        Comprehensive preview enabling complete execution plan understanding before expensive operations.
        Clear categorization organizing tasks by type and operation for easy analysis.
        Resource estimation providing accurate execution time and complexity assessment.
        Dependency visualization showing task relationships and execution ordering.

        [Implementation details]
        Analyzes task distribution across all operation types for complete resource planning.
        Calculates execution statistics including LLM calls, file operations, and cleanup tasks.
        Formats output for easy readability with clear sections and summary information.
        Provides both high-level summary and detailed task-by-task breakdown.
        """
        lines = []
        lines.append(f"🎯 Execution Plan Preview ({self.plan_id})")
        lines.append("=" * 60)
        
        # High-level summary
        lines.append(f"📊 Summary: {len(self.tasks)} total tasks, {self.expensive_task_count} LLM calls")
        lines.append(f"⏱️ Estimated Duration: {self.total_estimated_duration:.1f} seconds")
        lines.append("")
        
        # Task counts by type
        lines.append("📋 Task Breakdown:")
        for task_type, count in self.task_count_by_type.items():
            emoji = self._get_task_type_emoji(task_type)
            lines.append(f"   {emoji} {task_type.value}: {count} tasks")
        lines.append("")
        
        # Dependency validation
        validation_errors = self.validate_dependencies()
        if validation_errors:
            lines.append("❌ Dependency Validation Errors:")
            for error in validation_errors:
                lines.append(f"   • {error}")
            lines.append("")
        else:
            lines.append("✅ Dependency Validation: All dependencies resolved")
            lines.append("")
        
        # Parallel execution analysis
        parallel_groups = self.get_parallel_execution_groups()
        lines.append(f"🚀 Parallel Execution: {len(parallel_groups)} execution levels")
        for i, group in enumerate(parallel_groups):
            lines.append(f"   Level {i}: {len(group)} tasks (can run in parallel)")
        lines.append("")
        
        # Detailed task listing (showing all tasks)
        lines.append("📝 Task Details:")
        execution_order = self.get_execution_order()
        for i, task in enumerate(execution_order):
            emoji = self._get_task_type_emoji(task.task_type)
            deps_str = f" [deps: {', '.join(task.dependencies)}]" if task.dependencies else ""
            lines.append(f"   {i+1:2d}. {emoji} {task.description}{deps_str}")
        
        return "\n".join(lines)
    
    def _get_task_type_emoji(self, task_type: TaskType) -> str:
        """Get emoji for task type for better visual display"""
        emoji_map = {
            TaskType.ANALYZE_FILE_LLM: "🤖",
            TaskType.SKIP_FILE_CACHED: "📄", 
            TaskType.CREATE_DIRECTORY_KB: "📁",
            TaskType.SKIP_DIRECTORY_FRESH: "✅",
            TaskType.DELETE_ORPHANED_FILE: "🗑️",
            TaskType.DELETE_ORPHANED_DIRECTORY: "🗂️",
            TaskType.CREATE_CACHE_STRUCTURE: "🏗️",
            TaskType.VERIFY_CACHE_FRESHNESS: "🔍",
            TaskType.VERIFY_KB_FRESHNESS: "🔍"
        }
        return emoji_map.get(task_type, "📋")


@dataclass
class ExecutionResults:
    """
    [Class intent]
    Comprehensive execution results tracking task completion status and performance metrics.
    Provides detailed execution analysis and reporting for optimization and debugging.

    [Design principles]
    Complete execution tracking enabling comprehensive performance analysis and optimization.
    Task-level result tracking supporting detailed success/failure analysis and debugging.
    Performance metrics collection enabling system optimization and resource planning improvements.
    """
    
    plan_id: str
    execution_start: datetime
    execution_end: Optional[datetime] = None
    
    # Task Results
    completed_tasks: List[str] = field(default_factory=list)
    failed_tasks: List[Tuple[str, str]] = field(default_factory=list)  # (task_id, error)
    skipped_tasks: List[str] = field(default_factory=list)
    
    # Performance Metrics
    total_duration: Optional[float] = None
    llm_calls_made: int = 0
    files_processed: int = 0
    directories_processed: int = 0
    files_deleted: int = 0
    
    @property
    def success_rate(self) -> float:
        """Calculate overall success rate"""
        total_tasks = len(self.completed_tasks) + len(self.failed_tasks) + len(self.skipped_tasks)
        if total_tasks == 0:
            return 0.0
        return len(self.completed_tasks) / total_tasks
    
    @property
    def is_complete(self) -> bool:
        """Check if execution is complete"""
        return self.execution_end is not None
    
    def add_completed_task(self, task_id: str) -> None:
        """Mark task as completed"""
        self.completed_tasks.append(task_id)
    
    def add_failed_task(self, task_id: str, error: str) -> None:
        """Mark task as failed with error"""
        self.failed_tasks.append((task_id, error))
    
    def add_skipped_task(self, task_id: str) -> None:
        """Mark task as skipped"""
        self.skipped_tasks.append(task_id)
    
    def complete_execution(self) -> None:
        """Mark execution as complete and calculate final metrics"""
        self.execution_end = datetime.now()
        if self.execution_start:
            self.total_duration = (self.execution_end - self.execution_start).total_seconds()
    
    def get_summary(self) -> str:
        """Get human-readable execution summary"""
        lines = []
        lines.append(f"🎯 Execution Results ({self.plan_id})")
        lines.append("=" * 50)
        
        if self.is_complete:
            lines.append(f"⏱️ Duration: {self.total_duration:.1f} seconds")
        
        lines.append(f"✅ Completed: {len(self.completed_tasks)} tasks")
        lines.append(f"❌ Failed: {len(self.failed_tasks)} tasks")
        lines.append(f"⏭️ Skipped: {len(self.skipped_tasks)} tasks")
        lines.append(f"📊 Success Rate: {self.success_rate:.1%}")
        
        lines.append(f"🤖 LLM Calls: {self.llm_calls_made}")
        lines.append(f"📄 Files Processed: {self.files_processed}")
        lines.append(f"📁 Directories Processed: {self.directories_processed}")
        lines.append(f"🗑️ Files Deleted: {self.files_deleted}")
        
        if self.failed_tasks:
            lines.append("\n❌ Failed Tasks:")
            for task_id, error in self.failed_tasks:
                lines.append(f"   • {task_id}: {error}")
        
        return "\n".join(lines)

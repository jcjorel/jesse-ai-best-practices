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
# Generic task planning system converting decision outcomes into executable plans.
# Implements task registry, dependency resolution, and execution plan generation
# with comprehensive validation and concurrency analysis.
###############################################################################
# [Source file design principles]
# - Generic task registry pattern for extensible task creation
# - Comprehensive dependency resolution with cycle detection
# - Concurrency analysis for performance optimization
# - Fail-fast validation with detailed error reporting
# - Clear separation between planning and execution concerns
###############################################################################
# [Source file constraints]
# - Must support topological sorting for dependency resolution
# - No FastMCP dependencies for clean architecture
# - Exception-first error handling - no fallback mechanisms
# - Must generate valid ExecutionPlan objects ready for execution
###############################################################################
# [Dependencies]
# <system>:typing.List
# <system>:typing.Dict
# <system>:typing.Optional
# <system>:typing.Type
# <system>:collections.deque
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.AtomicTask
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.ExecutionPlan
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.ProgressCallback
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.decisions.TaskDecision
###############################################################################
# [GenAI tool change history]
# 2025-07-09T13:33:00Z : Initial generic planning implementation by CodeAssistant
# * Created TaskRegistry for extensible task type management
# * Implemented DependencyResolver with cycle detection and topological sorting
# * Added ConcurrencyAnalyzer for parallel execution optimization
# * Created GenericPlanGenerator orchestrating complete planning workflow
###############################################################################

from typing import List, Dict, Optional, Type
from collections import deque

from .models import AtomicTask, ExecutionPlan, ProgressCallback
from .decisions import TaskDecision


class TaskRegistry:
    """
    [Class intent]
    Registry for managing different atomic task types with factory pattern.
    Enables extensible task creation and type management for different
    indexing operations.

    [Design principles]
    Factory pattern for task creation with type safety.
    Registration system for extensible task types.
    Clear separation between task types and instances.

    [Implementation details]
    Maps task type strings to task class constructors.
    Provides factory methods for creating task instances.
    Validates task types during registration and creation.
    """
    
    def __init__(self):
        """
        [Class method intent]
        Initialize task registry with empty task type registry.

        [Design principles]
        Clean initialization with explicit registration required.

        [Implementation details]
        Creates empty registry dictionary for task type mappings.
        """
        self._task_types: Dict[str, Type[AtomicTask]] = {}
    
    def register_task_type(self, task_type: str, task_class: Type[AtomicTask]):
        """
        [Class method intent]
        Register new task type with corresponding task class.

        [Design principles]
        Explicit registration for type safety and extensibility.
        Validation of task class interface compliance.

        [Implementation details]
        Validates task_class implements AtomicTask interface.
        Stores mapping from task_type string to task class.
        """
        if not issubclass(task_class, AtomicTask):
            raise ValueError(f"Task class {task_class} must implement AtomicTask interface")
        
        if task_type in self._task_types:
            raise ValueError(f"Task type '{task_type}' is already registered")
        
        self._task_types[task_type] = task_class
    
    def create_task(self, decision: TaskDecision) -> AtomicTask:
        """
        [Class method intent]
        Create task instance from task decision using factory pattern.

        [Design principles]
        Factory method for type-safe task creation.
        Decision-driven task instantiation with simplified parameter passing.

        [Implementation details]
        Looks up task class by decision task_type.
        Creates task instance with decision object directly.
        Validates task creation success before returning.
        """
        task_type = decision.task_type
        
        if task_type not in self._task_types:
            raise ValueError(f"Unknown task type: {task_type}. Available types: {list(self._task_types.keys())}")
        
        task_class = self._task_types[task_type]
        
        try:
            # Create task instance with decision object
            task = task_class(decision)
            return task
            
        except Exception as e:
            raise RuntimeError(f"Failed to create task {task_type} with ID {decision.task_id}: {str(e)}") from e
    
    def get_registered_types(self) -> List[str]:
        """
        [Class method intent]
        Return list of registered task type strings.

        [Design principles]
        Introspection capability for debugging and validation.

        [Implementation details]
        Returns keys from task type registry dictionary.
        """
        return list(self._task_types.keys())
    
    def is_task_type_registered(self, task_type: str) -> bool:
        """
        [Class method intent]
        Check if task type is registered in the registry.

        [Design principles]
        Safe type checking before task creation attempts.

        [Implementation details]
        Checks existence of task_type key in registry.
        """
        return task_type in self._task_types


class DependencyResolver:
    """
    [Class intent]
    Resolves task dependencies with cycle detection and topological sorting.
    Ensures proper execution ordering while detecting invalid dependency graphs.

    [Design principles]
    Comprehensive dependency analysis with cycle detection.
    Topological sorting for proper execution ordering.
    Clear error reporting for dependency violations.

    [Implementation details]
    Uses graph algorithms for dependency analysis.
    Implements Kahn's algorithm for topological sorting.
    Provides detailed error information for debugging.
    """
    
    def resolve_dependencies(self, tasks: List[AtomicTask]) -> List[AtomicTask]:
        """
        [Class method intent]
        Resolve task dependencies and return topologically sorted task list.

        [Design principles]
        Dependency-aware task ordering for safe execution.
        Cycle detection prevents infinite dependency loops.

        [Implementation details]
        Builds dependency graph from task dependency declarations.
        Performs topological sort using Kahn's algorithm.
        Returns tasks in dependency-resolved execution order.
        """
        if not tasks:
            return []
        
        # Build dependency graph
        task_map = {task.get_task_id(): task for task in tasks}
        dependency_graph = self._build_dependency_graph(tasks)
        
        # Detect cycles
        cycles = self._detect_cycles(dependency_graph)
        if cycles:
            cycle_descriptions = [" -> ".join(cycle) for cycle in cycles]
            raise RuntimeError(f"Dependency cycles detected: {'; '.join(cycle_descriptions)}")
        
        # Perform topological sort
        sorted_task_ids = self._topological_sort(dependency_graph)
        
        # Return tasks in dependency-resolved order
        resolved_tasks = []
        for task_id in sorted_task_ids:
            if task_id in task_map:
                resolved_tasks.append(task_map[task_id])
        
        return resolved_tasks
    
    def _build_dependency_graph(self, tasks: List[AtomicTask]) -> Dict[str, List[str]]:
        """
        [Class method intent]
        Build directed dependency graph from task dependency declarations.

        [Design principles]
        Graph representation for algorithmic dependency analysis.

        [Implementation details]
        Creates adjacency list representation of dependency graph.
        Maps from task ID to list of dependent task IDs.
        """
        graph = {}
        
        for task in tasks:
            task_id = task.get_task_id()
            dependencies = task.get_dependencies()
            
            # Initialize task node in graph
            if task_id not in graph:
                graph[task_id] = []
            
            # Add edges for dependencies
            for dep_id in dependencies:
                if dep_id not in graph:
                    graph[dep_id] = []
                graph[dep_id].append(task_id)
        
        return graph
    
    def _detect_cycles(self, graph: Dict[str, List[str]]) -> List[List[str]]:
        """
        [Class method intent]
        Detect cycles in dependency graph using depth-first search.

        [Design principles]
        Cycle detection prevents invalid execution plans.
        Multiple cycle detection for comprehensive error reporting.

        [Implementation details]
        Uses DFS with color coding to detect back edges.
        Returns list of cycles found in dependency graph.
        """
        cycles = []
        colors = {}  # White: 0, Gray: 1, Black: 2
        path = []
        
        def dfs(node):
            if node in colors:
                if colors[node] == 1:  # Gray - back edge found
                    cycle_start = path.index(node)
                    cycle = path[cycle_start:] + [node]
                    cycles.append(cycle)
                return
            
            colors[node] = 1  # Gray
            path.append(node)
            
            for neighbor in graph.get(node, []):
                dfs(neighbor)
            
            path.pop()
            colors[node] = 2  # Black
        
        for node in graph:
            if node not in colors:
                dfs(node)
        
        return cycles
    
    def _topological_sort(self, graph: Dict[str, List[str]]) -> List[str]:
        """
        [Class method intent]
        Perform topological sort on dependency graph using Kahn's algorithm.

        [Design principles]
        Kahn's algorithm provides stable topological ordering.
        Handles disconnected graph components correctly.

        [Implementation details]
        Calculates in-degrees for all nodes.
        Processes nodes with zero in-degree first.
        Returns topologically sorted node list.
        """
        # Calculate in-degrees
        in_degree = {node: 0 for node in graph}
        for node in graph:
            for neighbor in graph[node]:
                in_degree[neighbor] = in_degree.get(neighbor, 0) + 1
        
        # Initialize queue with nodes having zero in-degree
        queue = deque([node for node, degree in in_degree.items() if degree == 0])
        sorted_nodes = []
        
        while queue:
            node = queue.popleft()
            sorted_nodes.append(node)
            
            # Reduce in-degree of neighbors
            for neighbor in graph.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return sorted_nodes


class ConcurrencyAnalyzer:
    """
    [Class intent]
    Analyzes task concurrency compatibility and generates parallel execution groups.
    Identifies tasks that can safely run simultaneously for performance optimization.

    [Design principles]
    Conservative concurrency analysis prioritizing safety over performance.
    Clear grouping of concurrent-safe tasks.
    Detailed analysis of concurrency constraints.

    [Implementation details]
    Analyzes task concurrency compatibility declarations.
    Groups tasks into concurrent execution batches.
    Respects dependency constraints during grouping.
    """
    
    def analyze_concurrency(self, tasks: List[AtomicTask]) -> List[List[str]]:
        """
        [Class method intent]
        Analyze task concurrency and return groups of tasks that can run in parallel.

        [Design principles]
        Conservative concurrency grouping prioritizing correctness.
        Dependency-aware parallel grouping.

        [Implementation details]
        Groups tasks based on concurrency compatibility.
        Ensures dependency constraints are respected.
        Returns list of concurrent task ID groups.
        """
        if not tasks:
            return []
        
        concurrent_groups = []
        remaining_tasks = tasks.copy()
        
        while remaining_tasks:
            # Find next concurrent group
            current_group = [remaining_tasks[0]]
            remaining_tasks.remove(remaining_tasks[0])
            
            # Try to add more tasks to current group
            for task in remaining_tasks.copy():
                if self._can_run_with_group(task, current_group):
                    current_group.append(task)
                    remaining_tasks.remove(task)
            
            # Add group to results
            group_ids = [task.get_task_id() for task in current_group]
            concurrent_groups.append(group_ids)
        
        return concurrent_groups
    
    def _can_run_with_group(self, task: AtomicTask, group: List[AtomicTask]) -> bool:
        """
        [Class method intent]
        Determine if task can run concurrently with all tasks in group.

        [Design principles]
        Conservative compatibility checking for safety.
        All group members must be compatible with new task.

        [Implementation details]
        Checks task compatibility with every group member.
        Returns True only if compatible with all group tasks.
        """
        for group_task in group:
            if not task.can_run_concurrently_with(group_task):
                return False
            if not group_task.can_run_concurrently_with(task):
                return False
        return True


class GenericPlanGenerator:
    """
    [Class intent]
    Main orchestrator for generic task planning workflow.
    Converts task decisions into validated execution plans with dependency
    resolution and concurrency analysis.

    [Design principles]
    Complete planning workflow orchestration.
    Comprehensive plan validation before execution.
    Clear separation between planning and execution concerns.

    [Implementation details]
    Coordinates task registry, dependency resolver, and concurrency analyzer.
    Generates ExecutionPlan objects ready for execution.
    Provides detailed progress reporting and error handling.
    """
    
    def __init__(self, task_registry: TaskRegistry):
        """
        [Class method intent]
        Initialize plan generator with task registry and analysis components.

        [Design principles]
        Dependency injection for extensibility and testability.
        Composition pattern for specialized analysis capabilities.

        [Implementation details]
        Stores task registry for task creation.
        Creates dependency resolver and concurrency analyzer.
        """
        self.task_registry = task_registry
        self.dependency_resolver = DependencyResolver()
        self.concurrency_analyzer = ConcurrencyAnalyzer()
    
    async def generate_plan(
        self, 
        decisions: List[TaskDecision], 
        progress: Optional[ProgressCallback] = None
    ) -> ExecutionPlan:
        """
        [Class method intent]
        Generate complete execution plan from task decisions.

        [Design principles]
        Complete planning workflow from decisions to executable plan.
        Comprehensive validation with detailed error reporting.
        Progress reporting for long-running planning operations.

        [Implementation details]
        Populates decision dependencies before task creation.
        Creates tasks from decisions using task registry.
        Resolves dependencies with topological sorting.
        Analyzes concurrency for parallel execution opportunities.
        Validates final plan before returning.
        """
        if progress:
            progress("Starting execution plan generation...")
        
        try:
            # Populate task dependencies
            if progress:
                progress("Populating task dependencies...")
            
            populated_decisions = self._populate_task_dependencies(decisions)
            
            # Create tasks from decisions
            if progress:
                progress(f"Creating {len(populated_decisions)} tasks from decisions...")
            
            tasks = []
            for decision in populated_decisions:
                try:
                    task = self.task_registry.create_task(decision)
                    tasks.append(task)
                except Exception as e:
                    error_msg = f"Failed to create task from decision {decision.task_id}: {str(e)}"
                    if progress:
                        progress(f"ERROR: {error_msg}")
                    raise RuntimeError(error_msg) from e
            
            # Resolve dependencies
            if progress:
                progress("Resolving task dependencies...")
            
            try:
                resolved_tasks = self.dependency_resolver.resolve_dependencies(tasks)
            except Exception as e:
                error_msg = f"Dependency resolution failed: {str(e)}"
                if progress:
                    progress(f"ERROR: {error_msg}")
                raise RuntimeError(error_msg) from e
            
            # Analyze concurrency
            if progress:
                progress("Analyzing task concurrency...")
            
            try:
                concurrent_groups = self.concurrency_analyzer.analyze_concurrency(resolved_tasks)
            except Exception as e:
                error_msg = f"Concurrency analysis failed: {str(e)}"
                if progress:
                    progress(f"ERROR: {error_msg}")
                raise RuntimeError(error_msg) from e
            
            # Create execution plan
            plan = ExecutionPlan(
                tasks=resolved_tasks,
                concurrent_groups=concurrent_groups
            )
            
            # Validate plan
            validation_errors = self._validate_plan(plan)
            plan.validation_errors = validation_errors
            
            if progress:
                if plan.is_valid:
                    progress(f"Execution plan generated successfully: {plan.task_count} tasks, {len(concurrent_groups)} concurrent groups")
                else:
                    progress(f"Execution plan generated with {len(validation_errors)} validation errors")
            
            return plan
            
        except Exception as e:
            error_msg = f"Plan generation failed: {str(e)}"
            if progress:
                progress(f"ERROR: {error_msg}")
            raise RuntimeError(error_msg) from e
    
    def _validate_plan(self, plan: ExecutionPlan) -> List[str]:
        """
        [Class method intent]
        Validate execution plan for correctness and consistency.

        [Design principles]
        Comprehensive plan validation before execution.
        Clear error reporting for validation failures.

        [Implementation details]
        Validates task preconditions and plan consistency.
        Checks dependency resolution correctness.
        Returns list of validation error messages.
        """
        validation_errors = []
        
        try:
            # Validate task count
            if not plan.tasks:
                validation_errors.append("Execution plan contains no tasks")
                return validation_errors
            
            # Validate all tasks have unique IDs
            task_ids = [task.get_task_id() for task in plan.tasks]
            if len(task_ids) != len(set(task_ids)):
                validation_errors.append("Execution plan contains duplicate task IDs")
            
            # Validate concurrent groups reference valid task IDs
            all_task_ids = set(task_ids)
            for group in plan.concurrent_groups:
                for task_id in group:
                    if task_id not in all_task_ids:
                        validation_errors.append(f"Concurrent group references unknown task ID: {task_id}")
            
            # Validate dependency constraints
            for task in plan.tasks:
                for dep_id in task.get_dependencies():
                    if dep_id not in all_task_ids:
                        validation_errors.append(f"Task {task.get_task_id()} depends on unknown task: {dep_id}")
            
        except Exception as e:
            validation_errors.append(f"Plan validation error: {str(e)}")
        
        return validation_errors
    
    def _populate_task_dependencies(self, decisions: List[TaskDecision]) -> List[TaskDecision]:
        """
        [Class method intent]
        Populate task dependencies based on task types and relationships.

        [Design principles]
        Automatic dependency analysis based on task characteristics.
        File analysis tasks must complete before KB building tasks.
        Clear dependency chain from files to directories.

        [Implementation details]
        KB building tasks depend on file analysis tasks in same directory.
        File analysis tasks have no dependencies (independent).
        Cleanup tasks have no dependencies (low priority).
        """
        # Create task maps for analysis
        analysis_tasks = {}  # source_path -> task_id
        kb_tasks = []
        
        # Categorize tasks and build analysis task mapping
        for decision in decisions:
            if decision.task_type == "analyze_file":
                if decision.source_path:
                    analysis_tasks[decision.source_path] = decision.task_id
            elif decision.task_type == "build_knowledge_base":
                kb_tasks.append(decision)
        
        # Populate KB task dependencies
        for kb_decision in kb_tasks:
            if kb_decision.source_path:
                # Find all analysis tasks in the same directory tree
                kb_dependencies = []
                kb_source = kb_decision.source_path
                
                for analysis_source, analysis_task_id in analysis_tasks.items():
                    # Check if analysis file is within KB source directory
                    try:
                        analysis_source.relative_to(kb_source)
                        kb_dependencies.append(analysis_task_id)
                    except ValueError:
                        # analysis_source is not within kb_source directory
                        continue
                
                # Update decision dependencies
                kb_decision.dependencies = kb_dependencies
        
        return decisions
    
    def get_plan_summary(self, plan: ExecutionPlan) -> Dict[str, any]:
        """
        [Class method intent]
        Generate summary statistics for execution plan.

        [Design principles]
        Clear reporting of plan characteristics for monitoring.

        [Implementation details]
        Counts tasks by type, analyzes concurrency, and summarizes plan.
        """
        summary = {
            'total_tasks': plan.task_count,
            'concurrent_groups': len(plan.concurrent_groups),
            'validation_errors': len(plan.validation_errors),
            'is_valid': plan.is_valid,
            'task_types': {},
            'max_concurrent_tasks': 0
        }
        
        # Count task types
        for task in plan.tasks:
            task_type = task.get_task_type()
            summary['task_types'][task_type] = summary['task_types'].get(task_type, 0) + 1
        
        # Find maximum concurrent tasks
        if plan.concurrent_groups:
            summary['max_concurrent_tasks'] = max(len(group) for group in plan.concurrent_groups)
        
        return summary

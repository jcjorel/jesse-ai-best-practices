<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/models/execution_plan.py -->
<!-- Cached On: 2025-07-06T21:08:13.191626 -->
<!-- Source Modified: 2025-07-06T20:51:08.177947 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file defines execution planning models for the Plan-then-Execute architecture in the Knowledge Bases Hierarchical Indexing System, enabling clear separation between decision-making and execution phases with comprehensive debuggability and task dependency management. The module implements atomic task definition through `AtomicTask` dataclass with complete execution specification, comprehensive execution planning via `ExecutionPlan` with dependency resolution and task ordering, and detailed execution tracking through `ExecutionResults` for performance analysis. Key semantic entities include `TaskType` enumeration with values like `ANALYZE_FILE_LLM`, `CREATE_DIRECTORY_KB`, and `DELETE_ORPHANED_FILE` for structured task classification, `@dataclass` decorators for immutable execution plans, `field(default_factory=datetime.now)` for automatic timestamp tracking, and `validate_dependencies()` method implementing directed acyclic graph validation. The system provides rich metadata support enabling detailed task analysis without execution, implements topological sorting for dependency-respecting execution order, and offers comprehensive preview functionality through `ExecutionPlan.preview()` generating human-readable execution plans for debugging and verification workflows.

##### Main Components

The file contains four primary components implementing the execution planning architecture. The `TaskType` enumeration defines comprehensive atomic task types including file analysis operations (`ANALYZE_FILE_LLM`, `SKIP_FILE_CACHED`), directory knowledge operations (`CREATE_DIRECTORY_KB`, `SKIP_DIRECTORY_FRESH`), cleanup operations (`DELETE_ORPHANED_FILE`, `DELETE_ORPHANED_DIRECTORY`), structure operations (`CREATE_CACHE_STRUCTURE`), and validation operations (`VERIFY_CACHE_FRESHNESS`, `VERIFY_KB_FRESHNESS`). The `AtomicTask` dataclass represents single atomic units of work with complete execution specification including task identity fields, dependency management through task ID lists, performance estimation with duration and priority, and task-specific parameters embedded in metadata dictionaries. The `ExecutionPlan` dataclass provides complete execution planning with ordered task lists, dependency validation, analysis capabilities, and cached performance metrics. The `ExecutionResults` dataclass tracks comprehensive execution outcomes with task completion status, performance metrics including LLM calls and file operations, and detailed success/failure analysis for optimization and debugging purposes.

###### Architecture & Design

The architecture implements Plan-then-Execute separation with immutable execution plans ensuring consistent task execution behavior across multiple runs. The design follows atomic task principles where each `AtomicTask` contains complete execution specification eliminating external state dependencies through comprehensive metadata embedding. The `ExecutionPlan` uses cached analysis pattern with lazy computation of task counts, dependency levels, and duration estimates, invalidating caches when plans are modified through `_invalidate_caches()`. Error handling architecture separates validation errors from execution errors, with `validate_dependencies()` performing comprehensive dependency analysis including circular dependency detection using depth-first search. The dependency management system uses task ID references enabling flexible execution ordering algorithms and parallel execution identification through `get_parallel_execution_groups()`. The preview and analysis system provides multiple views including task categorization, dependency visualization, and resource estimation without performing actual execution, supporting comprehensive debugging and optimization workflows.

####### Implementation Approach

The implementation uses dataclass-based immutable objects with `@dataclass` decorators and `field(default_factory=list)` for automatic collection initialization. Task validation employs `__post_init__()` hooks with task-type-specific validation ensuring required metadata is present before execution, raising descriptive errors for missing parameters. Dependency resolution implements topological sorting through iterative level calculation, assigning dependency levels to enable parallel execution identification and proper task ordering. The caching strategy uses optional fields with `None` initialization and lazy computation, calculating expensive analysis only when accessed and invalidating when plans are modified. Path display optimization uses smart truncation through `_truncate_path_smart()` limiting displayed paths to 50 characters while preserving important path information with "..." prefix truncation. Performance estimation integrates duration tracking, LLM call counting, and resource utilization metrics enabling accurate progress reporting and execution planning. The preview system generates comprehensive human-readable output with emoji-based task type visualization, dependency analysis, and detailed task breakdowns for debugging and verification purposes.

######## External Dependencies & Integration Points

**→ Inbound:**
- `pathlib.Path` (external library) - Cross-platform path operations and file metadata for task target specification
- `datetime.datetime` (external library) - Timestamp and duration tracking for task execution timing
- `datetime.timedelta` (external library) - Duration calculations for performance analysis and estimation
- `typing.Dict` (external library) - Type annotations for comprehensive static analysis and metadata structure
- `typing.List` (external library) - Type annotations for task collections and dependency management
- `typing.Optional` (external library) - Type annotations for nullable fields and optional metadata
- `typing.Any` (external library) - Type annotations for flexible metadata content and task parameters
- `typing.Set` (external library) - Type annotations for dependency validation and circular dependency detection
- `typing.Tuple` (external library) - Type annotations for structured data like failed task records
- `enum.Enum` (external library) - Task type enumeration for structured task classification
- `dataclasses.dataclass` (external library) - Immutable execution plan creation with validation
- `dataclasses.field` (external library) - Default factory configuration for automatic initialization
- `logging` (external library) - Structured logging for execution analysis and debugging

**← Outbound:**
- `../indexing/plan_generator.py:PlanGenerator` - Primary consumer creating ExecutionPlan objects from decisions
- `../indexing/execution_engine.py:ExecutionEngine` - Consumer executing AtomicTask objects with dependency resolution
- `../indexing/hierarchical_indexer.py:HierarchicalIndexer` - Consumer coordinating plan generation and execution workflows
- `execution_plans/` - Serialized ExecutionPlan objects for debugging and analysis workflows
- `execution_results/` - Generated ExecutionResults objects for performance analysis and optimization
- `task_metadata/` - Comprehensive task metadata for independent execution and troubleshooting

**⚡ System role and ecosystem integration:**
- **System Role**: Foundational execution model layer within the Jesse Framework MCP Plan-then-Execute architecture, providing structured task representation and execution planning capabilities for all knowledge base indexing operations
- **Ecosystem Position**: Core model component serving as the primary data contract between plan generation and execution systems, ensuring atomic task definition and dependency management across the indexing workflow
- **Integration Pattern**: Used by plan generators for structured task creation, consumed by execution engines for atomic task processing, and integrated with monitoring systems for comprehensive execution tracking and performance analysis

######### Edge Cases & Error Handling

The system implements comprehensive task validation through `_validate_task()` with task-type-specific checks ensuring required metadata is present, raising `ValueError` exceptions with descriptive messages for missing parameters like `file_size`, `source_root`, or `is_safe_to_delete`. Dependency validation handles missing task references and circular dependencies through `validate_dependencies()` using depth-first search to detect cycles and returning detailed error lists for targeted fixes. Path display handles edge cases through graceful fallback in `_get_display_path()` where relative path calculation failures fall back to basename display, and smart truncation handles extremely short maximum lengths by returning truncated filenames. Execution plan modification safety uses cache invalidation through `_invalidate_caches()` ensuring cached analysis remains consistent when tasks are added or modified. Task ordering handles circular dependencies by breaking with error logging when topological sorting cannot proceed, preventing infinite loops during execution order calculation. Performance estimation handles missing or invalid duration values by defaulting to zero and provides fallback emoji mapping for unknown task types in preview generation.

########## Internal Implementation Details

The task validation system uses dictionary-based required key checking with list comprehensions: `missing_keys = [key for key in required_keys if key not in self.metadata]` providing efficient validation for task-type-specific requirements. Dependency level calculation uses iterative algorithm with remaining task tracking, processing tasks with no unresolved dependencies in each iteration and incrementing level counters until all tasks are assigned levels. The caching mechanism uses `Optional` fields initialized to `None` with property-based lazy computation, checking cache validity before expensive calculations and storing results for subsequent access. Path truncation implements upfront truncation with character counting: `chars_to_keep = max_length - 3` reserving space for "..." prefix and ensuring total length constraints are respected. Task ordering uses multi-key sorting with tuple-based comparison: `(dependency_level, -priority, created_at)` ensuring proper execution order respecting dependencies, priorities, and creation timing. The preview system uses emoji mapping dictionaries and string formatting with consistent section headers, providing comprehensive execution plan visualization with task counts, dependency analysis, and detailed task listings for debugging and verification workflows.

########### Code Usage Examples

**Creating atomic tasks with comprehensive validation and metadata:** This example demonstrates creating validated atomic tasks with complete execution specification and task-type-specific metadata for independent execution.

```python
# Create LLM analysis task with required metadata
llm_task = AtomicTask(
    task_id="analyze_main_py",
    task_type=TaskType.ANALYZE_FILE_LLM,
    target_path=Path("src/main.py"),
    dependencies=["cleanup_orphaned", "create_cache_structure"],
    estimated_duration=30.0,
    priority=50,
    metadata={
        "file_size": 1024,
        "last_modified": "2025-01-01T12:00:00",
        "source_root": "/project/root"
    }
)

# Task validation occurs automatically in __post_init__
print(f"Task created: {llm_task.description}")
print(f"Is expensive: {llm_task.is_expensive}")
```

**Building execution plans with dependency validation and analysis:** This example shows creating comprehensive execution plans with dependency validation, task ordering, and parallel execution analysis for optimal resource utilization.

```python
# Create execution plan and add tasks
plan = ExecutionPlan(source_root=Path("/project/root"))
plan.add_task(llm_task)
plan.add_task(cleanup_task)

# Validate dependencies and get execution order
validation_errors = plan.validate_dependencies()
if not validation_errors:
    execution_order = plan.get_execution_order()
    parallel_groups = plan.get_parallel_execution_groups()
    
    print(f"Plan valid: {len(execution_order)} tasks in {len(parallel_groups)} levels")
    print(f"Estimated duration: {plan.total_estimated_duration:.1f}s")
    print(f"Expensive tasks: {plan.expensive_task_count}")
else:
    print(f"Validation errors: {validation_errors}")
```

**Comprehensive execution tracking and performance analysis:** This example demonstrates detailed execution result tracking with performance metrics, success rate calculation, and comprehensive reporting for optimization purposes.

```python
# Track execution results with comprehensive metrics
results = ExecutionResults(
    plan_id=plan.plan_id,
    execution_start=datetime.now()
)

# Record task outcomes during execution
results.add_completed_task("analyze_main_py")
results.add_failed_task("create_kb_utils", "LLM timeout error")
results.llm_calls_made = 5
results.files_processed = 10

# Complete execution and generate summary
results.complete_execution()
summary = results.get_summary()
print(f"Success rate: {results.success_rate:.1%}")
print(f"Total duration: {results.total_duration:.1f}s")
print(summary)
```
<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/plan_generator.py -->
<!-- Cached On: 2025-07-07T00:58:10.622880 -->
<!-- Source Modified: 2025-07-07T00:54:17.820516 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

Decision-to-plan translation engine converting `RebuildDecisionEngine` decisions into comprehensive atomic task execution plans for the Jesse Framework MCP knowledge base system. Provides Plan-then-Execute architecture implementation through `PlanGenerator` class that transforms high-level rebuild and deletion decisions into `ExecutionPlan` objects containing `AtomicTask` instances with proper dependencies and resource estimation. Enables developers to create reliable, debuggable execution workflows with comprehensive task metadata, dependency management, and performance estimation for hierarchical knowledge base processing. Key semantic entities include `PlanGenerator`, `ExecutionPlan`, `AtomicTask`, `TaskType`, `DecisionReport`, `RebuildDecision`, `DeletionDecision`, `DirectoryContext`, `FileContext`, `IndexingConfig`, `DecisionOutcome`, `DecisionReason`, `fastmcp.Context`, `pathlib.Path`, and `datetime` for comprehensive plan generation using five-phase workflow creating cleanup, cache structure, file processing, directory processing, and verification tasks with horizontal dependency management.

##### Main Components

Core `PlanGenerator` class serving as the primary decision-to-plan translation component with comprehensive task generation methods including `create_execution_plan()` for complete plan orchestration, `_generate_cleanup_tasks()` for deletion operations, `_generate_cache_structure_task()` for directory preparation, `_generate_file_tasks()` and `_generate_file_tasks_recursive()` for file processing, and `_generate_directory_tasks()` with `_generate_directory_tasks_recursive()` for knowledge base generation. Supporting utility methods including `_collect_cache_directories()` for structure preparation, `_get_base_dependencies()` for dependency management, `_collect_sibling_directory_tasks()` for horizontal dependencies, and `_sanitize_path_for_id()` for task identifier generation. Performance estimation parameters including `llm_analysis_duration`, `kb_generation_duration`, `file_operation_duration`, and `cleanup_operation_duration` for accurate resource planning.

###### Architecture & Design

Implements five-phase plan generation architecture: Phase 1 generates cleanup tasks with no dependencies for early execution, Phase 2 creates cache structure tasks for directory preparation, Phase 3 generates file processing tasks depending on cleanup and structure, Phase 4 creates directory tasks depending on file tasks with horizontal sibling dependencies, and Phase 5 adds verification tasks depending on all processing operations. Uses leaf-first recursive processing ensuring proper hierarchical dependency ordering where parent directories wait for all child directories and files. Employs atomic task decomposition with comprehensive metadata embedding eliminating external state dependencies during execution. Implements horizontal dependency management through sibling task collection ensuring parent directories synchronize with all sibling completion before processing.

####### Implementation Approach

Executes decision-driven task generation matching `RebuildDecisionEngine` decisions exactly to appropriate `TaskType` instances including `ANALYZE_FILE_LLM`, `SKIP_FILE_CACHED`, `CREATE_DIRECTORY_KB`, `SKIP_DIRECTORY_FRESH`, `DELETE_ORPHANED_FILE`, `DELETE_ORPHANED_DIRECTORY`, `CREATE_CACHE_STRUCTURE`, `VERIFY_CACHE_FRESHNESS`, and `VERIFY_KB_FRESHNESS`. Uses recursive directory traversal with consistent task ID generation through path sanitization ensuring reliable dependency resolution. Implements comprehensive metadata embedding including file characteristics, decision reasoning, directory contexts, and execution parameters for independent task execution. Employs priority-based task ordering with cleanup tasks at priority 100, file tasks at priority 50, directory tasks at priority 30, and verification tasks at priority 10 for optimal execution sequencing.

######## External Dependencies & Integration Points

**→ Inbound:**
- `fastmcp.Context` - FastMCP framework context interface for async progress reporting and logging during plan generation
- `jesse_framework_mcp.knowledge_bases.models:IndexingConfig` - Configuration object providing processing parameters and estimation settings
- `jesse_framework_mcp.knowledge_bases.models:DirectoryContext` - Directory structure representation with file and subdirectory contexts for task creation
- `jesse_framework_mcp.knowledge_bases.models:FileContext` - Individual file metadata including path, size, and timestamps for task metadata embedding
- `jesse_framework_mcp.knowledge_bases.models.rebuild_decisions` - Decision model classes including `DecisionReport`, `RebuildDecision`, `DeletionDecision` for decision-to-task translation
- `jesse_framework_mcp.knowledge_bases.models.execution_plan` - Execution planning models including `ExecutionPlan`, `AtomicTask`, `TaskType` for plan construction
- `pathlib.Path` (external library) - Cross-platform path operations and task target specification
- `datetime` (external library) - Timestamp generation for plan IDs and task metadata
- `logging` (external library) - Structured logging for plan generation analysis and debugging

**← Outbound:**
- `jesse_framework_mcp.knowledge_bases.indexing.hierarchical_indexer:HierarchicalIndexer` - Consumes execution plans for coordinated task execution
- Task execution engines - Receive atomic tasks with complete metadata for independent execution
- Monitoring and progress reporting systems - Consume task estimates and execution planning information
- Debugging and validation tools - Use comprehensive task metadata for execution analysis

**⚡ System role and ecosystem integration:**
- **System Role**: Critical translation component bridging decision-making and execution phases in the Jesse Framework MCP Plan-then-Execute architecture for knowledge base processing
- **Ecosystem Position**: Core component enabling reliable execution planning by converting high-level decisions into atomic, dependency-aware tasks with comprehensive metadata
- **Integration Pattern**: Used by hierarchical indexer to transform decision reports into executable plans, with generated tasks consumed by execution engines and monitoring systems

######### Edge Cases & Error Handling

Handles missing decisions by logging warnings and skipping task creation when `DecisionReport` lacks decisions for specific files or directories. Manages circular dependency prevention by avoiding sibling dependencies in directory task generation, using parent-child relationships exclusively for dependency management. Implements comprehensive plan validation through `ExecutionPlan.validate_dependencies()` ensuring all task dependencies are resolvable before execution begins. Provides graceful error handling in sibling collection with try-catch blocks returning empty lists when path calculations fail. Uses safe path sanitization preventing invalid task IDs from special characters or path separators while maintaining uniqueness across different files and directories.

########## Internal Implementation Details

Maintains performance estimation parameters as instance variables enabling realistic duration calculations for different task types with `llm_analysis_duration` at 30 seconds, `kb_generation_duration` at 15 seconds, and fast operations under 0.1 seconds. Uses consistent task ID generation through `_sanitize_path_for_id()` replacing path separators and special characters with underscores while removing consecutive underscores for clean identifiers. Implements comprehensive metadata embedding including file sizes, modification timestamps, decision reasoning, directory contexts, and dependency counts for complete task execution context. Employs priority-based task ordering ensuring cleanup executes first, followed by structure creation, file processing, directory processing, and verification last through numerical priority values.

########### Code Usage Examples

Essential plan generation workflow for converting decisions to executable tasks:

```python
# Initialize plan generator with configuration for task estimation and metadata
config = IndexingConfig(output_config=OutputConfig(knowledge_output_directory=knowledge_dir))
plan_generator = PlanGenerator(config)

# Create comprehensive execution plan from decision report and directory context
execution_plan = await plan_generator.create_execution_plan(
    root_context, decision_report, source_root, ctx
)

# Access generated tasks and execution metadata for processing coordination
total_tasks = len(execution_plan.tasks)
expensive_tasks = execution_plan.expensive_task_count
estimated_duration = sum(task.estimated_duration for task in execution_plan.tasks)
```

Task dependency analysis and execution ordering for debugging and monitoring:

```python
# Analyze task dependencies and execution ordering for validation
validation_errors = execution_plan.validate_dependencies()
if validation_errors:
    logger.error(f"Plan validation failed: {validation_errors}")

# Access individual tasks with complete metadata for execution engines
for task in execution_plan.tasks:
    task_type = task.task_type
    dependencies = task.dependencies
    metadata = task.metadata
    priority = task.priority
    estimated_duration = task.estimated_duration
```
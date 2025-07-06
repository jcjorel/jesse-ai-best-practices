<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/execution_engine.py -->
<!-- Cached On: 2025-07-06T23:42:01.411166 -->
<!-- Source Modified: 2025-07-06T23:40:39.056410 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

The `ExecutionEngine` class serves as the core execution orchestrator for the Jesse Framework's Plan-then-Execute architecture within the Knowledge Bases Hierarchical Indexing System. This component transforms `ExecutionPlan` objects containing atomic tasks into concrete file system operations, LLM-powered analysis, and knowledge base generation. The engine provides concurrent task execution with dependency resolution, comprehensive progress reporting, and robust error handling for reliable knowledge base construction. Key semantic entities include `ExecutionEngine`, `AtomicTask`, `TaskType`, `ExecutionResults`, `KnowledgeBuilder`, `FileAnalysisCache`, `DirectoryContext`, `FileContext`, `ProcessingStatus`, `IndexingConfig`, and `asyncio` semaphore-based concurrency control. The implementation leverages task dispatch patterns with specialized handlers for nine distinct task types including `ANALYZE_FILE_LLM`, `CREATE_DIRECTORY_KB`, and orphaned file cleanup operations.

##### Main Components

The execution engine contains several primary components: the `ExecutionEngine` class as the main orchestrator, task execution handlers dictionary (`_task_handlers`) mapping `TaskType` enum values to specialized async methods, concurrency control through `_execution_semaphore` limiting parallel operations, execution state tracking sets (`_completed_tasks`, `_failed_tasks`, `_running_tasks`), integrated `KnowledgeBuilder` for LLM-powered content analysis, and `FileAnalysisCache` for performance optimization. The engine includes nine specialized task handlers: `_execute_analyze_file_llm`, `_execute_skip_file_cached`, `_execute_create_directory_kb`, `_execute_skip_directory_fresh`, `_execute_delete_orphaned_file`, `_execute_delete_orphaned_directory`, `_execute_create_cache_structure`, `_execute_verify_cache_freshness`, and `_execute_verify_kb_freshness`. Additional utility components include `_strip_cache_metadata` for content cleaning, `_load_cached_analysis_content` for cache integration, and `_cleanup_execution_resources` for resource management.

###### Architecture & Design

The architecture implements a Plan-then-Execute pattern with atomic task execution ensuring complete task isolation and independent processing. The design uses dependency-aware execution respecting task prerequisites through `_are_dependencies_satisfied` validation, concurrent execution optimization via `asyncio.Semaphore` for resource utilization, and comprehensive progress reporting providing real-time execution status. The system employs a task dispatch pattern routing different `TaskType` values to specialized handlers, maintains execution state through set-based tracking of task completion status, and integrates existing components (`KnowledgeBuilder`, `FileAnalysisCache`) for seamless operation. Error handling enables graceful degradation with configurable `continue_on_file_errors` behavior, while resource management prevents memory leaks through proper cleanup procedures. The architecture supports both preview mode for plan analysis and full execution mode with performance metrics collection.

####### Implementation Approach

The implementation uses `asyncio` for concurrent task execution with semaphore-based concurrency control limiting parallel operations to `config.max_concurrent_operations`. Task execution follows dependency resolution through `plan.get_execution_order()` providing topologically sorted task sequences, with each task validated via `_are_dependencies_satisfied` before execution. The engine employs task dispatch using a handler dictionary mapping `TaskType` enum values to specialized async methods, maintaining execution state through three sets tracking completed, failed, and running tasks. Content processing involves reconstructing `FileContext` and `DirectoryContext` objects from task metadata, loading cached analysis content via `_load_cached_analysis_content`, and stripping metadata contamination through `_strip_cache_metadata`. Performance optimization includes bypass cache flags for stale content, parallel execution opportunities through dependency analysis, and comprehensive metrics collection in `ExecutionResults` objects. Error handling implements configurable failure behavior with detailed logging and graceful task failure recovery.

######## External Dependencies & Integration Points

**→ Inbound:**
- `..models.IndexingConfig` - Configuration parameters for execution behavior and resource limits
- `..models.DirectoryContext` - Directory processing context with file relationships and metadata
- `..models.FileContext` - File processing context with analysis results and status tracking
- `..models.ProcessingStatus` - Enumeration for tracking processing state transitions
- `..models.execution_plan.ExecutionPlan` - Plan objects containing atomic tasks and dependencies
- `..models.execution_plan.AtomicTask` - Individual task definitions with metadata and requirements
- `..models.execution_plan.TaskType` - Task type enumeration for handler dispatch
- `..models.execution_plan.ExecutionResults` - Results collection with performance metrics
- `.knowledge_builder.KnowledgeBuilder` - LLM-powered content analysis and KB generation
- `.file_analysis_cache.FileAnalysisCache` - Caching system for performance optimization
- `fastmcp.Context` - FastMCP context for progress reporting and logging
- `asyncio` (external library) - Async programming patterns and concurrency control
- `pathlib.Path` (external library) - Cross-platform path operations and file metadata
- `logging` (external library) - Structured logging for execution analysis

**← Outbound:**
- `jesse_framework_mcp/knowledge_bases/indexing/hierarchical_indexer.py:HierarchicalIndexer` - Main indexer consuming execution results
- `generated/knowledge_base_files/*.md` - Generated knowledge base files from directory processing
- `generated/cache_files/*.analysis.md` - Cached analysis files from LLM processing
- `logging_system` - Structured execution logs for debugging and monitoring

**⚡ System role and ecosystem integration:**
- **System Role**: Core execution engine transforming declarative execution plans into concrete file system operations and knowledge base generation within the Jesse Framework's hierarchical indexing workflow
- **Ecosystem Position**: Central component bridging high-level planning (`ExecutionPlan`) with low-level operations (`KnowledgeBuilder`, `FileAnalysisCache`) in the Plan-then-Execute architecture
- **Integration Pattern**: Used by `HierarchicalIndexer` for executing complex indexing workflows, consuming plans from planning components, and coordinating with FastMCP for progress reporting to human operators

######### Edge Cases & Error Handling

The engine handles multiple error scenarios including dependency validation failures where tasks cannot execute due to unsatisfied prerequisites, individual task execution failures with configurable `continue_on_file_errors` behavior allowing workflow continuation, and resource exhaustion through semaphore-based concurrency limiting. Cache-related edge cases include missing cached analysis content handled by `_load_cached_analysis_content` with fallback to placeholder text, metadata contamination prevented by `_strip_cache_metadata` stripping XML tags, and stale cache detection triggering LLM re-analysis. File system edge cases cover orphaned file deletion with safety checks via `is_safe_to_delete` metadata, empty directory removal using `rmdir()` for non-empty directory protection, and missing file handling during verification tasks. The system provides comprehensive error reporting through `ExecutionResults.failed_tasks` with detailed error messages, graceful degradation allowing partial execution completion, and proper resource cleanup via `_cleanup_execution_resources` preventing memory leaks. Debugging support includes detailed logging at multiple levels, execution state tracking through running/completed/failed task sets, and preview mode for plan analysis without side effects.

########## Internal Implementation Details

The execution engine maintains internal state through three sets: `_completed_tasks`, `_failed_tasks`, and `_running_tasks` for tracking task lifecycle progression. Concurrency control uses `asyncio.Semaphore(config.max_concurrent_operations)` with async context manager pattern in `_execute_single_task` for resource management. Task metadata reconstruction involves complex object rebuilding from serialized task data, particularly for `DirectoryContext` objects requiring `knowledge_file_path` assignment and `FileContext` objects needing cached content loading. The `_strip_cache_metadata` method uses regex pattern `r'<!-- CACHE_METADATA_START -->.*?<!-- CACHE_METADATA_END -->\s*'` with `DOTALL` flag for multiline metadata block removal. Cache integration through `_load_cached_analysis_content` handles file system errors gracefully, returning `None` for missing content to enable fallback behavior. Performance metrics collection in `ExecutionResults` tracks `llm_calls_made`, `files_processed`, `directories_processed`, and `files_deleted` with execution duration calculation. Resource cleanup involves `knowledge_builder.cleanup()` for connection management and execution state clearing for memory management. The task handler dispatch system uses dictionary lookup with runtime error handling for missing handlers, ensuring robust task execution even with configuration errors.

########### Code Usage Examples

**Basic execution engine initialization and plan execution:**
```python
# Initialize execution engine with configuration
config = IndexingConfig(max_concurrent_operations=4, continue_on_file_errors=True)
engine = ExecutionEngine(config)

# Execute a complete plan with progress reporting
async def execute_indexing_plan(plan: ExecutionPlan, ctx: Context):
    results = await engine.execute_plan(plan, ctx)
    print(f"Completed: {len(results.completed_tasks)}, Failed: {len(results.failed_tasks)}")
    print(f"LLM calls: {results.llm_calls_made}, Duration: {results.total_duration:.1f}s")
    return results
```

**Plan preview for debugging and analysis:**
```python
# Preview execution plan without executing tasks
async def preview_execution_strategy(plan: ExecutionPlan, ctx: Context):
    await engine.preview_plan(plan, ctx)
    # Shows task dependencies, execution order, and resource requirements
```

**Custom task execution with error handling:**
```python
# Execute individual tasks with dependency validation
async def execute_with_validation(task: AtomicTask, ctx: Context):
    if engine._are_dependencies_satisfied(task):
        await engine._execute_single_task(task, ctx)
        print(f"Task {task.task_id} completed successfully")
    else:
        print(f"Dependencies not satisfied for {task.task_id}")
```
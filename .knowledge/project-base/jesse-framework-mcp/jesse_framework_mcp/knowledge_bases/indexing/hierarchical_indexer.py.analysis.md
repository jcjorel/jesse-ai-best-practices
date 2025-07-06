<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/hierarchical_indexer.py -->
<!-- Cached On: 2025-07-06T20:56:51.157555 -->
<!-- Source Modified: 2025-07-06T20:36:29.172897 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This module implements the core orchestrator for hierarchical knowledge base indexing using a Plan-then-Execute architecture that separates decision-making from execution for perfect debuggability. The functional intent centers on coordinating leaf-first processing strategies to build hierarchical knowledge files throughout directory structures using bottom-up assembly approaches. Key semantic entities include `HierarchicalIndexer` class implementing the main orchestration logic, `RebuildDecisionEngine` for centralized decision-making, `PlanGenerator` for converting decisions into atomic tasks, `ExecutionEngine` for dependency-aware task execution, and integration with `FastMCP` `Context` for real-time progress reporting. The module provides comprehensive change detection through `DirectoryContext` and `FileContext` models, supports concurrent processing with configurable limits, and implements defensive error handling enabling graceful degradation and partial processing recovery for large-scale knowledge base maintenance operations.

##### Main Components

The module contains the `HierarchicalIndexer` class as the primary orchestrator with methods for complete indexing workflow coordination, `index_hierarchy()` method implementing the five-phase Plan-then-Execute architecture, `_discover_directory_structure()` and `_build_directory_context()` methods for recursive directory structure discovery, `_detect_changes()` and `_apply_comprehensive_change_detection()` methods for change detection using `RebuildDecisionEngine` integration, `_generate_execution_plan()`, `_preview_execution_plan()`, and `_execute_plan_with_progress()` methods for atomic task planning and execution, and utility methods including `_get_all_directories()` for hierarchy traversal and `_create_final_status()` for result mapping to `IndexingStatus` format.

###### Architecture & Design

The architecture implements Plan-then-Execute pattern separating decision-making from execution through distinct phases: Discovery builds complete `DirectoryContext` hierarchy, Decision Analysis generates comprehensive `DecisionReport` with change detection, Plan Generation converts decisions into atomic `ExecutionPlan` with dependencies, Plan Preview provides detailed execution analysis for debuggability, and Atomic Execution performs dependency-aware task execution. Design principles emphasize leaf-first hierarchical processing ensuring child completion before parent processing, bottom-up assembly aggregating child summaries into parent knowledge files, async-first architecture supporting concurrent operations with `FastMCP` `Context` integration, modular component delegation to specialized handlers, and defensive programming with comprehensive error handling and recovery mechanisms.

####### Implementation Approach

The implementation utilizes recursive directory discovery building complete hierarchy context through `_build_directory_context()` with configuration filtering via `should_process_file()` and `should_process_directory()` methods. Change detection employs `RebuildDecisionEngine.should_rebuild_directory()` for centralized decision-making with comprehensive constituent dependency checking. The Plan-then-Execute workflow delegates to `PlanGenerator.create_execution_plan()` for atomic task generation, `ExecutionEngine.preview_plan()` for detailed execution analysis, and `ExecutionEngine.execute_plan()` for dependency-aware task execution. Processing coordination maintains `IndexingStatus` with real-time progress updates, `ProcessingStats` for performance metrics, and error handling enabling graceful degradation through configurable `continue_on_file_errors` behavior.

######## External Dependencies & Integration Points

**→ Inbound:**
- `..models.IndexingConfig` - Configuration and filtering logic for processing rules and limits
- `..models.DirectoryContext` - Directory structure representation with processing status tracking
- `..models.FileContext` - File metadata and processing state management
- `..models.ProcessingStatus` - Status enumeration for processing state tracking
- `..models.IndexingStatus` - Comprehensive indexing operation status reporting
- `.rebuild_decision_engine.RebuildDecisionEngine` - Centralized decision-making for change detection
- `.knowledge_builder.KnowledgeBuilder` - LLM-powered content summarization and knowledge file generation
- `.special_handlers.ProjectBaseHandler` - Project-base specialized processing for whole codebase indexing
- `.special_handlers.GitCloneHandler` - Git-clone specialized processing for read-only repository handling
- `.plan_generator.PlanGenerator` - Decision-to-task conversion for atomic execution planning
- `.execution_engine.ExecutionEngine` - Dependency-aware atomic task execution with progress reporting
- `fastmcp.Context` (external library) - Real-time progress reporting and user interaction
- `asyncio` (standard library) - Async programming patterns and concurrency control
- `pathlib.Path` (standard library) - Cross-platform path operations and filesystem interaction

**← Outbound:**
- Knowledge base indexing tools consuming `HierarchicalIndexer.index_hierarchy()` method
- MCP server implementations requiring hierarchical processing coordination
- JESSE Framework components needing structured knowledge base maintenance
- Monitoring systems accessing `current_status` property for real-time progress tracking

**⚡ System role and ecosystem integration:**
- **System Role**: Serves as the central orchestrator for the Knowledge Bases Hierarchical Indexing System, coordinating all phases of directory discovery, change detection, plan generation, and atomic task execution
- **Ecosystem Position**: Core component bridging high-level indexing requests with specialized processing engines, decision systems, and execution frameworks
- **Integration Pattern**: Consumed by MCP tools requiring hierarchical knowledge base maintenance, integrating with specialized handlers for git-clones and project-base scenarios, and coordinating with LLM-powered content generation through structured Plan-then-Execute workflows

######### Edge Cases & Error Handling

Error handling implements comprehensive exception catching with detailed logging through `logger.error()` calls including stack traces and graceful degradation options. Edge cases include filesystem access failures handled through `OSError` and `PermissionError` catching with continued processing, change detection failures triggering conservative fallback marking directories for processing, execution failures managed through configurable `continue_on_file_errors` behavior, and resource cleanup errors handled gracefully in `cleanup()` method. The system provides defensive programming patterns including validation of root path existence and directory status, comprehensive error statistics tracking through `ProcessingStats.add_error()`, and status determination based on execution success rates with configurable thresholds for partial success scenarios.

########## Internal Implementation Details

Internal mechanisms utilize `datetime.now()` for processing timing and performance metrics, recursive directory traversal through `_get_all_directories()` for comprehensive hierarchy analysis, and status mapping between `ExecutionResults` and `IndexingStatus` formats for API compatibility. The implementation maintains processing coordination through `_current_status` updates with real-time operation tracking, component initialization with dependency injection for `RebuildDecisionEngine`, `PlanGenerator`, and `ExecutionEngine`, and resource management through `cleanup()` method delegating to `ExecutionEngine._cleanup_execution_resources()`. Processing statistics include accurate file and directory counts, error tracking with detailed messages, and performance metrics including LLM call counts and execution duration measurements.

########### Code Usage Examples

**Basic hierarchical indexing initialization and execution:** This example demonstrates how to initialize the indexer with configuration and execute hierarchical processing with progress reporting capabilities.

```python
from pathlib import Path
from fastmcp import Context
from jesse_framework_mcp.knowledge_bases.models import IndexingConfig
from jesse_framework_mcp.knowledge_bases.indexing.hierarchical_indexer import HierarchicalIndexer

# Initialize indexer with configuration
config = IndexingConfig()
indexer = HierarchicalIndexer(config)

# Execute hierarchical indexing with progress reporting
async def run_indexing():
    ctx = Context()
    root_path = Path(".knowledge/")
    status = await indexer.index_hierarchy(root_path, ctx)
    return status
```

**Real-time status monitoring during indexing operations:** This pattern enables monitoring of indexing progress with real-time status updates and progress percentage tracking.

```python
# Monitor indexing progress in real-time
async def monitor_indexing_progress(indexer):
    while indexer.current_status.overall_status == ProcessingStatus.PROCESSING:
        status = indexer.current_status
        print(f"Operation: {status.current_operation}")
        print(f"Progress: {status.processing_stats.progress_percentage:.1f}%")
        await asyncio.sleep(1)
```

**Plan-then-Execute architecture component access:** This example shows how to access the internal components of the Plan-then-Execute architecture and perform proper resource cleanup.

```python
# Access Plan-then-Execute architecture components
indexer = HierarchicalIndexer(config)
decision_engine = indexer.rebuild_decision_engine
plan_generator = indexer.plan_generator
execution_engine = indexer.execution_engine

# Cleanup resources after processing
await indexer.cleanup()
```
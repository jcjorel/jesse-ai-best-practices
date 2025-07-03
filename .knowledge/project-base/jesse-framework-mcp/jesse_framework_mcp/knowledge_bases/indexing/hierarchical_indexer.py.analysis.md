<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/hierarchical_indexer.py -->
<!-- Cached On: 2025-07-04T00:42:04.513624 -->
<!-- Source Modified: 2025-07-03T17:57:35.641806 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file serves as the core orchestrator for hierarchical knowledge base indexing within the JESSE Framework MCP system, implementing leaf-first processing strategy for building hierarchical knowledge files throughout directory structures using bottom-up assembly approach. The file provides comprehensive directory hierarchy processing capabilities with change detection, concurrent file processing, and specialized handling for different content types. Key semantic entities include `HierarchicalIndexer` class for orchestration, `IndexingConfig` for configuration management, `DirectoryContext` and `FileContext` for hierarchy representation, `ChangeDetector` for incremental processing, `KnowledgeBuilder` for content summarization, `GitCloneHandler` and `ProjectBaseHandler` for specialized scenarios, `ProcessingStatus` enumeration for state tracking, `IndexingStatus` for operation monitoring, `FastMCP Context` for progress reporting, and `asyncio` patterns for concurrent processing, evidenced by the class definition, method signatures, and comprehensive import statements throughout the implementation.

##### Main Components

Contains the `HierarchicalIndexer` class as the primary component with methods for complete hierarchy processing including `index_hierarchy()` for orchestration, `_discover_directory_structure()` for recursive discovery, `_detect_changes()` for incremental processing, `_process_directory_hierarchy()` for leaf-first processing, `_process_directory_leaf_first()` for recursive directory handling, `_process_directory_files()` for concurrent file processing, `_process_single_file()` for individual file handling, `_generate_directory_knowledge_file()` for summary generation, and utility methods for hierarchy navigation and status management. The class integrates with `ChangeDetector`, `KnowledgeBuilder`, `GitCloneHandler`, and `ProjectBaseHandler` components for specialized processing tasks. Processing coordination uses `asyncio.Semaphore` for concurrency control and comprehensive error handling throughout all operations.

###### Architecture & Design

Implements a modular architecture with dependency injection pattern enabling testability and component modularity through constructor-based initialization of specialized handlers. The design follows leaf-first processing principles ensuring child contexts are complete before parent processing, using bottom-up assembly pattern for hierarchical knowledge file generation. The architecture employs async-first design supporting concurrent operations with configurable limits through semaphore-based concurrency control. The system uses immutable context management with `DirectoryContext` and `FileContext` objects that are updated and returned rather than modified in place. Error handling follows defensive programming principles with comprehensive exception catching and graceful degradation when individual components fail.

####### Implementation Approach

Uses recursive directory traversal with leaf-first processing order implemented through depth-first traversal that processes subdirectories before parent directories. The implementation employs batch processing for file operations using configurable batch sizes and `asyncio.gather()` for concurrent execution within batches. Change detection uses comprehensive analysis through `ChangeDetector.check_comprehensive_directory_change()` method that evaluates constituent dependencies and cache staleness. The approach integrates `FileAnalysisCache` for performance optimization on unchanged files by passing `source_root` parameter to enable caching mechanisms. Processing statistics are maintained throughout operations with detailed tracking of files processed, directories completed, errors encountered, and timing information for performance analysis.

######## Code Usage Examples

Initialize the hierarchical indexer with configuration and process a directory hierarchy. This demonstrates the primary usage pattern for complete hierarchy processing:

```python
from jesse_framework_mcp.knowledge_bases.indexing.hierarchical_indexer import HierarchicalIndexer
from jesse_framework_mcp.knowledge_bases.models import IndexingConfig

config = IndexingConfig(
    indexing_mode="incremental",
    max_concurrent_operations=4,
    batch_size=10,
    continue_on_file_errors=True
)
indexer = HierarchicalIndexer(config)
status = await indexer.index_hierarchy(Path("/project/root"), ctx)
```

Monitor processing status and handle results from hierarchical indexing operations. This shows how to access real-time status information and processing statistics:

```python
# Access current processing status
current_status = indexer.current_status
print(f"Status: {current_status.overall_status}")
print(f"Operation: {current_status.current_operation}")
print(f"Files processed: {current_status.processing_stats.files_processed}")

# Handle completion
if status.overall_status == ProcessingStatus.COMPLETED:
    duration = status.processing_stats.processing_duration
    print(f"Indexing completed in {duration:.2f} seconds")
```

Implement custom error handling and cleanup for hierarchical indexing operations. This demonstrates proper resource management and error recovery patterns:

```python
try:
    status = await indexer.index_hierarchy(root_path, ctx)
    if status.overall_status == ProcessingStatus.FAILED:
        for error in status.processing_stats.errors:
            logger.error(f"Processing error: {error}")
finally:
    await indexer.cleanup()
```

######### External Dependencies & Integration Points

**→ Inbound:**

- `..models.indexing_config:IndexingConfig` - configuration and filtering logic for processing behavior
- `..models.knowledge_context:DirectoryContext` - directory context structures and processing state
- `..models.knowledge_context:FileContext` - file context structures and metadata
- `..models.knowledge_context:ProcessingStatus` - enumeration for processing state tracking
- `..models.knowledge_context:IndexingStatus` - comprehensive status tracking for operations
- `.change_detector:ChangeDetector` - change detection and timestamp comparison logic
- `.knowledge_builder:KnowledgeBuilder` - LLM-powered content summarization and analysis
- `.special_handlers:GitCloneHandler` - specialized handling for git-clone scenarios
- `.special_handlers:ProjectBaseHandler` - specialized handling for project-base scenarios
- `fastmcp:Context` (external library) - progress reporting and user interaction
- `asyncio` (standard library) - async programming patterns and concurrency control
- `pathlib:Path` (standard library) - cross-platform path operations
- `logging` (standard library) - structured logging and error reporting

**← Outbound:**

- Knowledge base consumers - systems that process generated hierarchical knowledge files
- MCP server endpoints - systems that expose hierarchical indexing capabilities
- CI/CD pipelines - automated systems that trigger hierarchical processing
- Development workflows/ - systems that integrate hierarchical indexing into development processes

**⚡ Integration:**

- Protocol: Direct Python imports with async/await patterns and context manager usage
- Interface: Class instantiation with IndexingConfig, async method calls with FastMCP Context
- Coupling: Tight coupling with models and component classes, loose coupling with external systems through configuration

########## Edge Cases & Error Handling

Handles missing or inaccessible directories through comprehensive filesystem error catching with `OSError` and `PermissionError` exceptions, logging warnings and continuing processing when individual items are inaccessible. Addresses change detection failures by implementing conservative fallback behavior that marks directories for processing when detection fails, preventing missed updates. Manages concurrent processing errors through semaphore-based concurrency control and individual file error handling that prevents single file failures from stopping entire hierarchy processing. Handles knowledge file generation failures with configurable error behavior through `continue_on_file_errors` setting that enables graceful degradation. Addresses resource cleanup failures through comprehensive cleanup methods with error logging that prevents cleanup exceptions from cascading to calling code.

########### Internal Implementation Details

The class maintains internal state through `_current_status` field containing `IndexingStatus` object with comprehensive processing statistics and progress information. Processing coordination uses `_processing_semaphore` initialized with `config.max_concurrent_operations` for controlling concurrent file processing operations. The implementation stores `_source_root` during processing to enable cache-aware operations in `KnowledgeBuilder` and `ChangeDetector` components. Context management follows immutable patterns where `DirectoryContext` and `FileContext` objects are created with updated information rather than modified in place. Statistics tracking includes detailed timing information with `processing_start_time` and `processing_end_time` fields, error collection with `add_error()` method, and comprehensive counters for files processed, directories completed, and operation failures. The leaf-first processing algorithm uses recursive traversal that processes all subdirectories before attempting parent directory knowledge file generation, ensuring proper dependency order for hierarchical assembly.
<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/hierarchical_indexer.py -->
<!-- Cached On: 2025-07-04T16:50:47.162160 -->
<!-- Source Modified: 2025-07-04T16:50:11.009117 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements the core orchestrator for hierarchical knowledge base indexing in the Jesse Framework MCP system, providing leaf-first processing strategy for building structured knowledge files throughout directory hierarchies. The `HierarchicalIndexer` class coordinates comprehensive change detection, concurrent file processing, and bottom-up assembly of hierarchical knowledge files using the `ChangeDetector`, `KnowledgeBuilder`, `GitCloneHandler`, and `ProjectBaseHandler` components. Key semantic entities include `IndexingConfig`, `DirectoryContext`, `FileContext`, `ProcessingStatus`, `IndexingStatus`, `ProcessingStats`, `FastMCP Context`, `strands_agent_driver`, `FileAnalysisCache`, and `asyncio` semaphore-based concurrency control. The system provides incremental processing capabilities through comprehensive change detection using `check_comprehensive_directory_change()` method, enabling efficient rebuilds when only modified files require reprocessing.

##### Main Components

The file contains the `HierarchicalIndexer` class as the primary orchestrator with key methods including `index_hierarchy()` for complete directory processing, `_discover_directory_structure()` for recursive file enumeration, `_detect_changes()` for incremental processing optimization, `_process_directory_hierarchy()` for leaf-first traversal coordination, `_process_directory_leaf_first()` for recursive directory processing, `_process_directory_files()` for concurrent file batch processing, `_process_single_file()` for individual file delegation, and `_generate_directory_knowledge_file()` for hierarchical summary creation. Supporting utility methods include `_build_directory_context()` for context construction, `_apply_comprehensive_change_detection()` for recursive change evaluation, and `_get_all_directories()` for statistics calculation.

###### Architecture & Design

The architecture implements a modular orchestration pattern with clear separation of concerns between change detection, content building, and special handling components. The design follows dependency injection principles with `IndexingConfig` driving behavior and specialized handlers managing git-clone and project-base scenarios. The leaf-first processing strategy ensures bottom-up assembly without parent-to-child context dependencies, using immutable `DirectoryContext` and `FileContext` objects for state management. Async-first architecture supports concurrent operations through `asyncio.Semaphore` for concurrency control and `FastMCP Context` for real-time progress reporting. The system implements defensive programming with comprehensive error handling and configurable failure recovery through `continue_on_file_errors` setting.

####### Implementation Approach

The implementation uses recursive depth-first traversal with leaf-first processing order, ensuring child directories complete before parent knowledge file generation. Concurrent processing occurs at the file level within directories using configurable batch sizes and semaphore-controlled concurrency limits. Change detection integrates `FileAnalysisCache` through `check_comprehensive_directory_change()` method for timestamp-based staleness evaluation and constituent dependency checking. The system maintains processing statistics through `ProcessingStats` class tracking files processed, directories completed, errors encountered, and timing metrics. Context management uses immutable data structures with explicit state updates, creating new `DirectoryContext` and `FileContext` instances rather than modifying existing ones.

######## External Dependencies & Integration Points

**→ Inbound:**
- `..models.indexing_config:IndexingConfig` - Configuration and filtering logic for processing behavior
- `..models.knowledge_context:DirectoryContext` - Directory structure and processing state management
- `..models.knowledge_context:FileContext` - Individual file metadata and processing status
- `.change_detector:ChangeDetector` - Comprehensive change detection and timestamp comparison
- `.knowledge_builder:KnowledgeBuilder` - LLM-powered content summarization and analysis
- `.special_handlers:GitCloneHandler` - Git repository clone handling
- `.special_handlers:ProjectBaseHandler` - Project base directory special processing
- `fastmcp:Context` - Progress reporting and user feedback interface
- `asyncio` (external library) - Async programming and concurrency control
- `pathlib` (external library) - Cross-platform path operations

**← Outbound:**
- `jesse_framework_mcp/main.py:index_command` - Main indexing command execution
- `jesse_framework_mcp/cli/` - Command-line interface integration
- `generated/.knowledge/` - Hierarchical knowledge file output structure

**⚡ System role and ecosystem integration:**
- **System Role**: Central orchestrator for the Jesse Framework MCP knowledge base indexing system, coordinating all phases of hierarchical processing from discovery through knowledge file generation
- **Ecosystem Position**: Core component that integrates change detection, content building, and special handling subsystems into cohesive workflow execution
- **Integration Pattern**: Used by CLI commands and main application entry points for complete directory hierarchy processing, with real-time progress reporting through FastMCP Context for user interfaces

######### Edge Cases & Error Handling

The system handles filesystem access errors through `OSError` and `PermissionError` catching with graceful degradation and continued processing. Truncation detection in LLM output returns `None` from `_process_single_file()` to completely omit files from processing rather than including incomplete analysis. Change detection failures trigger conservative fallback behavior marking directories for processing to prevent stale knowledge files. Individual file processing errors are isolated through semaphore-controlled concurrent processing, preventing cascading failures across file batches. The `continue_on_file_errors` configuration enables partial processing completion when individual components fail, with comprehensive error tracking through `ProcessingStats.add_error()` method.

########## Internal Implementation Details

The `_processing_semaphore` uses `asyncio.Semaphore` with `config.max_concurrent_operations` limit to prevent resource exhaustion during concurrent file processing. Context immutability is maintained through explicit `DirectoryContext` and `FileContext` reconstruction rather than in-place modification, ensuring proper state tracking throughout recursive processing. The `_source_root` attribute enables `FileAnalysisCache` integration by providing consistent path resolution for cache key generation and staleness detection. Processing statistics are updated atomically through dedicated methods preventing race conditions in concurrent processing scenarios. The leaf-first traversal algorithm uses recursive `_process_directory_leaf_first()` calls with explicit subdirectory context collection before parent processing, ensuring proper dependency order.

########### Code Usage Examples

**Basic hierarchical indexing execution:**
```python
config = IndexingConfig(indexing_mode=IndexingMode.INCREMENTAL)
indexer = HierarchicalIndexer(config)
status = await indexer.index_hierarchy(Path("/project/src"), ctx)
print(f"Processed {status.processing_stats.files_completed} files")
```

**Monitoring indexing progress:**
```python
indexer = HierarchicalIndexer(config)
task = asyncio.create_task(indexer.index_hierarchy(root_path, ctx))
while not task.done():
    status = indexer.current_status
    print(f"Progress: {status.processing_stats.progress_percentage:.1f}%")
    await asyncio.sleep(1)
```

**Error handling with graceful degradation:**
```python
config = IndexingConfig(continue_on_file_errors=True)
indexer = HierarchicalIndexer(config)
try:
    status = await indexer.index_hierarchy(root_path, ctx)
    if status.processing_stats.files_failed > 0:
        print(f"Completed with {status.processing_stats.files_failed} failures")
finally:
    await indexer.cleanup()
```
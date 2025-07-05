<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/hierarchical_indexer.py -->
<!-- Cached On: 2025-07-05T13:44:43.734991 -->
<!-- Source Modified: 2025-07-05T13:29:36.704303 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements the core orchestrator for hierarchical knowledge base indexing within the Jesse Framework MCP system, designed to coordinate leaf-first processing of directory hierarchies for building structured knowledge files throughout the `.knowledge/` directory structure. The module provides comprehensive indexing capabilities including change detection, content building, special handling, and orphaned file cleanup to maintain synchronized knowledge representations of source code repositories. Key semantic entities include `HierarchicalIndexer` class with `index_hierarchy` method, `ChangeDetector` for incremental processing, `KnowledgeBuilder` for LLM-powered content generation, `GitCloneHandler` and `ProjectBaseHandler` for special cases, `OrphanedAnalysisCleanup` for maintenance, `DirectoryContext` and `FileContext` data structures, `ProcessingStatus` and `IndexingStatus` enums, `FastMCP` context integration, and `asyncio` semaphore-based concurrency control. The system implements bottom-up assembly patterns aggregating child summaries into parent knowledge files while supporting both full and incremental indexing modes with comprehensive error handling and progress reporting.

##### Main Components

The file contains the `HierarchicalIndexer` class as the primary orchestrator with key methods including `index_hierarchy` for complete workflow coordination, `_discover_directory_structure` for recursive directory analysis, `_detect_changes` for incremental processing, `_process_directory_hierarchy` for leaf-first execution, `_process_directory_leaf_first` for recursive directory processing, `_process_directory_files` for concurrent file handling, `_process_single_file` for individual file analysis, and `_generate_directory_knowledge_file` for summary generation. The class integrates specialized components including `ChangeDetector` for timestamp-based change detection, `KnowledgeBuilder` for LLM content generation, `GitCloneHandler` and `ProjectBaseHandler` for special directory handling, and `OrphanedAnalysisCleanup` for maintenance operations. Supporting infrastructure includes processing semaphore for concurrency control, status tracking with `IndexingStatus`, and comprehensive error handling with configurable failure modes.

###### Architecture & Design

The architecture implements a modular orchestration pattern with clear separation of concerns between discovery, change detection, processing, and content generation phases. The design follows leaf-first processing strategy ensuring child contexts are completely processed before parent directory knowledge file generation, eliminating parent-to-child dependencies and enabling bottom-up assembly. The system uses dependency injection for component initialization, async-first architecture for concurrent operations, and immutable context management ensuring proper state updates throughout processing workflows. Key design patterns include the orchestrator pattern for workflow coordination, builder pattern delegation for content generation, semaphore-based concurrency control for performance optimization, and comprehensive error handling with graceful degradation capabilities.

####### Implementation Approach

The implementation uses a multi-phase processing approach starting with directory structure discovery, followed by optional change detection for incremental mode, then leaf-first hierarchical processing with concurrent file operations. The system implements recursive directory traversal with `_build_directory_context` creating nested `DirectoryContext` structures, comprehensive change detection using `check_comprehensive_directory_change` for constituent dependency checking, and batch-based concurrent file processing with configurable batch sizes and semaphore limits. Key algorithms include depth-first traversal for leaf identification, bottom-up assembly aggregating child summaries, and truncation detection handling where `None` returns from `KnowledgeBuilder` completely omit files from processing. The approach integrates caching through `FileAnalysisCache` for performance optimization and maintains detailed processing statistics throughout all operations.

######## External Dependencies & Integration Points

**→ Inbound:**
- `..models:IndexingConfig` - configuration and filtering logic for processing behavior
- `..models:DirectoryContext` - directory structure representation and processing state
- `..models:FileContext` - file metadata and processing context structures
- `..models:ProcessingStatus` - enumeration for processing state management
- `..models:ProcessingStats` - statistics tracking and performance metrics
- `..models:IndexingStatus` - overall indexing operation status representation
- `.change_detector:ChangeDetector` - timestamp-based change detection and incremental processing
- `.knowledge_builder:KnowledgeBuilder` - LLM-powered content summarization and analysis
- `.special_handlers:GitCloneHandler` - specialized handling for git-clone directories
- `.special_handlers:ProjectBaseHandler` - specialized handling for project-base scenarios
- `.orphaned_cleanup:OrphanedAnalysisCleanup` - maintenance operations for orphaned files
- `fastmcp:Context` - MCP context for progress reporting and user interaction
- `asyncio` (external library) - async programming patterns and concurrency control
- `pathlib` (external library) - cross-platform path operations and filesystem access
- `logging` (external library) - structured logging and error reporting

**← Outbound:**
- Knowledge base indexing workflows - primary orchestration for hierarchical processing
- MCP server operations - integration with Jesse Framework MCP server functionality
- CLI indexing commands - command-line interface for knowledge base operations
- Automated processing pipelines - scheduled or triggered indexing workflows

**⚡ System role and ecosystem integration:**
- **System Role**: Core orchestrator for hierarchical knowledge base indexing within Jesse Framework MCP, coordinating all phases of directory processing from discovery through content generation
- **Ecosystem Position**: Central component in the knowledge base indexing pipeline, integrating specialized handlers and builders while providing comprehensive workflow coordination
- **Integration Pattern**: Used by MCP server endpoints and CLI commands for knowledge base operations, with direct integration to specialized components for modular processing capabilities

######### Edge Cases & Error Handling

The system handles comprehensive error scenarios including filesystem access failures during directory traversal, individual file processing failures with configurable continuation modes, LLM truncation detection through `None` returns from `KnowledgeBuilder`, and change detection failures with conservative fallback to processing mode. Error handling includes permission errors during directory access with graceful skipping and logging, concurrent processing failures with semaphore-based recovery, and component initialization failures preventing construction errors. The implementation provides configurable error behavior through `continue_on_file_errors` setting, comprehensive error statistics tracking with `add_error` method, and detailed logging with `exc_info=True` for debugging support. Special handling includes truncation artifact prevention where truncated files are completely omitted from `DirectoryContext.file_contexts`, orphaned file cleanup error handling, and processing status management ensuring accurate completion tracking.

########## Internal Implementation Details

Internal mechanics include semaphore-based concurrency control with `_processing_semaphore` limiting concurrent operations, immutable context management creating new `DirectoryContext` instances for state updates, and comprehensive statistics tracking through `ProcessingStats` with timing, counts, and error collection. The implementation uses recursive context building with `_build_directory_context` creating nested structures, leaf-first processing order through `_process_directory_leaf_first` ensuring child completion, and batch processing with configurable `batch_size` for performance optimization. Key internal patterns include source root storage in `_source_root` for cache integration, processing status updates throughout workflow phases, and cleanup delegation to component-specific cleanup methods. The system maintains processing timing with `processing_start_time` and `processing_end_time`, handles component lifecycle through initialization and cleanup phases, and provides thread-safe status access through `current_status` property.

########### Code Usage Examples

Basic hierarchical indexing workflow initialization and execution pattern:

```python
# Initialize hierarchical indexer with configuration and execute complete indexing workflow
from jesse_framework_mcp.knowledge_bases.indexing.hierarchical_indexer import HierarchicalIndexer
from jesse_framework_mcp.knowledge_bases.models import IndexingConfig
from fastmcp import Context

# Create configuration and indexer
config = IndexingConfig(knowledge_output_directory=Path("./knowledge"))
indexer = HierarchicalIndexer(config)

# Execute hierarchical indexing with progress reporting
async with Context() as ctx:
    status = await indexer.index_hierarchy(Path("./source"), ctx)
    print(f"Indexing completed: {status.processing_stats.files_completed} files processed")
```

Advanced configuration with incremental processing and error handling:

```python
# Configure hierarchical indexer for incremental processing with custom error handling
config = IndexingConfig(
    indexing_mode=IndexingMode.INCREMENTAL,
    continue_on_file_errors=True,
    max_concurrent_operations=4,
    batch_size=10
)

indexer = HierarchicalIndexer(config)

# Execute with comprehensive error handling and status monitoring
try:
    status = await indexer.index_hierarchy(source_path, ctx)
    if status.overall_status == ProcessingStatus.COMPLETED:
        print(f"Success: {status.processing_stats.processing_duration:.2f}s")
    else:
        print(f"Partial completion: {len(status.processing_stats.errors)} errors")
finally:
    await indexer.cleanup()
```
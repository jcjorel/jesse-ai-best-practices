<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/hierarchical_indexer.py -->
<!-- Cached On: 2025-07-05T20:26:50.354928 -->
<!-- Source Modified: 2025-07-05T20:00:15.203738 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements the core orchestrator for hierarchical knowledge base indexing within the Jesse Framework MCP system, providing leaf-first processing strategy for building structured knowledge files throughout directory hierarchies. The system coordinates change detection, content building, and special handling to maintain `.knowledge/` directory structures using bottom-up assembly patterns. Key semantic entities include `HierarchicalIndexer` class, `index_hierarchy` method, `ChangeDetector` integration, `KnowledgeBuilder` delegation, `OrphanedAnalysisCleanup` component, `DirectoryContext` and `FileContext` models, `ProcessingStatus` enumeration, `IndexingConfig` configuration, `FastMCP` context integration, `asyncio` concurrency patterns, and `leaf-first` processing algorithms. The implementation enables developers to orchestrate comprehensive knowledge base generation with concurrent processing, progress reporting, and error recovery mechanisms across complex project directory structures.

##### Main Components

The file contains the `HierarchicalIndexer` class with core orchestration methods: `index_hierarchy()` for complete hierarchical processing coordination, `_discover_directory_structure()` for recursive directory traversal and context building, `_detect_changes()` and `_apply_comprehensive_change_detection()` for incremental processing optimization, `_process_directory_hierarchy()` and `_process_directory_leaf_first()` for leaf-first processing execution, `_process_directory_files()` and `_process_single_file()` for concurrent file processing, `_generate_directory_knowledge_file()` for directory summary generation, and utility methods `_get_all_directories()` for hierarchy analysis and `cleanup()` for resource management. Supporting components include initialization with `ChangeDetector`, `KnowledgeBuilder`, and `OrphanedAnalysisCleanup` dependencies, processing coordination through `asyncio.Semaphore`, and status tracking via `IndexingStatus` objects.

###### Architecture & Design

The architecture implements a modular orchestration pattern with clear separation of concerns between change detection, content building, and processing coordination. The design uses dependency injection for `ChangeDetector`, `KnowledgeBuilder`, and `OrphanedAnalysisCleanup` components, enabling testability and component modularity. The leaf-first processing strategy ensures child contexts complete before parent processing, eliminating parent-to-child dependencies and enabling bottom-up knowledge assembly. The system employs async-first architecture with `asyncio.Semaphore` for concurrency control, `FastMCP.Context` for progress reporting, and immutable context management through `DirectoryContext` and `FileContext` updates. Error handling follows defensive programming principles with configurable error recovery and comprehensive statistics tracking.

####### Implementation Approach

The implementation uses recursive directory traversal with `_build_directory_context()` creating hierarchical context structures, comprehensive change detection through `check_comprehensive_directory_change()` for incremental processing optimization, and leaf-first processing via depth-first traversal ensuring child completion before parent processing. Concurrent processing employs batch-based file processing with `asyncio.gather()` and semaphore-controlled concurrency limits. The system implements three processing modes: `incremental` with change detection, `full_kb_rebuild` with file analysis caching, and `full` nuclear rebuild bypassing all caches. Context immutability ensures proper state management through `DirectoryContext` and `FileContext` reconstruction rather than mutation. Processing statistics track files discovered, processed, completed, failed, and skipped with detailed error collection.

######## External Dependencies & Integration Points

**→ Inbound:**
- `..models.indexing_config:IndexingConfig` - configuration and filtering logic for processing behavior
- `..models.knowledge_context:DirectoryContext` - hierarchical directory context structures
- `..models.knowledge_context:FileContext` - individual file processing context
- `..models.knowledge_context:ProcessingStatus` - processing state enumeration
- `.change_detector:ChangeDetector` - comprehensive change detection and timestamp comparison
- `.knowledge_builder:KnowledgeBuilder` - LLM-powered content summarization and knowledge generation
- `.orphaned_cleanup:OrphanedAnalysisCleanup` - cleanup of orphaned analysis and knowledge files
- `fastmcp:Context` (external library) - progress reporting and logging interface
- `asyncio` (external library) - async programming patterns and concurrency control
- `pathlib.Path` (external library) - cross-platform path operations

**← Outbound:**
- `jesse_framework_mcp.main:main` - primary entry point for hierarchical indexing operations
- `jesse_framework_mcp.resources.knowledge:knowledge_resources` - MCP resource endpoints consuming generated knowledge
- `.knowledge/` directory structure - hierarchically organized knowledge files and analysis cache

**⚡ System role and ecosystem integration:**
- **System Role**: Central orchestrator coordinating all aspects of hierarchical knowledge base generation within the Jesse Framework MCP ecosystem
- **Ecosystem Position**: Core component that integrates change detection, content building, and cleanup operations for comprehensive knowledge base maintenance
- **Integration Pattern**: Used by MCP server initialization, CLI tools, and automated indexing workflows requiring structured knowledge generation across project hierarchies

######### Edge Cases & Error Handling

The system handles various error scenarios including inaccessible directories and files through `OSError` and `PermissionError` catching with continued processing, individual file processing failures with configurable `continue_on_file_errors` behavior, change detection failures with conservative fallback to processing mode, and truncated LLM responses through `None` return handling that completely omits files from processing. Memory constraints are managed through batch processing and semaphore-controlled concurrency limits. The system provides comprehensive error logging with `logger.error()` calls including stack traces, detailed error statistics collection through `ProcessingStats.add_error()`, and graceful degradation enabling partial processing completion when individual components fail.

########## Internal Implementation Details

Internal mechanisms include `_processing_semaphore` for concurrency control using `asyncio.Semaphore(config.max_concurrent_operations)`, `_current_status` tracking through `IndexingStatus` objects with real-time updates, and `_source_root` storage for knowledge file path calculations. The leaf-first algorithm uses recursive depth-first traversal with child processing completion before parent directory knowledge generation. Context immutability is maintained through `DirectoryContext` and `FileContext` reconstruction with updated fields rather than in-place mutation. Processing phases include discovery, cache preparation, orphaned cleanup, optional change detection, and leaf-first processing execution. Statistics tracking covers files discovered, processed, completed, failed, directories discovered and completed, with detailed error collection and processing timing measurements.

########### Code Usage Examples

Essential hierarchical indexing orchestration pattern for complete directory processing:

```python
# This pattern demonstrates complete hierarchical indexing with progress reporting and error handling
# The orchestrator coordinates all phases of knowledge base generation with comprehensive status tracking
indexer = HierarchicalIndexer(config)
status = await indexer.index_hierarchy(project_root, ctx)
print(f"Processing completed: {status.processing_stats.files_completed}/{status.processing_stats.total_files_discovered} files")
```

Leaf-first processing coordination ensuring proper dependency order:

```python
# This pattern shows how leaf-first processing ensures child contexts complete before parent processing
# The recursive approach eliminates parent-to-child dependencies enabling bottom-up knowledge assembly
async def _process_directory_leaf_first(self, directory_context, ctx):
    # Step 1: Process all subdirectories first (leaf-first)
    updated_subdirectory_contexts = []
    for subdir_context in directory_context.subdirectory_contexts:
        updated_subdir_context = await self._process_directory_leaf_first(subdir_context, ctx)
        updated_subdirectory_contexts.append(updated_subdir_context)
    
    # Step 2: Process files in current directory
    updated_directory_context = await self._process_directory_files(directory_context, ctx)
    
    # Step 3: Generate directory knowledge file from child summaries
    return await self._generate_directory_knowledge_file(complete_directory_context, ctx)
```

Concurrent file processing with semaphore control and error handling:

```python
# This pattern demonstrates concurrent file processing with proper resource management and error recovery
# Batch processing with semaphore control prevents resource exhaustion while maximizing throughput
async def _process_single_file(self, file_context, ctx):
    async with self._processing_semaphore:
        try:
            updated_context = await self.knowledge_builder.build_file_knowledge(
                file_context, ctx, source_root=self._source_root
            )
            # Handle truncation detection - None means omit file completely
            if updated_context is None:
                return None
            return updated_context
        except Exception as e:
            logger.error(f"File processing failed: {e}", exc_info=True)
            return FileContext(..., processing_status=ProcessingStatus.FAILED, error_message=str(e))
```
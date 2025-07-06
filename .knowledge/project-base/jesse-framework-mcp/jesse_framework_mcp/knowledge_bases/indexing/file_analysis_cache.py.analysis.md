<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/file_analysis_cache.py -->
<!-- Cached On: 2025-07-06T21:20:38.725458 -->
<!-- Source Modified: 2025-07-06T21:19:09.350007 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

The `FileAnalysisCache` class provides high-performance caching capabilities for individual LLM file analysis outputs within the Jesse Framework MCP knowledge building system. This cache manager eliminates redundant LLM API calls by storing and retrieving analysis results for unchanged source files, implementing timestamp-based staleness detection with `is_cache_fresh()` method returning detailed reasoning tuples. Key semantic entities include `FileAnalysisCache` class, `IndexingConfig` configuration model, `DirectoryContext` and `FileContext` data structures, `get_portable_path()` utility function, HTML comment metadata delimiters (`METADATA_START`, `METADATA_END`), project-base directory mirroring strategy, `.analysis.md` cache file suffix, `prepare_cache_structure()` method for concurrent operation safety, and `RebuildDecisionEngine` integration for staleness determination. The system provides clean metadata separation ensuring no cache artifacts contaminate final knowledge files through `_extract_analysis_content()` method, comprehensive error handling with graceful degradation on cache failures, and rich debugging capabilities with detailed timestamp comparisons and constituent staleness analysis.

##### Main Components

The module contains the primary `FileAnalysisCache` class with core caching operations including `get_cached_analysis()` for retrieval, `cache_analysis()` for storage, and `is_cache_fresh()` for staleness checking. Cache path management is handled by `get_cache_path()` following project-base directory structure mirroring. Knowledge file operations include `get_knowledge_file_path()` and `is_knowledge_file_stale()` for directory-level rebuild decisions. Metadata management components include `_create_metadata_header()` for rich cache tracking and `_extract_analysis_content()` for clean content extraction. Utility methods provide `get_constituent_staleness_info()` for detailed debugging analysis, `prepare_cache_structure()` for concurrent operation safety, `clear_cache()` for cache invalidation, and `get_cache_stats()` for monitoring. Helper methods include `_collect_all_files_recursive()` for directory traversal and `_is_handler_root_directory()` for consistent path generation across knowledge base handler types.

###### Architecture & Design

The architecture implements a cache-first processing strategy with clean metadata separation using HTML comment delimiters to prevent cache artifacts from contaminating final knowledge files. The design follows project-base directory structure mirroring as mandated by indexing business rules, creating `.analysis.md` cache files that mirror source file organization. Timestamp-based freshness checking uses direct filesystem timestamp comparison without tolerance for reliability and simplicity. The system employs upfront cache structure preparation through `prepare_cache_structure()` to eliminate race conditions during concurrent operations. Error handling follows graceful degradation principles where cache failures never break core knowledge building processes. The metadata system uses structured HTML comments with `CACHE_VERSION` for future compatibility and includes portable path references using `get_portable_path()` for cross-environment compatibility.

####### Implementation Approach

The implementation uses direct timestamp comparison between source files and cache files without tolerance, where cache is fresh if `cache_mtime >= source_mtime`. Cache files combine metadata headers with analysis content using clear HTML comment delimiters for reliable extraction. The system implements two-layer processing flow: source files trigger individual file reprocessing when changed, while knowledge files rebuild only when cached analyses or subdirectory knowledge files are newer. Directory structure preparation uses recursive `DirectoryContext` traversal to identify all files requiring cache directories, then creates unique cache directory sets atomically. Path calculation follows project-base indexing rules with relative path preservation and standardized `.analysis.md` suffix application. The staleness checking system specifically excludes cached analyses from directory rebuild decisions to prevent infinite rebuild loops, focusing only on source files and subdirectory knowledge files for directory-level staleness determination.

######## External Dependencies & Integration Points

**→ Inbound:**
- `..models.IndexingConfig` - Configuration model providing cache paths and timestamp tolerance settings
- `..models.DirectoryContext` - Hierarchical directory structure representation for cache preparation
- `..models.FileContext` - Individual file metadata with timestamps for staleness checking
- `...helpers.path_utils:get_portable_path` - Portable path generation using JESSE path variables
- `fastmcp.Context` - MCP framework context for progress reporting and user communication
- `pathlib.Path` (standard library) - Cross-platform path operations and file metadata access
- `datetime.datetime` (standard library) - Timestamp comparison and cache freshness determination
- `logging` (standard library) - Structured logging for cache operations and debugging

**← Outbound:**
- `knowledge_building/rebuild_decision_engine.py` - Consumes staleness checking methods for rebuild decisions
- `knowledge_building/knowledge_builder.py` - Uses cache retrieval and storage during file processing
- `indexing/hierarchical_indexer.py` - Integrates cache structure preparation in processing workflow
- `{PROJECT_ROOT}/jesse-framework-mcp/knowledge-base/project-base/` - Generated cache files with metadata headers

**⚡ System role and ecosystem integration:**
- **System Role**: Core performance optimization component in the Jesse Framework MCP knowledge building pipeline, serving as the primary cache layer between source file analysis and knowledge file generation
- **Ecosystem Position**: Central infrastructure component that significantly impacts system performance by reducing LLM API costs and processing time through intelligent caching
- **Integration Pattern**: Used by knowledge builders during file processing workflows, integrated with rebuild decision engines for staleness determination, and consumed by hierarchical indexers for structure preparation during batch operations

######### Edge Cases & Error Handling

The system handles missing cache files by returning `None` from `get_cached_analysis()` to trigger fresh LLM analysis. Filesystem access errors during timestamp comparison result in conservative staleness assumptions, treating files as requiring fresh analysis. Cache write failures are logged but never propagate to break core knowledge building processes. Path calculation errors fall back to flat structure in project-base directory to ensure cache operations continue. Metadata extraction failures return original content for backward compatibility with cache files lacking metadata delimiters. Concurrent access scenarios are handled through upfront directory structure preparation, with fallback to on-demand directory creation if preparation fails. The system treats cache freshness check failures conservatively by assuming staleness to trigger rebuilds rather than risk serving stale content. Directory structure preparation failures are logged but don't prevent processing, as individual cache operations fall back to on-demand directory creation.

########## Internal Implementation Details

Cache files use HTML comment metadata blocks with `CACHE_VERSION = "1.0"` for future compatibility and migration support. The metadata header includes portable source file paths using `get_portable_path()`, cache timestamp, source modification time, and cache version. Content extraction uses string operations to locate `METADATA_START` and `METADATA_END` delimiters, removing everything up to and including the end delimiter. Timestamp tolerance is calculated from `IndexingConfig.timestamp_tolerance_seconds` but currently unused in direct comparison logic. The `_is_handler_root_directory()` method implements identical logic to `KnowledgeBuilder` for consistent path generation across project-base, git-clones, and PDF-knowledge handlers. Cache statistics collection traverses the cache directory using `rglob("*.analysis.md")` pattern matching. The constituent staleness analysis builds comprehensive dictionaries with ISO timestamp formatting and detailed reasoning for debugging purposes. Directory structure preparation uses set operations to eliminate duplicate directory creation and batch processing for atomic structure creation.

########### Code Usage Examples

**Basic cache retrieval and storage pattern:**
```python
# Initialize cache with configuration
cache = FileAnalysisCache(config)

# Check for cached analysis
cached_content = await cache.get_cached_analysis(file_path, source_root)
if cached_content:
    # Use cached analysis directly
    analysis_result = cached_content
else:
    # Perform fresh LLM analysis
    analysis_result = await perform_llm_analysis(file_path)
    # Cache the result for future use
    await cache.cache_analysis(file_path, analysis_result, source_root)
```

**Cache structure preparation for concurrent operations:**
```python
# Prepare entire cache structure upfront to eliminate race conditions
await cache.prepare_cache_structure(root_context, source_root, ctx)

# Now safe to perform concurrent caching operations
tasks = [cache.cache_analysis(file_path, analysis, source_root) 
         for file_path, analysis in file_analyses]
await asyncio.gather(*tasks)
```

**Knowledge file staleness checking:**
```python
# Check if directory knowledge file needs rebuilding
is_stale, reason = cache.is_knowledge_file_stale(
    directory_path, source_root, file_contexts, subdirectory_paths
)
if is_stale:
    logger.info(f"Rebuilding knowledge file: {reason}")
    # Trigger knowledge file rebuild
```

**Detailed staleness analysis for debugging:**
```python
# Get comprehensive staleness information
staleness_info = await cache.get_constituent_staleness_info(
    directory_path, source_root, file_contexts, subdirectory_paths, ctx
)
# Access detailed timestamp comparisons and reasoning
for file_info in staleness_info['source_files']:
    print(f"File: {file_info['name']}, Modified: {file_info['mtime']}")
```
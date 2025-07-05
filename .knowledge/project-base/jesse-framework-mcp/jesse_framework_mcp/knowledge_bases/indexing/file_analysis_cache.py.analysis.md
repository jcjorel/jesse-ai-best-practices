<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/file_analysis_cache.py -->
<!-- Cached On: 2025-07-04T16:52:20.867617 -->
<!-- Source Modified: 2025-07-03T17:40:33.712319 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements a high-performance caching system for individual LLM analysis outputs in the Jesse Framework MCP knowledge building system, providing significant performance improvements by avoiding recomputation of file analyses when source files remain unchanged. The `FileAnalysisCache` class manages timestamp-based freshness checking, clean metadata separation, and project-base directory structure mirroring using `IndexingConfig`, `DirectoryContext`, `FileContext`, `get_portable_path()`, HTML comment delimiters (`METADATA_START`, `METADATA_END`), and `.analysis.md` cache file suffixes. Key semantic entities include `datetime` timestamp comparison with configurable tolerance, `pathlib.Path` operations, comprehensive staleness detection through `is_knowledge_file_stale()`, constituent dependency checking, and cache structure preparation via `prepare_cache_structure()` for concurrent operation safety.

##### Main Components

The file contains the `FileAnalysisCache` class with core methods including `get_cached_analysis()` for retrieving clean cached content, `cache_analysis()` for storing analysis results with metadata, `is_cache_fresh()` for timestamp-based freshness validation, `get_cache_path()` for project-base path calculation, `is_knowledge_file_stale()` for comprehensive directory knowledge file staleness checking, `get_constituent_staleness_info()` for detailed debugging analysis, `prepare_cache_structure()` for upfront directory creation, and `clear_cache()` for cache invalidation. Supporting utility methods include `_extract_analysis_content()` for metadata removal, `_create_metadata_header()` for portable path metadata generation, `_collect_all_files_recursive()` for hierarchy traversal, and `get_cache_stats()` for monitoring.

###### Architecture & Design

The architecture implements a cache-first processing strategy with clean metadata separation ensuring no cache artifacts contaminate final knowledge files. The design follows project-base indexing business rules with mirror directory structure organization and standardized `.analysis.md` file naming conventions. HTML comment-based metadata blocks enable reliable content extraction while maintaining backward compatibility. The system uses immutable timestamp-based freshness checking with configurable tolerance for filesystem precision handling. Upfront cache structure preparation eliminates race conditions during concurrent operations through pre-created directory hierarchies.

####### Implementation Approach

The implementation uses timestamp comparison with `datetime.fromtimestamp()` and configurable tolerance through `timedelta` for reliable freshness detection. Cache path calculation follows project-base subdirectory mirroring using `Path.relative_to()` and structured path reconstruction. Metadata management uses HTML comment delimiters for clean content extraction without markdown parsing conflicts. Comprehensive staleness checking evaluates cached analyses, subdirectory knowledge files, and source file timestamps against knowledge file modification times. Concurrent safety is achieved through upfront directory structure creation and atomic file operations with graceful error handling.

######## External Dependencies & Integration Points

**→ Inbound:**
- `..models.indexing_config:IndexingConfig` - Cache configuration and knowledge output directory paths
- `..models.knowledge_context:DirectoryContext` - Directory structure context for cache preparation
- `..models.knowledge_context:FileContext` - Individual file metadata and processing status
- `...helpers.path_utils:get_portable_path` - Portable path generation for cross-environment compatibility
- `fastmcp:Context` - Progress reporting during cache structure preparation
- `pathlib` (external library) - Cross-platform path operations and file metadata access
- `datetime` (external library) - Timestamp comparison and cache freshness determination
- `logging` (external library) - Structured logging for cache operations and debugging

**← Outbound:**
- `knowledge_builder.py:KnowledgeBuilder` - Cache retrieval and storage during file analysis
- `hierarchical_indexer.py:HierarchicalIndexer` - Cache structure preparation and staleness checking
- `change_detector.py:ChangeDetector` - Knowledge file staleness evaluation for incremental processing
- `generated/.knowledge/project-base/` - Cache file storage following mirror directory structure

**⚡ System role and ecosystem integration:**
- **System Role**: Critical performance optimization component providing LLM analysis caching to eliminate redundant processing and reduce API costs in the knowledge building pipeline
- **Ecosystem Position**: Core infrastructure component supporting the hierarchical indexing system with cache-first processing strategy and comprehensive staleness detection
- **Integration Pattern**: Used by knowledge builders for cache retrieval/storage, hierarchical indexers for structure preparation, and change detectors for staleness evaluation with concurrent operation safety

######### Edge Cases & Error Handling

The system handles missing cache files by returning `None` to trigger fresh LLM analysis rather than failing operations. Filesystem access errors during timestamp comparison are treated conservatively as requiring fresh analysis to prevent stale content usage. Cache extraction failures fall back to original content for backward compatibility with cache files lacking metadata delimiters. Concurrent directory creation race conditions are eliminated through upfront structure preparation with fallback to on-demand creation. Portable path conversion failures use absolute paths as fallback in metadata headers. Cache write failures are logged but don't break core processing through graceful degradation patterns.

########## Internal Implementation Details

The `METADATA_START` and `METADATA_END` HTML comment delimiters use `<!-- CACHE_METADATA_START -->` and `<!-- CACHE_METADATA_END -->` for reliable content extraction without markdown conflicts. Cache versioning uses `CACHE_VERSION = "1.0"` for future compatibility and migration support. Timestamp tolerance is calculated as `timedelta(seconds=config.timestamp_tolerance_seconds)` for consistent freshness checking. The `get_cache_path()` method applies project-base subdirectory structure with `.analysis.md` suffix following `Path("project-base") / relative_path.parent / f"{file_path.name}.analysis.md"` pattern. Staleness checking uses `cache_mtime > knowledge_mtime + self.timestamp_tolerance` comparison logic for all constituent dependencies.

########### Code Usage Examples

**Basic cache retrieval with freshness checking demonstrates how to check for cached analysis content before triggering expensive LLM operations. This pattern provides immediate performance benefits by avoiding redundant processing when files haven't changed.**
```python
cache = FileAnalysisCache(config)
cached_content = await cache.get_cached_analysis(file_path, source_root)
if cached_content:
    print(f"Cache hit: {len(cached_content)} characters")
else:
    print("Cache miss - fresh analysis required")
```

**Caching analysis results with metadata shows how to store LLM analysis outputs with portable path metadata for future retrieval. This enables persistent caching across different environments and working directories.**
```python
analysis_result = "# File Analysis\nThis file implements..."
await cache.cache_analysis(file_path, analysis_result, source_root)
print(f"Cached analysis for {file_path.name}")
```

**Comprehensive staleness checking for directory knowledge files demonstrates how to evaluate whether knowledge files need rebuilding based on constituent dependencies. This enables efficient incremental processing by only rebuilding when necessary.**
```python
is_stale, reason = cache.is_knowledge_file_stale(
    directory_path, source_root, file_contexts, subdirectory_paths
)
if is_stale:
    print(f"Knowledge file needs rebuild: {reason}")
```

**Upfront cache structure preparation for concurrent safety shows how to pre-create directory hierarchies before concurrent operations begin. This eliminates race conditions and ensures consistent cache state during parallel processing.**
```python
await cache.prepare_cache_structure(root_context, source_root, ctx)
print("Cache directories pre-created for safe concurrent operations")
```
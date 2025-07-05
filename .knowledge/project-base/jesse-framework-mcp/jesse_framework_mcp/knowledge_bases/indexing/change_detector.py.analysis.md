<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/change_detector.py -->
<!-- Cached On: 2025-07-04T16:54:15.603452 -->
<!-- Source Modified: 2025-07-03T17:21:13.448586 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This module implements timestamp-based change detection for incremental hierarchical indexing in the Jesse Framework MCP's knowledge base system. It provides comprehensive change identification by comparing source file modification times with existing knowledge file timestamps to minimize unnecessary LLM processing and enable efficient incremental updates. The system offers hierarchical dependency tracking, ensuring parent directory updates when children change, comprehensive constituent dependency checking through `FileAnalysisCache` integration, and detailed change analysis for debugging optimization. Key semantic entities include `ChangeDetector` class, `detect_changes()` method, `check_comprehensive_directory_change()` method, `ChangeInfo` model, `ChangeType` enum, `DirectoryContext` and `FileContext` models, `IndexingConfig` configuration, `FileAnalysisCache` integration, `timestamp_tolerance` configuration, and `datetime` timestamp comparison with configurable tolerance handling filesystem precision variations.

##### Main Components

The module contains the `ChangeDetector` class as the primary component with initialization accepting `IndexingConfig` for timestamp tolerance configuration. Core detection methods include `detect_changes()` for comprehensive hierarchy traversal, `_detect_directory_changes()` for single directory processing, `_check_file_change()` with enhanced heuristic-based detection, `_check_directory_change()` for directory-level timestamp comparison, and `_detect_dependency_changes()` for hierarchical change propagation. Advanced analysis methods include `check_comprehensive_directory_change()` using `FileAnalysisCache` for complete staleness checking, `get_detailed_change_analysis()` providing debugging information, and `get_stale_knowledge_files()` for orphaned knowledge file detection. Utility methods include `is_file_newer_than_knowledge()` for binary timestamp comparison, `_get_parent_directories()` for hierarchical path collection, and `_get_directory_knowledge_file_path()` for consistent knowledge file location determination.

###### Architecture & Design

The architecture implements a hierarchical change detection pattern with breadth-first directory traversal and recursive subdirectory processing. The design uses timestamp-based comparison with configurable tolerance to handle filesystem precision variations, defensive programming patterns for graceful handling of missing or corrupted knowledge files, and comprehensive dependency tracking ensuring parent updates when children change. The system integrates with `FileAnalysisCache` for sophisticated constituent dependency checking including source files, cached analyses, and subdirectory knowledge files. Error handling follows a graceful degradation approach where individual failures don't break the entire change detection process, and conservative fallback behavior assumes changes when detection fails to ensure processing completeness.

####### Implementation Approach

The implementation uses async/await patterns throughout for non-blocking change detection operations and efficient I/O handling. Change detection employs intelligent heuristics based on file modification recency rather than the MVP "process everything" approach, with files modified within 24 hours flagged for processing and very recent modifications (within 1 hour) automatically marked as changed. The system maintains processed path tracking using `Set[Path]` to avoid duplicate change detection and implements hierarchical dependency propagation by collecting parent directories from changed items up to the root. Timestamp comparison uses `datetime.fromtimestamp()` with configurable `timedelta` tolerance, and comprehensive staleness checking leverages `FileAnalysisCache.is_knowledge_file_stale()` for complete constituent dependency analysis.

######## External Dependencies & Integration Points

**→ Inbound:**
- `..models.indexing_config:IndexingConfig` - configuration and timestamp tolerance settings
- `..models.knowledge_context:DirectoryContext` - directory structure representation with file contexts
- `..models.knowledge_context:FileContext` - file metadata and processing status tracking
- `..models.knowledge_context:ChangeInfo` - change information structure for processing coordination
- `..models.knowledge_context:ChangeType` - enumeration of change types (NEW, MODIFIED, DELETED)
- `.file_analysis_cache:FileAnalysisCache` - sophisticated constituent dependency checking and staleness detection
- `fastmcp:Context` - logging and debugging context for change detection operations
- `pathlib` (external library) - cross-platform path operations and file metadata access
- `datetime` (external library) - timestamp comparison and manipulation with tolerance handling
- `logging` (external library) - structured logging for change detection operations

**← Outbound:**
- `knowledge_bases/indexing/hierarchical_indexer.py:HierarchicalIndexer` - consumes change detection results for incremental processing
- `knowledge_bases/builders/knowledge_builder.py` - uses change information for targeted knowledge file updates
- Processing coordination systems that consume `ChangeInfo` objects for incremental update strategies

**⚡ System role and ecosystem integration:**
- **System Role**: Core change detection engine enabling efficient incremental processing in the hierarchical knowledge indexing system
- **Ecosystem Position**: Central component bridging file system monitoring with knowledge base processing, essential for performance optimization
- **Integration Pattern**: Used by `HierarchicalIndexer` for incremental processing decisions, integrated with `FileAnalysisCache` for comprehensive staleness checking, and consumed by knowledge builders for targeted update strategies

######### Edge Cases & Error Handling

The system handles missing knowledge files by treating them as new content requiring processing, with `_check_directory_change()` returning `ChangeType.NEW` when knowledge files don't exist. Timestamp access failures are handled gracefully with conservative fallback behavior assuming changes are required when comparison fails. Filesystem precision variations are accommodated through configurable `timestamp_tolerance` using `timedelta` objects for reliable comparison. Individual file or directory change detection failures are logged as warnings but don't break the overall change detection process, ensuring comprehensive coverage even with partial failures. Race condition scenarios during concurrent file modifications are handled through defensive timestamp comparison and conservative change assumptions. The system provides detailed error logging with specific file paths and error messages for debugging filesystem access issues.

########## Internal Implementation Details

The change detection process maintains a `processed_paths` set to track already-processed items and prevent duplicate analysis during recursive traversal. Knowledge file path generation follows the convention of placing `{dirname}_kb.md` files in parent directories for consistent hierarchical organization. Timestamp tolerance is implemented using `timedelta(seconds=config.timestamp_tolerance_seconds)` for precise comparison control. The comprehensive directory change detection integrates with `FileAnalysisCache.is_knowledge_file_stale()` which checks source files, cached analyses, and subdirectory knowledge files for complete staleness determination. Hierarchical dependency tracking uses `_get_parent_directories()` to collect all parent paths from changed items to the root, ensuring complete change propagation. The system implements intelligent file change heuristics with 24-hour and 1-hour modification windows for performance optimization while maintaining processing completeness.

########### Code Usage Examples

**Basic change detection initialization and execution:**
```python
# Initialize change detector with configuration and execute comprehensive change detection
config = IndexingConfig(timestamp_tolerance_seconds=2)
detector = ChangeDetector(config)
changes = await detector.detect_changes(root_context, ctx)
```

**Comprehensive directory change checking with FileAnalysisCache integration:**
```python
# Check if directory needs rebuilding using comprehensive constituent dependency analysis
change_info = await detector.check_comprehensive_directory_change(
    directory_context, source_root, ctx
)
if change_info:
    print(f"Directory needs rebuild: {change_info.change_type}")
```

**Detailed change analysis for debugging and optimization:**
```python
# Get detailed information about why directory requires rebuilding
analysis = await detector.get_detailed_change_analysis(
    directory_context, source_root, ctx
)
print(f"Staleness reason: {analysis.get('staleness_reason')}")
```

**Simple file timestamp comparison for binary change detection:**
```python
# Check if source file is newer than corresponding knowledge file
needs_update = detector.is_file_newer_than_knowledge(
    source_file_path, knowledge_file_path
)
```
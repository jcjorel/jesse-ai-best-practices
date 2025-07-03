<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/change_detector.py -->
<!-- Cached On: 2025-07-04T00:49:23.126018 -->
<!-- Source Modified: 2025-07-03T17:21:13.448586 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements a timestamp-based change detection system for the JESSE Framework MCP knowledge base system, providing incremental processing capabilities by comparing source file modification times with existing knowledge file timestamps to identify content requiring updates. The system delivers efficient change identification to minimize unnecessary LLM processing, comprehensive change tracking supporting different change types and scenarios, and hierarchical dependency tracking ensuring parent updates when children change. Key semantic entities include `ChangeDetector` class for change orchestration, `IndexingConfig` for configuration and timestamp tolerance, `DirectoryContext` and `FileContext` for hierarchy representation, `ChangeInfo` and `ChangeType` for change information structures, `FileAnalysisCache` integration for comprehensive constituent dependency checking, `check_comprehensive_directory_change()` method for enhanced staleness detection, `get_detailed_change_analysis()` method for debugging information, and timestamp-based comparison methods evidenced by `detect_changes()`, `is_file_newer_than_knowledge()`, and hierarchical dependency propagation capabilities.

##### Main Components

Contains `ChangeDetector` class as the primary change detection orchestrator with initialization, detection, and analysis methods. Implements core detection methods including `detect_changes()` for comprehensive hierarchy analysis, `_detect_directory_changes()` for recursive directory processing, `_check_file_change()` for enhanced file-level detection, `_check_directory_change()` for directory-level analysis, and `_detect_dependency_changes()` for hierarchical propagation. Provides enhanced methods including `check_comprehensive_directory_change()` for FileAnalysisCache integration, `get_detailed_change_analysis()` for debugging support, and utility methods for timestamp comparison and knowledge file path resolution. Integrates with `FileAnalysisCache` for sophisticated constituent dependency checking including source files, cached analyses, and subdirectory knowledge files.

###### Architecture & Design

Implements timestamp-based change detection architecture with configurable tolerance for filesystem precision variations and comprehensive hierarchical dependency tracking. Uses breadth-first change detection traversing directory hierarchy efficiently while tracking processed paths to avoid duplicate analysis. Employs defensive programming patterns handling missing knowledge files gracefully and treating them as requiring processing. Integrates `FileAnalysisCache` for enhanced staleness checking providing comprehensive constituent dependency analysis beyond simple timestamp comparison. Follows separation of concerns with distinct methods for file-level, directory-level, and dependency change detection enabling targeted processing strategies.

####### Implementation Approach

Uses filesystem timestamp comparison with configurable tolerance through `timedelta` objects accommodating filesystem precision variations across different platforms. Implements intelligent heuristics for file change detection using modification time patterns and recency analysis rather than processing all files indiscriminately. Employs comprehensive constituent dependency checking through `FileAnalysisCache.is_knowledge_file_stale()` method evaluating source files, cached analyses, and subdirectory knowledge files. Uses hierarchical dependency propagation collecting parent directories requiring updates when child content changes. Implements breadth-first traversal with processed path tracking preventing duplicate change detection operations.

######## Code Usage Examples

Initialize the change detector with configuration parameters for timestamp tolerance and processing behavior. This establishes the foundation for incremental change detection operations:

```python
change_detector = ChangeDetector(config)
detected_changes = await change_detector.detect_changes(root_context, ctx)
```

Perform comprehensive directory change detection using FileAnalysisCache integration for sophisticated staleness checking. This demonstrates enhanced change detection with constituent dependency analysis:

```python
change_info = await change_detector.check_comprehensive_directory_change(
    directory_context, source_root, ctx
)
if change_info:
    # Directory needs processing due to constituent changes
    process_directory(directory_context)
```

Obtain detailed change analysis for debugging and optimization purposes using comprehensive staleness information. This provides detailed constituent analysis for troubleshooting change detection decisions:

```python
analysis = await change_detector.get_detailed_change_analysis(
    directory_context, source_root, ctx
)
print(f"Staleness reason: {analysis['staleness_reason']}")
```

######### External Dependencies & Integration Points

**→ Inbound:**

- `..models.indexing_config:IndexingConfig` - configuration and timestamp tolerance parameters
- `..models.knowledge_context:DirectoryContext` - directory context structures and processing state
- `..models.knowledge_context:FileContext` - file context structures and metadata
- `..models.knowledge_context:ChangeInfo` - change information structures for processing coordination
- `..models.knowledge_context:ChangeType` - enumeration for different change types and scenarios
- `.file_analysis_cache:FileAnalysisCache` - comprehensive constituent dependency checking and staleness analysis
- `fastmcp:Context` (external library) - progress reporting and user interaction
- `pathlib.Path` (standard library) - cross-platform path operations and file metadata
- `datetime.datetime, timedelta` (standard library) - timestamp comparison and manipulation
- `logging` (standard library) - structured logging for change detection operations

**← Outbound:**

- `hierarchical_indexer.HierarchicalIndexer` - consumes change detection for incremental processing coordination
- `knowledge_builder.KnowledgeBuilder` - uses change information for targeted content generation
- Processing workflows - systems that coordinate incremental updates based on change detection results
- Monitoring systems - tools that track change detection performance and statistics

**⚡ Integration:**

- Protocol: Direct Python imports and method calls with structured change information objects
- Interface: Class methods returning ChangeInfo objects and boolean change indicators
- Coupling: Tight coupling with models and FileAnalysisCache, loose coupling with processing systems

########## Edge Cases & Error Handling

Handles missing knowledge files gracefully by treating them as requiring processing rather than failing change detection operations. Addresses timestamp comparison failures through comprehensive error catching with conservative fallback behavior assuming changes when comparison fails. Manages filesystem access errors during directory traversal through individual item error handling preventing single access failures from breaking entire change detection. Handles FileAnalysisCache integration failures with fallback to basic timestamp comparison ensuring change detection continues despite cache issues. Addresses concurrent access scenarios through atomic timestamp reading and error recovery ensuring consistent change detection under concurrent operations.

########### Internal Implementation Details

Uses `timedelta` objects for timestamp tolerance configuration enabling precise filesystem precision accommodation across different platforms and storage systems. Implements processed path tracking through `Set[Path]` objects preventing duplicate change detection operations during recursive directory traversal. Uses conservative fallback strategies throughout error handling preferring to process content when change detection fails rather than missing required updates. Maintains hierarchical dependency tracking through parent directory collection and change propagation ensuring comprehensive incremental processing coverage. Integrates with `FileAnalysisCache.is_knowledge_file_stale()` method for sophisticated constituent dependency checking including source files, cached analyses, and subdirectory knowledge files providing comprehensive staleness analysis beyond simple timestamp comparison.
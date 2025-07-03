<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/knowledge_builder.py -->
<!-- Cached On: 2025-07-04T00:49:18.961411 -->
<!-- Source Modified: 2025-07-03T16:29:21.030720 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements a timestamp-based change detection system for the JESSE Framework MCP knowledge base system, providing incremental processing capabilities by comparing source file modification times with existing knowledge file timestamps to identify content requiring updates. The system delivers efficient change identification minimizing unnecessary LLM processing, comprehensive change tracking supporting different change types and scenarios, and hierarchical dependency tracking ensuring parent updates when children change. Key semantic entities include `ChangeDetector` class for change orchestration, `IndexingConfig` for timestamp tolerance configuration, `DirectoryContext` and `FileContext` for hierarchy representation, `ChangeInfo` and `ChangeType` for change tracking, `FileAnalysisCache` integration for comprehensive staleness checking, `detect_changes()` method for hierarchy traversal, `check_comprehensive_directory_change()` method for constituent dependency checking, and timestamp-based comparison methods evidenced by `is_file_newer_than_knowledge()`, `_check_file_change()`, and hierarchical dependency propagation through `_detect_dependency_changes()`.

##### Main Components

Contains `ChangeDetector` class as the primary change detection orchestrator with initialization, detection, and analysis methods. Implements core detection methods including `detect_changes()` for comprehensive hierarchy analysis, `_detect_directory_changes()` for recursive directory processing, `_check_file_change()` for individual file analysis, and `_check_directory_change()` for directory-level updates. Provides enhanced detection capabilities through `check_comprehensive_directory_change()` using `FileAnalysisCache` integration and `get_detailed_change_analysis()` for debugging support. Includes utility methods for hierarchical dependency tracking through `_detect_dependency_changes()`, parent directory collection via `_get_parent_directories()`, and knowledge file path resolution through `_get_directory_knowledge_file_path()`.

###### Architecture & Design

Implements timestamp-based change detection architecture with configurable tolerance for filesystem precision variations through `timedelta` objects. Uses hierarchical dependency tracking ensuring parent directory updates when child files or subdirectories change through bottom-up change propagation. Employs comprehensive constituent dependency checking through `FileAnalysisCache` integration evaluating source files, cached analyses, and subdirectory knowledge files. Integrates defensive programming patterns handling missing knowledge files gracefully by treating them as requiring updates. Follows breadth-first traversal patterns for efficient directory hierarchy processing while maintaining processed path tracking to avoid duplicate analysis.

####### Implementation Approach

Uses intelligent heuristic-based file change detection replacing MVP "process everything" approach with modification time patterns and recency analysis. Implements comprehensive staleness checking through `FileAnalysisCache.is_knowledge_file_stale()` method evaluating all constituent dependencies including source files, cached analyses, and subdirectory knowledge files. Employs recursive directory traversal with processed path tracking preventing duplicate change detection while ensuring complete hierarchy coverage. Uses conservative fallback strategies treating filesystem errors and access failures as requiring processing to ensure completeness. Implements hierarchical dependency propagation collecting parent directories from changed items and creating dependency change information for comprehensive incremental processing.

######## Code Usage Examples

Initialize the change detector with timestamp tolerance configuration for reliable incremental processing. This establishes the foundation for timestamp-based change detection operations:

```python
from jesse_framework_mcp.knowledge_bases.indexing.change_detector import ChangeDetector
from jesse_framework_mcp.knowledge_bases.models import IndexingConfig

config = IndexingConfig(timestamp_tolerance_seconds=2)
change_detector = ChangeDetector(config)
```

Detect changes in directory hierarchy for comprehensive incremental processing coordination. This demonstrates the primary change detection workflow with hierarchical dependency tracking:

```python
detected_changes = await change_detector.detect_changes(root_context, ctx)
for change in detected_changes:
    print(f"Change detected: {change.path} - {change.change_type.value}")
    if change.is_content_change:
        # Process this change
        pass
```

Perform comprehensive directory change checking with constituent dependency analysis. This shows enhanced change detection using FileAnalysisCache integration for sophisticated staleness evaluation:

```python
change_info = await change_detector.check_comprehensive_directory_change(
    directory_context, source_root, ctx
)
if change_info:
    print(f"Directory needs rebuild: {change_info.path}")
    detailed_analysis = await change_detector.get_detailed_change_analysis(
        directory_context, source_root, ctx
    )
```

######### External Dependencies & Integration Points

**→ Inbound:**

- `..models.indexing_config:IndexingConfig` - configuration and timestamp tolerance parameters
- `..models.knowledge_context:DirectoryContext` - directory context structures and processing state
- `..models.knowledge_context:FileContext` - file context structures and metadata
- `..models.knowledge_context:ChangeInfo` - change information tracking and reporting
- `..models.knowledge_context:ChangeType` - enumeration for change type classification
- `.file_analysis_cache:FileAnalysisCache` - comprehensive staleness checking and constituent dependency analysis
- `fastmcp:Context` (external library) - progress reporting and user interaction
- `pathlib:Path` (standard library) - cross-platform path operations and file metadata
- `datetime:datetime, timedelta` (standard library) - timestamp comparison and manipulation
- `logging` (standard library) - structured logging for change detection operations

**← Outbound:**

- `hierarchical_indexer.HierarchicalIndexer` - consumes change detection for incremental processing coordination
- `knowledge_builder.KnowledgeBuilder` - uses change information for targeted content generation
- Incremental processing workflows - systems that coordinate updates based on detected changes
- Knowledge base maintenance systems - tools that use change detection for cleanup and optimization

**⚡ Integration:**

- Protocol: Direct Python imports and async method calls with structured change information
- Interface: Class methods returning ChangeInfo objects and boolean change indicators
- Coupling: Tight coupling with models and FileAnalysisCache, loose coupling with processing systems

########## Edge Cases & Error Handling

Handles missing knowledge files gracefully by treating them as new content requiring processing through conservative change detection logic. Addresses filesystem timestamp access failures through comprehensive error catching with fallback to assuming changes are required for reliability. Manages timestamp precision variations through configurable tolerance using `timedelta` objects preventing false positives from filesystem precision differences. Handles corrupted or inaccessible knowledge files through defensive programming returning change requirements when comparison fails. Addresses concurrent access scenarios through individual file error handling preventing single file access failures from breaking entire change detection operations.

########### Internal Implementation Details

Uses `timedelta` objects with configurable seconds for timestamp tolerance handling filesystem precision variations across different platforms. Implements processed path tracking through `Set[Path]` collections preventing duplicate change detection during recursive directory traversal. Maintains change information through `ChangeInfo` objects containing path, change type, and timestamp details for comprehensive change tracking. Uses conservative fallback logic throughout error handling ensuring change detection errs on the side of processing rather than missing updates. Implements hierarchical dependency collection through parent directory traversal from changed items to root ensuring comprehensive dependency change propagation for bottom-up knowledge file generation.
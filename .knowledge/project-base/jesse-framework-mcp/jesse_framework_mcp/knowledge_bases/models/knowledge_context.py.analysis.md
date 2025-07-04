<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/models/knowledge_context.py -->
<!-- Cached On: 2025-07-04T08:18:00.825353 -->
<!-- Source Modified: 2025-07-02T13:39:29.712510 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This module provides runtime context data models for the Knowledge Bases Hierarchical Indexing System, enabling comprehensive tracking of processing state, file analysis results, change detection, and operation statistics throughout the hierarchical indexing workflow. The module defines immutable context structures for thread-safe operations with complete serialization support for debugging and persistence. Key semantic entities include `ProcessingStatus` enum, `ChangeType` enum, `FileContext` dataclass, `DirectoryContext` dataclass, `ChangeInfo` dataclass, `ProcessingStats` dataclass, and `IndexingStatus` dataclass. The module integrates with `dataclasses`, `datetime`, `pathlib`, `typing`, and `enum` standard library modules to provide type-safe models supporting async operations and bottom-up hierarchical context assembly without parent-to-child dependencies.

##### Main Components

The module contains five primary dataclasses and two enums: `ProcessingStatus` enum defining processing states (`PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`, `SKIPPED`), `ChangeType` enum for change detection (`NEW`, `MODIFIED`, `DELETED`, `MOVED`), `FileContext` frozen dataclass tracking individual file processing state and metadata, `DirectoryContext` frozen dataclass managing directory-level processing with child contexts, `ChangeInfo` frozen dataclass capturing change detection information, `ProcessingStats` mutable dataclass for operation statistics tracking, and `IndexingStatus` mutable dataclass providing overall indexing operation status and coordination.

###### Architecture & Design

The architecture follows an immutable context pattern using frozen dataclasses for `FileContext`, `DirectoryContext`, and `ChangeInfo` to ensure thread-safe operations during concurrent processing. Mutable dataclasses `ProcessingStats` and `IndexingStatus` enable real-time updates for statistics and status tracking. The design implements clear separation between processing state and configuration, with comprehensive tracking capabilities supporting async operations. Bottom-up hierarchical context assembly allows child contexts to be processed independently before parent directory processing, eliminating parent-to-child dependencies and enabling efficient parallel processing workflows.

####### Implementation Approach

The implementation uses frozen dataclasses with computed properties for immutable context tracking, while mutable dataclasses handle dynamic statistics and status updates. Timestamp-based change detection provides reliable incremental processing capabilities through `ChangeInfo` with `datetime` fields. Hierarchical statistics calculation uses recursive property methods in `DirectoryContext` for accurate progress reporting across directory trees. Processing duration calculation employs `datetime` arithmetic for performance metrics, while completion tracking uses boolean properties and status enums for workflow coordination. Error tracking maintains chronological error lists with detailed failure information for debugging and recovery operations.

######## Code Usage Examples

Creating a file context for processing tracking demonstrates basic instantiation patterns. This example shows how to initialize file metadata and processing state for workflow coordination.

```python
file_context = FileContext(
    file_path=Path("src/module.py"),
    file_size=1024,
    last_modified=datetime.now(),
    processing_status=ProcessingStatus.PENDING
)
```

Building directory context with child files and calculating progress enables hierarchical processing coordination. This pattern supports bottom-up context assembly and progress tracking across directory trees.

```python
dir_context = DirectoryContext(
    directory_path=Path("src/"),
    file_contexts=[file_context1, file_context2],
    subdirectory_contexts=[subdir_context]
)
completion_rate = dir_context.completion_percentage
is_ready = dir_context.is_ready_for_summary
```

Tracking processing statistics and errors provides comprehensive operation monitoring capabilities. This approach enables real-time progress reporting and detailed failure analysis throughout indexing operations.

```python
stats = ProcessingStats()
stats.total_files_discovered = 100
stats.files_completed = 75
stats.add_error("Failed to process file: permission denied")
error_rate = stats.error_rate
```

######### External Dependencies & Integration Points

**→ Inbound:** [what this file depends on]
- `dataclasses` (external library) - frozen and mutable dataclass definitions
- `datetime` (external library) - timestamp handling and duration calculations
- `pathlib` (external library) - Path object operations and validation
- `typing` (external library) - type annotations and Optional types
- `enum` (external library) - string-based enum definitions

**← Outbound:** [what depends on this file]
- `jesse_framework_mcp/knowledge_bases/indexer.py:HierarchicalIndexer` - uses context models for processing workflow
- `jesse_framework_mcp/tools/knowledge_bases.py:FastMCP` - consumes IndexingStatus for progress reporting
- `jesse_framework_mcp/knowledge_bases/change_detector.py` - produces ChangeInfo instances
- `.knowledge/` - serialized context data for debugging and persistence

**⚡ Integration:** [how connections work]
- Protocol: Direct-import with dataclass instantiation
- Interface: Dataclass constructors, property methods, and serialization methods
- Coupling: tight with indexer components, loose with external systems via serialization

########## Edge Cases & Error Handling

Empty directory handling returns 0.0 for completion percentages and total file counts to prevent division by zero errors. Missing timestamp scenarios in processing duration calculations return `None` values rather than raising exceptions. Incomplete processing state checks use multiple condition validation in `is_completed` and `is_ready_for_summary` properties to ensure data consistency. Error message accumulation in `ProcessingStats.add_error()` maintains chronological order without size limits, requiring external management for memory constraints. Serialization edge cases handle `None` datetime values with explicit checking before ISO format conversion in `to_dict()` methods.

########### Internal Implementation Details

Frozen dataclass implementation uses `object.__setattr__()` for post-initialization modifications when needed, though this pattern is avoided in the current implementation. Property method calculations use generator expressions for memory efficiency with large directory trees in `total_files` and `completed_files`. Status enum string values enable direct serialization compatibility without additional conversion logic. Processing statistics maintain separate counters for discovered, processed, completed, failed, and skipped items to support detailed progress analysis. Context assembly relies on list-based child storage maintaining processing order and enabling efficient iteration for statistics calculation and readiness checking.
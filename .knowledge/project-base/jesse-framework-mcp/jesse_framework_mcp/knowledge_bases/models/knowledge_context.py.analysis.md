<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/models/knowledge_context.py -->
<!-- Cached On: 2025-07-06T13:55:59.524181 -->
<!-- Source Modified: 2025-07-06T13:53:55.909657 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This module provides runtime context data models for the Jesse Framework MCP's Knowledge Bases Hierarchical Indexing System, enabling comprehensive tracking of directory processing, file analysis, change detection, and indexing operation status throughout the hierarchical processing workflow. The module delivers immutable context structures through `FileContext` and `DirectoryContext` classes that support thread-safe operations, comprehensive processing statistics via `ProcessingStats`, and overall operation coordination through `IndexingStatus`. Key semantic entities include `ProcessingStatus` enum for state tracking, `ChangeType` enum for incremental processing, `ChangeInfo` for timestamp-based change detection, and bottom-up hierarchical context assembly without parent-to-child dependencies. The module enables developers to implement robust indexing workflows with accurate progress reporting, error tracking, and performance analysis capabilities essential for large-scale knowledge base operations.

##### Main Components

The module contains five primary dataclass models and two enumeration types. `FileContext` provides immutable file-level processing context with metadata, status tracking, and LLM analysis content storage. `DirectoryContext` delivers hierarchical directory processing context with child file aggregation, subdirectory relationships, and processing statistics calculation. `ChangeInfo` tracks detected changes during incremental indexing operations with timestamp-based change detection. `ProcessingStats` offers mutable statistics tracking for comprehensive performance metrics and error reporting. `IndexingStatus` provides overall operation status coordination and progress tracking. `ProcessingStatus` enum defines processing state transitions, while `ChangeType` enum categorizes change detection scenarios.

###### Architecture & Design

The architecture follows immutable context pattern design using frozen dataclasses for `FileContext`, `DirectoryContext`, and `ChangeInfo` to ensure thread-safe concurrent operations. The design implements clear separation between processing state and configuration through dedicated context structures. Bottom-up hierarchical context assembly enables parent directory processing without requiring child dependencies. Mutable statistics classes `ProcessingStats` and `IndexingStatus` provide real-time updates during processing operations. The design uses string-based enums for serialization compatibility and debugging clarity. Comprehensive tracking architecture supports both incremental and full indexing operations with timestamp-based change detection and processing status transitions.

####### Implementation Approach

The implementation utilizes dataclass field factories for default list initialization and property methods for calculated statistics. Processing duration calculations use datetime arithmetic with safe None handling for incomplete timing information. Completion tracking implements recursive aggregation through child context traversal for accurate progress reporting. Change detection employs timestamp comparison strategies with content change classification for processing optimization. Statistics calculation uses generator expressions for memory efficiency with large directory trees. The approach implements comprehensive error tracking with message preservation and chronological ordering. Serialization support uses dictionary conversion with ISO timestamp formatting for external system integration.

######## External Dependencies & Integration Points

**→ Inbound:** [what this file depends on]
- `dataclasses` (external library) - frozen dataclass implementation for immutable context structures
- `datetime` (external library) - timestamp handling and processing duration calculations
- `pathlib.Path` (external library) - filesystem path operations and validation
- `typing` (external library) - type annotations for Optional, List, Dict, Set, Any
- `enum.Enum` (external library) - string-based enumeration definitions

**← Outbound:** [what depends on this file]
- `knowledge_bases/indexing/hierarchical_indexer.py` - primary consumer of context models for indexing operations
- `knowledge_bases/tools/` - FastMCP tools using IndexingStatus for progress reporting
- `knowledge_bases/change_detection/` - change detection systems using ChangeInfo and ChangeType
- External monitoring systems - consuming ProcessingStats.to_dict() and IndexingStatus.to_dict() outputs

**⚡ System role and ecosystem integration:**
- **System Role**: Core data model foundation for the entire Knowledge Bases Hierarchical Indexing System providing context tracking and statistics
- **Ecosystem Position**: Central component enabling hierarchical processing workflow coordination and progress reporting across the Jesse Framework MCP
- **Integration Pattern**: Used by hierarchical indexer for context management, FastMCP tools for status reporting, and external systems for monitoring through serialization methods

######### Edge Cases & Error Handling

The module handles empty directory scenarios through `DirectoryContext.is_ready_for_summary` preventing indexing of totally empty directories while accepting completed empty directories. Division by zero protection exists in percentage calculations returning 0.0 for empty collections. Incomplete timing information handling returns None for processing duration calculations when start or end times are missing. Error message preservation maintains chronological order through `ProcessingStats.add_error` method. Change detection handles missing timestamp scenarios with Optional datetime fields. Processing status transitions support both successful and failed scenarios through comprehensive enum values. Thread-safe operations rely on immutable context structures preventing concurrent modification issues.

########## Internal Implementation Details

Property methods use conditional expressions and generator comprehensions for efficient calculation of aggregated statistics. Frozen dataclass implementation prevents accidental mutation during concurrent processing operations. Default factory functions ensure proper list initialization without shared mutable defaults. ISO timestamp formatting in serialization methods provides standard compatibility for external system integration. Recursive statistics calculation traverses subdirectory contexts using sum aggregation for memory efficiency. Error tracking uses list append operations maintaining insertion order for debugging analysis. String-based enum inheritance enables both enumeration behavior and serialization compatibility. Optional field handling uses None checks preventing attribute errors during incomplete processing states.

########### Code Usage Examples

This example demonstrates creating file context for processing tracking with timing and error handling. The code shows how to initialize FileContext instances and track processing duration through immutable context updates.

```python
from pathlib import Path
from datetime import datetime
from knowledge_context import FileContext, ProcessingStatus

# Create file context for processing
file_ctx = FileContext(
    file_path=Path("src/main.py"),
    file_size=1024,
    last_modified=datetime.now(),
    processing_status=ProcessingStatus.PROCESSING,
    processing_start_time=datetime.now()
)

# Update with completion
completed_ctx = FileContext(
    file_path=file_ctx.file_path,
    file_size=file_ctx.file_size,
    last_modified=file_ctx.last_modified,
    processing_status=ProcessingStatus.COMPLETED,
    knowledge_content="LLM analysis result",
    processing_start_time=file_ctx.processing_start_time,
    processing_end_time=datetime.now()
)

print(f"Processing took {completed_ctx.processing_duration} seconds")
```

This example shows directory context creation with readiness checking for hierarchical processing. The code demonstrates how to aggregate file contexts and check processing readiness for parent directory operations.

```python
from knowledge_context import DirectoryContext, ProcessingStatus

# Create directory context with file contexts
dir_ctx = DirectoryContext(
    directory_path=Path("src/"),
    file_contexts=[completed_ctx],
    processing_status=ProcessingStatus.PENDING
)

# Check readiness for summary generation
if dir_ctx.is_ready_for_summary:
    print(f"Directory ready: {dir_ctx.completion_percentage}% complete")
    print(f"Total files: {dir_ctx.total_files}, Completed: {dir_ctx.completed_files}")
```
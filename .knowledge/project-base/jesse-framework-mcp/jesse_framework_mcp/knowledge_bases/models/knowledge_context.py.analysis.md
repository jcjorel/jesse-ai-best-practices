<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/models/knowledge_context.py -->
<!-- Cached On: 2025-07-05T13:48:23.805327 -->
<!-- Source Modified: 2025-07-02T13:39:29.712510 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file defines runtime context data models for the Jesse Framework MCP Knowledge Bases Hierarchical Indexing System, providing immutable context structures for directory processing, file analysis, change tracking, and indexing operation status throughout hierarchical processing workflows. The module enables comprehensive tracking of indexing operations through structured data models supporting thread-safe operations, serialization, and async processing patterns. Key semantic entities include `ProcessingStatus` enum with states (`PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`, `SKIPPED`), `ChangeType` enum for change detection (`NEW`, `MODIFIED`, `DELETED`, `MOVED`), `FileContext` frozen dataclass for individual file processing state, `DirectoryContext` frozen dataclass for hierarchical directory processing, `ChangeInfo` frozen dataclass for incremental processing coordination, `ProcessingStats` mutable dataclass for comprehensive metrics tracking, `IndexingStatus` mutable dataclass for overall operation status, `dataclasses` module for structure definition, `datetime` for timestamp handling, `pathlib.Path` for filesystem operations, and `typing` annotations for type safety. The system implements bottom-up hierarchical context assembly without parent-to-child dependencies while maintaining accurate processing statistics and progress reporting capabilities.

##### Main Components

The file contains five primary data model classes and two enumeration types providing comprehensive context tracking capabilities. The `ProcessingStatus` enum defines processing states with five values for workflow coordination, while `ChangeType` enum provides four change categories for incremental processing optimization. The `FileContext` frozen dataclass tracks individual file processing with properties including `file_path`, `file_size`, `last_modified`, `processing_status`, `knowledge_content`, error tracking, and timing information with computed properties `processing_duration` and `is_completed`. The `DirectoryContext` frozen dataclass manages hierarchical directory processing with `directory_path`, `file_contexts` list, `subdirectory_contexts` list, processing state, and computed properties `total_files`, `completed_files`, `completion_percentage`, and `is_ready_for_summary`. The `ChangeInfo` frozen dataclass captures change detection information with path tracking, timestamps, and `is_content_change` property. The `ProcessingStats` mutable dataclass provides comprehensive metrics tracking with file statistics, directory statistics, content processing metrics, performance timing, and error collection. The `IndexingStatus` mutable dataclass coordinates overall operation status with progress tracking and serialization capabilities.

###### Architecture & Design

The architecture implements immutable context structures using frozen dataclasses for thread-safe operations during concurrent processing, with clear separation between processing state tracking and configuration management. The design follows bottom-up hierarchical context assembly patterns where child contexts are processed independently before parent directory processing, eliminating parent-to-child dependencies and enabling efficient concurrent operations. Key design patterns include the frozen dataclass pattern for immutable context preservation, computed property patterns for derived statistics calculation, mutable statistics tracking for real-time updates, and comprehensive serialization support through `to_dict()` methods. The system uses string-based enums for serialization compatibility and debugging clarity, with status transitions supporting both successful and failed processing scenarios. Error handling is integrated throughout with optional error message fields and comprehensive error tracking in statistics objects.

####### Implementation Approach

The implementation uses frozen dataclasses with `@dataclass(frozen=True)` decorator for immutable context structures ensuring thread safety during concurrent processing operations. Computed properties leverage list comprehensions and generator expressions for efficient statistics calculation across hierarchical structures, with recursive aggregation for directory-level metrics. The system implements safe division handling in percentage calculations returning 0.0 for empty collections to prevent division by zero errors. Change detection uses timestamp-based comparison with `datetime` objects and optional path tracking for move operations. Statistics tracking employs mutable dataclasses with field factories for list initialization and real-time metric updates throughout processing workflows. Serialization support uses dictionary conversion with ISO timestamp formatting and comprehensive field inclusion for external system integration.

######## External Dependencies & Integration Points

**→ Inbound:**
- `dataclasses` (external library) - frozen and mutable dataclass decorators for structure definition and immutability
- `datetime` (external library) - timestamp handling, comparison operations, and ISO format serialization
- `pathlib` (external library) - Path objects for cross-platform filesystem operations and validation
- `typing` (external library) - type annotations including Dict, List, Optional, Set, Any for type safety
- `enum` (external library) - Enum base class for ProcessingStatus and ChangeType enumeration definitions

**← Outbound:**
- `jesse_framework_mcp/knowledge_bases/indexing/hierarchical_indexer.py:HierarchicalIndexer` - consumes context models for processing coordination
- `jesse_framework_mcp/knowledge_bases/indexing/change_detector.py:ChangeDetector` - uses ChangeInfo and ChangeType for incremental processing
- `jesse_framework_mcp/knowledge_bases/indexing/knowledge_builder.py:KnowledgeBuilder` - updates FileContext and DirectoryContext during processing
- `jesse_framework_mcp/server.py:JesseFrameworkMCPServer` - uses IndexingStatus for operation monitoring and progress reporting
- External monitoring systems - consume serialized statistics and status information through to_dict() methods

**⚡ System role and ecosystem integration:**
- **System Role**: Core data model foundation for the Jesse Framework MCP hierarchical indexing system, providing structured context tracking and statistics throughout all processing operations
- **Ecosystem Position**: Central infrastructure component supporting all indexing workflows, serving as the primary data contract between processing components and external monitoring systems
- **Integration Pattern**: Used by all indexing components for state management and progress tracking, consumed by MCP server for operation monitoring, and integrated with external systems through comprehensive serialization capabilities

######### Edge Cases & Error Handling

The system handles division by zero scenarios in percentage calculations by returning 0.0 when total counts are zero, preventing calculation errors in empty directory or file collection scenarios. Missing timestamp information is handled gracefully with None returns from duration calculation properties, supporting incomplete processing scenarios and timing failures. Error message tracking uses optional string fields allowing processing to continue without error information while preserving failure details when available. Completion status checking combines multiple criteria including both status enumeration and content validation, ensuring robust completion detection across different processing scenarios. Recursive statistics calculation handles empty subdirectory collections and missing child contexts through safe aggregation patterns. Serialization handles optional datetime fields with None checking and ISO format conversion, preventing serialization failures when timing information is incomplete.

########## Internal Implementation Details

The frozen dataclass implementation uses `@dataclass(frozen=True)` decorator creating immutable objects with hash support for set operations and dictionary keys. Computed properties use generator expressions and sum aggregation for memory-efficient calculation across large directory hierarchies. The `field(default_factory=list)` pattern initializes mutable collections preventing shared reference issues between dataclass instances. String-based enums inherit from both `str` and `Enum` enabling direct string comparison and JSON serialization compatibility. Error tracking uses list append operations in `add_error()` method maintaining chronological error order for debugging analysis. Statistics calculation properties implement safe division with zero checking and appropriate default values for edge cases. Serialization methods use dictionary comprehension and conditional formatting for optional fields, ensuring complete data preservation while handling None values appropriately.

########### Code Usage Examples

Basic file context creation and status tracking demonstrates the fundamental pattern for individual file processing state management. This approach provides comprehensive tracking throughout the processing lifecycle with immutable context preservation.

```python
# Create and track file processing context with comprehensive state management
from datetime import datetime
from pathlib import Path

file_context = FileContext(
    file_path=Path("src/components/button.py"),
    file_size=1024,
    last_modified=datetime.now(),
    processing_status=ProcessingStatus.PENDING
)

# Check processing completion with content validation
if file_context.is_completed:
    print(f"File processed: {file_context.processing_duration}s")
```

Directory context hierarchical assembly showcases the bottom-up processing pattern with recursive statistics calculation. This pattern enables comprehensive progress tracking across directory hierarchies without parent-to-child dependencies.

```python
# Build hierarchical directory context with child aggregation and progress tracking
directory_context = DirectoryContext(
    directory_path=Path("src/components/"),
    file_contexts=[file_context1, file_context2],
    subdirectory_contexts=[subdir_context1, subdir_context2],
    processing_status=ProcessingStatus.PROCESSING
)

# Calculate hierarchical completion metrics
total_files = directory_context.total_files
completion_rate = directory_context.completion_percentage
is_ready = directory_context.is_ready_for_summary
```

Comprehensive statistics tracking and serialization demonstrates real-time metrics collection with external system integration. This approach provides detailed performance analysis and monitoring capabilities throughout indexing operations.

```python
# Track processing statistics with comprehensive metrics and error handling
stats = ProcessingStats()
stats.processing_start_time = datetime.now()
stats.total_files_discovered = 150
stats.files_completed = 120
stats.files_failed = 5

# Add error information and calculate performance metrics
stats.add_error("Failed to process corrupted file: example.py")
completion_rate = stats.files_completion_rate
error_rate = stats.error_rate

# Serialize for external monitoring systems
stats_dict = stats.to_dict()
```
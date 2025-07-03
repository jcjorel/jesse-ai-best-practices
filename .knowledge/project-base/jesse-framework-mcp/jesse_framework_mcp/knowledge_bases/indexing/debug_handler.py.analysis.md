<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/debug_handler.py -->
<!-- Cached On: 2025-07-04T00:46:40.749615 -->
<!-- Source Modified: 2025-07-02T00:45:16.569540 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements a comprehensive debug handler for LLM interaction persistence and replay within the JESSE Framework MCP knowledge base system, providing capture and reuse capabilities for debugging markdown formatting issues and template generation problems. The system delivers complete LLM interaction capture with structured file organization, replay functionality for deterministic output reuse, and pipeline stage organization for clear debugging workflows. Key semantic entities include `DebugHandler` class for debug orchestration, `LLMInteraction` dataclass for structured interaction data, `PIPELINE_STAGES` dictionary defining stage organization, `capture_stage_llm_output()` method for stage-specific capture, `get_stage_replay_response()` method for predictable replay, `_normalize_path_for_filename()` method for deterministic filename generation, memory cache system for performance optimization, and comprehensive error handling throughout all operations evidenced by methods like `capture_llm_interaction()`, `get_replay_response()`, and debug artifact management capabilities.

##### Main Components

Contains `DebugHandler` class as the primary debug orchestrator with initialization, capture, replay, and management methods. Includes `LLMInteraction` dataclass with structured fields for `interaction_id`, `conversation_id`, `prompt`, `response`, `timestamp`, `processing_type`, and optional context fields. Implements `PIPELINE_STAGES` class variable defining five-stage processing organization from file analysis through global summary. Provides core methods including `capture_stage_llm_output()`, `get_stage_replay_response()`, `capture_llm_interaction()`, `get_replay_response()`, and utility methods for filename normalization, directory management, and debug artifact organization. Implements memory cache system and file system persistence with comprehensive error handling throughout all operations.

###### Architecture & Design

Implements stage-based debug architecture with pipeline phase separation and predictable filename generation for deterministic debugging workflows. Uses dual-mode operation supporting both memory-only mode for performance and file system persistence for comprehensive debugging. Employs lazy initialization minimizing overhead when debug mode is disabled and automatic directory structure creation for stage-based organization. Integrates memory cache system for optimal performance with file system fallback for persistent debugging sessions. Follows separation of concerns with distinct capture and replay functionality, comprehensive error handling preventing debug failures from impacting main operations.

####### Implementation Approach

Uses predictable filename generation through path normalization enabling deterministic debug file locations and reliable replay functionality. Implements stage-based directory organization with five distinct pipeline stages for clear debugging workflow understanding. Employs hash-based interaction identification using MD5 prompt hashing combined with timestamps for unique interaction tracking. Uses comprehensive metadata preservation including processing context, file paths, and timing information for complete debugging context. Implements dual caching strategy with memory cache for performance and file system persistence for cross-session debugging continuity.

######## Code Usage Examples

Initialize the debug handler with stage-based organization and configure capture and replay modes. This establishes the foundation for comprehensive LLM interaction debugging:

```python
debug_handler = DebugHandler(
    debug_enabled=True,
    debug_output_directory=Path("/project/debug/"),
    enable_replay=True
)
```

Capture LLM output with stage-specific organization and predictable filename generation. This demonstrates stage-aware capture enabling deterministic replay debugging:

```python
debug_handler.capture_stage_llm_output(
    stage="stage_1_file_analysis",
    prompt="Analyze this file...",
    response="File analysis response...",
    file_path=Path("/project/src/module.py")
)
```

Retrieve saved LLM responses for replay functionality using predictable filename lookup. This enables deterministic debugging without redundant LLM calls:

```python
replay_response = debug_handler.get_stage_replay_response(
    stage="stage_1_file_analysis",
    file_path=Path("/project/src/module.py")
)
if replay_response:
    # Use saved response instead of calling LLM
    return replay_response
```

######### External Dependencies & Integration Points

**→ Inbound:**

- `json` (standard library) - debug metadata serialization and structured data persistence
- `pathlib.Path` (standard library) - debug file organization and cross-platform path handling
- `datetime` (standard library) - timestamp generation for debug artifact organization
- `hashlib` (standard library) - content hashing for duplicate detection and interaction identification
- `typing.Dict, Any, Optional, NamedTuple` (standard library) - type annotations for debug data structures
- `dataclasses.dataclass, asdict` (standard library) - structured data containers and serialization
- `logging` (standard library) - structured logging for debug operations and error reporting
- `tempfile` (standard library) - temporary directory creation for debug artifact storage

**← Outbound:**

- `knowledge_builder.KnowledgeBuilder` - consumes debug handler for LLM interaction capture and replay
- `hierarchical_indexer.HierarchicalIndexer` - uses debug handler for debugging indexing operations
- Debug artifact consumers - systems that process generated debug files and interaction data
- Manual debugging workflows - human processes that inspect and modify debug artifacts

**⚡ Integration:**

- Protocol: Direct Python imports and method calls with structured debug data containers
- Interface: Class methods for capture and replay operations with file system persistence
- Coupling: Loose coupling through optional debug mode and graceful degradation on failures

########## Edge Cases & Error Handling

Handles debug directory creation failures through comprehensive error handling with graceful degradation to memory-only mode when file system operations fail. Addresses file system permission issues by disabling debug persistence while maintaining memory cache functionality for continued operation. Manages corrupted debug files through individual file error handling preventing partial loading failures from breaking entire debug session restoration. Handles concurrent access scenarios through atomic file operations and proper error logging when debug artifacts are inaccessible. Provides comprehensive fallback mechanisms ensuring debug failures never impact main knowledge base processing operations.

########### Internal Implementation Details

Uses MD5 hash-based interaction identification combining prompt content hash with timestamp for unique interaction tracking across debugging sessions. Implements normalized path conversion replacing path separators and special characters with underscores for cross-platform filename compatibility. Maintains dual cache system with memory cache for immediate access and file system persistence for cross-session debugging continuity. Uses JSON serialization for metadata persistence with human-readable debug artifact organization supporting manual inspection and modification. Implements incremental debug index updates rather than full rebuilds for performance optimization during active debugging sessions.
<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/debug_handler.py -->
<!-- Cached On: 2025-07-04T16:34:22.660208 -->
<!-- Source Modified: 2025-07-02T00:45:16.569540 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This module implements a comprehensive debug handler for LLM output persistence and replay in the Jesse Framework MCP knowledge base system, providing complete capture and reuse of LLM interactions for debugging markdown formatting issues and template generation problems. It provides extensive debugging functionality including stage-based LLM output capture, predictable filename generation for deterministic replay, memory-only operation for performance optimization, and comprehensive interaction metadata preservation. The system enables efficient debugging workflows by maintaining structured debug artifacts with pipeline stage organization while supporting both capture mode for saving LLM outputs and replay mode for loading saved outputs without redundant API calls. Key semantic entities include `DebugHandler`, `LLMInteraction`, `PIPELINE_STAGES`, `capture_stage_llm_output`, `get_stage_replay_response`, `capture_llm_interaction`, `get_replay_response`, `_normalize_path_for_filename`, `json`, `hashlib`, `pathlib.Path`, and stage-based directory organization. The implementation uses predictable filename generation based on normalized paths and pipeline stages enabling deterministic debug file locations for reliable debugging workflows.

##### Main Components

The module contains the primary `DebugHandler` class with core debugging operations including stage-based capture (`capture_stage_llm_output`), replay functionality (`get_stage_replay_response`), and complete interaction capture (`capture_llm_interaction`, `get_replay_response`). Supporting data structures include `LLMInteraction` dataclass for structured interaction storage with comprehensive metadata fields. Utility methods include path normalization (`_normalize_path_for_filename`), debug directory management (`_ensure_debug_directory`, `_create_stage_documentation`), and index management (`_update_debug_index`, `load_existing_interactions`). Administrative functions include debug summary generation (`get_debug_summary`) and cleanup operations (`cleanup`) for proper resource management and debugging session finalization.

###### Architecture & Design

The architecture follows a stage-based debug organization pattern with the `DebugHandler` class serving as the central coordinator for LLM interaction capture and replay using pipeline stage definitions (`PIPELINE_STAGES`) for clear debugging workflow understanding. The design implements dual-mode operation with memory-only caching for performance optimization when debug mode is disabled and persistent file storage for comprehensive debugging when enabled. Predictable filename generation uses normalized path components and stage identifiers enabling deterministic debug file locations for reliable replay functionality. The system uses structured data organization with separate files for prompts, responses, and metadata supporting easy manual inspection and modification. Error handling ensures debug operations never interfere with core knowledge building processes through graceful degradation and comprehensive exception management.

####### Implementation Approach

The implementation uses hash-based interaction identification combining prompt content hashes with timestamps for unique interaction IDs enabling efficient lookup and replay functionality. Path normalization employs character replacement and cleanup algorithms converting filesystem paths into underscore-separated filename components for cross-platform compatibility. Stage-based file organization creates separate subdirectories for each pipeline stage with predictable naming patterns enabling easy navigation and manual debugging workflows. Memory caching provides performance optimization through in-memory storage for non-debug mode operation while maintaining full functionality. The system employs lazy initialization minimizing overhead when debug mode is disabled and comprehensive metadata preservation ensuring complete context reproduction for debugging sessions.

######## External Dependencies & Integration Points

**→ Inbound:**
- `json` (standard library) - debug metadata serialization and structured data persistence
- `hashlib` (standard library) - content hashing for duplicate detection and unique interaction identification
- `pathlib.Path` (standard library) - debug file organization and cross-platform path handling
- `datetime` (standard library) - timestamp generation for debug artifact organization and chronological sorting
- `typing.Dict` (standard library) - type annotations for debug data structures and metadata parameters
- `typing.Optional` (standard library) - optional parameter handling for flexible debug capture
- `dataclasses` (standard library) - structured data containers for LLM interaction representation

**← Outbound:**
- `knowledge_builder.py:KnowledgeBuilder` - consumes debug handler for LLM interaction capture and replay
- `hierarchical_indexer.py:HierarchicalIndexer` - uses debug functionality for debugging indexing workflows
- `llm_debug/` directory structure populated with stage-organized debug artifacts
- Debug index files and documentation consumed by manual debugging workflows and analysis tools

**⚡ System role and ecosystem integration:**
- **System Role**: Auxiliary debugging component for the Jesse Framework MCP knowledge base system, providing comprehensive LLM interaction capture and replay capabilities for debugging markdown formatting and template generation issues
- **Ecosystem Position**: Peripheral debugging support component serving as the primary debugging infrastructure, integrating with knowledge builders and indexers for comprehensive debugging workflow support
- **Integration Pattern**: Used by knowledge building components for debug capture and replay, consumed by developers for manual debugging workflows while producing structured debug artifacts for analysis and troubleshooting

######### Edge Cases & Error Handling

The system handles debug directory creation failures by disabling debug functionality and falling back to memory-only operation, ensuring core processing continues when filesystem issues occur. Missing or corrupted debug files are handled gracefully during replay operations by returning `None` and allowing fallback to live LLM calls for continued processing. Path normalization errors are managed through fallback to generic filenames while logging warnings for debugging purposes. Interaction loading failures during replay initialization are handled individually with error logging while continuing to load remaining valid interactions. The system provides comprehensive error handling for JSON serialization failures, file I/O errors, and metadata corruption while maintaining debug session integrity and preventing debug failures from impacting main knowledge building operations.

########## Internal Implementation Details

The `PIPELINE_STAGES` dictionary defines five distinct processing stages (`stage_1_file_analysis`, `stage_2_chunk_analysis`, `stage_3_chunk_aggregation`, `stage_4_directory_analysis`, `stage_5_global_summary`) with descriptive purposes for clear debugging workflow organization. Path normalization uses character replacement algorithms converting path separators to underscores and handling special characters for filesystem-safe filename generation. Memory cache uses string-based keys combining stage names and normalized paths for efficient lookup during non-debug mode operation. Interaction ID generation combines processing type, prompt hash (8-character MD5), and ISO timestamp for unique identification enabling efficient replay lookup. The `_create_stage_documentation` method generates comprehensive README files with pipeline stage explanations, filename patterns, and debugging workflow instructions for user guidance.

########### Code Usage Examples

Basic debug handler initialization demonstrates the core setup pattern for enabling comprehensive LLM interaction capture with stage-based organization. This approach provides structured debugging capabilities with predictable file locations for reliable debugging workflows.

```python
# Initialize debug handler with stage-based organization
debug_handler = DebugHandler(
    debug_enabled=True,
    debug_output_directory=Path(".knowledge"),
    enable_replay=True
)

# Load existing interactions for replay functionality
debug_handler.load_existing_interactions()
```

Stage-based LLM output capture showcases the primary debugging workflow for capturing and organizing LLM interactions by pipeline stage. This pattern enables deterministic debugging with predictable file locations and easy manual inspection capabilities.

```python
# Capture stage-specific LLM output with predictable filename generation
stage = "stage_1_file_analysis"
file_path = Path("src/components/button.py")
prompt = "Analyze this file for architectural patterns..."
response = "## File Analysis\n\nThis component implements..."

debug_handler.capture_stage_llm_output(
    stage=stage,
    prompt=prompt,
    response=response,
    file_path=file_path
)
```

Replay functionality demonstrates the deterministic debugging workflow for reusing previously captured LLM outputs without redundant API calls. This pattern enables efficient debugging iterations and consistent testing scenarios.

```python
# Check for existing debug response before making LLM call
replay_response = debug_handler.get_stage_replay_response(
    stage="stage_1_file_analysis",
    file_path=Path("src/components/button.py")
)

if replay_response:
    # Use saved response for deterministic debugging
    analysis_result = replay_response
else:
    # Make live LLM call and capture result
    analysis_result = await llm_client.analyze(prompt)
    debug_handler.capture_stage_llm_output(stage, prompt, analysis_result, file_path)
```
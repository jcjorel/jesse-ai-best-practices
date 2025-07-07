<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/knowledge_builder.py -->
<!-- Cached On: 2025-07-07T10:31:08.912802 -->
<!-- Source Modified: 2025-07-07T10:24:40.341219 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This module implements a 3-phase LLM-powered knowledge file builder for hierarchical indexing systems, specifically designed to generate structured knowledge files using `Claude4SonnetConfig` through `StrandsClaude4Driver` integration. The module provides comprehensive file analysis with cache-first processing via `FileAnalysisCache`, empty file special handling to prevent infinite rebuild loops, and continuation-based retry mechanisms with intelligent response completion. Key semantic entities include `KnowledgeBuilder`, `TruncationDetectedError`, `IndexingConfig`, `DirectoryContext`, `FileContext`, `ProcessingStatus`, `EnhancedPrompts`, `KnowledgeFileGenerator`, `DebugHandler`, and `FileAnalysisCache` for performance optimization. The implementation uses `asyncio` for async LLM operations, `pathlib` for cross-platform file handling, and `fastmcp.Context` for progress reporting. Evidence includes methods like `build_file_knowledge()`, `build_directory_summary()`, `_retry_llm_call_with_truncation_check()`, and `_review_content_until_compliant()` with comprehensive error handling and truncation detection.

##### Main Components

The module contains the core `KnowledgeBuilder` class with initialization methods `__init__()` and `initialize()`, primary processing methods `build_file_knowledge()` and `build_directory_summary()`, and specialized utility methods for content processing. Key processing methods include `_process_single_file()` for cache-first LLM analysis, `_generate_global_summary()` and `_generate_global_summary_from_contexts()` for directory synthesis, and `_extract_subdirectory_content()` for hierarchical content assembly. The module implements empty file handling through `_is_empty_file()` and `_generate_empty_file_analysis()` methods. Advanced retry mechanisms are provided by `_retry_llm_call_with_truncation_check()`, `_review_content_until_compliant()`, `_generate_continuation_prompt()`, and `_merge_responses()`. Utility methods include `_read_file_content()`, `_extract_content_from_llm_response()`, `_has_truncation_marker()`, and `_remove_truncation_marker()` for content processing and validation.

###### Architecture & Design

The architecture follows a 3-phase generation workflow with Phase 1 implementing individual file analysis through factual LLM processing, Phase 2 handling programmatic content insertion and subdirectory assembly, and Phase 3 executing global summary generation using assembled content. The design implements cache-first processing strategy through `FileAnalysisCache` integration, avoiding unnecessary LLM calls when source files haven't changed. The module uses continuation-based retry mechanisms instead of fresh conversation restarts, providing 90%+ token savings through intelligent response completion. Error handling follows a fail-fast approach with `TruncationDetectedError` preventing artifact creation when LLM output is incomplete. The architecture separates concerns between LLM operations, content processing, cache management, and debug handling through dedicated component classes. Configuration management uses hierarchical `IndexingConfig` structure with specialized settings for different processing modes.

####### Implementation Approach

The implementation uses dual truncation detection strategy combining programmatic marker checking with LLM reviewer validation for maximum reliability. Cache-first processing checks `FileAnalysisCache` before making LLM calls, with selective caching based on compliance review outcomes. The module implements intelligent response merging for continuation scenarios, detecting overlapping content at merge boundaries and removing duplicate sentences. Empty file handling uses filesystem metadata through `Path.stat().st_size` for efficient detection without content reading. Content extraction employs string processing to remove LLM-generated headers while preserving legitimate section structure. The bounded loop reviewer workflow applies iterative corrections with configurable maximum iterations to prevent infinite loops. Knowledge file generation uses template-based approach through `KnowledgeFileGenerator` with alphabetical sorting and complete rebuild strategy. Debug handling provides comprehensive interaction capture with replay functionality for consistent testing workflows.

######## External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.knowledge_bases.models:IndexingConfig` - configuration and processing parameters for knowledge building operations
- `jesse_framework_mcp.knowledge_bases.models:DirectoryContext` - directory processing context with file and subdirectory information
- `jesse_framework_mcp.knowledge_bases.models:FileContext` - file processing context with metadata and processing status
- `jesse_framework_mcp.knowledge_bases.models:ProcessingStatus` - enumeration for tracking processing states
- `jesse_framework_mcp.llm.strands_agent_driver:StrandsClaude4Driver` - Claude 4 Sonnet LLM integration driver
- `jesse_framework_mcp.llm.strands_agent_driver:Claude4SonnetConfig` - LLM configuration for analysis tasks
- `jesse_framework_mcp.helpers.path_utils:get_portable_path` - cross-platform path handling utility
- `knowledge_file_generator:KnowledgeFileGenerator` - template-based knowledge file generation
- `knowledge_prompts:EnhancedPrompts` - specialized prompts for different analysis types
- `debug_handler:DebugHandler` - debug interaction capture and replay functionality
- `file_analysis_cache:FileAnalysisCache` - performance optimization through caching
- `fastmcp:Context` (external library) - progress reporting and logging interface
- `asyncio` (external library) - async programming patterns for LLM operations
- `pathlib` (external library) - cross-platform file operations and path handling
- `logging` (external library) - structured logging for operations and error tracking

**← Outbound:**
- `jesse_framework_mcp.knowledge_bases.indexing.hierarchical_indexer:HierarchicalIndexer` - consumes KnowledgeBuilder for directory processing
- `generated/knowledge_files/*.md` - produces structured knowledge files in markdown format
- `cache/analysis_cache/` - creates cached analysis files for performance optimization
- `debug/interactions/` - generates debug interaction files for replay and analysis

**⚡ System role and ecosystem integration:**
- **System Role**: Core LLM processing engine for the Jesse Framework MCP knowledge base system, responsible for converting raw source files into structured knowledge representations through Claude 4 Sonnet analysis
- **Ecosystem Position**: Central component in the knowledge building pipeline, serving as the primary interface between source content and LLM processing capabilities
- **Integration Pattern**: Used by HierarchicalIndexer for bottom-up knowledge assembly, integrates with caching layer for performance, and coordinates with debug system for development workflows

######### Edge Cases & Error Handling

The module handles truncation detection through multiple strategies including programmatic marker checking, LLM reviewer validation, and continuation-based recovery mechanisms. Empty file scenarios are managed through special handling that generates standardized analysis content to prevent infinite rebuild loops. The implementation detects binary files through encoding errors and skips them appropriately during content reading. Cache staleness verification ensures knowledge files remain fresh after rebuild operations through algorithmic validation. Technical LLM errors trigger retry mechanisms with exponential backoff, while persistent failures result in graceful degradation. The bounded loop reviewer prevents infinite correction cycles through configurable maximum iterations. File system errors during knowledge file writing are handled with proper directory creation and error reporting. Continuation merging handles overlapping content scenarios through intelligent duplicate detection and removal. Debug handler errors are isolated to prevent cascading failures in the main processing pipeline.

########## Internal Implementation Details

The `_has_truncation_marker()` method performs fast string-based detection of the "--END OF LLM OUTPUT--" marker for immediate truncation identification. The `_merge_responses()` method implements sentence-level overlap detection using string splitting and similarity matching algorithms. Cache path calculation uses relative path computation from source root with project-base subdirectory enforcement. The `_extract_content_from_llm_response()` method filters conversational headers using pattern matching while preserving legitimate section structure. Knowledge file path generation implements handler root detection through directory name analysis and source root comparison. The `_review_content_until_compliant()` method captures each iteration separately in the debug system with structured stage naming. Response continuation uses conversation ID preservation to maintain context across truncation recovery attempts. File size detection for empty files uses `os.stat()` metadata access for performance optimization without content reading. The debug handler maintains interaction history with normalized path handling for consistent replay functionality.

########### Code Usage Examples

**Basic knowledge builder initialization and file processing:**
```python
# Initialize KnowledgeBuilder with configuration
config = IndexingConfig(...)
builder = KnowledgeBuilder(config)
await builder.initialize()

# Process individual file with cache-first strategy
file_context = FileContext(file_path=Path("example.py"), ...)
result = await builder.build_file_knowledge(file_context, ctx, source_root)
```

**Directory knowledge building with global summary generation:**
```python
# Build complete directory knowledge with subdirectory assembly
directory_context = DirectoryContext(directory_path=Path("src/"), ...)
result = await builder.build_directory_summary(directory_context, ctx, source_root)

# Access generated knowledge file path and content
knowledge_path = result.knowledge_file_path
global_summary = result.directory_summary
```

**Empty file detection and standardized analysis generation:**
```python
# Check for empty files and generate standardized content
if builder._is_empty_file(file_path):
    analysis = builder._generate_empty_file_analysis(file_path)
    # Cache the standardized analysis to prevent rebuild loops
    await builder.analysis_cache.cache_analysis(file_path, analysis, source_root)
```

**Continuation-based retry with intelligent response merging:**
```python
# Retry LLM call with continuation support for truncated responses
response, success = await builder._retry_llm_call_with_truncation_check(
    prompt=analysis_prompt,
    base_conversation_id="file_analysis_example",
    call_description="file analysis for example.py",
    max_retries=2,
    ctx=ctx
)
```
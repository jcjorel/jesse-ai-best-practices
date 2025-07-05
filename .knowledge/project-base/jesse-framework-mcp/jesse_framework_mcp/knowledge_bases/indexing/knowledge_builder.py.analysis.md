<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/knowledge_builder.py -->
<!-- Cached On: 2025-07-05T13:06:44.393929 -->
<!-- Source Modified: 2025-07-05T11:28:13.532931 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements a comprehensive LLM-powered knowledge file builder for the JESSE Framework's hierarchical indexing system, providing structured knowledge base generation through Claude 4 Sonnet integration. The file enables automated analysis and documentation of codebases through the `KnowledgeBuilder` class which orchestrates file analysis, directory summarization, and global content synthesis using cache-first processing strategies. Key semantic entities include `KnowledgeBuilder` class for orchestrating knowledge generation, `StrandsClaude4Driver` for Claude 4 Sonnet LLM integration, `FileAnalysisCache` for performance optimization, `EnhancedPrompts` for structured prompt generation, `KnowledgeFileGenerator` for template-based output, `DebugHandler` for replay functionality, `TruncationDetectedError` for artifact prevention, `IndexingConfig` for configuration management, `DirectoryContext` and `FileContext` for processing state tracking, and `ProcessingStatus` enumeration for operation monitoring. The technical architecture implements a continuation-based retry mechanism with intelligent response completion, providing 90%+ token savings through conversation continuity rather than fresh conversation restarts.

##### Main Components

The file contains the `KnowledgeBuilder` class with comprehensive initialization including `__init__()` for component setup, `initialize()` for LLM driver preparation, and `cleanup()` for resource management. Core processing methods include `build_file_knowledge()` for individual file analysis with cache-first processing, `build_directory_summary()` for directory-level knowledge generation, and `_process_single_file()` for cache-optimized file processing. Content generation methods encompass `_generate_global_summary()` for directory overview synthesis, `_generate_global_summary_from_contexts()` for context-based summarization, and `_extract_subdirectory_content()` for hierarchical content extraction. Quality assurance components include `_review_content_until_compliant()` for bounded loop compliance checking, `_retry_llm_call_with_truncation_check()` for continuation-based retry logic, `_generate_continuation_prompt()` and `_merge_responses()` for intelligent response completion. Utility methods provide `_read_file_content()` for robust file reading, `_extract_content_from_llm_response()` for clean content extraction, `_get_knowledge_file_path()` for path resolution, and truncation detection through `_has_truncation_marker()` and `_remove_truncation_marker()`.

###### Architecture & Design

The architecture follows a three-phase knowledge generation workflow optimizing token usage and content quality through cache-first processing, continuation-based retry mechanisms, and bounded loop quality assurance. The design implements a layered approach with `FileAnalysisCache` providing performance optimization, `EnhancedPrompts` ensuring structured analysis, and `DebugHandler` enabling replay functionality for consistent testing. The class uses composition over inheritance with specialized components for different aspects of knowledge generation, including LLM integration through `StrandsClaude4Driver`, template generation through `KnowledgeFileGenerator`, and error handling through custom `TruncationDetectedError` exceptions. The retry mechanism employs conversation continuity maintaining context across truncation recovery attempts, using intelligent response merging to combine truncated and continuation responses seamlessly. Quality assurance implements dual truncation detection strategy combining programmatic checks with LLM reviewer validation, ensuring artifact prevention when truncation is detected while maximizing compliance success rates through bounded iteration.

####### Implementation Approach

The implementation uses cache-first processing strategy through `FileAnalysisCache` integration, checking for existing analyses before making LLM calls to maximize performance and reduce API costs. LLM integration employs `Claude4SonnetConfig.create_optimized_for_analysis()` with extended thinking enabled for complex analysis tasks, using conversation-specific caching architecture to prevent cross-conversation cache pollution. The continuation-based retry mechanism generates natural completion requests using `_generate_continuation_prompt()` and merges responses through `_merge_responses()` with overlap detection and duplicate sentence removal. Content processing implements robust file reading with multiple encoding strategies (UTF-8 with latin-1 fallback), binary file detection, and graceful error handling for unreadable files. Quality assurance uses bounded loop reviewer workflow with dual truncation detection, first checking programmatically for truncation markers then applying LLM reviewer prompts for compliance validation. Knowledge file generation follows project-base indexing business rule using mandatory `project-base/` subdirectory structure, with template-based complete file replacement strategy for consistent output formatting.

######## External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.models.indexing_config:IndexingConfig` - configuration management for LLM parameters and processing settings
- `jesse_framework_mcp.models.knowledge_context:DirectoryContext` - directory processing state and context management
- `jesse_framework_mcp.models.knowledge_context:FileContext` - file processing state and metadata tracking
- `jesse_framework_mcp.models.knowledge_context:ProcessingStatus` - enumeration for operation status tracking
- `jesse_framework_mcp.llm.strands_agent_driver:StrandsClaude4Driver` - Claude 4 Sonnet LLM integration and conversation management
- `jesse_framework_mcp.llm.strands_agent_driver:Claude4SonnetConfig` - LLM configuration optimization for analysis tasks
- `jesse_framework_mcp.helpers.path_utils:get_portable_path` - cross-platform path conversion for knowledge base compatibility
- `jesse_framework_mcp.knowledge_bases.indexing.knowledge_file_generator:KnowledgeFileGenerator` - template-based knowledge file generation
- `jesse_framework_mcp.knowledge_bases.indexing.enhanced_prompts:EnhancedPrompts` - structured prompt generation for different content types
- `jesse_framework_mcp.knowledge_bases.indexing.debug_handler:DebugHandler` - debug capture and replay functionality for testing
- `jesse_framework_mcp.knowledge_bases.indexing.file_analysis_cache:FileAnalysisCache` - performance optimization through intelligent caching
- `fastmcp.Context` (external library) - MCP server context for progress reporting and logging
- `asyncio` (external library) - asynchronous programming patterns for LLM request handling
- `pathlib.Path` (external library) - cross-platform file operations and path handling
- `logging` (external library) - structured logging for LLM operations and error tracking

**← Outbound:**
- `jesse_framework_mcp.knowledge_bases.indexing.hierarchical_indexer:HierarchicalIndexer` - consumes KnowledgeBuilder for directory processing workflows
- `knowledge base files` - generated markdown files following hierarchical semantic tree structure
- `cache files` - stored analysis results for performance optimization and replay functionality
- `debug artifacts` - captured LLM interactions for testing and development workflows

**⚡ System role and ecosystem integration:**
- **System Role**: Core knowledge generation engine for JESSE Framework's hierarchical indexing system, orchestrating LLM-powered analysis and structured knowledge base creation
- **Ecosystem Position**: Central component bridging LLM capabilities with knowledge base requirements, providing the primary interface for converting source code into structured documentation
- **Integration Pattern**: Used by HierarchicalIndexer during directory processing workflows, consumed by development teams for automated documentation generation, and integrated with caching and debug systems for performance optimization and testing reliability

######### Edge Cases & Error Handling

Error handling includes comprehensive truncation detection through dual strategy combining programmatic marker checking with LLM reviewer validation, raising `TruncationDetectedError` to prevent any artifact creation when truncation is detected. File processing handles encoding issues through multiple fallback strategies (UTF-8 to latin-1), binary file detection through null byte checking, and graceful degradation for unreadable files returning empty content. LLM integration implements continuation-based retry mechanism with intelligent response merging, handling technical errors through conversation-specific retry logic and progressive continuation attempts for complex truncation scenarios. Cache management handles cache miss scenarios gracefully, falling back to fresh LLM analysis when cached content is unavailable or stale, with selective caching based on compliance review outcomes. Quality assurance implements bounded loop reviewer workflow preventing infinite loops while maximizing compliance success rates, distinguishing between technical errors requiring file skipping and content issues allowing cache storage. Directory processing handles missing subdirectory content through extraction fallbacks, timestamp-based change detection for rebuild optimization, and comprehensive error propagation for failed processing states.

########## Internal Implementation Details

The class uses lazy initialization for `StrandsClaude4Driver` through `initialize()` method, enabling startup without immediate LLM connection requirements and proper resource management through `cleanup()`. Conversation management employs unique conversation IDs with UUID suffixes for isolation, using base conversation IDs with iteration tracking for reviewer workflows and continuation attempts. Content extraction implements sophisticated LLM response cleaning through `_extract_content_from_llm_response()`, filtering conversational headers while preserving legitimate section structure through `_has_legitimate_section_structure()` detection. Cache integration uses conversation-specific keys preventing cross-conversation pollution, with selective caching logic storing only usable content from compliant or max-iterations-reached scenarios. Debug capture employs structured stage naming with iteration tracking, enabling comprehensive replay functionality through `DebugHandler` integration for consistent testing workflows. Path resolution implements mandatory project-base indexing business rule through `_get_knowledge_file_path()`, always using `project-base/` subdirectory structure regardless of configuration settings. Response merging uses intelligent overlap detection through sentence-level analysis, removing duplicate content at merge boundaries while preserving truncation markers for compliance validation.

########### Code Usage Examples

Basic knowledge builder initialization demonstrates the standard setup pattern for LLM-powered knowledge generation. This approach provides the foundation for all knowledge building operations with proper resource management.

```python
# Initialize knowledge builder with configuration and LLM setup
config = IndexingConfig(
    llm_model="claude-3-5-sonnet-20241022",
    temperature=0.1,
    max_tokens=4000,
    debug_mode=True
)

builder = KnowledgeBuilder(config)
await builder.initialize()  # Setup Claude 4 Sonnet driver
```

File knowledge generation with cache-first processing demonstrates high-performance analysis with automatic caching. This pattern maximizes efficiency by avoiding redundant LLM calls for unchanged files.

```python
# Generate file knowledge with cache optimization
file_context = FileContext(
    file_path=Path("src/components/Button.tsx"),
    file_size=1024,
    last_modified=datetime.now()
)

result_context = await builder.build_file_knowledge(
    file_context=file_context,
    ctx=mcp_context,
    source_root=Path("src/")
)

if result_context.processing_status == ProcessingStatus.COMPLETED:
    print(f"Knowledge generated: {len(result_context.knowledge_content)} characters")
```

Directory summary generation with global synthesis demonstrates comprehensive directory analysis using assembled content. This approach creates cohesive understanding from individual file analyses and subdirectory summaries.

```python
# Build directory summary with global synthesis
directory_context = DirectoryContext(
    directory_path=Path("src/components/"),
    file_contexts=[file_context1, file_context2],
    subdirectory_contexts=[subdir_context1]
)

summary_context = await builder.build_directory_summary(
    directory_context=directory_context,
    ctx=mcp_context,
    source_root=Path("src/")
)

if summary_context.processing_status == ProcessingStatus.COMPLETED:
    print(f"Knowledge file created: {summary_context.knowledge_file_path}")
```
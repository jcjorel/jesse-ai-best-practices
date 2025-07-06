<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/knowledge_builder.py -->
<!-- Cached On: 2025-07-07T00:08:35.563913 -->
<!-- Source Modified: 2025-07-07T00:06:50.635563 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements a comprehensive LLM-powered knowledge file generation system using `Claude4SonnetConfig` for hierarchical semantic analysis and structured knowledge base creation. The `KnowledgeBuilder` class provides cache-first file analysis through `FileAnalysisCache`, continuation-based retry mechanisms with `StrandsClaude4Driver`, and template-driven knowledge file assembly via `KnowledgeFileGenerator`. Key semantic entities include `TruncationDetectedError` for artifact prevention, `EnhancedPrompts` for specialized analysis workflows, `DebugHandler` for replay functionality, and `ProcessingStatus` enumeration for workflow state management. The system implements a 3-phase generation workflow: individual file analysis with factual LLM processing, programmatic content insertion and subdirectory assembly, and global summary generation using assembled content for comprehensive synthesis.

##### Main Components

The file contains the `KnowledgeBuilder` class as the primary orchestrator, `TruncationDetectedError` custom exception for truncation handling, and multiple private methods for specialized processing workflows. Core processing methods include `build_file_knowledge()` for individual file analysis, `build_directory_summary()` for hierarchical directory processing, and `_process_single_file()` for cache-first LLM analysis. Content generation methods encompass `_generate_global_summary()` for directory-level synthesis, `_extract_subdirectory_content()` for filtered content extraction, and `_generate_global_summary_from_contexts()` for comprehensive context assembly. Utility methods provide `_retry_llm_call_with_truncation_check()` for robust LLM communication, `_review_content_until_compliant()` for quality assurance, and `_merge_responses()` for intelligent response combination.

###### Architecture & Design

The system follows a hierarchical bottom-up assembly pattern where individual files are analyzed first, then aggregated into directory summaries, and finally synthesized into global knowledge files. The architecture implements a dual content strategy using full subdirectory content for LLM context and filtered content for final knowledge base files to prevent truncation issues. Cache-first processing strategy maximizes performance through `FileAnalysisCache` integration with selective bypass mechanisms for rebuild scenarios. The design incorporates a bounded loop reviewer workflow with dual truncation detection combining programmatic marker checks and LLM reviewer validation. Error handling follows a fail-fast approach with `TruncationDetectedError` preventing any artifact creation when truncation is detected, ensuring knowledge base integrity.

####### Implementation Approach

The implementation uses continuation-based retry mechanisms that maintain conversation context across truncation recovery attempts, providing 90%+ token savings compared to fresh conversation approaches. Content processing employs intelligent response merging with overlap detection and duplicate sentence removal for seamless content combination. The system implements a triple detection strategy for truncation: programmatic marker detection, LLM reviewer validation, and reviewer correction truncation checks. File analysis utilizes content chunking for large files exceeding LLM context window constraints, with specialized prompts based on content-type detection. Directory processing follows a centralized decision engine pattern where `RebuildDecisionEngine` determines processing requirements, and `KnowledgeBuilder` executes template generation with alphabetical sorting and full rebuild approaches.

######## External Dependencies & Integration Points

**→ Inbound:**
- `..models.IndexingConfig` - configuration parameters for LLM model settings and processing options
- `..models.DirectoryContext` - directory processing state and file context aggregation
- `..models.FileContext` - individual file processing metadata and knowledge content storage
- `..models.ProcessingStatus` - enumeration for workflow state management and error tracking
- `...llm.strands_agent_driver.StrandsClaude4Driver` - Claude 4 Sonnet LLM integration for content analysis
- `...llm.strands_agent_driver.Claude4SonnetConfig` - LLM configuration optimization for analysis tasks
- `.knowledge_file_generator.KnowledgeFileGenerator` - template engine for structured knowledge file creation
- `.knowledge_prompts.EnhancedPrompts` - specialized prompt generation for different analysis contexts
- `.debug_handler.DebugHandler` - debug capture and replay functionality for development workflows
- `.file_analysis_cache.FileAnalysisCache` - performance optimization through timestamp-based cache management

**← Outbound:**
- `hierarchical_indexer.py:HierarchicalIndexer` - primary consumer for directory knowledge building workflows
- `knowledge_base_handlers/` - handler implementations consuming knowledge building services for different content types
- `debug_output/` - debug interaction capture files for replay and analysis workflows
- `cache/` - cached analysis files for performance optimization and staleness detection

**⚡ System role and ecosystem integration:**
- **System Role**: Core knowledge generation engine within the Jesse Framework MCP server, responsible for transforming raw file content into structured hierarchical knowledge bases through LLM analysis
- **Ecosystem Position**: Central component bridging file system analysis with LLM processing capabilities, serving as the primary content transformation layer
- **Integration Pattern**: Used by `HierarchicalIndexer` for bottom-up knowledge assembly, consumed by knowledge base handlers for different content types, and integrated with caching and debug systems for performance and development workflows

######### Edge Cases & Error Handling

The system implements comprehensive truncation detection through `TruncationDetectedError` which completely prevents artifact creation when LLM responses are incomplete, ensuring knowledge base integrity. Empty file handling gracefully skips unreadable or zero-length files with appropriate status tracking through `ProcessingStatus.SKIPPED`. Binary file detection prevents processing of unsuitable content through encoding error handling and null byte detection. Technical LLM errors are distinguished from content errors, with technical failures triggering file skipping while content issues allow caching of best-attempt results. The bounded loop reviewer prevents infinite loops through maximum iteration limits while preserving LLM work through forced caching when max iterations are reached. Cache staleness verification includes algorithm bug detection that raises runtime errors when freshness expectations are violated after rebuild operations.

########## Internal Implementation Details

The cache-first processing strategy checks `FileAnalysisCache` before LLM calls unless bypass conditions are met through rebuild decisions or full indexing mode. Conversation ID generation uses normalized path patterns with UUID suffixes for unique LLM conversation contexts. Content extraction employs header filtering to remove LLM conversational artifacts while preserving legitimate section structure through pattern recognition. The dual content strategy loads full KB content for LLM global summary context while extracting filtered fourth-level header content for final KB integration. Response merging implements sentence-level overlap detection with boundary analysis and duplicate removal for seamless content combination. Debug capture follows structured stage naming with iteration tracking for comprehensive replay functionality. Knowledge file path determination implements handler root detection for proper `root_kb.md` vs `{directory_name}_kb.md` naming conventions.

########### Code Usage Examples

**Basic knowledge builder initialization and file processing:**
```python
# Initialize knowledge builder with configuration
config = IndexingConfig(llm_model="claude-3-5-sonnet-20241022", debug_mode=True)
builder = KnowledgeBuilder(config)
await builder.initialize()

# Process individual file with cache-first approach
file_context = FileContext(file_path=Path("src/module.py"), file_size=5000, last_modified=datetime.now())
result = await builder.build_file_knowledge(file_context, ctx, source_root=Path("/project"))
```

**Directory knowledge building with hierarchical assembly:**
```python
# Build directory summary with subdirectory aggregation
directory_context = DirectoryContext(
    directory_path=Path("src/components/"),
    file_contexts=[completed_file_contexts],
    subdirectory_contexts=[completed_subdir_contexts]
)
result = await builder.build_directory_summary(directory_context, ctx, source_root)
```

**Error handling and truncation detection:**
```python
try:
    knowledge_content = await builder.build_file_knowledge(file_context, ctx)
except TruncationDetectedError as e:
    # Truncation detected - no artifacts created, file completely skipped
    logger.error(f"File skipped due to truncation: {e}")
    return None  # Indicates complete file omission from processing
```
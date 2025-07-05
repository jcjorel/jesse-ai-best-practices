<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/knowledge_builder.py -->
<!-- Cached On: 2025-07-05T20:34:27.399807 -->
<!-- Source Modified: 2025-07-05T20:01:14.887922 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

The `knowledge_builder.py` file implements a 3-phase LLM-powered knowledge file generation system for the Jesse Framework MCP's hierarchical indexing operations, providing automated analysis of source code files and directories through `Claude 4 Sonnet` integration via `StrandsClaude4Driver`. This module enables cache-first file analysis with `FileAnalysisCache` for performance optimization, intelligent truncation detection through `TruncationDetectedError` exception handling, and continuation-based retry mechanisms that preserve conversation context for 90%+ token savings during LLM failures. Key semantic entities include the `KnowledgeBuilder` class with methods like `build_file_knowledge()` and `build_directory_summary()`, integration with `EnhancedPrompts` for specialized analysis approaches, `DebugHandler` for replay functionality, and `KnowledgeFileGenerator` for template-based output generation. The system implements a bounded loop reviewer workflow through `_review_content_until_compliant()` that combines programmatic truncation detection with LLM-based compliance checking, ensuring robust quality assurance while preventing artifact creation when responses are incomplete.

##### Main Components

The file contains the `KnowledgeBuilder` class as the primary orchestrator with initialization methods `__init__()` and `initialize()`, core processing methods `build_file_knowledge()` and `build_directory_summary()` for content generation, and specialized helper methods including `_process_single_file()` for cache-first analysis, `_generate_global_summary()` for directory synthesis, and `_retry_llm_call_with_truncation_check()` for robust LLM communication. Supporting components include the `TruncationDetectedError` exception class for artifact prevention, content processing utilities like `_extract_content_from_llm_response()` and `_merge_responses()` for intelligent response handling, and infrastructure methods such as `_read_file_content()` for file operations and `cleanup()` for resource management.

###### Architecture & Design

The architecture follows a 3-phase generation workflow with Phase 1 implementing individual file analysis through cache-first LLM processing, Phase 2 handling programmatic content insertion and subdirectory assembly, and Phase 3 performing global summary generation using assembled content for comprehensive synthesis. The design implements a continuation-based retry pattern that maintains conversation context across truncation recovery attempts, combined with a dual detection strategy using both programmatic marker checking and LLM reviewer validation for maximum reliability. The system uses a bounded loop reviewer architecture with selective caching that preserves LLM work while preventing artifact creation on technical failures, integrated with debug replay functionality for consistent testing and development workflows.

####### Implementation Approach

The implementation employs cache-first processing through `FileAnalysisCache` integration with timestamp-based staleness detection, bypassed only in `full` indexing mode for nuclear rebuild scenarios. LLM communication uses `Claude4SonnetConfig.create_optimized_for_analysis()` with extended thinking enabled, processed through conversation-specific caching architecture that prevents cross-conversation cache pollution. The retry mechanism implements intelligent response merging with overlap detection and duplicate sentence removal, while the review system uses a triple detection strategy combining programmatic truncation marker checking, LLM reviewer prompts, and reviewer correction validation. Content processing includes specialized encoding detection with UTF-8 and latin-1 fallback strategies, binary file detection, and structured knowledge file generation following hierarchical semantic context patterns.

######## External Dependencies & Integration Points

**→ Inbound:** [knowledge building dependencies]
- `..models:IndexingConfig` - configuration parameters and processing settings
- `..models:DirectoryContext` - directory processing state and file contexts
- `..models:FileContext` - individual file processing metadata and status
- `...llm.strands_agent_driver:StrandsClaude4Driver` - Claude 4 Sonnet LLM integration
- `.knowledge_file_generator:KnowledgeFileGenerator` - template-based output generation
- `.enhanced_prompts:EnhancedPrompts` - specialized analysis prompt generation
- `.file_analysis_cache:FileAnalysisCache` - performance optimization through caching
- `fastmcp:Context` - progress reporting and logging integration
- `asyncio` (external library) - async programming patterns for LLM operations
- `pathlib` (external library) - cross-platform file system operations

**← Outbound:** [knowledge building consumers]
- `knowledge_bases/indexing/` - hierarchical indexing operations consuming generated knowledge files
- `*_kb.md` - generated knowledge files following hierarchical semantic context patterns
- `debug_output/` - captured LLM interactions and replay data for development workflows
- `cache/` - cached file analyses for performance optimization across indexing runs

**⚡ System role and ecosystem integration:**
- **System Role**: Core knowledge generation engine that transforms raw source code into structured, searchable knowledge bases through LLM analysis, serving as the primary content creation component in the Jesse Framework MCP indexing pipeline
- **Ecosystem Position**: Central processing component that bridges file system analysis with knowledge base creation, enabling automated documentation and code understanding workflows
- **Integration Pattern**: Used by indexing handlers during knowledge base construction, with cache-first processing for performance, debug replay for development consistency, and template-based output for standardized knowledge file formats

######### Edge Cases & Error Handling

The system handles truncation detection through multiple strategies including programmatic marker checking with `_has_truncation_marker()`, LLM reviewer validation returning "TRUNCATED" responses, and continuation response validation to prevent incomplete artifact creation. File processing errors include encoding detection failures with UTF-8/latin-1 fallback, binary file detection through null byte checking, and empty file handling with graceful skipping. LLM communication failures trigger continuation-based retry mechanisms with intelligent response merging, while technical errors during review processes result in selective file skipping to preserve cache integrity. The bounded loop reviewer prevents infinite iterations through `max_iterations` limits, with comprehensive error capture through `DebugHandler` for troubleshooting and replay functionality.

########## Internal Implementation Details

The `_config_cache` and conversation-specific caching architecture prevents cross-conversation cache pollution through conversation ID inclusion in cache keys. File analysis caching uses timestamp-based staleness detection with selective caching that preserves LLM work for both compliant and max-iterations-reached scenarios, bypassed only in `full` indexing mode. The continuation mechanism uses `_generate_continuation_prompt()` with context-aware completion requests and `_merge_responses()` with overlap detection and duplicate sentence removal for seamless content flow. Knowledge file generation follows the pattern `{directory_name}_kb.md` with mandatory `project-base/` subdirectory structure, using complete file replacement strategy with proper parent directory creation and UTF-8 encoding.

########### Code Usage Examples

This example demonstrates initializing the knowledge builder and processing a single file with cache-first analysis. The code shows the essential workflow for setting up the builder with configuration and processing individual files through the cache-first analysis system.

```python
from pathlib import Path
from jesse_framework_mcp.knowledge_bases.indexing.knowledge_builder import KnowledgeBuilder
from jesse_framework_mcp.knowledge_bases.models import IndexingConfig, FileContext

# Initialize knowledge builder with configuration
config = IndexingConfig.from_dict({"llm_model": "claude-3-5-sonnet-20241022"})
builder = KnowledgeBuilder(config)
await builder.initialize()

# Process single file with cache-first analysis
file_context = FileContext(file_path=Path("src/main.py"), file_size=1024)
result = await builder.build_file_knowledge(file_context, ctx, source_root=Path("."))
print(f"Analysis status: {result.processing_status}")
```

This example shows directory knowledge building with global summary generation and template-based output. The code demonstrates the complete workflow for processing directories with subdirectory assembly and knowledge file generation.

```python
# Build directory knowledge with subdirectory assembly
directory_context = DirectoryContext(
    directory_path=Path("src/components/"),
    file_contexts=[file_context1, file_context2],
    subdirectory_contexts=[subdir_context1]
)

result = await builder.build_directory_summary(directory_context, ctx, source_root=Path("."))
print(f"Knowledge file: {result.knowledge_file_path}")
print(f"Global summary length: {len(result.directory_summary)}")

# Cleanup resources
await builder.cleanup()
```
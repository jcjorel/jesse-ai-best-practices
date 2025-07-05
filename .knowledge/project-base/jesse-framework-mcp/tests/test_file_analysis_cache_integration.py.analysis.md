<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/tests/test_file_analysis_cache_integration.py -->
<!-- Cached On: 2025-07-05T20:05:41.306573 -->
<!-- Source Modified: 2025-07-05T18:03:27.972527 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file provides comprehensive integration testing for the `FileAnalysisCache` system within the Jesse Framework MCP knowledge building pipeline. It validates cache-first processing workflows, metadata handling, timestamp-based freshness detection, and performance optimization through cached analysis retrieval. The test suite ensures `FileAnalysisCache` correctly integrates with `KnowledgeBuilder`, `IndexingConfig`, `FileContext`, and `StrandsClaude4Driver` components while maintaining proper cache invalidation based on file modification timestamps. Key semantic entities include `FileAnalysisCache`, `KnowledgeBuilder`, `MockContext`, `IndexingConfig`, `OutputConfig`, `ChangeDetectionConfig`, `FileContext`, `ProcessingStatus`, `METADATA_START`, `METADATA_END`, `get_cached_analysis()`, `cache_analysis()`, `get_cache_path()`, `build_file_knowledge()`, `timestamp_tolerance_seconds`, and `cache_stats()` enabling comprehensive validation of the caching subsystem's integration points and performance characteristics.

##### Main Components

Contains four primary test functions: `test_cache_basic_functionality()` for storage/retrieval validation, `test_cache_freshness_checking()` for timestamp-based invalidation, `test_cache_integration_with_knowledge_builder()` for end-to-end workflow testing with mock LLM responses, and `test_cache_performance_simulation()` for multi-file cache hit rate analysis. Includes `MockContext` class simulating FastMCP logging interface and `MockKnowledgeBuilder` class extending `KnowledgeBuilder` with deterministic mock responses. The `run_all_cache_tests()` orchestrator executes all test scenarios and provides comprehensive result reporting with pass/fail statistics.

###### Architecture & Design

Implements isolated test environments using `tempfile.TemporaryDirectory()` for each test scenario, ensuring clean state between tests. Uses dependency injection pattern with mock objects (`MockContext`, `MockKnowledgeBuilder`) to eliminate external API dependencies while preserving integration behavior. Follows arrange-act-assert testing pattern with explicit validation checkpoints and detailed error reporting. Test architecture separates concerns between cache mechanics testing, freshness validation, integration workflow testing, and performance simulation through distinct test functions.

####### Implementation Approach

Employs realistic file system simulation with proper directory structures (`src/`, `components/`, `project/`) and authentic file content (Python scripts, TypeScript React components). Uses `asyncio.sleep()` for timestamp manipulation in freshness testing and implements cache hit/miss detection through return value analysis. Mock LLM responses provide deterministic test outcomes while preserving actual cache integration pathways. Performance testing simulates batch processing scenarios with multiple files to validate cache efficiency at scale.

######## External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.knowledge_bases.indexing.knowledge_builder:KnowledgeBuilder` - core knowledge building functionality
- `jesse_framework_mcp.knowledge_bases.indexing.file_analysis_cache:FileAnalysisCache` - primary cache implementation under test
- `jesse_framework_mcp.knowledge_bases.models.indexing_config:IndexingConfig` - configuration management
- `jesse_framework_mcp.knowledge_bases.models.knowledge_context:FileContext` - file processing context
- `jesse_framework_mcp.llm.strands_agent_driver:StrandsClaude4Driver` - LLM integration (mocked)
- `tempfile` (external library) - temporary directory management
- `asyncio` (external library) - asynchronous test execution

**← Outbound:**
- `sys.exit()` - process termination with success/failure codes
- Console output via `print()` - test progress and result reporting
- File system operations through `Path.write_text()` and `Path.read_text()`

**⚡ System role and ecosystem integration:**
- **System Role**: Critical validation component ensuring `FileAnalysisCache` integration reliability within Jesse Framework MCP knowledge building pipeline
- **Ecosystem Position**: Core testing infrastructure validating caching subsystem performance and correctness
- **Integration Pattern**: Executed by developers and CI/CD systems to validate cache implementation before deployment, ensuring knowledge building performance optimization works correctly

######### Edge Cases & Error Handling

Validates cache behavior when source files are modified after caching through timestamp comparison with configurable `timestamp_tolerance_seconds`. Tests cache miss scenarios when cache files don't exist or are stale, ensuring proper fallback to LLM processing. Handles metadata corruption scenarios by validating `METADATA_START` and `METADATA_END` delimiter presence in cache files. Includes whitespace tolerance in content comparison (up to 5 character differences) to handle minor formatting variations between cache storage and retrieval operations.

########## Internal Implementation Details

Cache files are stored with `.analysis.md` extension in knowledge directory structure mirroring source hierarchy. Metadata delimiters (`METADATA_START`, `METADATA_END`) wrap file timestamps and processing information while being stripped from retrieved content. Mock LLM responses are deterministic strings containing realistic analysis content for consistent test validation. Test execution uses temporary directories with automatic cleanup and provides detailed progress logging with emoji indicators for visual test status tracking.

########### Code Usage Examples

**Basic cache functionality validation:**
```python
cache = FileAnalysisCache(config)
test_analysis = "## Test Analysis\n\nThis is a test Python file."
await cache.cache_analysis(test_file, test_analysis, source_root)
retrieved_analysis = await cache.get_cached_analysis(test_file, source_root)
assert retrieved_analysis == test_analysis
```

**Cache freshness testing with file modification:**
```python
# Cache original content
await cache.cache_analysis(test_file, original_analysis, source_root)
# Modify file after caching
await asyncio.sleep(2)
test_file.write_text("# Modified content")
# Verify cache invalidation
stale_retrieval = await cache.get_cached_analysis(test_file, source_root)
assert stale_retrieval is None
```

**Integration testing with KnowledgeBuilder:**
```python
file_context = FileContext(
    file_path=test_file,
    file_size=test_file.stat().st_size,
    last_modified=datetime.fromtimestamp(test_file.stat().st_mtime)
)
result = await builder.build_file_knowledge(file_context, ctx, source_root)
assert result.processing_status == ProcessingStatus.COMPLETED
```
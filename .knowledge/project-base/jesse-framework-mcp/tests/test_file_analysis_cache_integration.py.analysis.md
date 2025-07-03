<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/tests/test_file_analysis_cache_integration.py -->
<!-- Cached On: 2025-07-04T00:18:48.270526 -->
<!-- Source Modified: 2025-07-03T16:30:11.962937 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

Validates comprehensive integration between `FileAnalysisCache` and the JESSE Framework MCP Server knowledge building system through automated testing of cache-first processing, metadata handling, freshness validation, and performance optimization scenarios. Provides end-to-end verification of caching mechanisms within the knowledge indexing pipeline, ensuring proper file analysis storage, retrieval, and staleness detection for LLM-generated content. Enables developers to verify cache functionality before deployment by testing storage/retrieval cycles, timestamp-based freshness checking, metadata stripping, and integration with `KnowledgeBuilder` workflows. Key semantic entities include `FileAnalysisCache` class, `KnowledgeBuilder` integration, `IndexingConfig` configuration management, `FileContext` and `ProcessingStatus` from knowledge context models, `MockContext` for testing, `tempfile.TemporaryDirectory` for isolated testing, `asyncio` for async execution, `METADATA_START` and `METADATA_END` delimiters, `get_cached_analysis()` and `cache_analysis()` methods, `get_cache_stats()` statistics, and `.knowledge/` directory structure conventions.

##### Main Components

Contains four primary test functions: `test_cache_basic_functionality()` for validating storage, retrieval, and metadata handling, `test_cache_freshness_checking()` for timestamp-based staleness detection, `test_cache_integration_with_knowledge_builder()` for end-to-end workflow testing with mock LLM responses, and `test_cache_performance_simulation()` for multi-file cache hit rate validation. Includes `MockContext` class providing async logging methods and `MockKnowledgeBuilder` subclass that overrides LLM processing with deterministic responses. The `run_all_cache_tests()` orchestration function executes sequential test execution with comprehensive result reporting and statistics.

###### Architecture & Design

Implements comprehensive testing strategy using temporary directories for isolated test environments and mock objects to eliminate external dependencies. Uses inheritance pattern with `MockKnowledgeBuilder` extending real `KnowledgeBuilder` to override LLM calls while preserving cache integration logic. Employs async context managers for proper resource cleanup and sequential test execution with individual result tracking. Separates concerns between basic cache functionality, freshness validation, integration testing, and performance simulation to enable precise failure identification.

####### Implementation Approach

Testing strategy uses `tempfile.TemporaryDirectory` for isolated file system operations and `asyncio.sleep()` for timestamp manipulation in freshness tests. Cache validation employs direct file system inspection to verify cache file creation at expected paths and content validation through metadata delimiter checking. Mock LLM integration uses predetermined response strings to ensure deterministic test results while preserving actual cache logic paths. Performance testing creates multiple files with simulated processing cycles to validate cache hit rates and statistics accuracy.

######## Code Usage Examples

Execute comprehensive cache integration testing with isolated environments. This demonstrates the complete test suite execution with result aggregation:

```python
# Run all cache integration tests with comprehensive reporting
success = asyncio.run(run_all_cache_tests())
sys.exit(0 if success else 1)
```

Test basic cache functionality with storage and retrieval validation. This validates fundamental cache operations with metadata handling:

```python
# Test cache storage and retrieval with metadata validation
config = IndexingConfig(knowledge_output_directory=knowledge_dir)
cache = FileAnalysisCache(config)
test_analysis = "## Test Analysis\n\nThis is a test analysis."
await cache.cache_analysis(test_file, test_analysis, source_root)
retrieved_analysis = await cache.get_cached_analysis(test_file, source_root)
assert retrieved_analysis == test_analysis
```

Validate cache freshness checking with file modification scenarios. This tests timestamp-based staleness detection and cache invalidation:

```python
# Test cache freshness with file modification
await cache.cache_analysis(test_file, original_analysis, source_root)
await asyncio.sleep(2)  # Ensure timestamp difference
test_file.write_text("# Modified content")
stale_retrieval = await cache.get_cached_analysis(test_file, source_root)
assert stale_retrieval is None  # Cache should be invalidated
```

######### External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.knowledge_bases.indexing.knowledge_builder:KnowledgeBuilder` - main knowledge building system
- `jesse_framework_mcp.knowledge_bases.indexing.file_analysis_cache:FileAnalysisCache` - caching system under test
- `jesse_framework_mcp.knowledge_bases.models.indexing_config:IndexingConfig` - configuration management
- `jesse_framework_mcp.knowledge_bases.models.knowledge_context:FileContext` - file processing context
- `jesse_framework_mcp.knowledge_bases.models.knowledge_context:ProcessingStatus` - processing status enumeration
- `jesse_framework_mcp.llm.strands_agent_driver:StrandsClaude4Driver` - LLM driver integration
- `jesse_framework_mcp.llm.strands_agent_driver:Claude4SonnetConfig` - LLM configuration
- `tempfile` (standard library) - temporary directory creation for isolated testing
- `asyncio` (standard library) - async execution framework
- `pathlib.Path` (standard library) - cross-platform path handling
- `datetime` (standard library) - timestamp manipulation for freshness testing

**← Outbound:**
- `console/stdout` - test results and progress reporting with emoji indicators
- `CI/CD pipelines/` - test success/failure status through exit codes
- `development workflows/` - cache integration validation for knowledge building
- `cache files/` - generated `.analysis.md` files in `.knowledge/` directory structure

**⚡ Integration:**
- Protocol: Direct Python imports with async/await patterns and file system operations
- Interface: Class instantiation, method calls, and file I/O operations
- Coupling: Tight coupling with cache system and loose coupling with LLM components through mocking

########## Edge Cases & Error Handling

Handles missing cache files gracefully by returning `None` from `get_cached_analysis()` calls and validating proper cache miss behavior. Manages file modification scenarios through timestamp comparison with configurable tolerance settings via `timestamp_tolerance_seconds`. Addresses test environment isolation through temporary directory cleanup and proper async context management. Provides comprehensive error reporting with detailed failure context including expected vs actual comparisons and cache file path validation. Implements graceful degradation for cache statistics when no files are cached and validates proper metadata delimiter presence in cache files.

########### Internal Implementation Details

Uses emoji-based status reporting (✅, ❌, 💥) for immediate visual feedback during test execution with detailed progress logging. Implements cache path validation through expected path construction using knowledge directory structure conventions like `project-base/` subdirectories. Employs content comparison with whitespace tolerance for cache hit validation, allowing up to 5 character differences for minor formatting variations. Test result aggregation uses tuple lists for test name and boolean result pairs, enabling summary statistics calculation and overall success determination. Mock LLM responses use predetermined analysis strings to ensure deterministic test outcomes while preserving actual cache integration logic paths.
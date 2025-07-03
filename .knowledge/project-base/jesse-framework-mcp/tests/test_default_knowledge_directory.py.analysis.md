<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/tests/test_default_knowledge_directory.py -->
<!-- Cached On: 2025-07-04T00:18:52.051850 -->
<!-- Source Modified: 2025-07-03T23:01:11.066874 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

Validates comprehensive `FileAnalysisCache` integration within the JESSE Framework MCP Server knowledge building system through automated testing of cache-first processing, metadata handling, freshness validation, and performance optimization scenarios. Provides extensive test coverage for cache storage and retrieval mechanisms, timestamp-based staleness detection, and seamless integration with `KnowledgeBuilder` workflows. Enables developers to verify caching system reliability before production deployment by testing cache hit/miss scenarios, metadata stripping functionality, and multi-file processing performance benefits. Key semantic entities include `FileAnalysisCache` class, `KnowledgeBuilder` integration, `IndexingConfig` configuration management, `FileContext` and `ProcessingStatus` from knowledge context models, `MockContext` test helper, `test_cache_basic_functionality()`, `test_cache_freshness_checking()`, `test_cache_integration_with_knowledge_builder()`, `test_cache_performance_simulation()`, `METADATA_START` and `METADATA_END` delimiters, `get_cached_analysis()` and `cache_analysis()` methods, `tempfile.TemporaryDirectory` for isolated testing, and `asyncio` for async test execution.

##### Main Components

Contains four primary test functions: `test_cache_basic_functionality()` for validating storage, retrieval, and metadata handling, `test_cache_freshness_checking()` for timestamp-based cache invalidation testing, `test_cache_integration_with_knowledge_builder()` for end-to-end workflow validation with mock LLM responses, and `test_cache_performance_simulation()` for multi-file cache hit rate verification. Includes `MockContext` class providing async logging methods and `MockKnowledgeBuilder` subclass that simulates LLM processing without external API calls. The `run_all_cache_tests()` orchestration function executes sequential test execution with comprehensive result aggregation and performance metrics reporting.

###### Architecture & Design

Implements comprehensive test architecture with isolated temporary directories for each test scenario to prevent cross-test contamination. Uses mock object pattern for external dependencies like LLM drivers and MCP contexts, enabling testing without actual API calls or server connections. Employs realistic file structure simulation with TypeScript React components and Python modules to validate cache behavior across different file types. Separates cache functionality testing from integration testing, allowing precise identification of cache-specific vs integration-specific issues.

####### Implementation Approach

Testing strategy uses `tempfile.TemporaryDirectory` for isolated file system operations and `asyncio.sleep()` for timestamp manipulation in freshness testing. Cache validation employs direct file system inspection of cache file locations and content verification through metadata delimiter checking. Mock LLM integration uses predefined response strings to simulate analysis generation without external dependencies. Performance testing creates multiple test files with systematic cache population and hit rate calculation. Error handling provides detailed failure context with expected vs actual value comparisons and cache statistics reporting.

######## Code Usage Examples

Execute the complete cache integration test suite. This validates all aspects of cache functionality from basic operations to performance optimization:

```python
# Run comprehensive cache integration tests
success = asyncio.run(run_all_cache_tests())
sys.exit(0 if success else 1)
```

Test basic cache storage and retrieval with metadata handling. This demonstrates fundamental cache operations and content validation:

```python
# Validate cache storage and retrieval functionality
cache = FileAnalysisCache(config)
test_analysis = "## Test Analysis\n\nThis is a test Python file that prints 'Hello World'."
await cache.cache_analysis(test_file, test_analysis, source_root)
retrieved_analysis = await cache.get_cached_analysis(test_file, source_root)
assert retrieved_analysis == test_analysis
```

Simulate cache freshness validation with file modification. This tests timestamp-based cache invalidation mechanisms:

```python
# Test cache invalidation after file modification
await cache.cache_analysis(test_file, original_analysis, source_root)
await asyncio.sleep(2)  # Ensure timestamp difference
test_file.write_text("# Modified content")
stale_retrieval = await cache.get_cached_analysis(test_file, source_root)
assert stale_retrieval is None  # Cache should be invalidated
```

######### External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.knowledge_bases.indexing.knowledge_builder:KnowledgeBuilder` - primary integration target for cache functionality
- `jesse_framework_mcp.knowledge_bases.indexing.file_analysis_cache:FileAnalysisCache` - core caching system under test
- `jesse_framework_mcp.knowledge_bases.models.indexing_config:IndexingConfig` - configuration management for cache behavior
- `jesse_framework_mcp.knowledge_bases.models.knowledge_context:FileContext` - file processing context objects
- `jesse_framework_mcp.knowledge_bases.models.knowledge_context:ProcessingStatus` - processing status enumeration
- `jesse_framework_mcp.llm.strands_agent_driver:StrandsClaude4Driver` - LLM driver integration (mocked in tests)
- `tempfile` (standard library) - temporary directory creation for isolated testing
- `asyncio` (standard library) - async test execution and timing control
- `pathlib.Path` (standard library) - cross-platform path manipulation
- `datetime` (standard library) - timestamp handling for freshness validation

**← Outbound:**
- `console/stdout` - detailed test results and progress reporting
- `CI/CD pipelines` - test success/failure status through exit codes
- `development workflows/` - cache integration validation for knowledge building systems
- `performance benchmarks/` - cache hit rate metrics and optimization validation

**⚡ Integration:**
- Protocol: Direct Python imports with async/await patterns and file system operations
- Interface: Class instantiation, async method calls, and file system interactions
- Coupling: Tight coupling with FileAnalysisCache and loose coupling with external LLM services

########## Edge Cases & Error Handling

Handles missing cache files gracefully by returning `None` from `get_cached_analysis()` calls and validating proper cache miss behavior. Manages file modification scenarios with timestamp tolerance configuration and sleep-based timing control for reliable freshness testing. Addresses temporary directory cleanup through context manager patterns and exception handling for file system operations. Provides comprehensive test failure reporting with cache statistics, file content previews, and detailed error context for debugging. Implements graceful degradation for mock LLM failures and validates cache behavior under various error conditions.

########### Internal Implementation Details

Uses emoji-based visual feedback system (✅, ❌, 💥) for immediate test status recognition and detailed progress reporting. Implements cache file structure validation through metadata delimiter checking and content length verification. Employs systematic test result tracking with boolean accumulation and percentage-based success rate calculation. Cache statistics reporting includes file count metrics and hit rate analysis for performance validation. Test orchestration uses exception handling with detailed error context and maintains test isolation through separate temporary directories for each test scenario.
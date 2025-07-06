<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/tests/test_file_analysis_cache_integration.py -->
<!-- Cached On: 2025-07-06T19:37:59.335337 -->
<!-- Source Modified: 2025-07-05T18:03:27.972527 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This comprehensive test suite validates the `FileAnalysisCache` integration within the JESSE Framework MCP Server knowledge building system, specifically designed to verify cache-first processing, metadata stripping, freshness checking, and performance optimization capabilities. The test suite provides extensive validation for cache storage and retrieval, timestamp-based staleness detection, and seamless integration with the knowledge building workflow. Key semantic entities include `FileAnalysisCache`, `KnowledgeBuilder`, `IndexingConfig`, `FileContext`, `ProcessingStatus`, `MockContext`, `MockKnowledgeBuilder`, `test_cache_basic_functionality`, `test_cache_freshness_checking`, `test_cache_integration_with_knowledge_builder`, `test_cache_performance_simulation`, `StrandsClaude4Driver`, `Claude4SonnetConfig`, `OutputConfig`, `ChangeDetectionConfig`, `LLMConfig`, `DebugConfig`, `METADATA_START`, `METADATA_END` delimiters, and `asyncio` async execution patterns. The testing framework implements four-phase validation through basic functionality testing, freshness checking validation, knowledge builder integration testing, and performance simulation with multiple file scenarios.

##### Main Components

The test suite contains four primary async test functions: `test_cache_basic_functionality()` implementing cache storage, retrieval, and metadata validation, `test_cache_freshness_checking()` validating timestamp-based cache invalidation, `test_cache_integration_with_knowledge_builder()` testing end-to-end integration with mock LLM responses, and `test_cache_performance_simulation()` demonstrating cache hit rate optimization across multiple files. The `MockContext` class provides simplified logging without actual LLM integration, while `MockKnowledgeBuilder` extends `KnowledgeBuilder` with simulated LLM responses for realistic testing. The `run_all_cache_tests()` function orchestrates sequential test execution with comprehensive result reporting and success rate calculation.

###### Architecture & Design

The architecture follows a comprehensive testing pattern with isolated test functions for different cache integration aspects, utilizing temporary directory structures and realistic file scenarios for validation. The design implements mock-based testing through `MockKnowledgeBuilder` to simulate LLM interactions without external API dependencies, enabling reliable and fast test execution. Error handling is structured with assertion-based validation and detailed console output for debugging. The testing framework uses realistic file content and directory structures combined with actual `FileAnalysisCache` and `KnowledgeBuilder` integration to validate end-to-end caching behavior.

####### Implementation Approach

The implementation uses temporary directory creation with `tempfile.TemporaryDirectory()` for isolated testing environments and realistic file system operations. Cache testing employs direct method calls to `get_cached_analysis()`, `cache_analysis()`, and `get_cache_stats()` for targeted validation. Mock LLM integration uses class inheritance with `MockKnowledgeBuilder` overriding `_process_single_file()` to provide deterministic responses. The testing strategy implements both positive path validation and edge case testing through file modification scenarios, cache invalidation testing, and performance measurement with multiple file processing cycles.

######## External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.knowledge_bases.indexing.knowledge_builder:KnowledgeBuilder` - primary knowledge building class
- `jesse_framework_mcp.knowledge_bases.indexing.file_analysis_cache:FileAnalysisCache` - cache implementation
- `jesse_framework_mcp.knowledge_bases.models.indexing_config:IndexingConfig` - configuration management
- `jesse_framework_mcp.knowledge_bases.models.indexing_config:OutputConfig` - output configuration
- `jesse_framework_mcp.knowledge_bases.models.indexing_config:ChangeDetectionConfig` - change detection settings
- `jesse_framework_mcp.knowledge_bases.models.indexing_config:LLMConfig` - LLM configuration
- `jesse_framework_mcp.knowledge_bases.models.indexing_config:DebugConfig` - debug configuration
- `jesse_framework_mcp.knowledge_bases.models.knowledge_context:FileContext` - file context modeling
- `jesse_framework_mcp.knowledge_bases.models.knowledge_context:ProcessingStatus` - processing status tracking
- `jesse_framework_mcp.llm.strands_agent_driver:StrandsClaude4Driver` - LLM driver integration
- `jesse_framework_mcp.llm.strands_agent_driver:Claude4SonnetConfig` - LLM configuration
- `asyncio` (external library) - async execution framework
- `tempfile` (external library) - temporary directory and file management
- `pathlib:Path` (external library) - cross-platform path manipulation
- `datetime` (external library) - timestamp handling for cache freshness validation

**← Outbound:**
- Console test output with detailed cache validation reporting
- Test result validation for cache integration functionality
- Performance metrics for cache hit rate optimization
- Exit code reporting for CI/CD pipeline integration

**⚡ System role and ecosystem integration:**
- **System Role**: Comprehensive validation component ensuring FileAnalysisCache reliability and performance optimization within the JESSE Framework MCP Server knowledge building ecosystem
- **Ecosystem Position**: Critical testing utility for cache integration functionality, validating the bridge between file analysis caching and knowledge building workflows with performance optimization
- **Integration Pattern**: Executed by developers and CI/CD systems to verify cache-first processing behavior, metadata handling, and performance benefits before knowledge building system deployment

######### Edge Cases & Error Handling

Error handling covers temporary directory creation failures with automatic cleanup, cache file access permission issues, and timestamp tolerance validation for freshness checking. The test suite handles file modification scenarios through sleep delays and timestamp comparison validation, ensuring cache invalidation works correctly. Edge cases include missing cache files with null return validation, metadata delimiter presence verification, content stripping accuracy, and cache statistics validation. The testing framework provides comprehensive error scenario coverage through assertion-based validation, detailed console output for debugging, and graceful handling of mock LLM response variations.

########## Internal Implementation Details

Cache functionality testing uses direct file system operations with temporary directories and realistic file content creation. Freshness checking employs `asyncio.sleep()` for timestamp manipulation and file modification simulation. Mock LLM integration overrides `_process_single_file()` method with predetermined responses while maintaining actual cache integration behavior. Performance testing creates multiple files with iterative processing cycles to measure cache hit rates and validate optimization benefits. Test orchestration uses tuple-based test definition with function references and comprehensive result aggregation through success rate calculation.

########### Code Usage Examples

**Basic cache functionality testing with storage and retrieval:**

This example demonstrates how to test fundamental cache operations including storage, retrieval, and metadata handling. The test validates that cache files are created in correct locations with proper metadata delimiters.

```python
# Test basic cache storage and retrieval functionality
cache = FileAnalysisCache(config)
test_analysis = "## Test Analysis\n\nThis is a test Python file analysis."
await cache.cache_analysis(test_file, test_analysis, source_root)
retrieved_analysis = await cache.get_cached_analysis(test_file, source_root)
assert retrieved_analysis == test_analysis
```

**Cache freshness validation with file modification scenarios:**

This snippet shows how to test cache invalidation based on file timestamps and modification detection. The test verifies that modified files correctly invalidate cached analysis results.

```python
# Test cache freshness checking with file modification
await cache.cache_analysis(test_file, original_analysis, source_root)
await asyncio.sleep(2)  # Ensure timestamp difference
test_file.write_text("# Modified content")
stale_retrieval = await cache.get_cached_analysis(test_file, source_root)
assert stale_retrieval is None  # Cache should be invalidated
```

**Mock knowledge builder integration with cache validation:**

This example demonstrates how to test cache integration with knowledge building workflows using mock LLM responses. The test validates that cache hits and misses are handled correctly during file processing.

```python
# Test knowledge builder integration with cache-first processing
class MockKnowledgeBuilder(KnowledgeBuilder):
    async def _process_single_file(self, file_path, content, ctx, source_root=None):
        cached_analysis = await self.analysis_cache.get_cached_analysis(file_path, source_root)
        if cached_analysis:
            await ctx.info(f"📄 CACHE HIT: Using cached analysis for {file_path.name}")
            return cached_analysis
        return self._mock_llm_response
```
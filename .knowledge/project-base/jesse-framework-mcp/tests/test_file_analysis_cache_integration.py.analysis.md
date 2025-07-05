<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/tests/test_file_analysis_cache_integration.py -->
<!-- Cached On: 2025-07-05T11:37:02.192687 -->
<!-- Source Modified: 2025-07-03T16:30:11.962937 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This test script validates the `FileAnalysisCache` integration with the JESSE Framework knowledge building system, specifically testing cache-first processing, metadata stripping, freshness checking, and performance optimization for LLM-generated file analyses. The script provides comprehensive validation of cache storage/retrieval, timestamp-based staleness detection, KnowledgeBuilder integration, and performance benefits through cache hit simulation. Key semantic entities include `FileAnalysisCache`, `KnowledgeBuilder`, `IndexingConfig`, `FileContext`, `ProcessingStatus`, `MockContext`, `MockKnowledgeBuilder`, `test_cache_basic_functionality()`, `test_cache_freshness_checking()`, `test_cache_integration_with_knowledge_builder()`, `test_cache_performance_simulation()`, `METADATA_START`, `METADATA_END`, `get_cached_analysis()`, `cache_analysis()`, `get_cache_path()`, `get_cache_stats()`, `tempfile.TemporaryDirectory`, `asyncio` async execution, and `.knowledge/` directory structure. The testing framework enables developers to verify that file analysis caching reduces LLM API calls, maintains content freshness, and integrates seamlessly with the knowledge building pipeline.

##### Main Components

The script contains four primary async test functions: `test_cache_basic_functionality()` for validating cache storage, retrieval, and metadata handling, `test_cache_freshness_checking()` for timestamp-based staleness detection, `test_cache_integration_with_knowledge_builder()` for end-to-end KnowledgeBuilder integration with mock LLM responses, and `test_cache_performance_simulation()` for multi-file cache hit rate validation. The `MockContext` class provides logging simulation for testing, while `MockKnowledgeBuilder` extends `KnowledgeBuilder` to simulate LLM responses without API calls. The `run_all_cache_tests()` function orchestrates sequential test execution with comprehensive result reporting and performance metrics.

###### Architecture & Design

The test architecture follows a comprehensive integration testing pattern where cache functionality is validated at multiple levels: basic operations, freshness logic, KnowledgeBuilder integration, and performance simulation. The design implements temporary directory isolation using `tempfile.TemporaryDirectory` for clean test environments and realistic file structure simulation. The script uses mock inheritance patterns with `MockKnowledgeBuilder` extending the real `KnowledgeBuilder` to test actual integration points while avoiding external API dependencies. Error handling is implemented through boolean return values with detailed diagnostic output for debugging cache behavior and integration issues.

####### Implementation Approach

The testing strategy employs realistic file structure creation with TypeScript/React components for authentic cache testing scenarios. Cache validation uses direct file system verification of cache file creation at expected paths (`knowledge_dir / "project-base" / "components" / "Button.tsx.analysis.md"`). Freshness testing implements controlled timestamp manipulation using `asyncio.sleep(2)` delays and file modification to trigger staleness detection. Performance simulation creates multiple test files with mock analyses to validate cache hit rates and storage efficiency. The implementation includes comprehensive metadata validation using `METADATA_START` and `METADATA_END` delimiter checking.

######## External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.knowledge_bases.indexing.knowledge_builder:KnowledgeBuilder` - primary knowledge building system
- `jesse_framework_mcp.knowledge_bases.indexing.file_analysis_cache:FileAnalysisCache` - cache system under test
- `jesse_framework_mcp.knowledge_bases.models.indexing_config:IndexingConfig` - configuration management
- `jesse_framework_mcp.knowledge_bases.models.knowledge_context:FileContext` - file processing context
- `jesse_framework_mcp.knowledge_bases.models.knowledge_context:ProcessingStatus` - processing state enumeration
- `jesse_framework_mcp.llm.strands_agent_driver:StrandsClaude4Driver` - LLM driver integration
- `jesse_framework_mcp.llm.strands_agent_driver:Claude4SonnetConfig` - LLM configuration
- `tempfile` (stdlib) - temporary directory management for test isolation
- `asyncio` (stdlib) - async execution framework
- `pathlib.Path` (stdlib) - cross-platform path operations
- `datetime` (stdlib) - timestamp manipulation for freshness testing

**← Outbound:**
- Test execution reports consumed by developers and CI/CD pipelines
- Console output with detailed cache behavior diagnostics
- Exit codes for automated testing pipeline integration
- Cache performance metrics for optimization validation

**⚡ System role and ecosystem integration:**
- **System Role**: Critical validation component ensuring FileAnalysisCache integration functions correctly within JESSE Framework knowledge building pipeline
- **Ecosystem Position**: Core testing infrastructure for cache-first processing validation and LLM API optimization verification
- **Integration Pattern**: Executed by developers during development, CI/CD pipelines for automated cache validation, and performance regression testing for knowledge building optimization

######### Edge Cases & Error Handling

The script handles multiple edge cases including cache file creation failures, timestamp tolerance edge cases with `timestamp_tolerance_seconds=1`, file modification during processing, missing cache directories, and metadata delimiter validation failures. Exception handling includes comprehensive error catching with detailed diagnostic output for cache misses, staleness detection failures, and integration issues. The testing framework provides graceful handling of temporary directory cleanup failures and validates cache behavior when source files are modified between cache operations. Individual test isolation ensures that failures in one cache scenario do not prevent execution of subsequent validation tests.

########## Internal Implementation Details

The test functions implement emoji-based status reporting using Unicode characters (`✅`, `❌`, `🎉`, `💥`, `🧪`, `📊`) for immediate visual feedback on cache behavior. Cache validation includes direct file system verification of cache file creation, metadata delimiter presence checking, and content comparison with whitespace tolerance for minor formatting differences. Mock LLM response simulation uses predefined analysis content to test cache storage without external API dependencies. The script uses controlled timestamp manipulation and file modification to trigger cache staleness detection with precise timing control through `asyncio.sleep()` delays.

########### Code Usage Examples

**Basic cache storage and retrieval validation pattern:**

This code demonstrates the fundamental cache operations testing approach with file creation and analysis storage. It validates that cache files are created in the correct directory structure and content is retrievable without metadata contamination.

```python
# Test basic cache functionality with temporary directory isolation
with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)
    knowledge_dir = temp_path / ".knowledge"
    source_root = temp_path / "project"
    test_file = source_root / "src" / "test.py"
    
    config = IndexingConfig(knowledge_output_directory=knowledge_dir)
    cache = FileAnalysisCache(config)
    
    test_analysis = "## Test Analysis\n\nThis is a test Python file analysis."
    await cache.cache_analysis(test_file, test_analysis, source_root)
    retrieved_analysis = await cache.get_cached_analysis(test_file, source_root)
```

**Cache freshness validation with timestamp manipulation:**

This pattern tests cache staleness detection by modifying files after caching and verifying that stale cache entries return None. It ensures that cache freshness checking works correctly with configurable timestamp tolerance.

```python
# Test cache freshness with controlled file modification timing
config = IndexingConfig(timestamp_tolerance_seconds=1)
cache = FileAnalysisCache(config)

await cache.cache_analysis(test_file, original_analysis, source_root)
await asyncio.sleep(2)  # Ensure timestamp difference
test_file.write_text("# Modified content")

stale_retrieval = await cache.get_cached_analysis(test_file, source_root)
if stale_retrieval is None:
    print("✅ Modified file correctly invalidated cache")
```

**KnowledgeBuilder integration testing with mock LLM responses:**

This approach demonstrates end-to-end cache integration testing by extending KnowledgeBuilder with mock responses. It validates that cache hits and misses work correctly within the actual knowledge building pipeline without requiring external API calls.

```python
# Mock KnowledgeBuilder for integration testing without API calls
class MockKnowledgeBuilder(KnowledgeBuilder):
    async def _process_single_file(self, file_path: Path, content: str, ctx, source_root=None) -> str:
        cached_analysis = await self.analysis_cache.get_cached_analysis(file_path, source_root)
        if cached_analysis:
            await ctx.info(f"📄 CACHE HIT: Using cached analysis for {file_path.name}")
            return cached_analysis
        
        await ctx.info(f"🤖 CACHE MISS: Generating mock analysis for {file_path.name}")
        await self.analysis_cache.cache_analysis(file_path, mock_response, source_root)
        return mock_response
```
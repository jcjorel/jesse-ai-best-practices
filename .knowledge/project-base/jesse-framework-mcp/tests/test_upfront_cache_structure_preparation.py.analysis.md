<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/tests/test_upfront_cache_structure_preparation.py -->
<!-- Cached On: 2025-07-05T11:40:21.576798 -->
<!-- Source Modified: 2025-07-03T16:56:08.413445 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This test script validates upfront cache structure preparation implementation for the JESSE Framework knowledge building system, specifically testing the `prepare_cache_structure()` method and its integration with the hierarchical indexer to eliminate race conditions during concurrent cache operations. The script provides comprehensive validation of cache directory pre-creation, race condition prevention, hierarchical indexer integration, and fallback behavior for on-demand directory creation. Key semantic entities include `FileAnalysisCache`, `HierarchicalIndexer`, `IndexingConfig`, `DirectoryContext`, `FileContext`, `ProcessingStatus`, `MockContext`, `MockKnowledgeBuilder`, `test_cache_structure_preparation()`, `test_hierarchical_indexer_integration()`, `test_fallback_behavior()`, `prepare_cache_structure()`, `get_cache_path()`, `cache_analysis()`, `get_cached_analysis()`, `_collect_all_files_recursive()`, `_discover_directory_structure()`, `tempfile.TemporaryDirectory`, `asyncio.gather()`, and `.knowledge/project-base/` cache directory structure. The testing framework enables developers to verify that cache directory structures are created upfront to prevent filesystem race conditions, ensure concurrent cache operations are safe, and validate seamless integration with the knowledge building pipeline.

##### Main Components

The script contains three primary async test functions: `test_cache_structure_preparation()` for validating basic cache structure pre-creation functionality, `test_hierarchical_indexer_integration()` for testing integration with the hierarchical indexer and concurrent operation safety, and `test_fallback_behavior()` for validating on-demand directory creation when structure preparation is bypassed. The `MockContext` class provides logging simulation with message tracking, while `MockKnowledgeBuilder` extends knowledge building functionality to simulate LLM operations without external API calls. The `create_directory_context()` helper function recursively builds `DirectoryContext` instances from file lists for realistic testing scenarios. The `run_all_tests()` function orchestrates sequential test execution with comprehensive result reporting and performance metrics.

###### Architecture & Design

The test architecture follows a comprehensive validation pattern where cache structure preparation is tested at multiple levels: basic functionality, integration with hierarchical processing, concurrent operation safety, and fallback behavior validation. The design implements isolated test environments using `tempfile.TemporaryDirectory` for clean filesystem testing and complex directory structure creation with nested subdirectories and files. The script uses mock inheritance patterns with `MockKnowledgeBuilder` to simulate knowledge building operations while testing cache structure preparation without external dependencies. Error handling and race condition detection employ message analysis and concurrent operation simulation using `asyncio.gather()` for parallel task execution.

####### Implementation Approach

The testing strategy employs complex directory structure creation with nested paths (`dir_i/subdir_j/file_k.py`) to simulate realistic project hierarchies and validate comprehensive cache directory preparation. Cache structure validation uses direct filesystem verification of expected cache directories based on source file paths and `get_cache_path()` resolution. Concurrent operation testing implements parallel cache operations using `asyncio.gather()` to simulate race conditions and validate thread-safe directory creation. The implementation includes recursive directory context building with parent-child relationship preservation and comprehensive error message analysis for race condition detection indicators.

######## External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.knowledge_bases.indexing.file_analysis_cache:FileAnalysisCache` - cache system with structure preparation
- `jesse_framework_mcp.knowledge_bases.indexing.hierarchical_indexer:HierarchicalIndexer` - hierarchical processing system
- `jesse_framework_mcp.knowledge_bases.models.indexing_config:IndexingConfig` - configuration management
- `jesse_framework_mcp.knowledge_bases.models.knowledge_context:DirectoryContext` - directory processing context
- `jesse_framework_mcp.knowledge_bases.models.knowledge_context:FileContext` - file processing context
- `jesse_framework_mcp.knowledge_bases.models.knowledge_context:ProcessingStatus` - processing state enumeration
- `tempfile` (stdlib) - temporary directory management for test isolation
- `asyncio` (stdlib) - async execution framework and concurrent operation testing
- `pathlib.Path` (stdlib) - cross-platform path operations and filesystem access
- `datetime` (stdlib) - timestamp generation for context creation

**← Outbound:**
- Test execution reports consumed by developers and CI/CD pipelines
- Console output with detailed cache structure preparation diagnostics
- Exit codes for automated testing pipeline integration
- Race condition prevention validation results for concurrent operation safety

**⚡ System role and ecosystem integration:**
- **System Role**: Critical validation component ensuring upfront cache structure preparation eliminates race conditions within JESSE Framework knowledge building pipeline
- **Ecosystem Position**: Core testing infrastructure for cache directory pre-creation validation and concurrent operation safety verification
- **Integration Pattern**: Executed by developers during development, CI/CD pipelines for automated cache structure validation, and performance regression testing for concurrent operation reliability

######### Edge Cases & Error Handling

The script handles multiple edge cases including missing cache directories (validated through initial state verification), concurrent directory creation attempts (tested through parallel `asyncio.gather()` operations), filesystem permission issues (graceful handling during cleanup), and fallback scenarios when structure preparation is bypassed (on-demand directory creation validation). Exception handling includes comprehensive error message analysis for race condition indicators (`FileExistsError`, `directory exists`, `cannot create directory`, `race condition`, `concurrent access`) and detailed validation of cache operation success after concurrent execution. The testing framework provides graceful handling of temporary directory cleanup failures and validates that cache operations work correctly both with pre-created structures and on-demand creation scenarios.

########## Internal Implementation Details

The test functions implement comprehensive validation using assertion-based testing with detailed filesystem state verification and concurrent operation simulation. Cache structure validation includes direct directory existence checking, expected directory set calculation based on file paths, and verification that all necessary cache directories are created before cache operations begin. Mock object creation uses simple class definitions for context simulation and knowledge builder mocking without complex external dependencies. The script includes recursive directory context building with proper parent-child relationship preservation and comprehensive message analysis for race condition detection across multiple concurrent operations.

########### Code Usage Examples

**Basic cache structure preparation with comprehensive validation:**

This code demonstrates the fundamental approach for testing upfront cache structure preparation. It validates that all necessary cache directories are created before any cache operations begin, eliminating potential race conditions.

```python
# Test comprehensive cache structure preparation with complex directory hierarchy
config = IndexingConfig(
    knowledge_output_directory=knowledge_dir,
    enable_project_base_indexing=True
)
cache = FileAnalysisCache(config)
root_context = await create_directory_context(source_root, files_created)

# Prepare cache structure upfront
await cache.prepare_cache_structure(root_context, source_root, ctx)

# Verify all expected directories were created
all_files = cache._collect_all_files_recursive(root_context)
expected_dirs = {cache.get_cache_path(file_path, source_root).parent for file_path in all_files}
missing_dirs = [dir for dir in expected_dirs if not dir.exists()]
assert len(missing_dirs) == 0, f"Missing cache directories: {missing_dirs}"
```

**Concurrent operation safety testing with race condition detection:**

This pattern demonstrates testing concurrent cache operations to validate that upfront structure preparation eliminates race conditions. It uses parallel task execution to simulate realistic concurrent scenarios.

```python
# Test concurrent cache operations safety after structure preparation
async def concurrent_cache_operation(file_path, analysis_content):
    await indexer.knowledge_builder.analysis_cache.cache_analysis(
        file_path, analysis_content, source_root
    )

# Execute multiple concurrent cache operations
tasks = [concurrent_cache_operation(file, f"Analysis {i}") for i, file in enumerate(test_files)]
await asyncio.gather(*tasks)

# Verify no race condition errors occurred
race_indicators = ["FileExistsError", "directory exists", "race condition"]
race_errors = [msg for msg in ctx.messages if any(indicator in msg for indicator in race_indicators)]
assert len(race_errors) == 0, f"Race condition errors detected: {race_errors}"
```

**Fallback behavior validation for on-demand directory creation:**

This approach demonstrates testing the fallback mechanism when cache structure preparation is bypassed. It validates that cache operations still work correctly through on-demand directory creation.

```python
# Test fallback behavior with on-demand directory creation
cache = FileAnalysisCache(config)
test_analysis = "## Fallback Test\n\nThis tests on-demand directory creation."

# Cache operation without prior structure preparation (should create directories on-demand)
await cache.cache_analysis(test_file, test_analysis, source_root)

# Verify cache file was created successfully
cache_path = cache.get_cache_path(test_file, source_root)
assert cache_path.exists(), "Cache file should exist after on-demand creation"
retrieved_analysis = await cache.get_cached_analysis(test_file, source_root)
assert retrieved_analysis == test_analysis, "Retrieved analysis should match"
```
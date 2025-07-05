<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/tests/test_upfront_cache_structure_preparation.py -->
<!-- Cached On: 2025-07-05T20:18:58.941158 -->
<!-- Source Modified: 2025-07-05T18:10:04.901167 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This test script validates upfront cache structure preparation implementation for the Jesse Framework MCP system, specifically testing the `prepare_cache_structure` method and its integration with `HierarchicalIndexer`. The script provides comprehensive validation of race condition elimination, concurrent cache operations safety, and fallback behavior mechanisms. Key semantic entities include `FileAnalysisCache`, `HierarchicalIndexer`, `IndexingConfig`, `DirectoryContext`, `FileContext`, `ProcessingStatus`, `MockContext`, `MockKnowledgeBuilder`, `tempfile`, `asyncio`, `pathlib.Path`, and `datetime`. The testing framework validates upfront directory creation, concurrent operation safety, hierarchical indexer integration, and on-demand fallback directory creation when structure preparation fails.

##### Main Components

The script contains three primary test functions: `test_cache_structure_preparation()` validates basic cache structure preparation functionality, `test_hierarchical_indexer_integration()` tests integration with the hierarchical indexer including concurrent operations, and `test_fallback_behavior()` validates on-demand directory creation when preparation fails. Supporting components include `MockContext` class for async logging simulation, `MockKnowledgeBuilder` class for avoiding actual LLM calls during testing, `create_directory_context()` helper function for building directory structures from file lists, and `run_all_tests()` orchestration function for comprehensive test execution.

###### Architecture & Design

The testing architecture follows an isolated environment pattern using `tempfile.TemporaryDirectory()` for each test scenario, ensuring no cross-test contamination. The design validates upfront cache structure preparation by creating complex directory hierarchies with nested subdirectories and multiple files per directory. The `MockKnowledgeBuilder` replaces actual LLM processing to focus purely on cache structure mechanics. Each test creates realistic project structures with multiple levels of nesting to validate comprehensive directory preparation and concurrent access patterns.

####### Implementation Approach

The implementation uses recursive directory context building through the `create_directory_context()` helper function that processes file lists into hierarchical `DirectoryContext` structures. Tests validate cache structure preparation by creating complex nested directories (`dir_0/subdir_0`, `dir_1/subdir_1`, etc.) and verifying all necessary cache directories are created upfront. Concurrent safety testing uses `asyncio.gather()` to execute multiple cache operations simultaneously, validating race condition prevention. The approach includes fallback testing where cache operations work without upfront preparation through on-demand directory creation.

######## External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.knowledge_bases.indexing.file_analysis_cache:FileAnalysisCache` - cache structure preparation testing
- `jesse_framework_mcp.knowledge_bases.indexing.hierarchical_indexer:HierarchicalIndexer` - integration validation
- `jesse_framework_mcp.knowledge_bases.models.indexing_config:IndexingConfig` - configuration model testing
- `jesse_framework_mcp.knowledge_bases.models.knowledge_context:DirectoryContext` - context structure validation
- `tempfile` (standard library) - isolated test environment creation
- `asyncio` (standard library) - concurrent operation testing framework
- `pathlib.Path` (standard library) - file system path manipulation

**← Outbound:**
- Test execution results consumed by CI/CD validation systems
- Cache structure validation reports for deployment verification
- Concurrent operation safety metrics for performance monitoring

**⚡ System role and ecosystem integration:**
- **System Role**: Critical validation component ensuring cache structure preparation eliminates race conditions and enables safe concurrent operations in the Jesse Framework MCP knowledge base system
- **Ecosystem Position**: Core testing infrastructure validating the foundation of cache directory management and concurrent access safety
- **Integration Pattern**: Executed by developers and CI systems to validate cache structure reliability before deployment, ensuring hierarchical indexer can safely perform concurrent operations

######### Edge Cases & Error Handling

The tests validate missing cache directories scenarios (should create upfront), concurrent cache operations (should not cause race conditions), hierarchical indexer integration (should prepare structure before processing), and fallback behavior when preparation fails (should create directories on-demand). Error handling includes assertion failures with descriptive messages for missing directories, race condition detection through error message analysis, exception catching with detailed reporting, and comprehensive test result summaries with pass/fail statistics. The tests specifically check for `FileExistsError`, directory creation failures, and concurrent access indicators.

########## Internal Implementation Details

Internal mechanisms include complex directory structure creation with nested loops generating `dir_{i}/subdir_{j}/file_{k}.py` patterns, recursive directory context building that processes file lists into hierarchical structures, and concurrent operation simulation using `asyncio.gather()` for race condition testing. The `MockKnowledgeBuilder` provides realistic processing simulation without LLM calls, while cache path validation ensures all expected directories exist after preparation. Performance measurement tracks directory creation counts and validates cache operation success rates across concurrent executions.

########### Code Usage Examples

Essential cache structure preparation pattern for upfront directory creation:

```python
# This pattern demonstrates upfront cache structure preparation to eliminate race conditions during concurrent operations
# The preparation phase creates all necessary cache directories before any file processing begins
cache = FileAnalysisCache(config)
root_context = await create_directory_context(source_root, files_created)

# Prepare all cache directories upfront
await cache.prepare_cache_structure(root_context, source_root, ctx)

# Verify cache root and subdirectories exist
cache_root = knowledge_dir / "project-base"
assert cache_root.exists(), "Cache root should exist after preparation"
```

Concurrent cache operations safety validation:

```python
# This pattern validates that concurrent cache operations work safely after structure preparation
# Multiple async operations can execute simultaneously without race conditions
async def concurrent_cache_operation(file_path, analysis_content):
    await indexer.knowledge_builder.analysis_cache.cache_analysis(
        file_path, analysis_content, source_root
    )

# Execute multiple concurrent cache operations
tasks = []
for i, test_file in enumerate(test_files):
    task = concurrent_cache_operation(test_file, f"Concurrent analysis {i}")
    tasks.append(task)

await asyncio.gather(*tasks)
```

Directory context creation helper for testing:

```python
# This helper function builds hierarchical DirectoryContext structures from file lists
# It recursively processes directories and creates proper context relationships
def build_directory_context(current_path: Path) -> DirectoryContext:
    file_contexts = []
    subdirectory_contexts = []
    processed_subdirs = set()
    
    # Find files directly in this directory
    for file_path in files:
        if file_path.parent == current_path:
            file_context = FileContext(
                file_path=file_path,
                file_size=file_path.stat().st_size,
                last_modified=datetime.fromtimestamp(file_path.stat().st_mtime)
            )
            file_contexts.append(file_context)
```
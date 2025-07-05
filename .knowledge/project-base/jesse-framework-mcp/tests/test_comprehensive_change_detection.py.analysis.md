<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/tests/test_comprehensive_change_detection.py -->
<!-- Cached On: 2025-07-05T20:18:12.938712 -->
<!-- Source Modified: 2025-07-05T18:06:16.556812 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This test script validates comprehensive change detection enhancements for the Jesse Framework MCP system, specifically testing enhanced constituent dependency checking for directory knowledge files. The script provides comprehensive validation of `FileAnalysisCache` staleness detection, `ChangeDetector` functionality, and hierarchical dependency propagation mechanisms. Key semantic entities include `FileAnalysisCache`, `ChangeDetector`, `IndexingConfig`, `DirectoryContext`, `FileContext`, `ProcessingStatus`, `MockContext`, `tempfile`, `asyncio`, `pathlib.Path`, `datetime`, and `timedelta`. The testing framework validates timestamp-based staleness detection, cached analysis propagation, subdirectory knowledge file dependencies, and performance optimization through smart change detection algorithms.

##### Main Components

The script contains five primary test functions: `test_file_analysis_cache_staleness_checking()` validates comprehensive staleness checking methods, `test_detailed_staleness_info()` tests detailed staleness information gathering, `test_change_detector_enhancements()` validates enhanced `ChangeDetector` functionality, `test_realistic_change_scenarios()` tests real-world development scenarios, and `test_performance_optimization()` measures performance benefits. Supporting components include `MockContext` class for testing context simulation, `create_directory_context()` helper function for test data creation, and `run_all_tests()` orchestration function for comprehensive test execution.

###### Architecture & Design

The testing architecture follows a hierarchical validation pattern with isolated test environments using `tempfile.TemporaryDirectory()` for each test scenario. The design implements layered processing validation where source file changes do not directly trigger knowledge file rebuilds, ensuring proper separation of concerns. Each test creates realistic project structures with multiple directories, files, and knowledge bases to validate constituent dependency relationships. The `MockContext` class provides async logging simulation for testing framework integration without external dependencies.

####### Implementation Approach

The implementation uses timestamp-based staleness detection with configurable tolerance (`timestamp_tolerance_seconds=0.05`) for precise change detection testing. Tests create realistic file hierarchies, modify timestamps through `time.sleep()` calls, and validate staleness propagation through cached analyses and subdirectory knowledge files. The approach validates that source file modifications trigger cached analysis updates, which then propagate to knowledge file rebuilds through hierarchical dependency chains. Performance testing measures detection times across moderate-sized project structures to validate optimization benefits.

######## External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.knowledge_bases.indexing.file_analysis_cache:FileAnalysisCache` - core caching functionality testing
- `jesse_framework_mcp.knowledge_bases.indexing.change_detector:ChangeDetector` - change detection validation
- `jesse_framework_mcp.knowledge_bases.models.indexing_config:IndexingConfig` - configuration model testing
- `jesse_framework_mcp.knowledge_bases.models.knowledge_context:DirectoryContext` - context model validation
- `tempfile` (standard library) - isolated test environment creation
- `asyncio` (standard library) - async test execution framework
- `pathlib.Path` (standard library) - file system path manipulation

**← Outbound:**
- Test execution results consumed by CI/CD validation systems
- Performance metrics output for optimization tracking
- Validation reports for constituent dependency checking verification

**⚡ System role and ecosystem integration:**
- **System Role**: Critical validation component ensuring constituent dependency checking works correctly across the Jesse Framework MCP knowledge base system
- **Ecosystem Position**: Core testing infrastructure validating the foundation of change detection and caching mechanisms
- **Integration Pattern**: Executed by developers and CI systems to validate knowledge base indexing reliability before deployment

######### Edge Cases & Error Handling

The tests validate missing knowledge file scenarios (should be stale), up-to-date knowledge file detection (should not be stale), source file modification impact (should not directly trigger rebuilds due to layered processing), cached analysis newer than knowledge files (should trigger rebuilds), and subdirectory knowledge files newer than parent directories (should trigger parent rebuilds). Error handling includes assertion failures with descriptive messages, exception catching with traceback printing, and comprehensive test result reporting with pass/fail statistics.

########## Internal Implementation Details

Internal mechanisms include `timestamp_tolerance_seconds=0.05` for precise timing control, `time.sleep(0.1)` calls to ensure proper timestamp ordering, temporary directory cleanup through context managers, and realistic project structure creation with multiple file types. The `MockContext` class captures logging messages for validation, while helper functions like `create_directory_context()` generate proper test data structures. Performance measurement uses `time.time()` for execution timing and calculates performance ratios between different scenarios.

########### Code Usage Examples

Essential test execution pattern for validating change detection:

```python
# Create test environment with proper configuration
with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)
    knowledge_dir = temp_path / ".knowledge"
    source_root = temp_path / "project"
    
    # Configure with small tolerance for testing
    output_config = OutputConfig(knowledge_output_directory=knowledge_dir)
    change_detection = ChangeDetectionConfig(timestamp_tolerance_seconds=0.05)
    config = IndexingConfig(
        handler_type="project-base",
        description="Test configuration for change detection",
        output_config=output_config,
        change_detection=change_detection
    )
```

Staleness checking validation pattern:

```python
# Test staleness detection with file contexts
cache = FileAnalysisCache(config)
file_contexts = [
    FileContext(
        file_path=file1,
        file_size=file1.stat().st_size,
        last_modified=datetime.fromtimestamp(file1.stat().st_mtime)
    )
]

is_stale, reason = cache.is_knowledge_file_stale(
    source_root / "src", source_root, file_contexts
)
assert is_stale == True, "Should be stale when knowledge file missing"
```

Comprehensive change detection testing:

```python
# Validate comprehensive directory change detection
detector = ChangeDetector(config)
directory_context = DirectoryContext(
    directory_path=source_root / "app",
    file_contexts=file_contexts
)

change_info = await detector.check_comprehensive_directory_change(
    directory_context, source_root, ctx
)
assert change_info is not None, "Should detect change when knowledge file missing"
```
<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/tests/test_project_base_indexing_rule.py -->
<!-- Cached On: 2025-07-04T00:29:32.214286 -->
<!-- Source Modified: 2025-07-03T16:02:35.983886 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This integration test validates the JESSE Framework's hierarchical knowledge indexing system through real-world project complexity testing, providing comprehensive verification of the `HierarchicalIndexer` class functionality against actual project structures and files. The script enables developers to verify system robustness, error handling, and performance characteristics through automated integration testing that examines `index_hierarchy()` method execution, `IndexingConfig` parameter validation, and `ProcessingStatus` result analysis. Key semantic entities include `HierarchicalIndexer` core indexing engine, `IndexingConfig` with `IndexingMode.INCREMENTAL` settings, `MockContext` for message capture, `ensure_project_root()` project detection, `ProcessingStatus.COMPLETED` validation, debug output directory management, and comprehensive success criteria analysis including file processing statistics and error rate monitoring.

##### Main Components

The script contains two primary async functions: `test_real_project_indexing()` which creates comprehensive integration testing by executing actual project indexing with real file structures, configuration validation, progress monitoring, and detailed result analysis; and `main()` which orchestrates test execution with clear pass/fail determination and debug artifact preservation. Supporting components include the `MockContext` class providing async logging interface simulation with categorized message collection (`info_messages`, `debug_messages`, `warning_messages`, `error_messages`), project structure analysis logic for file counting and directory exclusion validation, and comprehensive success criteria evaluation including processing statistics and debug file generation verification.

###### Architecture & Design

The script follows a real-world integration testing architecture that executes actual indexing operations against the live project structure rather than mock data. The design implements comprehensive monitoring through `MockContext` message capture, enabling detailed analysis of indexing behavior, error patterns, and performance characteristics. The architecture supports debug artifact preservation through dedicated debug directory creation, systematic success criteria evaluation, and detailed statistical analysis of processing results including file discovery rates, completion percentages, and error thresholds for realistic integration validation.

####### Implementation Approach

The implementation uses `ensure_project_root()` for dynamic project detection with comprehensive error handling for missing project environments. The script employs conservative configuration settings including `IndexingMode.INCREMENTAL`, moderate batch sizes, limited concurrency, and comprehensive debug output for stability during integration testing. Key technical strategies include real-time message capture through `MockContext` async methods, systematic project structure analysis with file counting and exclusion validation, comprehensive success criteria evaluation with configurable error thresholds, and debug directory preservation for post-test analysis and troubleshooting.

######## Code Usage Examples

Execute comprehensive integration testing against the actual project structure. This approach provides realistic validation of the indexing system's behavior with real-world complexity and file structures.

```python
# Run complete integration test with real project indexing
python test_project_indexing_integration.py

# Executes actual indexing against project files with comprehensive monitoring
# and generates detailed success/failure analysis with debug artifact preservation
```

Configure integration testing with custom parameters for specific validation scenarios. This method enables targeted testing of specific indexing configurations and performance characteristics.

```python
config = IndexingConfig(
    indexing_mode=IndexingMode.INCREMENTAL,
    enable_project_base_indexing=True,
    debug_mode=True,
    max_file_size=2 * 1024 * 1024,
    batch_size=5,
    max_concurrent_operations=2,
    continue_on_file_errors=True
)
indexer = HierarchicalIndexer(config)
result = await indexer.index_hierarchy(project_root, ctx)
```

Analyze integration test results with comprehensive success criteria evaluation. This verification provides detailed assessment of indexing performance and system reliability.

```python
success_criteria = {
    "Indexing completed": result.overall_status == ProcessingStatus.COMPLETED,
    "Files discovered": stats.total_files_discovered > 0,
    "Some files processed": stats.files_processed > 0,
    "No critical failure": len(ctx.error_messages) < stats.total_files_discovered
}
files_success_rate = (stats.files_completed / max(stats.total_files_discovered, 1)) * 100
integration_success = all_criteria_met and files_success_rate > 50
```

######### External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.knowledge_bases.indexing.hierarchical_indexer:HierarchicalIndexer` - core hierarchical indexing engine
- `jesse_framework_mcp.knowledge_bases.models.indexing_config:IndexingConfig` - indexing configuration model with `IndexingMode` enum
- `jesse_framework_mcp.knowledge_bases.models.knowledge_context:ProcessingStatus` - processing status enumeration for result validation
- `jesse_framework_mcp.helpers.path_utils:ensure_project_root` - project root detection and validation utility
- `asyncio` (stdlib) - async test execution and event loop management
- `tempfile` (stdlib) - temporary directory creation for debug output
- `pathlib.Path` (stdlib) - filesystem path operations and project structure analysis
- `datetime` (stdlib) - execution timing and duration measurement

**← Outbound:**
- `console/terminal` - comprehensive test output with progress monitoring and result analysis
- `/tmp/jesse_project_indexing_integration_test/` - debug artifact preservation directory
- `sys.exit()` - process exit codes for CI/CD integration (0 for success, 1 for failure)
- Debug files and processing artifacts for post-test analysis and troubleshooting

**⚡ Integration:**
- Protocol: Direct async method invocation with real project file processing
- Interface: `HierarchicalIndexer.index_hierarchy(project_root, context)` with `MockContext` simulation
- Coupling: Tight coupling to JESSE Framework indexing components, loose coupling to filesystem through debug directories

########## Edge Cases & Error Handling

The script handles missing project root scenarios through `ensure_project_root()` with comprehensive `ValueError` and generic exception catching, providing clear error messages for environment setup issues. Error handling includes systematic message categorization through `MockContext` with separate collections for info, debug, warning, and error messages, enabling detailed failure analysis. The script addresses integration test failures through comprehensive exception catching with traceback preservation, debug artifact preservation for post-failure analysis, and configurable success thresholds allowing partial failures while maintaining overall system validation.

########### Internal Implementation Details

The script uses `/tmp/jesse_project_indexing_integration_test` for debug output directory with automatic cleanup and recreation for consistent test environments. The `MockContext` class implements async logging methods (`info()`, `debug()`, `warning()`, `error()`) with real-time console output and message collection for comprehensive monitoring. Internal mechanics include project structure analysis with file counting and directory exclusion validation, systematic success criteria evaluation with configurable error thresholds (50% success rate minimum), and comprehensive statistical reporting including processing rates, completion percentages, and debug file generation verification. The integration test uses conservative configuration settings to ensure stability during real project processing while maintaining comprehensive validation coverage.
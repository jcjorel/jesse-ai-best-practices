<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/tests/test_project_indexing_integration.py -->
<!-- Cached On: 2025-07-04T00:28:58.601473 -->
<!-- Source Modified: 2025-07-03T23:00:13.434879 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This integration test validates the JESSE Framework's hierarchical knowledge indexing system by executing real-world project indexing operations on the actual project root, providing comprehensive verification of system functionality under authentic complexity conditions. The script enables developers to verify end-to-end indexing workflows, error handling robustness, and performance characteristics through automated testing that examines `HierarchicalIndexer` processing, `IndexingConfig` parameter validation, and `ProcessingStatus` result analysis. Key semantic entities include `asyncio` event loop management, `tempfile` temporary directory creation, `ensure_project_root()` project detection, `IndexingMode.INCREMENTAL` processing mode, `MockContext` message capture, `processing_stats` metrics collection, `debug_output_directory` artifact preservation, and comprehensive success criteria evaluation through file processing rates and error threshold analysis.

##### Main Components

The script contains three primary components: `MockContext` class which implements FastMCP context interface simulation with categorized message collection (`info_messages`, `debug_messages`, `warning_messages`, `error_messages`) and real-time console output for progress monitoring; `test_real_project_indexing()` async function which orchestrates comprehensive integration testing including project root detection, configuration setup, file structure analysis, indexing execution, and detailed result evaluation; and `main()` function providing test runner orchestration with clear pass/fail determination and debug artifact preservation. Supporting functionality includes project structure analysis with file counting and exclusion reporting, success criteria validation across multiple dimensions, and comprehensive error analysis with message categorization.

###### Architecture & Design

The script follows a comprehensive integration testing architecture with real project complexity validation rather than simplified mock scenarios. The design implements a message capture pattern using `MockContext` class that preserves all indexing system communications while providing real-time feedback through console output. The architecture emphasizes authentic testing conditions by targeting the actual project root with real file structures, using conservative configuration parameters for stability, and implementing comprehensive success criteria evaluation that accounts for partial failures while detecting critical system issues.

####### Implementation Approach

The implementation uses `ensure_project_root()` for dynamic project detection with comprehensive error handling for missing or invalid project environments. The script employs systematic project structure analysis through directory iteration with `config.should_process_directory()` and `config.should_process_file()` filtering to provide pre-indexing visibility into processing scope. Key technical strategies include conservative configuration with `IndexingMode.INCREMENTAL`, `max_concurrent_operations=2`, and `batch_size=5` for stability, comprehensive message capture through categorized lists, and multi-dimensional success evaluation including completion status, file processing rates, and error threshold analysis.

######## Code Usage Examples

Execute comprehensive real project integration testing with detailed monitoring:

```python
# Run complete integration test with real project complexity
python test_project_indexing_integration.py

# Provides comprehensive analysis of indexing system performance including
# file processing statistics, error analysis, and success criteria evaluation
```

Configure integration test parameters for specific testing scenarios:

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
# Conservative settings ensure stable testing while capturing debug information
```

Analyze integration test results programmatically:

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
- `jesse_framework_mcp.knowledge_bases.indexing.hierarchical_indexer:HierarchicalIndexer` - core indexing system execution
- `jesse_framework_mcp.knowledge_bases.models.indexing_config:IndexingConfig` - configuration management with `IndexingMode` enum
- `jesse_framework_mcp.knowledge_bases.models.knowledge_context:ProcessingStatus` - result status enumeration
- `jesse_framework_mcp.helpers.path_utils:ensure_project_root` - project root detection with error handling
- `asyncio` (stdlib) - async test execution and event loop management
- `tempfile` (stdlib) - temporary directory creation for debug output
- `shutil` (stdlib) - directory cleanup and management operations
- `pathlib.Path` (stdlib) - filesystem path operations and traversal
- `datetime` (stdlib) - execution timing and duration measurement

**← Outbound:**
- `/tmp/jesse_project_indexing_integration_test/` - debug artifact preservation directory
- `console/terminal` - comprehensive test progress reporting and result analysis
- `exit codes` - process exit status (0 for success, 1 for failure)
- `debug files` - detailed processing artifacts for post-test analysis
- `processing statistics` - file and directory processing metrics

**⚡ Integration:**
- Protocol: Direct async method invocation with comprehensive message capture
- Interface: `HierarchicalIndexer.index_hierarchy(project_root, context)` with `MockContext` simulation
- Coupling: Tight coupling to JESSE Framework indexing components, loose coupling to filesystem through temporary directories

########## Edge Cases & Error Handling

The script handles project root detection failures through `ensure_project_root()` exception catching with specific error messaging for missing project environments and unexpected detection errors. Error handling includes comprehensive exception management during indexing execution with detailed failure analysis, message capture preservation, and traceback reporting for debugging. The script addresses scenarios where indexing operations fail partially by implementing success criteria that allow controlled failure rates while detecting critical system issues, and preserves debug artifacts even during test failures for post-mortem analysis.

########### Internal Implementation Details

The script uses `/tmp/jesse_project_indexing_integration_test` as a fixed debug directory location with automatic cleanup and recreation for consistent test environments. The `MockContext` class implements async method signatures matching FastMCP interface requirements while storing messages in typed lists (`List[str]`) for categorized analysis. Internal mechanics include systematic project structure pre-analysis using `item.rglob("*")` for comprehensive file discovery, real-time progress monitoring through immediate console output in mock context methods, and multi-dimensional success evaluation combining `ProcessingStatus` enumeration checks, statistical thresholds (50% file success rate), and error count analysis relative to total file counts. The test orchestration preserves debug directories regardless of test outcome and provides detailed artifact location reporting for manual analysis.
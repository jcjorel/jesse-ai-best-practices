<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/tests/test_project_indexing_integration.py -->
<!-- Cached On: 2025-07-06T23:22:39.335172 -->
<!-- Source Modified: 2025-07-06T23:20:55.418259 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file provides comprehensive integration testing for the `HierarchicalIndexer` system by executing real-world project indexing on the actual JESSE Framework codebase. It validates the knowledge base indexing system's ability to handle authentic project complexity, file structures, and processing scenarios through direct execution against the live project root. The integration test offers configurable rebuild modes (`--full-rebuild`, `--kb-only-rebuild`) enabling targeted testing strategies from complete system rebuilds to surgical KB regeneration. Key semantic entities include `HierarchicalIndexer`, `IndexingConfig`, `MockContext`, `ProcessingStatus`, `ensure_project_root`, `get_default_config`, `IndexingMode`, `ProcessingStats`, and `FastMCP` protocol simulation, enabling comprehensive validation of the knowledge base hierarchical indexing pipeline with real project data and authentic edge cases.

##### Main Components

The test suite centers around the `MockContext` class that simulates `FastMCP` Context interface for message capture and monitoring, the `test_real_project_indexing` async function that orchestrates the complete integration test workflow, and utility functions `delete_kb_files` and `delete_analysis_files` for managing rebuild scenarios. The `main` function provides command-line interface with argument parsing for different rebuild modes. The integration leverages `HierarchicalIndexer` as the primary system under test, configured through `IndexingConfig` with project-specific settings and exclusions.

###### Architecture & Design

The architecture follows a comprehensive integration testing pattern with mock context simulation, real project targeting, and configurable rebuild strategies. The design separates concerns between message capture (`MockContext`), file management utilities, and the main test orchestration. The system employs a three-tier rebuild approach: incremental mode for normal operation, KB-only rebuild for surgical testing, and full rebuild for complete system validation. Debug artifact preservation enables post-test analysis through dedicated temporary directories with structured output organization.

####### Implementation Approach

The implementation uses async/await patterns throughout for compatibility with the `HierarchicalIndexer` async interface. Project root detection employs `ensure_project_root()` with comprehensive error handling for dynamic environment adaptation. Configuration management leverages `get_default_config('project-base')` with targeted overrides for integration testing parameters including file size limits, batch processing, and concurrency controls. Success criteria evaluation uses multiple validation checkpoints including completion status, file processing statistics, message analysis, and debug artifact generation.

######## External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.knowledge_bases.indexing.hierarchical_indexer:HierarchicalIndexer` - core indexing system under test
- `jesse_framework_mcp.knowledge_bases.models.indexing_config:IndexingConfig` - configuration management
- `jesse_framework_mcp.knowledge_bases.models.knowledge_context:ProcessingStatus` - status enumeration
- `jesse_framework_mcp.helpers.path_utils:ensure_project_root` - dynamic project root detection
- `jesse_framework_mcp.knowledge_bases.indexing.defaults:get_default_config` - default configuration provider
- `argparse` (external library) - command-line argument parsing
- `asyncio` (external library) - async execution framework
- `pathlib.Path` (external library) - path manipulation utilities

**← Outbound:**
- `/tmp/jesse_project_indexing_integration_test/` - debug artifact directory for analysis
- `project_root/.knowledge/` - knowledge base output directory structure
- `stdout` - comprehensive test progress and result reporting
- `exit codes` - process exit status for CI/CD integration

**⚡ System role and ecosystem integration:**
- **System Role**: Critical integration validation component ensuring the knowledge base indexing system functions correctly with real-world project complexity and file structures
- **Ecosystem Position**: Core testing infrastructure component validating the entire indexing pipeline from configuration through execution to output generation
- **Integration Pattern**: Executed by developers and CI/CD systems for comprehensive system validation, consuming actual project files and generating debug artifacts for analysis

######### Edge Cases & Error Handling

The test handles project root detection failures with specific error messages and graceful degradation. File processing errors are captured through the `MockContext` message system with categorized error collection and analysis. The system accommodates partial failures through success rate calculations allowing up to 50% file processing failures while maintaining overall test validity. Configuration errors, indexing exceptions, and setup failures are caught with detailed traceback reporting. Debug directory creation failures and cleanup issues are handled with appropriate fallback mechanisms.

########## Internal Implementation Details

The `MockContext` class maintains separate message lists (`info_messages`, `debug_messages`, `warning_messages`, `error_messages`) with real-time console output for monitoring. File deletion utilities use `rglob` patterns for comprehensive file discovery with relative path reporting for user feedback. Configuration overrides target specific integration testing requirements including 2MB file size limits, batch size of 5, and single concurrent operation for stability. Success criteria evaluation uses dictionary-based validation with boolean logic for clear pass/fail determination. Debug artifact preservation uses temporary directory structures with systematic file organization for post-test analysis.

########### Code Usage Examples

**Basic integration test execution with incremental processing:**
```python
# Run standard integration test with existing cache
python test_project_indexing_integration.py
```

**KB-only rebuild for testing synthesis improvements:**
```python
# Fast rebuild preserving analysis files, regenerating only KB files
python test_project_indexing_integration.py --kb-only-rebuild
```

**Complete system rebuild for comprehensive validation:**
```python
# Nuclear rebuild deleting all cached files and regenerating everything
python test_project_indexing_integration.py --full-rebuild
```

**Programmatic test execution with custom configuration:**
```python
# Execute integration test programmatically
success = await test_real_project_indexing(
    full_rebuild=False,
    kb_only_rebuild=True
)
```
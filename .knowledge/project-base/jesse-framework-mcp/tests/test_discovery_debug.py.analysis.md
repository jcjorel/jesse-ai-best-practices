<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/tests/test_discovery_debug.py -->
<!-- Cached On: 2025-07-06T11:22:12.966814 -->
<!-- Source Modified: 2025-07-06T11:18:12.560475 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file provides debug testing capabilities for the Jesse Framework MCP's directory discovery phase, specifically investigating why the `HierarchicalIndexer` component fails to properly exclude certain directories during project indexing. The file implements comprehensive discovery phase validation through the `test_discovery_debug()` async function, enabling developers to diagnose directory exclusion failures in knowledge base indexing workflows. Key semantic entities include `HierarchicalIndexer`, `IndexingConfig`, `get_default_config`, `should_process_directory()`, `_discover_directory_structure()`, project-base exclusions (`.coding_assistant/`, `.knowledge/`, `.clinerules/`, `scratchpad/`), `AsyncMock` context simulation, and tempfile-based test environment creation. The implementation uses structured test project creation with realistic directory hierarchies to validate exclusion logic against expected behavior patterns.

##### Main Components

The file contains the primary `test_discovery_debug()` async function that orchestrates the complete debug workflow, a `main()` function serving as the CLI entry point with result reporting, and comprehensive test infrastructure including temporary directory creation, mock context setup, and validation logic. The debug test creates a realistic project structure with both excluded directories (`.coding_assistant/`, `.knowledge/`, `.clinerules/`, `scratchpad/`) and included directories (`src/`, `docs/`) to simulate real-world indexing scenarios. The validation system compares expected versus actual discovery results through set operations and provides detailed diagnostic output including mock call analysis and final determination logic.

###### Architecture & Design

The debug test follows a structured validation architecture with distinct phases: test environment setup, configuration loading, individual directory exclusion testing, discovery phase execution, and comprehensive result analysis. The design uses temporary filesystem isolation through `tempfile.TemporaryDirectory` to ensure test reproducibility and cleanup. The validation approach employs set-based comparison logic to identify wrongly included or excluded directories, with comprehensive diagnostic reporting including mock context call analysis. The architecture separates concerns between test setup, execution, validation, and reporting phases for clear debugging workflow.

####### Implementation Approach

The implementation uses async/await patterns for compatibility with the `HierarchicalIndexer._discover_directory_structure()` method, employing `AsyncMock` objects to simulate the indexing context without actual logging infrastructure. The test creates a realistic project structure programmatically, then validates both individual directory exclusion logic through `config.should_process_directory()` and the complete discovery phase behavior. The validation strategy uses set operations (`excluded_expected & discovered_names`, `included_expected - discovered_names`) to identify discrepancies between expected and actual behavior. Diagnostic output includes structured reporting with emoji indicators, detailed mock call analysis, and final determination logic for root cause identification.

######## External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.knowledge_bases.indexing.hierarchical_indexer:HierarchicalIndexer` - core indexing component under test
- `jesse_framework_mcp.knowledge_bases.indexing.defaults:get_default_config` - configuration factory for project-base settings
- `jesse_framework_mcp.knowledge_bases.models.indexing_config:IndexingConfig` - configuration model with exclusion logic
- `asyncio` (external library) - async execution runtime for test orchestration
- `tempfile` (external library) - temporary filesystem creation for isolated testing
- `pathlib:Path` (external library) - filesystem path manipulation and directory operations
- `unittest.mock:AsyncMock` (external library) - mock context simulation for indexer testing

**← Outbound:**
- `console output` - structured diagnostic reporting for developers debugging discovery issues
- `test results` - boolean validation results for CI/CD integration or manual testing workflows
- `temporary filesystem artifacts` - test project structure creation for validation scenarios

**⚡ System role and ecosystem integration:**

- **System Role**: This debug test serves as a diagnostic tool for the Jesse Framework MCP's knowledge base indexing system, specifically targeting directory discovery phase failures that prevent proper exclusion of configuration and temporary directories
- **Ecosystem Position**: Peripheral debugging utility that validates core indexing functionality, essential for maintaining proper knowledge base creation workflows but not part of the production indexing pipeline
- **Integration Pattern**: Used by developers experiencing directory exclusion issues, executed manually or through test runners to diagnose `HierarchicalIndexer` behavior and validate configuration effectiveness

######### Edge Cases & Error Handling

The debug test handles scenarios where excluded directories are wrongly discovered or expected directories are missed during the discovery phase. The validation logic identifies both false positives (excluded directories appearing in results) and false negatives (expected directories missing from results) through comprehensive set-based comparison. The test provides detailed diagnostic output for debugging scenarios including empty discovery results, configuration loading failures, and mock context call analysis. Error scenarios include temporary directory creation failures, configuration parsing issues, and async execution problems, with structured reporting to identify whether issues originate in the discovery phase or elsewhere in the execution flow.

########## Internal Implementation Details

The test creates a specific directory structure with `.coding_assistant/workspace.json`, `.knowledge/kb.md`, `.clinerules/rules.md`, `scratchpad/notes.txt`, `src/main.py`, and `docs/README.md` files to simulate realistic project layouts. The configuration uses `project-base` defaults with custom knowledge output directory pointing to the temporary test location. Mock context setup includes `info`, `debug`, `warning`, and `error` methods as `AsyncMock` objects to capture indexer logging behavior. The validation logic uses `wrongly_included = excluded_expected & discovered_names` and `wrongly_excluded = included_expected - discovered_names` for precise discrepancy identification. Final determination combines both validation results to determine if the discovery phase is functioning correctly.

########### Code Usage Examples

**Running the debug test to diagnose directory exclusion issues:**

```python
# Execute the debug test directly
result = asyncio.run(test_discovery_debug())
if result:
    print("Discovery phase working correctly")
else:
    print("Discovery phase has issues")
```

**Using the CLI interface for manual debugging:**

```bash
# Run the debug test from command line
python test_discovery_debug.py
```

**Integrating debug validation into test workflows:**

```python
# Example integration for automated testing
async def validate_indexer_discovery():
    debug_result = await test_discovery_debug()
    assert debug_result, "Discovery phase validation failed"
    return debug_result
```
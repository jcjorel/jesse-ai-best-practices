<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/tests/test_centralized_decision_engine.py -->
<!-- Cached On: 2025-07-06T14:33:35.507289 -->
<!-- Source Modified: 2025-07-06T14:30:32.730902 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This test file validates the centralized `RebuildDecisionEngine` addressing two critical scattered decision logic issues: infinite rebuilding of empty directories (like "image" directory) and missing global project summaries (`root_kb.md`). The file provides comprehensive test coverage for decision engine functionality through `test_empty_directory_decision()`, `test_project_root_decision()`, `test_regular_directory_decision()`, and `test_comprehensive_decision_analysis()` functions. Key semantic entities include `RebuildDecisionEngine`, `IndexingConfig`, `DirectoryContext`, `FileContext`, `DecisionOutcome`, `DecisionReason`, `MockContext`, `IndexingMode.INCREMENTAL`, `OutputConfig`, `ChangeDetectionConfig`, and `DecisionReport` enabling rapid navigation of knowledge base indexing decision logic. The test suite validates that empty directories receive `SKIP` decisions with `EMPTY_DIRECTORY` reasoning, project roots get `REBUILD` decisions with `PROJECT_ROOT_FORCED` reasoning, and regular directories use staleness-based `COMPREHENSIVE_STALENESS` logic.

##### Main Components

The test file contains four primary test functions: `test_empty_directory_decision()` validates empty directory handling preventing infinite rebuilds, `test_project_root_decision()` ensures project root processing for `root_kb.md` generation, `test_regular_directory_decision()` verifies standard staleness-based decision logic, and `test_comprehensive_decision_analysis()` tests complete hierarchy analysis. The `MockContext` class provides FastMCP Context simulation with message capture capabilities through `info()`, `debug()`, `warning()`, and `error()` methods. The `main()` function orchestrates test execution with comprehensive result reporting and error isolation.

###### Architecture & Design

The test architecture follows a mock-based testing pattern with `MockContext` simulating the FastMCP Context interface for decision engine interaction. Each test function creates isolated temporary directory structures using `tempfile.TemporaryDirectory()` to simulate real filesystem scenarios. The design employs comprehensive assertion-based validation checking both decision outcomes (`DecisionOutcome.SKIP`, `DecisionOutcome.REBUILD`) and reasoning (`DecisionReason.EMPTY_DIRECTORY`, `DecisionReason.PROJECT_ROOT_FORCED`, `DecisionReason.COMPREHENSIVE_STALENESS`). Test isolation ensures individual test failures don't affect other test execution through try-catch error handling.

####### Implementation Approach

The implementation uses `asyncio` for asynchronous test execution matching the decision engine's async interface. Each test creates specific directory contexts using `DirectoryContext` and `FileContext` models to simulate different scenarios: empty directories with no file contexts, project roots with content, and regular directories with processable files. The testing strategy employs comprehensive verification checking decision outcomes, reasoning text content, and debug message patterns. Test data generation uses real file creation with `Path.write_text()` and `Path.mkdir()` for authentic filesystem simulation.

######## External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.knowledge_bases.indexing.rebuild_decision_engine:RebuildDecisionEngine` - core decision engine being tested
- `jesse_framework_mcp.knowledge_bases.models.indexing_config:IndexingConfig` - configuration model for decision engine setup
- `jesse_framework_mcp.knowledge_bases.models.knowledge_context:DirectoryContext` - directory context modeling
- `jesse_framework_mcp.knowledge_bases.models.rebuild_decisions:DecisionOutcome` - decision outcome enumeration
- `asyncio` (external library) - asynchronous test execution framework
- `tempfile` (external library) - temporary directory creation for test isolation
- `pathlib.Path` (external library) - filesystem path manipulation

**← Outbound:**
- `pytest` or direct execution - test runner consuming this test suite
- `CI/CD pipeline` - automated testing consuming test results
- `development workflow` - manual test execution for decision engine validation

**⚡ System role and ecosystem integration:**
- **System Role**: Critical validation component ensuring decision engine correctness within the Jesse Framework MCP knowledge base indexing system
- **Ecosystem Position**: Core testing infrastructure preventing regression in decision logic that could cause infinite rebuilds or missing project summaries
- **Integration Pattern**: Executed by developers and CI/CD systems to validate decision engine behavior before deployment, ensuring knowledge base indexing reliability

######### Edge Cases & Error Handling

The test suite handles multiple edge cases including completely empty directories with no files or subdirectories, project root directories requiring forced processing regardless of staleness, and mixed hierarchies combining empty directories with content-bearing directories. Error handling uses comprehensive try-catch blocks in each test function preventing individual test failures from stopping overall execution. The `MockContext` captures all message types (`info`, `debug`, `warning`, `error`) enabling verification of proper error communication. Test assertions include specific error message pattern matching ensuring decision engine provides appropriate feedback for different scenarios.

########## Internal Implementation Details

The `MockContext` class maintains separate message lists (`info_messages`, `debug_messages`, `warning_messages`, `error_messages`) for categorized message verification and real-time console output for debugging. Test functions use specific assertion patterns checking decision outcome enums, reasoning text content matching, and debug message emoji patterns (`📁 EMPTY`, `🏗️ PROJECT ROOT`). The comprehensive analysis test builds complex directory hierarchies with `subdirectory_contexts` nesting to validate recursive decision making. File timestamp simulation uses `datetime.fromtimestamp(file.stat().st_mtime)` for realistic staleness testing scenarios.

########### Code Usage Examples

**Basic decision engine test setup:**
```python
# Create test configuration for decision engine
config = IndexingConfig(
    output_config=OutputConfig(knowledge_output_directory=temp_path / ".knowledge"),
    change_detection=ChangeDetectionConfig(
        indexing_mode=IndexingMode.INCREMENTAL,
        timestamp_tolerance_seconds=1.0
    )
)

# Create decision engine and mock context
decision_engine = RebuildDecisionEngine(config)
ctx = MockContext()
```

**Empty directory decision testing:**
```python
# Create empty directory context (no files, no subdirectories)
empty_directory_context = DirectoryContext(
    directory_path=empty_dir,
    file_contexts=[],  # No files
    subdirectory_contexts=[]  # No subdirectories
)

# Make decision and verify outcome
decision = await decision_engine.should_rebuild_directory(
    empty_directory_context, temp_path, ctx
)
assert decision.outcome == DecisionOutcome.SKIP
assert decision.reason == DecisionReason.EMPTY_DIRECTORY
```

**Comprehensive hierarchy analysis:**
```python
# Perform comprehensive analysis on directory hierarchy
report = await decision_engine.analyze_hierarchy(root_context, temp_path, ctx)

# Verify report structure and decisions
assert report.total_decisions >= 3
root_decision = report.get_decision_for_path(temp_path)
stats = report.get_summary_statistics()
```
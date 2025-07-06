<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/tests/test_hierarchical_dependency_planning.py -->
<!-- Cached On: 2025-07-07T00:56:21.759804 -->
<!-- Source Modified: 2025-07-07T00:51:24.399307 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

Test suite validating hierarchical dependency planning architecture for the Jesse Framework MCP knowledge base system, specifically ensuring selective cascading and horizontal dependency management work correctly. Provides comprehensive validation of `RebuildDecisionEngine` selective ancestor propagation and `PlanGenerator` sibling dependency coordination through `test_selective_cascading()` and `test_horizontal_dependencies()` functions. Enables developers to verify that directory rebuild decisions correctly cascade to parent directories without affecting unrelated siblings, and that horizontal dependencies between sibling directories are properly established. Key semantic entities include `MockContext`, `RebuildDecisionEngine`, `PlanGenerator`, `DecisionReport`, `RebuildDecision`, `DirectoryContext`, `FileContext`, `IndexingConfig`, `DecisionOutcome`, `DecisionReason`, `tempfile`, `asyncio`, and `fastmcp.Context` for comprehensive dependency planning validation using async test execution patterns.

##### Main Components

Two primary test functions (`test_selective_cascading()` and `test_horizontal_dependencies()`) that validate different aspects of the hierarchical dependency system, plus a `MockContext` class for FastMCP context simulation and a `main()` orchestration function. The `MockContext` provides logging capabilities with debug, info, warning, and error methods that capture messages for test verification. Test functions create temporary directory structures, configure indexing parameters, and exercise the decision engine and plan generator components to verify correct behavior.

###### Architecture & Design

Follows async test architecture pattern with temporary filesystem setup for isolated testing environments. Uses dependency injection through mock objects to simulate FastMCP context without requiring full framework initialization. Implements comprehensive test scenarios that mirror real-world directory structures with nested hierarchies (`src/components/buttons/`, `src/components/forms/`, `src/utils/`) to validate both vertical cascading and horizontal dependency relationships. Test design separates concerns between decision-making logic and plan generation logic for focused validation.

####### Implementation Approach

Creates temporary directory structures using `tempfile.TemporaryDirectory()` context manager for clean test isolation, then populates with realistic file hierarchies to simulate actual project structures. Constructs `IndexingConfig` objects with minimal exclusions to focus testing on core logic rather than filtering behavior. Uses `DecisionReport` objects to track rebuild decisions and verify cascading propagation through `_propagate_cascading_decisions()` method calls. Implements assertion-based validation to verify ancestor directories receive `DecisionReason.CHILD_DIRECTORY_REBUILT` while sibling directories remain unaffected.

######## External Dependencies & Integration Points

**→ Inbound:**
- `fastmcp.Context` - FastMCP framework context interface for logging operations
- `jesse_framework_mcp.knowledge_bases.models` - Core data models including `IndexingConfig`, `DirectoryContext`, `FileContext`
- `jesse_framework_mcp.knowledge_bases.models.indexing_config` - Configuration models `OutputConfig`, `ContentFilteringConfig`
- `jesse_framework_mcp.knowledge_bases.models.rebuild_decisions` - Decision tracking models `DecisionReport`, `RebuildDecision`, `DecisionOutcome`, `DecisionReason`
- `jesse_framework_mcp.knowledge_bases.indexing.rebuild_decision_engine` - `RebuildDecisionEngine` for cascading logic validation
- `jesse_framework_mcp.knowledge_bases.indexing.plan_generator` - `PlanGenerator` for horizontal dependency testing
- `asyncio` (external library) - Async execution framework for test orchestration
- `tempfile` (external library) - Temporary filesystem creation for test isolation
- `pathlib.Path` (external library) - Path manipulation utilities
- `datetime.datetime` (external library) - Timestamp generation for file contexts

**← Outbound:**
- Test execution frameworks - Provides validation results for CI/CD pipeline integration
- Development workflow - Validates architectural fixes before deployment
- Knowledge base indexing system - Ensures dependency planning logic correctness

**⚡ System role and ecosystem integration:**
- **System Role**: Critical validation component ensuring the hierarchical dependency planning architecture functions correctly within the Jesse Framework MCP knowledge base system
- **Ecosystem Position**: Core testing infrastructure that validates fundamental indexing behavior, preventing regression in dependency management logic
- **Integration Pattern**: Executed by developers and CI systems to verify architectural fixes, with results feeding into deployment decisions and system reliability assurance

######### Edge Cases & Error Handling

Tests verify that sibling directories without content changes are correctly excluded from cascading rebuilds, preventing unnecessary work propagation. Validates that ancestor propagation stops at appropriate boundaries and doesn't create infinite loops or excessive cascading. Handles scenarios where decision reports contain mixed rebuild and skip decisions to ensure selective processing. Uses assertion-based validation that will raise clear exceptions if cascading logic fails, providing immediate feedback on architectural issues.

########## Internal Implementation Details

Uses `_propagate_cascading_decisions()` private method to test internal cascading logic directly, bypassing higher-level interfaces for focused validation. Employs `_collect_sibling_directory_tasks()` and `_sanitize_path_for_id()` methods to verify task ID generation and sibling relationship establishment. Creates realistic `DirectoryContext` and `FileContext` objects with proper parent-child relationships to mirror actual indexing scenarios. Implements comprehensive logging capture through `MockContext.logs` list for debugging test execution and verifying internal decision-making processes.

########### Code Usage Examples

Essential test execution pattern for validating hierarchical dependency planning:

```python
# Create isolated test environment with realistic directory structure
with tempfile.TemporaryDirectory() as temp_dir:
    source_root = Path(temp_dir)
    (source_root / "src" / "components" / "buttons").mkdir(parents=True)
    
    # Configure indexing with minimal exclusions for focused testing
    config = IndexingConfig(
        output_config=OutputConfig(knowledge_output_directory=knowledge_dir),
        content_filtering=ContentFilteringConfig(
            excluded_extensions={".pyc", ".pyo"},
            excluded_directories={".git", "__pycache__"}
        )
    )
    
    # Test selective cascading by marking specific directory for rebuild
    decision_engine = RebuildDecisionEngine(config)
    report = DecisionReport()
    buttons_decision = RebuildDecision(
        path=source_root / "src" / "components" / "buttons",
        outcome=DecisionOutcome.REBUILD,
        reason=DecisionReason.COMPREHENSIVE_STALENESS
    )
    report.add_rebuild_decision(buttons_decision)
    
    # Verify cascading propagation to ancestors only
    cascaded_count = await decision_engine._propagate_cascading_decisions(
        None, source_root, report, ctx
    )
    assert report.get_decision_for_path(source_root / "src").should_rebuild
```
<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/tests/test_indexing_core.py -->
<!-- Cached On: 2025-07-04T17:20:02.357747 -->
<!-- Source Modified: 2025-07-02T22:21:02.242270 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file provides comprehensive testing infrastructure for the Knowledge Bases Hierarchical Indexing System, specifically validating core indexing functionality, critical LLM response processing, and enhanced debug architecture. The test suite enables verification of `HierarchicalIndexer` entry points, `MockContext` message capture, `IndexingConfig` filtering behavior, and `DebugHandler` stage organization without requiring full LLM integration complexity. Key semantic entities include `HierarchicalIndexer`, `IndexingConfig`, `IndexingMode`, `ProcessingStatus`, `MockContext`, `DebugHandler`, `KnowledgeBuilder`, `create_test_directory_structure()`, `test_indexer_core_functionality()`, `test_llm_header_extraction()`, `test_enhanced_debug_mode()`, `tempfile`, `pathlib.Path`, `asyncio`, and `unittest` patterns. The testing framework addresses the critical LLM header extraction bug where LLM-generated headers interfere with `mistletoe` parsing during content extraction.

##### Main Components

`MockContext` class providing minimal `FastMCP` Context interface simulation with message categorization (`info_messages`, `debug_messages`, `warning_messages`, `error_messages`) and async method support. `create_test_directory_structure()` function generating realistic project hierarchy with `to_be_indexed/` and `indexed_knowledge/` separation, including `src/`, `docs/`, `tests/` directories with Python files, Markdown documentation, and test cases. `test_indexer_core_functionality()` async function executing direct `HierarchicalIndexer` testing with configuration validation, file filtering verification, and processing statistics analysis. `test_llm_header_extraction()` async function validating `KnowledgeBuilder._extract_content_from_llm_response()` method against various LLM response patterns. `test_enhanced_debug_mode()` async function testing `DebugHandler` stage organization, predictable filename generation, and replay functionality. `main()` async coordinator executing all test categories with comprehensive result reporting.

###### Architecture & Design

Test architecture follows isolated component testing pattern with temporary directory management and mock object simulation. The design separates core functionality testing from LLM integration complexity using `MockContext` to capture indexer messages without external dependencies. Test structure implements three-tier validation: basic functionality verification, critical bug fix testing, and enhanced feature validation. Debug mode testing uses fixed directory paths (`/tmp/debug_test_indexing_core`) enabling manual inspection and replay demonstration. The architecture emphasizes deterministic test execution with predictable file structures and comprehensive verification checkpoints. Stage-based debug testing validates pipeline organization with `stage_1_file_analysis`, `stage_2_chunk_analysis`, `stage_3_chunk_aggregation`, `stage_4_directory_analysis`, and `stage_5_global_summary` directories.

####### Implementation Approach

Core testing strategy directly instantiates `HierarchicalIndexer` with `IndexingConfig` containing `IndexingMode.FULL`, debug mode enabled, and replay functionality activated. Test directory creation uses `tempfile` and `pathlib.Path` for cross-platform compatibility with realistic project structure simulation including Python source files, Markdown documentation, and test cases. LLM header extraction testing implements pattern matching against various LLM response formats including "Here's my analysis", "Based on", and "Looking at" headers that interfere with content parsing. Debug mode testing validates `DebugHandler._normalize_path_for_filename()` method ensuring predictable filename generation and stage-based file organization. Error handling uses try-catch blocks with graceful degradation allowing partial test success when LLM components are unavailable.

######## External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.knowledge_bases.indexing.hierarchical_indexer:HierarchicalIndexer` - primary indexing system component under test
- `jesse_framework_mcp.knowledge_bases.models.indexing_config:IndexingConfig` - configuration management for indexing operations
- `jesse_framework_mcp.knowledge_bases.models.knowledge_context:ProcessingStatus` - status tracking for indexing progress
- `jesse_framework_mcp.knowledge_bases.indexing.knowledge_builder:KnowledgeBuilder` - LLM response processing component
- `jesse_framework_mcp.knowledge_bases.indexing.debug_handler:DebugHandler` - enhanced debug mode functionality
- `asyncio` (external library) - async test execution coordination
- `tempfile` (external library) - temporary directory management for isolated testing
- `pathlib.Path` (external library) - cross-platform file path handling
- `shutil` (external library) - directory cleanup operations

**← Outbound:**
- `test_results/debug_files/` - generated debug output for manual inspection
- `/tmp/debug_test_indexing_core/` - fixed debug directory for replay demonstration
- `stdout` - comprehensive test progress and result reporting
- `exit_code` - process exit status indicating overall test success/failure

**⚡ System role and ecosystem integration:**
- **System Role**: Critical validation component ensuring Knowledge Bases Hierarchical Indexing System reliability and correctness before deployment
- **Ecosystem Position**: Core testing infrastructure supporting development workflow and continuous integration validation
- **Integration Pattern**: Executed by developers during development cycles, CI/CD pipelines for automated validation, and manual testing for debug mode verification and LLM response processing validation

######### Edge Cases & Error Handling

LLM component unavailability handling with graceful degradation allowing basic functionality testing when full integration components are missing. Empty file and whitespace-only response processing in LLM header extraction testing ensuring robust content parsing. Malformed LLM responses with headers-only content or unexpected header structures validated through comprehensive test case coverage. Debug directory cleanup failure handling with warning messages rather than test failure. Import error handling for optional components allowing core functionality testing in minimal environments. File permission and disk space error scenarios during temporary directory creation with appropriate error reporting. Memory cache functionality testing ensuring proper fallback when debug files are unavailable.

########## Internal Implementation Details

`MockContext` message storage uses separate lists (`info_messages`, `debug_messages`, `warning_messages`, `error_messages`) with print statements for debugging visibility during test execution. Test directory structure creation implements nested directory hierarchy with realistic file content including Python docstrings, function definitions, and Markdown formatting. Debug mode testing uses deterministic filename generation through `_normalize_path_for_filename()` method converting path separators to underscores and removing file extensions. Stage organization validation checks for specific directory creation (`stage_1_file_analysis/`, `stage_2_chunk_analysis/`, etc.) with predictable file naming patterns. Test result aggregation uses dictionary-based tracking with boolean flags for each test category enabling detailed success/failure reporting. Cleanup operations preserve debug files for manual inspection while removing temporary test structures.

########### Code Usage Examples

Basic test execution pattern for validating indexing system functionality:

```python
# Execute comprehensive test suite
result = asyncio.run(main())
exit(0 if result else 1)
```

Mock context setup for capturing indexer messages during testing:

```python
# Create mock context for message capture
ctx = MockContext()

# Execute indexing with message capture
result = await indexer.index_hierarchy(to_be_indexed_dir, ctx)

# Verify captured messages
print(f"Info Messages: {len(ctx.info_messages)}")
print(f"Error Messages: {len(ctx.error_messages)}")
```

Test directory structure creation for realistic indexing scenarios:

```python
# Create separated source and target directories
to_be_indexed_dir, indexed_knowledge_dir = create_test_directory_structure(temp_dir)

# Configure indexing with target directory
config = IndexingConfig(
    indexing_mode=IndexingMode.FULL,
    knowledge_output_directory=indexed_knowledge_dir,
    debug_mode=True,
    enable_llm_replay=True
)
```

Debug mode testing with stage validation and predictable filename verification:

```python
# Test enhanced debug mode functionality
debug_handler = DebugHandler(
    debug_enabled=True,
    debug_output_directory=temp_debug_dir,
    enable_replay=True
)

# Verify predictable filename generation
normalized_name = debug_handler._normalize_path_for_filename(Path("src/main.py"))
# Result: "src_main_py"
```
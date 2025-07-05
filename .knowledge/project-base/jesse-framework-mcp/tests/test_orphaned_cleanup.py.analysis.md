<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/tests/test_orphaned_cleanup.py -->
<!-- Cached On: 2025-07-05T20:06:29.525915 -->
<!-- Source Modified: 2025-07-05T17:56:00.311858 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file provides comprehensive test coverage for the `OrphanedAnalysisCleanup` component within the Jesse Framework MCP knowledge building system. It validates orphaned file detection and removal functionality, ensuring proper cleanup of stale analysis files and knowledge files when their corresponding source files no longer exist. The test suite verifies directory structure preservation, leaf-first traversal algorithms, and cleanup statistics reporting through `pytest` framework integration. Key semantic entities include `OrphanedAnalysisCleanup`, `IndexingConfig`, `OutputConfig`, `cleanup_orphaned_files()`, `_collect_directories_leaf_first()`, `temp_directories`, `indexing_config`, `mock_context`, `analysis_files_deleted`, `knowledge_files_deleted`, `directories_deleted`, `total_items_deleted`, `project-base`, `.analysis.md`, and `_kb.md` enabling validation of knowledge base maintenance operations and file system consistency checks.

##### Main Components

Contains `TestOrphanedAnalysisCleanup` test class with six test methods: `test_cleanup_orphaned_analysis_files()` for validating removal of orphaned analysis files, `test_cleanup_orphaned_knowledge_files()` for knowledge file cleanup validation, `test_preserve_directories_with_content()` for content preservation verification, `test_no_cleanup_needed()` for empty structure handling, `test_preserve_empty_directories_with_existing_source()` for source-mirrored directory preservation, and `test_leaf_first_directory_collection()` for traversal algorithm validation. Includes three `pytest` fixtures: `temp_directories()` for temporary file system setup, `indexing_config()` for test configuration creation, and `mock_context()` for FastMCP context mocking.

###### Architecture & Design

Implements isolated test environments using `tempfile.TemporaryDirectory()` with structured directory hierarchies mirroring real knowledge base layouts. Uses `pytest` fixture dependency injection pattern for test setup and teardown management. Employs mock objects (`AsyncMock`) for external dependency isolation while preserving integration behavior. Test architecture separates concerns between orphaned file detection, directory preservation logic, cleanup statistics validation, and traversal algorithm verification through distinct test methods with clear arrange-act-assert patterns.

####### Implementation Approach

Creates realistic file system scenarios with `source_root/` and `knowledge_root/` directory structures containing `.analysis.md` and `_kb.md` files. Uses `Path.write_text()` and `Path.exists()` for file manipulation and validation. Implements cleanup statistics verification through assertion checks on `stats.analysis_files_deleted`, `stats.knowledge_files_deleted`, and `stats.directories_deleted` counters. Validates leaf-first directory traversal by creating nested directory structures and verifying collection order through index comparison of directory names.

######## External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.knowledge_bases.models:IndexingConfig` - configuration model for cleanup operations
- `jesse_framework_mcp.knowledge_bases.indexing.orphaned_cleanup:OrphanedAnalysisCleanup` - primary cleanup component under test
- `jesse_framework_mcp.knowledge_bases.models.indexing_config:OutputConfig` - output directory configuration
- `fastmcp:Context` - FastMCP context interface for logging operations
- `pytest` (external library) - testing framework and fixture management
- `tempfile` (external library) - temporary directory creation for isolated testing
- `unittest.mock:AsyncMock` (external library) - mock object creation for context isolation

**← Outbound:**
- `pytest.main()` - test execution entry point when run as script
- File system operations through `Path.mkdir()`, `Path.write_text()`, and `Path.exists()`
- Console output via `pytest` test result reporting

**⚡ System role and ecosystem integration:**
- **System Role**: Critical validation component ensuring `OrphanedAnalysisCleanup` reliability within Jesse Framework MCP knowledge base maintenance workflows
- **Ecosystem Position**: Core testing infrastructure validating cleanup subsystem correctness and preventing knowledge base corruption
- **Integration Pattern**: Executed by developers and CI/CD systems to validate cleanup implementation before deployment, ensuring knowledge base integrity and preventing orphaned file accumulation

######### Edge Cases & Error Handling

Validates preservation of directories with existing source counterparts even when empty, ensuring source-mirrored directory structures remain intact. Tests cleanup behavior when no orphaned files exist, verifying zero-impact operations on clean knowledge bases. Handles nested directory structures with proper leaf-first traversal to prevent directory deletion order conflicts. Validates content preservation logic by ensuring directories containing analysis files or subdirectories are never removed regardless of source file status.

########## Internal Implementation Details

Test fixtures create temporary directory structures with `source/` and `knowledge/project-base/` hierarchies. Analysis files use `.analysis.md` extension while knowledge files use `_kb.md` suffix for directory-level knowledge. Cleanup statistics are tracked through dedicated counter fields in the cleanup result object. Leaf-first directory collection is validated by creating `level1/level2/level3/` nested structures and verifying traversal order through list index comparisons of directory names.

########### Code Usage Examples

**Basic orphaned analysis file cleanup test setup:**
```python
# Creates test environment with source file and corresponding analysis file, plus orphaned analysis file
source_file = source_root / "existing_file.py"
source_file.write_text("print('hello world')")
valid_analysis = project_base_dir / "existing_file.py.analysis.md"
valid_analysis.write_text("# Analysis of existing_file.py")
orphaned_analysis = project_base_dir / "deleted_file.py.analysis.md"
orphaned_analysis.write_text("# Analysis of deleted_file.py")
```

**Cleanup execution and validation pattern:**
```python
# Executes cleanup operation and validates results through statistics checking
cleanup = OrphanedAnalysisCleanup(indexing_config)
stats = await cleanup.cleanup_orphaned_files(knowledge_root, source_root, mock_context)
assert stats.analysis_files_deleted == 1
assert not orphaned_analysis.exists()
assert valid_analysis.exists()
```

**Leaf-first directory traversal validation:**
```python
# Validates proper directory collection order for safe deletion operations
directories = cleanup._collect_directories_leaf_first(project_base)
directory_names = [d.name for d in directories]
assert directory_names.index("level3") < directory_names.index("level2")
assert directory_names.index("level2") < directory_names.index("level1")
```
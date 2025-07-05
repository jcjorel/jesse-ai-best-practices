<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/tests/test_project_base_indexing_rule.py -->
<!-- Cached On: 2025-07-05T20:19:45.598904 -->
<!-- Source Modified: 2025-07-05T19:33:08.162983 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This test script validates the project-base indexing business rule implementation for the Jesse Framework MCP system, specifically testing that knowledge files are stored in `{PROJECT_ROOT}/.knowledge/project-base/` with directory structure mirroring when `handler_type="project-base"`. The script provides comprehensive validation of mandatory project-base subdirectory usage, configuration detection, and fallback behavior mechanisms. Key semantic entities include `KnowledgeBuilder`, `IndexingConfig`, `OutputConfig`, `handler_type`, `project-base`, `git-clones`, `tempfile`, `pathlib.Path`, `_get_knowledge_file_path`, and `.knowledge/project-base/` directory structure. The testing framework validates that all configurations now use the project-base/ subdirectory regardless of handler type, eliminating backward compatibility for consistent knowledge file organization.

##### Main Components

The script contains three primary test functions: `test_project_base_indexing_path_rule()` validates correct directory structure usage with project-base indexing, `test_business_rule_configuration_detection()` tests configuration detection between project-base and git-clones handler types, and `test_mandatory_project_base_subdirectory()` validates that project-base/ subdirectory is mandatory regardless of configuration. Supporting components include temporary directory creation using `tempfile.TemporaryDirectory()`, path validation logic comparing expected vs actual knowledge file paths, and comprehensive test result reporting with pass/fail status indicators.

###### Architecture & Design

The testing architecture follows an isolated environment pattern using `tempfile.TemporaryDirectory()` for each test scenario, ensuring no cross-test contamination. The design validates business rule enforcement by creating realistic project structures with nested directories (`src/components/ui/buttons/`) and verifying knowledge file path generation follows the mandatory project-base/ pattern. Each test creates `KnowledgeBuilder` instances with different `IndexingConfig` settings to validate that all configurations produce identical project-base/ subdirectory paths, confirming the elimination of backward compatibility.

####### Implementation Approach

The implementation uses direct path comparison validation by calling `_get_knowledge_file_path()` method on `KnowledgeBuilder` instances and comparing results against expected paths. Tests validate multi-level directory structure preservation within project-base/, fallback behavior when relative path calculation fails, and flat structure handling when no source_root is provided. The approach includes comprehensive edge case testing with unrelated directory paths and various configuration combinations to ensure consistent project-base/ subdirectory usage across all scenarios.

######## External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.knowledge_bases.indexing.knowledge_builder:KnowledgeBuilder` - core knowledge file path generation testing
- `jesse_framework_mcp.knowledge_bases.models.indexing_config:IndexingConfig` - configuration model validation
- `jesse_framework_mcp.knowledge_bases.models.indexing_config:OutputConfig` - output configuration testing
- `tempfile` (standard library) - isolated test environment creation
- `pathlib.Path` (standard library) - file system path manipulation and validation

**← Outbound:**
- Test execution results consumed by CI/CD validation systems
- Business rule compliance reports for deployment verification
- Configuration validation metrics for system reliability monitoring

**⚡ System role and ecosystem integration:**
- **System Role**: Critical validation component ensuring project-base indexing business rule compliance across the Jesse Framework MCP knowledge base system
- **Ecosystem Position**: Core testing infrastructure validating the foundation of knowledge file organization and directory structure consistency
- **Integration Pattern**: Executed by developers and CI systems to validate business rule enforcement before deployment, ensuring all knowledge files follow mandatory project-base/ subdirectory structure

######### Edge Cases & Error Handling

The tests validate missing source_root scenarios (should use flat structure in project-base/), unrelated directory paths (should use fallback naming in project-base/), multi-level nested directories (should preserve structure within project-base/), and different handler_type configurations (should all use project-base/ subdirectory). Error handling includes assertion failures with descriptive messages for incorrect paths, comprehensive path comparison logging, and detailed test result reporting with specific expected vs actual path information. The tests specifically validate that no backward compatibility exists and all configurations produce consistent project-base/ subdirectory usage.

########## Internal Implementation Details

Internal mechanisms include temporary directory structure creation with nested paths like `src/components/ui/buttons/`, direct method invocation on `KnowledgeBuilder._get_knowledge_file_path()` for path generation testing, and comprehensive path validation comparing expected project-base/ patterns against actual results. The testing framework creates multiple `IndexingConfig` instances with different `handler_type` values to validate consistent behavior, while path comparison logic ensures exact matching of expected `.knowledge/project-base/` subdirectory structures with proper knowledge base file naming conventions.

########### Code Usage Examples

Essential project-base indexing path validation pattern:

```python
# This pattern demonstrates validation of mandatory project-base subdirectory usage regardless of handler type
# All configurations must produce paths within .knowledge/project-base/ directory structure
output_config = OutputConfig(knowledge_output_directory=knowledge_dir)
config_with_project_base = IndexingConfig(
    handler_type="project-base",
    description="Test configuration with project-base indexing",
    output_config=output_config
)

builder = KnowledgeBuilder(config_with_project_base)
knowledge_path = builder._get_knowledge_file_path(test_directory, source_root)
expected_path = knowledge_dir / "project-base" / "src" / "components" / "components_kb.md"
```

Configuration detection and validation testing:

```python
# This pattern validates that different handler types still use project-base subdirectory (no backward compatibility)
# Both project-base and git-clones configurations produce identical path structures
project_base_config = IndexingConfig(handler_type="project-base")
regular_config = IndexingConfig(handler_type="git-clones")

builder_project_base = KnowledgeBuilder(project_base_config)
builder_regular = KnowledgeBuilder(regular_config)

project_base_path = builder_project_base._get_knowledge_file_path(test_directory, source_root)
regular_path = builder_regular._get_knowledge_file_path(test_directory, source_root)

# Both paths should be identical and use project-base/ subdirectory
assert project_base_path == regular_path
```

Multi-level directory structure validation:

```python
# This pattern validates that complex nested directory structures are preserved within project-base subdirectory
# Deep directory hierarchies maintain their structure under the mandatory project-base/ root
deep_directory = source_root / "src" / "components" / "ui" / "buttons"
deep_path = builder._get_knowledge_file_path(deep_directory, source_root)

expected_deep_path = knowledge_dir / "project-base" / "src" / "components" / "ui" / "buttons" / "buttons_kb.md"
assert deep_path == expected_deep_path
```
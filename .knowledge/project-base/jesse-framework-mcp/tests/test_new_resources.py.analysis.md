<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/tests/test_new_resources.py -->
<!-- Cached On: 2025-07-04T00:14:50.214328 -->
<!-- Source Modified: 2025-07-01T08:59:29.265995 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

Validates knowledge resource functionality within the JESSE Framework MCP Server by testing README.md resource endpoints and registration mechanisms. Provides automated verification of `git-clones-readme` and `pdf-knowledge-readme` resources through file system validation and content inspection. Enables developers to verify knowledge base integration before deployment by confirming resource registration through the `register_knowledge_resources` function and validating expected content patterns like "Git Clone Knowledge Bases Index", "FastMCP", and "Cline" references. Key semantic entities include `asyncio` for async execution, `pathlib.Path` for file operations, `jesse_framework_mcp.resources.knowledge` module, `register_knowledge_resources` function, `fastmcp.Context` for MCP integration, `.knowledge/git-clones/README.md` and `.knowledge/pdf-knowledge/README.md` file paths, and UTF-8 encoding specifications.

##### Main Components

Contains three primary test functions: `test_git_clones_readme` for validating git clone knowledge base README files, `test_pdf_knowledge_readme` for testing PDF knowledge documentation resources, and `test_resource_registration` for verifying MCP resource registration. Includes a `main` orchestration function that coordinates sequential test execution with formatted output reporting. Implements file existence validation, content loading verification, and pattern matching for expected knowledge base references.

###### Architecture & Design

Follows sequential test execution pattern with isolated test functions for each resource type. Implements graceful degradation for missing directories through warning messages rather than failures. Uses direct file system access for validation rather than MCP resource calls, enabling testing of underlying file structure integrity. Employs exception handling at the function level with detailed error reporting and status indicators using emoji-based visual feedback system.

####### Implementation Approach

Utilizes `os.path.exists()` for file system validation combined with UTF-8 file reading for content inspection. Implements pattern matching through string containment checks for expected content markers. Uses `sys.path.insert(0)` for local module import resolution and async/await patterns for consistent execution flow. Applies defensive programming with try-catch blocks around each test operation and provides both positive and negative test result reporting.

######## Code Usage Examples

Execute the complete test suite to validate knowledge resource functionality:

```python
# Run all knowledge resource tests
asyncio.run(main())
```

Test individual git clones README resource with file validation:

```python
# Validate git clones README exists and contains expected content
readme_path = ".knowledge/git-clones/README.md"
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if "Git Clone Knowledge Bases Index" in content:
        print("✅ Git clones README contains expected header")
```

Verify resource registration without errors:

```python
# Test MCP resource registration
from jesse_framework_mcp.resources.knowledge import register_knowledge_resources
register_knowledge_resources()
print("✅ Knowledge resources registered successfully")
```

######### External Dependencies & Integration Points

**→ Inbound:** [dependencies this test file requires]
- `asyncio` (external library) - async execution framework for test coordination
- `sys` (external library) - Python path manipulation for module imports
- `pathlib.Path` (external library) - cross-platform file path handling
- `os` (external library) - file system operations and path validation
- `jesse_framework_mcp.resources.knowledge:register_knowledge_resources` - MCP resource registration function
- `jesse_framework_mcp.main:server` - MCP server instance for integration testing
- `fastmcp.Context` (external library) - MCP context interface for resource testing

**← Outbound:** [systems that depend on this test file]
- `tests/` - test suite execution framework that runs this validation
- `CI/CD pipelines` - automated testing systems that verify knowledge resource functionality
- `development workflows` - developer validation processes before deployment

**⚡ Integration:** [connection mechanisms]
- Protocol: Direct file system access and Python module imports
- Interface: Function calls, file I/O operations, and async execution
- Coupling: Loose coupling with graceful handling of missing directories

########## Edge Cases & Error Handling

Handles missing `.knowledge/pdf-knowledge/` directory gracefully with warning messages rather than test failures, recognizing this as expected behavior for new installations. Manages file encoding issues through explicit UTF-8 specification and provides detailed error messages with full exception details. Addresses import path resolution through `sys.path.insert(0)` for local module access. Implements comprehensive exception catching at each test function level with specific error context reporting and visual status indicators for rapid issue identification.

########### Internal Implementation Details

Uses emoji-based status reporting system with ✅ for success, ❌ for failures, and ⚠️ for warnings to provide immediate visual feedback. Implements character count reporting for loaded content to verify non-empty file reads. Employs string containment checks rather than regex patterns for content validation simplicity. Maintains consistent async function signatures across all test functions despite some not requiring async operations, ensuring uniform execution patterns. Uses formatted string output with separator lines for clear test section delineation and result visibility.
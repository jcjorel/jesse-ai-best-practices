<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/tests/test_new_resources.py -->
<!-- Cached On: 2025-07-05T11:34:27.587020 -->
<!-- Source Modified: 2025-07-01T08:59:29.265995 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This test script validates knowledge resource functionality for the JESSE Framework MCP Server, specifically testing README.md resources in the `.knowledge/` directory structure. The script provides automated validation of knowledge base file existence, content verification, and resource registration processes for MCP server integration. Key semantic entities include `test_git_clones_readme()`, `test_pdf_knowledge_readme()`, `test_resource_registration()` functions, `register_knowledge_resources` import, `asyncio` async execution framework, `pathlib.Path` file system operations, and `.knowledge/git-clones/README.md` and `.knowledge/pdf-knowledge/README.md` file paths. The testing framework enables developers to verify that knowledge base resources are properly accessible through the MCP server with appropriate content validation and graceful handling of missing directories.

##### Main Components

The script contains three primary async test functions: `test_git_clones_readme()` for validating git clones knowledge base README file, `test_pdf_knowledge_readme()` for PDF knowledge directory validation, and `test_resource_registration()` for verifying MCP resource registration. The `main()` function orchestrates sequential test execution with formatted console output. Each test function implements file existence checking, content validation, and expected content pattern matching with emoji-based status reporting for visual test result differentiation.

###### Architecture & Design

The test architecture follows a sequential validation pattern where individual knowledge resources are tested independently before validating the overall registration process. The design implements file system validation using `os.path.exists()` checks combined with content analysis for expected headers and knowledge base references. The script uses graceful degradation for missing directories, treating them as expected conditions for new installations rather than failures. Error isolation ensures that individual test failures do not prevent execution of subsequent tests.

####### Implementation Approach

The testing strategy employs direct file system access using `os.path.exists()` and file reading operations with UTF-8 encoding for content validation. Content verification uses string containment checks for expected headers like "Git Clone Knowledge Bases Index" and knowledge base references like "FastMCP" and "Cline". The implementation includes character counting for content size validation and pattern matching for structural verification. Resource registration testing uses direct function calls to `register_knowledge_resources()` with exception handling for registration failures.

######## External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.resources.knowledge:register_knowledge_resources` - knowledge resource registration function
- `jesse_framework_mcp.main:server` - MCP server instance for integration context
- `fastmcp.Context` (external library) - MCP context interface specification
- `asyncio` (stdlib) - async execution framework
- `pathlib.Path` (stdlib) - file system path manipulation
- `os` (stdlib) - file existence and directory operations
- `.knowledge/git-clones/README.md` - git clones knowledge base index file
- `.knowledge/pdf-knowledge/README.md` - PDF knowledge base index file

**← Outbound:**
- Test execution reports consumed by developers for validation
- Console output with emoji-based status indicators for debugging
- Validation results for CI/CD pipeline integration

**⚡ System role and ecosystem integration:**
- **System Role**: Validation component ensuring knowledge base resources are properly configured and accessible through MCP server endpoints
- **Ecosystem Position**: Supporting test infrastructure for JESSE Framework knowledge management system validation
- **Integration Pattern**: Executed by developers during development and automated testing pipelines to verify knowledge resource availability and content integrity

######### Edge Cases & Error Handling

The script handles multiple edge cases including missing knowledge directories (treated as expected for new installations), missing README files (with appropriate warning messages), and content validation failures when expected headers or references are absent. Exception handling includes comprehensive error catching with string representation of exceptions for debugging. The testing framework differentiates between critical failures (registration errors) and expected conditions (missing PDF knowledge directory) using different emoji indicators and message types.

########## Internal Implementation Details

The test functions implement emoji-based status reporting using Unicode characters (`✅`, `❌`, `⚠️`) for immediate visual feedback on test results. File content validation includes character counting with length reporting and specific string pattern matching for expected content elements. The script uses UTF-8 encoding explicitly for file reading operations to handle international characters in knowledge base content. Resource registration testing validates that the registration process completes without exceptions rather than testing specific registration outcomes.

########### Code Usage Examples

**Basic knowledge resource file validation pattern:**

This code demonstrates file existence checking and content validation for knowledge base resources. It provides a foundation for testing README files in knowledge directories with appropriate error handling.

```python
# Test file existence and content validation for knowledge resources
readme_path = ".knowledge/git-clones/README.md"
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if "Git Clone Knowledge Bases Index" in content:
        print("✅ Git clones README contains expected header")
```

**Resource registration validation for MCP server integration:**

This pattern validates that knowledge resources register successfully with the MCP server. It ensures the registration process completes without exceptions and provides appropriate error reporting.

```python
# Validate that knowledge resources register successfully with MCP server
try:
    register_knowledge_resources()
    print("✅ Knowledge resources registered successfully")
except Exception as e:
    print(f"❌ Resource registration test failed: {str(e)}")
```

**Sequential test execution with formatted output:**

This approach orchestrates comprehensive knowledge resource validation with visual formatting. It provides structured test execution with clear section boundaries for debugging purposes.

```python
# Execute comprehensive knowledge resource validation suite
async def main():
    print("=" * 60)
    print("TESTING NEW WRITABLE RESOURCES")
    await test_git_clones_readme()
    await test_pdf_knowledge_readme()
    await test_resource_registration()
```
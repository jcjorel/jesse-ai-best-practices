<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/tests/test_new_resources.py -->
<!-- Cached On: 2025-07-06T19:33:45.534484 -->
<!-- Source Modified: 2025-07-01T08:59:29.265995 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This test script validates README.md resource functionality within the JESSE Framework MCP Server knowledge management system, specifically designed to verify knowledge base resource registration and file accessibility. The script provides automated testing capabilities for knowledge resource validation, file existence verification, and content structure analysis. Key semantic entities include `register_knowledge_resources`, `test_git_clones_readme`, `test_pdf_knowledge_readme`, `asyncio` async execution, `fastmcp.Context` integration, and `.knowledge/` directory structure with `git-clones/README.md` and `pdf-knowledge/README.md` paths. The testing framework implements emoji-based status reporting and graceful handling of missing knowledge directories for new installations.

##### Main Components

The script contains three primary async test functions: `test_git_clones_readme()` for git clones knowledge base validation, `test_pdf_knowledge_readme()` for PDF knowledge directory testing, and `test_resource_registration()` for resource registration verification. The `main()` function orchestrates sequential test execution with formatted output headers. Each test function implements file existence checking, content loading with UTF-8 encoding, and expected content pattern matching for knowledge base validation.

###### Architecture & Design

The architecture follows a sequential testing pattern with individual resource validation followed by registration testing. The design implements graceful degradation for missing directories, treating them as expected conditions for new installations rather than failures. Error handling is structured with try-catch blocks around each test function, providing isolated failure reporting. The testing framework uses file system operations combined with content analysis to validate both resource availability and structural integrity.

####### Implementation Approach

The implementation uses direct file system access through `os.path.exists()` for file validation and standard file reading with UTF-8 encoding for content analysis. Content validation employs string containment checks for expected headers like "Git Clone Knowledge Bases Index" and knowledge base references including "FastMCP" and "Cline". The testing strategy differentiates between critical failures (file access errors) and expected conditions (missing directories in new installations) through warning versus error status indicators.

######## External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.resources.knowledge:register_knowledge_resources` - knowledge resource registration function
- `jesse_framework_mcp.main:server` - MCP server instance import
- `fastmcp:Context` (external library) - MCP context interface
- `asyncio` (external library) - async execution framework
- `.knowledge/git-clones/README.md` - git clones knowledge base index file
- `.knowledge/pdf-knowledge/README.md` - PDF knowledge base index file
- `os` (external library) - file system operations
- `pathlib:Path` (external library) - path manipulation utilities

**← Outbound:**
- Console test output for validation reporting
- Test status indicators for CI/CD pipeline integration
- Knowledge resource validation reports for deployment verification

**⚡ System role and ecosystem integration:**
- **System Role**: Validation component ensuring knowledge base resources are properly accessible and registered within the MCP server ecosystem
- **Ecosystem Position**: Testing utility for knowledge management system integrity, validating the bridge between file system knowledge bases and MCP resource endpoints
- **Integration Pattern**: Executed by developers and deployment systems to verify knowledge resource availability before MCP server activation

######### Edge Cases & Error Handling

Error handling covers missing knowledge directories (treated as warnings for new installations), file access permission issues, UTF-8 encoding failures, and resource registration exceptions. The script handles missing expected content patterns through conditional validation reporting. Edge cases include partial knowledge directory structures, corrupted README files, and resource registration conflicts. The testing framework provides differentiated status reporting using emoji indicators to distinguish between critical errors, warnings, and successful validations.

########## Internal Implementation Details

File existence checking uses `os.path.exists()` with relative path resolution from the script execution directory. Content validation reads entire files into memory using UTF-8 encoding with automatic error handling. String pattern matching uses case-sensitive containment checks for specific headers and knowledge base names. The resource registration test performs function invocation without parameter validation, focusing on execution success rather than functional correctness.

########### Code Usage Examples

**Basic knowledge resource testing execution:**

This code snippet demonstrates how to execute all knowledge resource validation tests in sequence. The main function orchestrates comprehensive testing of git clones, PDF knowledge, and registration components.

```python
# Execute all knowledge resource validation tests
await main()
# Runs git clones, PDF knowledge, and registration tests sequentially
```

**Individual git clones README validation:**

This example shows how to test specific knowledge base accessibility and content structure validation. The function validates both file existence and expected content patterns for git clones knowledge base.

```python
# Test git clones knowledge base accessibility and content structure
await test_git_clones_readme()
# Validates .knowledge/git-clones/README.md existence and expected content patterns
```

**Resource registration verification:**

This snippet demonstrates how to verify knowledge resources register without errors in the MCP server. The registration function confirms that knowledge base resources are accessible through MCP endpoints.

```python
# Verify knowledge resources register without errors
register_knowledge_resources()
print("✅ Knowledge resources registered successfully")
# Confirms MCP server can access knowledge base resources
```
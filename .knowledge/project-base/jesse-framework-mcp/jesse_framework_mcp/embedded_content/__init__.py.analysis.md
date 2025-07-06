<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/embedded_content/__init__.py -->
<!-- Cached On: 2025-07-06T12:25:28.071372 -->
<!-- Source Modified: 2025-07-06T00:28:31.438687 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file serves as the embedded content access module for the Jesse Framework MCP project, providing programmatic access to JESSE framework rules and workflow files that are embedded within the Python package during the build process. The module enables runtime retrieval of framework documentation, rule content, and workflow definitions without requiring external file system dependencies or installation procedures. Key semantic entities include `EMBEDDED_CONTENT_DIR` path constant using `Path(__file__).parent` for module-relative file access, `get_jesse_rule_content()` function for retrieving `JESSE_*.md` rule files, `get_workflow_content()` function for accessing workflow files from the `workflows/` subdirectory, `list_jesse_rules()` function returning available rule names with `JESSE_` prefix stripping, `list_workflows()` function for workflow file enumeration, `get_all_embedded_files()` function providing comprehensive content dictionary, `FileNotFoundError` exception handling for missing files, `pathlib.Path` usage for cross-platform file operations, `typing.List` and `typing.Dict` type annotations for function signatures, and `utf-8` encoding specification for text file reading ensuring consistent character handling across different environments.

##### Main Components

The module contains six primary functions providing comprehensive embedded content access: `get_jesse_rule_content()` for retrieving individual JESSE rule file content by name, `get_workflow_content()` for accessing workflow files with automatic `.md` extension handling, `list_jesse_rules()` for enumerating available rule names with prefix normalization, `list_workflows()` for workflow file discovery and listing, `get_all_embedded_files()` for bulk content retrieval combining rules and workflows, and the `EMBEDDED_CONTENT_DIR` constant establishing the base path for all embedded content access. Supporting components include comprehensive error handling through `FileNotFoundError` exceptions, automatic file extension management for workflow names, rule name normalization converting from filename format to lowercase identifiers, and directory existence checking for the workflows subdirectory.

###### Architecture & Design

The architecture implements a module-centric embedded content access pattern using `pathlib.Path` for cross-platform file operations and relative path resolution from the module location. The design employs function-based API with consistent naming conventions, comprehensive type annotations using `typing` module, and standardized error handling through `FileNotFoundError` exceptions. The system uses directory-based organization separating JESSE rules in the root embedded content directory from workflows in a dedicated `workflows/` subdirectory. The architectural pattern includes automatic file extension handling, rule name normalization through prefix stripping and case conversion, and bulk access capabilities through dictionary-based content aggregation enabling efficient framework content distribution and runtime access.

####### Implementation Approach

The implementation uses `pathlib.Path` for robust cross-platform file operations with `__file__.parent` for module-relative path resolution ensuring embedded content accessibility regardless of installation location. The approach employs consistent file reading patterns using `read_text(encoding='utf-8')` for reliable character encoding, comprehensive error handling through `FileNotFoundError` with descriptive messages, and automatic file extension management for workflow names. Content discovery uses `glob()` patterns for file enumeration with specific filtering for `JESSE_*.md` and `*.md` files. Rule name processing implements prefix stripping and case conversion transforming filenames like `JESSE_KNOWLEDGE_MANAGEMENT.md` to lowercase identifiers like `knowledge_management`. Bulk content access combines individual retrieval functions with dictionary comprehension for efficient content aggregation.

######## External Dependencies & Integration Points

**→ Inbound:**
- `os` (external library) - operating system interface for environment variables and system operations
- `pathlib.Path` (external library) - cross-platform path manipulation and file system operations
- `typing.List` (external library) - type annotation for function return values and parameter specifications
- `typing.Dict` (external library) - type annotation for dictionary-based content aggregation functions
- Embedded JESSE rule files - `JESSE_*.md` files containing framework rules and standards
- Embedded workflow files - `workflows/*.md` files containing workflow definitions and procedures

**← Outbound:**
- Jesse Framework MCP server components - consume embedded content for rule enforcement and workflow execution
- Framework installation processes - use embedded content access for rule deployment and configuration
- Development tools and IDEs - access framework rules and workflows for development assistance
- Documentation generation systems - retrieve embedded content for comprehensive framework documentation
- Testing frameworks - access embedded content for validation and compliance testing procedures

**⚡ System role and ecosystem integration:**
- **System Role**: Core content access layer for the Jesse Framework MCP ecosystem, providing programmatic interface to embedded framework rules and workflows enabling runtime access without external dependencies
- **Ecosystem Position**: Central infrastructure component that bridges embedded framework content with consuming applications, ensuring consistent access to rules and workflows across different deployment scenarios
- **Integration Pattern**: Used by Jesse Framework components through direct function imports, integrated with MCP server operations for rule enforcement, and consumed by development tools for framework-aware assistance while maintaining encapsulation of embedded content location and structure

######### Edge Cases & Error Handling

The module addresses missing rule files through `FileNotFoundError` exceptions with descriptive messages indicating the specific file path that could not be found. Workflow file access handles missing `.md` extensions through automatic extension appending while preserving existing extensions when provided. Non-existent workflows directory scenarios return empty lists from `list_workflows()` rather than raising exceptions, enabling graceful degradation when workflow content is unavailable. File encoding issues are mitigated through explicit `utf-8` encoding specification in all `read_text()` operations. The system handles invalid rule names by raising `FileNotFoundError` when the constructed file path does not exist, providing clear feedback about missing content. Path resolution failures are prevented through module-relative path construction using `__file__.parent` ensuring consistent embedded content location regardless of execution context.

########## Internal Implementation Details

The `EMBEDDED_CONTENT_DIR` constant uses `Path(__file__).parent` for module-relative path resolution ensuring embedded content accessibility from the package installation location. Rule content retrieval constructs file paths using f-string formatting with `JESSE_{rule_name.upper()}.md` pattern and validates existence before reading. Workflow content access implements conditional extension appending using `endswith('.md')` checking and path construction through directory joining. File enumeration uses `glob()` patterns with specific filtering: `JESSE_*.md` for rules and `*.md` for workflows. Rule name normalization employs `stem.replace("JESSE_", "").lower()` for filename to identifier conversion. Content aggregation combines individual retrieval functions with dictionary comprehension, handling both rule and workflow content types. Error handling uses consistent `FileNotFoundError` raising with formatted error messages including the attempted file path for debugging purposes.

########### Code Usage Examples

This example demonstrates basic rule content retrieval using the module's primary access function. The function handles rule name normalization and provides clear error messages for missing content.

```python
# Retrieve specific JESSE rule content by name
from jesse_framework_mcp.embedded_content import get_jesse_rule_content

rule_content = get_jesse_rule_content('knowledge_management')
# Returns content of JESSE_KNOWLEDGE_MANAGEMENT.md file
```

This example shows workflow content access with automatic extension handling. The function accepts workflow names with or without the `.md` extension for flexible usage patterns.

```python
# Access workflow content with flexible naming
from jesse_framework_mcp.embedded_content import get_workflow_content

workflow_content = get_workflow_content('jesse_wip_task_create')
# Automatically appends .md extension and retrieves workflow content
```

This example illustrates comprehensive content enumeration and bulk access capabilities. The functions provide complete visibility into available embedded content for framework introspection.

```python
# Enumerate and access all embedded content
from jesse_framework_mcp.embedded_content import list_jesse_rules, list_workflows, get_all_embedded_files

available_rules = list_jesse_rules()
available_workflows = list_workflows()
all_content = get_all_embedded_files()
# Returns dictionary with all embedded files and their content
```
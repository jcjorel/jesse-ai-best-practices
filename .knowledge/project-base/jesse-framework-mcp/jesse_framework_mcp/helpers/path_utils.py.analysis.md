<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/helpers/path_utils.py -->
<!-- Cached On: 2025-07-05T14:03:57.520747 -->
<!-- Source Modified: 2025-07-03T23:03:51.098843 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements path resolution utilities for the Jesse Framework MCP server, providing portable path variable resolution and path prefix detection with cross-platform compatibility and bidirectional path conversion capabilities. The module enables reliable project root detection, portable path variable substitution, and comprehensive project setup validation without circular import dependencies. Key semantic entities include `get_project_root()` for priority-based project root discovery, `ensure_project_root()` for exception-based root validation, `get_project_relative_path()` for centralized path resolution, `validate_project_setup()` for comprehensive project diagnostics, `resolve_portable_path()` for variable-to-path transformation, `get_portable_path()` for path-to-variable conversion, `JESSE_PROJECT_ROOT` environment variable support, `.git` directory detection patterns, `pathlib.Path` cross-platform operations, portable path variables `{PROJECT_ROOT}`, `{HOME}`, `{CLINE_RULES}`, `{CLINE_WORKFLOWS}`, Jesse Framework directory structure validation including `.knowledge/`, `.knowledge/work-in-progress/`, `.knowledge/git-clones/`, `.knowledge/pdf-knowledge/`, `.knowledge/persistent-knowledge/`, and `.clinerules/`, and Windows absolute path detection with `C:\\` pattern recognition. The system implements single responsibility design for path variable resolution with bidirectional conversion supporting both variable resolution and prefix detection.

##### Main Components

The file contains six primary functions providing comprehensive path resolution and project management capabilities. The `get_project_root()` function implements priority-based project root discovery using `JESSE_PROJECT_ROOT` environment variable first, then upward `.git` directory traversal with filesystem root protection. The `ensure_project_root()` function wraps root detection with exception handling, converting None returns to descriptive ValueError exceptions with setup guidance. The `get_project_relative_path()` function provides centralized path resolution relative to detected project root using `ensure_project_root()` for validation. The `validate_project_setup()` function performs comprehensive project validation returning structured diagnostic information including root detection method, directory existence checks, and validation metadata. The `resolve_portable_path()` function transforms portable path variables into absolute filesystem paths with cross-platform variable substitution. The `get_portable_path()` function converts full pathnames to portable paths with MCP server supported variables using priority-based variable detection and Windows absolute path handling.

###### Architecture & Design

The architecture implements single responsibility principle with dedicated focus on path variable resolution and project root detection, avoiding circular import dependencies through independent operation. The design follows cross-platform path handling patterns using `pathlib.Path` for reliable filesystem operations across different operating systems. Key design patterns include the priority-based discovery pattern for project root detection, exception wrapper pattern for graceful error handling, bidirectional conversion pattern supporting both variable resolution and path prefix detection, and comprehensive validation pattern with structured diagnostic reporting. The system uses upward directory traversal with filesystem root protection, Windows absolute path detection for cross-platform compatibility, and priority-ordered variable matching from most specific to most general paths.

####### Implementation Approach

The implementation uses priority-based project root discovery with `JESSE_PROJECT_ROOT` environment variable taking precedence over automatic Git repository detection through upward directory traversal. Path variable resolution employs dictionary-based substitution with predefined variable mappings for `{PROJECT_ROOT}`, `{HOME}`, `{CLINE_RULES}`, and `{CLINE_WORKFLOWS}` using string replacement operations. Portable path conversion uses priority-ordered variable checking with `Path.is_relative_to()` for reliable path hierarchy detection and relative path calculation. The approach implements Windows absolute path detection using string pattern matching for `C:\\` format recognition and cross-platform path normalization with forward slash conversion. Error handling provides comprehensive exception management with descriptive error messages and graceful fallback to original paths when variable matching fails.

######## External Dependencies & Integration Points

**→ Inbound:**
- `os` (external library) - environment variable access for `JESSE_PROJECT_ROOT` configuration and system environment integration
- `pathlib.Path` (external library) - cross-platform filesystem operations, path resolution, and directory traversal capabilities
- `typing.Union` (external library) - type annotations for flexible parameter types supporting both string and Path objects
- `typing.Optional` (external library) - type annotations for optional return values and None handling patterns

**← Outbound:**
- Jesse Framework MCP server components - consuming project root detection for resource path resolution
- MCP resource implementations - using portable path resolution for cross-platform resource access
- Project setup validation workflows - consuming diagnostic information for troubleshooting and status reporting
- Configuration management systems - using path utilities for Jesse Framework directory structure validation

**⚡ System role and ecosystem integration:**
- **System Role**: Core path resolution infrastructure for Jesse Framework MCP server, providing fundamental project root detection and portable path variable management for all framework components
- **Ecosystem Position**: Central utility component serving as the foundation for path-related operations across the framework, enabling cross-platform compatibility and consistent path handling
- **Integration Pattern**: Used by MCP server components for project root detection, consumed by resource implementations for portable path resolution, and integrated with setup validation workflows for comprehensive project diagnostics

######### Edge Cases & Error Handling

The system handles missing project root scenarios by returning None from `get_project_root()` and providing descriptive exceptions from `ensure_project_root()` with setup guidance including both environment variable and Git repository options. Invalid `JESSE_PROJECT_ROOT` environment variable values are handled by continuing with Git repository detection rather than failing immediately. Filesystem root traversal is protected by checking `current != current.parent` to prevent infinite loops during upward directory searching. Windows absolute path detection handles cross-platform scenarios by recognizing `C:\\` patterns and preserving original path format when no variable matches are found. Path resolution failures are managed through comprehensive exception handling with OSError wrapping and descriptive error messages including original path information. Variable substitution handles missing or invalid paths gracefully by falling back to original path strings with forward slash normalization.

########## Internal Implementation Details

The project root detection uses `Path.cwd().resolve()` for current directory resolution and iterative parent directory traversal with `.git` directory existence checking. Environment variable handling employs `os.getenv()` with validation through `Path.exists()` and `Path.is_dir()` checks for directory verification. Path variable resolution uses dictionary-based string replacement with predefined variable mappings and exception wrapping for error handling. Portable path conversion implements priority-ordered checking using `Path.is_relative_to()` method for reliable hierarchy detection and `Path.relative_to()` for relative path calculation. Windows path detection uses string slicing with `path_str[1:3] == ':\\'` pattern matching for absolute path identification. The system maintains cross-platform compatibility through `pathlib.Path` operations and forward slash normalization using `str.replace('\\', '/')` for consistent path formatting.

########### Code Usage Examples

Basic project root detection demonstrates the fundamental pattern for Jesse Framework project discovery. This approach provides reliable project root identification with graceful error handling for missing or invalid project configurations.

```python
# Detect Jesse Framework project root with priority-based discovery
project_root = get_project_root()
if project_root:
    print(f"Project root found: {project_root}")
else:
    print("No project root detected - check JESSE_PROJECT_ROOT or Git repository")
```

Portable path resolution showcases the bidirectional conversion pattern for cross-platform path management. This pattern enables consistent path handling across different operating systems and development environments.

```python
# Convert between portable path variables and absolute filesystem paths
portable_path = "{PROJECT_ROOT}/.knowledge/work-in-progress/current-task"
absolute_path = resolve_portable_path(portable_path)

# Convert absolute path back to portable format with variable prefixes
full_path = "/home/user/project/.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md"
portable_format = get_portable_path(full_path)
# Returns: "{PROJECT_ROOT}/.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md"
```
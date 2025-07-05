<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/build_scripts/copy_jesse_content.py -->
<!-- Cached On: 2025-07-05T14:47:11.060620 -->
<!-- Source Modified: 2025-06-27T23:02:12.955791 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements a build-time script for copying complete JESSE framework content from the `artifacts/` directory to `embedded_content/` for MCP server packaging, providing automated framework distribution preparation during package builds. The script enables single source of truth copying from `artifacts/.clinerules/` at build time only, ensuring complete framework content including both rules and workflows is embedded in the MCP server package for runtime access. Key semantic entities include primary function `copy_jesse_content()` orchestrating the complete copying process, specialized functions `copy_jesse_rules()` and `copy_jesse_workflows()` for component-specific copying, utility function `find_jesse_project_root()` for project root discovery, `JesseBuildHook` class implementing `BuildHookInterface` for Hatchling integration, legacy function `hatch_build_hook()` for backward compatibility, imported modules `os`, `shutil`, and `pathlib.Path` for file operations, `get_jesse_rule_files()` import from constants module for centralized rule configuration, source directory path `artifacts/.clinerules/` containing JESSE framework files, destination directory `embedded_content/` for runtime embedding, and comprehensive error handling with `ValueError` and `FileNotFoundError` exceptions for missing components. The system implements defensive programming with descriptive error messages and complete framework copying including both rules and workflows through build system integration via Hatchling build hook.

##### Main Components

The file contains four primary functions, one class, one legacy function, and direct execution support providing comprehensive build-time copying functionality. The `copy_jesse_content()` function serves as the main orchestrator locating JESSE project root and coordinating rule and workflow copying operations. The `copy_jesse_rules()` function handles copying of all `JESSE_*.md` rule files from source to destination with individual file verification. The `copy_jesse_workflows()` function manages complete `workflows/` directory copying with recursive structure preservation and file counting. The `find_jesse_project_root()` function implements upward directory traversal to locate project root containing `artifacts/.clinerules/` structure. The `JesseBuildHook` class provides Hatchling build system integration implementing `BuildHookInterface` with `initialize()` method for build-time execution. The `hatch_build_hook()` legacy function maintains backward compatibility with older Hatchling versions. Direct execution support enables testing through `if __name__ == "__main__"` block.

###### Architecture & Design

The architecture implements a build-time copying pattern with clear separation between orchestration, component-specific copying, and build system integration, following single source of truth principles with defensive programming and comprehensive error handling. The design emphasizes complete framework copying ensuring both rules and workflows are included, build system integration through Hatchling build hooks, and project root discovery through directory hierarchy traversal. Key design patterns include the orchestrator pattern with `copy_jesse_content()` coordinating all copying operations, component separation pattern with dedicated functions for rules and workflows copying, build hook integration pattern implementing `BuildHookInterface` for Hatchling compatibility, defensive programming pattern with explicit error checking and descriptive messages, and single source of truth pattern copying from `artifacts/` directory at build time only. The system uses composition over inheritance with specialized functions for different copying aspects, centralized error handling with specific exception types, and build system integration maintaining compatibility across Hatchling versions.

####### Implementation Approach

The implementation uses directory traversal algorithms with `find_jesse_project_root()` performing upward search through parent directories until finding `artifacts/.clinerules/` marker. File copying employs `shutil.copy2()` for individual rule files preserving metadata and `shutil.copytree()` for complete workflow directory structure. The approach implements centralized configuration through `get_jesse_rule_files()` import eliminating hardcoded rule filenames and enabling dynamic rule list management. Project root discovery uses `pathlib.Path.resolve()` with parent directory iteration stopping at filesystem root to prevent infinite recursion. Error handling employs specific exception types with `ValueError` for project root location failures and `FileNotFoundError` for missing required files or directories. Build system integration uses `BuildHookInterface` implementation with `initialize()` method called during Hatchling build process. File verification includes existence checking before copying and post-copy counting for workflow files ensuring complete transfer.

######## External Dependencies & Integration Points

**→ Inbound:**
- `os` (external library) - operating system interface for path operations and file system access
- `shutil` (external library) - high-level file operations for copying with metadata preservation
- `pathlib.Path` (external library) - object-oriented filesystem paths for cross-platform compatibility
- `hatchling.builders.hooks.plugin.interface:BuildHookInterface` (external library) - Hatchling build system integration interface
- `constants:get_jesse_rule_files` - centralized rule configuration eliminating hardcoded filenames
- `artifacts/.clinerules/` - source JESSE framework files including rules and workflows directories
- `sys` (external library) - Python system interface for path manipulation and module importing

**← Outbound:**
- Hatchling build system - consuming `JesseBuildHook` class for build-time framework copying integration
- MCP server package - receiving copied framework content in `embedded_content/` directory for runtime access
- Package distribution systems - using embedded content for complete JESSE framework distribution
- Runtime MCP server - accessing embedded JESSE rules and workflows from `embedded_content/` structure
- Build verification systems - consuming file count reports and success/failure status from copying operations

**⚡ System role and ecosystem integration:**
- **System Role**: Build-time content preparation system for Jesse Framework MCP Server ecosystem, copying complete framework content from development artifacts to package-embedded structure for distribution
- **Ecosystem Position**: Critical build infrastructure component bridging between framework development in `artifacts/` and runtime distribution through embedded content packaging
- **Integration Pattern**: Used by Hatchling build system through build hook interface for automated copying during package creation, consumed by MCP server runtime for embedded framework access, and coordinated with constants module for centralized configuration management

######### Edge Cases & Error Handling

The system handles missing JESSE project root through `find_jesse_project_root()` returning None when `artifacts/.clinerules/` structure unavailable, triggering `ValueError` with descriptive guidance. Missing source directories are managed through existence checking with `FileNotFoundError` exceptions providing specific paths and resolution instructions. Individual rule file copying handles missing files through per-file existence verification with detailed error messages including expected file locations. Workflow directory copying manages missing `workflows/` directory through existence and type checking before `shutil.copytree()` execution. Build system integration handles initialization failures through exception propagation with build hook status reporting. Filesystem permission errors are managed through `shutil` exception handling with error context preservation. Directory traversal prevents infinite recursion through filesystem root detection comparing `current != current.parent`. Legacy build hook compatibility handles different Hatchling versions through separate function entry points with identical error handling patterns.

########## Internal Implementation Details

The module uses `sys.path.insert()` for dynamic import path manipulation enabling constants module access from parent directory structure. Project root discovery implements `Path.resolve()` with parent directory iteration using `while current != current.parent` loop termination at filesystem root. File copying operations use `shutil.copy2()` preserving file metadata including timestamps and permissions for individual rule files. Directory copying employs `shutil.copytree()` with `dirs_exist_ok=True` parameter allowing destination directory pre-existence. Rule file enumeration uses `get_jesse_rule_files()` import eliminating hardcoded lists and centralizing configuration management. Workflow verification implements `glob("*.md")` pattern matching for post-copy file counting and listing. Build hook integration uses `PLUGIN_NAME = "jesse_build_hook"` class attribute for Hatchling plugin identification. Error messages include specific file paths, expected directory structures, and resolution guidance for debugging build failures. Progress reporting uses print statements with checkmark symbols and file counts for build process visibility.

########### Code Usage Examples

Build hook integration demonstrates the primary usage pattern for Hatchling build system integration with automated JESSE framework copying. This approach provides seamless build-time content preparation without manual intervention.

```python
# Hatchling build system integration for automated JESSE framework copying
# Provides build-time content preparation from artifacts/ to embedded_content/
from build_scripts.copy_jesse_content import JesseBuildHook

# Build hook automatically triggered during package build process
# Copies complete JESSE framework including rules and workflows
hook = JesseBuildHook()
hook.initialize(version="1.0.0", build_data={})
# Framework content copied to embedded_content/ for runtime access
```

Direct execution showcases the testing and manual execution pattern for development and debugging scenarios. This pattern enables standalone script execution for build process verification and troubleshooting.

```python
# Direct execution for testing and manual framework copying
# Provides standalone copying capability for development and debugging
from build_scripts.copy_jesse_content import copy_jesse_content

# Manual execution for testing build process
try:
    copy_jesse_content()
    print("Framework copying completed successfully")
except (ValueError, FileNotFoundError) as e:
    print(f"Copying failed: {e}")
    # Handle missing artifacts/ directory or required files
```
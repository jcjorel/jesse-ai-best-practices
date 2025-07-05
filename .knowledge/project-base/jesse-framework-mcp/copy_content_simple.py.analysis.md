<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/copy_content_simple.py -->
<!-- Cached On: 2025-07-05T14:55:01.610649 -->
<!-- Source Modified: 2025-06-28T10:22:34.170539 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements a simplified JESSE framework content copying script for testing and development purposes, providing standalone functionality without Hatchling build system dependencies for copying complete JESSE rules and workflows from development artifacts to embedded content structure. The script enables developers to test content copying operations independently of the build system while maintaining identical functionality to the main build hook implementation. Key semantic entities include primary orchestration function `copy_jesse_content()` for complete framework copying workflow, specialized copying functions `copy_jesse_rules()` and `copy_jesse_workflows()` for component-specific operations, utility function `find_jesse_project_root()` for project root discovery through directory traversal, imported modules `os`, `shutil`, `pathlib.Path`, `typing.Optional`, and `sys` for file operations and system integration, centralized configuration import `get_jesse_rule_files()` from `constants` module for rule file enumeration, source directory path `artifacts/.clinerules/` containing JESSE framework files, destination directory `jesse_framework_mcp/embedded_content/` for runtime embedding, shebang line `#!/usr/bin/env python3` for direct script execution, comprehensive error handling with `ValueError` and `FileNotFoundError` exceptions for missing components, and progress reporting through print statements with checkmark symbols for operation visibility. The system implements identical copying logic to the main build hook while eliminating external build system dependencies for testing and development scenarios.

##### Main Components

The file contains four primary functions and direct execution support providing comprehensive JESSE framework content copying functionality without build system dependencies. The `copy_jesse_content()` function serves as the main orchestrator locating JESSE project root and coordinating rule and workflow copying operations with progress reporting. The `copy_jesse_rules()` function handles copying of all JESSE rule files from source to destination with individual file verification and success reporting. The `copy_jesse_workflows()` function manages complete workflows directory copying with recursive structure preservation, file counting, and verification listing. The `find_jesse_project_root()` function implements upward directory traversal to locate project root containing `artifacts/.clinerules/` structure. Direct execution support enables standalone script usage through `if __name__ == "__main__"` block with test execution and completion reporting.

###### Architecture & Design

The architecture implements a simplified build-time copying pattern with identical functionality to the main build hook but without external build system dependencies, following standalone script design principles with comprehensive error handling and progress reporting. The design emphasizes testing and development support through independent execution capability, identical copying logic to production build hooks ensuring consistency, and comprehensive error handling with descriptive messages for debugging. Key design patterns include the standalone script pattern enabling independent execution without build system integration, orchestrator pattern with main function coordinating all copying operations, component separation pattern with dedicated functions for rules and workflows copying, defensive programming pattern with explicit error checking and descriptive messages, and progress reporting pattern providing visibility into copying operations through console output. The system uses direct file operations with `shutil` for copying and `pathlib` for cross-platform path handling.

####### Implementation Approach

The implementation uses identical algorithms and data structures to the main build hook while eliminating Hatchling dependencies for standalone execution. Directory traversal employs upward search through parent directories until finding `artifacts/.clinerules/` marker for project root discovery. File copying operations use `shutil.copy2()` for individual rule files preserving metadata and `shutil.copytree()` for complete workflow directory structure. The approach implements centralized configuration through `get_jesse_rule_files()` import with dynamic path manipulation using `sys.path.insert()` for constants module access. Project root discovery uses `pathlib.Path.resolve()` with parent directory iteration stopping at filesystem root to prevent infinite recursion. Error handling employs specific exception types with detailed error messages including file paths and resolution guidance. Progress reporting uses print statements with checkmark symbols and file counts for operation visibility and verification.

######## External Dependencies & Integration Points

**→ Inbound:**
- `os` (external library) - operating system interface for path operations and file system access
- `shutil` (external library) - high-level file operations for copying with metadata preservation
- `pathlib.Path` (external library) - object-oriented filesystem paths for cross-platform compatibility
- `typing.Optional` (external library) - type hints for optional return values and function signatures
- `sys` (external library) - Python system interface for path manipulation and module importing
- `jesse_framework_mcp/constants:get_jesse_rule_files` - centralized rule configuration eliminating hardcoded filenames
- `artifacts/.clinerules/` - source JESSE framework files including rules and workflows directories

**← Outbound:**
- Development workflows - consuming script for testing content copying operations without build system overhead
- Testing environments - using standalone script for verifying content copying functionality and debugging
- Manual build processes - executing script for content preparation when automated build hooks unavailable
- Debugging scenarios - providing isolated content copying for troubleshooting build system issues
- `jesse_framework_mcp/embedded_content/` - generating embedded content structure for runtime MCP server access

**⚡ System role and ecosystem integration:**
- **System Role**: Standalone testing and development utility for Jesse Framework MCP Server ecosystem, providing identical content copying functionality to main build hook without build system dependencies
- **Ecosystem Position**: Support utility serving development and testing needs, enabling independent content copying verification and debugging scenarios outside automated build processes
- **Integration Pattern**: Used by developers for manual testing and debugging, executed independently for content copying verification, integrated with constants module for centralized configuration, and coordinated with main build hook for functionality consistency

######### Edge Cases & Error Handling

The system handles missing JESSE project root through `find_jesse_project_root()` returning None when `artifacts/.clinerules/` structure unavailable, triggering `ValueError` with descriptive guidance for project structure requirements. Missing source directories are managed through existence checking with `FileNotFoundError` exceptions providing specific paths and resolution instructions for required directory structure. Individual rule file copying handles missing files through per-file existence verification with detailed error messages including expected file locations and setup guidance. Workflow directory copying manages missing workflows directory through existence and type checking before `shutil.copytree()` execution preventing copy failures. Constants module import handles path manipulation failures through `sys.path.insert()` with relative path resolution for module access. Directory traversal prevents infinite recursion through filesystem root detection comparing `current != current.parent` ensuring termination at system boundaries. File system permission errors are managed through `shutil` exception handling with error context preservation for troubleshooting access issues.

########## Internal Implementation Details

The script uses shebang line `#!/usr/bin/env python3` for direct execution with Python 3 interpreter discovery. Module docstring provides clear description of purpose and distinguishes from main build hook implementation. Path manipulation uses `sys.path.insert(0, str(Path(__file__).parent / "jesse_framework_mcp"))` for constants module access from relative directory structure. Project root discovery implements `Path.resolve()` with parent directory iteration using `while current != current.parent` loop termination at filesystem root. File copying operations use `shutil.copy2()` preserving file metadata including timestamps and permissions for individual rule files. Directory copying employs `shutil.copytree()` with `dirs_exist_ok=True` parameter allowing destination directory pre-existence during repeated executions. Rule file enumeration uses `get_jesse_rule_files()` import eliminating hardcoded lists and centralizing configuration management. Workflow verification implements `glob("*.md")` pattern matching for post-copy file counting and listing verification. Progress reporting uses print statements with Unicode checkmark symbols and descriptive messages for operation visibility.

########### Code Usage Examples

Standalone script execution demonstrates the primary testing pattern for JESSE framework content copying without build system dependencies. This approach enables developers to verify content copying functionality independently for debugging and development scenarios.

```python
# Direct script execution for testing JESSE framework content copying functionality
# Provides standalone copying capability without Hatchling or build system dependencies
#!/usr/bin/env python3

# Execute script directly for testing and verification
if __name__ == "__main__":
    print("Testing JESSE content copying...")
    copy_jesse_content()
    print("Test completed successfully")
```

Content copying workflow showcases the complete framework copying process with project root discovery and component-specific operations. This pattern demonstrates the identical functionality to the main build hook while maintaining independence from build system integration.

```python
# Complete JESSE framework content copying with project root discovery and error handling
# Replicates build hook functionality for testing and development scenarios
def copy_jesse_content() -> None:
    # Find JESSE project root through directory traversal
    current_dir = Path.cwd()
    jesse_project_root = find_jesse_project_root(current_dir)
    
    if not jesse_project_root:
        raise ValueError("Could not locate JESSE project with artifacts/ directory")
    
    # Copy JESSE rules and workflows with progress reporting
    source_dir = jesse_project_root / "artifacts" / ".clinerules"
    dest_dir = Path("jesse_framework_mcp") / "embedded_content"
    copy_jesse_rules(source_dir, dest_dir)
    copy_jesse_workflows(source_dir, dest_dir)
```
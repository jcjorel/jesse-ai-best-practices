<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/tests/test_project_root.py -->
<!-- Cached On: 2025-07-04T00:27:28.316038 -->
<!-- Source Modified: 2025-07-03T23:07:27.466816 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This test script validates project root detection functionality for the JESSE Framework MCP Server, providing comprehensive testing of path resolution mechanisms, environment variable detection, and session initialization workflows. The script enables developers to verify proper project setup and diagnose configuration issues through automated test suites that examine `get_project_root()`, `ensure_project_root()`, `get_project_relative_path()`, `validate_project_setup()` functions alongside `get_project_setup_guidance()` and `get_session_init_context()` resources. Key semantic entities include `asyncio` event loop management, `pathlib.Path` operations, `argparse` command-line interface, `JESSE_PROJECT_ROOT` environment variable, `.git` repository detection, and HTTP-style content sections for MCP resource validation.

##### Main Components

The script contains two primary async test functions: `test_project_root_detection()` which executes five sequential validation tests for basic root detection, environment variables, Git repository discovery, setup guidance generation, and project validation reporting; and `test_session_init_with_project_root()` which creates a mock context class with logging methods and tests the complete session initialization resource workflow. Supporting components include `parse_arguments()` for command-line option processing, `main()` orchestration function with dump/normal mode switching, and a `TestContext` class providing async logging interface methods (`info`, `error`, `warning`, `debug`, `report_progress`).

###### Architecture & Design

The script follows an async-first testing architecture with clear separation between detection logic testing and resource integration testing. The design implements a mock context pattern using a local `TestContext` class that simulates the MCP server's logging interface, enabling isolated testing of resource functions without full server initialization. The architecture supports dual execution modes through command-line arguments: normal comprehensive testing mode and content dump mode for resource inspection, with error handling and progress reporting integrated throughout the test flow.

####### Implementation Approach

The implementation uses sequential async test execution with detailed console output formatting using emoji indicators (🧪, ✅, ❌, ℹ️, ⚠️, 🐛, 📊) for visual test result identification. The script employs direct function imports from `jesse_framework_mcp.helpers.path_utils` and `jesse_framework_mcp.helpers.project_setup` modules, with dynamic path manipulation using `sys.path.insert()` for package discovery. Key technical strategies include environment variable inspection via `os.getenv('JESSE_PROJECT_ROOT')`, filesystem traversal for `.git` directory detection, and FastMCP function unwrapping through `unwrap_fastmcp_function()` utility for proper resource testing.

######## Code Usage Examples

Execute comprehensive project root testing with detailed output:

```python
# Run all project detection tests
python test_project_root.py

# Expected output includes project root detection, environment validation,
# Git repository discovery, and session initialization testing
```

Dump complete session initialization resource content for inspection:

```python
# Output raw resource content without test formatting
python test_project_root.py --dump

# Returns the complete HTTP-style resource content that would be
# provided to MCP clients during session initialization
```

Test individual project validation components programmatically:

```python
from jesse_framework_mcp.helpers.path_utils import validate_project_setup
validation = validate_project_setup()
for key, value in validation.items():
    print(f"{key}: {value}")
```

######### External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.helpers.path_utils` - core path detection functions (`get_project_root`, `ensure_project_root`, `get_project_relative_path`, `validate_project_setup`)
- `jesse_framework_mcp.helpers.project_setup` - setup guidance generation (`get_project_setup_guidance`)
- `jesse_framework_mcp.resources.session_init` - session initialization resource (`get_session_init_context`)
- `utils.py` - FastMCP function unwrapping utility (`unwrap_fastmcp_function`)
- `pathlib.Path` (stdlib) - filesystem path operations and resolution
- `asyncio` (stdlib) - async test execution and event loop management
- `argparse` (stdlib) - command-line argument parsing for execution modes

**← Outbound:**
- `console/terminal` - formatted test output with emoji indicators and progress reporting
- `JESSE_PROJECT_ROOT` environment variable - detection and validation testing
- `.git/` directory - Git repository detection validation
- `sys.path` - Python module path modification for package imports

**⚡ Integration:**
- Protocol: Direct function imports and async function calls
- Interface: Async test functions with mock context objects and console output
- Coupling: Tight coupling to JESSE Framework MCP modules, loose coupling to external environment

########## Edge Cases & Error Handling

The script handles missing project root scenarios by testing setup guidance generation and validating that appropriate fallback content is provided when `get_project_root()` returns `None`. Error handling includes comprehensive exception catching in the main execution flow with traceback printing for debugging, keyboard interrupt handling for graceful test termination, and validation of empty or missing resource content from session initialization. The script addresses scenarios where `JESSE_PROJECT_ROOT` environment variable is unset, Git repositories are not found in the directory hierarchy, and FastMCP function unwrapping fails during resource testing.

########### Internal Implementation Details

The script uses `sys.path.insert(0, str(Path(__file__).parent))` for dynamic package path resolution, enabling execution from various directory contexts without installation requirements. The `TestContext` class implements async logging methods that mirror the actual MCP server context interface, with conditional output suppression in dump mode to prevent interference with resource content extraction. Internal mechanics include string-based content analysis for detecting setup guidance versus actual session content, section counting using `result.count("Content-Type:")` for HTTP-style resource validation, and character count reporting for content size verification. The argument parser uses `RawDescriptionHelpFormatter` to preserve example formatting in help text, with boolean flag handling for execution mode switching.
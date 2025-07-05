<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/pyproject.toml -->
<!-- Cached On: 2025-07-05T14:53:52.394588 -->
<!-- Source Modified: 2025-07-01T17:30:44.433518 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements the Python package configuration for the Jesse Framework MCP Server, providing comprehensive build system setup with custom build hooks for embedding JESSE framework content at package creation time. The configuration enables automated distribution of a self-contained MCP server that includes all JESSE rules and workflows without requiring separate framework installation. Key semantic entities include build system configuration `hatchling` with `hatch-vcs` for version control integration, project metadata `name = "jesse-framework-mcp"` with `version = "0.1.0"` and `description = "MCP Server for JESSE AI Framework - Complete Rules and Workflows"`, runtime dependencies `fastmcp~=2.9.2`, `boto3>=1.38.46`, `strands-agents>=0.1.0`, and `mistletoe>=1.4.0` for MCP protocol and framework functionality, Python version requirement `requires-python = ">=3.10"` for FastMCP v2.9.2 compatibility, custom build hook configuration `[tool.hatch.build.hooks.custom]` with `path = "build_scripts/copy_jesse_content.py"` for JESSE content embedding, console script entry point `jesse-framework-mcp = "jesse_framework_mcp:main"` for command-line execution, development dependencies including `pytest>=7.0.0`, `black>=22.0.0`, `isort>=5.10.0`, `mypy>=0.950` for code quality, package data configuration for `embedded_content/*.md` and `embedded_content/workflows/*.md` files, and tool configurations for `black`, `isort`, `mypy`, and `pytest` with specific settings for Python 3.10+ development workflows. The system implements build-time integration of JESSE framework content through Hatchling custom hooks enabling portable MCP server distribution.

##### Main Components

The configuration contains eight primary sections providing comprehensive Python package setup with build-time content embedding capabilities. The `[build-system]` section defines Hatchling as the build backend with version control support. The `[project]` section establishes package metadata including name, version, description, authors, license, Python version requirements, and runtime dependencies. The `[project.urls]` section provides repository and documentation links. The `[project.scripts]` section defines the console script entry point for command-line execution. The `[tool.hatch.build.hooks.custom]` section configures custom build hooks for JESSE content copying. The `[tool.hatch.build.targets.wheel.shared-data]` section includes embedded content in wheel distribution. The `[project.optional-dependencies]` section defines development dependencies for testing and code quality. The tool configuration sections provide settings for Black, isort, mypy, and pytest development tools.

###### Architecture & Design

The architecture implements a modern Python packaging pattern with Hatchling build system integration, following PEP 517/518 standards with custom build hooks for content embedding and comprehensive development tool configuration. The design emphasizes build-time content integration through custom hooks that copy JESSE framework content from `artifacts/` directory to `embedded_content/` for package distribution, runtime dependency management with specific version constraints for MCP protocol compatibility, and development workflow support through comprehensive tool configurations. Key design patterns include the custom build hook pattern enabling build-time content processing, embedded content pattern packaging framework rules and workflows within the distribution, console script pattern providing command-line interface through entry points, development dependency pattern separating runtime and development requirements, and tool configuration pattern centralizing code quality and testing settings. The system uses Hatchling's extensible build system with shared data inclusion for embedded content distribution.

####### Implementation Approach

The implementation uses TOML configuration format with structured sections for build system, project metadata, dependencies, and tool configurations following Python packaging standards. Build-time content embedding employs custom Hatchling hooks executing `build_scripts/copy_jesse_content.py` during package creation. The approach implements version constraint management with tilde requirements for FastMCP compatibility and minimum version specifications for supporting libraries. Development workflow integration uses optional dependencies with comprehensive tool configurations for code formatting, type checking, and testing. Package data inclusion uses both Hatchling shared-data configuration and setuptools compatibility patterns for embedded content distribution. Console script configuration provides direct command-line access through Python entry points. Tool configurations specify Python 3.10+ target versions with appropriate settings for modern development workflows.

######## External Dependencies & Integration Points

**→ References:**
- `hatchling` (external library) - modern Python build backend providing PEP 517/518 compliance and custom hook support
- `hatch-vcs` (external library) - version control integration for Hatchling build system
- `fastmcp~=2.9.2` (external library) - FastMCP framework for MCP protocol implementation and server functionality
- `boto3>=1.38.46` (external library) - AWS SDK for cloud service integration and resource management
- `strands-agents>=0.1.0` (external library) - agent framework for AI assistant functionality
- `mistletoe>=1.4.0` (external library) - Markdown parsing and processing for documentation handling
- `build_scripts/copy_jesse_content.py` - custom build hook script for JESSE framework content embedding
- `jesse_framework_mcp/__init__.py:main` - package entry point for console script execution

**← Referenced By:**
- Python package managers - consuming configuration for installation and dependency resolution
- Build systems - using Hatchling configuration for package creation and distribution
- Development environments - referencing tool configurations for code quality and testing workflows
- CI/CD pipelines - using build configuration for automated package creation and testing
- Distribution platforms - consuming package metadata for PyPI publication and discovery
- Installation tools - using console script configuration for command-line interface setup

**⚡ System role and ecosystem integration:**
- **System Role**: Core package configuration for Jesse Framework MCP Server ecosystem, defining build system, dependencies, and distribution parameters for complete MCP server packaging with embedded JESSE framework content
- **Ecosystem Position**: Central configuration component enabling automated build processes, dependency management, and development workflows for the entire MCP server project
- **Integration Pattern**: Used by Python packaging tools for build and distribution, consumed by development environments for tool configuration, integrated with custom build hooks for content embedding, and coordinated with package managers for dependency resolution and installation

######### Edge Cases & Error Handling

The configuration addresses Python version compatibility through explicit `requires-python = ">=3.10"` requirement ensuring FastMCP v2.9.2 compatibility. Build hook failures are managed through Hatchling's error handling with custom hook path validation. Dependency conflicts are addressed through specific version constraints with tilde requirements for compatible updates and minimum version specifications for security and functionality requirements. Development environment variations are handled through optional dependencies separating runtime and development requirements. Package data inclusion uses dual configuration patterns for Hatchling and setuptools compatibility ensuring embedded content distribution across different build environments. Tool configuration compatibility addresses Python version targeting with specific settings for modern development workflows. Build system fallbacks are managed through standard Hatchling error handling and build backend specifications.

########## Internal Implementation Details

The configuration uses TOML syntax with structured sections following Python packaging standards and Hatchling-specific extensions. Project metadata includes comprehensive classifiers for Python versions 3.10, 3.11, and 3.12 with development status and intended audience specifications. Dependency specifications use semantic versioning with tilde constraints for compatible updates and greater-than-equal constraints for minimum requirements. Custom build hook configuration specifies exact path `build_scripts/copy_jesse_content.py` for content copying execution. Shared data configuration maps `embedded_content` directory to `jesse_framework_mcp/embedded_content` for package inclusion. Tool configurations specify line length 88 for Black, profile "black" for isort, Python version "3.10" for mypy, and asyncio mode "auto" for pytest. Console script configuration maps `jesse-framework-mcp` command to `jesse_framework_mcp:main` function for direct execution.

########### Usage Examples

Package installation demonstrates the primary distribution pattern for Jesse Framework MCP Server with automated dependency resolution. This approach provides complete MCP server installation with embedded JESSE framework content through standard Python packaging tools.

```bash
# Standard package installation using pip with automatic dependency resolution
# Installs MCP server with embedded JESSE framework content and all required dependencies
pip install jesse-framework-mcp

# Development installation with optional dependencies for code quality and testing
# Enables complete development workflow with formatting, type checking, and testing tools
pip install jesse-framework-mcp[dev]
```

Build configuration showcases the custom hook pattern for JESSE framework content embedding during package creation. This configuration enables automated content copying from development artifacts to package distribution.

```toml
# Custom build hook configuration for JESSE framework content embedding
# Executes content copying script during package build process
[tool.hatch.build.hooks.custom]
path = "build_scripts/copy_jesse_content.py"

# Embedded content inclusion in wheel distribution
# Maps source directory to package location for runtime access
[tool.hatch.build.targets.wheel.shared-data]
"embedded_content" = "jesse_framework_mcp/embedded_content"
```

Development workflow configuration demonstrates the tool integration pattern for code quality and testing. This setup provides comprehensive development environment with consistent formatting, type checking, and testing capabilities.

```toml
# Development dependencies for comprehensive code quality workflow
# Provides testing, formatting, linting, and type checking capabilities
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "black>=22.0.0",
    "isort>=5.10.0",
    "mypy>=0.950",
]

# Tool configurations for consistent development environment
# Specifies Python 3.10+ targeting with modern development practices
[tool.black]
line-length = 88
target-version = ['py310']

[tool.mypy]
python_version = "3.10"
disallow_untyped_defs = true
```
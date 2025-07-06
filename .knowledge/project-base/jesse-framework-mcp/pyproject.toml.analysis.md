<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/pyproject.toml -->
<!-- Cached On: 2025-07-06T12:29:39.018002 -->
<!-- Source Modified: 2025-07-06T00:52:31.904461 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file serves as the Python package configuration for the Jesse Framework MCP Server, defining build system requirements, dependencies, and metadata for distributing the complete JESSE AI Framework rules and workflows as an MCP-compatible server package. The configuration enables build-time embedding of JESSE framework content from the `artifacts/` directory through custom build hooks, providing a self-contained MCP server distribution with integrated framework governance. Key semantic entities include `hatchling` build system with `hatch-vcs` version control integration, `fastmcp~=2.9.2` as the primary MCP protocol implementation, `jesse-framework-mcp` package name with version `0.1.0`, `build_scripts/copy_jesse_content.py` custom build hook for content embedding, `jesse_framework_mcp/embedded_content/` directory for framework rules and workflows, `boto3>=1.38.46` for AWS service integration, `strands-agents>=0.1.0` for agent framework support, `mistletoe>=1.4.0` for markdown processing, `PyYAML>=6.0` for YAML output generation, `requires-python = ">=3.10"` compatibility requirement, and comprehensive development tooling configuration including `pytest`, `black`, `isort`, `flake8`, and `mypy` for code quality assurance.

##### Main Components

The configuration contains eight primary sections defining package structure and build behavior: `build-system` section specifying `hatchling` and `hatch-vcs` requirements, `project` section with package metadata including name, version, description, authors, and dependencies, `project.urls` section providing repository and documentation links, `project.scripts` section defining the `jesse-framework-mcp` command-line entry point, `tool.hatch.build.hooks.custom` section configuring the build-time content copying hook, `tool.hatch.build.targets.wheel.shared-data` section for embedded content distribution, `project.optional-dependencies` section with development tools, and comprehensive tool configuration sections for `black`, `isort`, `mypy`, and `pytest`. Supporting components include `tool.setuptools.package-data` for setuptools compatibility, `dependency-groups` for modern dependency management, and detailed Python version classifiers supporting 3.10, 3.11, and 3.12.

###### Architecture & Design

The architecture implements a build-time content embedding pattern using `hatchling` build system with custom hooks to integrate JESSE framework rules and workflows into the Python package distribution. The design employs a modular dependency structure with `fastmcp` as the core MCP protocol implementation, supplemented by specialized libraries for AWS integration, agent frameworks, markdown processing, and YAML generation. The system uses shared data distribution through wheel packaging to include embedded content in the final package, ensuring framework rules and workflows are available at runtime without external dependencies. The architectural pattern includes comprehensive development tooling integration with code formatting, linting, type checking, and testing frameworks configured for Python 3.10+ compatibility.

####### Implementation Approach

The implementation uses `hatchling` build backend with custom build hooks executing `build_scripts/copy_jesse_content.py` to embed JESSE framework content during package creation. The approach employs version pinning strategies with compatible version ranges (`~=2.9.2` for FastMCP, `>=1.38.46` for boto3) ensuring stable dependency resolution while allowing patch updates. Package data inclusion uses both modern `tool.hatch.build.targets.wheel.shared-data` configuration and legacy `tool.setuptools.package-data` for broad compatibility. Development workflow integration implements standardized tooling with `black` for code formatting, `isort` for import organization, `mypy` for type checking, and `pytest` for testing with asyncio support. The build process coordinates content copying, dependency resolution, and package assembly to produce a self-contained MCP server distribution.

######## External Dependencies & Integration Points

**→ References:**
- `hatchling` (external library) - modern Python build backend providing package creation and distribution capabilities
- `hatch-vcs` (external library) - version control integration for automatic version management from Git tags
- `fastmcp~=2.9.2` (external library) - FastMCP framework implementing MCP protocol for server functionality
- `boto3>=1.38.46` (external library) - AWS SDK for Python enabling cloud service integration
- `strands-agents>=0.1.0` (external library) - agent framework for AI assistant coordination and management
- `mistletoe>=1.4.0` (external library) - markdown parser and renderer for processing framework documentation
- `PyYAML>=6.0` (external library) - YAML processing library for configuration and data serialization
- `build_scripts/copy_jesse_content.py` - custom build hook script for embedding JESSE framework content

**← Referenced By:**
- Python package installers - `pip`, `poetry`, `conda` consume this configuration for package installation and dependency resolution
- CI/CD build systems - automated build pipelines reference this configuration for package creation and distribution
- Development environments - IDEs and development tools use tool configurations for code formatting and quality checks
- Package distribution platforms - PyPI and other repositories use metadata for package indexing and discovery
- MCP client applications - consume the built package as an MCP server providing JESSE framework functionality
- Docker containers and deployment systems - reference package configuration for containerized deployments

**⚡ System role and ecosystem integration:**
- **System Role**: Central package configuration defining the complete build, distribution, and runtime requirements for the Jesse Framework MCP Server, enabling seamless integration of JESSE framework rules with MCP protocol implementation
- **Ecosystem Position**: Core infrastructure component that bridges JESSE framework content with Python packaging ecosystem, ensuring framework rules and workflows are distributed as a standard Python package with MCP server capabilities
- **Integration Pattern**: Consumed by Python build tools for package creation, referenced by dependency managers for installation, and used by development tools for code quality assurance while coordinating build-time content embedding with runtime MCP server functionality

######### Edge Cases & Error Handling

The configuration addresses Python version compatibility issues through explicit `requires-python = ">=3.10"` specification ensuring FastMCP v2.9.2 compatibility requirements are met. Build hook failures are mitigated through the custom `copy_jesse_content.py` script which handles missing source content and provides error reporting during package creation. Dependency resolution conflicts are managed through version pinning strategies using compatible version specifiers (`~=` for patch-level updates, `>=` for minimum versions) preventing incompatible library combinations. Development tool configuration includes error handling through `mypy` type checking with `warn_return_any` and `disallow_untyped_defs` flags catching type-related issues. The system handles package data inclusion failures through dual configuration using both modern hatchling and legacy setuptools specifications ensuring broad compatibility across different installation environments.

########## Internal Implementation Details

The build system uses `hatchling.build` backend with custom hook integration executing during package creation to embed JESSE framework content from the `artifacts/` directory into `jesse_framework_mcp/embedded_content/`. Dependency management employs semantic versioning with `fastmcp~=2.9.2` allowing patch updates while preventing minor version changes that could introduce breaking changes. Package data configuration uses `tool.hatch.build.targets.wheel.shared-data` mapping `embedded_content` to the package directory structure ensuring framework rules and workflows are included in wheel distributions. Development tooling configuration implements standardized settings with `black` line length of 88 characters, `isort` black profile compatibility, `mypy` strict type checking for Python 3.10, and `pytest` asyncio mode for testing MCP server functionality. The entry point configuration maps `jesse-framework-mcp` command to `jesse_framework_mcp:main` function enabling command-line server execution.

########### Code Usage Examples

This example demonstrates the package installation and basic usage pattern for the Jesse Framework MCP Server. The installation process includes all embedded JESSE framework content through the build-time copying mechanism.

```bash
# Install the Jesse Framework MCP Server package with all dependencies
pip install jesse-framework-mcp

# Run the MCP server with stdio transport for client communication
jesse-framework-mcp
```

This example shows the development environment setup using the optional development dependencies. The configuration enables comprehensive code quality checking and testing capabilities for framework development.

```bash
# Install development dependencies for contributing to the framework
pip install jesse-framework-mcp[dev]

# Run code quality checks using configured tools
black --check .
isort --check-only .
flake8 .
mypy .
pytest
```

This example illustrates the build process configuration showing how JESSE framework content is embedded during package creation. The custom build hook ensures framework rules and workflows are included in the distribution.

```toml
# Build system configuration with custom content embedding
[tool.hatch.build.hooks.custom]
path = "build_scripts/copy_jesse_content.py"

# Embedded content distribution in wheel packages
[tool.hatch.build.targets.wheel.shared-data]
"embedded_content" = "jesse_framework_mcp/embedded_content"
```
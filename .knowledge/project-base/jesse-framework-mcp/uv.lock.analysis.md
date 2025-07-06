<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/uv.lock -->
<!-- Cached On: 2025-07-06T12:31:54.517724 -->
<!-- Source Modified: 2025-07-06T00:52:40.692511 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file serves as the dependency lock file for the Jesse Framework MCP Server project, providing deterministic package resolution and version pinning for all direct and transitive dependencies across the Python ecosystem. The lock file ensures reproducible builds and consistent development environments by specifying exact versions, checksums, and source locations for every package required by the project. Key semantic entities include `uv.lock` format with `version = 1` and `revision = 1` metadata, `requires-python = ">=3.10"` compatibility specification, `jesse-framework-mcp` as the main package with `version = "0.1.0"` and `source = { editable = "." }` configuration, comprehensive dependency graph including `fastmcp~=2.9.2` for MCP protocol implementation, `boto3>=1.38.46` for AWS integration, `strands-agents>=0.1.0` for agent framework support, `mistletoe>=1.4.0` for markdown processing, `PyYAML>=6.0` for YAML handling, development dependencies including `pytest>=8.4.1`, `black>=25.1.0`, `mypy>=1.16.1`, and `flake8>=7.3.0`, with detailed package metadata containing SHA256 hashes, wheel URLs, and source distribution information ensuring cryptographic verification and supply chain security for all dependencies.

##### Main Components

The lock file contains 77 distinct package entries organized into a flat dependency structure with comprehensive metadata for each package. Primary components include the main project package `jesse-framework-mcp` with editable source configuration and optional development dependencies, core runtime dependencies such as `fastmcp`, `boto3`, `strands-agents`, `mistletoe`, and `pyyaml`, development tooling packages including `pytest`, `pytest-asyncio`, `black`, `isort`, `flake8`, and `mypy`, and extensive transitive dependencies covering cryptography (`cryptography`, `cffi`), HTTP clients (`httpx`, `httpcore`, `h11`), async frameworks (`anyio`, `starlette`, `uvicorn`), data validation (`pydantic`, `pydantic-core`), and utility libraries (`click`, `rich`, `typer`). Each package entry includes version specifications, source registry information, dependency relationships, and cryptographic verification data through SHA256 hashes for both source distributions and wheel files.

###### Architecture & Design

The architecture implements a comprehensive dependency resolution system using the `uv` package manager format with deterministic version locking and cryptographic verification. The design employs a flat package structure where each dependency is explicitly listed with complete metadata including version constraints, source locations, and integrity checksums. The system uses semantic versioning with compatible version ranges (`~=` for patch-level updates, `>=` for minimum versions) while locking to specific versions for reproducibility. The architectural pattern includes conditional dependencies based on Python version markers (`python_full_version < '3.11'`, `python_full_version < '3.13'`) and platform-specific markers (`sys_platform == 'win32'`, `platform_python_implementation != 'PyPy'`), comprehensive wheel distribution support across multiple platforms (macOS, Linux, Windows) and architectures (x86_64, ARM64, i686), and development dependency separation through optional dependency groups enabling different installation profiles.

####### Implementation Approach

The implementation uses the `uv` lock file format version 1 with revision 1, providing structured dependency resolution with exact version pinning and cryptographic verification through SHA256 hashes. The approach employs comprehensive package metadata including source registry URLs (`https://pypi.org/simple`), wheel and source distribution URLs with integrity hashes, and dependency relationship mapping with conditional markers. Version resolution implements semantic versioning constraints while locking to specific versions ensuring reproducible builds across different environments. The system handles platform-specific dependencies through conditional markers, supports both wheel and source distribution installations, and maintains separate dependency groups for development and runtime requirements. Package verification uses SHA256 checksums for both wheel files and source distributions, ensuring supply chain security and preventing dependency tampering.

######## External Dependencies & Integration Points

**→ References:**
- `https://pypi.org/simple` - primary package index registry for all external dependencies and package resolution
- `https://files.pythonhosted.org/packages/` - CDN hosting wheel and source distribution files with SHA256 verification
- `fastmcp~=2.9.2` (external library) - FastMCP framework for MCP protocol implementation and server functionality
- `boto3>=1.38.46` (external library) - AWS SDK for Python enabling cloud service integration and API access
- `strands-agents>=0.1.0` (external library) - agent framework for AI assistant coordination and management capabilities
- `mistletoe>=1.4.0` (external library) - markdown parser and renderer for processing framework documentation
- `PyYAML>=6.0` (external library) - YAML processing library for configuration and data serialization operations

**← Referenced By:**
- `uv` package manager - consumes lock file for deterministic dependency resolution and installation operations
- CI/CD build systems - reference lock file for consistent dependency installation across build environments
- Development environments - use lock file to ensure consistent package versions across team members
- Docker containers - leverage lock file for reproducible container builds with exact dependency versions
- Package distribution systems - reference dependency specifications for package metadata and requirements
- Security scanning tools - analyze lock file for vulnerability detection and dependency audit procedures

**⚡ System role and ecosystem integration:**
- **System Role**: Central dependency management artifact for the Jesse Framework MCP Server, ensuring deterministic package resolution and reproducible builds across all deployment environments
- **Ecosystem Position**: Critical infrastructure component that defines the complete dependency graph for the project, enabling consistent development, testing, and production deployments
- **Integration Pattern**: Consumed by package managers for installation, referenced by CI/CD systems for build reproducibility, and used by security tools for vulnerability scanning while maintaining cryptographic verification of all dependencies through SHA256 checksums

######### Edge Cases & Error Handling

The lock file addresses dependency resolution conflicts through exact version pinning and comprehensive constraint satisfaction across the entire dependency graph. Platform compatibility issues are handled through conditional dependency markers and multiple wheel distributions supporting different operating systems and architectures. Python version compatibility constraints prevent installation on unsupported Python versions through `requires-python = ">=3.10"` specification. Package integrity failures are detected through SHA256 hash verification for both wheel and source distributions. The system handles missing optional dependencies through conditional markers and graceful degradation patterns. Network connectivity issues during package installation are mitigated through multiple mirror support and cached wheel distributions. Version constraint conflicts are resolved through the lock file's deterministic resolution ensuring all transitive dependencies are compatible.

########## Internal Implementation Details

The lock file format uses TOML syntax with structured package entries containing comprehensive metadata including version specifications, source registry information, dependency relationships, and cryptographic verification data. Each package entry includes `name`, `version`, `source` registry information, `dependencies` array with conditional markers, `sdist` source distribution metadata with URL and SHA256 hash, and `wheels` array containing platform-specific wheel files with URLs and integrity checksums. Dependency resolution implements constraint satisfaction algorithms ensuring all version requirements are met across the entire dependency graph. Platform-specific handling uses conditional markers like `python_full_version < '3.11'` and `sys_platform == 'win32'` for targeted dependency inclusion. The system maintains separate dependency groups through `optional-dependencies` and `dev-dependencies` sections enabling different installation profiles for development and production environments.

########### Code Usage Examples

This example demonstrates installing dependencies using the lock file for reproducible development environment setup. The lock file ensures exact versions are installed matching the project's tested configuration.

```bash
# Install dependencies using uv with lock file for exact version matching
uv sync
# Installs all dependencies with exact versions specified in uv.lock
```

This example shows how to install only production dependencies excluding development tools. The lock file supports selective installation based on dependency groups and optional requirements.

```bash
# Install production dependencies only using lock file specifications
uv sync --no-dev
# Excludes development dependencies like pytest, black, mypy from installation
```

This example illustrates adding a new dependency while maintaining lock file integrity. The lock file must be updated to include new dependencies with proper version resolution and hash verification.

```bash
# Add new dependency and update lock file with resolved versions
uv add requests
uv lock
# Updates uv.lock with new dependency and all transitive requirements
```
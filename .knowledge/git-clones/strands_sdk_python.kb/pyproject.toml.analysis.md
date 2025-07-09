<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/.knowledge/git-clones/strands_sdk_python/pyproject.toml -->
<!-- Cached On: 2025-07-07T22:35:00.906226 -->
<!-- Source Modified: 2025-06-30T17:02:52.899757 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This `pyproject.toml` configuration file defines the build system, dependencies, and development environment for the `strands-agents` Python package, enabling standardized project management through `hatchling` build backend and `hatch-vcs` version control integration. The configuration provides multi-provider AI model support, development tooling automation, and testing infrastructure for building AI agents with minimal code complexity. Key semantic entities include `hatchling`, `hatch-vcs`, `boto3`, `botocore`, `mcp`, `pydantic`, `anthropic`, `litellm`, `ollama`, `openai`, `pytest`, `mypy`, `ruff`, `commitizen`, and environment configurations like `hatch-static-analysis`, `hatch-test`, `dev`, and `a2a`. The file implements a comprehensive dependency management strategy supporting Python 3.10-3.13 with optional feature groups for different AI model providers and development workflows.

##### Main Components

The configuration contains core project metadata in the `[project]` section defining package name, version, and dependencies, optional dependency groups for AI providers (`anthropic`, `litellm`, `ollama`, `openai`) and development tools (`dev`, `docs`, `otel`, `a2a`), Hatch environment configurations for testing (`hatch-test`), static analysis (`hatch-static-analysis`), and specialized workflows (`dev`, `a2a`), and tool-specific configurations for `mypy`, `ruff`, `pytest`, `coverage`, and `commitizen`. The build system section specifies `hatchling` as the build backend with `hatch-vcs` for version management from Git tags.

###### Architecture & Design

The configuration follows a modular dependency architecture separating core dependencies from optional provider-specific packages, enabling users to install only required AI model integrations. The Hatch environment system provides isolated development environments with feature-based dependency resolution, supporting matrix testing across Python versions 3.10-3.13. The design implements dependency conflict resolution through environment separation, particularly for `A2A` and `OTEL` http exporter conflicts that require dedicated testing environments.

####### Implementation Approach

The build system uses `hatch-vcs` for automatic version determination from Git tags, while dependency management employs semantic versioning constraints with upper bounds to prevent breaking changes. Testing infrastructure implements parallel execution through `pytest-xdist` with coverage reporting via `pytest-cov`, and static analysis combines `ruff` for linting/formatting with `mypy` for type checking. The configuration supports multi-environment workflows through Hatch scripts that automate common development tasks like formatting, linting, testing, and release preparation.

######## External Dependencies & Integration Points

**→ References:**
- `hatchling` (external library) - Modern Python build backend for package creation
- `hatch-vcs` (external library) - Version control system integration for automatic versioning
- `boto3>=1.26.0,<2.0.0` (external library) - AWS SDK for Python enabling Bedrock model access
- `mcp>=1.8.0,<2.0.0` (external library) - Model Context Protocol implementation
- `pydantic>=2.0.0,<3.0.0` (external library) - Data validation and serialization framework
- `anthropic>=0.21.0,<1.0.0` (external library) - Anthropic Claude API client
- `openai>=1.68.0,<2.0.0` (external library) - OpenAI API client for GPT models
- `pytest>=8.0.0,<9.0.0` (external library) - Testing framework with async support

**← Referenced by:**
- `src/strands/` - Source code package structure and module organization
- CI/CD pipeline - Automated testing, linting, and release workflows
- Package distribution - PyPI publishing and version management
- Developer environments - Local development setup and tooling

**⚡ Integration:**
This configuration serves as the central build and dependency specification for the Strands Agents SDK, coordinating AI model provider integrations, development tooling, and testing infrastructure while managing complex dependency relationships and environment isolation requirements.

######### Edge Cases & Error Handling

The configuration addresses dependency conflicts between `A2A` and `OTEL` http exporter through environment separation, requiring manual test execution for `a2a` environment. Version constraints prevent breaking changes through upper bound specifications, while `mypy` overrides handle missing type stubs for `litellm` package. The testing matrix excludes conflicting test suites using `--ignore=tests/multiagent/a2a` flags, and coverage reporting handles parallel execution through thread and multiprocessing concurrency settings.

########## Internal Implementation Details

The package source location maps to `src/strands/` through `tool.hatch.build.targets.wheel.packages` configuration, while version determination uses Git VCS through `tool.hatch.version.source = "vcs"`. Static analysis environments include all AI provider features for comprehensive type checking, and test environments support parallel execution with coverage collection across Python version matrices. The `commitizen` configuration implements conventional commit standards with custom styling and automatic changelog generation during version bumps.

########### Code Usage Examples

These configuration examples demonstrate the project structure and dependency management patterns. The examples show how to define core dependencies, optional features, and development environments for the Strands Agents package.

Basic project installation with core dependencies for AWS Bedrock integration:
```toml
[project]
name = "strands-agents"
dependencies = [
    "boto3>=1.26.0,<2.0.0",
    "botocore>=1.29.0,<2.0.0",
    "mcp>=1.8.0,<2.0.0",
    "pydantic>=2.0.0,<3.0.0",
]
```

Optional dependency installation for specific AI model providers:
```toml
[project.optional-dependencies]
anthropic = ["anthropic>=0.21.0,<1.0.0"]
openai = ["openai>=1.68.0,<2.0.0"]
ollama = ["ollama>=0.4.8,<1.0.0"]
```

Development environment configuration with testing and linting tools:
```toml
[tool.hatch.envs.dev]
dev-mode = true
features = ["dev", "docs", "anthropic", "litellm", "llamaapi", "ollama", "otel"]
```
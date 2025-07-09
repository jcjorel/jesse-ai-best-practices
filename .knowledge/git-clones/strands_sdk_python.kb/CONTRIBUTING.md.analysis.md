<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/.knowledge/git-clones/strands_sdk_python/CONTRIBUTING.md -->
<!-- Cached On: 2025-07-07T22:38:11.988769 -->
<!-- Source Modified: 2025-06-30T17:02:52.895757 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This contributing guidelines document establishes standardized development workflows and community engagement protocols for the Strands Agents SDK project, providing comprehensive instructions for bug reporting, feature requests, development environment setup, and pull request submission processes. The document enables consistent code quality through automated tooling integration and establishes clear contribution pathways for community developers. Key semantic entities include `hatchling`, `hatch`, `pre-commit`, `ruff`, `mypy`, `Bug Reports`, `Feature Requests`, `Conventional Commits`, `Amazon Open Source Code of Conduct`, `vulnerability reporting page`, and workflow commands like `hatch shell dev`, `hatch fmt --formatter`, `hatch test`. The guidelines implement a comprehensive development lifecycle management system integrating build tools, quality gates, and community standards for open source collaboration.

##### Main Components

The document contains seven primary sections: bug reporting and feature request procedures with GitHub issue templates, development environment setup using `hatch` and `pre-commit` workflows, code formatting and style guidelines with `ruff` and `mypy` integration, pull request contribution process with `Conventional Commits` requirements, guidance for finding contribution opportunities through existing issues, code of conduct enforcement through Amazon Open Source standards, and security issue reporting protocols with dedicated vulnerability channels. Each section provides specific tooling instructions and workflow requirements for different aspects of project contribution.

###### Architecture & Design

The guidelines follow a structured workflow architecture separating issue reporting, development setup, code quality enforcement, and contribution submission into distinct phases. The design implements automated quality gates through `pre-commit` hooks that execute formatting, linting, testing, and commit message validation before code submission. The architecture emphasizes tool integration through `hatch` as the central build system, coordinating development dependencies, testing environments, and quality checks through unified command interfaces.

####### Implementation Approach

The development workflow uses `hatch shell dev` for environment management and dependency installation, `pre-commit install` for automated quality gate setup, and `hatch fmt` commands for code formatting and linting execution. The approach implements multi-stage quality validation through pre-commit hooks that run `hatch run format`, `hatch run lint`, `hatch run test`, and `hatch run cz check` during commit operations. The strategy centralizes tool configuration through `pyproject.toml` while maintaining granular control over formatting, linting, type checking, and testing phases.

######## External Dependencies & Integration Points

**→ References:**
- `hatchling` (external library) - Build backend for Python package management
- `hatch` (external tool) - Development workflow and environment management
- `pre-commit` (external framework) - Git hook automation for quality checks
- `ruff` (external tool) - Code formatting and linting enforcement
- `mypy` (external tool) - Static type checking validation
- `../../issues/new?template=bug_report.yml` - GitHub issue template for bug reports
- `../../issues/new?template=feature_request.yml` - GitHub issue template for feature requests
- `https://www.conventionalcommits.org` - Conventional commit message specification
- `https://aws.github.io/code-of-conduct` - Amazon Open Source Code of Conduct
- `http://aws.amazon.com/security/vulnerability-reporting/` - AWS security vulnerability reporting

**← Referenced by:**
- Developer onboarding process - New contributor setup and workflow guidance
- CI/CD pipeline - Automated quality validation and testing workflows
- Code review process - Pull request validation and merge requirements
- Community engagement - Issue tracking and feature request management

**⚡ Integration:**
This document serves as the central coordination mechanism for all development activities in the Strands Agents project, integrating GitHub issue management, automated quality tooling, and community standards to ensure consistent contribution quality and maintainable codebase evolution.

######### Edge Cases & Error Handling

The guidelines address tool availability issues through alternative installation methods when `hatch shell dev` is unavailable, providing fallback `pip install -e ".[dev]"` commands for manual environment setup. The document handles security-sensitive contributions through dedicated vulnerability reporting channels, explicitly prohibiting public GitHub issue creation for security concerns. The workflow accommodates different IDE configurations by suggesting VS Code and PyCharm integration for automated tool execution, while maintaining command-line alternatives for all quality checks.

########## Internal Implementation Details

The pre-commit configuration executes multiple quality checks including `hatch run format` for code formatting, `hatch run lint` for style validation, `hatch run test` for unit testing, and `hatch run cz check` for commit message compliance. The development environment setup supports both automated `hatch shell dev` activation and manual virtual environment creation with explicit dependency installation. The quality gate system requires all checks to pass before commit completion, preventing defective code from entering the repository through automated enforcement mechanisms.

########### Code Usage Examples

These examples demonstrate the essential development workflow commands and setup procedures. The commands show how to establish a complete development environment with automated quality checks and testing capabilities.

Development environment setup using hatch for dependency management and virtual environment activation:

```bash
hatch shell dev
```

Alternative manual setup for environments where hatch shell is not available:

```bash
pip install -e ".[dev]" && pip install -e ".[litellm]"
```

Pre-commit hook installation for automated quality gate enforcement during commit operations:

```bash
pre-commit install -t pre-commit -t commit-msg
```

Code quality validation commands for manual execution of formatting and linting checks:

```bash
hatch fmt --formatter
hatch fmt --linter
```

Testing workflow execution for unit and integration test validation:

```bash
hatch test
hatch run test-integ
```
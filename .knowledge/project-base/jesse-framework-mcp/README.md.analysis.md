<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/README.md -->
<!-- Cached On: 2025-07-05T14:52:38.127385 -->
<!-- Source Modified: 2025-06-27T08:20:45.634656 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements comprehensive documentation for the Jesse Framework MCP Server, providing complete installation, configuration, and usage guidance for developers integrating the JESSE AI Framework through Model Context Protocol implementation. The documentation enables developers to replace manual 6-step session setup with single MCP tool calls while understanding build-time content embedding, project knowledge integration, and lazy loading capabilities. Key semantic entities include core MCP tools `jesse_start_session` and `jesse_load_knowledge_base` for framework initialization and knowledge base loading, installation methods using `uv` package manager and `pip` for distribution, configuration patterns for `Cline` MCP integration with `mcpServers` JSON configuration, directory structures `.knowledge/git-clones/`, `.knowledge/pdf-knowledge/`, `.knowledge/work-in-progress/` for project knowledge organization, build process components `artifacts/.clinerules/` source directory and `embedded_content/` destination, command-line interface `jesse-framework-mcp` for direct execution, session logging format with `.coding_assistant/jesse/session.log` file path, troubleshooting scenarios for build and runtime issues, development workflow commands `uv build`, `uv sync --dev`, `pytest`, `black`, `isort`, and `mypy` for code quality, and architectural patterns including build-time embedding, session initialization flow, and knowledge base discovery mechanisms. The system implements self-contained distribution with version-locked JESSE rules and portable execution across project directories.

##### Main Components

The documentation contains eleven primary sections providing comprehensive coverage of installation, usage, architecture, development, and troubleshooting for the Jesse Framework MCP Server. The Overview section establishes core functionality including complete session initialization, embedded framework content, and project knowledge integration. The Features section details core tools `jesse_start_session` and `jesse_load_knowledge_base` with self-contained distribution capabilities. The Installation section covers prerequisites, PyPI installation, and source installation methods. The Usage section provides Cline integration configuration, direct usage commands, and tool usage examples. The Architecture section explains build-time content embedding, session initialization flow, and knowledge base structure. The Development section covers building from source, testing procedures, and development dependencies. The Configuration section details session logging and knowledge base discovery mechanisms. The Troubleshooting section addresses build issues, runtime issues, and logging problems. The License, Contributing, and Support sections provide project governance and community information.

###### Architecture & Design

The architecture implements a comprehensive documentation structure with clear separation between user-facing functionality and technical implementation details, following standard open-source project documentation patterns with installation, usage, development, and troubleshooting sections. The design emphasizes practical guidance through concrete examples, step-by-step procedures, and troubleshooting scenarios while maintaining technical accuracy and completeness. Key design patterns include the progressive disclosure pattern starting with overview and features before diving into technical details, example-driven documentation pattern providing concrete code snippets and configuration examples, troubleshooting pattern addressing common issues with specific solutions, architectural explanation pattern using diagrams and flow descriptions for complex processes, and comprehensive coverage pattern addressing all aspects from installation to contribution guidelines. The system uses standard Markdown formatting with code blocks, JSON configurations, directory trees, and structured sections for maximum readability and accessibility.

####### Implementation Approach

The implementation uses structured Markdown documentation with hierarchical organization through header levels, code block formatting for examples and configurations, and comprehensive cross-referencing between related sections. Content organization follows logical user journey from installation through usage to development and troubleshooting. The approach implements concrete examples with actual command lines, configuration files, and directory structures rather than abstract descriptions. Technical concepts are explained through architectural diagrams using ASCII art and step-by-step process flows. Error scenarios include specific error messages with corresponding solutions and explanations. Development guidance provides complete workflow from building to testing with specific tool commands and dependencies. Installation instructions cover multiple package managers and deployment scenarios with platform-specific considerations.

######## External Dependencies & Integration Points

**→ References:**
- `Python 3.8+` runtime environment - required for MCP server execution and package installation
- `uv` package manager - recommended installation and development tool for dependency management
- `pip` package manager - alternative installation method for broader compatibility
- `Cline` AI assistant - primary integration target consuming MCP server through stdio transport
- `PyPI` package repository - distribution platform for jesse-framework-mcp package
- `Git` version control - source code management and repository cloning for development
- `artifacts/.clinerules/` directory - source location for JESSE framework content during build process
- `.knowledge/` directory structure - project-specific knowledge base organization and discovery

**← Referenced By:**
- Developer installation workflows - using documentation for package setup and configuration
- Cline MCP configuration - consuming JSON configuration examples for server integration
- Build systems - referencing build process documentation for content embedding procedures
- Troubleshooting workflows - using error scenarios and solutions for issue resolution
- Development teams - following contribution guidelines and development setup procedures
- Package managers - distributing through PyPI with installation instructions and dependencies

**⚡ System role and ecosystem integration:**
- **System Role**: Comprehensive documentation hub for Jesse Framework MCP Server ecosystem, providing authoritative guidance for installation, configuration, usage, and development workflows
- **Ecosystem Position**: Central reference point serving developers, integrators, and contributors with complete project information from basic usage to advanced development scenarios
- **Integration Pattern**: Used by developers for initial setup and ongoing reference, consumed by AI assistants through MCP protocol integration, referenced by build systems for content embedding procedures, and coordinated with package distribution platforms for installation and dependency management

######### Edge Cases & Error Handling

The documentation addresses build-time issues including missing JESSE project hierarchy with specific error messages and resolution steps. Installation problems are covered through multiple package manager options and troubleshooting for dependency conflicts. Runtime errors include embedded content loading failures with rebuild recommendations and knowledge base discovery issues with file path verification. Configuration problems address MCP server integration with Cline including transport protocol setup and command execution paths. Development environment issues cover build script testing, dependency installation, and code quality tool execution. Session logging failures are documented as non-blocking with permission-based solutions. Cross-platform compatibility considerations address different operating system requirements and path handling. Version compatibility issues between JESSE framework versions and MCP server releases are addressed through version-locking mechanisms and rebuild procedures.

########## Internal Implementation Details

The documentation uses standard Markdown syntax with consistent header hierarchy, code block formatting with language identifiers, and structured section organization. Installation procedures specify exact command sequences with package manager alternatives and environment setup requirements. Configuration examples provide complete JSON structures with proper syntax and required fields. Architectural explanations use ASCII art diagrams for build processes and directory structures with clear input-output relationships. Development workflows specify exact tool commands with dependency management and testing procedures. Error messages are quoted verbatim with corresponding solution steps and verification procedures. File path specifications use consistent notation with directory trailing slashes and relative path conventions. Code examples include both command-line usage and programmatic API calls with proper syntax highlighting and context explanations.

########### Usage Examples

MCP server installation demonstrates the primary setup workflow for developers integrating the Jesse Framework. This approach provides multiple installation methods with package manager flexibility and environment compatibility.

```bash
# Primary installation method using UV package manager for optimal dependency management
# Provides fastest installation with automatic virtual environment handling
uv add jesse-framework-mcp

# Alternative installation using pip for broader compatibility across development environments
# Supports traditional Python package installation workflows
pip install jesse-framework-mcp
```

Cline integration configuration showcases the MCP server setup pattern for AI assistant integration. This configuration enables seamless JESSE framework access through standardized MCP protocol communication.

```json
# Cline MCP server configuration for Jesse Framework integration
# Enables AI assistant access to complete JESSE framework through stdio transport
{
  "mcpServers": {
    "jesse-framework": {
      "command": "uv",
      "args": ["run", "jesse-framework-mcp"],
      "transport": "stdio"
    }
  }
}
```

Tool usage examples demonstrate the core MCP functionality for session initialization and knowledge base loading. These patterns enable developers to leverage JESSE framework capabilities through standardized tool calls.

```javascript
// Complete JESSE framework session initialization with project context loading
// Replaces manual 6-step setup with single tool call including WIP task integration
const context = await mcpClient.callTool("jesse_start_session", {
    user_prompt: "Help me implement authentication",
    load_wip_tasks: true
});

// Selective knowledge base loading for efficient context window management
// Enables targeted knowledge access based on task relevance and LLM selection
const kbContent = await mcpClient.callTool("jesse_load_knowledge_base", {
    kb_names: ["fastapi_kb", "aws_cdk_kb"]
});
```
# Git Clone Knowledge Bases Index

This directory contains knowledge bases extracted from external git repositories that provide context and patterns relevant to the JESSE Framework development.

## Storage Policy
**CRITICAL**: All git clones are stored **EXCLUSIVELY** in this directory (`<project_root>/.knowledge/git-clones/`).

- **Single Location Rule**: Git clones must **NEVER** exist anywhere else in the project structure
- **No Exceptions**: This policy has no exceptions - all external repositories are cloned only to `.knowledge/git-clones/`
- **Centralized Management**: This ensures consistent knowledge management and prevents scattered repository copies
- **Version Control Separation**: Keeps external repository content separate from project codebase through .gitignore rules

## Directory Structure
```
.knowledge/git-clones/
├── README.md                        # This index file
├── [repo-name]/                     # Actual git clone (ignored by .gitignore)
├── [repo-name]_kb.md               # Knowledge base extracted from repo (tracked)
└── [another-repo]_kb.md            # Additional knowledge bases (tracked)
```

## Available Knowledge Bases

### Strands Agents Ecosystem - Complete AI Agent Framework
**Ecosystem Import**: 6 repositories comprising the complete Strands Agents framework (2,813+ stars combined)  
**Import Session**: 2025-06-30T17:02:13Z → 2025-06-30T17:21:27Z (19 minutes)  
**Total Size**: ~115+ MiB of comprehensive AI agent framework knowledge  
**Relevance**: Production-ready AI agent framework patterns, tool ecosystem design, developer experience, and AWS integration strategies

#### Core SDK (`strands_sdk_python`) ⭐ 1,800 stars
**Repository**: https://github.com/strands-agents/sdk-python  
**Purpose**: Foundational Python SDK for AI agent development with comprehensive architecture  
**Key Features**: Complete agent lifecycle management, tools integration, model provider abstraction, production deployment patterns  
**Knowledge Base**: [strands_sdk_python_kb.md](strands_sdk_python_kb.md)  
**Size**: Core SDK with extensive documentation and examples

#### Tools Ecosystem (`strands_tools`) ⭐ 341 stars  
**Repository**: https://github.com/strands-agents/tools  
**Purpose**: 28+ powerful capabilities toolkit for agents (AWS, HTTP, Python, shell, image generation, etc.)  
**Key Features**: Professional-grade tool implementations, proper abstractions, extensible architecture, comprehensive AWS integration  
**Knowledge Base**: [strands_tools_kb.md](strands_tools_kb.md)  
**Size**: Complete toolkit for real-world agent applications

#### Samples & Examples (`strands_samples`) ⭐ 190 stars
**Repository**: https://github.com/strands-agents/samples  
**Purpose**: Comprehensive tutorials and real-world implementations (102.87 MiB - largest repository)  
**Key Features**: Production-ready examples from basic to advanced scenarios, complete learning path, implementation templates  
**Knowledge Base**: [strands_samples_kb.md](strands_samples_kb.md)  
**Size**: 102.87 MiB of comprehensive examples and tutorials

#### Interactive Builder (`strands_agent_builder`) ⭐ 174 stars
**Repository**: https://github.com/strands-agents/agent-builder  
**Purpose**: CLI tool for interactive agent development with streaming and hot-reloading  
**Key Features**: Exceptional developer experience, real-time feedback, knowledge base integration, multi-agent orchestration  
**Knowledge Base**: [strands_agent_builder_kb.md](strands_agent_builder_kb.md)  
**Size**: 87.17 KiB - lightweight but powerful CLI tool

#### MCP Integration (`strands_mcp_server`) ⭐ 109 stars  
**Repository**: https://github.com/strands-agents/mcp-server  
**Purpose**: Model Context Protocol server for AI tool integration (40+ compatible applications)  
**Key Features**: Universal compatibility with AI coding assistants, documentation access, minimal architecture, testing frameworks  
**Knowledge Base**: [strands_mcp_server_kb.md](strands_mcp_server_kb.md)  
**Size**: 29.31 KiB - focused MCP server implementation

#### Documentation (`strands_docs`) ⭐ 59 stars
**Repository**: https://github.com/strands-agents/docs  
**Purpose**: Comprehensive MkDocs-based documentation (11.90 MiB)  
**Key Features**: Professional documentation architecture, CDK examples, automated deployment, quality assurance  
**Knowledge Base**: [strands_docs_kb.md](strands_docs_kb.md)  
**Size**: 11.90 MiB - extensive documentation and deployment examples

### FastMCP - Modern MCP Framework
**Repository**: https://github.com/jlowin/fastmcp  
**Purpose**: Comprehensive Python framework for building Model Context Protocol (MCP) servers and clients  
**Key Features**: Production-ready MCP implementation with authentication, multiple transports, OpenAPI integration, comprehensive testing  
**Knowledge Base**: [fastmcp_kb.md](fastmcp_kb.md)  
**Added**: 2025-06-27T11:46:00Z  
**Relevance**: Modern MCP server development patterns for JESSE Framework MCP server modernization

### Cline AI Assistant - MCP Integration Reference
**Repository**: https://github.com/cline/cline.git  
**Purpose**: Autonomous AI coding assistant VSCode extension with comprehensive MCP integration for understanding how to integrate and interact with MCP servers  
**Key Features**: Multi-server MCP support, marketplace integration, tool auto-approval, real-time management, rich UI integration  
**Knowledge Base**: [cline_kb.md](cline_kb.md)  
**Added**: 2025-06-27T12:17:00Z  
**Relevance**: MCP client-side integration patterns, server discovery, connection management, and user interaction patterns for JESSE Framework MCP development

## How to Add Git Clone Knowledge Bases
Use the Git Clone Import workflow to add external repositories:

```bash
/jesse_wip_kb_git_clone_import.md
```

This workflow will:
1. Prompt for repository URL and focus areas
2. Clone repository to `.knowledge/git-clones/[repo-name]/`
3. Create knowledge base file `[repo-name]_kb.md`
4. Index important files and patterns
5. Update main knowledge base with reference

## .gitignore Protection
When any git clone is added to the knowledge base, the project `.gitignore` file contains these protective rules:

```
# Knowledge Management System - Git Clones
# Ignore actual git clone directories but keep knowledge base files
.knowledge/git-clones/*/
!.knowledge/git-clones/*.md
!.knowledge/git-clones/README.md
```

This ensures that:
- Actual git clone directories are ignored and not committed to the project repository
- Knowledge base files (`[repo-name]_kb.md`) are preserved and version controlled
- This index file (`README.md`) is maintained in version control
- External repository content remains separate from project codebase

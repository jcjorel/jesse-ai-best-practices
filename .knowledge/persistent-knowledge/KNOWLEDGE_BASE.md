# JESSE Framework Development - Project Knowledge Base
*Last Updated: 2025-06-27T23:35:00Z*

## Session-Specific Knowledge Loading Strategy
**LAZY LOADING APPROACH**: Knowledge bases related to the current session task are loaded on-demand when specifically needed, rather than automatically at session initialization. This approach:

- **Reduces Context Window Usage**: Only loads relevant knowledge bases for the current task
- **Improves Performance**: Avoids loading unnecessary external repository content
- **Maintains Focus**: Keeps session context aligned with current work objectives
- **Enables Selective Access**: Allows targeted knowledge base consultation when specific expertise is required

**Loading Triggers**: Knowledge bases are loaded when:
- User explicitly requests information from a specific repository or PDF
- Current task requires specific external API or framework knowledge
- Implementation needs reference patterns from external sources
- Debugging requires consultation of external documentation

**Available Knowledge Sources**:
- Git Clone Knowledge Bases: `.knowledge/git-clones/[repo-name]_kb.md`
- PDF Knowledge Bases: `.knowledge/pdf-knowledge/[source-name]/[source-name]_kb.md`
- Essential Knowledge Base: Always loaded (this file)

## Project Purpose
The JESSE AI Best Practices Framework is a comprehensive system that transforms AI coding assistants (particularly Cline) into intelligent, knowledge-aware development partners through structured knowledge management, automated workflows, and enforced coding standards.

**Meta-Development Context**: This project uses the JESSE Framework to develop the JESSE Framework itself, providing real-world testing of framework capabilities during development.

**Trust Sources**:
- Codebase: `README.md`
- Codebase: `HOWTO_USE.md`
- Documentation: `howtos/AI_ASSISTANT_INTEGRATION.md`

## Critical Framework Separation
**🚨 FRAMEWORK SEPARATION PROTOCOL 🚨**:
- **Framework we're BUILDING**: `artifacts/` directory contains all framework components under development
- **Framework we're USING**: Global installation (`${HOME}/Cline/Rules/`) + `.knowledge/` project files for managing THIS project

**Trust Sources**:
- Project Structure: `artifacts/.clinerules/` (framework components being developed)
- Project Structure: `.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md` (project management)

## Key Development Patterns

### Framework Component Development
**Pattern**: Develop all framework components in `artifacts/` directory
**Implementation**:
- All JESSE_*.md files developed in `artifacts/.clinerules/`
- All workflow files developed in `artifacts/.clinerules/workflows/`
- Complete isolation from operational framework files
- Clear separation between "building" vs "using"

**Benefits**:
- No confusion between framework versions
- Safe testing of framework modifications
- Clear deployment path from development to production

**Trust Sources**:
- Directory Structure: `artifacts/.clinerules/`
- Directory Structure: `artifacts/.clinerules/workflows/`

### Documentation-Driven Development
**Pattern**: Maintain comprehensive documentation in `howtos/` directory
**Implementation**:
- Each major component has corresponding howto guide
- Clear usage instructions for framework users
- Visual diagrams and examples for complex concepts
- Cross-referenced documentation preventing duplication

**Benefits**:
- Framework users have clear guidance
- Development decisions are documented
- Examples demonstrate real usage patterns

**Trust Sources**:
- Documentation: `howtos/KNOWLEDGE_MANAGEMENT.md`
- Documentation: `howtos/TASK_MANAGEMENT.md`
- Documentation: `howtos/CODING_STANDARDS.md`
- Documentation: `howtos/WORKFLOW_REFERENCE.md`

### Meta-Development Testing
**Pattern**: Using JESSE Framework to develop JESSE Framework itself
**Implementation**:
- Framework dogfooding during development
- Real-world testing of all framework capabilities
- Continuous improvement through self-application
- Knowledge capture about framework design decisions

**Benefits**:
- Framework quality validation through actual usage
- Documentation accuracy verification
- Workflow effectiveness confirmation
- Edge case discovery and resolution

**Trust Sources**:
- Development Process: This knowledge management system usage
- Development Process: WIP task workflows used for framework development

## Development Environment
### Repository Structure
**Primary Directories**:
- **artifacts/**: Framework components we're building (JESSE_*.md files, workflows)
- **howtos/**: User documentation and guides  
- **Root files**: README.md, HOWTO_USE.md, LICENSE
- **.knowledge/**: Our project knowledge management (what we're using)
- **.clinerules/**: Project-specific configuration

**Trust Sources**:
- Repository Structure: Root directory listing
- Directory Structure: `artifacts/` vs operational directories

### Global Framework Installation
**Location**: `${HOME}/Cline/Rules/` and `${HOME}/Cline/Workflows/`
**Purpose**: Provides framework capabilities for managing THIS project
**Separation**: Complete isolation from `artifacts/` development components

**Trust Sources**:
- Installation: `${HOME}/Cline/Rules/JESSE_*.md`
- Installation: `${HOME}/Cline/Workflows/jesse_*.md`

## JESSE Framework MCP Server Implementation
**Status**: ✅ **COMPLETED** - Complete MCP Server Implementation (2025-06-27)

**MCP Server Architecture**: FastMCP-based server providing complete JESSE framework initialization through two primary tools:
- `jesse_start_session(user_prompt, load_wip_tasks)` - Complete framework initialization 
- `jesse_load_knowledge_base(kb_names)` - Lazy loading of specific knowledge bases

**Build-Time Content Embedding**: All JESSE rules and workflows from `artifacts/.clinerules/` are embedded at build time into the MCP server package, ensuring complete self-contained distribution.

**🚨 CRITICAL UV CONTEXT REQUIREMENT**: 
- **Operational Requirement**: MCP server MUST always run and be tested in a "uv" context
- **Testing Environment**: All MCP server tests must use UV environment exclusively
- **Deployment Standard**: UV is the primary and required package manager for distribution
- **Cline Integration**: MCP configuration must use UV commands: `"command": "uv", "args": ["run", "jesse-framework-mcp"]`
- **Build Process**: All build operations must use UV toolchain
- **Development Workflow**: Local development and testing requires UV environment activation

**🔒 CRITICAL SESSION LOGGING LOCATION**: 
- **Log File Path**: `<project_root>/.coding_assistant/jesse/session.log`
- **Directory Structure**: Uses `parents=True` for nested directory creation
- **Content**: JSON-formatted session logs with UUID tracking for analytics

**🏗️ CRITICAL ASYNC ARCHITECTURE REQUIREMENT**: 
- **Fully Python Async Design**: JESSE MCP Server MUST use comprehensive async patterns for optimal performance
- **Modern FastMCP Standards**: Implementation must follow FastMCP 2.0 async architecture patterns
- **High-Performance Foundation**: Async design ensures best performance for real-time MCP communication
- **Production-Ready Async**: Built-in async context management, connection pooling, and resource lifecycle management
- **Multiple Transport Async Support**: Single async codebase supporting stdio, HTTP, and SSE transports
- **Async Tool Execution**: All tool handlers must be async for non-blocking operation
- **Real-Time Notification Async**: Async notification system supports real-time progress updates during long-running operations

**Trust Sources**:
- Implementation: `jesse-framework-mcp/` directory
- Source Code: `jesse-framework-mcp/jesse_framework_mcp/main.py`
- Documentation: `jesse-framework-mcp/README.md`
- Tests: `jesse-framework-mcp/tests/test_content_loading.py`
- Async Patterns: `.knowledge/git-clones/fastmcp_kb.md` (modern async MCP architecture reference)

## Available Knowledge Sources (Lazy Loading)
**Note**: These knowledge bases are loaded on-demand when specifically needed for the current session task, following the lazy loading strategy described above.

### Git Clone Knowledge Bases

#### FastMCP - Modern MCP Framework
**Repository**: https://github.com/jlowin/fastmcp  
**Knowledge Base**: `.knowledge/git-clones/fastmcp_kb.md`  
**Purpose**: Comprehensive Python framework for building Model Context Protocol (MCP) servers and clients  
**Relevance**: Modern MCP server development patterns for JESSE Framework MCP server modernization  
**Key Features**: Production-ready MCP implementation with authentication, multiple transports, OpenAPI integration, comprehensive testing  
**Added**: 2025-06-27T11:46:00Z

#### Cline AI Assistant - MCP Integration Reference
**Repository**: https://github.com/cline/cline.git  
**Knowledge Base**: `.knowledge/git-clones/cline_kb.md`  
**Purpose**: Autonomous AI coding assistant VSCode extension with comprehensive MCP integration for understanding how to integrate and interact with MCP servers  
**Relevance**: MCP client-side integration patterns, server discovery, connection management, and user interaction patterns for JESSE Framework MCP development  
**Key Features**: Multi-server MCP support, marketplace integration, tool auto-approval, real-time management, rich UI integration  
**Added**: 2025-06-27T12:17:00Z

**Critical Knowledge**: Detailed MCP workflow integration architecture and technical implementation patterns documented in dedicated knowledge base file.

**To add additional git clone knowledge bases**:
1. Use the Git Clone Import workflow: `/jesse_wip_kb_git_clone_import.md`
2. The workflow will clone the repository and create the knowledge base
3. Git clones are stored in `.knowledge/git-clones/[repo-name]/`
4. Knowledge bases are created as `.knowledge/git-clones/[repo-name]_kb.md`

### PDF Knowledge Bases
*No PDF knowledge bases imported yet*

**To import a PDF knowledge base**:
1. Use the PDF Import workflow: `/jesse_wip_kb_pdf_import.md`
2. The workflow will process the PDF and create indexed knowledge base
3. PDFs are stored in `.knowledge/pdf-knowledge/[pdf-name]/`
4. Knowledge bases are created as `.knowledge/pdf-knowledge/[pdf-name]/[pdf-name]_kb.md`
5. PDF chunks are stored in `.knowledge/pdf-knowledge/[pdf-name]/pdf_chunks/`

## Project PR/FAQ Documents

### Press Release & FAQ
**Status**: ✅ **COMPLETED** (2025-06-26)

**JESSE AI Best Practices Framework Launches Intelligent Context Server**
*Revolutionary MCP server eliminates 2-3 hours daily lost to AI context setup for development teams*

**Key Innovation**: Intelligent MCP Context Server providing background-scanning capabilities with semantic context database and intent-driven context selection.

**Primary Customer**: Senior/Lead Developers at growth companies (50-500 employees) who lead development teams of 5-15 developers and lose 2-3 hours daily to AI context management.

**The ONE Benefit**: "Eliminates the 2-3 hours daily lost to AI context setup so developers can focus entirely on building features"

**Success Metrics**: 15% adoption within 12 months, 70+ NPS score, $150-225 daily value per developer

**Trust Sources**:
- Complete PR/FAQ: `working_backwards/current/pr_faq_draft.md`
- Working Backwards Process: `working_backwards/current/` directory
- Market Research: 30% AI code generation, 25% CAGR market growth

### Working Backwards Summary

**Status**: ✅ **COMPLETED** - All 5 Customer Questions Answered

**The 5 Customer Questions Framework**:
```
✅ WHO is the customer?     → Senior/Lead Developers at growth companies (50-500 employees)
✅ WHAT is the problem?     → 2-3 hours daily lost to AI context setup and re-explaining project details
✅ WHAT is the solution?    → Intelligent MCP Context Server with background scanning and semantic context
✅ WHAT is the experience?  → Instant productivity: 2-minute startup vs 20-30 minutes, progressive intelligence
✅ HOW measure success?     → Time savings, adoption rates, customer satisfaction (comprehensive metrics)
```

**Market Opportunity**: $30 billion AI coding assistant market (25% CAGR), 300K+ target developers

**Competitive Advantage**: Only solution combining persistent context preservation with intelligent context selection

**Trust Sources**:
- Working Backwards Completion: `working_backwards/current/five_questions_answers.md`
- Customer Research: `working_backwards/current/customer_research.md`
- Solution Architecture: `working_backwards/current/solution_development.md`
- Experience Design: `working_backwards/current/experience_design.md`
- Success Framework: `working_backwards/current/success_metrics.md`

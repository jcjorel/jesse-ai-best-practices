# Project Knowledge Management
*This file contains project-specific knowledge while system rules remain at ${HOME}/Cline/Rules/*

---

# 🚨 FRAMEWORK-WIDE SESSION INITIALIZATION REQUIREMENT 🚨

## Mandatory Session Initialization Command
**EVERY JESSE FRAMEWORK DEVELOPMENT SESSION MUST START WITH:**
```bash
cd jesse-framework-mcp && uv run python tests/test_project_root.py --dump
```

**REQUIREMENT LEVEL**: 🔒 **HARD BLOCKING** - Development work cannot proceed without this  
**SCOPE**: All JESSE Framework development sessions (framework-wide requirement)  
**MODES**: **BOTH PLAN AND ACT MODES** - This command must be executed even when starting a PLAN session  
**ENFORCEMENT**: Manual verification required before ANY development activity (planning or implementation)
**IMPORTANT**: You are allowed to execute this command in PLAN mode.

**⚠️ CRITICAL**: This initialization command is required to be executed **as soon as possible**, regardless of whether you begin in PLAN mode or ACT mode. Planning activities also require proper project context initialization.

**This requirement is documented in detail in**: `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md`

---

# Essential Knowledge Base
*Last Updated: 2025-07-01T10:39:00Z*

## Current Work-in-Progress Task
**Active Task**: Knowledge Bases Hierarchical Indexing System
**Status**: ✅ **ACTIVE** - WIP task created with comprehensive design documentation
**Last Updated**: 2025-07-01T10:27:00Z
**Phase**: Planning & Design → Implementation
**Priority**: High - Core framework capability
**Purpose**: Create FastMCP-based knowledge indexing system implementing Hierarchical Semantic Context pattern
**Target Completion**: 2025-07-15T00:00:00Z (2 weeks)
**Task Directory**: `.knowledge/work-in-progress/knowledge_bases_hierarchical_indexing_system/`
**Next Action**: Create knowledge-bases/ directory structure and implement core indexing components

## Other Active Tasks
*Note: These tasks exist but are NOT loaded automatically. Use /jesse_wip_task_switch to make one current.*
- None currently active

## Recently Completed
- **MCP Server Context Size Optimization** (2025-06-29 → 2025-07-01)
  - Status: ✅ **COMPLETED** - Significantly exceeded original scope
  - Outcome: Advanced LLM integration, Strands Agent ecosystem import (115+ MiB), enhanced MCP architecture
  - Archive: `.knowledge/work-in-progress/_archived/mcp_server_context_optimization_20250701_0900/`
  - Key Achievement: Complete transformation from planning-phase to comprehensive implementation

## Quick Access Links
- [Persistent Knowledge Base](.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md)
- [WIP Tasks Directory](.knowledge/work-in-progress/)
- [Git Clones Directory](.knowledge/git-clones/)

## Project Context
This project (jesse-ai-best-practices) is the development repository for the JESSE AI Best Practices Framework itself. We are using the JESSE Framework to develop the JESSE Framework (meta-development).

**🚨 CRITICAL SEPARATION PROTOCOL 🚨**:
- **Framework we're BUILDING**: `artifacts/` directory contains all framework components under development
- **Framework we're USING**: Global installation (`${HOME}/Cline/Rules/`) + `.knowledge/` project files for managing THIS project

## Key Project Components
- **Framework Rules**: JESSE_*.md files in `artifacts/.clinerules/` (components being developed)
- **Automated Workflows**: Workflow files in `artifacts/.clinerules/workflows/` (components being developed)
- **Documentation**: `howtos/` directory with comprehensive usage guides
- **Examples**: Implementation examples and templates in README.md and HOWTO_USE.md
- **Project Management**: This knowledge management system for tracking framework development

## Development Patterns

### Meta-Development Context
**Pattern**: Using JESSE Framework to develop JESSE Framework itself
**Benefits**: 
- Real-world testing of framework capabilities during development
- Continuous improvement through self-application
- Documentation excellence through practical usage
- Knowledge capture about framework design decisions

**Trust Sources**:
- Codebase: `README.md`
- Codebase: `HOWTO_USE.md`

### Framework Component Development
**Pattern**: Develop all framework components in `artifacts/` directory
**Implementation**:
- All JESSE_*.md files developed in `artifacts/.clinerules/`
- All workflow files developed in `artifacts/.clinerules/workflows/`
- Complete isolation from operational framework files
- Clear separation between "building" vs "using"

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

**Trust Sources**:
- Documentation: `howtos/KNOWLEDGE_MANAGEMENT.md`
- Documentation: `howtos/TASK_MANAGEMENT.md`
- Documentation: `howtos/CODING_STANDARDS.md`
- Documentation: `howtos/WORKFLOW_REFERENCE.md`

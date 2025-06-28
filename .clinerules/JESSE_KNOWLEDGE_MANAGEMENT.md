# Project Knowledge Management
*This file contains project-specific knowledge while system rules remain at ${HOME}/Cline/Rules/*

---

# Essential Knowledge Base
*Last Updated: 2025-06-27T12:18:00Z*

## Current Work-in-Progress Task
**Active Task**: None
**Status**: None
**Last Updated**: YYYY-MM-DDThh:mm:ssZ
**Phase**: None
**Next Action**: "Define a current WIP task for JESSE Framework development"

## Other Active Tasks
*Note: These tasks exist but are NOT loaded automatically. Use /jesse_wip_task_switch to make one current.*
- None currently active

## Recently Completed
- None yet

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

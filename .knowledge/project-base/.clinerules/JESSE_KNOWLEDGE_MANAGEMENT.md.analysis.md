<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md -->
<!-- Cached On: 2025-07-05T16:25:58.778752 -->
<!-- Source Modified: 2025-07-01T10:50:59.758716 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This project knowledge management configuration file serves as the central coordination hub for JESSE Framework development sessions, enforcing mandatory session initialization protocols and maintaining comprehensive project state tracking. The file provides essential project context management, work-in-progress task coordination, and meta-development workflow guidance for building the JESSE AI Best Practices Framework using itself. Key semantic entities include `uv run python jesse-framework-mcp/tests/test_project_root.py --dump` mandatory initialization command, `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md` knowledge base reference, `.knowledge/work-in-progress/` task directory structure, `artifacts/.clinerules/` framework component development area, `${HOME}/Cline/Rules/` global framework installation, `FastMCP-based` knowledge indexing system, `Hierarchical Semantic Context` pattern implementation, `/jesse_wip_task_switch` task switching command, and comprehensive project separation protocols distinguishing between framework components being built versus framework tools being used. The system enables coordinated development sessions with proper project context initialization while maintaining clear architectural boundaries between development artifacts and operational framework files.

##### Main Components

The file contains five primary content sections: Framework-Wide Session Initialization Requirement establishing the mandatory `uv run python` command execution protocol with hard blocking enforcement, Essential Knowledge Base section tracking current work-in-progress tasks including the active Knowledge Bases Hierarchical Indexing System implementation, Quick Access Links providing direct navigation to `.knowledge/persistent-knowledge/`, `.knowledge/work-in-progress/`, and `.knowledge/git-clones/` directories, Project Context section defining the meta-development approach and critical separation protocol between `artifacts/` development components and operational framework files, and Development Patterns section documenting meta-development context, framework component development workflows, and documentation-driven development practices with comprehensive trust source references.

###### Architecture & Design

The architecture implements a centralized project coordination pattern with mandatory session initialization enforcement and clear separation between development artifacts and operational framework components. The design establishes a meta-development workflow where the JESSE Framework is used to develop itself, creating real-world testing scenarios and continuous improvement cycles. The knowledge management system follows a hierarchical organization with persistent knowledge bases, work-in-progress task tracking, and archived completion records. The separation protocol maintains strict boundaries between `artifacts/` directory containing framework components under development and operational framework files in global installation and `.knowledge/` project files, preventing confusion between building versus using framework capabilities.

####### Implementation Approach

The implementation strategy employs mandatory command execution patterns with hard blocking requirements ensuring proper project context initialization before any development activity. Task management utilizes directory-based organization with `.knowledge/work-in-progress/` for active tasks and `_archived/` subdirectories for completed work. The meta-development approach implements self-application testing where framework capabilities are validated through actual usage during framework development. Documentation-driven development maintains comprehensive guides in `howtos/` directory with cross-referenced content preventing duplication. Trust source validation references specific files including `README.md`, `HOWTO_USE.md`, and directory structures for authoritative information verification.

######## External Dependencies & Integration Points

**→ References:**
- `${HOME}/Cline/Rules/` - global JESSE Framework installation providing operational framework rules
- `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md` - comprehensive knowledge base documentation
- `.knowledge/work-in-progress/knowledge_bases_hierarchical_indexing_system/` - active task implementation directory
- `jesse-framework-mcp/tests/test_project_root.py` - mandatory session initialization script
- `artifacts/.clinerules/` - framework component development directory
- `howtos/KNOWLEDGE_MANAGEMENT.md` - knowledge management documentation
- `howtos/TASK_MANAGEMENT.md` - task management workflow documentation

**← Referenced By:**
- Development session initialization workflows requiring mandatory command execution
- Task switching operations using `/jesse_wip_task_switch` command
- Framework component development processes accessing `artifacts/` directory
- Documentation workflows referencing trust sources and cross-linked guides
- Project context validation ensuring proper separation protocol adherence

**⚡ System role and ecosystem integration:**
- **System Role**: Central coordination hub for JESSE Framework development sessions providing mandatory initialization protocols, project state tracking, and meta-development workflow guidance
- **Ecosystem Position**: Core operational component that all JESSE Framework development activities depend on for proper session initialization and project context management
- **Integration Pattern**: Used by developers at session start for initialization, task management systems for work coordination, and documentation workflows for maintaining comprehensive project knowledge and architectural boundaries

######### Edge Cases & Error Handling

The system handles session initialization failures through hard blocking enforcement preventing development work from proceeding without proper project context. Task switching scenarios are managed through explicit `/jesse_wip_task_switch` command usage with clear documentation of inactive tasks. Meta-development confusion between building versus using framework components is addressed through critical separation protocol documentation and trust source validation. Archive management handles completed tasks through systematic `_archived/` directory organization with timestamp-based naming conventions. Documentation consistency is maintained through cross-referenced trust sources and comprehensive howto guide integration preventing information duplication and ensuring accuracy.

########## Internal Implementation Details

The mandatory session initialization uses specific command syntax `uv run python jesse-framework-mcp/tests/test_project_root.py --dump` with hard blocking requirement level and both PLAN and ACT mode enforcement. Task tracking maintains timestamp-based updates with ISO 8601 format (`2025-07-01T10:39:00Z`) and status indicators using emoji-based visual markers (✅ for completed, 🚨 for critical requirements). Directory organization follows systematic patterns with `.knowledge/` prefix for all knowledge management files and `artifacts/` prefix for framework development components. Trust source validation references specific files and directory structures providing authoritative information sources. Archive naming conventions use timestamp suffixes (`_20250701_0900`) for systematic organization and retrieval.

########### Code Usage Examples

**Mandatory session initialization command execution:**

This command must be executed at the beginning of every JESSE Framework development session to establish proper project context. The initialization is required regardless of whether starting in PLAN or ACT mode and provides essential project root detection and context setup.

```bash
# Execute mandatory session initialization (hard blocking requirement)
uv run python jesse-framework-mcp/tests/test_project_root.py --dump
```

**Task switching and project navigation:**

This pattern demonstrates how to switch between work-in-progress tasks and navigate the knowledge management structure. The commands provide access to different project areas and task coordination capabilities.

```bash
# Switch to different WIP task (when multiple tasks exist)
/jesse_wip_task_switch

# Navigate to key project directories
ls -la .knowledge/persistent-knowledge/
ls -la .knowledge/work-in-progress/
ls -la artifacts/.clinerules/
```

**Framework component development workflow:**

This example shows the proper approach for developing framework components while maintaining separation between building and using framework capabilities. The workflow ensures components are developed in the correct directory structure.

```bash
# Develop framework rules in artifacts directory (building framework)
ls -la artifacts/.clinerules/JESSE_*.md
ls -la artifacts/.clinerules/workflows/

# Reference operational framework files (using framework)
ls -la ${HOME}/Cline/Rules/
cat .knowledge/persistent-knowledge/KNOWLEDGE_BASE.md
```
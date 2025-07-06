<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/embedded_content/workflows/jesse_wip_task_create.md -->
<!-- Cached On: 2025-07-06T12:07:44.351049 -->
<!-- Source Modified: 2025-06-26T12:37:12.126415 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This workflow documentation provides a comprehensive WIP task creation system for the Jesse Framework, designed to establish structured work-in-progress tasks with integrated Git branch management, knowledge base synchronization, and project lifecycle tracking. The system delivers mandatory Git repository validation with uncommitted changes detection, structured task directory creation in `.knowledge/work-in-progress/` with standardized templates, and comprehensive Git branch management including automatic branch creation and parent branch selection. Key semantic entities include `git rev-parse --is-inside-work-tree` repository validation, `git status --porcelain` working directory checks, `.knowledge/work-in-progress/[task_name_snake_case]/` directory structure creation, `WIP_TASK.md` and `PROGRESS.md` template population, `snake_case` task name conversion, Git branch naming with `jesse-wip/[task_name_snake_case]` pattern, `.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md` Essential Knowledge Base integration, parallel task detection and warning systems, file restriction capabilities for multi-task scenarios, mandatory WIP task files commit requirements, and comprehensive error handling with complete rollback mechanisms ensuring consistent project state management and task isolation.

##### Main Components

The workflow contains seven primary execution steps with critical validation checkpoints and comprehensive error handling mechanisms. Core components include Git Repository Validation checking repository status and working directory cleanliness, Task Information Gathering collecting user requirements for task definition, Task Directory Structure Creation establishing standardized file organization, WIP_TASK.md Template Population with comprehensive task metadata, Git Branch Management Setup providing branch creation and selection options, PROGRESS.md Template Creation for milestone tracking, and Essential Knowledge Base Updates maintaining system-wide task awareness. The system incorporates specialized validation steps including Git Working Directory Prerequisites ensuring clean repository state, parallel task detection with risk warnings, mandatory WIP task files commit procedures, and comprehensive error handling with rollback capabilities.

###### Architecture & Design

The architecture implements a state-driven workflow pattern with mandatory validation checkpoints preventing inconsistent task creation and ensuring Git repository integrity. The design employs a fail-fast approach with comprehensive prerequisite validation before any file system modifications, ensuring clean rollback capabilities when validation fails. The system uses structured template-based task creation with standardized directory organization and file naming conventions enabling consistent task management across projects. The architectural pattern includes integrated Git workflow management with branch creation, parent branch selection, and automatic commit procedures ensuring proper version control integration. The design incorporates knowledge base synchronization maintaining system-wide awareness of active tasks and their status through Essential Knowledge Base updates.

####### Implementation Approach

The implementation uses Git command-line integration for repository validation and branch management operations, employing `git rev-parse --is-inside-work-tree` for repository detection and `git status --porcelain` for working directory validation. The approach employs structured template generation for task files with standardized markdown formats and comprehensive metadata sections. Task naming uses snake_case conversion algorithms ensuring consistent directory naming and Git branch creation patterns. The system implements comprehensive validation workflows with user confirmation dialogs and risk warnings for parallel task scenarios. File system operations use atomic creation patterns with rollback capabilities ensuring consistent state management during failures. Git integration employs standard branching workflows with automatic commit procedures and parent branch selection mechanisms.

######## External Dependencies & Integration Points

**→ References:**
- `git` (external tool) - Git version control system for repository validation, branch management, and commit operations
- `.knowledge/work-in-progress/` - dedicated directory structure for WIP task organization and file storage
- `.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md` - Essential Knowledge Base requiring updates for active task tracking
- `WIP_TASK.md` template - standardized task definition format with Git integration metadata
- `PROGRESS.md` template - milestone tracking format for task progress monitoring
- Git branch naming convention `jesse-wip/[task_name_snake_case]` - standardized branch naming pattern
- Snake_case conversion algorithms - task name standardization for directory and branch naming

**← Referenced By:**
- Jesse Framework knowledge management system - processes consuming WIP task information for project coordination
- Git workflow management tools - systems requiring standardized branch naming and commit patterns
- Task completion workflows - procedures referencing WIP task structure for completion and cleanup operations
- Project status reporting systems - tools aggregating WIP task information for progress tracking
- Development team coordination processes - workflows requiring active task awareness and conflict prevention

**⚡ System role and ecosystem integration:**
- **System Role**: Critical task lifecycle management component within the Jesse Framework ecosystem, providing structured WIP task creation with integrated Git workflow management and knowledge base synchronization
- **Ecosystem Position**: Core infrastructure component that establishes the foundation for all work-in-progress task management, serving as the entry point for structured development workflows
- **Integration Pattern**: Used by development teams through direct workflow invocation, integrated with Git repositories for version control coordination, synchronized with knowledge management systems for project awareness, and coordinated with task completion workflows for full lifecycle management

######### Edge Cases & Error Handling

The workflow handles uncommitted Git changes by immediately failing with comprehensive guidance for resolution through commit, stash, or reset operations. Task name conflicts with existing tasks trigger alternative name prompts preventing directory structure collisions. File creation failures implement complete rollback procedures removing partial directory structures and restoring original system state. WIP task files commit failures trigger comprehensive cleanup including file removal and Essential Knowledge Base restoration. Git branch creation failures provide fallback options to current branch usage while maintaining task functionality. Essential Knowledge Base update failures implement complete rollback with previous state restoration. The system addresses parallel task scenarios with risk warnings and optional file restriction capabilities preventing task interference and state inconsistencies.

########## Internal Implementation Details

The workflow uses bash command execution for Git operations including `git rev-parse --is-inside-work-tree` for repository validation and `git status --porcelain` for working directory assessment. Task directory creation employs atomic file system operations with structured template population using markdown formatting standards. Snake_case conversion algorithms process user-provided task names ensuring consistent naming across directory structures and Git branches. Git branch management uses standard Git commands including `git checkout -b [branch_name] [parent_branch]` for branch creation and `git branch -a` for branch listing. Commit operations use structured commit messages with standardized formatting for task lifecycle tracking. Error handling implements comprehensive state validation with rollback procedures ensuring consistent system state during failures. Template population uses structured markdown generation with placeholder replacement and metadata integration.

########### Code Usage Examples

This example demonstrates the Git repository validation and working directory prerequisite checks that ensure clean task creation:

```bash
# Git repository validation and working directory assessment
git rev-parse --is-inside-work-tree
git status --porcelain
# Validates repository status and detects uncommitted changes before task creation
```

This example shows the mandatory WIP task files commit procedure ensuring proper Git integration:

```bash
# Mandatory commit of WIP task files for Git branch management
git add .knowledge/work-in-progress/[task_name]/
git add .clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md
git commit -m "feat: Create WIP task '[task_name]' with initial structure

- Add WIP_TASK.md with task definition and scope  
- Add PROGRESS.md for milestone tracking
- Update Essential Knowledge Base with active task"
# Ensures WIP task files are tracked and available across branches
```

This example illustrates the Git branch creation workflow with standardized naming patterns:

```bash
# Git branch creation with standardized naming convention
git checkout -b jesse-wip/[task_name_snake_case] [parent_branch]
git branch -a
# Creates dedicated task branch following Jesse Framework naming standards
```
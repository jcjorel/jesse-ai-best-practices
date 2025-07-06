<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/embedded_content/workflows/jesse_wip_task_switch.md -->
<!-- Cached On: 2025-07-06T11:51:12.205261 -->
<!-- Source Modified: 2025-06-26T12:39:06.867045 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This workflow specification defines the complete process for safely switching between existing Work-in-Progress tasks within the Jesse Framework development environment. The functional intent centers on providing developers with a robust task context switching mechanism that maintains Git repository integrity while preserving task state and progress information. Key semantic entities include `git status --porcelain` for repository validation, `.knowledge/work-in-progress/` directory structure for task storage, `WIP_TASK.md` and `PROGRESS.md` files for task metadata, `.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md` for Essential Knowledge Base updates, and `git checkout` operations for branch switching. The workflow provides comprehensive Git safety validation, multi-task warning systems, branch compatibility checking, and automated context loading to ensure seamless transitions between parallel development efforts without data loss or state corruption.

##### Main Components

The workflow contains seven primary execution steps: Git Repository Safety Validation, List Available WIP Tasks, Display Multiple WIP Tasks Warning, Display Current Active Task, Prompt for Task Selection, Git Branch Safety Validation, Load Selected Task Context, and Update Essential Knowledge Base. Additional components include comprehensive error handling for uncommitted changes, branch switch failures, and missing task files, plus special case handling for scenarios like no active tasks, same task selection, and detached HEAD states. The workflow integrates with the Jesse Framework's knowledge management system through specific file structures and validation checkpoints.

###### Architecture & Design

The architectural design implements a multi-stage validation pattern with fail-fast error handling and rollback capabilities. The workflow follows a linear progression with mandatory safety checkpoints at each Git operation, ensuring repository integrity throughout the switching process. The design separates concerns between Git operations, file system interactions, and knowledge base updates, allowing for granular error recovery and state consistency. Branch switching operations are isolated with explicit user confirmation, while task context loading operates independently of Git state changes to prevent partial failures.

####### Implementation Approach

The implementation strategy utilizes Git porcelain commands for repository state validation, file system scanning for task discovery, and structured markdown parsing for task metadata extraction. The workflow employs conditional branching based on Git repository state, with explicit user prompts for potentially destructive operations like branch switching. Task context loading involves parsing multiple markdown files to extract objective, progress, and milestone information, while Essential Knowledge Base updates follow a structured template format for consistency across task switches.

######## External Dependencies & Integration Points

**→ References:** [external systems and files this workflow depends on]
- `git status --porcelain` - Git repository state validation command
- `.knowledge/work-in-progress/` - task storage directory structure
- `WIP_TASK.md` - individual task definition and context files
- `PROGRESS.md` - task progress tracking and milestone files
- `.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md` - Essential Knowledge Base file
- `git checkout` - Git branch switching operations

**← Referenced By:** [systems that invoke this workflow]
- Jesse Framework task management system - primary workflow consumer
- Developer workflow automation tools - task switching triggers
- CI/CD pipeline integration - automated task context management

**⚡ System role and ecosystem integration:**
- **System Role**: Serves as the core task switching orchestrator within the Jesse Framework development workflow, coordinating Git operations with knowledge management systems
- **Ecosystem Position**: Central component bridging Git repository management with task-based development workflows, ensuring data integrity during context switches
- **Integration Pattern**: Invoked by developers through command-line interfaces or IDE integrations, with dependencies on Git CLI tools and file system access for task metadata management

######### Edge Cases & Error Handling

The workflow addresses multiple critical error scenarios including uncommitted changes detection with immediate failure and clear resolution guidance, Git branch switch failures with automatic rollback to previous branch state, missing or corrupted task files with template recreation options, and Essential Knowledge Base update failures with previous active task restoration. Special handling covers no WIP tasks scenarios with creation workflow suggestions, partial switch failures ensuring complete success or rollback, branch validation errors for missing Git integration information, and detached HEAD state management for repository consistency.

########## Internal Implementation Details

The internal implementation relies on Git porcelain command parsing for repository state detection, directory traversal algorithms for task discovery excluding archived tasks, markdown file parsing for extracting task metadata including objectives and progress percentages, and template-based Essential Knowledge Base updates with timestamp management. The workflow maintains internal state tracking for rollback operations, implements atomic operations for Git branch switching, and utilizes structured error reporting with specific resolution guidance for each failure scenario.

########### Code Usage Examples

The following examples demonstrate key workflow validation patterns. Git safety validation ensures clean working directory before task switching:

```bash
# Git repository state validation command
git status --porcelain
```

Task selection interface provides numbered options with branch information:

```markdown
# Available WIP Tasks:
1️⃣ feature-authentication (branch: auth-implementation) - 65% complete
2️⃣ api-refactoring (branch: api-cleanup) - 30% complete
3️⃣ documentation-update (branch: main) - 85% complete
```

Branch switching confirmation dialog for different target branches:

```markdown
⚠️ Git Branch Switch Required
Current Task: feature-authentication
Current Branch: auth-implementation
Target Task: api-refactoring
Target Branch: api-cleanup
Continue with branch switch? [1/2]:
```
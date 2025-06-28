# Knowledge Management System

## System Directives

### Automatic Session Initialization - MANDATORY SYSTEM DIRECTIVE

**🚨 CRITICAL SYSTEM REQUIREMENT - NO EXCEPTIONS PERMITTED 🚨**

At the start of EVERY new [Cline](https://github.com/cline/cline) session, these steps are MANDATORY and MUST be executed BEFORE processing ANY user request. This is a non-negotiable system requirement that takes precedence over all other considerations:

#### MANDATORY EXECUTION SEQUENCE:
1. **MANDATORY STEP 1**: Read this file (JESSE_KNOWLEDGE_MANAGEMENT.md) completely to load system rules and essential knowledge
   - **VERIFICATION**: Confirm knowledge management rules are loaded
   - **FAILURE ACTION**: If this step fails, STOP and report system initialization error

2. **MANDATORY STEP 2**: Read `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md` for accumulated project knowledge
   - **VERIFICATION**: Confirm knowledge base content is loaded
   - **FAILURE ACTION**: If file doesn't exist, create it with basic structure

3. **MANDATORY STEP 3**: IF git clone or imported PDF references exist in .knowledge/persistent-knowledge/KNOWLEDGE_BASE.md, automatically load ALL corresponding `.knowledge/git-clones/[repo-name]_kb.md` and `.knowledge/pdf-knowledge/[PDF-name]_kb.md` files
   - **VERIFICATION**: Confirm all referenced git clone knowledge bases are loaded
   - **FAILURE ACTION**: Report missing knowledge base files

4. **MANDATORY STEP 4**: IF a current WIP task exists (as specified in the Essential Knowledge Base section), automatically load ONLY that task's files: `.knowledge/work-in-progress/[current_task]/WIP_TASK.md` and `.knowledge/work-in-progress/[current_task]/PROGRESS.md`
   - **IMPORTANT**: Load ONLY the current task, NOT other active tasks listed in "Other Active Tasks"
   - **VERIFICATION**: Confirm only the current WIP task context is loaded (unless explicitly disabled via `/jesse_wip_task_disable`)
   - **FAILURE ACTION**: Report WIP task loading issues

5. **MANDATORY STEP 5**: Display brief context summary including:
   - Current task status and available resources
   - Loaded knowledge bases count
   - Active WIP task status (if any)
   - Session initialization confirmation

6. **MANDATORY STEP 6**: Only after ALL above steps are completed successfully, proceed with user request processing

#### SESSION INITIALIZATION TRIGGERS:
- **New [Cline](https://github.com/cline/cline) conversation/chat session**
- **Fresh IDE restart with [Cline](https://github.com/cline/cline) activation**
- **Any context reset or session boundary**
- **Explicit user request for session reinitialization**

#### ENFORCEMENT MECHANISMS:
- **Self-Verification**: After each mandatory step, confirm successful completion
- **Error Reporting**: Any initialization failure must be immediately reported to user
- **No Bypass**: These steps cannot be skipped, deferred, or bypassed under any circumstances
- **Priority Override**: Session initialization takes absolute priority over user requests

#### COMPLIANCE VERIFICATION:
Before processing any user request, internally verify:
- [ ] Knowledge management rules loaded
- [ ] Essential knowledge base accessed
- [ ] Git clone knowledge bases loaded (if applicable)
- [ ] WIP task context loaded (if applicable and not disabled)
- [ ] Context summary provided to user
- [ ] All mandatory steps completed successfully

**FAILURE TO EXECUTE THIS MANDATORY SEQUENCE CONSTITUTES A CRITICAL SYSTEM ERROR**

### Session Initialization Enforcement Protocol

**IMMEDIATE COMPLIANCE CHECK**: If you are reading this file and have NOT executed the Mandatory Session Initialization sequence above, you MUST:

1. **STOP** processing any current user request immediately
2. **EXECUTE** the complete Mandatory Session Initialization sequence now
3. **REPORT** to the user: "Session initialization was incomplete. Executing mandatory knowledge loading sequence..."
4. **COMPLETE** all 6 mandatory steps before resuming any other activities
5. **CONFIRM** successful initialization with context summary

**SESSION BOUNDARY DETECTION**: A new session is detected when:
- No previous knowledge of Essential Knowledge Base content exists in current context
- No awareness of current WIP task status exists
- First interaction in a new [Cline](https://github.com/cline/cline) conversation thread
- Context has been reset or cleared

**SELF-ENFORCEMENT MECHANISM**: Every time this knowledge management file is accessed:
1. Verify that session initialization has been completed
2. If not completed, immediately execute the mandatory sequence
3. Document the initialization in your response to the user
4. Never proceed with user requests until initialization is verified complete

**CRITICAL REMINDER**: This is not a suggestion or best practice - it is a mandatory system requirement that cannot be bypassed, deferred, or ignored under any circumstances.

## Installation Location and Preferences

### Preferred Installation Location
**JESSE_*.md files and associated workflows SHOULD preferably be installed in `${USER_HOME_DIR}/Cline/Rules/` and `${USER_HOME_DIR}/Cline/Workflows/` respectively** to make them permanent and available across all projects. This ensures consistent behavior and rule enforcement regardless of the specific project being worked on.

### Installation Process Requirements
**CRITICAL**: At installation time of these files, **YOU MUST** ask the user what to do with the following exact options:

1. **OPTION 1 - PREFERRED LOCATION**: Install JESSE_*.md files at `${USER_HOME_DIR}/Cline/Rules/` and workflows at `${USER_HOME_DIR}/Cline/Workflows/`
2. **OPTION 2 - PROJECT LEVEL**: Install files at project level in `<project_root>/.clinerules/` and `<project_root>/.clinerules/workflows/`

### Location-Specific Behavior

#### When Installed at Preferred Location (${USER_HOME_DIR}/Cline/)
- **Global Rules**: All JESSE_*.md files remain in their installed state at `${USER_HOME_DIR}/Cline/Rules/`
- **Project-Specific Knowledge**: `<project_root>/.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md` contains **ONLY** project-related information:
  - Essential Knowledge Base section
  - Project-specific context
  - Current and active WIP tasks
  - Project quick access links
- **File Separation**: The global `${USER_HOME_DIR}/Cline/Rules/JESSE_KNOWLEDGE_MANAGEMENT.md` remains unchanged from installation time, containing only the system directives and operational frameworks

#### When Installed at Project Level (<project_root>/.clinerules/)
- **Self-Contained**: All JESSE_*.md files and workflows remain within the project directory
- **Complete Functionality**: The project-level `JESSE_KNOWLEDGE_MANAGEMENT.md` contains both system directives AND project-specific information
- **Project Isolation**: Rules and knowledge management are contained within the specific project scope

### File Management After Installation

#### Preferred Location Installation Protocol
1. **System Files**: JESSE_*.md files installed at `${USER_HOME_DIR}/Cline/Rules/` are never modified after installation
2. **Project Knowledge File**: Create `<project_root>/.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md` containing:
   ```markdown
   # Project Knowledge Management
   *This file contains project-specific knowledge while system rules remain at ${USER_HOME_DIR}/Cline/Rules/*
   
   # Essential Knowledge Base
   [Project-specific content only]
   ```
3. **Workflow Access**: Workflows at `${USER_HOME_DIR}/Cline/Workflows/` remain globally accessible
4. **Consistency**: Project knowledge file follows same structure as global file but contains only project-related sections

#### Installation Verification
After installation, verify:
- [ ] User choice was explicitly requested and confirmed
- [ ] Files are installed at chosen location
- [ ] If preferred location: project knowledge file created with appropriate content separation at `<project_root>/.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md`
- [ ] All workflow references remain functional regardless of installation location

#### Critical File Location Reminder
**IMPORTANT**: When using global deployment (`${USER_HOME_DIR}/Cline/Rules/`), the project-specific knowledge file must ALWAYS be created at:
- ✅ **CORRECT**: `<project_root>/.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md`
- ❌ **INCORRECT**: `<project_root>/JESSE_KNOWLEDGE_MANAGEMENT.md` (this is the root cause of common installation errors)

This ensures proper project isolation and prevents conflicts with global framework rules.

### Knowledge Capture Rules
- **Automatic Capture**: When user says "remember this", "capture this knowledge", or similar phrases, automatically append structured information to appropriate knowledge files
- **Intemporal Writing**: All knowledge entries must be written in present tense, stating facts rather than referencing past implementations
- **Consistency Maintenance**: Essential Knowledge Base and WIP Task learnings must never contradict each other
- **Single Source of Truth**: Each piece of knowledge has consistent representation across all knowledge files
- **External Knowledge Auto-Capture**: Knowledge gathered through Perplexity MCP server and direct Web Browsing must be **AUTOMATICALLY** captured:
  - **If active WIP task exists**: Append knowledge to `.knowledge/work-in-progress/[current_task]/WIP_TASK.md`
  - **If no active task**: Append knowledge to `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md`
  - **No manual trigger required**: This capture happens automatically whenever external knowledge is retrieved
- **Test Result Auto-Update**: When executing any test, automatically update the current WIP task's PROGRESS.md file with test results:
  - **If active WIP task exists**: Update `.knowledge/work-in-progress/[current_task]/PROGRESS.md` with test outcome, timestamp, and relevant details
  - **Include both successful and failed test results**: Document what was tested, the result, and any significant findings or error messages
  - **Overwrite previous results**: Replace any existing test status and context for the same test rather than accumulating multiple entries
  - **Automatic execution**: This update happens automatically whenever tests are run, no manual trigger required
  - **If no active WIP task**: Test results are not automatically captured (focus on current task context)
  - **Standardized logging format**: Use this exact format for test result entries in PROGRESS.md:
    ```
    ## Test Status: [Test Name/Description]
    **Status**: ✅ PASSED | ❌ FAILED | 🔄 RUNNING | ⏸️ SKIPPED
    **Timestamp**: YYYY-MM-DDThh:mm:ssZ
    **Test Command**: [exact command executed]
    **Result Summary**: [brief outcome description]
    **Details**: [relevant findings, error messages, or significant observations]
    **Context**: [any additional context relevant to debugging or understanding]
    ```

### Current vs. Other Active Tasks Policy
- **Current WIP Task**: The single task currently being worked on, loaded automatically at session start
- **Other Active Tasks**: Tasks that exist but are NOT the current focus, these are NOT loaded automatically
- **Task Switching**: Use `/jesse_wip_task_switch.md` workflow to change which task is current
- **Single Task Focus**: Only one WIP task can be "current" at any time to maintain clear context

### Git Branch Integration Policy
**CRITICAL**: WIP tasks include comprehensive Git branch management integration:

#### Git Branch Tracking
- **All WIP tasks track their associated Git branch** in WIP_TASK.md Git Integration section
- **Branch information includes**: Branch name, parent branch, creation timestamp, and status
- **Branch status values**: Active, Merged, Deleted
- **Branch naming convention**: Proposed format `jesse-wip/[task_name]` but user can customize

#### Git Safety Requirements
- **Clean Working Directory Prerequisite**: ALL WIP task operations require clean Git working directory
  - **Task Creation**: Cannot create WIP task with uncommitted changes
  - **Task Switching**: Cannot switch WIP tasks with uncommitted changes  
  - **Task Completion**: Git operations require clean state for merge assistance
- **Mandatory Commit Flow**: WIP task files must be committed before Git branch operations
- **Branch Isolation**: Each WIP task can have its own dedicated Git branch for work isolation

#### Git Branch Management Features
- **Task Creation**: Offers branch creation with parent branch selection and custom naming
- **Task Switching**: Automatic Git branch switching when tasks use different branches
- **Task Completion**: Comprehensive merge assistance with multiple merge strategies:
  - Fast-Forward Merge (clean linear history)
  - Three-Way Merge (preserves branch context)
  - Squash and Merge (single commit for feature)
  - Rebase and Merge (clean linear history with individual commits)
- **Branch Cleanup**: Explicit user choice for branch deletion after merge

#### Multiple Tasks Branch Conflict Management
- **Same Branch Detection**: System detects when multiple WIP tasks share the same branch
- **Manual Management Warning**: Users warned about manual Git management requirements
- **Branch Deletion Restrictions**: Automatic branch operations disabled when multiple tasks share branch
- **User Guidance**: Clear explanations provided for complex Git scenarios

#### Git Repository Validation
- **Repository Detection**: All workflows validate Git repository presence before offering Git features
- **Fallback Behavior**: WIP tasks function normally in non-Git environments
- **Error Handling**: Comprehensive Git operation failure recovery with clear user guidance

### Git Clone Storage Policy
**CRITICAL**: All git clones are stored **EXCLUSIVELY** in `<project_root>/.knowledge/git-clones/` directory.

- **Single Location Rule**: Git clones must **NEVER** exist anywhere else in the project structure
- **No Exceptions**: This policy has no exceptions - all external repositories are cloned only to `.knowledge/git-clones/`
- **Centralized Management**: This ensures consistent knowledge management and prevents scattered repository copies
- **Version Control Separation**: Keeps external repository content separate from project codebase through .gitignore rules

### Large File Processing Protocol
When attempting to access files from git clones (which are exclusively located in `.knowledge/git-clones/`):
1. Check if file is documented in corresponding `[repo-name]_kb.md`
2. If not documented and file exceeds 4000 lines:
   - Mark file in `KNOWLEDGE_BASE.md` as requiring processing with priority "**before any other tasks**"
   - Warn user about context window limitations
   - Recommend dedicated processing session using `/jesse_wip_task_process_large_file.md`

### Git Clone .gitignore Requirements
When any git clone is added to the knowledge base, the `<project_root>/.gitignore` file MUST contain these exact rules:

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
- The git clones index file (`README.md`) is maintained in version control
- External repository content remains separate from project codebase

This `.gitignore` configuration enforces the exclusive storage policy by ensuring that only the centralized `.knowledge/git-clones/` location is managed for git clone content.

## Operational Modes Integration

### ACT Mode Enhancement
- Knowledge capture operates seamlessly during implementation
- Automatic context loading does not interrupt task execution
- WIP task progress updates occur after significant milestones

### PLAN Mode Enhancement
- WIP task creation automatically triggers PLAN mode for complex tasks
- Knowledge base consultation informs planning decisions
- Task scope and success criteria benefit from accumulated learnings

### DESIGN Mode Enhancement
- Knowledge base provides historical context for design decisions
- WIP tasks can reference design documentation
- Captured patterns inform architectural choices

## Workflow Commands

Users can invoke knowledge management workflows using `/[workflow-name].md` syntax:

### Core Workflows
- `/jesse_wip_task_create.md` - Create new Work-in-Progress task
- `/jesse_wip_task_switch.md` - Switch between existing WIP tasks
- `/jesse_wip_task_complete.md` - Complete current WIP task and extract learnings
- `/jesse_wip_task_archive.md` - Archive WIP task without completion processing
- `/jesse_wip_task_capture_knowledge.md` - Capture and structure knowledge
- `/jesse_wip_kb_git_clone_import.md` - Add external git repository to knowledge base
- `/jesse_wip_task_check_consistency.md` - Verify knowledge consistency
- `/jesse_wip_task_process_large_file.md` - Process large files from git clones
- `/jesse_wip_task_disable.md` - Temporarily disable WIP task auto-loading for current session
- `/jesse_wip_kb_pdf_import.md` - Import and index PDF documents with LLM-based understanding

### Workflow Execution Rules
- Workflows operate in current operational mode unless explicitly specified
- Knowledge updates maintain consistency across all related files
- Workflow completion includes verification of knowledge integrity
- Failed workflows must restore previous consistent state

---

# Essential Knowledge Base
*Last Updated: 2025-06-21T23:20:00Z*

## Current Work-in-Progress Task
**Active Task**: None
**Status**: None
**Last Updated**: YYYY-MM-DDThh:mm:ssZ
**Phase**: None
**Next Action**: "Define a current WIP task"

## Other Active Tasks
*Note: These tasks exist but are NOT loaded automatically. Use /jesse_wip_task_switch to make one current.*
- None currently active

## Recently Completed
- `audio_device_management` - Completed 2025-06-21T23:20:00Z, archived with full knowledge extraction

## Quick Access Links
- [Persistent Knowledge Base](.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md)
- [WIP Tasks Directory](.knowledge/work-in-progress/)
- [Git Clones Directory](.knowledge/git-clones/)

## Project Context
This project (nova-sonic-ui) appears to be a speech-to-text application with AWS integration, featuring a Nova Sonic speech processing backend and comprehensive testing infrastructure.

## Key Project Components
- **Backend Services**: FastAPI-based backend with AWS Nova Sonic integration
- **Audio Processing**: WebM/Opus audio format handling with streaming capabilities
- **Testing Framework**: Comprehensive test suite with CLI tools and performance benchmarks
- **Documentation**: Extensive API and architecture documentation
- **Development Tools**: Docker containerization and debugging scripts

# WIP Task Creation Workflow

## Workflow Purpose
Create a new Work-in-Progress task with proper structure, templates, Git branch management, and integration with the knowledge management system.

## Execution Steps

### 1. Git Repository Validation
Check if current directory is a Git repository:
- Run `git rev-parse --is-inside-work-tree`
- If NOT a Git repository: Continue without Git features, inform user
- If IS a Git repository: Proceed with Git integration features

### 1.5. Git Working Directory Prerequisites
**CRITICAL**: Before any task creation, validate Git repository state:

```
### 🔍 Git Working Directory Check

Validating Git repository state for WIP task creation...
Checking for uncommitted changes: git status --porcelain
```

**If Uncommitted Changes Found:**
```
❌ WIP Task Creation Prerequisites Not Met

Your Git working directory has uncommitted changes that must be resolved 
before creating a new WIP task.

Current uncommitted changes:
• [list each file with status]

📋 Why This Requirement Exists:
• WIP task creation involves committing task files to enable Git branch management
• Mixing unrelated changes with WIP task commits creates confusing Git history
• Clean branch operations require a clean working directory
• Task isolation is compromised when mixed with unrelated changes

🔧 Required Actions (choose one):

1️⃣ Commit your current changes:
   git add .
   git commit -m "Your descriptive commit message"

2️⃣ Stash your current changes:
   git stash push -m "Temporary stash - will create WIP task next"

3️⃣ Reset your changes (⚠️ DESTRUCTIVE - changes will be lost):
   git reset --hard HEAD

After resolving uncommitted changes, you can retry WIP task creation.

❌ WIP Task Creation Cancelled
```

**If Working Directory is Clean:**
```
✅ Git Working Directory Clean
No uncommitted changes detected. Proceeding with WIP task creation...
```

### 2. Gather Task Information
Prompt user for the following information:
- **Task Name**: Brief descriptive name (will be converted to snake_case for directory)
- **Objective**: Clear statement of what needs to be accomplished
- **Target Timeline**: Estimated completion date
- **Scope**: What is included and excluded from this task

### 2.5. Check for Existing WIP Tasks and Warn About Parallel Work
Check if any WIP tasks already exist in `.knowledge/work-in-progress/`:
- If YES: Display parallel task warning
- If NO: Proceed directly to step 3

**Parallel Task Warning (if applicable):**
```
⚠️ WARNING: Multiple WIP Tasks Detected ⚠️

You currently have [N] active WIP task(s). Working with multiple parallel WIP tasks carries significant risks:

• **State Inconsistency Risk**: Changes made in one task may render the state and progress of other tasks out of sync
• **File Conflict Risk**: Modifying files tracked in multiple tasks can create conflicting implementations
• **Context Confusion**: Switching between tasks may lead to mixing concerns and implementations

RECOMMENDATION: Create parallel WIP tasks ONLY when working on completely different sets of files and features.

To mitigate risks, would you like to restrict this new task to specific files or directories?
[Yes/No]
```

If user chooses Yes:
- Prompt for list of files/directories to include
- Document these restrictions in the task's scope section
- Add a "**File Restrictions**" subsection under the Scope section in WIP_TASK.md

### 3. Create Task Directory Structure
Generate unique snake_case directory name from task name and create:
```
.knowledge/work-in-progress/[task_name_snake_case]/
├── WIP_TASK.md
└── PROGRESS.md
```

### 4. Populate WIP_TASK.md Template
Create WIP_TASK.md with the following structure:
```markdown
# Task: [Task Name]

## Git Integration
- **Branch**: [To be determined during setup]
- **Parent Branch**: [To be determined if new branch created]
- **Branch Created**: [Timestamp if new branch created]
- **Branch Status**: Active

## Task Context

### Objective
[User-provided objective]

### Scope
- **In Scope**: [User-provided scope items]
- **Out of Scope**: [User-provided exclusions]
- **File Restrictions**: [Only included if user chose to restrict task to specific files/directories]
  - [List of restricted files/directories]

### Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]

### Dependencies
- [External dependencies]
- [Internal project dependencies]

### Timeline
- **Started**: [Current date]
- **Target**: [User-provided target date]
- **Milestones**: [Key checkpoints]

## Task Learnings

### Key Discoveries
*No discoveries recorded yet*

### Patterns Identified
*No patterns identified yet*

### Challenges & Solutions
*No challenges documented yet*

## Task Resources

### External Links
*No external links captured yet*

### Reference Materials
*No reference materials added yet*

### Tools & APIs
*No tools or APIs documented yet*
```

### 4.5. Mandatory WIP Task Files Commit
**CRITICAL**: After creating WIP task files, they must be committed before Git branch operations:

```
### 📝 WIP Task Files Commit Required

The following WIP task files have been created:
• .knowledge/work-in-progress/[task_name]/WIP_TASK.md
• .knowledge/work-in-progress/[task_name]/PROGRESS.md
• Updated: .clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md (Essential Knowledge Base)

🔒 CRITICAL: Git Branch Management Requirement

To proceed with Git branch creation and management, these WIP task files must be 
committed to the repository. This ensures:

✅ Clean working directory for branch operations
✅ WIP task files are tracked and available across branches
✅ Safe branch switching without losing task context
✅ Proper Git history for task lifecycle

📋 Proposed commit message:
"feat: Create WIP task '[task_name]' with initial structure

- Add WIP_TASK.md with task definition and scope  
- Add PROGRESS.md for milestone tracking
- Update Essential Knowledge Base with active task"

Do you want to commit these WIP task files now?

1️⃣ Yes, commit the WIP task files (REQUIRED to continue with Git features)
2️⃣ No, do not commit (will terminate WIP task creation process)

⚠️  WARNING: Choosing option 2 will completely cancel the WIP task creation 
   process and remove the created files.

Choose option [1/2]:
```

**If User Chooses Option 2 (No Commit):**
```
❌ WIP Task Creation Terminated

WIP task creation has been cancelled because Git branch management requires 
committed WIP task files for safe operation.

Why this requirement exists:
• Git branch switching requires a clean working directory
• Uncommitted WIP files would be lost or cause conflicts during branch operations  
• Task continuity across branch switches requires tracked files
• Proper task lifecycle management needs Git history

Cleanup performed:
• Removed .knowledge/work-in-progress/[task_name]/ directory
• Reverted Essential Knowledge Base changes
• Repository returned to original state

To create a WIP task with Git integration, you must allow the initial commit.
For WIP tasks without Git integration, consider using a non-Git workflow.
```

**If User Chooses Option 1 (Commit Allowed):**
Execute the commit:
- `git add .knowledge/work-in-progress/[task_name]/`
- `git add .clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md`
- `git commit -m "[proposed_commit_message]"`

### 4.8. Git Branch Management Setup
After successfully committing WIP task files, proceed with Git branch integration:

**Check for Multiple WIP Tasks on Current Branch:**
- Scan existing WIP tasks for same branch
- If >1 active WIP task on current branch:
  ```
  ⚠️ Multiple WIP tasks detected on branch [branch_name]. You will need to manage 
  branch deletion manually when completing tasks.
  ```

**Present Git Branch Options:**
```
🌿 Git Branch Management

Current branch: [current_branch_name]

How would you like to handle Git branching for this WIP task?

1️⃣ Create a new branch for this WIP task
   • Isolates your work from other changes
   • Enables clean merge strategies
   • Recommended for significant changes

2️⃣ Use current branch ([current_branch_name]) for this WIP task
   • Continue working on existing branch
   • No branch switching required
   • Good for small fixes or when branch is already task-specific

Choose option [1/2]:
```

**Branch Creation Flow (if option 1 selected):**
```
🔧 Branch Creation Setup

Proposed branch name: jesse-wip/[task_name_snake_case]

1️⃣ Use proposed name: jesse-wip/[task_name_snake_case]
2️⃣ Enter custom branch name

Choose option [1/2]:
```

If custom name selected, prompt: "Enter branch name: "

**Parent Branch Selection:**
```
🌳 Parent Branch Selection

Create new branch as child of:

1️⃣ Current branch ([current_branch_name])
2️⃣ Choose from available branches

Choose option [1/2]:
```

If option 2: List all branches with `git branch -a` and let user select

**Execute Branch Creation:**
- Create branch: `git checkout -b [new_branch_name] [parent_branch]`
- Update WIP_TASK.md Git Integration section with:
  - Branch: [new_branch_name]  
  - Parent Branch: [parent_branch_name]
  - Branch Created: [current_timestamp]
  - Branch Status: Active

**If Option 2 Selected (Use Current Branch):**
- Update WIP_TASK.md Git Integration section with:
  - Branch: [current_branch_name]
  - Parent Branch: N/A (using existing branch)
  - Branch Created: N/A
  - Branch Status: Active

### 5. Populate PROGRESS.md Template
Create PROGRESS.md with the following structure:
```markdown
# Progress Tracking: [Task Name]

## Current Status
**Overall Progress**: 0% complete
**Current Phase**: Planning
**Last Updated**: [Current date and time]

## Completed Milestones
*No milestones completed yet*

## Upcoming Milestones
- [Target Date] - [Milestone description]

## Blockers & Issues
*No blockers identified yet*
```

### 6. Update Essential Knowledge Base
Update `.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md` Essential Knowledge Base section:
- Set new task as active task
- Update task status, purpose, start date, and priority
- Update "Next Actions" with immediate task steps

### 7. Display Confirmation
Show user:
- Task creation confirmation
- Task directory path
- Quick access links to WIP_TASK.md and PROGRESS.md
- Summary of next steps

## Workflow Completion
- Verify all files are created successfully
- Confirm Essential Knowledge Base is updated
- Set task as active in knowledge management system
- Provide user with task context summary

## Error Handling
- **Git Prerequisites**: If uncommitted changes exist, fail immediately with clear guidance
- **Task Name Conflicts**: If task name conflicts with existing task, prompt for alternative name
- **File Creation Failures**: Clean up partial directory structure if file creation fails
- **Commit Failures**: If WIP files commit fails, clean up created files and restore state
- **Branch Creation Failures**: If branch creation fails, provide fallback to current branch usage
- **Essential Knowledge Base**: If update fails, restore previous state and provide rollback
- **Partial Failures**: Ensure consistent state - either complete success or complete rollback

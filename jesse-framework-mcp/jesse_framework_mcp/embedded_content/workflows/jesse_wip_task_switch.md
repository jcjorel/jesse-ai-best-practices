# WIP Task Switch Workflow

## Workflow Purpose
Switch between existing Work-in-Progress tasks with Git branch safety validation, updating the active task context and loading relevant task information.

## Execution Steps

### 1. Git Repository Safety Validation
**CRITICAL**: Before any task switching, validate Git repository state:

```
### 🔍 Git Safety Check for Task Switching

Validating Git repository state for safe task switching...
Checking for uncommitted changes: git status --porcelain
```

**If Uncommitted Changes Found:**
```
❌ Cannot Switch WIP Tasks

You have uncommitted changes in your working directory.
Please commit or stash your changes before switching WIP tasks.

Current changes:
[list of modified files with status]

🔧 Options to resolve:
• git add . && git commit -m "WIP: [description]"
• git stash push -m "Temporary stash before task switch"

WIP task switching requires a clean working directory for safe Git operations.

❌ Task Switch Cancelled
```

**If Working Directory is Clean:**
```
✅ Git Working Directory Clean
No uncommitted changes detected. Safe to proceed with task switching...
```

### 2. List Available WIP Tasks
Scan `.knowledge/work-in-progress/` directory for existing tasks:
- List all task directories (excluding `_archived/`)
- For each task, display:
  - Task name (from directory name)
  - Current status (from PROGRESS.md)
  - Git branch (from WIP_TASK.md Git Integration section)
  - Last updated date
  - Brief objective (from WIP_TASK.md)

### 2.5. Display Multiple WIP Tasks Warning
If more than one WIP task exists, display warning:

```
⚠️ WARNING: Multiple WIP Tasks Detected ⚠️

You have [N] active WIP task(s). Switching between parallel WIP tasks carries significant risks:

• **State Inconsistency Risk**: Changes made in one task may render the state and progress of other tasks out of sync
• **File Conflict Risk**: Modifying files tracked in multiple tasks can create conflicting implementations
• **Context Confusion**: Switching between tasks may lead to mixing concerns and implementations

RECOMMENDATION: Work with parallel WIP tasks ONLY when they involve completely different sets of files and features.

Before switching tasks, consider:
1. Have you documented all current progress in the active task?
2. Are there any uncommitted changes that might conflict with the target task?
3. Do these tasks modify any of the same files?
4. Do these tasks use different Git branches that require branch switching?
```

### 3. Display Current Active Task
Show currently active task from Essential Knowledge Base:
- Current active task name
- Task status and progress
- Last activity date

### 4. Prompt for Task Selection
Present user with:
- Numbered list of available tasks with Git branch information
- Option to cancel switch operation
- Brief description of each task's current state
- Git branch for each task clearly indicated

### 4.5. Git Branch Safety Validation
After user selects target task, perform Git branch safety checks:

**Get Current and Target Task Branch Information:**
- Get current task branch from current WIP_TASK.md Git Integration section
- Get target task branch from target WIP_TASK.md Git Integration section
- Compare branches for compatibility

**If Branches are the Same:**
```
✅ Git Branch Compatibility
Both tasks use the same branch: [branch_name]
Safe to switch without branch operations.
```

**If Branches are Different:**
```
⚠️ Git Branch Switch Required

Current Task: [current_task_name]
Current Branch: [current_branch_name]

Target Task: [target_task_name]  
Target Branch: [target_branch_name]

Switching WIP tasks will also switch Git branches. This means:
• Your working directory will change to reflect the target branch
• Files may appear/disappear based on branch differences
• Any uncommitted work should be committed first (already verified)
• Branch context will change to match the target task

Continue with branch switch?

1️⃣ Yes, switch to [target_branch_name] and load [target_task_name]
2️⃣ No, cancel the switch operation

Choose option [1/2]:
```

**Execute Branch Switch (if confirmed):**
- Switch to target branch: `git checkout [target_branch_name]`
- Verify successful branch switch
- Display confirmation of branch change

**If Branch Switch Cancelled:**
```
❌ Task Switch Cancelled
Remaining on current task: [current_task_name]
Branch remains: [current_branch_name]
```

### 5. Load Selected Task Context
Once branch operations are complete, load task context:
- Read WIP_TASK.md for task context
- Read PROGRESS.md for current status
- Extract key information:
  - Task objective and scope
  - Current progress percentage
  - Git branch information
  - Active milestones
  - Recent discoveries or challenges
  - Available resources

### 6. Update Essential Knowledge Base
Update `.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md` Essential Knowledge Base section:
- Set selected task as new active task
- Update task status, purpose, and priority
- Update "Next Actions" based on task progress
- Update timestamp for last session context

### 7. Display Task Context Summary
Show user comprehensive task summary:
- Task objective and current status
- Git branch and integration status
- Recent progress and completed milestones
- Upcoming milestones and deadlines
- Active blockers or challenges
- Available resources and reference materials
- Suggested next actions

## Workflow Completion
- Verify Essential Knowledge Base is updated with new active task
- Confirm task context is properly loaded
- Display quick access links to task files
- Provide summary of immediate next steps

## Error Handling
- **No WIP Tasks**: If no WIP tasks exist, suggest creating a new task using `/jesse_wip_task_create.md`
- **Uncommitted Changes**: If uncommitted changes exist, fail immediately with clear guidance
- **Git Branch Switch Failures**: If branch switch fails, restore to previous branch and cancel task switch
- **Missing Task Files**: If selected task files are corrupted or missing, offer to recreate templates
- **Essential Knowledge Base Failures**: If update fails, restore previous active task
- **Partial Switch Failures**: Ensure consistent state - either complete success or complete rollback
- **Branch Validation Errors**: Handle cases where Git branch information is missing or invalid

## Special Cases
- **No Active Task**: If no task is currently active, simply set selected task as active (no branch switching needed)
- **Same Task Selected**: If user selects currently active task, display current context without changes
- **Same Branch Tasks**: If tasks share the same Git branch, switch without Git operations
- **No Git Integration**: Handle tasks without Git Integration section gracefully
- **Archived Tasks**: Do not include archived tasks in selection list
- **Incomplete Tasks**: Handle tasks with missing PROGRESS.md or WIP_TASK.md files gracefully
- **Detached HEAD**: Handle cases where repository is in detached HEAD state

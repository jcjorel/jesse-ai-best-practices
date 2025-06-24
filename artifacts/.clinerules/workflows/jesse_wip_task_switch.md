# WIP Task Switch Workflow

## Workflow Purpose
Switch between existing Work-in-Progress tasks, updating the active task context and loading relevant task information.

## Execution Steps

### 1. List Available WIP Tasks
Scan `.knowledge/work-in-progress/` directory for existing tasks:
- List all task directories (excluding `_archived/`)
- For each task, display:
  - Task name (from directory name)
  - Current status (from PROGRESS.md)
  - Last updated date
  - Brief objective (from WIP_TASK.md)

### 1.5. Display Multiple WIP Tasks Warning
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
```

### 2. Display Current Active Task
Show currently active task from Essential Knowledge Base:
- Current active task name
- Task status and progress
- Last activity date

### 3. Prompt for Task Selection
Present user with:
- Numbered list of available tasks
- Option to cancel switch operation
- Brief description of each task's current state

### 4. Load Selected Task Context
Once user selects a task:
- Read WIP_TASK.md for task context
- Read PROGRESS.md for current status
- Extract key information:
  - Task objective and scope
  - Current progress percentage
  - Active milestones
  - Recent discoveries or challenges
  - Available resources

### 5. Update Essential Knowledge Base
Update `.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md` Essential Knowledge Base section:
- Set selected task as new active task
- Update task status, purpose, and priority
- Update "Next Actions" based on task progress
- Update timestamp for last session context

### 6. Display Task Context Summary
Show user comprehensive task summary:
- Task objective and current status
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
- If no WIP tasks exist, suggest creating a new task using `/jesse_wip_task_create.md`
- If selected task files are corrupted or missing, offer to recreate templates
- If Essential Knowledge Base update fails, restore previous active task
- Handle cases where task directory exists but files are missing

## Special Cases
- **No Active Task**: If no task is currently active, simply set selected task as active
- **Same Task Selected**: If user selects currently active task, display current context without changes
- **Archived Tasks**: Do not include archived tasks in selection list
- **Incomplete Tasks**: Handle tasks with missing PROGRESS.md or WIP_TASK.md files gracefully

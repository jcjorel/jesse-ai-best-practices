# WIP Task Creation Workflow

## Workflow Purpose
Create a new Work-in-Progress task with proper structure, templates, and integration with the knowledge management system.

## Execution Steps

### 1. Gather Task Information
Prompt user for the following information:
- **Task Name**: Brief descriptive name (will be converted to snake_case for directory)
- **Objective**: Clear statement of what needs to be accomplished
- **Target Timeline**: Estimated completion date
- **Scope**: What is included and excluded from this task

### 1.5. Check for Existing WIP Tasks and Warn About Parallel Work
Check if any WIP tasks already exist in `.knowledge/work-in-progress/`:
- If YES: Display parallel task warning
- If NO: Proceed directly to step 2

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

### 2. Create Task Directory Structure
Generate unique snake_case directory name from task name and create:
```
.knowledge/work-in-progress/[task_name_snake_case]/
├── WIP_TASK.md
└── PROGRESS.md
```

### 3. Populate WIP_TASK.md Template
Create WIP_TASK.md with the following structure:
```markdown
# Task: [Task Name]

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

### 4. Populate PROGRESS.md Template
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

### 5. Update Essential Knowledge Base
Update `.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md` Essential Knowledge Base section:
- Set new task as active task
- Update task status, purpose, start date, and priority
- Update "Next Actions" with immediate task steps

### 6. Display Confirmation
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
- If task name conflicts with existing task, prompt for alternative name
- If file creation fails, clean up partial directory structure
- If Essential Knowledge Base update fails, restore previous state
- Provide clear error messages and recovery options

# WIP Task Archive Workflow

## Workflow Purpose
Archive a Work-in-Progress task without full completion processing, preserving task information while removing it from active task management.

## Execution Steps

### 1. List Available Tasks for Archival
Display all available WIP tasks for archival selection:
- List all task directories in `.knowledge/work-in-progress/` (excluding `_archived/`)
- Show task information for each:
  - Task name and directory
  - Current status from PROGRESS.md
  - Last updated date
  - Brief objective from WIP_TASK.md
- Include currently active task in the list

### 2. Prompt for Task Selection
Present user with:
- Numbered list of available tasks
- Option to cancel archive operation
- Warning about archival implications (task becomes read-only)
- Confirmation that valuable learnings should be extracted before archival

### 3. Extract Valuable Learnings (Optional)
Before archiving, offer to extract key learnings:
- Prompt user if they want to extract learnings to persistent knowledge
- If yes, process key discoveries, patterns, and solutions from WIP_TASK.md
- Add extracted knowledge to `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md`
- Use intemporal writing format for extracted learnings
- Skip detailed completion processing (unlike full completion workflow)

### 4. Create Archive Directory
Prepare archived task location:
- Generate timestamped archive directory name: `[task_name]_archived_[YYYYMMDD_HHMMSS]`
- Create directory in `.knowledge/work-in-progress/_archived/`
- Ensure archive directory name doesn't conflict with existing archives

### 5. Move Task to Archive
Transfer task files to archived location:
- Move entire task directory to `_archived/[timestamped_directory_name]/`
- Preserve all original files: WIP_TASK.md, PROGRESS.md, and any additional files
- Verify all files transferred successfully
- Remove original task directory from active work-in-progress area

### 6. Add Archive Metadata
Create archive summary in archived task directory:
- Add `ARCHIVE_INFO.md` file with:
  - Archive date and time
  - Reason for archival (incomplete, superseded, cancelled, etc.)
  - Final status at time of archival
  - Any extracted learnings summary
  - Original task timeline and objectives

### 7. Update Essential Knowledge Base
If archived task was the active task:
- Clear active task from `.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md`
- Set active task to "None"
- Update session context to reflect archival
- Update "Next Actions" to suggest next steps
- Update timestamp

### 8. Update Knowledge References
Clean up any references to archived task:
- Check persistent knowledge for references to archived task
- Update or remove outdated cross-references
- Maintain knowledge consistency across all files

### 9. Display Archive Confirmation
Show user:
- Archive completion confirmation
- Archive location and directory name
- Summary of any learnings extracted
- Suggestions for next actions (create new task, switch to existing task)

## Archive Information Template

The `ARCHIVE_INFO.md` file created in each archived task should follow this format:

```markdown
# Archive Information: [Task Name]

## Archive Details
**Archived Date**: [ISO timestamp]
**Archive Reason**: [Incomplete/Superseded/Cancelled/Other]
**Final Status**: [Last known status from PROGRESS.md]
**Progress at Archive**: [Percentage complete]

## Original Task Information
**Started**: [Original start date]
**Target Completion**: [Original target date]
**Priority**: [Original priority level]
**Objective**: [Original task objective]

## Archive Summary
**Key Achievements**: [What was accomplished]
**Remaining Work**: [What was left incomplete]
**Learnings Extracted**: [Yes/No - whether learnings were saved to persistent knowledge]

## Access Information
**Original Location**: `.knowledge/work-in-progress/[original_directory]/`
**Archive Location**: `.knowledge/work-in-progress/_archived/[archive_directory]/`
**Files Preserved**: [List of files in archive]

## Notes
[Any additional context about why task was archived]
```

## Workflow Completion
- Verify task is properly moved to archived location
- Confirm all original files are preserved in archive
- Verify Essential Knowledge Base is updated if necessary
- Check that no broken references remain in knowledge base
- Display archive summary and next action suggestions

## Error Handling
- If no WIP tasks exist, inform user and suggest task creation
- If selected task doesn't exist or is corrupted, offer to clean up references
- If archive operation fails, preserve task in original location
- If Essential Knowledge Base update fails, restore previous active task state
- Provide rollback options if archival process fails partway through

## Special Cases
- **Active Task Archival**: If archiving the currently active task, clear active status
- **Incomplete Task Files**: Handle tasks with missing PROGRESS.md or WIP_TASK.md gracefully
- **Large Tasks**: Handle tasks with many additional files or subdirectories
- **Duplicate Archives**: Prevent conflicts with existing archived tasks of same name

## Post-Archive Options
After successful archival, offer user:
- Create new WIP task for different objective
- Switch to existing active WIP task
- Review archived tasks for reference
- Extract additional learnings from archived task if needed

## Archive Access
Archived tasks remain accessible for reference:
- All files preserved in read-only archive location
- Archive information provides context for future reference
- Learnings may be extracted from archived tasks at any time
- Archives can be restored to active status if needed (manual process)

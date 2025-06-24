# WIP Task Completion Workflow

## Workflow Purpose
Complete the current Work-in-Progress task, extract valuable learnings to persistent knowledge, and properly archive the task.

## Execution Steps

### 1. Verify Active Task
Confirm there is an active WIP task to complete:
- Check Essential Knowledge Base for active task
- Verify task directory and files exist
- Display current task summary for user confirmation

### 2. Extract Task Learnings
Process WIP_TASK.md to extract reusable knowledge:
- **Key Discoveries**: Extract discoveries that apply beyond this specific task
- **Patterns Identified**: Document reusable patterns for future reference
- **Challenges & Solutions**: Extract solutions that could help with similar future challenges
- **Tools & APIs**: Document useful tools and API knowledge for persistent reference

### 3. Update Persistent Knowledge Base
Append extracted learnings to `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md`:
- Add new patterns to "Patterns and Solutions" section
- Add API knowledge to "External APIs" section
- Add web resources to "Web Resources" section if any were captured
- Maintain intemporal writing style (present tense, factual statements)

### 4. Generate Task Completion Summary
Create completion summary including:
- Task objective and final outcome
- Key achievements and deliverables
- Lessons learned and knowledge gained
- Time invested and efficiency metrics
- Recommendations for similar future tasks

### 5. Archive Task
Move completed task to archived location:
- Create timestamped directory in `.knowledge/work-in-progress/_archived/`
- Move entire task directory to archived location
- Preserve all task files and progress history
- Update archived task with completion timestamp and summary

### 6. Update Essential Knowledge Base
Update `.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md` Essential Knowledge Base section:
- Clear active task (set to "None")
- Update session context with completion
- Update "Next Actions" to suggest next steps
- Update timestamp

### 7. Display Completion Confirmation
Show user:
- Task completion confirmation
- Summary of knowledge extracted to persistent storage
- Archive location of completed task
- Suggestions for next actions or new tasks

## Knowledge Extraction Guidelines

### Intemporal Writing Standards
When extracting learnings to persistent knowledge:
- Write in present tense: "This approach works" not "This approach worked"
- State facts rather than historical events: "The API requires authentication" not "We discovered the API requires authentication"
- Focus on what IS known rather than what WAS learned
- Maintain consistency with existing knowledge entries

### Knowledge Categories
Extract learnings into appropriate categories:
- **Patterns**: Reusable approaches and architectural patterns
- **Solutions**: Specific solutions to common problems
- **APIs**: External service knowledge and usage patterns
- **Tools**: Useful development tools and their applications
- **Resources**: Valuable reference materials and documentation

## Workflow Completion
- Verify task is properly archived with all files intact
- Confirm persistent knowledge is updated with extracted learnings
- Verify Essential Knowledge Base reflects completion
- Check for knowledge consistency across all files

## Error Handling
- If no active task exists, inform user and suggest task switching or creation
- If task files are missing or corrupted, offer to complete with available information
- If archival fails, preserve task in current location and log error
- If knowledge extraction fails, complete archival but warn about lost learnings
- Provide rollback options if completion process fails partway through

## Post-Completion Options
After successful completion, offer user:
- Create new WIP task for next objective
- Switch to existing WIP task
- Review archived tasks for reference
- Update project documentation based on learnings

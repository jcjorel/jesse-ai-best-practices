# WIP Task Completion Workflow

## Workflow Purpose
Complete the current Work-in-Progress task, extract valuable learnings to persistent knowledge, handle Git branch operations, and properly archive the task.

## Execution Steps

### 1. Verify Active Task
Confirm there is an active WIP task to complete:
- Check Essential Knowledge Base for active task
- Verify task directory and files exist
- Display current task summary for user confirmation

### 1.5. Git Branch Assessment and Merge Assistance
After verifying the active task, check for Git branch integration:

**Check if WIP task has dedicated Git branch:**
- Read Git Integration section from WIP_TASK.md
- If no branch or "No dedicated branch": Continue to standard completion

**Check for Multiple WIP Tasks on Same Branch:**
- Scan other active WIP tasks for same branch
- If multiple tasks share the branch:
  ```
  ⚠️ Multiple WIP Tasks - Manual Management Required
  
  Multiple WIP tasks detected on branch [branch_name]:
  - [task_1_name]
  - [task_2_name]  
  - [current_task_name] (completing)
  
  📋 Impact on Completion Process:
  • Cannot provide automated Git merge assistance
  • Cannot automatically archive in parent branch
  • YOU must manually manage Git operations
  • YOU must ensure task archival reaches parent branch
  
  🔧 Your Manual Responsibilities:
  1. Merge/integrate your changes to parent branch when ready
  2. Archive completed WIP task files in parent branch
  3. Manage branch cleanup as appropriate
  
  💡 Recommendation: Avoid multiple WIP tasks per branch in future.
     One task per branch significantly reduces manual overhead and complexity.
  ```
  Continue to standard completion without Git assistance.

**Offer Merge Assistance (if single task on branch):**
```
🔀 Git Branch Merge Assistance

Your WIP task is on dedicated branch: [branch_name]
Parent branch: [parent_branch_name]

Would you like assistance merging this branch back to [parent_branch_name]?

1️⃣ Yes, help me merge the branch
2️⃣ No, I'll handle Git operations manually

Choose option [1/2]:
```

**Manual Git Management Warning (if option 2 selected):**
```
⚠️ Manual Git Management - Your Responsibility

You chose to handle Git operations manually. This means:

📋 Your Responsibilities:
• Merge your feature branch [feature_branch_name] to parent branch when ready  
• Ensure WIP task archival is committed to parent branch [parent_branch_name]
• The archived task files must be accessible from the parent branch
• Manage branch cleanup as appropriate

⚠️ Critical Reminder: 
The WIP task will be archived on current branch [current_branch_name].
If you delete this branch before merging to parent, the archived task data 
may be lost from the main project history.

🔧 Recommended Next Steps:
1. Complete this task workflow (archival happens on current branch)
2. Manually merge [feature_branch_name] to [parent_branch_name]  
3. Verify archived task files are accessible from parent branch
4. Clean up feature branch only after confirming parent branch has the data

Continuing with standard completion process...
```

**Present Merge Strategies (if assistance requested):**
```
🔀 Git Merge Strategy Selection

Choose your merge strategy:

1️⃣ Fast-Forward Merge (if possible)
   ✅ Clean, linear history
   ✅ Simple and straightforward
   ❌ Only works if no other commits on parent branch
   ❌ Loses branch context in history

2️⃣ Three-Way Merge
   ✅ Preserves complete branch history
   ✅ Shows feature development context
   ❌ Creates merge commit
   ❌ More complex history graph

3️⃣ Squash and Merge
   ✅ Clean single commit for entire feature
   ✅ Simplified parent branch history
   ❌ Loses individual commit history
   ❌ Makes it harder to track specific changes

4️⃣ Rebase and Merge
   ✅ Clean linear history with individual commits
   ✅ Preserves commit granularity
   ❌ Rewrites commit history (timestamps change)
   ❌ More complex operation

Choose strategy [1-4]:
```

**Execute Merge Operation:**
- Switch to parent branch: `git checkout [parent_branch_name]`
- Execute selected merge strategy:
  - Option 1: `git merge [branch_name]` (fast-forward if possible)
  - Option 2: `git merge --no-ff [branch_name]` (force merge commit)
  - Option 3: `git merge --squash [branch_name]` then `git commit`
  - Option 4: `git rebase [branch_name]` then `git merge [branch_name]`
- Handle any merge conflicts with user guidance

**Update WIP Task Status (BEFORE archival):**
```
### 📝 Update WIP Task Status

Updating WIP_TASK.md Git Integration section:
- Branch Status: Active → Completed
- Completion Timestamp: [current_timestamp]
- Final Status: Task completed and ready for archival

Committing status update to feature branch before archival...
```

Execute:
- `git checkout [branch_name]` (switch back to feature branch temporarily)
- Update WIP_TASK.md Git Integration section
- `git add .knowledge/work-in-progress/[task_name]/WIP_TASK.md`
- `git commit -m "feat: Mark WIP task '[task_name]' as completed"`

**Parent Branch Switch for Archival:**
```
### 🔄 Parent Branch Archival Process

Switching to parent branch for task archival:
• Current branch: [feature_branch_name] 
• Parent branch: [parent_branch_name]
• Switching: git checkout [parent_branch_name]

✅ Now on parent branch: [parent_branch_name]

Proceeding with WIP task archival in parent branch context...
This ensures the completed task is preserved in the main branch history.
```

**Offer Branch Deletion:**
```
🗑️ Branch Cleanup

Branch [branch_name] has been successfully merged to [parent_branch_name].
WIP task has been archived in parent branch context.

Would you like to delete the feature branch [branch_name]?

1️⃣ Yes, delete the branch (keeps history clean)
2️⃣ No, keep the branch (for reference or future work)

Choose option [1/2]:
```

If user chooses deletion: `git branch -d [branch_name]`

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
- **No Active Task**: If no active task exists, inform user and suggest task switching or creation
- **Missing Task Files**: If task files are missing or corrupted, offer to complete with available information
- **Git Operation Failures**: If merge fails, provide manual resolution guidance and continue with standard completion
- **Branch Deletion Failures**: If branch deletion fails, warn user but continue with completion
- **Parent Branch Switch Failures**: If switching to parent branch fails, provide detailed error explanation and user options
- **Archival Failures**: If archival fails, preserve task in current location and provide detailed error explanation
- **Knowledge Extraction Failures**: If knowledge extraction fails, complete archival but warn about lost learnings
- **Partial Failures**: Provide rollback options if completion process fails partway through
- **Merge Conflicts**: Guide user through conflict resolution process before completing task

### Parent Branch Switch Failure Handling
If parent branch switch fails during archival process:
```
❌ Parent Branch Switch Failed

Attempted to switch from [feature_branch] to [parent_branch] but failed.

🔍 Possible Causes:
• Parent branch doesn't exist locally
• Uncommitted changes preventing switch  
• Git repository in unexpected state
• Network issues if parent branch needs fetching

🔧 Your Options:
1. Fix the Git issue manually and restart completion workflow
2. Complete archival on current branch (feature branch)
3. Cancel completion workflow to investigate

📋 Detailed Error Information:
[Git error message]
[Current Git status]

Please resolve the Git issue and choose how to proceed:
1️⃣ I fixed it, retry parent branch switch
2️⃣ Archive on current branch instead  
3️⃣ Cancel completion workflow

Choose option [1-3]:
```

## Post-Completion Options
After successful completion, offer user:
- Create new WIP task for next objective
- Switch to existing WIP task
- Review archived tasks for reference
- Update project documentation based on learnings

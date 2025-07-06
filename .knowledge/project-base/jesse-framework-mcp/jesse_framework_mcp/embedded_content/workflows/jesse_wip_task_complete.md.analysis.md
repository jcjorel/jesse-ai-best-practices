<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/embedded_content/workflows/jesse_wip_task_complete.md -->
<!-- Cached On: 2025-07-06T12:09:42.895281 -->
<!-- Source Modified: 2025-06-26T12:53:41.415393 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This workflow documentation provides a comprehensive WIP task completion system for the Jesse Framework, designed to finalize work-in-progress tasks with integrated Git branch management, knowledge extraction to persistent storage, and proper task archival with lifecycle tracking. The system delivers active task verification with Essential Knowledge Base validation, sophisticated Git branch assessment including merge assistance with multiple strategy options (`Fast-Forward`, `Three-Way`, `Squash and Merge`, `Rebase and Merge`), and comprehensive knowledge extraction following intemporal writing standards. Key semantic entities include `WIP_TASK.md` Git Integration section processing, `.knowledge/work-in-progress/_archived/` timestamped archival directory structure, `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md` knowledge persistence, `.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md` Essential Knowledge Base updates, Git command integration with `git checkout`, `git merge`, `git branch -d` operations, multiple WIP task detection and manual management warnings, parent branch switching for archival context, intemporal writing conversion from past to present tense, and comprehensive error handling with rollback capabilities ensuring consistent task lifecycle management and knowledge preservation across the Jesse Framework ecosystem.

##### Main Components

The workflow contains seven primary execution steps with comprehensive Git integration and knowledge management capabilities. Core components include Verify Active Task confirming task existence and displaying summary, Git Branch Assessment and Merge Assistance providing automated merge workflows with strategy selection, Extract Task Learnings processing reusable knowledge from task files, Update Persistent Knowledge Base appending extracted insights to permanent storage, Generate Task Completion Summary creating comprehensive completion documentation, Archive Task moving completed work to timestamped archived locations, and Update Essential Knowledge Base clearing active task status. The system incorporates specialized components including multiple WIP task detection with manual management warnings, merge conflict resolution guidance, parent branch switching for proper archival context, and comprehensive error handling with detailed failure recovery procedures.

###### Architecture & Design

The architecture implements a state-driven completion workflow with comprehensive Git integration and knowledge preservation mechanisms ensuring proper task lifecycle management. The design employs conditional Git assistance based on branch configuration and multi-task detection, providing automated merge workflows for single-task branches while requiring manual management for complex scenarios. The system uses structured knowledge extraction patterns converting task-specific learnings into reusable persistent knowledge following intemporal writing standards. The architectural pattern includes comprehensive error handling with rollback capabilities, parent branch context switching for proper archival, and multi-stage validation ensuring consistent completion across different Git repository states and task configurations.

####### Implementation Approach

The implementation uses Git command-line integration for branch assessment, merge operations, and repository state management, employing conditional logic to handle single-task versus multi-task branch scenarios. The approach employs structured knowledge extraction algorithms processing WIP task files to identify reusable patterns, solutions, and insights for persistent storage. Task archival uses timestamped directory creation in `.knowledge/work-in-progress/_archived/` with complete file preservation and metadata enhancement. The system implements intemporal writing conversion transforming historical task learnings into present-tense factual statements for knowledge base integration. Git merge assistance provides four distinct strategies with user selection and automated execution including conflict resolution guidance and branch cleanup options.

######## External Dependencies & Integration Points

**→ References:**
- `git` (external tool) - Git version control system for branch management, merge operations, and repository state assessment
- `.knowledge/work-in-progress/_archived/` - timestamped archival directory structure for completed task preservation
- `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md` - persistent knowledge repository for extracted learnings and patterns
- `.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md` - Essential Knowledge Base requiring active task status updates
- `WIP_TASK.md` - task definition files containing Git Integration sections and completion metadata
- `PROGRESS.md` - task progress tracking files requiring archival with completion timestamps
- Git branch naming conventions - standardized patterns for feature branch identification and parent branch relationships

**← Referenced By:**
- Jesse Framework knowledge management system - processes consuming completed task information and extracted learnings
- Git workflow management tools - systems requiring standardized merge strategies and branch cleanup procedures
- Task creation workflows - procedures referencing completion patterns for lifecycle management
- Project documentation systems - tools aggregating completed task insights for project knowledge
- Development team coordination processes - workflows requiring task completion awareness and knowledge sharing

**⚡ System role and ecosystem integration:**
- **System Role**: Critical task lifecycle completion component within the Jesse Framework ecosystem, providing comprehensive WIP task finalization with integrated Git workflow management and knowledge preservation
- **Ecosystem Position**: Core infrastructure component that completes the task management lifecycle, serving as the bridge between active development work and persistent project knowledge
- **Integration Pattern**: Used by development teams through direct workflow invocation, integrated with Git repositories for version control coordination, synchronized with knowledge management systems for learning preservation, and coordinated with archival systems for historical task reference and project continuity

######### Edge Cases & Error Handling

The workflow handles scenarios where no active task exists by providing user guidance and suggesting task switching or creation alternatives. Multiple WIP tasks on the same branch trigger manual management warnings with detailed responsibility explanations and complexity reduction recommendations. Git operation failures including merge conflicts, branch switching errors, and parent branch access issues provide comprehensive resolution guidance with fallback options. Parent branch switch failures during archival trigger detailed error analysis with user choice options for resolution or alternative archival approaches. Knowledge extraction failures preserve task archival while warning about lost learning opportunities. The system addresses partial completion failures with rollback options and state restoration capabilities ensuring consistent project state regardless of failure points.

########## Internal Implementation Details

The workflow uses Git command execution for repository state assessment including branch detection, merge conflict identification, and parent branch validation. Knowledge extraction employs pattern matching algorithms identifying reusable insights from task files and converting historical learnings to intemporal present-tense statements. Task archival implements atomic file system operations with timestamped directory creation and complete metadata preservation including completion summaries and learning extractions. Git merge assistance uses conditional strategy execution with user-selected approaches including fast-forward detection, three-way merge commit creation, squash commit generation, and rebase operations. Error handling implements comprehensive state validation with detailed error message generation and user guidance for manual resolution procedures.

########### Code Usage Examples

This example demonstrates the Git branch assessment and merge assistance workflow providing automated merge strategies:

```bash
# Git branch assessment and merge strategy execution
git checkout [parent_branch_name]
git merge --no-ff [branch_name]
# Provides automated merge assistance with strategy selection and conflict resolution
```

This example shows the parent branch switching procedure ensuring proper archival context:

```bash
# Parent branch context switching for proper task archival
git checkout [feature_branch_name]
git add .knowledge/work-in-progress/[task_name]/WIP_TASK.md
git commit -m "feat: Mark WIP task '[task_name]' as completed"
git checkout [parent_branch_name]
# Ensures task completion is recorded and archived in proper branch context
```

This example illustrates the comprehensive error handling for parent branch switch failures:

```text
# Parent branch switch failure handling with user options
❌ Parent Branch Switch Failed
Attempted to switch from [feature_branch] to [parent_branch] but failed.
🔧 Your Options:
1. Fix the Git issue manually and restart completion workflow
2. Complete archival on current branch (feature branch)
3. Cancel completion workflow to investigate
# Provides detailed error context and recovery options for Git operation failures
```
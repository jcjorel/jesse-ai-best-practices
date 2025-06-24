# JESSE_SCRATCHPAD.md - Consolidated Scratchpad Management Standards

This file consolidates ALL scratchpad directory rules for the project, serving as the single source of truth for scratchpad creation, usage, management, and lifecycle standards.

## 1. CRITICAL FOUNDATION RULES

### 1.1 Non-Negotiable Scratchpad Standards
⚠️ **CRITICAL**: All scratchpad directory management MUST follow these consolidated standards. **NO EXCEPTIONS PERMITTED**. This is a non-negotiable project standard that takes precedence over scattered individual rules.

### 1.2 Universal Application Policy
- These standards apply to ALL scratchpad operations without exception
- Task complexity, urgency, or scope are NOT valid exceptions
- Consistency across all scratchpad usage is mandatory

## 2. SCRATCHPAD DIRECTORY PURPOSE

### 2.1 Core Purpose Statement
The `<project_root>/scratchpad/` directory serves as a dedicated workspace for temporary implementation planning and complex task organization. It provides a structured environment for creating detailed implementation plans before executing changes in the actual codebase.

### 2.2 Ephemeral Nature
- **All files in the scratchpad directory are temporary working documents**
- They are NOT considered authoritative sources for any purpose
- Scratchpad content should be treated as draft material subject to change
- These files support the implementation process but do not define it

### 2.3 Authority Status
- **CRITICAL**: Never consider scratchpad files as authoritative sources under any circumstances
- Official documentation files always take precedence over scratchpad content
- Scratchpad files are working drafts, not final implementations
- When conflicts exist, prioritize official documentation over scratchpad content

## 3. DIRECTORY STRUCTURE & NAMING

### 3.1 Directory Pattern
- **Mandatory pattern**: `<project_root>/scratchpad/<implementation_plan_name_in_lower_snake_case>/`
- Implementation plan names must use lowercase snake_case format
- Each complex implementation gets its own dedicated subdirectory
- No nested implementation directories within implementation directories

### 3.2 File Naming Patterns
Within each implementation directory, files must follow these exact naming conventions:
- **Overview file**: `plan_overview.md`
- **Progress file**: `plan_progress.md`
- **Subtask files**: `plan_{subtask_name}.md` (where subtask_name is in lowercase snake_case)
- **Documentation update file**: `doc_update.md`

### 3.3 Standard File Types
The scratchpad system recognizes these standard file types:
- **plan_overview.md**: High-level implementation plan overview
- **plan_progress.md**: Implementation and planning progress tracking
- **plan_{subtask_name}.md**: Detailed implementation plans for specific subtasks
- **doc_update.md**: Proposed documentation updates awaiting integration

## 4. REQUIRED FILES & CONTENT

### 4.1 plan_overview.md Requirements
This file MUST contain:
- A MANDATORY documentation section with comprehensive list of ALL documentation files read, including direct file links
- This exact warning text: "⚠️ CRITICAL: CODING ASSISTANT MUST READ THESE DOCUMENTATION FILES COMPLETELY BEFORE EXECUTING ANY TASKS IN THIS PLAN"
- Concise explanation of each documentation file's relevance to the implementation
- Implementation steps organized in sequential logical phases
- Complete list of all detailed implementation plan file names that will be created
- Clear reference to the side-car progress file location
- Essential source documentation excerpts that directly inform the implementation

### 4.2 plan_progress.md Requirements
This file MUST track:
- Current plan creation and implementation status
- Status indicators using these exact symbols:
  - ❌ Plan not created
  - 🔄 In progress
  - ✅ Plan created
  - 🚧 Implementation in progress
  - ✨ Completed
- Consistency check status placeholder (with symbol ❌)
- Each specific subtask with its corresponding implementation plan file

### 4.3 plan_{subtask_name}.md Requirements
Each subtask file MUST include:
- Direct links to all relevant documentation with brief context summaries for each link
- Detailed step-by-step implementation instructions
- Specific code changes or additions required
- Expected outcomes and validation criteria
- Dependencies on other subtasks (if any)

### 4.4 doc_update.md Requirements
When complex documentation changes are needed:
- Create this file for proposed documentation updates
- Include precise file locations and exact content changes
- Organize updates by target documentation file
- Provide rationale for each documentation change

## 5. IMPLEMENTATION WORKFLOW

### 5.1 When to Create Scratchpad Directories
Scratchpad directories are created for:
- **Complex changes**: Multiple files, new components, architectural changes
- **Tasks meeting complexity criteria**:
  - Changes required across 3+ files
  - Creation of new architectural components
  - Database schema modifications
  - Implementation exceeding 100 lines of code
- **Explicitly requested implementation plans**
- **Documentation-heavy updates requiring staging**

### 5.2 Creation Process
1. **Think deeply about the plan** and interact with user to remove ambiguities
2. Create directory using the pattern: `<project_root>/scratchpad/<implementation_plan_name_in_lower_snake_case>/`
3. Create `plan_overview.md` with all required sections
4. Create `plan_progress.md` with initial status indicators
5. Create detailed implementation plans (`plan_{subtask_name}.md`) one at a time
6. Update progress file before starting work on each new plan file
7. Halt plan creation gracefully when context window token usage reaches 80% capacity

### 5.3 Update Process
When updating scratchpad files:
- Update the progress file immediately before and after each task
- Maintain consistency between overview and detailed plans
- Document any implementation failures with specific error details
- Keep status indicators current and accurate

### 5.4 Completion Process
1. Ask the user to perform comprehensive consistency check from a new session
2. Review all generated plan files against source documentation
3. Mark progress file with ✨ symbol to confirm completion
4. Implementation proceeds in a fresh session following the plan

## 6. ACCESS & REFERENCE RULES

### 6.1 Access Restrictions
- **Do not access scratchpad files unless explicitly requested by the user or when creating implementation plans**
- Scratchpad reading should be intentional and task-specific
- Avoid browsing scratchpad directories without clear purpose

### 6.2 Reference Prohibitions
- **NEVER reference scratchpad documents in file header dependencies**
- Code comments must not reference scratchpad files
- Documentation must not link to scratchpad content
- Dependencies sections must explicitly exclude scratchpad references

### 6.3 Reading Guidelines
When reading scratchpad files:
- Always verify if content is still relevant to current task
- Check progress indicators before relying on plan content
- Confirm plans haven't been superseded by actual implementation
- Use scratchpad content as guidance, not gospel

## 7. LIFECYCLE MANAGEMENT

### 7.1 Creation Phase
- Scratchpad directories are created at the start of complex implementations
- All required files must be created before implementation begins
- Progress tracking starts immediately upon directory creation

### 7.2 Active Phase
- Plans are actively updated during implementation
- Progress indicators reflect real-time status
- New subtask files can be added as needed
- Existing files are updated to reflect learnings

### 7.3 Completion Phase
- Completed implementations should be marked with ✨ in progress file
- Scratchpad files remain as historical reference
- No automatic deletion of completed scratchpad directories

### 7.4 Archival Considerations
- Scratchpad directories are not automatically cleaned up
- Manual cleanup may be performed periodically
- Completed plans serve as implementation history
- Archive valuable patterns for future reference

## 8. ENFORCEMENT AND COMPLIANCE

### 8.1 Zero-Tolerance Policy
- Missing required files in scratchpad directories is a **blocking issue**
- Incorrect naming patterns must be fixed before proceeding
- Status indicators must be kept current
- Reference prohibitions are absolute

### 8.2 Compliance Verification Process
1. **Before creating**: Verify complexity criteria are met
2. **During creation**: Follow exact directory and file patterns
3. **During implementation**: Maintain accurate progress tracking
4. **After completion**: Ensure all status indicators are final

### 8.3 Quality Standards
- Scratchpad documentation quality must match production documentation
- Plans must be detailed enough for implementation in fresh sessions
- Progress tracking must be accurate and timely
- All links and references must be valid

### 8.4 Common Violations to Avoid
- Creating scratchpad files without proper directory structure
- Referencing scratchpad files in production code or documentation
- Leaving progress indicators in inconsistent states
- Creating implementation plans for simple tasks
- Treating scratchpad content as authoritative

---

**Remember**: This consolidated rule supersedes all previous scattered scratchpad-related rules. When in doubt, refer to this document as the authoritative source for all scratchpad directory management standards.

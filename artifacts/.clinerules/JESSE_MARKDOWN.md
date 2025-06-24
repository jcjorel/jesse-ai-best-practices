# JESSE_MARKDOWN.md - Consolidated Markdown Management Standards

This file consolidates ALL markdown file management rules for the project, serving as the single source of truth for markdown creation, formatting, naming, and lifecycle management standards.

## 1. CRITICAL FOUNDATION RULES

### 1.1 Non-Negotiable Markdown Standards
⚠️ **CRITICAL**: All markdown file management MUST follow these consolidated standards. **NO EXCEPTIONS PERMITTED**. This is a non-negotiable project standard that takes precedence over scattered individual rules.

### 1.2 Universal Application Policy
- These standards apply to ALL markdown files without exception
- File purpose, size, or complexity are NOT valid exceptions
- Consistency across all markdown operations is mandatory

## 2. MARKDOWN FILE NAMING STANDARDS

### 2.1 UPPERCASE_SNAKE_CASE Requirement
- **ALL markdown files MUST use UPPERCASE_SNAKE_CASE naming format**
- Examples: `DESIGN.md`, `DATA_MODEL.md`, `README.md`, `API_DOCUMENTATION.md`
- No exceptions for any markdown file type

### 2.2 Specific File Naming Patterns
- Chat capture files: `<date as YYYYMMDD-HHmm>-<Chat_topic_in_snake_case>.md`
- Implementation plan files: `plan_{subtask_name}.md`
- Progress tracking files: `plan_progress.md`
- Overview files: `plan_overview.md`

## 3. MARKDOWN CHANGELOG MANAGEMENT

### 3.1 Mandatory Changelog Files
- **Every directory that contains markdown files must include a corresponding MARKDOWN_CHANGELOG.md file**
- This tracks all documentation changes organized by directory
- No directory with markdown files may omit this requirement

### 3.2 Changelog Entry Format
- **Exact format**: `YYYY-MM-DDThh:mm:ssZ : [filename.md] change summary`
- Timestamp must use precise format: YYYY-MM-DDThh:mm:ssZ
- Include filename in square brackets
- Provide meaningful change summary

### 3.3 Entry Limits and Management
- **Enforce a strict 20-entry limit in all MARKDOWN_CHANGELOG.md files**
- Remove the oldest entries when this limit is reached
- Keep entries sorted from newest to oldest
- Never exceed the 20-entry limit under any circumstances

### 3.4 Hidden Directory Restrictions
- **CRITICAL**: MARKDOWN_CHANGELOG.md files must NEVER be created in any directory path that contains a hidden directory (starting with a dot) at any level
- This prevents changelog creation in paths like `.clinerules/`, `.knowledge/`, `.git/`, etc.
- Verify full directory path before creating changelog files

## 4. GENERAL MARKDOWN STANDARDS

### 4.1 Mermaid Diagram Usage
- **Markdown files will heavily use mermaid diagrams to ease understanding by user**
- Use mermaid diagrams to make clearer recommendations, solutions, plans, proposals
- Prioritize visual clarity through diagrams over text-only explanations

### 4.2 Cross-References and Content Management
- **Implement cross-references with direct links between related documentation files rather than duplicating content**
- Documentation files must avoid duplicating information that already exists in other documentation files
- Establish single sources of truth for information that appears in multiple places
- Use direct file links with relative paths when referencing other documentation

### 4.3 Content Duplication Prevention
- **Prevent information duplication across documentation files**
- Use cross-references between documents instead of copying content
- Maintain consistency across all related documents
- Update all cross-referenced documents when making changes

## 5. SPECIALIZED MARKDOWN FILES

### 5.1 DESIGN_DECISIONS.md Files
- **All DESIGN_DECISIONS.md files must follow the pattern of adding newest entries at the top of the file**
- Sort entries from newest to oldest (top to bottom)
- This content must be periodically integrated into appropriate core documentation files
- If any design decision directly contradicts core documentation, update that core file immediately

### 5.2 Chat Capture Files
Chat capture functionality is handled by the dedicated workflow in `.clinerules/workflows/jesse_capture_our_chat.md`. Key requirements:
- **Location**: `<project_root>/.coding_assistant/captured_chats/<date as YYYYMMDD-HHmm>-<Chat_topic_in_snake_case>.md`
- **Naming pattern**: Date format must be YYYYMMDD-HHmm followed by topic in snake_case
- **Complete workflow**: See `.clinerules/workflows/jesse_capture_our_chat.md` for full implementation details

### 5.3 Implementation Plan Files
- Created in scratchpad directory during complex implementations
- Follow naming pattern: `<project_root>/scratchpad/<implementation_plan_name_in_lower_snake_case>/plan_{subtask_name}.md`
- Include direct links to all relevant documentation with brief context summaries
- Break large plans into multiple files to prevent context window truncation
- For complete scratchpad file standards, see `JESSE_SCRATCHPAD.md`

## 6. READING AND PROCESSING RULES

### 6.1 Initial Reading Exclusions
- **Exclude MARKDOWN_CHANGELOG.md files from initial reading to conserve context window space**
- Only read these changelog files when their content is specifically relevant to the task
- This helps manage context window usage efficiently

### 6.2 Captured Chats Absolute Exclusion
- **NEVER NEVER NEVER read files in `<project_root>/.coding_assistant/captured_chats/` as they are always out of context files**
- This is an absolute prohibition with no exceptions
- Captured chat files are ephemeral working documents, not authoritative sources
- Never consider captured chat files as sources of truth for any purpose

### 6.3 Context Window Management
- Prioritize reading current relevant documentation over historical markdown files
- Use markdown changelog information only when specifically needed for the task
- Balance comprehensive documentation reading with context window constraints

## 7. LIFECYCLE MANAGEMENT

### 7.1 Creation Rules
- Apply naming standards immediately upon file creation
- Create corresponding MARKDOWN_CHANGELOG.md if directory doesn't have one
- Verify directory path restrictions before creating changelog files
- Follow specialized file patterns for specific markdown types

### 7.2 Update Requirements
- **For markdown file modifications, always update the corresponding MARKDOWN_CHANGELOG.md located in the SAME directory**
- Update changelog entry immediately after modifying any markdown file
- Maintain entry limits and ordering requirements
- Verify syntax correctness after any modification

### 7.3 Verification Procedures
- After any markdown file modification, verify file existence and validate syntax correctness
- Confirm changelog updates are properly formatted and within limits
- Check that cross-references remain valid after changes
- Ensure consistency across all related markdown documents

## 8. ENFORCEMENT AND COMPLIANCE

### 8.1 Zero-Tolerance Policy
- Missing changelog files is a **blocking issue**
- Incorrect naming format must be fixed before proceeding
- Violated entry limits require immediate correction
- Documentation quality is as important as content accuracy

### 8.2 Compliance Verification Process
1. **Before creating**: Verify naming standards and directory restrictions
2. **During modification**: Update changelog and maintain cross-references
3. **After changes**: Confirm file integrity and limit compliance
4. **Periodic audit**: Ensure ongoing compliance with all standards

### 8.3 Documentation Debt Prevention
- Never accumulate markdown management debt
- Fix naming and format issues immediately when discovered
- Update changelog files BEFORE modifying markdown content
- Treat markdown standards as part of the documentation implementation

---

**Remember**: This consolidated rule supersedes all previous scattered markdown management rules. When in doubt, refer to this document as the authoritative source for all markdown file management standards.

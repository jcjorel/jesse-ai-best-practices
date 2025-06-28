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

## 3. GENERAL MARKDOWN STANDARDS

### 3.1 Mermaid Diagram Usage
- **Markdown files will heavily use mermaid diagrams to ease understanding by user**
- Use mermaid diagrams to make clearer recommendations, solutions, plans, proposals
- Prioritize visual clarity through diagrams over text-only explanations

### 3.2 Cross-References and Content Management
- **Implement cross-references with direct links between related documentation files rather than duplicating content**
- Documentation files must avoid duplicating information that already exists in other documentation files
- Establish single sources of truth for information that appears in multiple places
- Use direct file links with relative paths when referencing other documentation

### 3.3 Content Duplication Prevention
- **Prevent information duplication across documentation files**
- Use cross-references between documents instead of copying content
- Maintain consistency across all related documents
- Update all cross-referenced documents when making changes

## 4. SPECIALIZED MARKDOWN FILES

### 4.1 DESIGN_DECISIONS.md Files
- **All DESIGN_DECISIONS.md files must follow the pattern of adding newest entries at the top of the file**
- Sort entries from newest to oldest (top to bottom)
- This content must be periodically integrated into appropriate core documentation files
- If any design decision directly contradicts core documentation, update that core file immediately

### 4.2 Chat Capture Files
Chat capture functionality is handled by the dedicated workflow in `.clinerules/workflows/jesse_capture_our_chat.md`. Key requirements:
- **Location**: `<project_root>/.coding_assistant/captured_chats/<date as YYYYMMDD-HHmm>-<Chat_topic_in_snake_case>.md`
- **Naming pattern**: Date format must be YYYYMMDD-HHmm followed by topic in snake_case
- **Complete workflow**: See `.clinerules/workflows/jesse_capture_our_chat.md` for full implementation details

### 4.3 Implementation Plan Files
- Created in scratchpad directory during complex implementations
- Follow naming pattern: `<project_root>/scratchpad/<implementation_plan_name_in_lower_snake_case>/plan_{subtask_name}.md`
- Include direct links to all relevant documentation with brief context summaries
- Break large plans into multiple files to prevent context window truncation
- For complete scratchpad file standards, see `JESSE_SCRATCHPAD.md`

## 5. READING AND PROCESSING RULES

### 5.1 Captured Chats Absolute Exclusion
- **NEVER NEVER NEVER read files in `<project_root>/.coding_assistant/captured_chats/` as they are always out of context files**
- This is an absolute prohibition with no exceptions
- Captured chat files are ephemeral working documents, not authoritative sources
- Never consider captured chat files as sources of truth for any purpose

### 5.2 Context Window Management
- Prioritize reading current relevant documentation over historical markdown files
- Balance comprehensive documentation reading with context window constraints

## 6. LIFECYCLE MANAGEMENT

### 6.1 Creation Rules
- Apply naming standards immediately upon file creation
- Follow specialized file patterns for specific markdown types

### 6.2 Verification Procedures
- After any markdown file modification, verify file existence and validate syntax correctness
- Check that cross-references remain valid after changes
- Ensure consistency across all related markdown documents

## 7. ENFORCEMENT AND COMPLIANCE

### 7.1 Zero-Tolerance Policy
- Incorrect naming format must be fixed before proceeding
- Documentation quality is as important as content accuracy

### 7.2 Compliance Verification Process
1. **Before creating**: Verify naming standards
2. **During modification**: Maintain cross-references
3. **After changes**: Confirm file integrity
4. **Periodic audit**: Ensure ongoing compliance with all standards

### 7.3 Documentation Debt Prevention
- Never accumulate markdown management debt
- Fix naming and format issues immediately when discovered
- Treat markdown standards as part of the documentation implementation

---

**Remember**: This consolidated rule supersedes all previous scattered markdown management rules. When in doubt, refer to this document as the authoritative source for all markdown file management standards.

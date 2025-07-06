<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/embedded_content/JESSE_MARKDOWN.md -->
<!-- Cached On: 2025-07-06T12:12:24.709483 -->
<!-- Source Modified: 2025-06-25T07:59:10.782599 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file serves as the consolidated markdown management standards document for the Jesse Framework MCP project, establishing unified rules for markdown file creation, formatting, naming conventions, and lifecycle management across all project documentation. The system provides comprehensive governance for markdown operations through mandatory `UPPERCASE_SNAKE_CASE` naming requirements, specialized file patterns for different document types, and strict compliance enforcement mechanisms. Key semantic entities include `UPPERCASE_SNAKE_CASE` naming format requirement, `mermaid` diagram integration for visual clarity, `DESIGN_DECISIONS.md` chronological ordering patterns, `.coding_assistant/captured_chats/` directory exclusion rules, `YYYYMMDD-HHmm` timestamp formatting for chat captures, `plan_{subtask_name}.md` implementation file patterns, `cross-references` with direct file linking requirements, `zero-tolerance policy` enforcement mechanisms, and `single source of truth` principle implementation preventing content duplication across documentation files. The document establishes authoritative standards superseding all previous scattered markdown rules while ensuring consistency, maintainability, and quality across the entire project documentation ecosystem.

##### Main Components

The document contains seven primary sections establishing comprehensive markdown governance: Critical Foundation Rules defining non-negotiable standards and universal application policies, Markdown File Naming Standards specifying `UPPERCASE_SNAKE_CASE` requirements and specialized naming patterns, General Markdown Standards covering `mermaid` diagram usage and cross-reference management, Specialized Markdown Files detailing requirements for `DESIGN_DECISIONS.md`, chat capture files, and implementation plan files, Reading and Processing Rules establishing absolute exclusions for captured chat files and context window management, Lifecycle Management covering creation rules and verification procedures, and Enforcement and Compliance defining zero-tolerance policies and compliance verification processes. Each section provides specific requirements, examples, and implementation guidance ensuring consistent application across all project markdown operations.

###### Architecture & Design

The architecture implements a hierarchical governance model with consolidated standards superseding scattered individual rules, establishing clear authority and precedence for markdown management decisions. The design employs mandatory compliance patterns with zero-tolerance enforcement, specialized file type handling through dedicated naming conventions and processing rules, and cross-reference management preventing content duplication while maintaining information consistency. The system uses exclusion-based processing rules for ephemeral documents, chronological organization patterns for design decisions, and verification procedures ensuring ongoing compliance. The architectural pattern includes single source of truth principles, direct file linking mechanisms, and lifecycle management protocols covering creation, modification, and maintenance phases.

####### Implementation Approach

The implementation uses strict naming convention enforcement through `UPPERCASE_SNAKE_CASE` requirements applied universally across all markdown files, specialized pattern matching for different file types including chat captures with `YYYYMMDD-HHmm` formatting and implementation plans with `plan_{subtask_name}.md` structures. The approach employs content duplication prevention through mandatory cross-reference usage, direct file linking with relative paths, and single source maintenance protocols. File processing implements absolute exclusion rules for `.coding_assistant/captured_chats/` directory contents, chronological ordering for `DESIGN_DECISIONS.md` files with newest entries at top, and comprehensive verification procedures after modifications. Quality assurance uses zero-tolerance compliance checking, immediate correction requirements, and periodic audit processes ensuring ongoing standards adherence.

######## External Dependencies & Integration Points

**→ References:**
- `.clinerules/workflows/jesse_capture_our_chat.md` - dedicated workflow handling chat capture functionality and file management
- `JESSE_SCRATCHPAD.md` - scratchpad file standards for implementation plan requirements and directory organization
- `<project_root>/.coding_assistant/captured_chats/` - chat capture directory with absolute exclusion rules for processing
- `scratchpad/` directory - implementation plan file storage location with structured naming patterns
- `mermaid` diagram syntax - visual diagram integration requirements for enhanced documentation clarity

**← Referenced By:**
- All project markdown files - consume naming standards and formatting requirements for consistent implementation
- Documentation creation workflows - reference standards for file naming, structure, and content organization
- Quality assurance processes - enforce compliance verification and zero-tolerance policy implementation
- Cross-reference management systems - use direct linking requirements and content duplication prevention rules
- Lifecycle management procedures - apply creation, modification, and verification standards across documentation operations

**⚡ System role and ecosystem integration:**
- **System Role**: Authoritative governance document for all markdown operations within the Jesse Framework MCP project, establishing unified standards and superseding scattered individual rules
- **Ecosystem Position**: Central documentation infrastructure component providing mandatory standards for all markdown file creation, modification, and management across the entire project
- **Integration Pattern**: Referenced by all documentation workflows and quality processes, enforced through zero-tolerance compliance policies, and integrated with specialized file handling for different document types while maintaining cross-reference consistency and preventing content duplication

######### Edge Cases & Error Handling

The document addresses compliance violations through zero-tolerance enforcement requiring immediate correction before proceeding with any operations. Missing or incorrect naming formats trigger mandatory fixes with no exceptions permitted regardless of file purpose, size, or complexity. Cross-reference validation failures require immediate resolution to maintain link integrity across documentation. Content duplication scenarios mandate consolidation into single source of truth locations with proper cross-reference implementation. The system handles specialized file type exceptions through dedicated patterns while maintaining overall naming consistency. Verification procedure failures trigger comprehensive audit processes ensuring all related documents remain consistent and compliant with established standards.

########## Internal Implementation Details

The naming convention system uses `UPPERCASE_SNAKE_CASE` pattern matching with specific exceptions for timestamped files using `YYYYMMDD-HHmm` format and specialized implementation files with `plan_{subtask_name}.md` structure. Cross-reference management implements direct file linking with relative path resolution and content duplication detection algorithms. Compliance verification uses multi-stage checking including pre-creation validation, modification monitoring, post-change confirmation, and periodic audit cycles. File exclusion processing maintains absolute prohibition lists for `.coding_assistant/captured_chats/` directory contents with no exception handling. Quality assurance implements immediate correction requirements, documentation debt prevention mechanisms, and comprehensive standards enforcement across all markdown operations.

########### Code Usage Examples

This example demonstrates the mandatory naming convention requirements for all markdown files in the project:

```markdown
# Correct naming examples following UPPERCASE_SNAKE_CASE requirements
DESIGN.md
DATA_MODEL.md
API_DOCUMENTATION.md
README.md
```

This example shows the specialized naming pattern for chat capture files with timestamp and topic formatting:

```markdown
# Chat capture file naming pattern with date and topic structure
20240315-1430-authentication_implementation.md
20240316-0900-database_migration_planning.md
20240317-1600-api_endpoint_design.md
```

This example illustrates the implementation plan file structure with proper directory organization and naming:

```markdown
# Implementation plan file organization in scratchpad directory
scratchpad/authentication_system/plan_overview.md
scratchpad/authentication_system/plan_database_schema.md
scratchpad/authentication_system/plan_api_endpoints.md
scratchpad/authentication_system/plan_progress.md
```
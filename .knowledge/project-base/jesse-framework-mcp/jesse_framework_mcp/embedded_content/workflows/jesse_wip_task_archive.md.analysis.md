<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/embedded_content/workflows/jesse_wip_task_archive.md -->
<!-- Cached On: 2025-07-06T11:47:30.393831 -->
<!-- Source Modified: 2025-06-24T19:31:39.887820 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file defines the comprehensive `WIP Task Archive Workflow` for preserving incomplete Work-in-Progress tasks while removing them from active task management within the Jesse Framework ecosystem, providing structured archival with optional knowledge extraction and metadata preservation. The workflow delivers systematic task archival through nine execution steps including task selection, optional learning extraction, timestamped archive creation, and knowledge base updates. Key semantic entities include `.knowledge/work-in-progress/` directory structure with `_archived/` subdirectory organization, timestamped archive naming pattern `[task_name]_archived_[YYYYMMDD_HHMMSS]`, `ARCHIVE_INFO.md` metadata template with structured archive information, `WIP_TASK.md` and `PROGRESS.md` file preservation, `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md` integration for learning extraction, `.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md` active task management, `intemporal writing` format for extracted learnings, `ISO timestamp` formatting for archive dates, read-only archive access patterns, rollback options for failed operations, and post-archive workflow suggestions including task creation and switching capabilities. The system enables developers to maintain organized task management while preserving valuable work context and enabling future reference access to incomplete tasks.

##### Main Components

The workflow contains nine primary execution steps: available task listing from `.knowledge/work-in-progress/` with status and metadata display, user task selection with archival confirmation and warning presentation, optional valuable learning extraction with persistent knowledge integration, timestamped archive directory creation in `_archived/` location, complete task file transfer with verification and cleanup, archive metadata generation using `ARCHIVE_INFO.md` template, Essential Knowledge Base updates for active task management, knowledge reference cleanup for consistency maintenance, and archive confirmation display with next action suggestions. Supporting components include archive information template specification with structured metadata fields, workflow completion verification procedures, comprehensive error handling for operation failures, special case management for active tasks and incomplete files, post-archive option presentation, and archive access documentation ensuring read-only reference availability with restoration possibilities.

###### Architecture & Design

The architecture implements a preservation-focused archival pattern with structured metadata generation and optional knowledge extraction capabilities. The design uses timestamped directory organization for conflict prevention, complete file preservation with verification protocols, and optional learning extraction with persistent knowledge integration. The system employs structured metadata templates for archive documentation, active task management integration for session state updates, and comprehensive error handling with rollback capabilities. The workflow follows a preservation-first approach ensuring no data loss during archival operations while maintaining knowledge consistency through reference cleanup and cross-reference validation across multiple knowledge storage locations.

####### Implementation Approach

The implementation uses directory scanning algorithms for task discovery with metadata extraction from `WIP_TASK.md` and `PROGRESS.md` files, timestamped naming generation with conflict resolution for unique archive identification, and optional knowledge extraction using `intemporal writing` format conversion for persistent storage. The approach employs complete file transfer operations with verification protocols, structured metadata generation using template processing with dynamic content insertion, and active task management updates through Essential Knowledge Base modification. Archive operations implement atomic file movement with rollback capabilities, knowledge reference scanning with cleanup protocols, and comprehensive verification procedures ensuring successful archival completion before confirmation display.

######## External Dependencies & Integration Points

**→ References:**
- `.knowledge/work-in-progress/` directory - active task storage requiring scanning and archival source operations
- `.knowledge/work-in-progress/_archived/` directory - archive destination requiring timestamped directory creation
- `WIP_TASK.md` and `PROGRESS.md` files - task documentation requiring preservation and metadata extraction
- `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md` - persistent knowledge repository for optional learning extraction
- `.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md` - Essential Knowledge Base requiring active task management updates
- `ARCHIVE_INFO.md` template - structured metadata format for archive documentation generation

**← Referenced By:**
- Task management workflows - consume archival services for incomplete task preservation and organization
- Knowledge management workflows - reference archived tasks for historical context and learning extraction
- Development workflows - access archived task information for project continuity and reference purposes
- Session management workflows - use archive operations for active task state transitions and cleanup

**⚡ System role and ecosystem integration:**
- **System Role**: Core task lifecycle management workflow within the Jesse Framework knowledge management ecosystem, serving as the primary mechanism for preserving incomplete work while maintaining organized active task management
- **Ecosystem Position**: Central task management component bridging active work-in-progress operations with long-term knowledge preservation through structured archival and optional learning extraction
- **Integration Pattern**: Invoked by developers for task lifecycle management, consumes task storage directories and knowledge bases, produces archived task collections with metadata for future reference and potential restoration

######### Edge Cases & Error Handling

The workflow handles non-existent WIP tasks by informing users and suggesting task creation workflows for proper task management initialization. Corrupted or missing task files trigger graceful handling with cleanup options and reference validation for consistency maintenance. Archive operation failures preserve tasks in original locations with rollback capabilities and detailed error reporting for resolution guidance. Essential Knowledge Base update failures restore previous active task states with transaction-like error recovery. Incomplete task files with missing `PROGRESS.md` or `WIP_TASK.md` receive graceful handling with partial archival and metadata generation. Large tasks with multiple files and subdirectories implement comprehensive transfer verification with progress tracking and failure recovery mechanisms.

########## Internal Implementation Details

The task listing mechanism scans `.knowledge/work-in-progress/` directory excluding `_archived/` subdirectory with metadata extraction from task files and status determination. Archive directory naming uses timestamp generation with `YYYYMMDD_HHMMSS` format and conflict resolution algorithms for unique identification. Learning extraction implements content analysis with `intemporal writing` conversion and structured insertion into persistent knowledge storage. File transfer operations use atomic movement with verification protocols and rollback capabilities for operation integrity. Metadata generation employs template processing with dynamic content insertion including archive dates, reasons, progress summaries, and file inventories. Knowledge reference cleanup uses scanning algorithms with pattern matching and cross-reference validation across multiple knowledge storage locations for consistency maintenance.

########### Code Usage Examples

This example demonstrates task listing and selection for archival operations. The structured approach provides comprehensive task information enabling informed archival decisions with status and metadata display.

```bash
# List available WIP tasks for archival with metadata extraction
ls -la .knowledge/work-in-progress/ | grep -v _archived
# Display task status and last updated information for selection
```

This example shows timestamped archive directory creation with conflict resolution. The naming pattern ensures unique archive identification while preserving chronological organization for future reference.

```bash
# Create timestamped archive directory with conflict prevention
mkdir -p ".knowledge/work-in-progress/_archived/task_name_archived_$(date +%Y%m%d_%H%M%S)"
```

This example illustrates complete task file transfer with verification protocols. The atomic operation ensures data integrity during archival with comprehensive file preservation and cleanup verification.

```bash
# Move task directory to archive location with verification
mv ".knowledge/work-in-progress/task_name" ".knowledge/work-in-progress/_archived/task_name_archived_20240115_143000/"
# Verify all files transferred successfully
ls -la ".knowledge/work-in-progress/_archived/task_name_archived_20240115_143000/"
```

This example demonstrates the structured archive metadata template for comprehensive task preservation. The template ensures consistent documentation with detailed context preservation for future reference and potential restoration.

```markdown
# Archive Information: Authentication System Implementation

## Archive Details
**Archived Date**: 2024-01-15T14:30:00Z
**Archive Reason**: Superseded by new authentication approach
**Final Status**: 60% complete - core implementation finished
**Progress at Archive**: 60%

## Original Task Information
**Started**: 2024-01-10T09:00:00Z
**Target Completion**: 2024-01-20T17:00:00Z
**Priority**: High
**Objective**: Implement OAuth2 authentication system for API endpoints

## Archive Summary
**Key Achievements**: OAuth2 flow implementation, token validation middleware
**Remaining Work**: Integration testing, error handling, documentation
**Learnings Extracted**: Yes - OAuth2 patterns added to persistent knowledge

## Access Information
**Original Location**: `.knowledge/work-in-progress/auth_system_implementation/`
**Archive Location**: `.knowledge/work-in-progress/_archived/auth_system_implementation_archived_20240115_143000/`
**Files Preserved**: WIP_TASK.md, PROGRESS.md, oauth_implementation.py, test_cases.md
```
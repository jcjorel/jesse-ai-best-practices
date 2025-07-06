<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/embedded_content/JESSE_SCRATCHPAD.md -->
<!-- Cached On: 2025-07-06T12:16:00.392905 -->
<!-- Source Modified: 2025-06-24T19:31:39.895821 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file serves as the consolidated scratchpad management standards document for the Jesse Framework MCP project, establishing unified rules for temporary implementation planning workspace creation, usage, and lifecycle management across all complex development tasks. The system provides comprehensive governance for scratchpad operations through mandatory directory structure patterns, specialized file naming conventions, and strict compliance enforcement mechanisms for temporary working documents. Key semantic entities include `<project_root>/scratchpad/` directory structure requirement, `lower_snake_case` implementation plan naming format, `plan_overview.md` mandatory documentation section with comprehensive file links, `plan_progress.md` status tracking with specific symbols (`❌`, `🔄`, `✅`, `🚧`, `✨`), `plan_{subtask_name}.md` detailed implementation files, `doc_update.md` documentation staging files, `zero-tolerance policy` enforcement mechanisms, `ephemeral nature` classification preventing authoritative reference usage, complexity criteria thresholds (3+ files, 100+ lines of code), context window management with 80% capacity monitoring, and absolute reference prohibitions preventing scratchpad content from appearing in production code or documentation dependencies. The document establishes authoritative standards for temporary workspace management while ensuring clear separation between draft planning materials and production documentation.

##### Main Components

The document contains eight primary sections establishing comprehensive scratchpad governance: Critical Foundation Rules defining non-negotiable standards and universal application policies, Scratchpad Directory Purpose establishing core workspace functionality and ephemeral nature classification, Directory Structure & Naming specifying mandatory patterns and file naming conventions, Required Files & Content detailing mandatory file types and content requirements, Implementation Workflow covering creation triggers and process management, Access & Reference Rules establishing usage restrictions and prohibition policies, Lifecycle Management covering creation through archival phases, and Enforcement and Compliance defining zero-tolerance policies and verification processes. Each section provides specific requirements, examples, and implementation guidance ensuring consistent application across all complex implementation planning operations while maintaining clear boundaries between temporary workspace content and authoritative project documentation.

###### Architecture & Design

The architecture implements a structured temporary workspace model with mandatory directory patterns, specialized file types, and strict separation between draft planning materials and production documentation. The design employs complexity-based activation criteria triggering scratchpad creation for tasks meeting specific thresholds, standardized file naming conventions ensuring consistent organization, and ephemeral content classification preventing authoritative reference usage. The system uses progress tracking mechanisms with specific status symbols, mandatory documentation linking requirements, and absolute reference prohibitions maintaining clear boundaries between temporary planning content and production systems. The architectural pattern includes lifecycle management protocols covering creation through completion phases, context window monitoring for graceful plan creation halting, and compliance verification processes ensuring adherence to established standards.

####### Implementation Approach

The implementation uses complexity threshold evaluation determining when scratchpad directories are required based on file count (3+), code volume (100+ lines), and architectural impact criteria. The approach employs structured directory creation following `<project_root>/scratchpad/<implementation_plan_name_in_lower_snake_case>/` patterns with mandatory file types including overview, progress tracking, and detailed subtask plans. Content management implements comprehensive documentation linking requirements, status indicator maintenance using specific symbols, and progress tracking throughout implementation phases. Quality assurance uses zero-tolerance compliance checking, immediate correction requirements for violations, and periodic verification processes ensuring ongoing standards adherence while maintaining clear separation between temporary planning materials and authoritative project documentation.

######## External Dependencies & Integration Points

**→ References:**
- `<project_root>/scratchpad/` directory - mandatory workspace location for all temporary implementation planning activities
- Official project documentation files - comprehensive linking requirements in `plan_overview.md` files for context establishment
- Production codebase files - implementation targets referenced in detailed subtask planning documents
- Context window monitoring systems - 80% capacity thresholds triggering graceful plan creation halting
- Session management systems - fresh session requirements for consistency checking and implementation execution

**← Referenced By:**
- Complex implementation workflows - consume scratchpad planning documents for structured task execution
- Documentation update processes - reference `doc_update.md` files for proposed documentation changes
- Progress tracking systems - monitor implementation status through `plan_progress.md` status indicators
- Quality assurance processes - enforce compliance verification and zero-tolerance policy implementation
- Lifecycle management procedures - apply creation, maintenance, and completion standards across scratchpad operations

**⚡ System role and ecosystem integration:**
- **System Role**: Temporary workspace management system within the Jesse Framework MCP project, providing structured planning environment for complex implementations while maintaining strict separation from production documentation
- **Ecosystem Position**: Auxiliary infrastructure component supporting complex development workflows through structured planning capabilities while explicitly preventing authoritative reference usage in production systems
- **Integration Pattern**: Created by development workflows for complex task planning, consumed by implementation processes for structured execution guidance, and managed through lifecycle protocols while maintaining absolute prohibition against production code or documentation references

######### Edge Cases & Error Handling

The document addresses compliance violations through zero-tolerance enforcement requiring immediate correction of missing required files, incorrect naming patterns, and inconsistent status indicators. Reference prohibition violations trigger absolute blocking with no exceptions permitted for scratchpad content appearing in production code or documentation dependencies. Complexity criteria edge cases receive explicit guidance for borderline tasks with clear thresholds and evaluation criteria. Context window exhaustion scenarios implement graceful halting at 80% capacity with proper progress preservation and session handoff procedures. The system handles incomplete plan creation through structured recovery processes, maintains consistency checking requirements across fresh sessions, and provides specific violation categories with corresponding resolution procedures ensuring adherence to established standards.

########## Internal Implementation Details

The directory structure system uses `lower_snake_case` pattern matching for implementation plan names with mandatory subdirectory creation under `<project_root>/scratchpad/` location. File naming conventions implement exact patterns including `plan_overview.md`, `plan_progress.md`, `plan_{subtask_name}.md`, and `doc_update.md` with specific content requirements for each file type. Status tracking uses precise symbol definitions (`❌`, `🔄`, `✅`, `🚧`, `✨`) with mandatory maintenance throughout implementation phases. Compliance verification implements multi-stage checking including creation validation, progress monitoring, completion confirmation, and periodic audit cycles. Reference prohibition enforcement maintains absolute exclusion lists preventing scratchpad content from appearing in production systems while ensuring clear separation between temporary planning materials and authoritative project documentation.

########### Code Usage Examples

This example demonstrates the mandatory directory structure pattern for complex implementation planning. The structured approach ensures consistent workspace organization across all temporary planning activities.

```bash
# Create scratchpad directory following mandatory pattern structure
mkdir -p scratchpad/authentication_system_implementation/
# Directory name uses lower_snake_case format as required
```

This example shows the required file structure within scratchpad directories with mandatory file types. The standardized naming patterns enable consistent organization and automated processing of planning documents.

```markdown
# Standard scratchpad file organization with required naming conventions
scratchpad/authentication_system_implementation/plan_overview.md
scratchpad/authentication_system_implementation/plan_progress.md
scratchpad/authentication_system_implementation/plan_database_schema.md
scratchpad/authentication_system_implementation/plan_api_endpoints.md
scratchpad/authentication_system_implementation/doc_update.md
```

This example illustrates the mandatory progress tracking format with specific status symbols. The standardized tracking system enables consistent monitoring and reporting across all implementation planning activities.

```markdown
# Progress tracking format using required status symbols
## Implementation Progress Status
- Database Schema Plan: ✅ Plan created
- API Endpoints Plan: 🔄 In progress  
- Authentication Logic Plan: ❌ Plan not created
- Integration Testing Plan: 🚧 Implementation in progress
- Documentation Updates: ✨ Completed
```
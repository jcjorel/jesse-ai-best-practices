<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/embedded_content/workflows/jesse_wip_task_new_session.md -->
<!-- Cached On: 2025-07-06T11:44:00.675657 -->
<!-- Source Modified: 2025-06-27T22:21:30.667473 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file defines the comprehensive `WIP Stack New Session Workflow` for enforcing strict adherence to knowledge management system rules by simulating fresh Cline session initialization within the Jesse Framework ecosystem. The workflow provides mandatory execution of all initialization steps from `JESSE_KNOWLEDGE_MANAGEMENT.md` without exception, ensuring complete system state reset and context loading when normal session startup procedures may have been skipped or incomplete. Key semantic entities include `Cline` session management integration via `https://github.com/cline/cline`, mandatory file loading from `.knowledge/JESSE_KNOWLEDGE_MANAGEMENT.md`, Essential Knowledge Base processing from `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md`, git clone knowledge loading from `.knowledge/git-clones/` directory with `[repo-name]_kb.md` files, WIP task context loading from `.knowledge/work-in-progress/[current_task]/WIP_TASK.md` and `PROGRESS.md`, structured status summary display format, compliance verification protocols, session readiness confirmation messages, strict execution order requirements, error handling with immediate stop conditions, and integration compatibility with `/jesse_wip_task_create.md`, `/jesse_wip_task_switch.md`, and `/jesse_wip_task_capture_knowledge.md` workflows. The system enables developers to guarantee complete knowledge management system initialization and context restoration when session state consistency is questionable or incomplete.

##### Main Components

The workflow contains seven mandatory execution steps: system rules reload requiring complete reading of `.knowledge/JESSE_KNOWLEDGE_MANAGEMENT.md`, Essential Knowledge Base loading from persistent knowledge storage, git clone knowledge loading with repository verification, WIP task context loading including active task identification and progress assessment, context summary display with structured status reporting, compliance verification for knowledge management rule activation, and session readiness confirmation with initialization completion status. Supporting components include implementation requirements specifying strict execution order and no conditional logic, comprehensive error handling procedures with immediate failure reporting and remediation steps, usage examples demonstrating basic invocation and specific focus scenarios, integration specifications with other knowledge management workflows, and success criteria validation including file processing verification and knowledge consistency checking.

###### Architecture & Design

The architecture implements a mandatory sequential execution pattern with strict adherence to knowledge management system initialization protocols. The design uses unconditional step execution regardless of current session state, comprehensive file loading from multiple knowledge storage locations, and structured status reporting with detailed context summaries. The system employs fail-fast error handling with immediate execution termination upon any step failure, mandatory verification requirements after each major step, and session state reset functionality while preserving persistent knowledge and WIP task progress. The workflow follows a compliance-first approach ensuring all knowledge management rules are actively enforced and session initialization is complete before normal operation resumption.

####### Implementation Approach

The implementation uses sequential mandatory step execution with no shortcuts or conditional logic, comprehensive file reading operations across multiple knowledge storage directories, and structured verification protocols after each major loading phase. The approach employs strict error handling with immediate execution termination and specific remediation step provision, detailed status summary generation with formatted output templates, and integration compatibility verification with existing workflow systems. File loading operations target specific paths including `.knowledge/JESSE_KNOWLEDGE_MANAGEMENT.md`, `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md`, `.knowledge/git-clones/` directory contents, and `.knowledge/work-in-progress/[current_task]/` files with comprehensive content processing and consistency validation.

######## External Dependencies & Integration Points

**→ References:**
- `.knowledge/JESSE_KNOWLEDGE_MANAGEMENT.md` - system rules and knowledge management directives requiring complete processing
- `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md` - Essential Knowledge Base with accumulated project learnings
- `.knowledge/git-clones/` directory - external repository knowledge storage with `[repo-name]_kb.md` files
- `.knowledge/work-in-progress/[current_task]/WIP_TASK.md` - active task definition and context
- `.knowledge/work-in-progress/[current_task]/PROGRESS.md` - current task progress and status tracking
- `https://github.com/cline/cline` - Cline session management system for initialization simulation

**← Referenced By:**
- `/jesse_wip_task_create.md` - workflow requiring complete session initialization as prerequisite
- `/jesse_wip_task_switch.md` - workflow benefiting from full context loading and system state verification
- `/jesse_wip_task_capture_knowledge.md` - workflow requiring active knowledge management rule enforcement
- Development workflows - consume initialized session state for consistent knowledge management operation
- Debugging procedures - use session reset functionality for troubleshooting knowledge management issues

**⚡ System role and ecosystem integration:**
- **System Role**: Critical session initialization workflow within the Jesse Framework knowledge management ecosystem, serving as the authoritative method for ensuring complete system state compliance and context loading
- **Ecosystem Position**: Core infrastructure component providing mandatory initialization services for all knowledge management operations, essential for maintaining system consistency and rule adherence
- **Integration Pattern**: Invoked by developers through direct command execution, serves as prerequisite for other workflows, and provides session state reset functionality while preserving persistent knowledge and active task context

######### Edge Cases & Error Handling

The workflow handles missing or inaccessible knowledge files through immediate execution termination with specific failure point reporting and exact remediation step provision. Corrupted or inconsistent knowledge base content triggers verification failure with detailed error reporting and resolution guidance. Session state inconsistencies are resolved through complete system reset while preserving persistent knowledge and WIP task progress. File permission issues during knowledge loading provide clear access configuration guidance and alternative loading strategies. Network connectivity problems affecting external repository access implement graceful degradation with offline knowledge processing capabilities. Incomplete WIP task context scenarios trigger comprehensive task identification and progress reconstruction procedures with user guidance for manual context restoration.

########## Internal Implementation Details

The system rules reload mechanism performs complete file reading with content processing and session flag reset functionality. Essential Knowledge Base loading implements comprehensive content analysis with knowledge gap identification and consistency validation algorithms. Git clone knowledge loading uses directory scanning with repository verification and storage policy compliance checking. WIP task context loading employs active task identification through Essential Knowledge Base analysis and comprehensive file loading from task-specific directories. Status summary generation uses structured template processing with dynamic content insertion and comprehensive resource listing. Compliance verification implements rule activation checking with automatic knowledge capture enablement and consistency maintenance protocol activation. Session readiness confirmation uses multi-phase validation with completion status verification and user notification formatting.

########### Code Usage Examples

This example demonstrates basic workflow invocation for complete session initialization. The command triggers mandatory execution of all initialization steps without conditional logic or shortcuts.

```bash
User: /wip_stack_new_session
```

This example shows workflow usage with specific focus on current task context. The initialization process emphasizes WIP task progress and immediate next actions while maintaining complete system loading.

```bash
User: /wip_stack_new_session
Focus on the current WIP task progress and next actions.
```

This example illustrates workflow invocation after suspected system issues. The complete reinitialization addresses potential missed initialization steps and ensures full compliance with knowledge management rules.

```bash
User: /wip_stack_new_session
I think Cline missed some initialization steps. Please reload everything.
```

This example demonstrates the structured status summary output format providing comprehensive system state information. The template ensures consistent reporting of all loaded knowledge components and session readiness status.

```markdown
=== KNOWLEDGE MANAGEMENT SYSTEM STATUS ===
✓ System Rules: Loaded from JESSE_KNOWLEDGE_MANAGEMENT.md
✓ Essential Knowledge: [summary of key project knowledge]
✓ Git Clones: [list of available repositories and their status]
✓ Active WIP Task: [task_name] | Status: [current_status]
✓ Session State: Fully initialized and compliant

Current Task Context:
- Purpose: [WIP task purpose]
- Progress: [current progress summary]
- Next Actions: [immediate next steps]
- Priority: [task priority level]

Available Resources:
- [list of key knowledge resources]
- [list of relevant git clone repositories]
- [list of related documentation files]
=== END STATUS SUMMARY ===
```
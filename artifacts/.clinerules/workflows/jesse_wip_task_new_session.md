# WIP Stack New Session Workflow

## Purpose
Force strict adherence to all knowledge management system rules by simulating a fresh Cline session initialization. This workflow ensures that all mandatory behaviors from `JESSE_KNOWLEDGE_MANAGEMENT.md` are executed when they may have been skipped during normal session startup.

## When to Use
- When Cline has skipped automatic session initialization
- When knowledge management rules are not being followed
- When WIP task context is missing or incomplete
- When starting work after a break and need full context reload
- When debugging knowledge management system issues
- When you suspect the session state is inconsistent

## Critical Enforcement
This workflow **MANDATORILY** executes ALL initialization steps from `JESSE_KNOWLEDGE_MANAGEMENT.md` without exception, regardless of current session state.

## Workflow Steps

### 1. System Rules Reload
**MANDATORY**: Read and process knowledge management system rules:
- Read `JESSE_KNOWLEDGE_MANAGEMENT.md` completely
- Confirm understanding of all system directives
- Reset any session flags or cached state

### 2. Essential Knowledge Base Loading
**MANDATORY**: Load persistent project knowledge:
- Read `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md`
- Process all accumulated project learnings
- Identify any knowledge gaps or inconsistencies

### 3. Git Clone Knowledge Loading
**MANDATORY**: Load all external repository knowledge:
- Check `.knowledge/git-clones/` directory for available repositories
- Read all `[repo-name]_kb.md` files referenced in Essential Knowledge Base
- Verify git clone storage policy compliance (exclusive `.knowledge/git-clones/` location)

### 4. WIP Task Context Loading
**MANDATORY**: Load active Work-in-Progress task information:
- Identify current active WIP task from Essential Knowledge Base
- Read `.knowledge/work-in-progress/[current_task]/WIP_TASK.md`
- Read `.knowledge/work-in-progress/[current_task]/PROGRESS.md`
- Load any additional WIP task assets

### 5. Context Summary Display
**MANDATORY**: Provide comprehensive context summary:
```
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

### 6. Compliance Verification
**MANDATORY**: Verify all knowledge management rules are active:
- Confirm automatic knowledge capture is enabled
- Verify intemporal writing standards are understood
- Check consistency maintenance protocols are active
- Validate single source of truth principles are enforced

### 7. Session Readiness Confirmation
**MANDATORY**: Confirm session is ready for user requests:
```
✓ KNOWLEDGE MANAGEMENT SYSTEM FULLY INITIALIZED
✓ All mandatory initialization steps completed
✓ Session ready for user requests with full context
```

## Implementation Requirements

### Strict Execution Order
All steps must be executed in the exact order specified, with no exceptions or shortcuts.

### Error Handling
If any step fails:
1. Stop execution immediately
2. Report the specific failure point
3. Provide exact remediation steps
4. Do not proceed until the issue is resolved

### No Conditional Logic
This workflow executes ALL steps regardless of:
- Current session state
- Previously loaded information
- User preferences
- Time constraints

### Verification Requirements
After each major step, verify:
- Information was successfully loaded
- No conflicts or inconsistencies exist
- All required files are accessible
- Knowledge integrity is maintained

## Usage Examples

### Basic Usage
```
User: /wip_stack_new_session
```

### With Specific Focus
```
User: /wip_stack_new_session
Focus on the current WIP task progress and next actions.
```

### After System Issues
```
User: /wip_stack_new_session
I think Cline missed some initialization steps. Please reload everything.
```

## Integration with Other Workflows

### Compatibility
This workflow is compatible with all other knowledge management workflows and can be used as a prerequisite for:
- `/jesse_wip_task_create.md`
- `/jesse_wip_task_switch.md`
- `/jesse_wip_task_capture_knowledge.md`
- Any other knowledge management operation

### Session State Reset
This workflow effectively resets the session to a clean, fully-initialized state while preserving all persistent knowledge and WIP task progress.

## Success Criteria
The workflow is successful when:
1. All mandatory files have been read and processed
2. Complete context summary is displayed
3. No knowledge inconsistencies are detected
4. Session is ready for normal operation
5. All knowledge management rules are actively enforced

---

**Note**: This workflow enforces the **mandatory** nature of knowledge management system initialization. It should be used whenever there is any doubt about the completeness of session initialization or adherence to system rules.

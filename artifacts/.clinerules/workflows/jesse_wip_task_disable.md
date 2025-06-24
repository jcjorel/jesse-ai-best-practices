# WIP Task Disable Workflow

## Purpose
Temporarily disable automatic reading of the current WIP task assets for the current [Cline](https://github.com/cline/cline) session. This is a session-only setting that does not persist across sessions.

## When to Use
- When working on tasks unrelated to the current WIP task
- When the WIP task context is causing confusion or interference
- When you need a clean context without WIP task information
- During debugging or troubleshooting sessions

## Workflow Steps

### 1. Confirm Disable Action
Ask user to confirm they want to disable WIP task loading for this session:
```
"This will disable automatic loading of WIP task '[task_name]' for the current session only. 
The WIP task will remain active and will be loaded in future sessions unless explicitly disabled again.
Do you want to proceed?"
```

### 2. Set Session Flag
Create a session-only flag to prevent WIP task loading:
- This flag exists only in memory for the current session
- Does not modify any persistent files
- Will be reset when starting a new [Cline](https://github.com/cline/cline) session

### 3. Provide Confirmation
Confirm to the user:
```
✓ WIP task auto-loading DISABLED for this session
- Current WIP task: [task_name]
- Status: Temporarily disabled (this session only)
- To re-enable: Start a new Cline session or use /wip_task_enable
```

### 4. Document Session State
Note in responses that WIP task is disabled when relevant:
```
Note: WIP task auto-loading is currently disabled for this session
```

## Implementation Notes

### Session Behavior
- The disable flag is session-scoped only
- New [Cline](https://github.com/cline/cline) sessions will load WIP tasks normally
- No persistent state changes are made

### Knowledge Management Impact
- Essential Knowledge Base continues to load normally
- Git clone knowledge bases continue to load normally
- Only WIP task files are skipped during initialization

### Re-enabling Options
1. Start a new [Cline](https://github.com/cline/cline) session (automatic re-enable)
2. Use `/wip_task_enable` workflow (if needed in same session)

## Example Usage

User: `/wip_task_disable`

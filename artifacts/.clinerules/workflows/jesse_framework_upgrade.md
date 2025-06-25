# JESSE Framework Upgrade Workflow

## Purpose
Upgrade the JESSE AI Best Practices Framework by temporarily disabling WIP task loading and re-executing the documented installation process to ensure a clean upgrade experience.

## When to Use
- When new framework features or updates are available
- When experiencing issues with current framework installation
- When framework files may be outdated or corrupted
- When needing to refresh framework configuration and templates
- When recommended by framework maintainers or release notes

## Workflow Steps

### 1. Disable WIP Task Loading
Set session-only flag to prevent current WIP task context from interfering with upgrade:
- Create temporary session flag to disable WIP task auto-loading
- This prevents current task context from confusing the upgrade process
- Flag exists only for current session and doesn't modify persistent files

### 2. User Confirmation
Confirm upgrade intention with user:
```
"This will upgrade the JESSE AI Framework by re-running the installation process.
Current WIP task loading will be temporarily disabled for this session.
The upgrade will refresh all framework files and configurations.
Do you want to proceed with the framework upgrade?"
```

### 3. Execute Framework Upgrade
Run the documented installation process from the framework README:

**Execute this exact command to the user:**
```
"Please install (or update) the JESSE AI Best Practices Framework from https://github.com/jcjorel/jesse-ai-best-practices"
```

This triggers the AI-guided installation process which will:
- Download latest framework files
- Update all JESSE_*.md files
- Refresh workflows and templates
- Verify installation integrity
- Handle both global and project-level installations appropriately

### 4. Upgrade Verification
After installation completes, verify the upgrade:
- Confirm all framework files are updated
- Check that workflows are accessible
- Verify knowledge management system is functional
- Test basic framework operations

### 5. Session Restart Recommendation
Provide user guidance for full restoration:
```
✓ JESSE Framework upgrade completed successfully!

RECOMMENDED NEXT STEPS:
1. Start a new Cline session to restore normal WIP task loading
2. Run /jesse_wip_task_new_session.md to fully reinitialize if needed
3. Verify your current WIP task context is properly loaded

Note: WIP task auto-loading is temporarily disabled for this session only.
```

## Implementation Notes

### Upgrade Safety
- **Non-destructive**: Preserves all user data, knowledge bases, and WIP tasks
- **Session-scoped**: WIP task disable is temporary and session-only
- **Incremental**: Updates framework files while preserving user customizations
- **Reversible**: No permanent changes to user workflow or data

### Installation Process Integration
- Leverages the documented AI-guided installation from README.md
- Handles both global (`${HOME}/Cline/Rules/`) and project-level (`.clinerules/`) installations
- Preserves user identity configuration and project-specific knowledge
- Updates core framework files while maintaining user customizations

### Context Management
- Temporarily disables WIP task loading to prevent context confusion
- Maintains essential knowledge base and git clone references
- Preserves all persistent knowledge and progress tracking
- Ensures clean upgrade environment without WIP task interference

### Post-Upgrade Behavior
- Framework upgrade will be available in the next session
- WIP task context restoration requires new session or explicit re-enable
- All persistent data (knowledge bases, tasks, git clones) remains intact
- User can continue work immediately after restart

## Usage Examples

### Basic Upgrade
```
User: /jesse_framework_upgrade.md
```

### Upgrade with Verification
```
User: /jesse_framework_upgrade.md
AI: [Confirms upgrade, disables WIP, executes installation]
User: [Starts new session]
User: /jesse_wip_task_new_session.md
```

### Troubleshooting Upgrade
```
User: /jesse_framework_upgrade.md
AI: [If upgrade fails, provides specific error guidance]
User: [Addresses specific issues]
User: /jesse_framework_upgrade.md (retry)
```

## Integration Notes

### Compatibility
- Compatible with both global and project-level framework installations
- Works with all existing WIP tasks and knowledge management structures
- Preserves all user customizations and project-specific configurations
- Maintains backward compatibility with existing workflows

### Workflow Relationship
- Complements `/jesse_wip_task_disable.md` (uses same WIP disable mechanism)
- Pairs with `/jesse_wip_task_new_session.md` for post-upgrade initialization
- Independent of other task management workflows
- Safe to use at any time regardless of current WIP task status

## Success Criteria
The upgrade is successful when:
1. All framework files are updated to latest versions
2. Workflows are accessible and functional
3. Knowledge management system operates correctly
4. User can create new sessions with full framework functionality
5. All persistent data and configurations are preserved

---

**Note**: This workflow provides a simple, safe way to upgrade the JESSE AI Framework while ensuring minimal disruption to ongoing work. The temporary WIP task disable ensures a clean upgrade environment, while the session-scoped nature means normal operation resumes immediately after starting a new session.

###############################################################################
# IMPORTANT: This header comment is designed for GenAI code review and maintenance
# Any GenAI tool working with this file MUST preserve and update this header
###############################################################################
# [GenAI coding tool directive]
# - Maintain this header with all modifications
# - Update History section with each change
# - Keep only the 4 most recent records in the history section. Sort from newer to older.
# - Preserve Intent, Design, and Constraints sections
# - Use this header as context for code reviews and modifications
# - Ensure all changes align with the design principles
# - Respect system prompt directives at all times
###############################################################################
# [Source file intent]
# Project setup guidance utilities for JESSE Framework MCP server.
# Provides standardized HTTP-formatted guidance for missing project setup.
###############################################################################
# [Source file design principles]
# - Single responsibility for project setup guidance generation
# - HTTP-formatted responses for consistent MCP resource integration
# - Clear, actionable instructions for users to resolve setup issues
# - No dependencies on other project modules to avoid circular imports
###############################################################################
# [Source file constraints]
# - Must work independently without project root detection
# - HTTP formatting must match existing MCP response patterns
# - Setup instructions must be clear and actionable for end users
# - No circular import dependencies with other helper modules
###############################################################################
# [Dependencies]
# codebase:jesse_framework_mcp.helpers.http_formatter - HTTP section formatting
# system:typing - Type hints for better code documentation
###############################################################################
# [GenAI tool change history]
# 2025-07-03T22:05:00Z : Created dedicated project setup guidance module by CodeAssistant
# * Moved get_project_setup_guidance() from circular import situation to dedicated module
# * Established single responsibility for project setup error responses
# * Clean HTTP formatting with no circular dependencies
###############################################################################

from ..helpers.http_formatter import format_http_section, ContentCriticality


def get_project_setup_guidance() -> str:
    """
    [Function intent]
    Generate standardized HTTP-formatted guidance for missing project setup.
    
    [Design principles]
    Consistent error response across all JESSE Framework MCP resources.
    CRITICAL criticality ensures users see this important setup information.
    Clear, actionable instructions for both setup methods.
    
    [Implementation details]
    Returns HTTP-formatted markdown content with setup instructions.
    Includes both Git repository and environment variable approaches.
    Uses CRITICAL criticality to ensure visibility in AI assistant processing.
    
    Returns:
        HTTP-formatted setup guidance message
    """
    guidance_content = """# JESSE Framework Setup Required

The JESSE Framework MCP server requires a project root to function properly.

## Current Status
❌ **No project root detected**

The server attempted to locate your project root using these methods:
1. **JESSE_PROJECT_ROOT environment variable** - Not set or invalid
2. **Git repository detection** - No .git directory found in current path or parent directories

## Solution Options

### Option 1: Work in a Git Repository (Recommended)
```bash
cd /path/to/your/git/repository
# Then restart the MCP server
```

### Option 2: Set Environment Variable
```bash
# Linux/macOS
export JESSE_PROJECT_ROOT=/path/to/your/project

# Windows
set JESSE_PROJECT_ROOT=C:\\path\\to\\your\\project

# Then restart the MCP server
```

## What This Enables
Once properly configured, the JESSE Framework provides:

- ✅ **Project-specific knowledge management** (`.knowledge/` directory)
- ✅ **WIP task tracking and management** (`.knowledge/work-in-progress/`)
- ✅ **Git integration features** (branch management, commit workflows)
- ✅ **Project context resources** (gitignore files, project structure)
- ✅ **Workflow automation** (slash commands in Cline)

## Next Steps
1. Choose one of the setup options above
2. Restart the MCP server
3. Verify setup by accessing any JESSE Framework resource

The server will automatically detect your project root and enable all features once properly configured.
"""
    
    return format_http_section(
        content=guidance_content,
        content_type="text/markdown",
        criticality=ContentCriticality.CRITICAL,
        description="JESSE Framework Setup Required",
        section_type="setup-guidance",
        location="setup://project-root-missing",
        additional_headers={
            "Setup-Required": "true",
            "Setup-Methods": "git-repo, env-variable", 
            "Documentation": "https://github.com/jesse-framework/docs/setup"
        }
    )

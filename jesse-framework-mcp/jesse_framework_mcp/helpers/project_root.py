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
# Centralized project root detection and setup guidance for JESSE Framework MCP server.
# Provides robust project directory discovery with environment variable and Git repository support.
###############################################################################
# [Source file design principles]
# - Priority-based project root detection (JESSE_PROJECT_ROOT env var, then Git repo)
# - Standardized error messaging for missing project setup
# - Defensive programming with comprehensive error handling
# - HTTP-formatted guidance responses for consistent user experience
###############################################################################
# [Source file constraints]
# - Must work correctly regardless of MCP server launch method (direct, uv run, etc.)
# - Project root detection must be reliable across different operating systems
# - Error guidance must be clear and actionable for end users
# - HTTP formatting must match existing resource response patterns
###############################################################################
# [Dependencies]
# system:os - Environment variable access for JESSE_PROJECT_ROOT
# system:pathlib.Path - Cross-platform path operations
# codebase:http_formatter - HTTP section formatting for error responses
###############################################################################
# [GenAI tool change history]
# 2025-06-28T12:09:56Z : Initial project root detection implementation by CodeAssistant
# * Created centralized project root detection with JESSE_PROJECT_ROOT env var priority
# * Implemented Git repository upward traversal for automatic project discovery
# * Added standardized HTTP-formatted error guidance for missing project setup
# * Established robust cross-platform path handling for various MCP launch scenarios
###############################################################################

import os
from pathlib import Path
from typing import Optional
from .http_formatter import format_http_section, ContentCriticality


def get_project_root() -> Optional[Path]:
    """
    [Function intent]
    Detect the JESSE Framework project root directory using priority-based discovery.
    
    [Design principles]
    Environment variable takes precedence over automatic Git repository detection.
    Upward directory traversal ensures discovery regardless of current working directory.
    Returns None rather than raising exceptions for graceful error handling.
    
    [Implementation details]
    Priority 1: JESSE_PROJECT_ROOT environment variable (if set and valid)
    Priority 2: Search upward from current directory for .git/ directory
    Stops at filesystem root to prevent infinite traversal.
    
    Returns:
        Path object pointing to project root, or None if not found
        
    Raises:
        No exceptions raised - returns None for missing/invalid project roots
    """
    
    # Priority 1: Check JESSE_PROJECT_ROOT environment variable
    env_root = os.getenv('JESSE_PROJECT_ROOT')
    if env_root:
        project_path = Path(env_root).resolve()
        if project_path.exists() and project_path.is_dir():
            return project_path
        # Invalid JESSE_PROJECT_ROOT set - continue with Git detection
    
    # Priority 2: Search upward for .git/ directory
    current = Path.cwd().resolve()
    while current != current.parent:  # Stop at filesystem root
        git_dir = current / '.git'
        if git_dir.exists():
            return current
        current = current.parent
    
    # No project root found
    return None


def ensure_project_root() -> Path:
    """
    [Function intent]
    Get project root or raise clear exception if not found.
    
    [Design principles]
    Wrapper around get_project_root() that converts None to descriptive exception.
    Provides clear guidance in exception message for troubleshooting.
    
    [Implementation details]
    Calls get_project_root() and raises ValueError with guidance if None returned.
    Exception message includes both setup options for user convenience.
    
    Returns:
        Path object pointing to valid project root
        
    Raises:
        ValueError: When project root cannot be detected with setup guidance
    """
    
    project_root = get_project_root()
    if project_root is None:
        raise ValueError(
            "JESSE Framework project root not found. "
            "Either work in a Git repository or set JESSE_PROJECT_ROOT environment variable."
        )
    
    return project_root


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


def get_project_relative_path(relative_path: str) -> Path:
    """
    [Function intent]
    Get absolute path relative to detected project root.
    
    [Design principles]
    Centralized path resolution based on detected project root.
    Raises clear exceptions if project root cannot be determined.
    
    [Implementation details]
    Uses ensure_project_root() to get valid project root, then resolves relative path.
    Returns absolute Path object for reliable file operations.
    
    Args:
        relative_path: Path relative to project root (e.g., '.knowledge/work-in-progress')
        
    Returns:
        Absolute Path object relative to project root
        
    Raises:
        ValueError: When project root cannot be detected
    """
    
    project_root = ensure_project_root()
    return project_root / relative_path


def validate_project_setup() -> dict:
    """
    [Function intent]
    Validate current project setup and return diagnostic information.
    
    [Design principles]
    Comprehensive project validation for debugging and status reporting.
    Structured return data for easy processing by calling code.
    
    [Implementation details]
    Checks project root detection, validates key directories and files,
    returns structured diagnostic information for troubleshooting.
    
    Returns:
        Dictionary with project setup validation results and diagnostics
    """
    
    validation = {
        "project_root_found": False,
        "project_root_path": None,
        "project_root_method": None,
        "jesse_directories": {},
        "validation_timestamp": Path.cwd().resolve().as_posix(),
        "current_working_directory": Path.cwd().resolve().as_posix()
    }
    
    # Check project root detection
    try:
        project_root = get_project_root()
        if project_root:
            validation["project_root_found"] = True
            validation["project_root_path"] = project_root.as_posix()
            
            # Determine detection method
            env_root = os.getenv('JESSE_PROJECT_ROOT')
            if env_root and Path(env_root).resolve() == project_root:
                validation["project_root_method"] = "environment_variable"
            elif (project_root / '.git').exists():
                validation["project_root_method"] = "git_repository"
            else:
                validation["project_root_method"] = "unknown"
            
            # Check JESSE directories
            jesse_dirs = [
                '.knowledge',
                '.knowledge/work-in-progress',
                '.knowledge/git-clones', 
                '.knowledge/pdf-knowledge',
                '.knowledge/persistent-knowledge',
                '.clinerules'
            ]
            
            for dir_path in jesse_dirs:
                full_path = project_root / dir_path
                validation["jesse_directories"][dir_path] = {
                    "exists": full_path.exists(),
                    "is_directory": full_path.is_dir() if full_path.exists() else False,
                    "absolute_path": full_path.as_posix()
                }
        
    except Exception as e:
        validation["error"] = str(e)
    
    return validation

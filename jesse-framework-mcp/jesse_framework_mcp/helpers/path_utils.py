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
# Path resolution utilities for JESSE Framework MCP server.
# Provides portable path variable resolution and path prefix detection.
###############################################################################
# [Source file design principles]
# - Single responsibility for path variable resolution
# - Cross-platform path handling using pathlib
# - Bidirectional path conversion (resolve variables and detect prefixes)
# - No dependencies on other helper modules to avoid circular imports
###############################################################################
# [Source file constraints]
# - Must work correctly regardless of current working directory
# - Path resolution must be reliable across different operating systems
# - No circular import dependencies with other helper modules
###############################################################################
# [Dependencies]
# system:pathlib.Path - Cross-platform path operations
# system:typing - Type hints for better code documentation
###############################################################################
# [GenAI tool change history]
# 2025-07-03T10:04:30Z : Created path utilities module to resolve circular import by CodeAssistant
# * Moved resolve_portable_path() and get_portable_path() from project_root.py
# * Created independent path utilities module without circular dependencies
# * Maintains all existing functionality while resolving import issues
###############################################################################

import os
from pathlib import Path
from typing import Union, Optional


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


def resolve_portable_path(location: str) -> str:
    """
    [Function intent]
    Resolve portable path variables to actual filesystem paths for cross-platform compatibility.
    Transforms JESSE path variables into absolute paths for current environment.
    
    [Design principles]
    Cross-platform path resolution supporting all standard JESSE path variables.
    Immediate resolution without caching for current working directory accuracy.
    
    [Implementation details]
    Replaces {PROJECT_ROOT}, {HOME}, {CLINE_RULES}, {CLINE_WORKFLOWS} variables
    with actual resolved paths using pathlib for cross-platform compatibility.
    
    Args:
        location: Path string with variable placeholders
        
    Returns:
        Resolved absolute path with all variables substituted
        
    Raises:
        OSError: When path resolution fails due to filesystem issues
    """
    try:
        # Define path variable mappings
        variables = {
            '{PROJECT_ROOT}': str(Path.cwd()),
            '{HOME}': str(Path.home()),
            '{CLINE_RULES}': str(Path.home() / 'Cline' / 'Rules'),
            '{CLINE_WORKFLOWS}': str(Path.home() / 'Cline' / 'Workflows')
        }
        
        # Resolve all variables in the location
        resolved = location
        for variable, value in variables.items():
            resolved = resolved.replace(variable, value)
        
        return resolved
        
    except Exception as e:
        raise OSError(f"Failed to resolve portable path '{location}': {str(e)}")


def get_portable_path(full_path: Union[str, Path]) -> str:
    """
    [Function intent]
    Convert full pathname to portable path with MCP server supported variables.
    Returns path prefixed with appropriate variable ({PROJECT_ROOT}, {HOME}, etc.)
    or original path if no supported variable matches.
    
    [Design principles]
    Priority-based variable detection from most specific to most general.
    Cross-platform path resolution using pathlib for reliability.
    Graceful fallback to original path when no variables match.
    Windows absolute path detection to avoid incorrect resolution.
    
    [Implementation details]
    Priority order: {CLINE_WORKFLOWS} > {CLINE_RULES} > {PROJECT_ROOT} > {HOME}.
    Detects Windows absolute paths (C:\\, D:\\, etc.) and returns them as-is.
    Only resolves paths that exist or are relative to avoid cross-platform issues.
    Uses Path.is_relative_to() for reliable path hierarchy checking.
    
    Args:
        full_path: Full pathname as string or Path object
        
    Returns:
        Portable path with variable prefix, or original path if no match
        
    Raises:
        OSError: When path resolution fails due to filesystem issues
    """
    try:
        # Convert input to Path object (but don't resolve yet)
        if isinstance(full_path, str):
            path_obj = Path(full_path)
        else:
            path_obj = Path(full_path)
        
        # Check if this is a Windows absolute path on non-Windows system
        path_str = str(path_obj)
        if len(path_str) >= 3 and path_str[1:3] == ':\\':
            # This is a Windows absolute path (C:\, D:\, etc.)
            # Return as-is with backslashes preserved for Windows path format
            return path_str
        
        # For non-Windows absolute paths and existing paths, try to resolve
        try:
            # Only resolve if the path exists or if it's relative
            if path_obj.exists() or not path_obj.is_absolute():
                path_obj = path_obj.resolve()
            elif path_obj.is_absolute():
                # Absolute path that doesn't exist - use as-is
                path_obj = path_obj
        except (OSError, RuntimeError):
            # Resolution failed, use original path
            pass
        
        # Get actual project root instead of current working directory
        project_root = get_project_root()
        if project_root is None:
            # Fallback to current working directory if project root cannot be detected
            project_root = Path.cwd()
        
        # Define variable paths in priority order (most specific first)
        variable_paths = [
            ('{CLINE_WORKFLOWS}', Path.home() / 'Cline' / 'Workflows'),
            ('{CLINE_RULES}', Path.home() / 'Cline' / 'Rules'),
            ('{PROJECT_ROOT}', project_root),
            ('{HOME}', Path.home())
        ]
        
        # Check each variable path for matches
        for variable, base_path in variable_paths:
            try:
                base_path_resolved = base_path.resolve()
                # Check if path is under this base directory
                if path_obj.is_relative_to(base_path_resolved):
                    # Calculate relative path from base
                    relative_path = path_obj.relative_to(base_path_resolved)
                    # Return portable path with variable
                    return f"{variable}/{relative_path}".replace('\\', '/')
            except (ValueError, OSError):
                # Path is not relative to this base, continue to next
                continue
        
        # No variable matches - return original path as string with forward slashes
        return str(full_path).replace('\\', '/')
        
    except Exception as e:
        raise OSError(f"Failed to convert path to portable format '{full_path}': {str(e)}")

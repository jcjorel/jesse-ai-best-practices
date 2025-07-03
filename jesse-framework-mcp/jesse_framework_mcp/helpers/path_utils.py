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

from pathlib import Path
from typing import Union


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
        
        # Define variable paths in priority order (most specific first)
        variable_paths = [
            ('{CLINE_WORKFLOWS}', Path.home() / 'Cline' / 'Workflows'),
            ('{CLINE_RULES}', Path.home() / 'Cline' / 'Rules'),
            ('{PROJECT_ROOT}', Path.cwd()),
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

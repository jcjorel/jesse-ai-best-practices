#!/usr/bin/env python3
"""Debug script to identify the path resolution issue."""

import sys
from pathlib import Path

# Add the project to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from jesse_framework_mcp.helpers.path_utils import get_portable_path

def debug_path_resolution():
    """Debug the path resolution issue step by step."""
    
    print("=== PATH RESOLUTION DEBUG ===")
    print()
    
    # Current working directory (should be project root)
    cwd = Path.cwd()
    print(f"Current working directory: {cwd}")
    
    # Test file path (the problematic case)
    test_file = cwd / "jesse-framework-mcp" / "tests" / "test_session_init_resource.py"
    print(f"Test file path: {test_file}")
    print(f"Test file exists: {test_file.exists()}")
    print()
    
    # Debug the get_portable_path function step by step
    print("=== DEBUGGING get_portable_path() ===")
    
    # Check if it's a Windows absolute path
    path_str = str(test_file)
    print(f"Path as string: {path_str}")
    is_windows_abs = len(path_str) >= 3 and path_str[1:3] == ":\\"
    print(f"Is Windows absolute path: {is_windows_abs}")
    print()
    
    # Try to resolve the path
    try:
        resolved_path = test_file.resolve()
        print(f"Resolved test file path: {resolved_path}")
    except Exception as e:
        print(f"Failed to resolve test file path: {e}")
        resolved_path = test_file
    print()
    
    # Check PROJECT_ROOT resolution
    project_root_base = cwd
    try:
        project_root_resolved = project_root_base.resolve()
        print(f"PROJECT_ROOT base: {project_root_base}")
        print(f"PROJECT_ROOT resolved: {project_root_resolved}")
    except Exception as e:
        print(f"Failed to resolve PROJECT_ROOT: {e}")
        project_root_resolved = project_root_base
    print()
    
    # Check if path is relative to PROJECT_ROOT
    try:
        is_relative = resolved_path.is_relative_to(project_root_resolved)
        print(f"Is test file relative to PROJECT_ROOT: {is_relative}")
        
        if is_relative:
            relative_path = resolved_path.relative_to(project_root_resolved)
            print(f"Relative path: {relative_path}")
            expected_portable = f"{{PROJECT_ROOT}}/{relative_path}".replace('\\\\', '/')
            print(f"Expected portable path: {expected_portable}")
        
    except Exception as e:
        print(f"Failed to calculate relative path: {e}")
    print()
    
    # Test the actual function
    print("=== TESTING get_portable_path() FUNCTION ===")
    try:
        result = get_portable_path(test_file)
        print(f"Actual result: {result}")
        
        # Check if it starts with {{PROJECT_ROOT}}
        if result.startswith("{PROJECT_ROOT}"):
            path_after_root = result.replace("{PROJECT_ROOT}/", "")
            print(f"Path after PROJECT_ROOT: {path_after_root}")
            expected = "jesse-framework-mcp/tests/test_session_init_resource.py"
            print(f"Expected: {expected}")
            print(f"Match: {path_after_root == expected}")
        
    except Exception as e:
        print(f"get_portable_path() failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_path_resolution()

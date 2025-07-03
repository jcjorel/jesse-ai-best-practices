#!/usr/bin/env python3
"""Debug script to test path resolution from correct project root."""

import sys
import os
from pathlib import Path

# Set working directory to the actual project root
actual_project_root = Path(__file__).parent.parent
os.chdir(actual_project_root)
print(f"Changed working directory to: {Path.cwd()}")

# Add the project to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from jesse_framework_mcp.helpers.path_utils import get_portable_path

def debug_path_resolution_from_correct_root():
    """Debug the path resolution from the correct project root."""
    
    print("=== PATH RESOLUTION FROM CORRECT PROJECT ROOT ===")
    print()
    
    # Current working directory (should be actual project root)
    cwd = Path.cwd()
    print(f"Current working directory: {cwd}")
    
    # Test file path (the problematic case)
    test_file = cwd / "jesse-framework-mcp" / "tests" / "test_session_init_resource.py"
    print(f"Test file path: {test_file}")
    print(f"Test file exists: {test_file.exists()}")
    print()
    
    # Test the actual function from correct working directory
    print("=== TESTING get_portable_path() FROM CORRECT ROOT ===")
    try:
        result = get_portable_path(test_file)
        print(f"Actual result: {result}")
        
        # Check if it starts with {PROJECT_ROOT}
        if result.startswith("{PROJECT_ROOT}"):
            path_after_root = result.replace("{PROJECT_ROOT}/", "")
            print(f"Path after PROJECT_ROOT: {path_after_root}")
            expected = "jesse-framework-mcp/tests/test_session_init_resource.py"
            print(f"Expected: {expected}")
            print(f"Match: {path_after_root == expected}")
            
            if path_after_root != expected:
                print(f"❌ MISMATCH! Expected '{expected}', got '{path_after_root}'")
            else:
                print("✅ CORRECT!")
        else:
            print(f"Result doesn't start with {{PROJECT_ROOT}}: {result}")
        
    except Exception as e:
        print(f"get_portable_path() failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_path_resolution_from_correct_root()

#!/usr/bin/env python3
"""Simple debug script to test path resolution."""

import sys
import os
from pathlib import Path

# Add current directory to path for importing
sys.path.insert(0, str(Path(__file__).parent))

# Direct import just the path utils
from jesse_framework_mcp.helpers.path_utils import get_portable_path

def test_from_project_root():
    """Test path resolution from the actual project root."""
    
    print("=== TESTING FROM ACTUAL PROJECT ROOT ===")
    
    # Save current directory
    original_cwd = Path.cwd()
    print(f"Original working directory: {original_cwd}")
    
    try:
        # Change to actual project root 
        project_root = Path(__file__).parent.parent
        os.chdir(project_root)
        print(f"Changed to project root: {Path.cwd()}")
        
        # Test file path
        test_file = Path.cwd() / "jesse-framework-mcp" / "tests" / "test_session_init_resource.py"
        print(f"Test file: {test_file}")
        print(f"Exists: {test_file.exists()}")
        
        # Test portable path conversion
        result = get_portable_path(test_file)
        print(f"Result: {result}")
        
        # Analyze result
        if result.startswith("{PROJECT_ROOT}"):
            path_part = result.replace("{PROJECT_ROOT}/", "")
            print(f"Path after PROJECT_ROOT: '{path_part}'")
            
            expected = "jesse-framework-mcp/tests/test_session_init_resource.py"
            print(f"Expected: '{expected}'")
            
            if path_part == expected:
                print("✅ CORRECT!")
            else:
                print("❌ INCORRECT!")
                print(f"   Missing part: '{expected}' should be '{path_part}'")
                
                # Debug further
                print("\n=== DEBUGGING THE DIFFERENCE ===")
                expected_parts = expected.split('/')
                actual_parts = path_part.split('/')
                print(f"Expected parts: {expected_parts}")
                print(f"Actual parts: {actual_parts}")
                
                if len(actual_parts) < len(expected_parts):
                    missing_parts = expected_parts[:len(expected_parts) - len(actual_parts)]
                    print(f"Missing parts: {missing_parts}")
        else:
            print(f"❌ Result doesn't start with {{PROJECT_ROOT}}: {result}")
            
    finally:
        # Restore original directory
        os.chdir(original_cwd)
        print(f"Restored working directory: {Path.cwd()}")

if __name__ == "__main__":
    test_from_project_root()

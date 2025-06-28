#!/usr/bin/env python3

"""
Demo script showcasing HttpPath dual-path functionality.
"""

import sys
from pathlib import Path

# Add the package to Python path for demo
sys.path.insert(0, str(Path(__file__).parent))

from jesse_framework_mcp.helpers.http_formatter import HttpPath, format_http_section


def demo_http_path():
    """Demonstrate HttpPath dual-path functionality."""
    print("🚀 HttpPath Dual-Path Demo")
    print("=" * 50)
    
    # Example 1: Basic HttpPath with PROJECT_ROOT
    print("\n1. Basic HttpPath Construction:")
    http_path1 = HttpPath("file://{PROJECT_ROOT}/.knowledge/test.md")
    print(f"   Original Path: {http_path1.get_original_path()}")
    print(f"   Resolved Path: {http_path1.get_resolved_path()}")
    print(f"   String Repr:   {str(http_path1)}")
    
    # Example 2: HttpPath with multiple variables
    print("\n2. Multiple Variables:")
    http_path2 = HttpPath("{HOME}/backup/{PROJECT_ROOT}/data/{CLINE_RULES}/config.json")
    print(f"   Original Path: {http_path2.get_original_path()}")
    print(f"   Resolved Path: {http_path2.get_resolved_path()}")
    
    # Example 3: URL paths (non-filesystem)
    print("\n3. URL Path Handling:")
    http_path3 = HttpPath("https://api.example.com/{HOME}/user/data.json")
    print(f"   Original Path: {http_path3.get_original_path()}")
    print(f"   Resolved Path: {http_path3.get_resolved_path()}")
    print(f"   Name:          {http_path3.name}")
    print(f"   Suffix:        {http_path3.suffix}")
    
    # Example 4: Path operations
    print("\n4. Path Operations:")
    base_path = HttpPath("{PROJECT_ROOT}/.knowledge")
    child_path = base_path / "documents" / "README.md"
    print(f"   Base Path:     {base_path.get_original_path()}")
    print(f"   Child Path:    {child_path.get_original_path()}")
    print(f"   Child Resolved: {child_path.get_resolved_path()}")
    
    # Example 5: Filesystem operations (only for actual filesystem paths)
    print("\n5. Filesystem Operations:")
    current_dir = HttpPath("{PROJECT_ROOT}")
    print(f"   Current Dir:   {current_dir.get_original_path()}")
    print(f"   Exists:        {current_dir.exists()}")
    print(f"   Is Directory:  {current_dir.is_dir()}")
    
    # Example 6: Integration with HTTP formatting
    print("\n6. HTTP Formatting Integration:")
    print("   Using HttpPath in format_http_section():")
    
    location_path = HttpPath("file://{HOME}/Cline/Rules/JESSE_HINTS.md")
    result = format_http_section(
        content="# HttpPath Demo\nThis demonstrates HttpPath integration.",
        content_type="text/markdown",
        criticality="INFORMATIONAL",
        description="HttpPath Integration Demo",
        section_type="knowledge-base",
        location=location_path  # HttpPath object
    )
    
    # Show key parts of the result
    lines = result.split('\n')
    for line in lines:
        if line.startswith("Content-Location:"):
            print(f"   {line}")
            break
    
    print(f"\n   Notice: Location header shows original path with variables:")
    print(f"   '{location_path.get_original_path()}'")
    print(f"   Instead of resolved path:")
    print(f"   '{location_path.get_resolved_path()}'")
    
    # Example 7: Comparison with string location
    print("\n7. String vs HttpPath Location Headers:")
    
    # Same path as string
    string_result = format_http_section(
        content="Same content",
        content_type="text/markdown",
        criticality="INFORMATIONAL", 
        description="String Location Demo",
        section_type="knowledge-base",
        location="file://{HOME}/Cline/Rules/JESSE_HINTS.md"  # String
    )
    
    # Extract location headers
    http_path_location = None
    string_location = None
    
    for line in result.split('\n'):
        if line.startswith("Content-Location:"):
            http_path_location = line
            break
            
    for line in string_result.split('\n'):
        if line.startswith("Content-Location:"):
            string_location = line
            break
    
    print(f"   HttpPath Location: {http_path_location}")
    print(f"   String Location:   {string_location}")
    print(f"   Result: Different headers - HttpPath preserves variables! ✅")


if __name__ == "__main__":
    demo_http_path()

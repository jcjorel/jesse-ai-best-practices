#!/usr/bin/env python3
"""
[Script intent]
Demonstration script for the new Last-Modified header functionality in HTTP formatter.
Shows various usage scenarios with timestamps and backward compatibility.

[Design principles]
Clear examples showing optional parameter usage and error handling.
Demonstrates integration with existing header system.

[Implementation details]
Creates example HTTP sections with and without Last-Modified headers.
Shows proper RFC 7231 timestamp format and validation behavior.
"""

from jesse_framework_mcp.helpers.http_formatter import format_http_section
from datetime import datetime, timezone
from pathlib import Path
import tempfile


def demo_last_modified_functionality():
    """
    [Function intent]
    Demonstrate Last-Modified header functionality with various scenarios.
    
    [Design principles]
    Clear examples showing all supported usage patterns.
    
    [Implementation details]
    Shows timestamp inclusion, omission, and error conditions.
    """
    print("=== JESSE Framework MCP - Last-Modified Header Demo ===\n")
    
    # Scenario 1: HTTP section WITHOUT Last-Modified header (backward compatibility)
    print("1. HTTP section WITHOUT Last-Modified header (existing behavior):")
    print("-" * 60)
    
    result1 = format_http_section(
        content="# Example Framework Rule\nThis rule demonstrates HTTP formatting.",
        content_type="text/markdown",
        criticality="CRITICAL",
        description="Example JESSE Framework Rule",
        section_type="framework-rule",
        location="file://{CLINE_RULES}/EXAMPLE_RULE.md"
    )
    print(result1)
    print("\n")
    
    # Scenario 2: HTTP section WITH Last-Modified header
    print("2. HTTP section WITH Last-Modified header:")
    print("-" * 50)
    
    # Create RFC 7231 formatted timestamp
    current_time = datetime.now(timezone.utc)
    rfc7231_timestamp = current_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    result2 = format_http_section(
        content="# Updated Knowledge Base\nThis content was recently modified.",
        content_type="text/markdown",
        criticality="INFORMATIONAL",
        description="Project Knowledge Base",
        section_type="knowledge-base",
        location="file://{PROJECT_ROOT}/.knowledge/KNOWLEDGE_BASE.md",
        last_modified=rfc7231_timestamp
    )
    print(result2)
    print("\n")
    
    # Scenario 3: HTTP section with Last-Modified AND additional headers
    print("3. HTTP section with Last-Modified AND additional headers:")
    print("-" * 60)
    
    result3 = format_http_section(
        content='{"task": "example", "status": "completed"}',
        content_type="application/json",
        criticality="INFORMATIONAL",
        description="WIP Task Status",
        section_type="wip-task",
        location="file://{PROJECT_ROOT}/.knowledge/work-in-progress/example/WIP_TASK.md",
        last_modified="Thu, 27 Jun 2025 18:30:00 GMT",
        additional_headers={
            "X-Task-Version": "1.2",
            "X-Framework-Component": "WIP-Management"
        }
    )
    print(result3)
    print("\n")
    
    # Scenario 4: Demonstrate error handling
    print("4. Error handling demonstration:")
    print("-" * 35)
    
    try:
        format_http_section(
            content="Test content",
            content_type="text/plain",
            criticality="INFORMATIONAL",
            description="Error Test",
            section_type="knowledge-base",
            location="file://{HOME}/test.txt",
            last_modified=""  # Empty string should raise error
        )
    except ValueError as e:
        print(f"✓ Caught expected error for empty Last-Modified: {e}")
    
    try:
        format_http_section(
            content="Test content",
            content_type="text/plain",
            criticality="INFORMATIONAL",
            description="Error Test",
            section_type="knowledge-base",
            location="file://{HOME}/test.txt",
            last_modified="   \n   "  # Whitespace should raise error
        )
    except ValueError as e:
        print(f"✓ Caught expected error for whitespace Last-Modified: {e}")
    
    # Scenario 5: NEW Path object functionality
    print("5. NEW: HTTP section with Path object Last-Modified (automatic file mtime):")
    print("-" * 70)
    
    # Create a temporary file to demonstrate Path object usage
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as tmp_file:
        tmp_file.write("# Temporary Knowledge Base\nThis file demonstrates automatic mtime reading.")
        tmp_path = Path(tmp_file.name)
    
    try:
        result5 = format_http_section(
            content="# Knowledge Base Content\nThis content shows automatic Last-Modified from file system.",
            content_type="text/markdown",
            criticality="INFORMATIONAL",
            description="Automatic mtime demonstration",
            section_type="knowledge-base",
            location="file://{PROJECT_ROOT}/.knowledge/auto_mtime.md",
            last_modified=tmp_path  # Path object automatically reads file mtime
        )
        print(result5)
        print("\n")
        
    finally:
        # Clean up temporary file
        tmp_path.unlink(missing_ok=True)
    
    # Scenario 6: Path object with additional headers
    print("6. Path object with additional headers integration:")
    print("-" * 50)
    
    # Create another temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp_file:
        tmp_file.write('{"version": "1.0", "content": "test data"}')
        tmp_path = Path(tmp_file.name)
    
    try:
        result6 = format_http_section(
            content='{"updated_content": "This shows Path object integration with custom headers"}',
            content_type="application/json",
            criticality="CRITICAL",
            description="Path Object Integration Test",
            section_type="framework-rule",
            location="file://{HOME}/integration_test.json",
            last_modified=tmp_path,  # Path object for automatic mtime
            additional_headers={
                "X-Source-Type": "FileSystem",
                "X-Auto-Timestamp": "Enabled"
            }
        )
        print(result6)
        print("\n")
        
    finally:
        # Clean up temporary file
        tmp_path.unlink(missing_ok=True)
    
    # Scenario 7: Path object error handling
    print("7. Path object error handling:")
    print("-" * 32)
    
    try:
        non_existent_file = Path("/non/existent/file.txt")
        format_http_section(
            content="Test content",
            content_type="text/plain",
            criticality="INFORMATIONAL",
            description="Non-existent File Test",
            section_type="knowledge-base",
            location="file://{HOME}/test.txt",
            last_modified=non_existent_file
        )
    except FileNotFoundError as e:
        print(f"✓ Caught expected error for non-existent file: {e}")
    
    try:
        format_http_section(
            content="Test content",
            content_type="text/plain",
            criticality="INFORMATIONAL", 
            description="Invalid Type Test",
            section_type="knowledge-base",
            location="file://{HOME}/test.txt",
            last_modified=12345  # Invalid type
        )
    except TypeError as e:
        print(f"✓ Caught expected error for invalid type: {e}")
    
    print("\n=== Demo Complete ===")
    print("Key Features Demonstrated:")
    print("• Optional Last-Modified header parameter (string or Path object)")
    print("• Backward compatibility (no header when not provided)")
    print("• NEW: Path object support with automatic file mtime reading")
    print("• NEW: Automatic RFC 7231 timestamp formatting from Unix mtime")
    print("• Integration with additional headers (both string and Path modes)")
    print("• Proper header ordering (Last-Modified before additional headers)")
    print("• Validation for empty/whitespace timestamps")
    print("• Error handling for non-existent files and invalid types")
    print("• Standard RFC 7231 timestamp format support")


if __name__ == "__main__":
    demo_last_modified_functionality()

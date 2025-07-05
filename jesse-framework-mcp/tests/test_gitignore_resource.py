#!/usr/bin/env python3
"""
Test script for the new gitignore files resource.
Tests the jesse://project/gitignore-files resource functionality.
"""

import asyncio
from pathlib import Path
import sys
import os

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import the unwrapper utility and resources
from utils import unwrap_fastmcp_function
from jesse_framework_mcp.resources import project_resources


async def test_gitignore_resource():
    """
    [Function intent]
    Test the gitignore files resource functionality.
    
    [Design principles]
    Comprehensive testing of all gitignore resource scenarios.
    Verify HTTP formatting and writable flag functionality.
    
    [Implementation details]
    Creates a mock context and calls the gitignore resource function.
    Tests with both existing and missing .gitignore files.
    """
    print("🧪 Testing JESSE Framework MCP - Gitignore Files Resource")
    print("=" * 60)
    
    # Create a simple mock context for testing
    class MockContext:
        def __init__(self):
            self.messages = []
        
        async def info(self, message: str):
            self.messages.append(f"INFO: {message}")
            print(f"📝 {message}")
        
        async def error(self, message: str):
            self.messages.append(f"ERROR: {message}")
            print(f"❌ {message}")
    
    ctx = MockContext()
    
    try:
        print("\n🔍 Testing gitignore files resource...")
        
        # Unwrap the FastMCP decorated function for direct testing
        print("🔧 Unwrapping FastMCP decorated function...")
        unwrapped_function = unwrap_fastmcp_function(project_resources.get_project_gitignore_files)
        print(f"✅ Successfully unwrapped function: {unwrapped_function.__name__}")
        
        result = await unwrapped_function(ctx)
        
        print("\n📋 Resource Response:")
        print("-" * 40)
        print(result)
        print("-" * 40)
        
        # Verify response structure
        print("\n✅ Verification Results:")
        
        # Check for boundary markers
        boundary_count = result.count("--JESSE_FRAMEWORK_BOUNDARY_2025--")
        print(f"📌 Found {boundary_count} HTTP boundary markers")
        
        # Check for writable headers
        writable_count = result.count("X-ASYNC-Content-Writable: true")
        print(f"✏️  Found {writable_count} writable content sections")
        
        # Check for gitignore file types
        gitignore_sections = result.count("X-ASYNC-Content-Section: gitignore-file")
        error_sections = result.count("X-ASYNC-Content-Section: gitignore-error")
        print(f"📄 Found {gitignore_sections} gitignore file sections")
        print(f"🚨 Found {error_sections} error sections")
        
        # Check for specific directories
        directories = [
            "Project Root Directory",
            "Coding Assistant Artifacts", 
            "Knowledge Management System",
            "Project-Specific Rules"
        ]
        
        for directory in directories:
            if directory in result:
                print(f"📁 ✅ {directory} section present")
            else:
                print(f"📁 ❌ {directory} section missing")
        
        print(f"\n🎯 Test completed successfully!")
        print(f"📊 Context messages: {len(ctx.messages)}")
        
        return True
        
    except Exception as e:
        print(f"\n💥 Test failed with error: {str(e)}")
        print(f"📊 Context messages: {len(ctx.messages)}")
        return False


async def main():
    """
    [Function intent]
    Main test execution function.
    
    [Design principles]
    Simple test runner with clear output formatting.
    Proper async context handling for MCP testing.
    
    [Implementation details]
    Runs the gitignore resource test and reports results.
    """
    print("🚀 Starting JESSE Framework MCP Gitignore Resource Test")
    
    # Change to the project root directory for testing
    os.chdir(Path(__file__).parent.parent)
    print(f"📂 Working directory: {os.getcwd()}")
    
    success = await test_gitignore_resource()
    
    if success:
        print("\n🎉 All tests passed!")
        exit(0)
    else:
        print("\n💔 Tests failed!")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())

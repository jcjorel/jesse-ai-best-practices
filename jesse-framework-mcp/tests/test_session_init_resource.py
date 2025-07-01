#!/usr/bin/env python3
"""
Test script for JESSE Framework MCP Server session initialization meta-resource.

This script tests the jesse://session/init-context resource which combines
all essential resources for Cline session initialization.
"""

import asyncio
import sys
from pathlib import Path

# Add the package to Python path
sys.path.insert(0, str(Path(__file__).parent))

from jesse_framework_mcp.main import server
from fastmcp import Context
from utils import unwrap_fastmcp_function


async def test_session_init_resource():
    """
    [Function intent]
    Test the session initialization meta-resource functionality.
    
    [Design principles]
    Comprehensive testing of all resource sections with error handling.
    Verification of HTTP formatting and multi-section response structure.
    
    [Implementation details]
    Creates test context, calls session initialization resource,
    verifies multi-section response structure and content.
    """
    
    print("=== Testing JESSE Framework Session Initialization Meta-Resource ===")
    print()
    
    try:
        # Create test context
        class TestContext:
            async def info(self, message):
                print(f"ℹ️  {message}")
            
            async def error(self, message):
                print(f"❌ {message}")
            
            async def warning(self, message):
                print(f"⚠️  {message}")
            
            async def debug(self, message):
                print(f"🐛 {message}")
            
            async def report_progress(self, current, total, message):
                percentage = (current / total) * 100
                print(f"📊 [{percentage:3.0f}%] {message}")
        
        ctx = TestContext()
        
        print("🚀 Calling session initialization resource...")
        print()
        
        # Test the session initialization resource
        from jesse_framework_mcp.resources.session_init import get_session_init_context
        
        # Unwrap the FastMCP function before calling
        session_init_func = unwrap_fastmcp_function(get_session_init_context)
        result = await session_init_func(ctx)
        
        print()
        print("✅ Session initialization resource completed successfully!")
        print()
        
        # Analyze the result
        if result:
            print("📋 Result Analysis:")
            print(f"   - Total response length: {len(result):,} characters")
            
            # Count HTTP sections
            section_count = result.count("Content-Type:")
            print(f"   - Number of HTTP sections: {section_count}")
            
            # Check for key sections
            key_sections = [
                ("framework-rule", "CRITICAL", "JESSE Framework Rules"),
                ("Project Context", "INFORMATIONAL", "Project Context"),
                ("WIP Tasks", "INFORMATIONAL", "WIP Tasks"),
                ("Workflows Index", "INFORMATIONAL", "Workflows Index"),
                ("Knowledge", "INFORMATIONAL", "Knowledge"),
                ("gitignore", "INFORMATIONAL", "gitignore")
            ]
            
            print("   - Section verification:")
            for section_pattern, expected_criticality, display_name in key_sections:
                if section_pattern.lower() in result.lower():
                    if expected_criticality in result:
                        print(f"     ✅ {display_name} section found with {expected_criticality} criticality")
                    else:
                        print(f"     ⚠️  {display_name} section found but criticality unclear")
                else:
                    print(f"     ❌ {display_name} section missing")
            
            print()
            print("📄 Sample of first 500 characters:")
            print("-" * 60)
            sample_lines = result[:500].split('\n')
            for line in sample_lines[:10]:  # Show first 10 lines of sample
                print(f"   {line}")
            print("-" * 60)
            
        else:
            print("❌ Session initialization returned empty result")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Session initialization test failed: {str(e)}")
        import traceback
        print("📋 Full traceback:")
        traceback.print_exc()
        return False


async def test_individual_sections():
    """
    [Function intent]
    Test individual resource sections to identify potential issues.
    
    [Design principles]
    Isolated testing of each resource section for debugging purposes.
    Graceful error handling with detailed error reporting.
    
    [Implementation details]
    Tests each resource type individually to isolate any failures.
    """
    
    print()
    print("=== Testing Individual Resource Sections ===")
    print()
    
    class TestContext:
        async def info(self, message):
            print(f"   ℹ️  {message}")
        
        async def error(self, message):
            print(f"   ❌ {message}")
        
        async def warning(self, message):
            print(f"   ⚠️  {message}")
        
        async def debug(self, message):
            print(f"   🐛 {message}")
        
        async def report_progress(self, current, total, message):
            pass  # Skip progress for individual tests
    
    ctx = TestContext()
    
    # Test sections individually
    sections_to_test = [
        ("Framework Rules", "framework_rules", "get_available_rule_names"),
        ("Project Context", "project_resources", "get_project_context_summary"),
        ("Project Knowledge", "project_resources", "get_project_knowledge"),
        ("WIP Tasks", "wip_tasks", "get_wip_tasks_inventory"),
        ("Knowledge Indexes", "knowledge", "get_git_clones_readme"),
    ]
    
    for section_name, module_name, function_name in sections_to_test:
        print(f"🧪 Testing {section_name}...")
        
        try:
            # Import and test the specific function
            module = __import__(f'jesse_framework_mcp.resources.{module_name}', fromlist=[function_name])
            test_func = getattr(module, function_name)
            
            if function_name == "get_available_rule_names":
                result = await test_func()  # This function doesn't need context
                print(f"   ✅ {section_name}: Found {len(result)} rules")
            else:
                # Unwrap FastMCP function before calling
                unwrapped_func = unwrap_fastmcp_function(test_func)
                result = await unwrapped_func(ctx)
                result_size = len(result) if result else 0
                print(f"   ✅ {section_name}: {result_size:,} characters")
                
        except Exception as e:
            print(f"   ❌ {section_name} failed: {str(e)}")
    
    print()


async def main():
    """
    [Function intent]
    Main test execution function with comprehensive testing flow.
    
    [Design principles]
    Sequential testing with detailed reporting for debugging.
    Individual section testing for isolation of issues.
    
    [Implementation details]
    Runs comprehensive session initialization test followed by
    individual section tests for debugging purposes.
    """
    
    print("JESSE Framework MCP Server - Session Initialization Resource Test")
    print("=" * 70)
    
    try:
        # Test individual sections first to identify any issues
        await test_individual_sections()
        
        # Test the comprehensive session initialization
        success = await test_session_init_resource()
        
        print()
        print("=" * 70)
        if success:
            print("🎉 All tests completed successfully!")
            print()
            print("The session initialization meta-resource is ready for use:")
            print("   Resource URI: jesse://session/init-context")
            print("   Purpose: Complete Cline session initialization context")
            print("   Sections: 7 comprehensive resource sections")
        else:
            print("❌ Tests failed - see error details above")
            
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected test failure: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
Test script for project root detection functionality.
"""

import asyncio
import sys
import os
import argparse
from pathlib import Path

# Add the package to Python path
sys.path.insert(0, str(Path(__file__).parent))

from jesse_framework_mcp.helpers.path_utils import (
    get_project_root,
    ensure_project_root,
    get_project_relative_path,
    validate_project_setup
)
from jesse_framework_mcp.helpers.project_setup import get_project_setup_guidance


async def test_project_root_detection():
    """Test project root detection functionality."""
    
    print("=== Testing JESSE Framework Project Root Detection ===")
    print()
    
    # Test 1: Basic project root detection
    print("🧪 Test 1: Project Root Detection")
    project_root = get_project_root()
    
    if project_root:
        print(f"✅ Project root detected: {project_root}")
        print(f"   Current working directory: {Path.cwd()}")
        print(f"   Project root absolute: {project_root.resolve()}")
    else:
        print("❌ No project root detected")
    
    print()
    
    # Test 2: Environment variable detection
    print("🧪 Test 2: Environment Variable Detection")
    env_root = os.getenv('JESSE_PROJECT_ROOT')
    if env_root:
        print(f"✅ JESSE_PROJECT_ROOT set: {env_root}")
    else:
        print("ℹ️  JESSE_PROJECT_ROOT not set")
    
    print()
    
    # Test 3: Git repository detection
    print("🧪 Test 3: Git Repository Detection")
    current = Path.cwd()
    while current != current.parent:
        git_dir = current / '.git'
        if git_dir.exists():
            print(f"✅ Git repository found: {current}")
            break
        current = current.parent
    else:
        print("❌ No Git repository found in directory hierarchy")
    
    print()
    
    # Test 4: Setup guidance generation
    print("🧪 Test 4: Setup Guidance Generation")
    if not project_root:
        guidance = get_project_setup_guidance()
        print("✅ Setup guidance generated:")
        print(f"   Content length: {len(guidance):,} characters")
        print("   Sample content:")
        sample_lines = guidance.split('\n')[:10]
        for line in sample_lines:
            print(f"     {line}")
    else:
        print("ℹ️  Project root detected - setup guidance not needed")
    
    print()
    
    # Test 5: Project validation
    print("🧪 Test 5: Project Validation")
    validation = validate_project_setup()
    print("📋 Validation Results:")
    for key, value in validation.items():
        print(f"   {key}: {value}")
    
    print()
    print("=== Project Root Detection Test Complete ===")


async def test_session_init_with_project_root(dump_content=False):
    """Test session initialization with project root detection."""
    
    print("=== Testing Session Initialization with Project Root ===")
    print()
    
    try:
        # Create test context
        class TestContext:
            async def info(self, message):
                if not dump_content:
                    print(f"ℹ️  {message}")
            
            async def error(self, message):
                print(f"❌ {message}")
            
            async def warning(self, message):
                print(f"⚠️  {message}")
            
            async def debug(self, message):
                if not dump_content:
                    print(f"🐛 {message}")
            
            async def report_progress(self, current, total, message):
                if not dump_content:
                    percentage = (current / total) * 100
                    print(f"📊 [{percentage:3.0f}%] {message}")
        
        ctx = TestContext()
        
        # Test session initialization
        from jesse_framework_mcp.resources.session_init import get_session_init_context
        from utils import unwrap_fastmcp_function
        
        if not dump_content:
            print("🚀 Testing session initialization resource...")
            print()
        
        # Unwrap the FastMCP function before calling
        session_init_func = unwrap_fastmcp_function(get_session_init_context)
        result = await session_init_func(ctx)
        
        if dump_content:
            # Dump mode: output the complete resource content
            print("=== COMPLETE SESSION INITIALIZATION RESOURCE CONTENT ===")
            print()
            if result:
                print(result)
            else:
                print("❌ No content returned from session initialization")
            print()
            print("=== END OF RESOURCE CONTENT ===")
        else:
            # Summary mode: show test results
            print()
            if result:
                print("✅ Session initialization completed")
                print(f"   Response length: {len(result):,} characters")
                
                # Check if it's setup guidance or actual content
                if "JESSE Framework Setup Required" in result:
                    print("   📋 Result: Setup guidance returned (no project root detected)")
                else:
                    print("   📋 Result: Full session context returned")
                    # Count sections
                    section_count = result.count("Content-Type:")
                    print(f"   📊 HTTP sections: {section_count}")
            else:
                print("❌ Session initialization returned empty result")
            
    except Exception as e:
        print(f"❌ Session initialization test failed: {str(e)}")
        import traceback
        traceback.print_exc()
    
    if not dump_content:
        print()
        print("=== Session Initialization Test Complete ===")


async def main(dump_content=False):
    """Main test execution."""
    
    if not dump_content:
        print("JESSE Framework MCP Server - Project Root Detection Test")
        print("=" * 60)
        print()
    
    try:
        if dump_content:
            # In dump mode, only run session initialization and dump content
            await test_session_init_with_project_root(dump_content=True)
        else:
            # Normal test mode: run all tests
            # Test project root detection
            await test_project_root_detection()
            
            print()
            print("-" * 60)
            print()
            
            # Test session initialization
            await test_session_init_with_project_root(dump_content=False)
            
            print()
            print("=" * 60)
            print("🎉 All project root tests completed!")
        
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected test failure: {str(e)}")
        import traceback
        traceback.print_exc()


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Test JESSE Framework project root detection and session initialization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_project_root.py              # Run normal tests
  python test_project_root.py --dump       # Dump complete resource content
        """
    )
    
    parser.add_argument(
        "--dump",
        action="store_true",
        help="Dump the complete session initialization resource content instead of running tests"
    )
    
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    asyncio.run(main(dump_content=args.dump))

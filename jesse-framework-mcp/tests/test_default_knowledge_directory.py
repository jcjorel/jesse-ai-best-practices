#!/usr/bin/env python3
"""
Test script to verify that IndexingConfig now defaults to {PROJECT_ROOT}/.knowledge/ 
for knowledge_output_directory when not explicitly specified.
"""

import sys
from pathlib import Path

# Add the package to the path so we can import from it
sys.path.insert(0, str(Path(__file__).parent.parent))

from jesse_framework_mcp.knowledge_bases.models.indexing_config import IndexingConfig
from jesse_framework_mcp.helpers.path_utils import get_project_root


def test_default_knowledge_directory():
    """Test that knowledge_output_directory defaults to {PROJECT_ROOT}/.knowledge/"""
    print("=== Testing Default Knowledge Directory ===")
    
    # Test 1: Default behavior (should set to PROJECT_ROOT/.knowledge)
    print("Test 1: Default behavior")
    config = IndexingConfig()
    
    expected_project_root = get_project_root()
    if expected_project_root:
        expected_knowledge_dir = expected_project_root / '.knowledge'
        print(f"Expected: {expected_knowledge_dir}")
        print(f"Actual: {config.knowledge_output_directory}")
        
        if config.knowledge_output_directory == expected_knowledge_dir:
            print("✅ Test 1 PASSED: Default correctly set to PROJECT_ROOT/.knowledge/")
        else:
            print("❌ Test 1 FAILED: Default not set correctly")
            return False
    else:
        print("⚠️ Test 1 SKIPPED: Could not detect project root")
        if config.knowledge_output_directory is None:
            print("✅ Fallback behavior working correctly (None when project root not detected)")
        else:
            print("❌ Fallback behavior failed")
            return False
    
    # Test 2: Explicit specification (should override default)
    print("\nTest 2: Explicit specification")
    custom_path = Path("/tmp/custom_knowledge")
    config2 = IndexingConfig(knowledge_output_directory=custom_path)
    
    print(f"Expected: {custom_path}")
    print(f"Actual: {config2.knowledge_output_directory}")
    
    if config2.knowledge_output_directory == custom_path:
        print("✅ Test 2 PASSED: Explicit specification overrides default")
    else:
        print("❌ Test 2 FAILED: Explicit specification not working")
        return False
    
    # Test 3: Verify the configuration serializes correctly
    print("\nTest 3: Serialization")
    config_dict = config.to_dict()
    knowledge_dir_str = config_dict.get('knowledge_output_directory')
    
    if expected_project_root and knowledge_dir_str:
        expected_str = str(expected_project_root / '.knowledge')
        print(f"Expected serialized: {expected_str}")
        print(f"Actual serialized: {knowledge_dir_str}")
        
        if knowledge_dir_str == expected_str:
            print("✅ Test 3 PASSED: Serialization working correctly")
        else:
            print("❌ Test 3 FAILED: Serialization not working")
            return False
    else:
        print("⚠️ Test 3 SKIPPED: No project root or serialization is None")
    
    print("\n🎉 All tests passed! Default knowledge directory is working correctly.")
    return True


def test_project_root_integration():
    """Test that project root detection is working"""
    print("\n=== Testing Project Root Integration ===")
    
    project_root = get_project_root()
    if project_root:
        print(f"✅ Project root detected: {project_root}")
        print(f"Expected knowledge directory: {project_root / '.knowledge'}")
        return True
    else:
        print("❌ Project root detection failed")
        print("This may indicate an issue with the test environment")
        return False


if __name__ == "__main__":
    print("Testing IndexingConfig default knowledge_output_directory behavior")
    print("=" * 60)
    
    success = True
    
    # Test project root detection
    if not test_project_root_integration():
        success = False
    
    # Test default knowledge directory
    if not test_default_knowledge_directory():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED")
        print("✅ Default knowledge_output_directory is working correctly")
        print("✅ Knowledge files will be stored in {PROJECT_ROOT}/.knowledge/ by default")
    else:
        print("❌ SOME TESTS FAILED")
        print("💥 Issues detected with default knowledge directory configuration")
    
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Test script to verify project-base indexing business rule implementation.
Tests that knowledge files are stored in {PROJECT_ROOT}/.knowledge/project-base/ 
with directory structure mirroring when enable_project_base_indexing=True.
"""

import sys
import tempfile
import shutil
from pathlib import Path

# Add the package to the path so we can import from it
sys.path.insert(0, str(Path(__file__).parent.parent))

from jesse_framework_mcp.knowledge_bases.indexing.knowledge_builder import KnowledgeBuilder
from jesse_framework_mcp.knowledge_bases.models.indexing_config import IndexingConfig


def test_project_base_indexing_path_rule():
    """Test that project-base indexing uses correct directory structure"""
    print("=== Testing Project-Base Indexing Business Rule ===")
    
    # Create temporary directories for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        knowledge_dir = temp_path / ".knowledge"
        source_root = temp_path / "project"
        test_directory = source_root / "src" / "components"
        
        # Create test directory structure
        test_directory.mkdir(parents=True)
        
        print(f"Test environment: {temp_path}")
        print(f"Source root: {source_root}")
        print(f"Test directory: {test_directory}")
        print(f"Knowledge directory: {knowledge_dir}")
        
        # Test 1: With project-base indexing enabled
        print("\n--- Test 1: handler_type='project-base' ---")
        from jesse_framework_mcp.knowledge_bases.models.indexing_config import OutputConfig
        
        output_config = OutputConfig(knowledge_output_directory=knowledge_dir)
        
        config_with_project_base = IndexingConfig(
            handler_type="project-base",
            description="Test configuration with project-base indexing",
            output_config=output_config
        )
        
        builder = KnowledgeBuilder(config_with_project_base)
        knowledge_path = builder._get_knowledge_file_path(test_directory, source_root)
        
        expected_path = knowledge_dir / "project-base" / "src" / "components" / "components_kb.md"
        print(f"Expected: {expected_path}")
        print(f"Actual:   {knowledge_path}")
        
        if knowledge_path == expected_path:
            print("✅ Test 1 PASSED: Project-base indexing uses project-base/ subdirectory with structure mirroring")
        else:
            print("❌ Test 1 FAILED: Project-base indexing path incorrect")
            assert False, "Project-base indexing path incorrect"
        
        # Test 2: With git-clones handler type (should still use project-base/ - no backward compatibility)
        print("\n--- Test 2: handler_type='git-clones' (still uses project-base/) ---")
        
        output_config2 = OutputConfig(knowledge_output_directory=knowledge_dir)
        
        config_without_project_base = IndexingConfig(
            handler_type="git-clones",
            description="Test configuration with git-clones handler",
            output_config=output_config2
        )
        
        builder2 = KnowledgeBuilder(config_without_project_base)
        knowledge_path2 = builder2._get_knowledge_file_path(test_directory, source_root)
        
        expected_path2 = knowledge_dir / "project-base" / "src" / "components" / "components_kb.md"
        print(f"Expected: {expected_path2}")
        print(f"Actual:   {knowledge_path2}")
        
        if knowledge_path2 == expected_path2:
            print("✅ Test 2 PASSED: System always uses project-base/ subdirectory (no backward compatibility)")
        else:
            print("❌ Test 2 FAILED: System should always use project-base/ subdirectory")
            assert False, "System should always use project-base/ subdirectory"
        
        # Test 3: Verify different directory levels with project-base
        print("\n--- Test 3: Multi-level directory structure ---")
        deep_directory = source_root / "src" / "components" / "ui" / "buttons"
        deep_path = builder._get_knowledge_file_path(deep_directory, source_root)
        
        expected_deep_path = knowledge_dir / "project-base" / "src" / "components" / "ui" / "buttons" / "buttons_kb.md"
        print(f"Expected: {expected_deep_path}")
        print(f"Actual:   {deep_path}")
        
        if deep_path == expected_deep_path:
            print("✅ Test 3 PASSED: Multi-level directory structure preserved in project-base/")
        else:
            print("❌ Test 3 FAILED: Multi-level structure not preserved correctly")
            assert False, "Multi-level structure not preserved correctly"
        
        # Test 4: Fallback behavior when relative path calculation fails
        print("\n--- Test 4: Fallback behavior ---")
        unrelated_directory = Path("/some/unrelated/path")
        fallback_path = builder._get_knowledge_file_path(unrelated_directory, source_root)
        
        expected_fallback = knowledge_dir / "project-base" / "path_kb.md"
        print(f"Expected fallback: {expected_fallback}")
        print(f"Actual fallback:   {fallback_path}")
        
        if fallback_path == expected_fallback:
            print("✅ Test 4 PASSED: Fallback behavior works correctly with project-base/")
        else:
            print("❌ Test 4 FAILED: Fallback behavior incorrect")
            assert False, "Fallback behavior incorrect"
        
        # Test 5: Flat structure when no source_root provided
        print("\n--- Test 5: Flat structure (no source_root) ---")
        flat_path = builder._get_knowledge_file_path(test_directory, None)
        
        expected_flat = knowledge_dir / "project-base" / "components_kb.md"
        print(f"Expected flat: {expected_flat}")
        print(f"Actual flat:   {flat_path}")
        
        if flat_path == expected_flat:
            print("✅ Test 5 PASSED: Flat structure works correctly with project-base/")
        else:
            print("❌ Test 5 FAILED: Flat structure incorrect")
            assert False, "Flat structure incorrect"
        
        print("\n🎉 All project-base indexing business rule tests passed!")


def test_business_rule_configuration_detection():
    """Test that the configuration properly detects project-base vs regular indexing"""
    print("\n=== Testing Configuration Detection ===")
    
    # Test default configuration
    default_config = IndexingConfig()
    print(f"Default handler_type: {default_config.handler_type}")
    
    # Test explicit configuration
    project_base_config = IndexingConfig(handler_type="project-base")
    regular_config = IndexingConfig(handler_type="git-clones")
    
    print(f"Explicit project-base: {project_base_config.handler_type}")
    print(f"Explicit git-clones: {regular_config.handler_type}")
    
    if (project_base_config.handler_type == "project-base" and 
        regular_config.handler_type == "git-clones"):
        print("✅ Configuration detection works correctly")
    else:
        print("❌ Configuration detection failed")
        assert False, "Configuration detection failed"


def test_mandatory_project_base_subdirectory():
    """Test that project-base/ subdirectory is now mandatory regardless of configuration"""
    print("\n=== Testing Mandatory Project-Base Subdirectory ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        knowledge_dir = temp_path / ".knowledge"
        source_root = temp_path / "project"
        test_directory = source_root / "src"
        
        test_directory.mkdir(parents=True)
        
        # Test with project-base indexing enabled
        from jesse_framework_mcp.knowledge_bases.models.indexing_config import OutputConfig
        
        output_config3 = OutputConfig(knowledge_output_directory=knowledge_dir)
        
        project_base_config = IndexingConfig(
            handler_type="project-base",
            description="Test configuration for mandatory project-base test",
            output_config=output_config3
        )
        
        builder_project_base = KnowledgeBuilder(project_base_config)
        project_base_path = builder_project_base._get_knowledge_file_path(test_directory, source_root)
        
        # Test with git-clones indexing (should still use project-base/)
        output_config4 = OutputConfig(knowledge_output_directory=knowledge_dir)
        
        regular_config = IndexingConfig(
            handler_type="git-clones",
            description="Test configuration for mandatory project-base test with git-clones",
            output_config=output_config4
        )
        
        builder_regular = KnowledgeBuilder(regular_config)
        regular_path = builder_regular._get_knowledge_file_path(test_directory, source_root)
        
        print(f"Project-base enabled path:  {project_base_path}")
        print(f"Project-base disabled path: {regular_path}")
        
        expected_project_base = knowledge_dir / "project-base" / "src" / "src_kb.md"
        expected_regular = knowledge_dir / "project-base" / "src" / "src_kb.md"  # Should also use project-base/
        
        if (project_base_path == expected_project_base and 
            regular_path == expected_regular and
            project_base_path == regular_path):  # Should be the same now
            print("✅ Mandatory project-base subdirectory works correctly")
            print("  - Both configurations use project-base/ subdirectory")
            print("  - No backward compatibility - project-base/ is mandatory")
            print("  - Configuration flag is ignored for path resolution")
        else:
            print("❌ Mandatory project-base subdirectory failed")
            print(f"  Expected both paths to be: {expected_project_base}")
            assert False, "Mandatory project-base subdirectory failed"


if __name__ == "__main__":
    print("Testing Project-Base Indexing Business Rule Implementation")
    print("=" * 65)
    
    success = True
    
    # Test the main business rule implementation
    if not test_project_base_indexing_path_rule():
        success = False
    
    # Test configuration detection
    if not test_business_rule_configuration_detection():
        success = False
    
    # Test mandatory project-base subdirectory
    if not test_mandatory_project_base_subdirectory():
        success = False
    
    print("\n" + "=" * 65)
    if success:
        print("🎉 ALL BUSINESS RULE TESTS PASSED")
        print("✅ Mandatory project-base indexing business rule correctly implemented")
        print("✅ Knowledge files always stored in {PROJECT_ROOT}/.knowledge/project-base/")
        print("✅ Directory structure mirroring works within project-base/")
        print("✅ No backward compatibility - project-base/ subdirectory is mandatory")
    else:
        print("❌ SOME BUSINESS RULE TESTS FAILED")
        print("💥 Project-base indexing business rule needs fixes")
    
    sys.exit(0 if success else 1)

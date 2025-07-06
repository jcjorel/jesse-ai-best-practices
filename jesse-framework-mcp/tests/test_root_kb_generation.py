#!/usr/bin/env python3
"""
Focused test for root_kb.md generation fix.

This test specifically verifies that the hierarchical indexer generates root_kb.md
for handler root directories instead of {directory_name}_kb.md.
"""

import asyncio
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# Import the indexing system components
from jesse_framework_mcp.knowledge_bases.indexing.knowledge_builder import KnowledgeBuilder
from jesse_framework_mcp.knowledge_bases.models.indexing_config import IndexingConfig
from jesse_framework_mcp.knowledge_bases.models.knowledge_context import DirectoryContext, FileContext, ProcessingStatus


class MockContext:
    """Simple mock for testing without actual LLM calls."""
    
    def __init__(self):
        self.messages = []
    
    async def info(self, message: str) -> None:
        self.messages.append(f"INFO: {message}")
        print(f"INFO: {message}")
    
    async def debug(self, message: str) -> None:
        self.messages.append(f"DEBUG: {message}")
        print(f"DEBUG: {message}")
    
    async def warning(self, message: str) -> None:
        self.messages.append(f"WARNING: {message}")
        print(f"WARNING: {message}")
    
    async def error(self, message: str) -> None:
        self.messages.append(f"ERROR: {message}")
        print(f"ERROR: {message}")


async def test_root_kb_filename_generation():
    """
    Test that knowledge file paths are generated correctly for root directories.
    Specifically tests that root directories get root_kb.md instead of {directory_name}_kb.md.
    """
    print("=== Testing root_kb.md Filename Generation ===")
    
    # Create a temporary test environment
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test directory structure
        project_root = temp_path / "test_project"
        knowledge_dir = temp_path / "knowledge"
        project_root.mkdir()
        knowledge_dir.mkdir()
        
        # Create a simple test file
        test_file = project_root / "test.txt"
        test_file.write_text("This is a test file.")
        
        print(f"Test project root: {project_root}")
        print(f"Knowledge output directory: {knowledge_dir}")
        
        # Create minimal config for testing
        config_dict = {
            "handler_type": "project-base",
            "file_processing": {
                "max_file_size": 1024,
                "batch_size": 1,
                "max_concurrent_operations": 1
            },
            "content_filtering": {
                "excluded_extensions": [],
                "excluded_directories": []
            },
            "llm_config": {
                "llm_model": "claude-4-sonnet",
                "temperature": 0.3,
                "max_tokens": 1000
            },
            "change_detection": {
                "indexing_mode": "full_kb_rebuild",
                "timestamp_tolerance_seconds": 2
            },
            "error_handling": {
                "max_retries": 1,
                "retry_delay_seconds": 0.1,
                "continue_on_file_errors": True
            },
            "output_config": {
                "knowledge_output_directory": str(knowledge_dir)
            },
            "debug_config": {
                "debug_mode": False,
                "debug_output_directory": None,
                "enable_llm_replay": False
            }
        }
        
        config = IndexingConfig.from_dict(config_dict)
        knowledge_builder = KnowledgeBuilder(config)
        
        # Test 1: Project root directory (source_root == directory_path)
        print("\n--- Test 1: Project Root Directory ---")
        root_kb_path = knowledge_builder._get_knowledge_file_path(project_root, project_root)
        expected_root_path = knowledge_dir / "project-base" / "root_kb.md"
        
        print(f"Generated path: {root_kb_path}")
        print(f"Expected path: {expected_root_path}")
        
        if root_kb_path == expected_root_path:
            print("✅ PASS: Project root generates root_kb.md")
        else:
            print("❌ FAIL: Project root should generate root_kb.md")
            return False
        
        # Test 2: Regular subdirectory
        print("\n--- Test 2: Regular Subdirectory ---")
        subdir = project_root / "subdir"
        subdir.mkdir()
        
        subdir_kb_path = knowledge_builder._get_knowledge_file_path(subdir, project_root)
        expected_subdir_path = knowledge_dir / "project-base" / "subdir" / "subdir_kb.md"
        
        print(f"Generated path: {subdir_kb_path}")
        print(f"Expected path: {expected_subdir_path}")
        
        if subdir_kb_path == expected_subdir_path:
            print("✅ PASS: Subdirectory generates {directory_name}_kb.md")
        else:
            print("❌ FAIL: Subdirectory should generate {directory_name}_kb.md")
            return False
        
        # Test 3: Git clone .kb directory (simulated)
        print("\n--- Test 3: Git Clone .kb Directory ---")
        git_clone_kb_dir = temp_path / "some_repo.kb"
        git_clone_kb_dir.mkdir()
        
        git_clone_kb_path = knowledge_builder._get_knowledge_file_path(git_clone_kb_dir, None)
        expected_git_clone_path = knowledge_dir / "project-base" / "root_kb.md"
        
        print(f"Generated path: {git_clone_kb_path}")
        print(f"Expected path: {expected_git_clone_path}")
        
        if git_clone_kb_path.name == "root_kb.md":
            print("✅ PASS: .kb directory generates root_kb.md")
        else:
            print("❌ FAIL: .kb directory should generate root_kb.md")
            return False
        
        # Test 4: Root detection logic
        print("\n--- Test 4: Root Detection Logic ---")
        
        # Test project root detection
        is_project_root = knowledge_builder._is_handler_root_directory(project_root, project_root)
        print(f"Project root detection: {is_project_root}")
        if not is_project_root:
            print("❌ FAIL: Project root should be detected as root directory")
            return False
        else:
            print("✅ PASS: Project root correctly detected as root directory")
        
        # Test subdirectory detection (should NOT be root)
        is_subdir_root = knowledge_builder._is_handler_root_directory(subdir, project_root)
        print(f"Subdirectory root detection: {is_subdir_root}")
        if is_subdir_root:
            print("❌ FAIL: Subdirectory should NOT be detected as root directory")
            return False
        else:
            print("✅ PASS: Subdirectory correctly NOT detected as root directory")
        
        # Test .kb directory detection
        is_kb_root = knowledge_builder._is_handler_root_directory(git_clone_kb_dir, None)
        print(f".kb directory root detection: {is_kb_root}")
        if not is_kb_root:
            print("❌ FAIL: .kb directory should be detected as root directory")
            return False
        else:
            print("✅ PASS: .kb directory correctly detected as root directory")
        
        print("\n=== ALL TESTS PASSED ===")
        print("✅ Root KB filename generation is working correctly")
        print("✅ The fix should generate root_kb.md for handler root directories")
        
        return True


async def main():
    """Main test runner."""
    print("Root KB Generation Test")
    print("=" * 50)
    
    try:
        success = await test_root_kb_filename_generation()
        
        if success:
            print("\n🎉 SUCCESS: Root KB generation fix is working correctly!")
            print("The missing global summary issue should be resolved.")
            return True
        else:
            print("\n❌ FAILURE: Root KB generation has issues")
            return False
        
    except Exception as e:
        print(f"\n🚨 TEST ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Run the test
    result = asyncio.run(main())
    exit(0 if result else 1)

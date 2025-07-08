#!/usr/bin/env python3
"""
Focused test for root_kb.md generation fix.

This test specifically verifies that the hierarchical indexer generates root_kb.md
for handler root directories instead of {directory_name}_kb.md.

NOTE: As of 2025-07-07, path generation was moved from KnowledgeBuilder to handlers.
This test now verifies the handler-based path generation architecture.
"""

import asyncio
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# Import the indexing system components
from jesse_framework_mcp.knowledge_bases.indexing.special_handlers import ProjectBaseHandler, GitCloneHandler
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
    
    Tests the handler-based architecture where each handler type controls its own path generation.
    """
    print("=== Testing root_kb.md Filename Generation (Handler Architecture) ===")
    
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
        
        # Test 1: Project-base handler - root directory path generation
        print("\n--- Test 1: Project-base Handler Root Directory ---")
        project_handler = ProjectBaseHandler(config)
        
        root_kb_path = project_handler.get_knowledge_path(project_root, project_root)
        expected_root_path = knowledge_dir / "project-base" / "root_kb.md"
        
        print(f"Generated path: {root_kb_path}")
        print(f"Expected path: {expected_root_path}")
        
        if root_kb_path == expected_root_path:
            print("✅ PASS: Project-base handler root generates root_kb.md")
        else:
            print("❌ FAIL: Project-base handler root should generate root_kb.md")
            return False
        
        # Test 2: Project-base handler - regular subdirectory
        print("\n--- Test 2: Project-base Handler Subdirectory ---")
        subdir = project_root / "subdir"
        subdir.mkdir()
        
        subdir_kb_path = project_handler.get_knowledge_path(subdir, project_root)
        expected_subdir_path = knowledge_dir / "project-base" / "subdir_kb.md"
        
        print(f"Generated path: {subdir_kb_path}")
        print(f"Expected path: {expected_subdir_path}")
        
        if subdir_kb_path == expected_subdir_path:
            print("✅ PASS: Project-base handler subdirectory generates {directory_name}_kb.md")
        else:
            print("❌ FAIL: Project-base handler subdirectory should generate {directory_name}_kb.md")
            return False
        
        # Test 3: Git-clone handler path generation
        print("\n--- Test 3: Git-clone Handler ---")
        git_clone_config = IndexingConfig.from_dict({
            **config_dict,
            "handler_type": "git-clone"
        })
        git_clone_handler = GitCloneHandler(git_clone_config)
        
        # Simulate git clone directory
        git_clone_root = temp_path / "some_repo"
        git_clone_root.mkdir()
        
        git_clone_kb_path = git_clone_handler.get_knowledge_path(git_clone_root, git_clone_root)
        
        print(f"Generated path: {git_clone_kb_path}")
        print(f"Path filename: {git_clone_kb_path.name}")
        
        # Git-clone handler should generate repo_name_kb.md format
        expected_filename = "some_repo_kb.md"
        if git_clone_kb_path.name == expected_filename:
            print("✅ PASS: Git-clone handler generates {repo_name}_kb.md")
        else:
            print(f"❌ FAIL: Git-clone handler should generate {expected_filename}, got {git_clone_kb_path.name}")
            return False
        
        # Test 4: Handler type detection
        print("\n--- Test 4: Handler Type Verification ---")
        
        # Verify project-base handler type
        if project_handler.get_handler_type() == "project-base":
            print("✅ PASS: Project-base handler type correctly identified")
        else:
            print("❌ FAIL: Project-base handler type incorrect")
            return False
        
        # Verify git-clone handler type
        if git_clone_handler.get_handler_type() == "git-clone":
            print("✅ PASS: Git-clone handler type correctly identified")
        else:
            print("❌ FAIL: Git-clone handler type incorrect")
            return False
        
        print("\n=== ALL TESTS PASSED ===")
        print("✅ Handler-based KB filename generation is working correctly")
        print("✅ Each handler type controls its own path generation logic")
        
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

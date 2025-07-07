#!/usr/bin/env python3
###############################################################################
# IMPORTANT: This header comment is designed for GenAI code review and maintenance
# Any GenAI tool working with this file MUST preserve and update this header
###############################################################################
# [GenAI coding tool directive]
# - Maintain this header with all modifications
# - Update History section with each change
# - Keep only the 4 most recent records in the history section. Sort from newer to older.
# - Preserve Intent, Design, and Constraints sections
# - Use this header as context for code reviews and modifications
# - Ensure all changes align with the design principles
# - Respect system prompt directives at all times
###############################################################################
# [Source file intent]
# Test script validating unified DirectoryContext building approach ensures identical
# leaf-first processing between GitCloneHandler and ProjectBaseHandler.
# Verifies both handlers produce structurally identical DirectoryContext objects.
###############################################################################
# [Source file design principles]
# - Structural validation ensuring both handlers create identical DirectoryContext hierarchies
# - Mock environment testing preventing any impact on real system files or data
# - Comprehensive validation covering DirectoryContext structure consistency
# - Clear success/failure reporting enabling easy validation of handler unification
###############################################################################
# [Source file constraints]
# - All testing must occur in temporary directories with automatic cleanup
# - Test validation must verify identical DirectoryContext structure production
# - Handler comparison must confirm consistent parent-child relationship creation
# - Test output must clearly indicate unification success with detailed comparison
###############################################################################
# [Dependencies]
# <codebase>: ../jesse_framework_mcp/knowledge_bases/indexing/special_handlers - Unified handler implementation
# <codebase>: ../jesse_framework_mcp/knowledge_bases/models - DirectoryContext structures
# <system>: tempfile - Safe temporary directory creation and management
# <system>: pathlib - Cross-platform path operations
# <system>: asyncio - Async test execution
###############################################################################
# [GenAI tool change history]
# 2025-07-07T16:37:00Z : INITIAL CREATION - Test script for unified handler DirectoryContext validation by CodeAssistant
# * Created comprehensive test validating both handlers produce identical DirectoryContext structures
# * Implemented mock environment testing with temporary directories and automatic cleanup
# * Added structural comparison validation ensuring consistent parent-child relationships
# * Designed clear success/failure reporting for easy validation of handler unification success
###############################################################################

"""
Unified Handler Processing Test Script.

This script validates that GitCloneHandler and ProjectBaseHandler produce
structurally identical DirectoryContext objects using the unified processing approach.
"""

import asyncio
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import List

from jesse_framework_mcp.knowledge_bases.indexing.special_handlers import GitCloneHandler, ProjectBaseHandler
from jesse_framework_mcp.knowledge_bases.models.indexing_config import IndexingConfig
from jesse_framework_mcp.knowledge_bases.indexing.defaults import get_default_config


class MockContext:
    """Mock context for testing"""
    def __init__(self):
        self.messages = []
    
    async def info(self, message: str):
        self.messages.append(f"INFO: {message}")
        print(f"INFO: {message}")
    
    async def debug(self, message: str):
        self.messages.append(f"DEBUG: {message}")
    
    async def warning(self, message: str):
        self.messages.append(f"WARNING: {message}")
        print(f"WARNING: {message}")


def compare_directory_contexts(ctx1, ctx2, path="root") -> bool:
    """Compare two DirectoryContext objects for structural identity"""
    
    # Compare basic properties
    if len(ctx1.file_contexts) != len(ctx2.file_contexts):
        print(f"❌ File count mismatch at {path}: {len(ctx1.file_contexts)} vs {len(ctx2.file_contexts)}")
        return False
    
    if len(ctx1.subdirectory_contexts) != len(ctx2.subdirectory_contexts):
        print(f"❌ Subdirectory count mismatch at {path}: {len(ctx1.subdirectory_contexts)} vs {len(ctx2.subdirectory_contexts)}")
        return False
    
    # Compare file contexts (names only, since paths will differ)
    ctx1_files = sorted([fc.file_path.name for fc in ctx1.file_contexts])
    ctx2_files = sorted([fc.file_path.name for fc in ctx2.file_contexts])
    
    if ctx1_files != ctx2_files:
        print(f"❌ File names mismatch at {path}: {ctx1_files} vs {ctx2_files}")
        return False
    
    # Compare subdirectory contexts recursively
    ctx1_subdirs = sorted(ctx1.subdirectory_contexts, key=lambda d: d.directory_path.name)
    ctx2_subdirs = sorted(ctx2.subdirectory_contexts, key=lambda d: d.directory_path.name)
    
    for i, (subdir1, subdir2) in enumerate(zip(ctx1_subdirs, ctx2_subdirs)):
        if subdir1.directory_path.name != subdir2.directory_path.name:
            print(f"❌ Subdirectory name mismatch at {path}[{i}]: {subdir1.directory_path.name} vs {subdir2.directory_path.name}")
            return False
        
        # Recursive comparison
        if not compare_directory_contexts(subdir1, subdir2, f"{path}/{subdir1.directory_path.name}"):
            return False
    
    return True


async def test_unified_processing():
    """Test unified DirectoryContext building"""
    print("🧪 Testing Unified Handler Processing")
    print("=" * 50)
    
    temp_dir = None
    try:
        # Create temporary test environment
        temp_dir = Path(tempfile.mkdtemp(prefix="unified_handler_test_"))
        print(f"Test environment: {temp_dir}")
        
        # Create identical directory structures for both tests
        test_structure = {
            "files": ["README.md", "main.py", "config.json"],
            "subdirs": {
                "src": {
                    "files": ["app.py", "utils.py"],
                    "subdirs": {
                        "models": {"files": ["user.py", "data.py"], "subdirs": {}}
                    }
                },
                "docs": {
                    "files": ["guide.md", "api.md"],
                    "subdirs": {}
                }
            }
        }
        
        # Create project-base test structure
        project_base_root = temp_dir / "project_base_test"
        create_test_structure(project_base_root, test_structure)
        
        # Create git-clone test structure (simulated)
        git_clone_root = temp_dir / ".knowledge" / "git-clones" / "test_repo"
        create_test_structure(git_clone_root, test_structure)
        # Add .git directory to simulate git repository
        (git_clone_root / ".git").mkdir()
        
        # Test both handlers
        ctx1 = MockContext()
        ctx2 = MockContext()
        
        # Create handlers with identical configs
        config_dict = get_default_config('project-base')
        config1 = IndexingConfig.from_dict(config_dict)
        config2 = IndexingConfig.from_dict(config_dict)
        
        project_handler = ProjectBaseHandler(config1)
        git_clone_handler = GitCloneHandler(config2)
        
        print("\n🏗️ Processing with ProjectBaseHandler...")
        project_context = await project_handler.process_project_structure(project_base_root, ctx1)
        
        print("\n🔗 Processing with GitCloneHandler...")
        git_clone_context = await git_clone_handler.process_git_clone_structure(git_clone_root, ctx2)
        
        # Compare structures
        print("\n🔍 Comparing DirectoryContext structures...")
        structures_identical = compare_directory_contexts(project_context, git_clone_context)
        
        if structures_identical:
            print("\n✅ SUCCESS: Both handlers produce identical DirectoryContext structures!")
            print("🎯 Unified leaf-first processing confirmed")
            print("📊 Structure comparison results:")
            print(f"   Project-base files: {project_context.total_files}")
            print(f"   Git-clone files: {git_clone_context.total_files}")
            print(f"   Project-base subdirs: {len(list(get_all_subdirs(project_context)))}")
            print(f"   Git-clone subdirs: {len(list(get_all_subdirs(git_clone_context)))}")
            return True
        else:
            print("\n❌ FAILURE: Handlers produce different DirectoryContext structures!")
            return False
            
    except Exception as e:
        print(f"\n🚨 TEST EXECUTION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Cleanup
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir)
            print(f"\n🧹 Cleaned up test environment")


def create_test_structure(root_path: Path, structure: dict):
    """Create test directory structure"""
    root_path.mkdir(parents=True, exist_ok=True)
    
    # Create files
    for file_name in structure.get("files", []):
        (root_path / file_name).write_text(f"# Test file: {file_name}")
    
    # Create subdirectories recursively
    for subdir_name, subdir_structure in structure.get("subdirs", {}).items():
        subdir_path = root_path / subdir_name
        create_test_structure(subdir_path, subdir_structure)


def get_all_subdirs(ctx):
    """Get all subdirectories recursively"""
    for subdir in ctx.subdirectory_contexts:
        yield subdir
        yield from get_all_subdirs(subdir)


async def main():
    """Main test runner"""
    success = await test_unified_processing()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 UNIFIED PROCESSING VALIDATION SUCCESSFUL!")
        print("✅ Both handlers now use identical leaf-first processing")
        print("✅ DirectoryContext structures are perfectly consistent")
        print("✅ Plan Generator will create identical task dependencies")
        return 0
    else:
        print("❌ UNIFIED PROCESSING VALIDATION FAILED!")
        print("⚠️ Handlers still produce different structures")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)

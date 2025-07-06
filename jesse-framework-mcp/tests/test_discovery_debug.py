#!/usr/bin/env python3
"""
Debug test to investigate why discovery phase doesn't exclude directories properly.
"""

import asyncio
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock

from jesse_framework_mcp.knowledge_bases.indexing.hierarchical_indexer import HierarchicalIndexer
from jesse_framework_mcp.knowledge_bases.indexing.defaults import get_default_config
from jesse_framework_mcp.knowledge_bases.models.indexing_config import IndexingConfig


async def test_discovery_debug():
    """Debug test to understand discovery phase behavior with excluded directories."""
    print("=== Discovery Phase Debug Test ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create a realistic project structure
        project_root = temp_path / "test_project"
        project_root.mkdir()
        
        # Create directories that should be excluded
        (project_root / ".coding_assistant").mkdir()
        (project_root / ".knowledge").mkdir()
        (project_root / ".clinerules").mkdir()
        (project_root / "scratchpad").mkdir()
        
        # Create directories that should be included
        (project_root / "src").mkdir()
        (project_root / "docs").mkdir()
        
        # Create some files in each directory
        (project_root / ".coding_assistant" / "workspace.json").write_text('{"config": "data"}')
        (project_root / ".knowledge" / "kb.md").write_text("# Knowledge")
        (project_root / ".clinerules" / "rules.md").write_text("# Rules")
        (project_root / "scratchpad" / "notes.txt").write_text("Temp notes")
        (project_root / "src" / "main.py").write_text("print('hello')")
        (project_root / "docs" / "README.md").write_text("# Documentation")
        
        print(f"Created test project structure in: {project_root}")
        
        # Create configuration
        config_dict = get_default_config('project-base')
        config_dict['output_config']['knowledge_output_directory'] = str(temp_path / "knowledge")
        config = IndexingConfig.from_dict(config_dict)
        
        print(f"\nConfiguration loaded:")
        print(f"  Excluded directories: {sorted(config.excluded_directories)}")
        print(f"  Project-base exclusions: {sorted(config.project_base_exclusions or set())}")
        
        # Test individual directory exclusion logic
        print(f"\n=== Testing Individual Directory Exclusion ===")
        for dir_path in project_root.iterdir():
            if dir_path.is_dir():
                should_process = config.should_process_directory(dir_path)
                status = "✅ INCLUDE" if should_process else "🚫 EXCLUDE"
                print(f"  {status}: {dir_path.name}")
        
        # Create hierarchical indexer
        indexer = HierarchicalIndexer(config)
        ctx = AsyncMock()
        ctx.info = AsyncMock()
        ctx.debug = AsyncMock()
        ctx.warning = AsyncMock()
        ctx.error = AsyncMock()
        
        # Run discovery phase only
        print(f"\n=== Running Discovery Phase ===")
        root_context = await indexer._discover_directory_structure(project_root, ctx)
        
        # Analyze discovery results
        print(f"\n=== Discovery Results ===")
        print(f"Root directory: {root_context.directory_path}")
        print(f"Discovered subdirectories:")
        
        for subdir_context in root_context.subdirectory_contexts:
            print(f"  📁 {subdir_context.directory_path.name}: {len(subdir_context.file_contexts)} files")
        
        # Check if excluded directories were discovered
        discovered_names = {subdir.directory_path.name for subdir in root_context.subdirectory_contexts}
        excluded_expected = {'.coding_assistant', '.knowledge', '.clinerules', 'scratchpad'}
        included_expected = {'src', 'docs'}
        
        print(f"\n=== Analysis ===")
        print(f"Expected to exclude: {sorted(excluded_expected)}")
        print(f"Expected to include: {sorted(included_expected)}")
        print(f"Actually discovered: {sorted(discovered_names)}")
        
        # Check for problems
        wrongly_included = excluded_expected & discovered_names
        wrongly_excluded = included_expected - discovered_names
        
        if wrongly_included:
            print(f"❌ PROBLEM: These excluded directories were discovered: {sorted(wrongly_included)}")
        else:
            print(f"✅ GOOD: No excluded directories were discovered")
            
        if wrongly_excluded:
            print(f"❌ PROBLEM: These included directories were NOT discovered: {sorted(wrongly_excluded)}")
        else:
            print(f"✅ GOOD: All expected directories were discovered")
        
        # Print mock calls for debugging
        print(f"\n=== Mock Context Calls ===")
        print(f"Info calls: {len(ctx.info.call_args_list)}")
        for call in ctx.info.call_args_list:
            print(f"  INFO: {call[0][0]}")
        
        if ctx.warning.call_args_list:
            print(f"Warning calls: {len(ctx.warning.call_args_list)}")
            for call in ctx.warning.call_args_list:
                print(f"  WARNING: {call[0][0]}")
        
        if ctx.error.call_args_list:
            print(f"Error calls: {len(ctx.error.call_args_list)}")
            for call in ctx.error.call_args_list:
                print(f"  ERROR: {call[0][0]}")
        
        # Final determination
        discovery_working = len(wrongly_included) == 0 and len(wrongly_excluded) == 0
        
        print(f"\n=== RESULT ===")
        if discovery_working:
            print("🎉 DISCOVERY PHASE IS WORKING CORRECTLY")
            print("The issue must be elsewhere in the execution flow")
        else:
            print("❌ DISCOVERY PHASE HAS ISSUES")
            print("This is likely the root cause of the problem")
        
        return discovery_working


def main():
    """Run the discovery debug test."""
    print("Discovery Phase Debug Test")
    print("=" * 50)
    
    result = asyncio.run(test_discovery_debug())
    
    print("=" * 50)
    if result:
        print("✅ Discovery phase working correctly")
    else:
        print("❌ Discovery phase has issues")
    
    return result


if __name__ == "__main__":
    main()

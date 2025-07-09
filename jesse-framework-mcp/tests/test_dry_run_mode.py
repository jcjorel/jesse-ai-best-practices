#!/usr/bin/env python3
"""
Test for dry-run mode functionality in the JESSE Framework indexing system.

This test demonstrates the new dry-run mode that allows users to see what would be
executed without actually performing the expensive LLM calls and file operations.
"""

import asyncio
import tempfile
from pathlib import Path
from datetime import datetime

# Import the indexing system components
from jesse_framework_mcp.knowledge_bases.indexing.hierarchical_indexer import HierarchicalIndexer
from jesse_framework_mcp.knowledge_bases.models.indexing_config import IndexingConfig, DebugConfig
from jesse_framework_mcp.knowledge_bases.models.knowledge_context import ProcessingStatus
from jesse_framework_mcp.helpers.path_utils import ensure_project_root


class MockContext:
    """Mock FastMCP Context for dry-run testing."""
    
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


async def test_dry_run_mode():
    """
    Test the dry-run mode functionality.
    
    This test demonstrates:
    1. How to enable dry-run mode in configuration
    2. How the system runs discovery and planning phases
    3. How execution is skipped in dry-run mode
    4. What kind of information is provided in dry-run results
    """
    print("=== DRY-RUN MODE TEST ===")
    print("Testing dry-run functionality with discovery + planning only")
    
    # Create a temporary test directory with some files
    with tempfile.TemporaryDirectory() as temp_dir:
        test_root = Path(temp_dir)
        
        # Create some test files
        (test_root / "README.md").write_text("# Test Project\nThis is a test.")
        (test_root / "main.py").write_text("def main():\n    print('Hello, World!')")
        
        # Create a subdirectory with files
        sub_dir = test_root / "src"
        sub_dir.mkdir()
        (sub_dir / "module.py").write_text("class TestClass:\n    pass")
        (sub_dir / "utils.py").write_text("def helper():\n    return True")
        
        print(f"Created test directory: {test_root}")
        print(f"Test files: {list(test_root.rglob('*'))}")
        
        # Test 1: Regular mode (no dry-run)
        print(f"\n--- Test 1: Regular Mode (for comparison) ---")
        
        regular_config = IndexingConfig(
            handler_type="test-regular",
            debug_config=DebugConfig(
                debug_mode=True,
                dry_run=False  # Regular execution
            )
        )
        
        ctx_regular = MockContext()
        indexer_regular = HierarchicalIndexer(regular_config)
        
        start_time = datetime.now()
        try:
            result_regular = await indexer_regular.index_hierarchy(test_root, ctx_regular)
            end_time = datetime.now()
            
            print(f"✅ Regular mode completed in {(end_time - start_time).total_seconds():.2f}s")
            print(f"Status: {result_regular.overall_status}")
            print(f"Operation: {result_regular.current_operation}")
            print(f"Files discovered: {result_regular.processing_stats.total_files_discovered}")
            print(f"Directories discovered: {result_regular.processing_stats.total_directories_discovered}")
            
        except Exception as e:
            print(f"⚠️ Regular mode test failed (expected): {e}")
            print("This is expected if LLM components are not available")
        
        # Test 2: Dry-run mode
        print(f"\n--- Test 2: Dry-Run Mode ---")
        
        dry_run_config = IndexingConfig(
            handler_type="test-dry-run",
            debug_config=DebugConfig(
                debug_mode=True,
                dry_run=True  # Enable dry-run mode
            )
        )
        
        ctx_dry_run = MockContext()
        indexer_dry_run = HierarchicalIndexer(dry_run_config)
        
        start_time = datetime.now()
        result_dry_run = await indexer_dry_run.index_hierarchy(test_root, ctx_dry_run)
        end_time = datetime.now()
        
        print(f"✅ Dry-run mode completed in {(end_time - start_time).total_seconds():.2f}s")
        print(f"Status: {result_dry_run.overall_status}")
        print(f"Operation: {result_dry_run.current_operation}")
        
        # Analyze dry-run results
        stats = result_dry_run.processing_stats
        print(f"\n=== DRY-RUN RESULTS ===")
        print(f"Files discovered: {stats.total_files_discovered}")
        print(f"Directories discovered: {stats.total_directories_discovered}")
        print(f"Files processed: {stats.files_processed} (should be 0)")
        print(f"Directories processed: {stats.directories_processed} (should be 0)")
        
        # Check dry-run specific messages
        dry_run_messages = [err for err in stats.errors if err.startswith("DRY-RUN:")]
        print(f"\nDry-run information:")
        for msg in dry_run_messages:
            print(f"  {msg}")
        
        # Verify dry-run behavior
        assert result_dry_run.overall_status == ProcessingStatus.COMPLETED, "Dry-run should complete successfully"
        assert stats.files_processed == 0, "No files should be processed in dry-run"
        assert stats.directories_processed == 0, "No directories should be processed in dry-run"
        assert stats.total_files_discovered > 0, "Files should be discovered in dry-run"
        assert len(dry_run_messages) > 0, "Should have dry-run specific messages"
        
        # Check for key dry-run messages in context
        dry_run_context_messages = [msg for msg in ctx_dry_run.messages if "DRY-RUN MODE" in msg]
        assert len(dry_run_context_messages) > 0, "Should have dry-run mode messages in context"
        
        print(f"\n🎉 DRY-RUN MODE TEST: SUCCESS")
        print(f"✅ Discovery phase completed - found {stats.total_files_discovered} files")
        print(f"✅ Planning phase completed - execution plan generated")
        print(f"✅ Execution phase skipped - no LLM calls or file operations")
        print(f"✅ Dry-run completed successfully in {(end_time - start_time).total_seconds():.2f}s")
        
        return True


async def test_configuration_creation():
    """Test different ways to create dry-run configuration."""
    print(f"\n=== CONFIGURATION CREATION TEST ===")
    
    # Method 1: Direct configuration creation
    config1 = IndexingConfig(
        debug_config=DebugConfig(dry_run=True)
    )
    assert config1.dry_run == True, "Direct configuration should set dry_run"
    print("✅ Method 1: Direct DebugConfig creation")
    
    # Method 2: Using from_dict
    config_dict = {
        'debug_config': {
            'dry_run': True,
            'debug_mode': False
        }
    }
    config2 = IndexingConfig.from_dict(config_dict)
    assert config2.dry_run == True, "from_dict should set dry_run"
    print("✅ Method 2: from_dict configuration")
    
    # Method 3: Default value
    config3 = IndexingConfig()
    assert config3.dry_run == False, "Default dry_run should be False"
    print("✅ Method 3: Default configuration (dry_run=False)")
    
    # Method 4: Serialization round-trip
    config4_dict = config1.to_dict()
    assert config4_dict['debug_config']['dry_run'] == True, "Serialization should preserve dry_run"
    config4 = IndexingConfig.from_dict(config4_dict)
    assert config4.dry_run == True, "Deserialization should restore dry_run"
    print("✅ Method 4: Serialization round-trip")
    
    print("🎉 CONFIGURATION CREATION TEST: SUCCESS")
    return True


async def main():
    """Main test runner."""
    print("JESSE Framework Dry-Run Mode Test")
    print("=" * 50)
    
    try:
        # Test configuration creation
        await test_configuration_creation()
        
        # Test dry-run functionality
        await test_dry_run_mode()
        
        print(f"\n{'='*50}")
        print("🎉 ALL TESTS PASSED")
        print("✅ Dry-run mode is working correctly")
        print("✅ Configuration system supports dry-run flag")
        print("✅ Discovery and planning phases work without execution")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Run the test
    result = asyncio.run(main())
    exit(0 if result else 1)

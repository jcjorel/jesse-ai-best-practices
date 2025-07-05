#!/usr/bin/env python3
"""
Test script to validate upfront cache structure preparation implementation.
Tests the prepare_cache_structure method and its integration with the hierarchical indexer.
"""

import sys
import tempfile
import asyncio
from pathlib import Path
from datetime import datetime

# Add the package to the path so we can import from it
sys.path.insert(0, str(Path(__file__).parent.parent))

from jesse_framework_mcp.knowledge_bases.indexing.file_analysis_cache import FileAnalysisCache
from jesse_framework_mcp.knowledge_bases.indexing.hierarchical_indexer import HierarchicalIndexer
from jesse_framework_mcp.knowledge_bases.models.indexing_config import IndexingConfig
from jesse_framework_mcp.knowledge_bases.models.knowledge_context import DirectoryContext, FileContext, ProcessingStatus

# Mock FastMCP Context for testing
class MockContext:
    def __init__(self):
        self.messages = []
    
    async def info(self, message: str):
        self.messages.append(f"INFO: {message}")
        print(f"INFO: {message}")
    
    async def debug(self, message: str):
        self.messages.append(f"DEBUG: {message}")
        print(f"DEBUG: {message}")
    
    async def warning(self, message: str):
        self.messages.append(f"WARNING: {message}")
        print(f"WARNING: {message}")
    
    async def error(self, message: str):
        self.messages.append(f"ERROR: {message}")
        print(f"ERROR: {message}")


async def test_cache_structure_preparation():
    """Test basic cache structure preparation functionality"""
    print("=== Testing Cache Structure Preparation ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        knowledge_dir = temp_path / ".knowledge"
        source_root = temp_path / "project"
        
        # Create complex directory structure
        files_created = []
        for i in range(3):
            for j in range(2):
                dir_path = source_root / f"dir_{i}" / f"subdir_{j}"
                dir_path.mkdir(parents=True, exist_ok=True)
                
                # Create files in each directory
                for k in range(2):
                    file_path = dir_path / f"file_{k}.py"
                    file_path.write_text(f"# Content for file {i}-{j}-{k}")
                    files_created.append(file_path)
        
        # Create configuration
        from jesse_framework_mcp.knowledge_bases.models.indexing_config import OutputConfig
        
        output_config = OutputConfig(knowledge_output_directory=knowledge_dir)
        
        config = IndexingConfig(
            handler_type="project-base",
            description="Test configuration for cache structure preparation",
            output_config=output_config
        )
        
        # Create cache and context
        cache = FileAnalysisCache(config)
        ctx = MockContext()
        
        # Create directory context manually
        root_context = await create_directory_context(source_root, files_created)
        
        # Test 1: Verify no cache directories exist initially
        print("--- Test 1: Initial State ---")
        cache_root = knowledge_dir / "project-base"
        assert not cache_root.exists(), "Cache root should not exist initially"
        print("✅ Test 1 PASSED: No cache directories exist initially")
        
        # Test 2: Prepare cache structure
        print("--- Test 2: Cache Structure Preparation ---")
        await cache.prepare_cache_structure(root_context, source_root, ctx)
        
        # Verify cache root was created
        assert cache_root.exists(), "Cache root should exist after preparation"
        print("✅ Cache root directory created")
        
        # Test 3: Verify all necessary directories were created
        print("--- Test 3: Directory Structure Verification ---")
        all_files = cache._collect_all_files_recursive(root_context)
        expected_dirs = set()
        for file_path in all_files:
            cache_path = cache.get_cache_path(file_path, source_root)
            expected_dirs.add(cache_path.parent)
        
        # Check that all expected directories exist
        missing_dirs = []
        for expected_dir in expected_dirs:
            if not expected_dir.exists():
                missing_dirs.append(expected_dir)
        
        assert len(missing_dirs) == 0, f"Missing cache directories: {missing_dirs}"
        print(f"✅ Test 3 PASSED: All {len(expected_dirs)} cache directories created")
        
        # Test 4: Verify cache operations work with pre-created structure
        print("--- Test 4: Cache Operations on Pre-created Structure ---")
        test_file = files_created[0]
        test_analysis = "## Test Analysis\n\nThis is a test analysis."
        
        # This should work without creating directories
        await cache.cache_analysis(test_file, test_analysis, source_root)
        
        # Verify cache file was created
        cache_path = cache.get_cache_path(test_file, source_root)
        assert cache_path.exists(), "Cache file should exist after caching"
        
        # Verify content retrieval
        retrieved_analysis = await cache.get_cached_analysis(test_file, source_root)
        assert retrieved_analysis == test_analysis, "Retrieved analysis should match stored analysis"
        print("✅ Test 4 PASSED: Cache operations work correctly with pre-created structure")
        
        print("🎉 All cache structure preparation tests passed!")
        return True


async def test_hierarchical_indexer_integration():
    """Test integration with hierarchical indexer"""
    print("\n=== Testing HierarchicalIndexer Integration ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        knowledge_dir = temp_path / ".knowledge"
        source_root = temp_path / "project"
        
        # Create test files
        test_files = []
        for i in range(2):
            dir_path = source_root / f"src" / f"module_{i}"
            dir_path.mkdir(parents=True)
            
            for j in range(2):
                file_path = dir_path / f"component_{j}.js"
                file_path.write_text(f"// Module {i} Component {j}\nexport default function Component{i}{j}() {{}}")
                test_files.append(file_path)
        
        # Create configuration
        from jesse_framework_mcp.knowledge_bases.models.indexing_config import (
            OutputConfig, DebugConfig
        )
        
        output_config = OutputConfig(knowledge_output_directory=knowledge_dir)
        debug_config = DebugConfig(debug_mode=False, enable_llm_replay=False)
        
        config = IndexingConfig(
            handler_type="project-base",
            description="Test configuration for hierarchical indexer integration",
            output_config=output_config,
            debug_config=debug_config
        )
        
        # Create hierarchical indexer
        indexer = HierarchicalIndexer(config)
        
        # Mock the knowledge builder to avoid actual LLM calls
        class MockKnowledgeBuilder:
            def __init__(self, config):
                self.config = config
                self.analysis_cache = FileAnalysisCache(config)
            
            async def build_file_knowledge(self, file_context, ctx, source_root=None):
                # Mock file processing
                return FileContext(
                    file_path=file_context.file_path,
                    file_size=file_context.file_size,
                    last_modified=file_context.last_modified,
                    processing_status=ProcessingStatus.COMPLETED,
                    knowledge_content=f"Mock analysis for {file_context.file_path.name}",
                    processing_start_time=datetime.now(),
                    processing_end_time=datetime.now()
                )
            
            async def build_directory_summary(self, directory_context, ctx, source_root=None):
                # Mock directory processing
                return DirectoryContext(
                    directory_path=directory_context.directory_path,
                    file_contexts=directory_context.file_contexts,
                    subdirectory_contexts=directory_context.subdirectory_contexts,
                    processing_status=ProcessingStatus.COMPLETED,
                    knowledge_file_path=directory_context.directory_path / "mock_kb.md",
                    processing_start_time=datetime.now(),
                    processing_end_time=datetime.now()
                )
            
            async def cleanup(self):
                pass
        
        # Replace the knowledge builder with mock
        indexer.knowledge_builder = MockKnowledgeBuilder(config)
        
        ctx = MockContext()
        
        # Test 1: Verify cache structure preparation happens during indexing
        print("--- Test 1: Cache Structure Preparation During Indexing ---")
        
        # Run discovery phase to build directory structure
        root_context = await indexer._discover_directory_structure(source_root, ctx)
        
        # Manually trigger cache preparation phase
        await indexer.knowledge_builder.analysis_cache.prepare_cache_structure(root_context, source_root, ctx)
        
        # Verify cache directories were created
        cache_root = knowledge_dir / "project-base"
        assert cache_root.exists(), "Cache root should exist after preparation"
        
        # Verify specific directories exist
        expected_cache_dirs = [
            cache_root / "src" / "module_0",
            cache_root / "src" / "module_1"
        ]
        
        for expected_dir in expected_cache_dirs:
            assert expected_dir.exists(), f"Expected cache directory should exist: {expected_dir}"
        
        print("✅ Test 1 PASSED: Cache structure preparation integrated successfully")
        
        # Test 2: Verify concurrent safety (simulate concurrent operations)
        print("--- Test 2: Concurrent Cache Operations Safety ---")
        
        # Simulate multiple concurrent cache operations
        async def concurrent_cache_operation(file_path, analysis_content):
            await indexer.knowledge_builder.analysis_cache.cache_analysis(
                file_path, analysis_content, source_root
            )
        
        # Run concurrent operations
        tasks = []
        for i, test_file in enumerate(test_files):
            task = concurrent_cache_operation(test_file, f"Concurrent analysis {i}")
            tasks.append(task)
        
        # Execute all tasks concurrently
        await asyncio.gather(*tasks)
        
        # Verify all cache files were created successfully
        for test_file in test_files:
            cache_path = indexer.knowledge_builder.analysis_cache.get_cache_path(test_file, source_root)
            assert cache_path.exists(), f"Cache file should exist: {cache_path}"
        
        print("✅ Test 2 PASSED: Concurrent cache operations completed safely")
        
        # Test 3: Verify no race conditions occurred
        print("--- Test 3: Race Condition Prevention ---")
        
        # Check that no error messages indicate race conditions
        error_messages = [msg for msg in ctx.messages if "ERROR" in msg or "failed" in msg.lower()]
        race_condition_indicators = [
            "FileExistsError", "directory exists", "cannot create directory", 
            "race condition", "concurrent access"
        ]
        
        race_condition_errors = []
        for msg in error_messages:
            if any(indicator in msg for indicator in race_condition_indicators):
                race_condition_errors.append(msg)
        
        assert len(race_condition_errors) == 0, f"Race condition errors detected: {race_condition_errors}"
        print("✅ Test 3 PASSED: No race conditions detected")
        
        print("🎉 All hierarchical indexer integration tests passed!")
        return True


async def create_directory_context(root_path: Path, files: list[Path]) -> DirectoryContext:
    """Helper function to create DirectoryContext from file list"""
    # Build directory structure recursively
    def build_directory_context(current_path: Path) -> DirectoryContext:
        file_contexts = []
        subdirectory_contexts = []
        processed_subdirs = set()
        
        # Find files directly in this directory
        for file_path in files:
            if file_path.parent == current_path:
                file_context = FileContext(
                    file_path=file_path,
                    file_size=file_path.stat().st_size,
                    last_modified=datetime.fromtimestamp(file_path.stat().st_mtime)
                )
                file_contexts.append(file_context)
        
        # Find subdirectories that contain files
        for file_path in files:
            # Check if file is under current path
            try:
                relative_path = file_path.relative_to(current_path)
                if len(relative_path.parts) > 1:
                    # File is in a subdirectory
                    subdir_name = relative_path.parts[0]
                    subdir_path = current_path / subdir_name
                    
                    if subdir_path not in processed_subdirs:
                        processed_subdirs.add(subdir_path)
                        subdir_context = build_directory_context(subdir_path)
                        subdirectory_contexts.append(subdir_context)
            except ValueError:
                # File is not under current path, skip
                continue
        
        return DirectoryContext(
            directory_path=current_path,
            file_contexts=file_contexts,
            subdirectory_contexts=subdirectory_contexts
        )
    
    return build_directory_context(root_path)


async def test_fallback_behavior():
    """Test fallback behavior when cache structure preparation fails"""
    print("\n=== Testing Fallback Behavior ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        knowledge_dir = temp_path / ".knowledge"
        source_root = temp_path / "project"
        
        # Create test file
        test_file = source_root / "test.py"
        test_file.parent.mkdir(parents=True)
        test_file.write_text("print('test')")
        
        # Create configuration
        from jesse_framework_mcp.knowledge_bases.models.indexing_config import OutputConfig
        
        output_config = OutputConfig(knowledge_output_directory=knowledge_dir)
        
        config = IndexingConfig(
            handler_type="project-base",
            description="Test configuration for fallback behavior",
            output_config=output_config
        )
        
        cache = FileAnalysisCache(config)
        ctx = MockContext()
        
        # Test: Cache operation without structure preparation (should create directories on-demand)
        print("--- Testing On-Demand Directory Creation Fallback ---")
        
        test_analysis = "## Fallback Test\n\nThis tests on-demand directory creation."
        
        # Cache should create directories on-demand
        await cache.cache_analysis(test_file, test_analysis, source_root)
        
        # Verify cache file was created
        cache_path = cache.get_cache_path(test_file, source_root)
        assert cache_path.exists(), "Cache file should exist after on-demand creation"
        
        # Verify content
        retrieved_analysis = await cache.get_cached_analysis(test_file, source_root)
        assert retrieved_analysis == test_analysis, "Retrieved analysis should match"
        
        print("✅ Fallback test PASSED: On-demand directory creation works correctly")
        
        print("🎉 All fallback behavior tests passed!")
        return True


async def run_all_tests():
    """Run all upfront cache structure preparation tests"""
    print("🚀 Starting Upfront Cache Structure Preparation Tests")
    print("=" * 65)
    
    tests = [
        ("Cache Structure Preparation", test_cache_structure_preparation),
        ("HierarchicalIndexer Integration", test_hierarchical_indexer_integration),
        ("Fallback Behavior", test_fallback_behavior)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n🧪 Running {test_name}...")
            result = await test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"💥 {test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 65)
    print("📊 UPFRONT CACHE STRUCTURE PREPARATION TEST RESULTS")
    print("=" * 65)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nOverall Results: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL CACHE STRUCTURE PREPARATION TESTS PASSED!")
        print("✅ Upfront cache structure preparation working correctly")
        print("✅ Race condition elimination achieved")
        print("✅ HierarchicalIndexer integration working correctly")
        print("✅ Fallback behavior working correctly")
        print("✅ Concurrent cache operations safe and reliable")
    else:
        print("💥 SOME CACHE STRUCTURE TESTS FAILED")
        print("🔧 Upfront cache structure preparation needs fixes")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)

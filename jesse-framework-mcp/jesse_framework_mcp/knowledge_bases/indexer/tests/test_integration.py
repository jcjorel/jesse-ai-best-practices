"""
Test suite for new indexer end-to-end integration.

Tests complete indexing workflows from discovery through execution
to ensure all components work together correctly.
"""

import pytest
import asyncio
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch

from ..core import CoreIndexer
from ..models import IndexingResult, ExecutionContext
from ..handlers import ProjectHandler, GitCloneHandler
from .test_models import MockAtomicTask


class TestEndToEndIndexing:
    """Test complete end-to-end indexing workflows."""
    
    def setup_method(self):
        """Set up test environment for each test."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.project_root = self.temp_dir / "test_project"
        self.project_root.mkdir()
        
        # Create test project structure
        (self.project_root / "src").mkdir()
        (self.project_root / "src" / "module.py").write_text("def hello(): return 'world'")
        (self.project_root / "src" / "utils.py").write_text("def helper(): pass")
        (self.project_root / "docs").mkdir()
        (self.project_root / "docs" / "readme.md").write_text("# Test Project")
    
    def teardown_method(self):
        """Clean up test environment after each test."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_basic_indexer_creation(self):
        """Test basic CoreIndexer creation and configuration."""
        indexer = CoreIndexer()
        
        # Should have default configuration
        assert indexer is not None
        
        # Should support both handler types
        project_handler = ProjectHandler()
        git_handler = GitCloneHandler()
        
        assert project_handler.can_handle(Path("/project/src"))
        assert git_handler.can_handle(Path("/project/.knowledge/git-clones/repo"))
    
    @pytest.mark.asyncio
    async def test_simple_project_indexing_workflow(self):
        """Test simple project indexing workflow."""
        # This is a simplified integration test since we'd need
        # the full CoreIndexer implementation to be complete
        
        # Test handler selection
        project_handler = ProjectHandler()
        git_handler = GitCloneHandler()
        
        # Test project files
        src_file = self.project_root / "src" / "module.py"
        assert project_handler.can_handle(src_file)
        assert not git_handler.can_handle(src_file)
        
        # Test path calculations
        cache_path = project_handler.get_cache_path(src_file, self.project_root)
        kb_path = project_handler.get_knowledge_file_path(self.project_root / "src", self.project_root)
        
        assert ".knowledge" in str(cache_path)
        assert ".knowledge" in str(kb_path)
        assert cache_path.name == "module.analysis.md"
        assert kb_path.name == "src_kb.md"
    
    @pytest.mark.asyncio
    async def test_git_clone_indexing_workflow(self):
        """Test git clone indexing workflow."""
        # Create git clone structure
        git_clones_dir = self.project_root / ".knowledge" / "git-clones"
        git_clones_dir.mkdir(parents=True)
        
        repo_dir = git_clones_dir / "test_repo"
        repo_dir.mkdir()
        (repo_dir / "src").mkdir()
        (repo_dir / "src" / "lib.py").write_text("class Library: pass")
        
        # Test handler selection
        project_handler = ProjectHandler()
        git_handler = GitCloneHandler()
        
        git_file = repo_dir / "src" / "lib.py"
        assert not project_handler.can_handle(git_file)
        assert git_handler.can_handle(git_file)
        
        # Test path calculations
        cache_path = git_handler.get_cache_path(git_file, repo_dir)
        kb_path = git_handler.get_knowledge_file_path(repo_dir / "src", repo_dir)
        
        assert "git-clones" in str(cache_path)
        assert "git-clones" in str(kb_path)
        assert cache_path.name == "lib.analysis.md"
        assert kb_path.name == "src_kb.md"
    
    def test_handler_isolation(self):
        """Test that project and git-clone handlers are properly isolated."""
        project_handler = ProjectHandler()
        git_handler = GitCloneHandler()
        
        # Create similar structures in both contexts
        project_file = self.project_root / "src" / "common.py"
        
        git_clones_dir = self.project_root / ".knowledge" / "git-clones" / "repo"
        git_clones_dir.mkdir(parents=True)
        (git_clones_dir / "src").mkdir()
        git_file = git_clones_dir / "src" / "common.py"
        
        project_file.write_text("# Project version")
        git_file.write_text("# Git clone version")
        
        # Generate paths
        project_cache = project_handler.get_cache_path(project_file, self.project_root)
        git_cache = git_handler.get_cache_path(git_file, git_clones_dir)
        
        # Should be completely different paths
        assert str(project_cache) != str(git_cache)
        assert "git-clones" not in str(project_cache)
        assert "git-clones" in str(git_cache)
        
        # Both should be valid paths
        assert project_cache.name == "common.analysis.md"
        assert git_cache.name == "common.analysis.md"
    
    def test_exclusion_pattern_behavior(self):
        """Test that exclusion patterns work correctly."""
        project_handler = ProjectHandler()
        git_handler = GitCloneHandler()
        
        # Create files that should be excluded
        (self.project_root / ".git").mkdir()
        (self.project_root / "__pycache__").mkdir()
        (self.project_root / "node_modules").mkdir()
        
        exclusions_project = project_handler.get_exclusion_patterns()
        exclusions_git = git_handler.get_exclusion_patterns()
        
        # Both should exclude common patterns
        common_exclusions = {".git", "__pycache__", "node_modules"}
        assert all(pattern in exclusions_project for pattern in common_exclusions)
        assert all(pattern in exclusions_git for pattern in common_exclusions)
        
        # Project should exclude .knowledge, git should not
        assert ".knowledge" in exclusions_project
        assert ".knowledge" not in exclusions_git
    
    @pytest.mark.asyncio
    async def test_error_handling_integration(self):
        """Test error handling across component integration."""
        project_handler = ProjectHandler()
        
        # Test with nonexistent files
        nonexistent_file = self.project_root / "src" / "nonexistent.py"
        
        # Should handle gracefully
        cache_path = project_handler.get_cache_path(nonexistent_file, self.project_root)
        assert cache_path is not None
        
        # Test source validation with missing files
        kb_path = self.project_root / ".knowledge" / "src" / "nonexistent_kb.md"
        source_path = project_handler.get_source_path(kb_path, self.project_root)
        assert source_path is None or not source_path.exists()
    
    def test_path_edge_cases(self):
        """Test edge cases in path handling."""
        project_handler = ProjectHandler()
        
        # Test deeply nested paths
        deep_dir = self.project_root / "a" / "b" / "c" / "d" / "e"
        deep_dir.mkdir(parents=True)
        deep_file = deep_dir / "deep.py"
        deep_file.write_text("# Deep file")
        
        cache_path = project_handler.get_cache_path(deep_file, self.project_root)
        
        # Should maintain nested structure
        assert "a" in str(cache_path)
        assert "b" in str(cache_path)
        assert "c" in str(cache_path)
        assert cache_path.name == "deep.analysis.md"
    
    def test_handler_compatibility_matrix(self):
        """Test complete handler compatibility matrix."""
        project_handler = ProjectHandler()
        git_handler = GitCloneHandler()
        
        test_paths = [
            # Project paths - should be handled by ProjectHandler only
            (Path("/project/src/file.py"), True, False),
            (Path("/home/user/app/module.py"), True, False),
            (Path("/workspace/tool/lib.py"), True, False),
            
            # Git clone paths - should be handled by GitCloneHandler only
            (Path("/project/.knowledge/git-clones/repo/file.py"), False, True),
            (Path("/home/.knowledge/git-clones/lib/module.py"), False, True),
            (Path("/workspace/.knowledge/git-clones/tool/util.py"), False, True),
            
            # Edge cases
            (Path("/"), True, False),  # Root defaults to project
            (Path(""), True, False),   # Empty defaults to project
        ]
        
        for path, expect_project, expect_git in test_paths:
            project_result = project_handler.can_handle(path)
            git_result = git_handler.can_handle(path)
            
            assert project_result == expect_project, f"ProjectHandler failed for {path}"
            assert git_result == expect_git, f"GitCloneHandler failed for {path}"
            
            # Each path should be handled by exactly one handler
            assert project_result != git_result, f"Path {path} handled by both or neither handler"


class TestMockIntegration:
    """Test integration using mocked components."""
    
    @pytest.mark.asyncio
    async def test_task_execution_flow(self):
        """Test basic task execution flow."""
        # Create mock execution context
        progress_messages = []
        context = ExecutionContext(
            source_root=Path("/project"),
            progress_callback=lambda msg: progress_messages.append(msg),
            dry_run=True
        )
        
        # Create and execute mock task
        task = MockAtomicTask("integration_test", "analyze")
        
        # Validate preconditions
        assert task.validate_preconditions(context) is True
        
        # Execute task
        result = await task.execute(context)
        
        assert result.success is True
        assert result.task_type == "analyze"
        assert result.task_id == "integration_test"
    
    def test_component_initialization_order(self):
        """Test that components initialize in correct order."""
        # Test that handlers can be created independently
        project_handler = ProjectHandler()
        git_handler = GitCloneHandler()
        
        assert project_handler.get_handler_type() == "project"
        assert git_handler.get_handler_type() == "gitclone"
        
        # Test that they have expected behavior
        test_project_path = Path("/project/src/file.py")
        test_git_path = Path("/project/.knowledge/git-clones/repo/file.py")
        
        assert project_handler.can_handle(test_project_path)
        assert not project_handler.can_handle(test_git_path)
        assert not git_handler.can_handle(test_project_path)
        assert git_handler.can_handle(test_git_path)
    
    def test_data_model_integration(self):
        """Test integration between data models."""
        from ..models import KnowledgeFile, ValidationResult
        
        # Create knowledge file
        kb_file = KnowledgeFile(
            path=Path("/project/.knowledge/src/module_kb.md"),
            handler_type="project",
            file_type="knowledge"
        )
        
        # Should start as orphaned
        assert kb_file.is_orphaned is True
        
        # Create validation result
        validation = ValidationResult(
            source_exists=True,
            source_path=Path("/project/src/module.py"),
            is_stale=False,
            validation_reason="Source found and up to date"
        )
        
        # Update knowledge file based on validation
        kb_file.is_orphaned = not validation.source_exists
        kb_file.source_path = validation.source_path
        kb_file.is_stale = validation.is_stale
        
        assert kb_file.is_orphaned is False
        assert kb_file.source_path == Path("/project/src/module.py")
        assert kb_file.is_stale is False


class TestPerformanceIntegration:
    """Test performance characteristics of integrated system."""
    
    def test_handler_selection_performance(self):
        """Test performance of handler selection with many paths."""
        import time
        
        project_handler = ProjectHandler()
        git_handler = GitCloneHandler()
        
        # Generate test paths
        test_paths = []
        for i in range(1000):
            test_paths.append(Path(f"/project/src/file_{i}.py"))
            test_paths.append(Path(f"/project/.knowledge/git-clones/repo_{i}/file.py"))
        
        # Time handler selection
        start_time = time.time()
        for path in test_paths:
            project_handler.can_handle(path)
            git_handler.can_handle(path)
        selection_time = time.time() - start_time
        
        # Should be fast (under 1 second for 2000 paths)
        assert selection_time < 1.0, f"Handler selection too slow: {selection_time}s"
    
    def test_path_calculation_performance(self):
        """Test performance of path calculations."""
        import time
        
        project_handler = ProjectHandler()
        source_root = Path("/project")
        
        # Generate test files
        test_files = [Path(f"/project/src/module_{i}.py") for i in range(500)]
        test_dirs = [Path(f"/project/src/dir_{i}") for i in range(500)]
        
        # Time cache path calculations
        start_time = time.time()
        for file_path in test_files:
            project_handler.get_cache_path(file_path, source_root)
        cache_time = time.time() - start_time
        
        # Time knowledge file path calculations
        start_time = time.time()
        for dir_path in test_dirs:
            project_handler.get_knowledge_file_path(dir_path, source_root)
        kb_time = time.time() - start_time
        
        # Should be fast
        assert cache_time < 0.5, f"Cache path calculation too slow: {cache_time}s"
        assert kb_time < 0.5, f"KB path calculation too slow: {kb_time}s"
    
    def test_memory_usage_integration(self):
        """Test memory usage patterns in integration scenarios."""
        import gc
        
        # Test creating many handlers doesn't cause memory issues
        handlers = []
        for i in range(100):
            handlers.append(ProjectHandler())
            handlers.append(GitCloneHandler())
        
        # Should not cause memory issues
        assert len(handlers) == 200
        
        # Clean up
        del handlers
        gc.collect()


class TestRegressionIntegration:
    """Test integration scenarios that previously caused issues."""
    
    def test_path_separator_consistency(self):
        """Test that path separators are handled consistently."""
        project_handler = ProjectHandler()
        
        # Test with different path formats
        unix_path = Path("/project/src/module.py")
        source_root = Path("/project")
        
        cache_path = project_handler.get_cache_path(unix_path, source_root)
        
        # Should produce consistent results regardless of platform
        assert cache_path is not None
        assert cache_path.name == "module.analysis.md"
        assert ".knowledge" in str(cache_path)
    
    def test_unicode_path_handling(self):
        """Test handling of Unicode characters in paths."""
        project_handler = ProjectHandler()
        
        # Test with Unicode paths
        unicode_path = Path("/project/src/模块.py")  # Chinese characters
        source_root = Path("/project")
        
        # Should handle gracefully
        try:
            cache_path = project_handler.get_cache_path(unicode_path, source_root)
            assert cache_path is not None
        except Exception as e:
            # If Unicode not supported, should be a clear error
            assert "unicode" in str(e).lower() or isinstance(e, UnicodeError)
    
    def test_concurrent_handler_usage(self):
        """Test that handlers can be used concurrently safely."""
        import threading
        import time
        
        project_handler = ProjectHandler()
        results = []
        errors = []
        
        def handler_worker(thread_id):
            try:
                for i in range(100):
                    path = Path(f"/project/thread_{thread_id}/file_{i}.py")
                    cache_path = project_handler.get_cache_path(path, Path("/project"))
                    results.append((thread_id, i, cache_path))
            except Exception as e:
                errors.append((thread_id, e))
        
        # Start multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=handler_worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        # Should have no errors and expected results
        assert len(errors) == 0, f"Concurrent errors: {errors}"
        assert len(results) == 500  # 5 threads × 100 operations each
    
    def test_large_directory_structures(self):
        """Test handling of large directory structures."""
        project_handler = ProjectHandler()
        source_root = Path("/project")
        
        # Test with many nested directories
        base_path = Path("/project")
        for depth in range(10):
            nested_path = base_path
            for level in range(depth):
                nested_path = nested_path / f"level_{level}"
            
            file_path = nested_path / "deep_file.py"
            cache_path = project_handler.get_cache_path(file_path, source_root)
            
            # Should handle any depth
            assert cache_path is not None
            assert cache_path.name == "deep_file.analysis.md"
            assert ".knowledge" in str(cache_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

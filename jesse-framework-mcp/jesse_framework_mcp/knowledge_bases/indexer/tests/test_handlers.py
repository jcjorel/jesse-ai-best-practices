"""
Test suite for new indexer handlers.

Tests handler interface and concrete implementations to ensure proper
path calculations, exclusion patterns, and handler type detection.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import tempfile

from ..handlers import ProjectHandler, GitCloneHandler


class TestProjectHandler:
    """Test ProjectHandler implementation."""
    
    def test_handler_type(self):
        """Test ProjectHandler returns correct type."""
        handler = ProjectHandler()
        assert handler.get_handler_type() == "project"
    
    def test_can_handle_project_paths(self):
        """Test ProjectHandler can handle regular project paths."""
        handler = ProjectHandler()
        
        # Regular project paths should be handled
        assert handler.can_handle(Path("/project/src")) is True
        assert handler.can_handle(Path("/home/user/myproject")) is True
        assert handler.can_handle(Path("/workspace/app")) is True
    
    def test_cannot_handle_git_clone_paths(self):
        """Test ProjectHandler cannot handle git clone paths."""
        handler = ProjectHandler()
        
        # Git clone paths should not be handled
        assert handler.can_handle(Path("/project/.knowledge/git-clones/repo")) is False
        assert handler.can_handle(Path("/home/.knowledge/git-clones/myrepo")) is False
    
    def test_exclusion_patterns(self):
        """Test ProjectHandler exclusion patterns."""
        handler = ProjectHandler()
        
        # Should exclude standard patterns
        exclusions = handler.get_exclusion_patterns()
        
        expected_patterns = {".git", ".knowledge", "__pycache__", "node_modules", ".pytest_cache"}
        assert all(pattern in exclusions for pattern in expected_patterns)
    
    def test_cache_path_calculation(self):
        """Test ProjectHandler cache path calculation."""
        handler = ProjectHandler()
        
        file_path = Path("/project/src/module.py")
        source_root = Path("/project")
        
        cache_path = handler.get_cache_path(file_path, source_root)
        
        # Should create cache path in .knowledge directory
        assert cache_path.parts[-3:] == (".knowledge", "src", "module.analysis.md")
        assert str(cache_path).startswith(str(source_root))
    
    def test_knowledge_file_path_calculation(self):
        """Test ProjectHandler knowledge file path calculation.""" 
        handler = ProjectHandler()
        
        directory_path = Path("/project/src")
        source_root = Path("/project")
        
        kb_path = handler.get_knowledge_file_path(directory_path, source_root)
        
        # Should create KB path in .knowledge directory
        assert kb_path.parts[-2:] == ("src", "src_kb.md")
        assert str(kb_path).startswith(str(source_root))
    
    def test_source_path_validation(self):
        """Test ProjectHandler source path validation."""
        handler = ProjectHandler()
        
        kb_path = Path("/project/.knowledge/src/module_kb.md")
        source_root = Path("/project")
        
        # Should find corresponding source file
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = True
            
            source_path = handler.get_source_path(kb_path, source_root)
            assert source_path == Path("/project/src/module.py")
    
    def test_missing_source_path_validation(self):
        """Test ProjectHandler with missing source."""
        handler = ProjectHandler()
        
        kb_path = Path("/project/.knowledge/src/missing_kb.md")
        source_root = Path("/project")
        
        # Should return None for missing source
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = False
            
            source_path = handler.get_source_path(kb_path, source_root)
            assert source_path is None


class TestGitCloneHandler:
    """Test GitCloneHandler implementation."""
    
    def test_handler_type(self):
        """Test GitCloneHandler returns correct type."""
        handler = GitCloneHandler()
        assert handler.get_handler_type() == "gitclone"
    
    def test_can_handle_git_clone_paths(self):
        """Test GitCloneHandler can handle git clone paths."""
        handler = GitCloneHandler()
        
        # Git clone paths should be handled
        assert handler.can_handle(Path("/project/.knowledge/git-clones/repo")) is True
        assert handler.can_handle(Path("/home/.knowledge/git-clones/myrepo/src")) is True
    
    def test_cannot_handle_regular_project_paths(self):
        """Test GitCloneHandler cannot handle regular project paths."""
        handler = GitCloneHandler()
        
        # Regular project paths should not be handled
        assert handler.can_handle(Path("/project/src")) is False
        assert handler.can_handle(Path("/home/user/myproject")) is False
    
    def test_exclusion_patterns(self):
        """Test GitCloneHandler exclusion patterns."""
        handler = GitCloneHandler()
        
        # Should exclude standard patterns plus git-clone specific ones
        exclusions = handler.get_exclusion_patterns()
        
        expected_patterns = {".git", "__pycache__", "node_modules", ".pytest_cache"}
        assert all(pattern in exclusions for pattern in expected_patterns)
        
        # Should NOT exclude .knowledge in git clones
        assert ".knowledge" not in exclusions
    
    def test_cache_path_calculation(self):
        """Test GitCloneHandler cache path calculation."""
        handler = GitCloneHandler()
        
        file_path = Path("/project/.knowledge/git-clones/repo/src/module.py")
        source_root = Path("/project/.knowledge/git-clones/repo")
        
        cache_path = handler.get_cache_path(file_path, source_root)
        
        # Should create cache path within the git clone
        assert "git-clones" in str(cache_path)
        assert cache_path.name == "module.analysis.md"
    
    def test_knowledge_file_path_calculation(self):
        """Test GitCloneHandler knowledge file path calculation."""
        handler = GitCloneHandler()
        
        directory_path = Path("/project/.knowledge/git-clones/repo/src")
        source_root = Path("/project/.knowledge/git-clones/repo")
        
        kb_path = handler.get_knowledge_file_path(directory_path, source_root)
        
        # Should create KB path within the git clone
        assert "git-clones" in str(kb_path)
        assert kb_path.name == "src_kb.md"
    
    def test_source_path_validation(self):
        """Test GitCloneHandler source path validation."""
        handler = GitCloneHandler()
        
        kb_path = Path("/project/.knowledge/git-clones/repo/src/module_kb.md")
        source_root = Path("/project/.knowledge/git-clones/repo")
        
        # Should find corresponding source file
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = True
            
            source_path = handler.get_source_path(kb_path, source_root)
            assert source_path == Path("/project/.knowledge/git-clones/repo/src/module.py")


class TestHandlerIntegration:
    """Test integration between different handlers."""
    
    def test_handler_selection_for_different_paths(self):
        """Test that correct handlers are selected for different path types."""
        project_handler = ProjectHandler()
        git_handler = GitCloneHandler()
        
        # Test various path scenarios
        test_cases = [
            (Path("/project/src"), project_handler, git_handler, True, False),
            (Path("/home/user/app"), project_handler, git_handler, True, False),
            (Path("/project/.knowledge/git-clones/repo"), project_handler, git_handler, False, True),
            (Path("/home/.knowledge/git-clones/myrepo/src"), project_handler, git_handler, False, True),
        ]
        
        for path, proj_handler, git_handler, expect_project, expect_git in test_cases:
            assert proj_handler.can_handle(path) == expect_project
            assert git_handler.can_handle(path) == expect_git
    
    def test_complementary_handler_coverage(self):
        """Test that handlers provide complementary coverage."""
        project_handler = ProjectHandler()
        git_handler = GitCloneHandler()
        
        test_paths = [
            Path("/project/src/file.py"),
            Path("/project/.knowledge/git-clones/repo/file.py"),
            Path("/home/user/app/module.py"),
            Path("/workspace/.knowledge/git-clones/lib/util.py")
        ]
        
        for path in test_paths:
            # Each path should be handled by exactly one handler
            project_can_handle = project_handler.can_handle(path)
            git_can_handle = git_handler.can_handle(path)
            
            assert project_can_handle != git_can_handle, f"Path {path} should be handled by exactly one handler"
    
    def test_handler_path_isolation(self):
        """Test that handlers generate isolated paths."""
        project_handler = ProjectHandler()
        git_handler = GitCloneHandler()
        
        # Same relative path in different contexts
        project_file = Path("/project/src/module.py")
        git_file = Path("/project/.knowledge/git-clones/repo/src/module.py")
        
        project_root = Path("/project")
        git_root = Path("/project/.knowledge/git-clones/repo")
        
        # Cache paths should be isolated
        project_cache = project_handler.get_cache_path(project_file, project_root)
        git_cache = git_handler.get_cache_path(git_file, git_root)
        
        assert project_cache != git_cache
        assert "git-clones" not in str(project_cache)
        assert "git-clones" in str(git_cache)
        
        # Knowledge file paths should be isolated
        project_dir = Path("/project/src")
        git_dir = Path("/project/.knowledge/git-clones/repo/src")
        
        project_kb = project_handler.get_knowledge_file_path(project_dir, project_root)
        git_kb = git_handler.get_knowledge_file_path(git_dir, git_root)
        
        assert project_kb != git_kb
        assert "git-clones" not in str(project_kb)
        assert "git-clones" in str(git_kb)


class TestHandlerEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_empty_path_handling(self):
        """Test handlers with empty or invalid paths."""
        project_handler = ProjectHandler()
        git_handler = GitCloneHandler()
        
        # Test with empty path
        empty_path = Path()
        assert project_handler.can_handle(empty_path) is True  # Default to project
        assert git_handler.can_handle(empty_path) is False
    
    def test_root_path_handling(self):
        """Test handlers with root paths."""
        project_handler = ProjectHandler()
        git_handler = GitCloneHandler()
        
        root_path = Path("/")
        assert project_handler.can_handle(root_path) is True
        assert git_handler.can_handle(root_path) is False
    
    def test_nested_git_clone_paths(self):
        """Test handlers with deeply nested git clone paths."""
        git_handler = GitCloneHandler()
        
        nested_path = Path("/project/.knowledge/git-clones/repo/deep/nested/dir/file.py")
        assert git_handler.can_handle(nested_path) is True
        
        source_root = Path("/project/.knowledge/git-clones/repo")
        cache_path = git_handler.get_cache_path(nested_path, source_root)
        
        # Should maintain nested structure in cache
        assert "deep" in str(cache_path)
        assert "nested" in str(cache_path)
        assert cache_path.name == "file.analysis.md"
    
    def test_case_sensitivity(self):
        """Test handlers with case variations (if applicable)."""
        project_handler = ProjectHandler()
        
        # Test exclusion pattern case sensitivity
        exclusions = project_handler.get_exclusion_patterns()
        test_path = Path("/project/NODE_MODULES/package")
        
        # Should handle case variations appropriately for the platform
        # This test depends on filesystem case sensitivity
        pass  # Implementation depends on platform-specific requirements
    
    def test_symlink_handling(self):
        """Test handlers with symbolic links.""" 
        project_handler = ProjectHandler()
        
        # Test with potential symbolic link paths
        symlink_path = Path("/project/link-to-src/module.py")
        source_root = Path("/project")
        
        # Should handle symlinks gracefully
        cache_path = project_handler.get_cache_path(symlink_path, source_root)
        assert cache_path is not None
        assert ".knowledge" in str(cache_path)
    
    def test_very_long_paths(self):
        """Test handlers with very long file paths."""
        project_handler = ProjectHandler()
        
        # Create a very long path
        long_components = ["very_long_directory_name_that_exceeds_normal_limits"] * 10
        long_path = Path("/project") / Path(*long_components) / "file.py"
        source_root = Path("/project")
        
        # Should handle long paths without errors
        try:
            cache_path = project_handler.get_cache_path(long_path, source_root)
            assert cache_path is not None
        except Exception as e:
            # If path is too long for filesystem, should handle gracefully
            assert "path too long" in str(e).lower() or isinstance(e, OSError)


class TestHandlerPerformance:
    """Test handler performance characteristics."""
    
    def test_can_handle_performance(self):
        """Test that can_handle method is efficient."""
        import time
        
        project_handler = ProjectHandler()
        git_handler = GitCloneHandler()
        
        test_paths = [
            Path(f"/project/src/module_{i}.py") for i in range(1000)
        ] + [
            Path(f"/project/.knowledge/git-clones/repo_{i}/file.py") for i in range(1000)
        ]
        
        # Test project handler performance
        start_time = time.time()
        for path in test_paths:
            project_handler.can_handle(path)
        project_time = time.time() - start_time
        
        # Test git handler performance  
        start_time = time.time()
        for path in test_paths:
            git_handler.can_handle(path)
        git_time = time.time() - start_time
        
        # Should complete quickly (under 1 second for 2000 paths)
        assert project_time < 1.0, f"Project handler too slow: {project_time}s"
        assert git_time < 1.0, f"Git handler too slow: {git_time}s"
    
    def test_path_calculation_performance(self):
        """Test that path calculations are efficient.""" 
        import time
        
        project_handler = ProjectHandler()
        
        source_root = Path("/project")
        test_files = [Path(f"/project/src/module_{i}.py") for i in range(100)]
        
        # Test cache path calculation performance
        start_time = time.time()
        for file_path in test_files:
            project_handler.get_cache_path(file_path, source_root)
        cache_time = time.time() - start_time
        
        # Test knowledge file path calculation performance
        test_dirs = [Path(f"/project/src/dir_{i}") for i in range(100)]
        
        start_time = time.time()
        for dir_path in test_dirs:
            project_handler.get_knowledge_file_path(dir_path, source_root)
        kb_time = time.time() - start_time
        
        # Should complete quickly
        assert cache_time < 0.5, f"Cache path calculation too slow: {cache_time}s"
        assert kb_time < 0.5, f"KB path calculation too slow: {kb_time}s"


class TestHandlerErrorHandling:
    """Test handler error handling and edge cases."""
    
    def test_invalid_source_root(self):
        """Test handlers with invalid source root paths."""
        project_handler = ProjectHandler()
        
        file_path = Path("/project/src/module.py")
        invalid_root = Path("/different/project")
        
        # Should handle gracefully when file is outside source root
        try:
            cache_path = project_handler.get_cache_path(file_path, invalid_root)
            # If it succeeds, should return a valid path
            assert cache_path is not None
        except Exception as e:
            # If it fails, should be a clear error
            assert "outside source root" in str(e).lower() or isinstance(e, ValueError)
    
    def test_permission_denied_paths(self):
        """Test handlers with permission-denied paths."""
        project_handler = ProjectHandler()
        
        # Test with paths that might have permission issues
        restricted_path = Path("/root/restricted/file.py")
        source_root = Path("/root/restricted")
        
        # Should not crash on permission errors
        try:
            cache_path = project_handler.get_cache_path(restricted_path, source_root)
            assert cache_path is not None
        except PermissionError:
            # Permission errors are acceptable
            pass
    
    def test_nonexistent_path_handling(self):
        """Test handlers with nonexistent paths."""
        project_handler = ProjectHandler()
        
        nonexistent_path = Path("/project/src/nonexistent.py")
        source_root = Path("/project")
        
        # Should handle nonexistent paths gracefully
        cache_path = project_handler.get_cache_path(nonexistent_path, source_root)
        assert cache_path is not None
        
        kb_path = Path("/project/.knowledge/src/nonexistent_kb.md")
        source_path = project_handler.get_source_path(kb_path, source_root)
        # Should return None for nonexistent source
        assert source_path is None or not source_path.exists()

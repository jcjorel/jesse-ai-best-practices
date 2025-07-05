"""
Test suite for OrphanedAnalysisCleanup functionality.

This module tests the orphaned analysis cleanup component to ensure it properly
identifies and removes orphaned analysis files and knowledge files from the
knowledge base directory structure.
"""

import pytest
import tempfile
import asyncio
from pathlib import Path
from unittest.mock import AsyncMock

from jesse_framework_mcp.knowledge_bases.models import IndexingConfig
from jesse_framework_mcp.knowledge_bases.indexing.orphaned_cleanup import OrphanedAnalysisCleanup
from fastmcp import Context


@pytest.fixture
def temp_directories():
    """Create temporary directories for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create source directory structure
        source_root = temp_path / "source"
        source_root.mkdir()
        
        # Create knowledge directory structure
        knowledge_root = temp_path / "knowledge"
        knowledge_root.mkdir()
        project_base = knowledge_root / "project-base"
        project_base.mkdir()
        
        yield {
            'temp_root': temp_path,
            'source_root': source_root,
            'knowledge_root': knowledge_root,
            'project_base': project_base
        }


@pytest.fixture
def indexing_config(temp_directories):
    """Create test indexing configuration."""
    # Create configuration with explicit knowledge output directory
    from jesse_framework_mcp.knowledge_bases.models.indexing_config import (
        OutputConfig, FileProcessingConfig, ContentFilteringConfig, 
        LLMConfig, ChangeDetectionConfig, ErrorHandlingConfig, DebugConfig
    )
    
    output_config = OutputConfig(knowledge_output_directory=temp_directories['knowledge_root'])
    
    return IndexingConfig(
        handler_type="project-base",
        description="Test configuration for orphaned cleanup",
        output_config=output_config
    )


@pytest.fixture
def mock_context():
    """Create mock FastMCP context."""
    ctx = AsyncMock(spec=Context)
    return ctx


class TestOrphanedAnalysisCleanup:
    """Test cases for OrphanedAnalysisCleanup component."""
    
    @pytest.mark.asyncio
    async def test_cleanup_orphaned_analysis_files(self, temp_directories, indexing_config, mock_context):
        """Test cleanup of orphaned analysis files without corresponding source files."""
        source_root = temp_directories['source_root']
        project_base = temp_directories['project_base']
        
        # Create a source file
        source_file = source_root / "existing_file.py"
        source_file.write_text("print('hello world')")
        
        # Create analysis files - one with source, one orphaned
        project_base_dir = project_base / "subdir"
        project_base_dir.mkdir()
        
        valid_analysis = project_base_dir / "existing_file.py.analysis.md"
        valid_analysis.write_text("# Analysis of existing_file.py\nThis file prints hello world.")
        
        orphaned_analysis = project_base_dir / "deleted_file.py.analysis.md"
        orphaned_analysis.write_text("# Analysis of deleted_file.py\nThis file was deleted.")
        
        # Create corresponding source directory structure
        source_subdir = source_root / "subdir"
        source_subdir.mkdir()
        actual_source = source_subdir / "existing_file.py"
        actual_source.write_text("print('hello world')")
        
        # Run cleanup
        cleanup = OrphanedAnalysisCleanup(indexing_config)
        stats = await cleanup.cleanup_orphaned_files(
            temp_directories['knowledge_root'], 
            source_root, 
            mock_context
        )
        
        # Verify results
        assert stats.analysis_files_deleted == 1
        assert stats.total_items_deleted == 1
        assert valid_analysis.exists()  # Should still exist
        assert not orphaned_analysis.exists()  # Should be deleted
    
    @pytest.mark.asyncio
    async def test_cleanup_orphaned_knowledge_files(self, temp_directories, indexing_config, mock_context):
        """Test cleanup of orphaned knowledge files in empty directories."""
        source_root = temp_directories['source_root']
        knowledge_root = temp_directories['knowledge_root']
        project_base = temp_directories['project_base']
        
        # Create empty directory structure in project-base (no analysis files)
        empty_dir = project_base / "empty_directory"
        empty_dir.mkdir()
        
        # Create corresponding knowledge file
        knowledge_file = knowledge_root / "project-base" / "empty_directory" / "empty_directory_kb.md"
        knowledge_file.parent.mkdir(parents=True, exist_ok=True)
        knowledge_file.write_text("# Knowledge file for empty directory")
        
        # Run cleanup
        cleanup = OrphanedAnalysisCleanup(indexing_config)
        stats = await cleanup.cleanup_orphaned_files(knowledge_root, source_root, mock_context)
        
        # Verify results
        assert stats.knowledge_files_deleted == 1
        assert stats.directories_deleted == 1  # Empty directory should also be removed
        assert not knowledge_file.exists()
        assert not empty_dir.exists()
    
    @pytest.mark.asyncio
    async def test_preserve_directories_with_content(self, temp_directories, indexing_config, mock_context):
        """Test that directories with analysis files or subdirectories are preserved."""
        source_root = temp_directories['source_root']
        knowledge_root = temp_directories['knowledge_root']
        project_base = temp_directories['project_base']
        
        # Create directory with analysis file
        dir_with_content = project_base / "content_directory"
        dir_with_content.mkdir()
        
        analysis_file = dir_with_content / "source_file.py.analysis.md"
        analysis_file.write_text("# Analysis content")
        
        # Create corresponding source structure
        source_dir = source_root / "content_directory"
        source_dir.mkdir()
        source_file = source_dir / "source_file.py"
        source_file.write_text("print('content')")
        
        # Create knowledge file
        knowledge_file = knowledge_root / "project-base" / "content_directory" / "content_directory_kb.md"
        knowledge_file.parent.mkdir(parents=True, exist_ok=True)
        knowledge_file.write_text("# Knowledge file with content")
        
        # Run cleanup
        cleanup = OrphanedAnalysisCleanup(indexing_config)
        stats = await cleanup.cleanup_orphaned_files(knowledge_root, source_root, mock_context)
        
        # Verify nothing was deleted (directory has content)
        assert stats.total_items_deleted == 0
        assert analysis_file.exists()
        assert knowledge_file.exists()
        assert dir_with_content.exists()
    
    @pytest.mark.asyncio
    async def test_no_cleanup_needed(self, temp_directories, indexing_config, mock_context):
        """Test cleanup when no orphaned files exist."""
        source_root = temp_directories['source_root']
        knowledge_root = temp_directories['knowledge_root']
        
        # Run cleanup on empty structure
        cleanup = OrphanedAnalysisCleanup(indexing_config)
        stats = await cleanup.cleanup_orphaned_files(knowledge_root, source_root, mock_context)
        
        # Verify no cleanup occurred
        assert stats.total_items_deleted == 0
        assert stats.analysis_files_deleted == 0
        assert stats.knowledge_files_deleted == 0
        assert stats.directories_deleted == 0
    
    @pytest.mark.asyncio
    async def test_preserve_empty_directories_with_existing_source(self, temp_directories, indexing_config, mock_context):
        """Test that empty mirrored directories are preserved when corresponding source directory exists."""
        source_root = temp_directories['source_root']
        project_base = temp_directories['project_base']
        
        # Create empty source directory
        empty_source_dir = source_root / "empty_but_exists"
        empty_source_dir.mkdir()
        
        # Create corresponding empty mirrored directory
        empty_mirrored_dir = project_base / "empty_but_exists"
        empty_mirrored_dir.mkdir()
        
        # Create another empty mirrored directory WITHOUT corresponding source directory
        orphaned_mirrored_dir = project_base / "orphaned_empty"
        orphaned_mirrored_dir.mkdir()
        
        # Run cleanup
        cleanup = OrphanedAnalysisCleanup(indexing_config)
        stats = await cleanup.cleanup_orphaned_files(
            temp_directories['knowledge_root'], 
            source_root, 
            mock_context
        )
        
        # Verify results: only the orphaned directory should be deleted
        assert stats.directories_deleted == 1  # Only orphaned_empty should be deleted
        assert empty_mirrored_dir.exists()  # Should still exist because source exists
        assert not orphaned_mirrored_dir.exists()  # Should be deleted because no source
    
    @pytest.mark.asyncio
    async def test_leaf_first_directory_collection(self, temp_directories, indexing_config):
        """Test that directories are collected in leaf-first order."""
        project_base = temp_directories['project_base']
        
        # Create nested directory structure
        level1 = project_base / "level1"
        level1.mkdir()
        level2 = level1 / "level2"
        level2.mkdir()
        level3 = level2 / "level3"
        level3.mkdir()
        
        cleanup = OrphanedAnalysisCleanup(indexing_config)
        directories = cleanup._collect_directories_leaf_first(project_base)
        
        # Verify leaf-first order: deepest directories should come first
        directory_names = [d.name for d in directories]
        
        # level3 should come before level2, level2 before level1, level1 before project-base
        assert directory_names.index("level3") < directory_names.index("level2")
        assert directory_names.index("level2") < directory_names.index("level1")
        assert directory_names.index("level1") < directory_names.index("project-base")


if __name__ == "__main__":
    pytest.main([__file__])

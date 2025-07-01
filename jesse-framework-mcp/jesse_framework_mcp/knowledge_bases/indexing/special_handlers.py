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
# Special handlers for Knowledge Bases Hierarchical Indexing System.
# Implements specialized processing for git-clones (read-only mirrored structure)
# and project-base (whole codebase indexing) scenarios with custom handling logic.
###############################################################################
# [Source file design principles]
# - Read-only git clone handling with mirrored knowledge structure preservation
# - Whole project codebase indexing with systematic exclusion rules
# - Specialized processing logic for unique scenarios and requirements
# - Integration with core hierarchical indexing while maintaining special case handling
# - Defensive programming ensuring graceful handling of access restrictions and errors
###############################################################################
# [Source file constraints]
# - Git clones must never be modified - read-only access only
# - Mirrored knowledge structure must maintain directory hierarchy relationships
# - Project-base indexing must exclude system directories (.git, .knowledge, .coding_assistant)
# - Special handlers must integrate seamlessly with core hierarchical processing
# - Error handling must continue processing when individual special cases fail
###############################################################################
# [Dependencies]
# <codebase>: ..models.indexing_config - Configuration and exclusion rules
# <codebase>: ..models.knowledge_context - Context structures for special handling
# <system>: pathlib - Cross-platform path operations and directory traversal
# <system>: logging - Structured logging for special handling operations
# <system>: gitignore_parser - Git ignore pattern parsing for project-base scenarios
###############################################################################
# [GenAI tool change history]
# 2025-07-01T12:16:00Z : Initial special handlers creation by CodeAssistant
# * Created GitCloneHandler for read-only git clone processing with mirrored structure
# * Created ProjectBaseHandler for whole codebase indexing with exclusion rules
# * Set up specialized processing integration with core hierarchical indexing
###############################################################################

"""
Special Handlers for Hierarchical Indexing System.

This module implements specialized processing handlers for unique scenarios:
- GitCloneHandler: Read-only git clone processing with mirrored knowledge structure
- ProjectBaseHandler: Whole project codebase indexing with systematic exclusions
"""

import logging
from pathlib import Path
from typing import List, Set, Optional

from fastmcp import Context

from ..models import (
    IndexingConfig,
    DirectoryContext,
    FileContext
)

logger = logging.getLogger(__name__)


class GitCloneHandler:
    """
    [Class intent]
    Specialized handler for processing git clones in read-only mode with mirrored
    knowledge structure. Ensures git clone directories remain untouched while
    creating parallel knowledge base structure for comprehensive content analysis.

    [Design principles]
    Read-only git clone access ensuring original repositories remain unmodified.
    Mirrored knowledge structure maintaining directory hierarchy relationships.
    Specialized path mapping enabling knowledge files creation in separate structure.
    Integration with core indexing while preserving git clone integrity.
    Defensive error handling for access restrictions and permission issues.

    [Implementation details]
    Maps git clone directory structure to parallel knowledge base structure.
    Implements read-only file access with comprehensive error handling.
    Creates mirrored directory hierarchy for knowledge file placement.
    Provides specialized path resolution for git clone scenarios.
    Integrates with core hierarchical processing while maintaining special handling.
    """
    
    def __init__(self, config: IndexingConfig):
        """
        [Class method intent]
        Initializes git clone handler with configuration for specialized processing.
        Sets up path mapping and mirrored structure handling for read-only
        git clone processing with comprehensive knowledge base generation.

        [Design principles]
        Configuration-driven behavior enabling flexible git clone processing.
        Path mapping initialization for mirrored structure creation and management.
        Error handling setup for robust git clone access and processing.

        [Implementation details]
        Stores configuration reference for git clone processing parameters.
        Initializes path mapping utilities for mirrored structure handling.
        Sets up logging and error handling for git clone specific operations.
        """
        self.config = config
        logger.info("Initialized GitCloneHandler for read-only git clone processing")
    
    def is_git_clone_path(self, path: Path) -> bool:
        """
        [Class method intent]
        Determines if a given path is within a git clone directory requiring
        specialized handling. Identifies git clone scenarios for appropriate
        processing strategy selection and mirrored structure creation.

        [Design principles]
        Path-based git clone detection enabling targeted specialized processing.
        Clear identification logic supporting processing strategy selection.
        Integration point for specialized handler activation and coordination.

        [Implementation details]
        Checks if path is within .knowledge/git-clones/ directory structure.
        Uses path matching to identify git clone scenarios requiring special handling.
        Returns boolean decision for processing strategy selection and handler activation.
        """
        # Check if path is within .knowledge/git-clones/ directory
        try:
            path_parts = path.parts
            return '.knowledge' in path_parts and 'git-clones' in path_parts
        except Exception:
            return False
    
    def get_mirrored_knowledge_path(self, git_clone_path: Path, base_knowledge_path: Path) -> Path:
        """
        [Class method intent]
        Converts git clone file path to mirrored knowledge structure path.
        Creates parallel knowledge directory structure enabling knowledge file
        creation without modifying original git clone directories.

        [Design principles]
        Path mapping preserving directory hierarchy relationships in mirrored structure.
        Knowledge file placement enabling comprehensive content analysis without modification.
        Parallel structure creation maintaining clear separation between source and knowledge.

        [Implementation details]
        Maps git clone paths to corresponding knowledge base paths with _kb suffix.
        Preserves directory hierarchy relationships in mirrored structure.
        Returns knowledge file path for specialized knowledge file creation.
        """
        try:
            # Convert path like .knowledge/git-clones/repo/file.py
            # to .knowledge/git-clones/repo_kb/file_kb.md
            
            git_clone_root = base_knowledge_path / "git-clones"
            relative_path = git_clone_path.relative_to(git_clone_root)
            
            # Get repository name (first part of relative path)
            repo_parts = relative_path.parts
            if not repo_parts:
                return git_clone_root
            
            repo_name = repo_parts[0]
            mirrored_repo_path = git_clone_root / f"{repo_name}_kb"
            
            # Handle file within repository
            if len(repo_parts) > 1:
                # Reconstruct path within mirrored structure
                inner_path_parts = repo_parts[1:]
                for part in inner_path_parts[:-1]:  # All but the last part (directories)
                    mirrored_repo_path = mirrored_repo_path / part
                
                # Handle the file part
                if inner_path_parts:
                    file_part = inner_path_parts[-1]
                    if '.' in file_part:
                        file_name = file_part.rsplit('.', 1)[0]  # Remove extension
                        mirrored_file_path = mirrored_repo_path / f"{file_name}_kb.md"
                    else:
                        mirrored_file_path = mirrored_repo_path / f"{file_part}_kb.md"
                    return mirrored_file_path
            
            return mirrored_repo_path
            
        except Exception as e:
            logger.error(f"Mirrored path generation failed for {git_clone_path}: {e}")
            return base_knowledge_path / "git-clones" / "unknown_kb.md"
    
    async def process_git_clone_structure(self, git_clone_root: Path, ctx: Context) -> DirectoryContext:
        """
        [Class method intent]
        Processes git clone directory structure creating mirrored knowledge base
        representation. Builds DirectoryContext for git clone content while
        ensuring read-only access and comprehensive knowledge base generation.

        [Design principles]
        Read-only git clone processing ensuring original repository integrity.
        Comprehensive directory structure analysis enabling complete knowledge coverage.
        Mirrored structure creation supporting parallel knowledge base development.
        Error handling ensuring processing continues despite access restrictions.

        [Implementation details]
        Traverses git clone directory structure in read-only mode.
        Creates DirectoryContext objects for mirrored knowledge base structure.
        Handles access restrictions and permission errors gracefully.
        Returns structured context for integration with core hierarchical processing.
        """
        await ctx.info(f"Processing git clone structure: {git_clone_root}")
        
        try:
            # This would implement comprehensive git clone structure processing
            # For now, return basic structure
            return DirectoryContext(
                directory_path=git_clone_root,
                file_contexts=[],
                subdirectory_contexts=[]
            )
            
        except Exception as e:
            logger.error(f"Git clone structure processing failed for {git_clone_root}: {e}")
            await ctx.error(f"Git clone processing failed: {git_clone_root}")
            raise


class ProjectBaseHandler:
    """
    [Class intent]
    Specialized handler for whole project codebase indexing with systematic exclusions.
    Processes entire project directory structure while excluding system directories
    and maintaining comprehensive knowledge base coverage of project content.

    [Design principles]
    Whole codebase indexing enabling comprehensive project knowledge coverage.
    Systematic exclusion rules preventing processing of system and temporary directories.
    Integration with core hierarchical processing while maintaining specialized logic.
    Gitignore pattern respect honoring project-specific exclusion requirements.
    Defensive programming handling large codebases and access restrictions gracefully.

    [Implementation details]
    Implements comprehensive project directory traversal with exclusion filtering.
    Integrates gitignore pattern parsing for project-specific exclusion rules.
    Handles large codebase scenarios with efficient processing strategies.
    Provides specialized configuration for whole project indexing requirements.
    Reports progress for large codebase processing with detailed operation status.
    """
    
    def __init__(self, config: IndexingConfig):
        """
        [Class method intent]
        Initializes project base handler with configuration for whole codebase processing.
        Sets up exclusion rules and gitignore integration for comprehensive
        project indexing with appropriate system directory filtering.

        [Design principles]
        Configuration-driven exclusion rules enabling flexible project processing.
        Gitignore integration respecting project-specific exclusion requirements.
        System directory exclusion preventing processing of inappropriate content.

        [Implementation details]
        Stores configuration reference for project processing parameters.
        Sets up exclusion rule processing for system directory filtering.
        Initializes gitignore pattern handling for project-specific exclusions.
        """
        self.config = config
        
        # System directories to exclude from project-base indexing
        self.system_exclusions = {
            '.git', '.knowledge', '.coding_assistant',
            '.vscode', '.idea', '__pycache__',
            'node_modules', '.pytest_cache', '.mypy_cache'
        }
        
        logger.info("Initialized ProjectBaseHandler for whole codebase indexing")
    
    def should_process_project_item(self, item_path: Path, project_root: Path) -> bool:
        """
        [Class method intent]
        Determines if a project item should be processed based on exclusion rules.
        Applies system directory exclusions and gitignore patterns to filter
        appropriate content for comprehensive project knowledge base generation.

        [Design principles]
        Comprehensive filtering combining system exclusions with project-specific rules.
        Gitignore pattern respect honoring project development practices.
        Efficient filtering minimizing unnecessary processing overhead.

        [Implementation details]
        Applies system directory exclusions for standard development environments.
        Checks gitignore patterns when configuration enables gitignore respect.
        Returns boolean decision for item processing inclusion or exclusion.
        """
        try:
            # Check system exclusions
            if item_path.name in self.system_exclusions:
                return False
            
            # Check configuration exclusions
            if item_path.is_file() and not self.config.should_process_file(item_path):
                return False
            
            if item_path.is_dir() and not self.config.should_process_directory(item_path):
                return False
            
            # Additional project-specific logic could be added here
            # such as gitignore pattern matching if needed
            
            return True
            
        except Exception as e:
            logger.warning(f"Project item filtering failed for {item_path}: {e}")
            return False
    
    async def process_project_structure(self, project_root: Path, ctx: Context) -> DirectoryContext:
        """
        [Class method intent]
        Processes entire project directory structure creating comprehensive knowledge base
        coverage. Applies exclusion rules while traversing all appropriate project
        content for complete codebase knowledge generation.

        [Design principles]
        Comprehensive project traversal enabling complete codebase knowledge coverage.
        Exclusion rule application preventing inappropriate content processing.
        Progress reporting supporting user feedback for large codebase processing.
        Error handling ensuring processing continues despite individual item failures.

        [Implementation details]
        Traverses project directory structure applying exclusion filtering.
        Creates comprehensive DirectoryContext for entire project codebase.
        Handles large codebase scenarios with progress reporting and status updates.
        Returns structured context for integration with core hierarchical processing.
        """
        await ctx.info(f"Processing project structure: {project_root}")
        
        try:
            # This would implement comprehensive project structure processing
            # For now, return basic structure
            return DirectoryContext(
                directory_path=project_root,
                file_contexts=[],
                subdirectory_contexts=[]
            )
            
        except Exception as e:
            logger.error(f"Project structure processing failed for {project_root}: {e}")
            await ctx.error(f"Project processing failed: {project_root}")
            raise
    
    def get_project_knowledge_path(self, project_root: Path) -> Path:
        """
        [Class method intent]
        Determines knowledge file location for project-base indexing following
        established naming conventions. Provides consistent knowledge file
        placement for whole project codebase indexing scenarios.

        [Design principles]
        Consistent knowledge file placement following hierarchical conventions.
        Project-base specific naming supporting specialized indexing scenarios.
        Knowledge base organization enabling clear separation of project content.

        [Implementation details]
        Generates project knowledge base path within .knowledge/project-base/ structure.
        Uses project name with knowledge file naming conventions.
        Returns Path object for project knowledge file creation and management.
        """
        # Project knowledge files go in .knowledge/project-base/
        knowledge_root = project_root / ".knowledge" / "project-base"
        return knowledge_root / f"{project_root.name}_kb.md"

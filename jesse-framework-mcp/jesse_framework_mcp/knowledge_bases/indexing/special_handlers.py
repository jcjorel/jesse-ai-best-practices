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
# 2025-07-07T21:14:00Z : CRITICAL ROOT CAUSE FIX - Fixed git-clone KB hierarchy creation in wrong location by CodeAssistant
# * FIXED ROOT CAUSE: Modified _build_unified_directory_context() to accept handler and source_root parameters enabling proper knowledge_file_path calculation
# * BEFORE: DirectoryContext objects created with knowledge_file_path=None causing git-clone KBs to use project-base paths as fallback
# * AFTER: Each handler now calculates correct knowledge_file_path during discovery phase eliminating path confusion
# * UPDATED HANDLERS: Both GitCloneHandler and ProjectBaseHandler now pass handler instances enabling get_knowledge_path() calls
# * PREVENTS CROSS-CONTAMINATION: Git-clone repositories now create KB files in .knowledge/git-clones/<repo>.kb/ instead of .knowledge/project-base/
# * ELIMINATES WORKAROUNDS: Removed complex downstream path extraction workarounds in PlanGenerator and ExecutionEngine
# 2025-07-07T16:36:00Z : CRITICAL LEAF-FIRST UNIFICATION - Unified DirectoryContext building ensuring identical leaf-first processing by CodeAssistant
# * UNIFIED PROCESSING: Created _build_unified_directory_context() function used by both GitCloneHandler and ProjectBaseHandler
# * IDENTICAL LEAF-FIRST: Both handlers now produce structurally identical DirectoryContext objects ensuring consistent Plan Generator task dependencies
# * SIMPLIFIED GIT-CLONE: Removed complex mirrored path logic, git-clone uses root_kb.md naming for consistency with project-base
# * ZERO REGRESSION: ProjectBaseHandler maintains proven processing logic while gaining unified approach benefits
# * ENSURES: Git-clone processing follows exact same leaf-first order as project-base (deepest directories first, then parents)
# 2025-07-07T14:08:00Z : COMPLETE IMPLEMENTATION - GitCloneHandler full implementation for integration test support by CodeAssistant
# * Implemented complete process_git_clone_structure() with real directory traversal similar to ProjectBaseHandler
# * Added _build_git_clone_directory_context() method with recursive processing and git-clone specific filtering
# * Added git-clone exclusions (.git, build artifacts, caches) while preserving repository integrity
# * Added should_process_git_clone_item() method for git-clone specific filtering rules
# * ENABLES: Integration test to process all 8 git-clone repositories (strands_*, fastmcp, cline) with proper knowledge file generation
# 2025-07-06T22:13:00Z : CRITICAL BUG FIX - Implemented actual subdirectory discovery in ProjectBaseHandler by CodeAssistant
# * Fixed ProjectBaseHandler.process_project_structure() which was just a placeholder stub returning empty subdirectory_contexts=[]
# * Added comprehensive _build_project_directory_context() method with recursive directory traversal and proper filtering
# * Implemented actual FileContext and DirectoryContext creation with metadata extraction and project-base exclusions
# * RESOLVES: root_kb.md showing "No subdirectories processed" despite project having multiple subdirectories (artifacts/, howtos/, etc.)
# 2025-07-06T13:33:00Z : Fixed project-base root naming to use root_kb.md by CodeAssistant
# * Updated ProjectBaseHandler.get_project_knowledge_path() to return root_kb.md instead of {project_name}_kb.md
# * Aligned implementation with established root_kb.md naming decision for project-base handler
# * Updated method documentation to reflect root_kb.md naming convention for project root
###############################################################################

"""
Special Handlers for Hierarchical Indexing System.

This module implements specialized processing handlers for unique scenarios:
- GitCloneHandler: Read-only git clone processing with mirrored knowledge structure
- ProjectBaseHandler: Whole project codebase indexing with systematic exclusions

Updated to implement the standardized IndexingHandler interface for proper
path delegation and extensible architecture.
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
from .handler_interface import IndexingHandler

logger = logging.getLogger(__name__)


async def _build_unified_directory_context(
    directory_path: Path, 
    filter_func, 
    handler,
    ctx: Context, 
    handler_name: str,
    source_root: Path
) -> DirectoryContext:
    """
    [Function intent]
    Unified DirectoryContext building function used by both GitCloneHandler and ProjectBaseHandler.
    Ensures identical leaf-first processing logic and DirectoryContext structure across all handlers
    while applying handler-specific filtering rules and knowledge file path calculation.

    [Design principles]
    Unified processing logic ensuring consistent leaf-first DirectoryContext building across handlers.
    Handler-specific filtering enabling specialized exclusion rules while maintaining processing consistency.
    Handler-specific knowledge file path calculation ensuring correct KB file placement.
    Identical recursive structure ensuring Plan Generator creates consistent task dependencies.
    Error handling enabling graceful degradation when individual items are inaccessible.
    Progress reporting supporting handler-specific logging and debugging capabilities.

    [Implementation details]
    Uses provided filter_func for handler-specific item filtering (git-clone vs project-base exclusions).
    Uses handler reference to calculate correct knowledge file paths for each directory.
    Creates identical FileContext and DirectoryContext objects with consistent metadata extraction.
    Implements identical recursive processing ensuring consistent parent-child relationships.
    Handles filesystem errors gracefully with logging and continued processing.
    Returns DirectoryContext with correct knowledge_file_path set by handler.

    Args:
        directory_path: Path to directory being processed
        filter_func: Handler-specific filtering function (should_process_* method)
        handler: Handler instance for knowledge file path calculation
        ctx: FastMCP context for progress reporting
        handler_name: Handler name for logging ("git-clone" or "project-base")
        source_root: Source root path for handler knowledge file path calculation

    Returns:
        DirectoryContext: Unified DirectoryContext with handler-specific knowledge file path
    """
    from datetime import datetime
    
    file_contexts = []
    subdirectory_contexts = []
    
    try:
        # Process files and directories in current directory using unified logic
        for item in directory_path.iterdir():
            try:
                # Apply handler-specific filtering
                if not filter_func(item, directory_path):
                    continue
                
                if item.is_file():
                    # Create FileContext with identical metadata extraction
                    file_context = FileContext(
                        file_path=item,
                        file_size=item.stat().st_size,
                        last_modified=datetime.fromtimestamp(item.stat().st_mtime)
                    )
                    file_contexts.append(file_context)
                    
                elif item.is_dir():
                    # Recursive directory processing with identical structure
                    await ctx.debug(f"Discovering {handler_name} subdirectory: {item.name}")
                    subdir_context = await _build_unified_directory_context(
                        item, filter_func, handler, ctx, handler_name, source_root
                    )
                    subdirectory_contexts.append(subdir_context)
                    
            except (OSError, PermissionError) as e:
                logger.warning(f"Skipping inaccessible {handler_name} item {item}: {e}")
                continue
    
    except (OSError, PermissionError) as e:
        logger.error(f"Cannot access {handler_name} directory {directory_path}: {e}")
        await ctx.warning(f"{handler_name.title()} directory access failed: {directory_path.name}")
    
    # Report discovery results with handler-specific logging
    if subdirectory_contexts:
        await ctx.debug(f"Discovered {len(subdirectory_contexts)} subdirectories in {handler_name} {directory_path.name}")
    
    # Calculate handler-specific knowledge file path
    knowledge_file_path = handler.get_knowledge_path(directory_path, source_root)
    await ctx.debug(f"Handler {handler_name} determined KB path: {knowledge_file_path}")
    
    return DirectoryContext(
        directory_path=directory_path,
        file_contexts=file_contexts,
        subdirectory_contexts=subdirectory_contexts,
        knowledge_file_path=knowledge_file_path
    )


class GitCloneHandler(IndexingHandler):
    """
    [Class intent]
    Specialized handler for processing git clones implementing IndexingHandler interface.
    Uses unified DirectoryContext building with git-clone specific exclusions,
    ensuring consistent leaf-first processing and proper path delegation.

    [Design principles]
    IndexingHandler interface implementation ensuring consistent behavior across all content types.
    Git-clone specific path calculation and filtering preserving repository integrity.
    Warn-and-skip approach for unsupported paths preventing incorrect processing.
    Handler-specific orphaned file detection for git-clone managed directories.
    Unified DirectoryContext building ensuring identical processing as other handlers.

    [Implementation details]
    Implements all IndexingHandler abstract methods for complete interface compliance.
    Uses git-clone specific path detection and calculation for proper file placement.
    Delegates processing to unified _build_unified_directory_context() method.
    Provides reverse path mapping for validation and cleanup operations.
    Integrates seamlessly with HandlerRegistry and warn-and-skip architecture.
    """
    
    def __init__(self, config: IndexingConfig):
        """
        [Class method intent]
        Initializes git clone handler with configuration and unified processing approach.
        Sets up git-clone specific exclusions while using proven DirectoryContext building patterns.

        [Design principles]
        Configuration-driven behavior enabling flexible git clone processing with proven patterns.
        Git-clone exclusion setup preserving repository integrity during unified processing.
        Simplified initialization removing complex path mapping in favor of unified approach.

        [Implementation details]
        Stores configuration reference for processing parameters and exclusion rules.
        Sets up git-clone specific exclusions for development artifacts and system files.
        Initializes unified processing approach using proven project-base patterns.
        """
        self.config = config
        
        # Git clone specific exclusions - preserve repository integrity
        self.git_clone_exclusions = {
            '.git',           # Git metadata directory
            '__pycache__',    # Python compiled files
            '.pytest_cache',  # Pytest cache
            '.mypy_cache',    # MyPy cache
            'node_modules',   # Node.js dependencies
            '.vscode',        # VS Code settings
            '.idea',          # IntelliJ settings
            'build',          # Build directories
            'dist',           # Distribution directories
            '.tox',           # Tox testing
            '.coverage',      # Coverage files
            '*.egg-info',     # Python egg info
            '.DS_Store'       # macOS system files
        }
        
        logger.info("Initialized GitCloneHandler with unified processing approach")
    
    # IndexingHandler interface implementation
    def get_handler_type(self) -> str:
        """
        [Class method intent]
        Returns handler type identifier for git-clone content processing.
        Enables registry identification and routing for git-clone directories.

        [Design principles]
        Clear handler identification supporting automatic routing and debugging.
        Consistent naming convention following handler type standards.

        [Implementation details]
        Returns "git-clone" string identifier for registry lookup and routing.
        Used by HandlerRegistry for capability-based handler selection.
        """
        return "git-clone"
    
    def can_handle(self, source_path: Path) -> bool:
        """
        [Class method intent]
        Determines if this handler can process git-clone source paths.
        Enables automatic handler selection based on path characteristics.

        [Design principles]
        Git-clone path detection enabling specialized processing for git repositories.
        Clear capability declaration supporting registry-based handler routing.

        [Implementation details]
        Delegates to is_git_clone_path() method for consistent path detection logic.
        Returns True only for paths within .knowledge/git-clones/ directory structure.
        """
        return self.is_git_clone_path(source_path)
    
    def get_knowledge_path(self, target_path: Path, source_root: Path) -> Path:
        """
        [Class method intent]
        Calculates knowledge file path for git-clone target using handler-specific logic.
        Provides git-clone specific knowledge file placement for proper hierarchy organization.

        [Design principles]
        Git-clone specific path calculation ensuring knowledge files are placed in git-clone directories.
        Consistent root_kb.md naming convention matching project-base handler approach.
        Handler-controlled file placement eliminating hardcoded path assumptions.

        [Implementation details]
        Uses target_path as git-clone root for knowledge file calculation.
        Delegates to get_git_clone_knowledge_path() for consistent path generation.
        Returns absolute path for git-clone knowledge file creation and management.
        """
        return self.get_git_clone_knowledge_path(target_path)
    
    def get_cache_path(self, file_path: Path, source_root: Path) -> Path:
        """
        [Class method intent]
        Calculates analysis cache path for git-clone files using separate .kb directory structure.
        Provides git-clone specific cache organization ensuring separation from source repository
        while maintaining clear relationship between source files and cache files.

        [Design principles]
        Separate .kb directory cache structure ensuring cache files never modify git-clone repositories.
        Read-only git-clone preservation maintaining original repository integrity.
        Mirrored cache structure within .kb directory enabling efficient cache operations and cleanup.
        Handler-controlled cache placement ensuring proper isolation from other content types.

        [Implementation details]
        Finds git-clone root directory from file path for cache base calculation.
        Creates separate .kb directory adjacent to git-clone directory for cache file storage.
        Uses mirrored structure within .kb directory maintaining relationship between source and cache.
        Returns absolute path pointing to cache file within dedicated .kb directory structure.
        """
        # Find git-clone root directory
        git_clone_root = self._find_git_clone_root(file_path)
        
        # Create relative path from git-clone root
        relative_path = file_path.relative_to(git_clone_root)
        
        # Cache files go in separate .kb directory with mirrored structure
        kb_directory = git_clone_root.parent / f"{git_clone_root.name}.kb"
        cache_filename = f"{file_path.name}.analysis.md"
        return kb_directory / relative_path.parent / cache_filename
    
    def should_process_item(self, item_path: Path, source_root: Path) -> bool:
        """
        [Class method intent]
        Determines if git-clone item should be processed based on handler-specific rules.
        Delegates to existing git-clone filtering logic ensuring consistent behavior.

        [Design principles]
        Handler-specific filtering enabling git-clone exclusions and configuration rules.
        Consistent filtering behavior maintaining existing processing logic.

        [Implementation details]
        Delegates to should_process_git_clone_item() method for consistent filtering.
        Uses source_root as git-clone root for filtering context.
        """
        return self.should_process_git_clone_item(item_path, source_root)
    
    async def process_structure(self, source_path: Path, ctx: Context) -> DirectoryContext:
        """
        [Class method intent]
        Processes git-clone structure returning DirectoryContext for indexing.
        Delegates to existing git-clone processing logic ensuring consistent behavior.

        [Design principles]
        Handler-specific processing enabling git-clone unified DirectoryContext building.
        Consistent processing behavior maintaining existing processing logic.

        [Implementation details]
        Delegates to process_git_clone_structure() method for unified processing.
        Returns structured context ready for Plan-then-Execute architecture.
        """
        return await self.process_git_clone_structure(source_path, ctx)
    
    async def find_orphaned_files(self, source_root: Path, ctx: Context) -> List[Path]:
        """
        [Class method intent]
        Finds orphaned files in git-clone managed areas for cleanup operations.
        Implements git-clone specific orphaned file detection and cleanup logic.

        [Design principles]
        Git-clone specific cleanup ensuring only appropriate files are identified for removal.
        Safe cleanup operations preventing accidental deletion of repository files.

        [Implementation details]
        Scans git-clone directories for knowledge and cache files without corresponding sources.
        Validates orphaned status using git-clone specific validation logic.
        Returns list of confirmed orphaned files ready for safe deletion.
        """
        orphaned_files = []
        
        try:
            # Find orphaned knowledge files in git-clone directories
            if self.is_git_clone_path(source_root):
                knowledge_file = self.get_git_clone_knowledge_path(source_root)
                if knowledge_file.exists():
                    # Check if source directory still exists
                    if not source_root.exists():
                        orphaned_files.append(knowledge_file)
                        await ctx.debug(f"Found orphaned git-clone knowledge file: {knowledge_file}")
                
                # Find orphaned cache files
                cache_dir = source_root / ".cache"
                if cache_dir.exists():
                    for cache_file in cache_dir.rglob("*.analysis.md"):
                        source_file = self.map_cache_to_source(cache_file, source_root)
                        if source_file is None or not source_file.exists():
                            orphaned_files.append(cache_file)
                            await ctx.debug(f"Found orphaned git-clone cache file: {cache_file}")
        
        except Exception as e:
            logger.warning(f"Git-clone orphaned file detection failed for {source_root}: {e}")
        
        return orphaned_files
    
    def map_knowledge_to_source(self, knowledge_path: Path, source_root: Path) -> Optional[Path]:
        """
        [Class method intent]
        Maps git-clone knowledge file back to corresponding source path for validation.
        Implements git-clone specific reverse path mapping for cleanup operations.

        [Design principles]
        Git-clone specific reverse mapping supporting validation and cleanup operations.
        Robust error handling returning None for invalid or unresolvable paths.

        [Implementation details]
        Validates knowledge file is git-clone root_kb.md and maps to git-clone directory.
        Uses git-clone path structure knowledge for accurate reverse mapping.
        Returns None for paths that cannot be resolved to valid git-clone sources.
        """
        try:
            # Git-clone knowledge files are root_kb.md in git-clone directories
            if knowledge_path.name == "root_kb.md" and self.is_git_clone_path(knowledge_path.parent):
                return knowledge_path.parent
            return None
        except Exception:
            return None
    
    def map_cache_to_source(self, cache_path: Path, source_root: Path) -> Optional[Path]:
        """
        [Class method intent]
        Maps git-clone cache file back to corresponding source path for validation.
        Implements git-clone specific reverse cache mapping for cleanup operations using .kb directory structure.

        [Design principles]
        Git-clone specific cache mapping supporting validation and cleanup operations.
        Separate .kb directory structure understanding for accurate reverse mapping.
        Robust error handling returning None for invalid or unresolvable paths.

        [Implementation details]
        Calculates corresponding source path from git-clone cache file location within .kb directory.
        Uses git-clone .kb directory cache structure knowledge for accurate reverse mapping.
        Returns None for paths that cannot be resolved to valid git-clone sources.
        """
        try:
            # Git-clone cache files are in .kb directory with mirrored structure
            if cache_path.name.endswith(".analysis.md") and ".kb" in cache_path.parts:
                # Find .kb directory (should be <repo_name>.kb)
                kb_directory = None
                for part_idx, part in enumerate(cache_path.parts):
                    if part.endswith(".kb"):
                        kb_directory = Path(*cache_path.parts[:part_idx+1])
                        break
                
                if kb_directory is None:
                    return None
                
                # Get corresponding git-clone directory name (remove .kb suffix)
                git_clone_name = kb_directory.name[:-3]  # Remove '.kb'
                git_clone_root = kb_directory.parent / git_clone_name
                
                # Extract relative path from cache structure within .kb directory
                cache_relative = cache_path.relative_to(kb_directory)
                
                # Remove .analysis.md suffix to get original filename
                original_name = cache_path.name.replace(".analysis.md", "")
                
                # Reconstruct source path
                source_path = git_clone_root / cache_relative.parent / original_name
                return source_path
            
            return None
        except Exception:
            return None
    
    # Helper methods (existing functionality)
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
    
    def get_git_clone_knowledge_path(self, git_clone_root: Path) -> Path:
        """
        [Class method intent]
        Determines knowledge file location for git-clone indexing using separate .kb directory structure.
        Provides git-clone specific knowledge file placement ensuring separation from source repository
        while maintaining clear organization and read-only git-clone integrity.

        [Design principles]
        Separate .kb directory structure ensuring knowledge files never modify git-clone repositories.
        Read-only git-clone preservation maintaining original repository integrity.
        Clear knowledge organization enabling easy identification of processed git-clone knowledge.
        Consistent root_kb.md naming convention across all git-clone repositories.

        [Implementation details]
        Creates separate .kb directory adjacent to git-clone directory for knowledge file storage.
        Uses <repo_name>.kb naming pattern for clear identification and organization.
        Returns Path object pointing to root_kb.md within dedicated knowledge directory.
        Ensures complete separation between source repository and processed knowledge content.
        """
        # Git-clone knowledge files go in separate .kb directory: .knowledge/git-clones/<repo_name>.kb/root_kb.md
        kb_directory = git_clone_root.parent / f"{git_clone_root.name}.kb"
        return kb_directory / "root_kb.md"
    
    def should_process_git_clone_item(self, item_path: Path, git_clone_root: Path) -> bool:
        """
        [Class method intent]
        Determines if a git clone item should be processed based on git-clone specific exclusion rules.
        Applies git clone exclusions and configuration filters to preserve repository integrity
        while enabling comprehensive content analysis.

        [Design principles]
        Git-clone specific filtering preserving repository integrity and read-only access.
        Comprehensive filtering combining git exclusions with configuration rules.
        Efficient filtering minimizing unnecessary processing overhead for git repositories.

        [Implementation details]
        Applies git clone specific exclusions for development artifacts and system files.
        Checks configuration exclusions when file and directory filters are enabled.
        Returns boolean decision for item processing inclusion or exclusion.
        """
        try:
            # Check git clone specific exclusions
            if item_path.name in self.git_clone_exclusions:
                return False
            
            # Check for pattern matches (like *.egg-info)
            if item_path.name.endswith('.egg-info'):
                return False
            
            # Check configuration exclusions
            if item_path.is_file() and not self.config.should_process_file(item_path):
                return False
            
            if item_path.is_dir() and not self.config.should_process_directory(item_path):
                return False
            
            return True
            
        except Exception as e:
            logger.warning(f"Git clone item filtering failed for {item_path}: {e}")
            return False

    async def process_git_clone_structure(self, git_clone_root: Path, ctx: Context) -> DirectoryContext:
        """
        [Class method intent]
        Processes git clone directory structure using unified DirectoryContext building approach.
        Uses same processing logic as ProjectBaseHandler with git-clone specific filtering
        ensuring identical leaf-first processing and Plan-then-Execute integration.

        [Design principles]
        Unified DirectoryContext building ensuring consistent leaf-first processing across handlers.
        Git-clone specific filtering preserving repository integrity during unified processing.
        Read-only git clone access ensuring original repository integrity.
        Error handling ensuring processing continues despite access restrictions.

        [Implementation details]
        Delegates to unified _build_unified_directory_context() method with git-clone filter.
        Uses identical processing logic as project-base handler for consistent DirectoryContext structure.
        Handles access restrictions and permission errors gracefully with continued processing.
        Returns structured context for integration with Plan-then-Execute architecture.
        """
        await ctx.info(f"Processing git clone structure: {git_clone_root}")
        
        try:
            # Use unified DirectoryContext building with git-clone specific filtering
            return await _build_unified_directory_context(
                directory_path=git_clone_root,
                filter_func=lambda item_path, root_path: self.should_process_git_clone_item(item_path, root_path),
                handler=self,
                ctx=ctx,
                handler_name="git-clone",
                source_root=git_clone_root
            )
            
        except Exception as e:
            logger.error(f"Git clone structure processing failed for {git_clone_root}: {e}")
            await ctx.error(f"Git clone processing failed: {git_clone_root}")
            raise
    
    def _find_git_clone_root(self, path: Path) -> Optional[Path]:
        """
        [Class method intent]
        Finds git-clone root directory from any path within git-clone structure.
        Enables cache path calculation and reverse mapping operations.

        [Design principles]
        Robust path traversal handling various path depths within git-clone structure.
        Git-clone root identification supporting cache and knowledge file operations.

        [Implementation details]
        Traverses path upward looking for .knowledge/git-clones/ pattern.
        Returns git-clone root directory or None if not found.
        """
        try:
            current = path
            while current.parent != current:  # Not at filesystem root
                if (current.parent.name == "git-clones" and 
                    current.parent.parent.name == ".knowledge"):
                    return current
                current = current.parent
            return None
        except Exception:
            return None


class ProjectBaseHandler(IndexingHandler):
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
    
    # IndexingHandler interface implementation
    def get_handler_type(self) -> str:
        """
        [Class method intent]
        Returns handler type identifier for project-base content processing.
        Enables registry identification and routing for project-base directories.

        [Design principles]
        Clear handler identification supporting automatic routing and debugging.
        Consistent naming convention following handler type standards.

        [Implementation details]
        Returns "project-base" string identifier for registry lookup and routing.
        Used by HandlerRegistry for capability-based handler selection.
        """
        return "project-base"
    
    def can_handle(self, source_path: Path) -> bool:
        """
        [Class method intent]
        Determines if this handler can process project-base source paths.
        Acts as universal fallback handler accepting paths not handled by specialized handlers.

        [Design principles]
        Universal fallback capability ensuring all project content can be processed.
        Non-specialized path handling supporting general project directory processing.

        [Implementation details]
        Returns True for all paths not explicitly handled by specialized handlers.
        Serves as fallback handler in warn-and-skip architecture.
        """
        # Project-base handler accepts all paths not handled by specialized handlers
        # In practice, this is controlled by the HandlerRegistry ordering
        return not self._is_specialized_path(source_path)
    
    def get_knowledge_path(self, target_path: Path, source_root: Path) -> Path:
        """
        [Class method intent]
        Calculates knowledge file path for project-base target using handler-specific logic.
        Provides project-base specific knowledge file placement for proper hierarchy organization.

        [Design principles]
        Project-base specific path calculation ensuring knowledge files are placed in project-base directories.
        Mirrored directory structure maintaining relationship between source and knowledge hierarchies.
        Handler-controlled file placement eliminating hardcoded path assumptions.

        [Implementation details]
        Creates mirrored structure in .knowledge/project-base/ directory.
        Uses root_kb.md for project root and directory_kb.md for subdirectories.
        Returns absolute path for project-base knowledge file creation and management.
        """
        # Calculate relative path from source root
        if target_path == source_root:
            # Project root gets root_kb.md
            knowledge_root = source_root / ".knowledge" / "project-base"
            return knowledge_root / "root_kb.md"
        else:
            # Subdirectories get mirrored structure with directory_kb.md
            relative_path = target_path.relative_to(source_root)
            knowledge_dir = source_root / ".knowledge" / "project-base" / relative_path
            return knowledge_dir / f"{target_path.name}_kb.md"
    
    def get_cache_path(self, file_path: Path, source_root: Path) -> Path:
        """
        [Class method intent]
        Calculates analysis cache path for project-base files using handler-specific logic.
        Provides project-base specific cache organization aligned with project structure.

        [Design principles]
        Project-base cache organization maintaining relationship between source and cache files.
        Mirrored cache structure enabling efficient cache operations and cleanup.
        Handler-controlled cache placement ensuring proper isolation from other content types.

        [Implementation details]
        Creates mirrored cache structure in .knowledge/project-base/ hierarchy.
        Maintains relationship between source files and corresponding cache files.
        Returns absolute path for project-base cache file creation and management.
        """
        # Calculate relative path from source root
        relative_path = file_path.relative_to(source_root)
        
        # Cache files go in mirrored structure with .analysis.md suffix
        cache_filename = f"{file_path.name}.analysis.md"
        cache_path = source_root / ".knowledge" / "project-base" / relative_path.parent / cache_filename
        return cache_path
    
    def should_process_item(self, item_path: Path, source_root: Path) -> bool:
        """
        [Class method intent]
        Determines if project-base item should be processed based on handler-specific rules.
        Delegates to existing project-base filtering logic ensuring consistent behavior.

        [Design principles]
        Handler-specific filtering enabling project-base exclusions and configuration rules.
        Consistent filtering behavior maintaining existing processing logic.

        [Implementation details]
        Delegates to should_process_project_item() method for consistent filtering.
        Uses source_root as project root for filtering context.
        """
        return self.should_process_project_item(item_path, source_root)
    
    async def process_structure(self, source_path: Path, ctx: Context) -> DirectoryContext:
        """
        [Class method intent]
        Processes project-base structure returning DirectoryContext for indexing.
        Delegates to existing project-base processing logic ensuring consistent behavior.

        [Design principles]
        Handler-specific processing enabling project-base unified DirectoryContext building.
        Consistent processing behavior maintaining existing processing logic.

        [Implementation details]
        Delegates to process_project_structure() method for unified processing.
        Returns structured context ready for Plan-then-Execute architecture.
        """
        return await self.process_project_structure(source_path, ctx)
    
    async def find_orphaned_files(self, source_root: Path, ctx: Context) -> List[Path]:
        """
        [Class method intent]
        Finds orphaned files in project-base managed areas for cleanup operations.
        Implements project-base specific orphaned file detection and cleanup logic.

        [Design principles]
        Project-base specific cleanup ensuring only appropriate files are identified for removal.
        Safe cleanup operations preventing accidental deletion of project files.

        [Implementation details]
        Scans project-base directories for knowledge and cache files without corresponding sources.
        Validates orphaned status using project-base specific validation logic.
        Returns list of confirmed orphaned files ready for safe deletion.
        """
        orphaned_files = []
        
        try:
            # Find orphaned knowledge files in project-base structure
            knowledge_base_dir = source_root / ".knowledge" / "project-base"
            if knowledge_base_dir.exists():
                for knowledge_file in knowledge_base_dir.rglob("*.md"):
                    source_file = self.map_knowledge_to_source(knowledge_file, source_root)
                    if source_file is None or not source_file.exists():
                        orphaned_files.append(knowledge_file)
                        await ctx.debug(f"Found orphaned project-base knowledge file: {knowledge_file}")
                
                # Find orphaned cache files
                for cache_file in knowledge_base_dir.rglob("*.analysis.md"):
                    source_file = self.map_cache_to_source(cache_file, source_root)
                    if source_file is None or not source_file.exists():
                        orphaned_files.append(cache_file)
                        await ctx.debug(f"Found orphaned project-base cache file: {cache_file}")
        
        except Exception as e:
            logger.warning(f"Project-base orphaned file detection failed for {source_root}: {e}")
        
        return orphaned_files
    
    def map_knowledge_to_source(self, knowledge_path: Path, source_root: Path) -> Optional[Path]:
        """
        [Class method intent]
        Maps project-base knowledge file back to corresponding source path for validation.
        Implements project-base specific reverse path mapping for cleanup operations.

        [Design principles]
        Project-base specific reverse mapping supporting validation and cleanup operations.
        Robust error handling returning None for invalid or unresolvable paths.

        [Implementation details]
        Calculates corresponding source path from project-base knowledge file location.
        Uses project-base mirrored structure knowledge for accurate reverse mapping.
        Returns None for paths that cannot be resolved to valid project-base sources.
        """
        try:
            # Check if it's a project-base knowledge file
            knowledge_base_dir = source_root / ".knowledge" / "project-base"
            if not str(knowledge_path).startswith(str(knowledge_base_dir)):
                return None
            
            if knowledge_path.name == "root_kb.md":
                # Root knowledge file maps to project root
                return source_root
            elif knowledge_path.name.endswith("_kb.md"):
                # Directory knowledge file maps to corresponding directory
                relative_path = knowledge_path.relative_to(knowledge_base_dir)
                source_path = source_root / relative_path.parent
                return source_path
            
            return None
        except Exception:
            return None
    
    def map_cache_to_source(self, cache_path: Path, source_root: Path) -> Optional[Path]:
        """
        [Class method intent]
        Maps project-base cache file back to corresponding source path for validation.
        Implements project-base specific reverse cache mapping for cleanup operations.

        [Design principles]
        Project-base specific cache mapping supporting validation and cleanup operations.
        Robust error handling returning None for invalid or unresolvable paths.

        [Implementation details]
        Calculates corresponding source path from project-base cache file location.
        Uses project-base mirrored cache structure knowledge for accurate reverse mapping.
        Returns None for paths that cannot be resolved to valid project-base sources.
        """
        try:
            # Check if it's a project-base cache file
            knowledge_base_dir = source_root / ".knowledge" / "project-base"
            if not str(cache_path).startswith(str(knowledge_base_dir)):
                return None
            
            if cache_path.name.endswith(".analysis.md"):
                # Extract relative path from cache structure
                cache_relative = cache_path.relative_to(knowledge_base_dir)
                
                # Remove .analysis.md suffix to get original filename
                original_name = cache_path.name.replace(".analysis.md", "")
                
                # Reconstruct source path
                source_path = source_root / cache_relative.parent / original_name
                return source_path
            
            return None
        except Exception:
            return None
    
    # Helper methods (existing and new functionality)
    def _is_specialized_path(self, path: Path) -> bool:
        """
        [Class method intent]
        Determines if path requires specialized handling by other handlers.
        Enables project-base handler to avoid processing specialized content types.

        [Design principles]
        Specialized path detection supporting proper handler delegation.
        Clear separation between general project content and specialized content types.

        [Implementation details]
        Checks for git-clone paths and other specialized content type patterns.
        Returns True if path should be handled by specialized handlers.
        """
        try:
            path_parts = path.parts
            # Check for git-clone paths
            if '.knowledge' in path_parts and 'git-clones' in path_parts:
                return True
            # Add other specialized path checks here as needed
            return False
        except Exception:
            return False
    
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
        Processes entire project directory structure using unified DirectoryContext building approach.
        Uses same processing logic as GitCloneHandler with project-base specific filtering
        ensuring identical leaf-first processing and Plan-then-Execute integration.

        [Design principles]
        Unified DirectoryContext building ensuring consistent leaf-first processing across handlers.
        Project-base specific filtering preserving system directory exclusions during unified processing.
        Comprehensive project traversal enabling complete codebase knowledge coverage.
        Error handling ensuring processing continues despite individual item failures.

        [Implementation details]
        Delegates to unified _build_unified_directory_context() method with project-base filter.
        Uses identical processing logic as git-clone handler for consistent DirectoryContext structure.
        Handles large codebase scenarios with progress reporting and status updates.
        Returns structured context for integration with Plan-then-Execute architecture.
        """
        await ctx.info(f"Processing project structure: {project_root}")
        
        try:
            # Use unified DirectoryContext building with project-base specific filtering
            return await _build_unified_directory_context(
                directory_path=project_root,
                filter_func=lambda item_path, root_path: self.should_process_project_item(item_path, root_path),
                handler=self,
                ctx=ctx,
                handler_name="project-base",
                source_root=project_root
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
        placement for whole project codebase indexing scenarios with root_kb.md naming.

        [Design principles]
        Consistent knowledge file placement following hierarchical conventions.
        Project-base root naming using root_kb.md for clear identification of project-level summary.
        Knowledge base organization enabling clear separation of project content.

        [Implementation details]
        Generates project knowledge base path within .knowledge/project-base/ structure.
        Uses root_kb.md naming convention for project root knowledge files.
        Returns Path object for project knowledge file creation and management.
        """
        # Project knowledge files go in .knowledge/project-base/
        knowledge_root = project_root / ".knowledge" / "project-base"
        return knowledge_root / "root_kb.md"

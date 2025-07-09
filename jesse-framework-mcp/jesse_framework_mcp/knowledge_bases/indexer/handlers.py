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
# Simplified content handlers for different indexing source types.
# Implements clean handler interface supporting two-subphase discovery
# with project-base and git-clone content processing capabilities.
###############################################################################
# [Source file design principles]
# - Single responsibility per handler type
# - Clean abstract interface for extensibility  
# - Reuse existing path utilities from shared_utilities
# - Exception-first error handling with clear failure reasons
# - Efficient knowledge area scanning with proper exclusions
###############################################################################
# [Source file constraints]
# - Must support two-subphase discovery pattern
# - No FastMCP dependencies for clean architecture
# - Must handle both knowledge and cache file types
# - Exception-first error handling - no fallback mechanisms
###############################################################################
# [Dependencies]
# <system>:pathlib.Path
# <system>:typing.List
# <system>:typing.Optional
# <system>:abc.ABC
# <system>:abc.abstractmethod
# <system>:os.path.getmtime
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.KnowledgeFile
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.ValidationResult
# <codebase>:jesse_framework_mcp.knowledge_bases.indexing.shared_utilities.handler_path_manager.HandlerPathManager
# <codebase>:jesse_framework_mcp.knowledge_bases.indexing.shared_utilities.timestamp_manager.TimestampManager
###############################################################################
# [GenAI tool change history]
# 2025-07-09T13:29:00Z : Initial handler implementation by CodeAssistant
# * Created IndexingHandler abstract base class with discovery methods
# * Implemented ProjectHandler for project-base content processing
# * Added GitCloneHandler for git-clone repository handling
# * Integrated with existing shared utilities for path management
###############################################################################

from pathlib import Path
from typing import List, Optional
from abc import ABC, abstractmethod
import os

from .models import BaseIndexedFile, AnalysisFile, KnowledgeBaseFile, ValidationResult
from ..indexing.shared_utilities.handler_path_manager import HandlerPathManager
from ..indexing.shared_utilities.timestamp_manager import TimestampManager


class IndexingHandler(ABC):
    """
    [Class intent]
    Abstract base class for indexing handlers supporting two-subphase discovery.
    Defines interface for knowledge area scanning, source validation, and
    path resolution for different content types.

    [Design principles]
    Clean abstract interface for extensible handler system.
    Separation of concerns between discovery and validation.
    Reuse existing utilities for path management and validation.

    [Implementation details]
    Abstract methods enforce implementation of all required behaviors.
    Concrete handlers implement specific logic for their content types.
    Uses existing shared utilities for consistency and reliability.
    """
    
    @abstractmethod
    def get_type(self) -> str:
        """
        [Class method intent]
        Return string identifier for this handler type.

        [Design principles]
        Enables handler identification and registry management.
        
        [Implementation details]
        Must return consistent string for handler type identification.
        """
        pass
    
    @abstractmethod
    def can_handle(self, source_path: Path) -> bool:
        """
        [Class method intent]
        Determine if this handler can process the given source path.

        [Design principles]
        Handler selection based on source path characteristics.
        
        [Implementation details]
        Returns True if handler is appropriate for source path.
        """
        pass
    
    # Tree-based discovery support methods
    @abstractmethod
    def get_knowledge_directory_path(self, source_root: Path) -> Path:
        """
        [Class method intent]
        Return the knowledge directory path for this handler type.

        [Design principles]
        Consistent knowledge directory structure per handler.
        
        [Implementation details]
        Returns path to handler's knowledge directory (e.g., .knowledge/project-base).
        """
        pass
    
    # Path calculation methods
    @abstractmethod
    def get_knowledge_path(self, source_path: Path, source_root: Path) -> Path:
        """
        [Class method intent]
        Calculate knowledge file path for given source path.

        [Design principles]
        Consistent path calculation for knowledge file placement.
        
        [Implementation details]
        Returns path where knowledge file should be stored.
        """
        pass
    
    @abstractmethod
    def get_cache_path(self, source_path: Path, source_root: Path) -> Path:
        """
        [Class method intent]
        Calculate cache file path for given source path.

        [Design principles]
        Consistent path calculation for cache file placement.
        
        [Implementation details]
        Returns path where cache file should be stored.
        """
        pass
    
    # Subphase 2 - Source file discovery methods
    @abstractmethod
    def get_source_directories(self, source_root: Path) -> List[Path]:
        """
        [Class method intent]
        Return list of source directories to scan for this handler.

        [Design principles]
        Handler-specific source location identification.
        Enables Subphase 2 source file discovery.
        
        [Implementation details]
        Returns list of directories containing source files for this handler.
        """
        pass
    
    @abstractmethod
    def should_index_file(self, source_file: Path) -> bool:
        """
        [Class method intent]
        Determine if a source file should be indexed by this handler.

        [Design principles]
        File type filtering for indexing decisions.
        Handler-specific indexing rules.
        
        [Implementation details]
        Returns True if source file should have analysis created.
        """
        pass
    
    @abstractmethod
    def get_analysis_path(self, source_file: Path, source_root: Path) -> Path:
        """
        [Class method intent]
        Calculate analysis file path for a given source file.

        [Design principles]
        Consistent analysis file path calculation.
        Enables future AnalysisFile object creation.
        
        [Implementation details]
        Returns path where analysis file should be created for source file.
        """
        pass


class ProjectHandler(IndexingHandler):
    """
    [Class intent]
    Handler for project-base content processing.
    Manages knowledge files for entire codebase with proper exclusions
    and generates root_kb.md for project root directory.

    [Design principles]
    Project-wide content indexing with system directory exclusions.
    Special handling for project root (root_kb.md) vs subdirectories.
    Integration with existing path management utilities.

    [Implementation details]
    Uses HandlerPathManager for consistent path calculations.
    Excludes .git, .knowledge, .coding_assistant directories.
    Handles both root and subdirectory knowledge file naming.
    """
    
    def __init__(self, handler_registry=None):
        """
        [Class method intent]
        Initialize project handler with path management capabilities.

        [Design principles]
        Simple initialization with shared utilities integration.

        [Implementation details]
        Sets up path manager and timestamp manager for handler operations.
        Handler registry is optional for backward compatibility.
        """
        # For new indexer, we'll use direct path calculations instead of shared HandlerPathManager
        # This avoids circular dependency issues with handler registry
        self.handler_registry = handler_registry
        self.timestamp_manager = TimestampManager()
        
        # Project exclusions - directories to skip during indexing
        self.exclusions = {
            '.git', '.knowledge', '.coding_assistant', 
            '__pycache__', '.pytest_cache', 'node_modules',
            '.venv', 'venv', '.env'
        }
    
    def get_type(self) -> str:
        """
        [Class method intent]
        Return handler type identifier for project content.

        [Design principles]
        Consistent type identification for handler registry.
        
        [Implementation details]
        Returns "project" as handler type string.
        """
        return "project"
    
    def can_handle(self, source_path: Path) -> bool:
        """
        [Class method intent]
        Determine if source path is project content (not in exclusions).

        [Design principles]
        Exclusion-based filtering for project content identification.
        
        [Implementation details]
        Returns True if path is not in exclusion list.
        """
        return source_path.name not in self.exclusions
    
    def get_knowledge_directory_path(self, source_root: Path) -> Path:
        """
        [Class method intent]
        Return the knowledge directory path for project handler.

        [Design principles]
        Consistent knowledge directory structure per handler.
        
        [Implementation details]
        Returns path to project-base knowledge directory.
        """
        return source_root / ".knowledge" / "project-base"
    
    def get_knowledge_path(self, source_path: Path, source_root: Path) -> Path:
        """
        [Class method intent]
        Calculate knowledge file path for project source directory.

        [Design principles]
        Consistent knowledge file placement in project-base structure.
        Special handling for project root (root_kb.md).
        
        [Implementation details]
        Direct path calculation avoiding circular dependencies.
        Returns root_kb.md for project root, {dir}_kb.md for subdirectories.
        """
        # Direct path calculation for project content
        project_base_dir = source_root / ".knowledge" / "project-base"
        
        if source_path == source_root:
            # Project root gets root_kb.md
            return project_base_dir / "root_kb.md"
        else:
            # Subdirectories get {dir_name}_kb.md
            rel_path = source_path.relative_to(source_root)
            return project_base_dir / rel_path / f"{source_path.name}_kb.md"
    
    def get_cache_path(self, source_path: Path, source_root: Path) -> Path:
        """
        [Class method intent]
        Calculate cache file path for project source file.

        [Design principles]
        Consistent cache file placement in project-base structure.
        
        [Implementation details]
        Direct path calculation avoiding circular dependencies.
        Returns .analysis.md cache file path.
        """
        # Direct path calculation for project content
        project_base_dir = source_root / ".knowledge" / "project-base"
        rel_path = source_path.relative_to(source_root)
        return project_base_dir / rel_path.parent / f"{source_path.stem}.analysis.md"
    
    # Subphase 2 - Source file discovery implementation
    def get_source_directories(self, source_root: Path) -> List[Path]:
        """
        [Class method intent]
        Return project source directories to scan for indexable files.

        [Design principles]
        Recursive directory scanning with exclusion filtering.
        Project-wide content discovery.
        
        [Implementation details]
        Starts from project root and recursively finds all non-excluded directories.
        """
        source_dirs = []
        
        def scan_directory(directory: Path):
            if not directory.exists() or not directory.is_dir():
                return
            
            # Skip excluded directories
            if directory.name in self.exclusions:
                return
            
            # Add this directory to source dirs
            source_dirs.append(directory)
            
            # Recursively scan subdirectories
            try:
                for item in directory.iterdir():
                    if item.is_dir() and item.name not in self.exclusions:
                        scan_directory(item)
            except PermissionError:
                # Skip directories we can't read
                pass
        
        # Start scanning from project root
        scan_directory(source_root)
        return source_dirs
    
    def should_index_file(self, source_file: Path) -> bool:
        """
        [Class method intent]
        Determine if project source file should be indexed.

        [Design principles]
        File extension and content-based filtering.
        Common source file type recognition.
        
        [Implementation details]
        Returns True for common source code, documentation, and configuration files.
        """
        if not source_file.is_file():
            return False
        
        # Common indexable file extensions
        indexable_extensions = {
            # Source code
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', '.hpp',
            '.cs', '.php', '.rb', '.go', '.rs', '.kt', '.swift', '.scala', '.sh',
            
            # Documentation and markup
            '.md', '.rst', '.txt', '.doc', '.docx', '.pdf',
            
            # Configuration and data
            '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf',
            '.xml', '.html', '.htm', '.css', '.scss', '.less',
            
            # Project files
            '.gitignore', '.dockerignore', 'Dockerfile', 'requirements.txt',
            'package.json', 'pyproject.toml', 'Cargo.toml', 'pom.xml'
        }
        
        # Check file extension
        file_extension = source_file.suffix.lower()
        if file_extension in indexable_extensions:
            return True
        
        # Check for files without extensions that should be indexed
        special_files = {
            'README', 'LICENSE', 'CHANGELOG', 'CONTRIBUTING', 'Dockerfile',
            'Makefile', 'CMakeLists.txt', 'requirements.txt'
        }
        
        if source_file.name in special_files:
            return True
        
        # Skip very large files (> 10MB) for performance
        try:
            if source_file.stat().st_size > 10 * 1024 * 1024:
                return False
        except OSError:
            return False
        
        return False
    
    def get_analysis_path(self, source_file: Path, source_root: Path) -> Path:
        """
        [Class method intent]
        Calculate analysis file path for project source file.

        [Design principles]
        Consistent analysis file path calculation.
        Mirror source directory structure in knowledge area.
        
        [Implementation details]
        Places analysis file in same relative path within project-base knowledge area.
        """
        project_base_dir = source_root / ".knowledge" / "project-base"
        rel_path = source_file.relative_to(source_root)
        return project_base_dir / rel_path.parent / f"{source_file.stem}.analysis.md"
    


class GitCloneHandler(IndexingHandler):
    """
    [Class intent]
    Handler for git-clone repository content processing.
    Manages knowledge files for external git repositories stored in
    .knowledge/git-clones/ with read-only access patterns.

    [Design principles]
    Read-only access to git clone repositories.
    Separate knowledge base structure per repository.
    Integration with existing path management utilities.

    [Implementation details]
    Uses HandlerPathManager for consistent path calculations.
    Never modifies source git repositories (read-only).
    Handles repository-specific knowledge file organization.
    """
    
    def __init__(self, handler_registry=None):
        """
        [Class method intent]
        Initialize git clone handler with path management capabilities.

        [Design principles]
        Simple initialization with shared utilities integration.

        [Implementation details]
        Sets up path manager and timestamp manager for handler operations.
        Handler registry is optional for backward compatibility.
        """
        # For new indexer, we'll use direct path calculations instead of shared HandlerPathManager
        # This avoids circular dependency issues with handler registry
        self.handler_registry = handler_registry
        self.timestamp_manager = TimestampManager()
    
    def get_type(self) -> str:
        """
        [Class method intent]
        Return handler type identifier for git clone content.

        [Design principles]
        Consistent type identification for handler registry.
        
        [Implementation details]
        Returns "gitclone" as handler type string.
        """
        return "gitclone"
    
    def can_handle(self, source_path: Path) -> bool:
        """
        [Class method intent]
        Determine if source path is within git-clones directory but not a .kb file.

        [Design principles]
        Path-based filtering for git clone content identification.
        Excludes .kb files and directories from being treated as source files.
        
        [Implementation details]
        Returns True if path is within .knowledge/git-clones/ structure and not a .kb file.
        """
        path_str = str(source_path)
        # Must be within git-clones directory
        if ".knowledge/git-clones" not in path_str:
            return False
        
        # Exclude .kb files and directories - these are knowledge outputs, not source
        if source_path.name.endswith('.kb') or '.kb/' in path_str:
            return False
            
        return True
    
    def get_knowledge_directory_path(self, source_root: Path) -> Path:
        """
        [Class method intent]
        Return the knowledge directory path for git clone handler.

        [Design principles]
        Consistent knowledge directory structure per handler.
        
        [Implementation details]
        Returns path to git-clones knowledge directory.
        """
        return source_root / ".knowledge" / "git-clones"
    
    def get_knowledge_path(self, source_path: Path, source_root: Path) -> Path:
        """
        [Class method intent]
        Calculate knowledge file path for git clone source directory.

        [Design principles]
        Consistent knowledge file placement in git-clone structure.
        Repository-specific knowledge organization.
        
        [Implementation details]
        Direct path calculation avoiding circular dependencies.
        Returns path within appropriate .kb directory.
        """
        # Direct path calculation for git clone content
        git_clones_dir = source_root / ".knowledge" / "git-clones"
        
        # Extract repository name from source path
        if ".knowledge/git-clones" in str(source_path):
            repo_path = source_path
            while repo_path.parent != git_clones_dir:
                repo_path = repo_path.parent
            repo_name = repo_path.name
        else:
            # This shouldn't happen with proper handler selection
            repo_name = "unknown"
        
        # Calculate path within .kb directory
        kb_dir = git_clones_dir / f"{repo_name}.kb"
        rel_path = source_path.relative_to(git_clones_dir / repo_name)
        
        if source_path == git_clones_dir / repo_name:
            # Repository root gets root_kb.md
            return kb_dir / "root_kb.md"
        else:
            # Subdirectories get {dir_name}_kb.md
            return kb_dir / rel_path / f"{source_path.name}_kb.md"
    
    def get_cache_path(self, source_path: Path, source_root: Path) -> Path:
        """
        [Class method intent]
        Calculate cache file path for git clone source file.

        [Design principles]
        Consistent cache file placement in git-clone structure.
        
        [Implementation details]
        Direct path calculation avoiding circular dependencies.
        Returns .analysis.md cache file path within .kb directory.
        """
        # Direct path calculation for git clone content
        git_clones_dir = source_root / ".knowledge" / "git-clones"
        
        # Extract repository name from source path
        if ".knowledge/git-clones" in str(source_path):
            repo_path = source_path
            while repo_path.parent != git_clones_dir:
                repo_path = repo_path.parent
            repo_name = repo_path.name
        else:
            # This shouldn't happen with proper handler selection
            repo_name = "unknown"
        
        # Calculate path within .kb directory
        kb_dir = git_clones_dir / f"{repo_name}.kb"
        rel_path = source_path.relative_to(git_clones_dir / repo_name)
        return kb_dir / rel_path.parent / f"{source_path.stem}.analysis.md"
    
    # Subphase 2 - Source file discovery implementation
    def get_source_directories(self, source_root: Path) -> List[Path]:
        """
        [Class method intent]
        Return git clone source directories to scan for indexable files.

        [Design principles]
        Repository-based directory scanning.
        Read-only access to git clone repositories.
        
        [Implementation details]
        Scans all git repositories within .knowledge/git-clones/.
        """
        source_dirs = []
        git_clones_dir = source_root / ".knowledge" / "git-clones"
        
        if not git_clones_dir.exists():
            return source_dirs
        
        def scan_repository(repo_dir: Path):
            """Recursively scan a git repository for source directories."""
            if not repo_dir.exists() or not repo_dir.is_dir():
                return
            
            # Skip .git directories and .kb directories (knowledge outputs)
            if repo_dir.name in {'.git', '.kb'} or repo_dir.name.endswith('.kb'):
                return
            
            # Add this directory to source dirs
            source_dirs.append(repo_dir)
            
            # Recursively scan subdirectories
            try:
                for item in repo_dir.iterdir():
                    if item.is_dir():
                        scan_repository(item)
            except PermissionError:
                # Skip directories we can't read
                pass
        
        # Scan each repository in git-clones
        try:
            for repo_item in git_clones_dir.iterdir():
                if repo_item.is_dir() and not repo_item.name.endswith('.kb'):
                    scan_repository(repo_item)
        except OSError:
            # git-clones directory doesn't exist or can't be read
            pass
        
        return source_dirs
    
    def should_index_file(self, source_file: Path) -> bool:
        """
        [Class method intent]
        Determine if git clone source file should be indexed.

        [Design principles]
        File extension and content-based filtering.
        Repository-appropriate file type recognition.
        
        [Implementation details]
        Returns True for common source code, documentation, and configuration files.
        """
        if not source_file.is_file():
            return False
        
        # Similar indexable extensions as ProjectHandler but more focused on code repositories
        indexable_extensions = {
            # Source code (comprehensive for any repository)
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', '.hpp',
            '.cs', '.php', '.rb', '.go', '.rs', '.kt', '.swift', '.scala', '.sh', '.bat',
            '.r', '.R', '.m', '.mm', '.pl', '.lua', '.dart', '.elm', '.clj', '.ml',
            
            # Documentation and markup
            '.md', '.rst', '.txt', '.adoc', '.asciidoc',
            
            # Configuration and data
            '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf',
            '.xml', '.html', '.htm', '.css', '.scss', '.less', '.sass',
            
            # Project and build files
            '.gitignore', '.dockerignore', 'Dockerfile', 'requirements.txt',
            'package.json', 'pyproject.toml', 'Cargo.toml', 'pom.xml',
            'build.gradle', 'CMakeLists.txt', 'Makefile'
        }
        
        # Check file extension
        file_extension = source_file.suffix.lower()
        if file_extension in indexable_extensions:
            return True
        
        # Check for files without extensions that should be indexed
        special_files = {
            'README', 'LICENSE', 'CHANGELOG', 'CONTRIBUTING', 'Dockerfile',
            'Makefile', 'CMakeLists.txt', 'requirements.txt', 'INSTALL',
            'COPYING', 'AUTHORS', 'NEWS', 'HISTORY'
        }
        
        if source_file.name in special_files:
            return True
        
        # Skip very large files (> 5MB for git repos to be more conservative)
        try:
            if source_file.stat().st_size > 5 * 1024 * 1024:
                return False
        except OSError:
            return False
        
        return False
    
    def get_analysis_path(self, source_file: Path, source_root: Path) -> Path:
        """
        [Class method intent]
        Calculate analysis file path for git clone source file.

        [Design principles]
        Consistent analysis file path calculation.
        Repository-specific knowledge organization within .kb structure.
        
        [Implementation details]
        Places analysis file in corresponding .kb directory structure.
        """
        git_clones_dir = source_root / ".knowledge" / "git-clones"
        
        # Extract repository name from source file path
        repo_path = source_file
        while repo_path.parent != git_clones_dir and repo_path.parent != repo_path:
            repo_path = repo_path.parent
        
        if repo_path.parent == git_clones_dir:
            repo_name = repo_path.name
        else:
            # Fallback if path calculation fails
            repo_name = "unknown"
        
        # Calculate relative path within repository
        repo_root = git_clones_dir / repo_name
        rel_path = source_file.relative_to(repo_root)
        
        # Place analysis file in .kb directory structure
        kb_dir = git_clones_dir / f"{repo_name}.kb"
        return kb_dir / rel_path.parent / f"{source_file.stem}.analysis.md"

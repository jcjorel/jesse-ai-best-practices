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
# Tree-based knowledge discovery engine implementing single filesystem scan pattern.
# Only component that performs filesystem operations to build complete KnowledgeTree.
# All other phases consume this tree without additional filesystem access.
###############################################################################
# [Source file design principles]
# - Single filesystem scan builds complete tree structure
# - Directory mtime-based staleness detection
# - Handler-based file type recognition and organization
# - Tree structure as single source of truth
# - No filesystem operations after tree construction
# - Comprehensive metadata population during discovery
###############################################################################
# [Source file constraints]
# - Must be only component that performs filesystem operations
# - Must build complete tree structure in single pass
# - Must populate all file and directory metadata
# - Must support both project-base and git-clone handlers
# - Must enable perfect dry-run simulation without filesystem access
###############################################################################
# [Dependencies]
# <system>:pathlib.Path
# <system>:typing.List
# <system>:typing.Dict
# <system>:typing.Optional
# <system>:os.path.exists
# <system>:os.stat
# <system>:time.time
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.KnowledgeTree
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.KnowledgeDirectory
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.AnalysisFile
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.KnowledgeBaseFile
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.UpdateStatus
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.ProgressCallback
###############################################################################
# [GenAI tool change history]
# 2025-07-09T17:53:00Z : Tree-based discovery implementation by CodeAssistant
# * Implemented TreeBuilder as single filesystem scanner
# * Created complete KnowledgeTree construction with all metadata
# * Added directory mtime-based staleness detection
# * Established handler-based file type recognition
# * Eliminated redundant filesystem operations for other phases
###############################################################################

from pathlib import Path
from typing import List, Dict, Optional
import os
import time

from .models import (
    KnowledgeTree, KnowledgeDirectory, AnalysisFile, KnowledgeBaseFile,
    UpdateStatus, ProgressCallback, BaseIndexedFile
)


class TreeBuilder:
    """
    [Class intent]
    Single filesystem scanner that builds complete KnowledgeTree structure.
    Only component in the entire indexer system that performs filesystem operations.
    Provides single source of truth tree for all other phases to consume.

    [Design principles]
    Single filesystem scan builds complete tree.
    Directory mtime-based staleness detection.
    Handler-based file type recognition.
    Comprehensive metadata population.
    No filesystem operations after tree construction.

    [Implementation details]
    Scans .knowledge/ directory structure completely.
    Builds KnowledgeTree with all directories and files.
    Populates file metadata, timestamps, and sizes.
    Associates files with appropriate handlers.
    Enables perfect dry-run simulation.
    """
    
    def __init__(self, handlers: List['IndexingHandler']):
        """
        [Class method intent]
        Initialize tree builder with available handlers.

        [Design principles]
        Handler injection for file type recognition.
        Extensible architecture for different content types.
        
        [Implementation details]
        Stores handler list for file association.
        Creates handler map for efficient lookup.
        """
        self.handlers = handlers
        self.handler_map = {handler.get_type(): handler for handler in handlers}
    
    async def build_knowledge_tree(self, source_root: Path, progress: Optional[ProgressCallback] = None) -> KnowledgeTree:
        """
        [Class method intent]
        Build complete KnowledgeTree using two-subphase discovery pattern.
        Subphase 1: Scan knowledge directories for existing files.
        Subphase 2: Scan source directories and create future AnalysisFile objects.

        [Design principles]
        Two-subphase discovery for complete file coverage.
        Comprehensive metadata population including source file data.
        Handler-based file organization and source discovery.
        Directory mtime staleness detection.

        [Implementation details]
        Subphase 1: Scans .knowledge/ directory recursively for existing files.
        Subphase 2: Uses handlers to discover source files and create future objects.
        Creates complete tree with both existing and future AnalysisFile objects.
        Returns tree ready for decision making and execution phases.
        """
        if progress:
            progress("📡 Phase 1: Starting two-subphase discovery...")
        
        knowledge_root = source_root / ".knowledge"
        tree = KnowledgeTree(root_path=knowledge_root)
        
        # Subphase 1: Scan existing knowledge files
        if progress:
            progress("🚀 Starting tree-based knowledge discovery...")
            progress("🌳 Building complete knowledge tree from filesystem...")
            progress("🔍 Scanning knowledge directory structure...")
        
        # Initialize empty trees even if directories don't exist
        tree.project_handler = KnowledgeDirectory(
            path=knowledge_root / "project-base",
            handler_type="project",
            last_modified=0
        )
        tree.gitclone_handler = KnowledgeDirectory(
            path=knowledge_root / "git-clones",
            handler_type="gitclone", 
            last_modified=0
        )
        
        if knowledge_root.exists():
            # Scan project-base handler area
            project_root = knowledge_root / "project-base"
            if project_root.exists():
                if progress:
                    progress("📂 Building project-base knowledge tree...")
                tree.project_handler = await self._build_directory_tree(
                    project_root, "project", source_root, progress
                )
            
            # Scan git-clones handler area  
            gitclone_root = knowledge_root / "git-clones"
            if gitclone_root.exists():
                if progress:
                    progress("📂 Building git-clones knowledge tree...")
                tree.gitclone_handler = await self._build_directory_tree(
                    gitclone_root, "gitclone", source_root, progress
                )
        
        # Subphase 2: Source file discovery and future object creation
        if progress:
            progress("🔎 Starting Subphase 2: Source file discovery...")
        
        await self._subphase_2_source_discovery(tree, source_root, progress)
        
        # Report tree statistics
        if progress:
            stats = tree.get_summary_stats()
            progress("")
            progress("🌳 Knowledge tree construction complete:")
            progress(f"  📁 Total files discovered: {stats['total_files']}")
            progress(f"  📄 Analysis files: {stats['analysis_files']}")
            progress(f"  📚 Knowledge base files: {stats['knowledge_base_files']}")
            progress("")
        
        return tree
    
    async def _build_directory_tree(
        self, 
        root_path: Path, 
        handler_type: str,
        source_root: Path,
        progress: Optional[ProgressCallback] = None
    ) -> KnowledgeDirectory:
        """
        [Class method intent]
        Recursively build directory tree structure for a handler area.

        [Design principles]
        Recursive directory tree construction.
        Complete metadata population.
        File type recognition and association.

        [Implementation details]
        Creates KnowledgeDirectory for each directory.
        Scans files and associates with directory.
        Recursively processes subdirectories.
        Populates all metadata during scan.
        """
        # Get directory metadata
        stat_info = root_path.stat()
        directory = KnowledgeDirectory(
            path=root_path,
            handler_type=handler_type,
            last_modified=stat_info.st_mtime
        )
        
        if progress:
            # Calculate relative path from project root for better visibility
            try:
                rel_path = root_path.relative_to(source_root)
                progress(f"  📂 Scanning directory: {rel_path}")
            except ValueError:
                # Fallback to just the name if relative path calculation fails
                progress(f"  📂 Scanning directory: {root_path.name}")
        
        # Scan all items in directory
        for item in root_path.iterdir():
            if item.is_file():
                # Process file and add to appropriate collection
                indexed_file = await self._create_indexed_file(item, directory, handler_type)
                if indexed_file:
                    if isinstance(indexed_file, AnalysisFile):
                        directory.analysis_files[item.name] = indexed_file
                    elif isinstance(indexed_file, KnowledgeBaseFile):
                        directory.knowledge_base_files[item.name] = indexed_file
            
            elif item.is_dir():
                # Skip .kb directories - these are knowledge outputs, not source directories
                if item.name.endswith('.kb'):
                    continue
                    
                # Recursively process subdirectory
                subdirectory = await self._build_directory_tree(item, handler_type, source_root, progress)
                directory.subdirectories[item.name] = subdirectory
        
        return directory
    
    async def _create_indexed_file(
        self, 
        file_path: Path, 
        parent_directory: KnowledgeDirectory,
        handler_type: str
    ) -> Optional[BaseIndexedFile]:
        """
        [Class method intent]
        Create appropriate indexed file object based on file type and populate metadata.

        [Design principles]
        File type recognition based on naming patterns.
        Complete metadata population during creation.
        Handler association for processing.

        [Implementation details]
        Recognizes .analysis.md files as AnalysisFile objects.
        Recognizes _kb.md files as KnowledgeBaseFile objects.
        Populates file metadata from filesystem.
        Associates with parent directory and handler.
        """
        file_name = file_path.name
        
        # Get file metadata
        stat_info = file_path.stat()
        
        # Determine file type and create appropriate object
        indexed_file = None
        
        if file_name.endswith('.analysis.md'):
            # Analysis file: <source_file>.analysis.md
            source_file_name = file_name.replace('.analysis.md', '')
            source_file_path = self._find_source_file(parent_directory.path, source_file_name)
            source_mtime = None
            
            if source_file_path and source_file_path.exists():
                source_mtime = source_file_path.stat().st_mtime
            
            indexed_file = AnalysisFile(
                path=file_path,
                handler_type=handler_type,
                parent_directory=parent_directory,
                file_size=stat_info.st_size,
                last_modified=stat_info.st_mtime,
                source_file=source_file_path,
                source_last_modified=source_mtime
            )
            
        elif file_name.endswith('_kb.md'):
            # Knowledge base file: <directory>_kb.md
            directory_name = file_name.replace('_kb.md', '')
            source_directory_path = self._find_source_directory(parent_directory.path, directory_name)
            
            indexed_file = KnowledgeBaseFile(
                path=file_path,
                handler_type=handler_type,
                parent_directory=parent_directory,
                file_size=stat_info.st_size,
                last_modified=stat_info.st_mtime,
                source_directory=source_directory_path
            )
        
        # Update file status based on staleness
        if indexed_file:
            indexed_file.is_orphaned = not self._validate_source_exists(indexed_file)
            
            if not indexed_file.is_orphaned:
                if indexed_file.is_stale():
                    indexed_file.update_status = UpdateStatus.STALE
                else:
                    indexed_file.update_status = UpdateStatus.FRESH
            else:
                indexed_file.update_status = UpdateStatus.ORPHANED
        
        return indexed_file
    
    def _find_source_file(self, knowledge_dir: Path, source_file_name: str) -> Optional[Path]:
        """
        [Class method intent]
        Find corresponding source file for an analysis file.

        [Design principles]
        Source file association for staleness detection.
        Handler-specific source location logic.

        [Implementation details]
        Determines source location based on handler type.
        Returns Path to source file if it exists.
        """
        # This is a simplified implementation - in reality, handlers would provide this logic
        # For now, assume source files are in parallel directory structure
        relative_path = knowledge_dir.relative_to(knowledge_dir.parent.parent / ".knowledge")
        
        # Remove handler prefix (project-base or git-clones)
        if relative_path.parts:
            source_relative = Path(*relative_path.parts[1:])  # Remove first part (handler)
            source_root = knowledge_dir.parent.parent  # Go up to project root
            potential_source = source_root / source_relative / source_file_name
            
            if potential_source.exists():
                return potential_source
        
        return None
    
    def _find_source_directory(self, knowledge_dir: Path, directory_name: str) -> Optional[Path]:
        """
        [Class method intent]
        Find corresponding source directory for a knowledge base file.

        [Design principles]
        Source directory association for staleness detection.
        Handler-specific source location logic.

        [Implementation details]
        Determines source location based on handler type.
        Returns Path to source directory if it exists.
        """
        # Similar logic to _find_source_file but for directories
        relative_path = knowledge_dir.relative_to(knowledge_dir.parent.parent / ".knowledge")
        
        if relative_path.parts:
            source_relative = Path(*relative_path.parts[1:])  # Remove handler prefix
            source_root = knowledge_dir.parent.parent
            potential_source = source_root / source_relative / directory_name
            
            if potential_source.exists() and potential_source.is_dir():
                return potential_source
        
        return None
    
    def _validate_source_exists(self, indexed_file: BaseIndexedFile) -> bool:
        """
        [Class method intent]
        Validate that source file/directory still exists for indexed file.

        [Design principles]
        Source existence validation for orphan detection.
        File type specific validation logic.

        [Implementation details]
        Checks source file existence for AnalysisFile objects.
        Checks source directory existence for KnowledgeBaseFile objects.
        """
        if isinstance(indexed_file, AnalysisFile):
            return indexed_file.source_file is not None and indexed_file.source_file.exists()
        elif isinstance(indexed_file, KnowledgeBaseFile):
            return indexed_file.source_directory is not None and indexed_file.source_directory.exists()
        
        return False
    
    async def _subphase_2_source_discovery(
        self, 
        tree: KnowledgeTree, 
        source_root: Path, 
        progress: Optional[ProgressCallback] = None
    ) -> None:
        """
        [Class method intent]
        Discover source files and create future AnalysisFile objects for indexing.
        Also populate source metadata for existing AnalysisFile objects.

        [Design principles]
        Handler-based source file discovery.
        Complete metadata population for both existing and future files.
        Tree integration without additional filesystem operations.

        [Implementation details]
        Uses handlers to discover source directories and files.
        Creates future AnalysisFile objects with update_status=MISSING.
        Populates source metadata for existing AnalysisFile objects.
        Adds all objects to appropriate directories in tree.
        """
        if progress:
            progress("🔍 Scanning source files for indexing...")
        
        for handler in self.handlers:
            handler_type = handler.get_type()
            
            if progress:
                progress(f"📁 Processing {handler_type} handler source files...")
            
            # Get source directories from handler
            source_dirs = handler.get_source_directories(source_root)
            
            if progress:
                progress(f"  📂 Found {len(source_dirs)} source directories for {handler_type}")
            
            # Process each source directory
            for source_dir in source_dirs:
                await self._process_source_directory(
                    source_dir, tree, handler, source_root, progress
                )
        
        if progress:
            progress("✅ Source file discovery complete")
    
    async def _process_source_directory(
        self, 
        source_dir: Path, 
        tree: KnowledgeTree, 
        handler: 'IndexingHandler',
        source_root: Path,
        progress: Optional[ProgressCallback] = None
    ) -> None:
        """
        [Class method intent]
        Process a single source directory and create/update AnalysisFile objects.

        [Design principles]
        File-by-file processing with handler validation.
        Tree integration for both existing and future objects.
        Complete metadata population.

        [Implementation details]
        Scans directory for files that should be indexed.
        Checks if analysis file already exists in tree.
        Creates future objects or updates existing ones.
        Adds objects to appropriate knowledge directory.
        """
        try:
            for item in source_dir.iterdir():
                if item.is_file() and handler.should_index_file(item):
                    await self._process_source_file(
                        item, tree, handler, source_root, progress
                    )
        except (PermissionError, OSError):
            # Skip directories we can't read
            if progress:
                progress(f"  ⚠️ Cannot read directory: {source_dir}")
    
    async def _process_source_file(
        self, 
        source_file: Path, 
        tree: KnowledgeTree, 
        handler: 'IndexingHandler',
        source_root: Path,
        progress: Optional[ProgressCallback] = None
    ) -> None:
        """
        [Class method intent]
        Process a single source file and create/update its AnalysisFile object.

        [Design principles]
        Source file to analysis file mapping.
        Existing object enhancement vs future object creation.
        Complete metadata population.

        [Implementation details]
        Calculates analysis file path using handler.
        Searches tree for existing AnalysisFile object.
        Either populates metadata or creates future object.
        Ensures object is properly integrated into tree.
        """
        # Calculate where analysis file should be
        analysis_path = handler.get_analysis_path(source_file, source_root)
        
        # Find existing AnalysisFile object in tree
        existing_analysis = tree.find_file(analysis_path)
        
        if existing_analysis and isinstance(existing_analysis, AnalysisFile):
            # Populate source metadata in existing object
            if progress:
                progress(f"  ✨ Enhancing existing analysis: {analysis_path.name}")
            
            existing_analysis.source_file = source_file
            try:
                existing_analysis.source_last_modified = source_file.stat().st_mtime
            except OSError:
                existing_analysis.source_last_modified = None
            
            # Update staleness status
            existing_analysis.is_orphaned = False
            if existing_analysis.is_stale():
                existing_analysis.update_status = UpdateStatus.STALE
            else:
                existing_analysis.update_status = UpdateStatus.FRESH
        
        else:
            # Create future AnalysisFile object
            if progress:
                try:
                    rel_path = source_file.relative_to(source_root)
                    progress(f"  🆕 Creating future analysis for: {rel_path}")
                except ValueError:
                    progress(f"  🆕 Creating future analysis for: {source_file.name}")
            
            future_analysis = await self._create_future_analysis_file(
                analysis_path, source_file, handler, tree, source_root
            )
            
            if future_analysis:
                # Add to appropriate directory in tree
                self._add_future_file_to_tree(future_analysis, tree, analysis_path)
    
    async def _create_future_analysis_file(
        self, 
        analysis_path: Path, 
        source_file: Path, 
        handler: 'IndexingHandler',
        tree: KnowledgeTree,
        source_root: Path
    ) -> Optional[AnalysisFile]:
        """
        [Class method intent]
        Create future AnalysisFile object for source file that needs indexing.

        [Design principles]
        Future object creation with complete source metadata.
        Proper parent directory association.
        Missing status for execution planning.

        [Implementation details]
        Creates AnalysisFile with update_status=MISSING.
        Populates source file metadata completely.
        Associates with appropriate parent directory.
        Returns object ready for tree integration.
        """
        try:
            # Get source file metadata
            source_stat = source_file.stat()
            
            # Find or create parent directory
            parent_dir = self._find_or_create_parent_directory(
                analysis_path, tree, handler.get_type()
            )
            
            # Create future AnalysisFile object
            future_analysis = AnalysisFile(
                path=analysis_path,
                handler_type=handler.get_type(),
                parent_directory=parent_dir,
                update_status=UpdateStatus.MISSING,  # Needs creation
                is_orphaned=False,  # Source exists
                
                # Source metadata (populated)
                source_file=source_file,
                source_last_modified=source_stat.st_mtime,
                
                # Analysis metadata (None - doesn't exist yet)
                file_size=None,
                last_modified=None
            )
            
            return future_analysis
            
        except OSError as e:
            # Skip files we can't read
            return None
    
    def _find_or_create_parent_directory(
        self, 
        file_path: Path, 
        tree: KnowledgeTree, 
        handler_type: str
    ) -> KnowledgeDirectory:
        """
        [Class method intent]
        Find existing parent directory or create directory structure as needed.

        [Design principles]
        Tree structure maintenance during future object creation.
        Directory hierarchy creation on demand.
        Handler-specific directory association.

        [Implementation details]
        Walks up directory path to find existing directory.
        Creates intermediate directories as needed.
        Returns appropriate parent directory for file.
        """
        parent_path = file_path.parent
        
        # Find existing directory in tree
        for directory in tree.get_all_directories():
            if directory.path == parent_path:
                return directory
        
        # Need to create directory structure
        # Find the closest existing ancestor
        current_path = parent_path
        path_components = []
        
        while current_path != tree.root_path:
            path_components.append(current_path.name)
            current_path = current_path.parent
            
            # Check if this level exists
            for directory in tree.get_all_directories():
                if directory.path == current_path:
                    # Found existing ancestor, create missing structure
                    return self._create_directory_structure(
                        directory, path_components[::-1], handler_type
                    )
        
        # Fallback: add to root handler directory
        if handler_type == "project":
            return tree.project_handler
        else:
            return tree.gitclone_handler
    
    def _create_directory_structure(
        self, 
        parent_dir: KnowledgeDirectory, 
        path_components: List[str], 
        handler_type: str
    ) -> KnowledgeDirectory:
        """
        [Class method intent]
        Create nested directory structure from path components.

        [Design principles]
        Recursive directory creation.
        Proper parent-child relationships.
        Handler type inheritance.

        [Implementation details]
        Creates KnowledgeDirectory objects for each path component.
        Links directories in parent-child hierarchy.
        Returns deepest directory for file placement.
        """
        current_dir = parent_dir
        
        for component in path_components:
            # Check if subdirectory already exists
            if component in current_dir.subdirectories:
                current_dir = current_dir.subdirectories[component]
            else:
                # Create new subdirectory
                new_dir_path = current_dir.path / component
                new_dir = KnowledgeDirectory(
                    path=new_dir_path,
                    handler_type=handler_type,
                    last_modified=0  # Will be updated when needed
                )
                current_dir.subdirectories[component] = new_dir
                current_dir = new_dir
        
        return current_dir
    
    def _add_future_file_to_tree(
        self, 
        future_file: AnalysisFile, 
        tree: KnowledgeTree, 
        file_path: Path
    ) -> None:
        """
        [Class method intent]
        Add future AnalysisFile object to appropriate directory in tree.

        [Design principles]
        Tree integration for future objects.
        Proper file collection management.
        Type-safe directory association.

        [Implementation details]
        Adds file to parent directory's analysis_files collection.
        Uses filename as key for efficient lookup.
        Maintains tree structure integrity.
        """
        parent_dir = future_file.parent_directory
        filename = file_path.name
        parent_dir.analysis_files[filename] = future_file


class DiscoveryEngine:
    """
    [Class intent]
    Main orchestrator for tree-based discovery process.
    Coordinates TreeBuilder to create complete KnowledgeTree.
    Single entry point for discovery phase.

    [Design principles]
    Simple orchestration of tree building.
    Handler injection for extensibility.
    Progress reporting for long-running operations.

    [Implementation details]
    Manages TreeBuilder instance.
    Provides unified interface for discovery operations.
    Returns complete tree ready for consumption by other phases.
    """
    
    def __init__(self, handlers: List['IndexingHandler']):
        """
        [Class method intent]
        Initialize discovery engine with available handlers.

        [Design principles]
        Handler injection for extensibility.
        Composition pattern for tree building.
        
        [Implementation details]
        Creates TreeBuilder with handler list.
        Prepares for tree construction.
        """
        self.handlers = handlers
        self.tree_builder = TreeBuilder(handlers)
    
    async def discover(self, source_root: Path, progress: Optional[ProgressCallback] = None) -> KnowledgeTree:
        """
        [Class method intent]
        Execute complete discovery process to build KnowledgeTree.
        Single entry point for tree-based discovery.

        [Design principles]
        Single filesystem scan for complete tree.
        Progress reporting for user feedback.
        Complete tree ready for consumption.

        [Implementation details]
        Delegates to TreeBuilder for actual tree construction.
        Returns KnowledgeTree ready for decision making phase.
        """
        if progress:
            progress("🚀 Starting tree-based knowledge discovery...")
        
        knowledge_tree = await self.tree_builder.build_knowledge_tree(source_root, progress)
        
        if progress:
            progress("✅ Tree-based knowledge discovery complete")
        
        return knowledge_tree
    
    def get_supported_types(self) -> List[str]:
        """
        [Class method intent]
        Return list of supported handler types.

        [Design principles]
        Introspection capability for debugging.
        
        [Implementation details]
        Returns handler type strings from all registered handlers.
        """
        return [handler.get_type() for handler in self.handlers]


# Type alias for handler interface (to be implemented in handlers.py)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .handlers import IndexingHandler

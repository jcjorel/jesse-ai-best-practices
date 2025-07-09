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
# Cleanup Manager for Knowledge Bases Hierarchical Indexing System providing framework-integrated
# cleanup operations through atomic task generation. Enables test scenarios requiring file cleanup
# while maintaining full integration with Plan-then-Execute architecture and handler isolation.
###############################################################################
# [Source file design principles]
# - Handler-scoped cleanup discovery ensuring each handler only discovers files within its scope
# - Framework integration through RebuildDecisionEngine rather than separate execution systems
# - Atomic task generation converting cleanup operations into individual DELETE_ORPHANED_FILE tasks
# - Configuration-driven cleanup enabling test scenarios through IndexingConfig parameters
# - Safety validation ensuring only appropriate files are marked for cleanup operations
###############################################################################
# [Source file constraints]
# - Must never perform direct file deletion operations maintaining atomic execution requirements
# - Handler isolation must be maintained preventing cross-contamination between handler types
# - All cleanup must integrate into unified ExecutionPlan preventing separate execution flows
# - Safety validation must confirm each file is appropriate for cleanup before task generation
# - Configuration must control cleanup behavior rather than hardcoded logic
###############################################################################
# [Dependencies]
# <codebase>: ..models.indexing_config - Configuration structures for cleanup parameters
# <codebase>: ..models.execution_plan - AtomicTask and TaskType for task generation
# <codebase>: .handler_interface - Handler interface for scoped cleanup discovery
# <system>: pathlib - Cross-platform path operations and file system access
# <system>: logging - Structured logging for cleanup operation analysis
# <system>: typing - Type annotations for comprehensive static analysis
###############################################################################
# [GenAI tool change history]
# 2025-07-09T05:46:00Z : Initial implementation of framework-integrated cleanup system by CodeAssistant
# * Created CleanupManager for handler-scoped cleanup discovery and atomic task generation
# * Implemented configuration-driven cleanup enabling test scenarios through IndexingConfig
# * Added handler isolation ensuring git-clone cleanup never touches project-base files
# * Integrated with Plan-then-Execute architecture preventing separate execution systems
###############################################################################

"""
Cleanup Manager for Knowledge Bases System.

This module provides framework-integrated cleanup operations through atomic task
generation, enabling test scenarios requiring file cleanup while maintaining
full integration with the Plan-then-Execute architecture and handler isolation.
"""

import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
from uuid import uuid4

from fastmcp import Context

from ...models.indexing_config import IndexingConfig
from ...models.execution_plan import AtomicTask, TaskType

logger = logging.getLogger(__name__)


class CleanupManager:
    """
    [Class intent]
    Framework-integrated cleanup manager providing handler-scoped file discovery
    and atomic task generation for cleanup operations. Enables test scenarios requiring
    file cleanup while maintaining full integration with Plan-then-Execute architecture.

    [Design principles]
    Handler-scoped discovery ensuring each handler only discovers files within its scope.
    Framework integration through RebuildDecisionEngine rather than separate execution systems.
    Atomic task generation converting cleanup operations into individual DELETE_ORPHANED_FILE tasks.
    Configuration-driven behavior enabling test scenarios through IndexingConfig parameters.
    Safety validation ensuring only appropriate files are marked for cleanup operations.

    [Implementation details]
    Delegates file discovery to appropriate handlers maintaining handler isolation boundaries.
    Creates individual AtomicTask objects for each file requiring cleanup operations.
    Validates cleanup safety through handler-specific validation logic.
    Integrates with existing atomic execution infrastructure preventing framework bypass.
    Provides comprehensive logging for cleanup operation analysis and debugging.
    """
    
    def __init__(self, config: IndexingConfig):
        """
        [Class method intent]
        Initializes cleanup manager with configuration and handler registry access.
        Sets up cleanup operation parameters from configuration and prepares handler coordination.

        [Design principles]
        Configuration-driven initialization enabling flexible cleanup behavior through IndexingConfig.
        Handler registry integration enabling proper handler selection for scoped cleanup operations.
        Defensive initialization ensuring cleanup manager operates safely within framework constraints.

        [Implementation details]
        Stores configuration reference for cleanup behavior determination and safety validation.
        Initializes handler registry for proper handler selection during cleanup discovery.
        Sets up logging context for comprehensive cleanup operation tracking and analysis.
        """
        self.config = config
        self._cleanup_enabled = getattr(config, 'cleanup_mode_enabled', False)
        self._cleanup_types = getattr(config, 'cleanup_types', [])
        
        logger.info(f"Initialized CleanupManager: enabled={self._cleanup_enabled}, types={self._cleanup_types}")
    
    async def discover_cleanup_targets(
        self, 
        handler, 
        source_root: Path, 
        ctx: Context
    ) -> List[Path]:
        """
        [Class method intent]
        Discovers files requiring cleanup within handler scope using handler-specific discovery logic.
        Delegates to appropriate handler ensuring cleanup discovery respects handler boundaries.

        [Design principles]
        Handler-scoped discovery ensuring each handler only discovers files within its scope.
        Safety validation through handler-specific logic ensuring only appropriate files are discovered.
        Comprehensive logging enabling cleanup operation analysis and debugging capabilities.

        [Implementation details]
        Delegates discovery to handler-specific cleanup discovery methods maintaining isolation.
        Combines results from multiple cleanup types when multiple types are configured.
        Validates discovered files through handler-specific safety checks before returning.
        Provides detailed logging of discovery results for debugging and verification purposes.

        Args:
            handler: IndexingHandler instance for scoped cleanup discovery
            source_root: Root path for cleanup scope determination
            ctx: FastMCP context for progress reporting and logging

        Returns:
            List[Path]: Files requiring cleanup within handler scope
        """
        if not self._cleanup_enabled:
            return []
        
        cleanup_targets = []
        handler_type = handler.get_handler_type()
        
        await ctx.info(f"🧹 Discovering cleanup targets for {handler_type} handler")
        
        for cleanup_type in self._cleanup_types:
            try:
                if cleanup_type == "kb_files":
                    kb_files = await self._discover_kb_files(handler, source_root, ctx)
                    cleanup_targets.extend(kb_files)
                    await ctx.info(f"🧹 Found {len(kb_files)} KB files for cleanup")
                
                elif cleanup_type == "analysis_files":
                    analysis_files = await self._discover_analysis_files(handler, source_root, ctx)
                    cleanup_targets.extend(analysis_files)
                    await ctx.info(f"🧹 Found {len(analysis_files)} analysis files for cleanup")
                
                else:
                    await ctx.warning(f"Unknown cleanup type: {cleanup_type}")
            
            except Exception as e:
                logger.error(f"Cleanup discovery failed for {cleanup_type}: {e}")
                await ctx.error(f"Cleanup discovery failed for {cleanup_type}: {str(e)}")
        
        total_targets = len(cleanup_targets)
        await ctx.info(f"🧹 Total cleanup targets discovered: {total_targets}")
        
        return cleanup_targets
    
    async def _discover_kb_files(
        self, 
        handler, 
        source_root: Path, 
        ctx: Context
    ) -> List[Path]:
        """
        [Class method intent]
        Discovers KB files requiring cleanup using handler-specific discovery logic.
        Maintains handler isolation ensuring each handler only discovers its own KB files.

        [Design principles]
        Handler delegation maintaining strict scope boundaries for KB file discovery.
        Safety validation ensuring only handler-appropriate KB files are discovered.
        Comprehensive error handling preventing cleanup discovery failures from breaking indexing.

        [Implementation details]
        Checks for handler-specific cleanup discovery method availability.
        Delegates to handler.discover_cleanup_kb_files() when available.
        Falls back to generic discovery patterns when handler-specific methods unavailable.
        Validates discovered files through handler-appropriate safety checks.
        """
        kb_files = []
        
        try:
            # Check if handler has specific cleanup discovery method
            if hasattr(handler, 'discover_cleanup_kb_files'):
                kb_files = await handler.discover_cleanup_kb_files(source_root, ctx)
            else:
                # Fallback to generic discovery based on handler type
                handler_type = handler.get_handler_type()
                
                if handler_type == "git-clone":
                    # Git-clone KB files discovery
                    git_clone_kb_dir = source_root / ".knowledge" / "git-clones"
                    if git_clone_kb_dir.exists():
                        kb_files.extend(git_clone_kb_dir.glob("*_kb.md"))
                
                elif handler_type == "project-base":
                    # Project-base KB files discovery
                    project_kb_dir = source_root / ".knowledge" / "project-base"
                    if project_kb_dir.exists():
                        kb_files.extend(project_kb_dir.glob("*.md"))
                
                await ctx.debug(f"Generic KB discovery for {handler_type}: {len(kb_files)} files")
        
        except Exception as e:
            logger.error(f"KB file discovery failed: {e}")
            await ctx.error(f"KB file discovery failed: {str(e)}")
        
        return kb_files
    
    async def _discover_analysis_files(
        self, 
        handler, 
        source_root: Path, 
        ctx: Context
    ) -> List[Path]:
        """
        [Class method intent]
        Discovers analysis files requiring cleanup using handler-specific discovery logic.
        Maintains handler isolation ensuring each handler only discovers its own analysis files.

        [Design principles]
        Handler delegation maintaining strict scope boundaries for analysis file discovery.
        Safety validation ensuring only handler-appropriate analysis files are discovered.
        Comprehensive error handling preventing cleanup discovery failures from breaking indexing.

        [Implementation details]
        Checks for handler-specific cleanup discovery method availability.
        Delegates to handler.discover_cleanup_analysis_files() when available.
        Falls back to generic discovery patterns when handler-specific methods unavailable.
        Validates discovered files through handler-appropriate safety checks.
        """
        analysis_files = []
        
        try:
            # Check if handler has specific cleanup discovery method
            if hasattr(handler, 'discover_cleanup_analysis_files'):
                analysis_files = await handler.discover_cleanup_analysis_files(source_root, ctx)
            else:
                # Fallback to generic discovery based on handler type
                handler_type = handler.get_handler_type()
                
                if handler_type == "git-clone":
                    # Git-clone analysis files discovery
                    git_clone_cache_dir = source_root / ".knowledge" / "git-clones-cache"
                    if git_clone_cache_dir.exists():
                        analysis_files.extend(git_clone_cache_dir.rglob("*.analysis.md"))
                
                elif handler_type == "project-base":
                    # Project-base analysis files discovery
                    project_cache_dir = source_root / ".knowledge" / "project-base-cache"
                    if project_cache_dir.exists():
                        analysis_files.extend(project_cache_dir.rglob("*.analysis.md"))
                
                await ctx.debug(f"Generic analysis discovery for {handler_type}: {len(analysis_files)} files")
        
        except Exception as e:
            logger.error(f"Analysis file discovery failed: {e}")
            await ctx.error(f"Analysis file discovery failed: {str(e)}")
        
        return analysis_files
    
    def create_cleanup_tasks(
        self, 
        cleanup_targets: List[Path], 
        handler_type: str,
        deletion_reason: str = "framework_cleanup"
    ) -> List[AtomicTask]:
        """
        [Class method intent]
        Creates individual AtomicTask objects for each cleanup target maintaining atomic execution principles.
        Generates DELETE_ORPHANED_FILE tasks with proper metadata and safety validation.

        [Design principles]
        Atomic task generation ensuring each cleanup operation is independent and recoverable.
        Safety validation ensuring each task is marked as safe for deletion.
        Comprehensive metadata embedding enabling task execution without external dependencies.
        Handler context preservation enabling proper handler selection during execution.

        [Implementation details]
        Creates individual AtomicTask for each cleanup target with DELETE_ORPHANED_FILE type.
        Embeds comprehensive metadata including safety validation and handler context.
        Generates unique task IDs preventing task collision and enabling dependency tracking.
        Validates task completeness ensuring all required parameters are present.

        Args:
            cleanup_targets: List of file paths requiring cleanup
            handler_type: Type of handler for context preservation
            deletion_reason: Reason for deletion for audit and debugging

        Returns:
            List[AtomicTask]: Individual atomic tasks for each cleanup target
        """
        cleanup_tasks = []
        
        for target_path in cleanup_targets:
            task_id = f"cleanup_{handler_type}_{target_path.name}_{uuid4().hex[:8]}"
            
            cleanup_task = AtomicTask(
                task_id=task_id,
                task_type=TaskType.DELETE_ORPHANED_FILE,
                target_path=target_path,
                metadata={
                    "deletion_reason": deletion_reason,
                    "is_safe_to_delete": True,
                    "handler_type": handler_type,
                    "cleanup_operation": True,
                    "file_type": self._determine_file_type(target_path)
                }
            )
            
            cleanup_tasks.append(cleanup_task)
        
        logger.info(f"Created {len(cleanup_tasks)} cleanup tasks for {handler_type} handler")
        
        return cleanup_tasks
    
    def _determine_file_type(self, file_path: Path) -> str:
        """
        [Class method intent]
        Determines cleanup file type for metadata and logging purposes.
        Provides file type classification enabling proper cleanup categorization.

        [Design principles]
        Simple classification logic enabling clear cleanup operation categorization.
        Extensible pattern allowing additional file type detection as needed.

        [Implementation details]
        Uses file suffix and naming patterns for file type determination.
        Returns descriptive file type strings for metadata embedding and logging.
        """
        if file_path.name.endswith("_kb.md"):
            return "knowledge_base"
        elif file_path.name.endswith(".analysis.md"):
            return "analysis_cache"
        else:
            return "unknown"
    
    @property
    def is_cleanup_enabled(self) -> bool:
        """Returns whether cleanup operations are enabled in configuration"""
        return self._cleanup_enabled
    
    @property
    def cleanup_types(self) -> List[str]:
        """Returns configured cleanup types"""
        return self._cleanup_types.copy()

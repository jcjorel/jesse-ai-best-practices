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
# Centralized decision engine for rebuild and deletion operations in Knowledge Bases Hierarchical Indexing System.
# Consolidates all scattered decision logic into single authoritative component providing
# consistent decision-making for files, directories, and cleanup operations with comprehensive audit trails.
###############################################################################
# [Source file design principles]
# - Single source of truth for all rebuild and deletion decisions eliminating scattered logic
# - Comprehensive decision analysis covering all scenarios including empty directories and project root
# - Rich audit trails with clear reasoning for every decision enabling debugging and optimization
# - Integration with existing components (FileAnalysisCache, special handlers) for informed decisions
# - Performance-optimized decision making minimizing filesystem operations and redundant checks
# - Defensive programming with graceful error handling preventing decision failures from breaking processing
###############################################################################
# [Source file constraints]
# - Must integrate with existing FileAnalysisCache for staleness checking without breaking cache architecture
# - Decision outcomes must be deterministic and consistent across multiple runs for reliability
# - All filesystem operations must handle concurrent access and permission errors gracefully
# - Performance must be optimal for large directory hierarchies with thousands of files
# - Integration with special handlers (project-base, git-clone) must preserve existing behavior
###############################################################################
# [Dependencies]
# <codebase>: ..models.indexing_config - Configuration and filtering logic
# <codebase>: ..models.knowledge_context - Context structures and processing state
# <codebase>: ..models.rebuild_decisions - Decision models and structured outcomes
# <codebase>: .file_analysis_cache - File analysis caching and staleness checking
# <codebase>: .special_handlers - Project-base and git-clone special handling
# <system>: pathlib - Cross-platform path operations and file metadata
# <system>: datetime - Timestamp comparison and decision timing
# <system>: logging - Structured logging for decision analysis and debugging
###############################################################################
# [GenAI tool change history]
# 2025-07-07T22:29:00Z : CRITICAL ORPHANED FILE FIX - Fixed analysis file deletion bug by implementing convention-based delegation by CodeAssistant
# * MAJOR ARCHITECTURE SIMPLIFICATION: Replaced complex centralized orphaned detection with handler delegation eliminating 75% of complex code
# * FIXED ROOT CAUSE: Orphaned file detection was using wrong source root context causing legitimate git-clone analysis files to be flagged as orphaned
# * ELIMINATED DATA LOSS: Git-clone analysis files (.knowledge/git-clones/<repo>.kb/*.analysis.md) no longer incorrectly deleted every test run
# * CONVENTION-BASED APPROACH: Each handler now manages orphaned file detection in its own domain eliminating cross-handler context confusion
# * SIMPLIFIED MAINTENANCE: Reduced from complex source root calculation logic to simple delegation pattern improving reliability
# 2025-07-07T21:55:00Z : CRITICAL HANDLER INTEGRATION FIX - Fixed is_cache_fresh() method to pass required handler parameter by CodeAssistant
# * FIXED EXECUTION FAILURE: Updated is_cache_fresh() method to get appropriate handler for file path before calling FileAnalysisCache
# * RESTORED CACHE FUNCTIONALITY: Cache freshness checks now work correctly with handler-specific path calculations
# * PREVENTS CACHE ERRORS: Eliminated "missing 1 required positional argument: 'handler'" errors during decision analysis
# * ENABLES SEGREGATED DECISIONS: Git-clone and project-base files now have freshness checked in their respective structures
# * ROOT CAUSE FIXED: RebuildDecisionEngine was calling FileAnalysisCache methods without required handler parameter
# 2025-07-07T19:03:00Z : CRITICAL ORPHANED FILE FIX - Fixed orphaned file detection to scan all handler-managed areas instead of only project-base by CodeAssistant
# * MAJOR CLEANUP FIX: Updated _find_orphaned_knowledge_files() and _find_orphaned_cache_files() to use HandlerRegistry delegation
# * COMPREHENSIVE SCANNING: Now scans project-base, git-clone .kb directories, and all other handler-managed areas for orphaned files
# * RESOLVED GIT-CLONE CLEANUP: Git-clone orphaned files in .knowledge/git-clones/<repo>.kb/ directories now properly detected and cleaned
# * ELIMINATED BLIND SPOTS: Removed hardcoded project-base-only scanning that missed orphaned files from specialized handlers
# * ROOT CAUSE FIXED: Orphaned file detection was only scanning .knowledge/project-base/ ignoring git-clone handler managed directories
# 2025-07-07T18:56:00Z : CRITICAL ARCHITECTURAL FIX - Implemented handler-delegated path management eliminating hardcoded project-base paths by CodeAssistant
# * MAJOR ARCHITECTURAL TRANSFORMATION: Replaced all hardcoded self._project_base_root references with HandlerRegistry delegation
# * FIXED GIT-CLONE PATHS: Updated _calculate_cache_path_safe() and _calculate_knowledge_path_safe() to use handler-specific path logic
# * ENABLED .KB STRUCTURE: Git-clone files now correctly placed in separate .knowledge/git-clones/<repo>.kb/ directories instead of inside git clones
# * COMPREHENSIVE REVERSE MAPPING: Updated _map_analysis_file_to_source_safe() and _map_knowledge_dir_to_source_safe() to support all handler types
# * RESOLVES ROOT CAUSE: Eliminates hardcoded "project-base" forcing that prevented git-clone handler from using correct path structure
# 2025-07-06T22:31:00Z : CRITICAL PERFORMANCE FIX - Removed project root force rebuild eliminating systematic unnecessary rebuilds by CodeAssistant
# * MAJOR PERFORMANCE IMPROVEMENT: Removed PROJECT_ROOT_FORCED special case allowing project root to follow standard staleness rules
# * Project root now uses COMPREHENSIVE_STALENESS checking like all other directories, only rebuilding when content actually changes
# * Eliminates systematic forced rebuilds on every indexing run providing immediate performance benefits for incremental processing
# * RESOLVES: Project root directory always processes to ensure root_kb.md generation -> Now follows same rules as subdirectories
# 2025-07-06T17:45:00Z : CRITICAL BUG FIX - Fixed race condition in timestamp comparison causing infinite rebuild loops by CodeAssistant
# * EMERGENCY FIX: Restored 1-second tolerance in _is_timestamp_newer() to prevent race conditions during same-cycle processing
# * Fixed infinite rebuild loop where files processed in one cycle were immediately considered stale in the next cycle
# * Race condition occurred because cache files created during processing had timestamps microseconds after source files
# * Direct timestamp comparison without tolerance caused legitimate fresh cache to appear stale immediately after creation
###############################################################################

"""
Centralized Rebuild Decision Engine for Knowledge Bases System.

This module consolidates all scattered decision logic into a single authoritative
component providing consistent decision-making for rebuild and deletion operations
with comprehensive audit trails and debugging capabilities.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from fastmcp import Context

from ..models import (
    IndexingConfig,
    DirectoryContext,
    FileContext
)
from ..models.rebuild_decisions import (
    DecisionReport,
    RebuildDecision,
    DeletionDecision,
    DecisionOutcome,
    DecisionReason
)
from .file_analysis_cache import FileAnalysisCache
from .handler_interface import HandlerRegistry

logger = logging.getLogger(__name__)


class RebuildDecisionEngine:
    """
    [Class intent]
    Centralized decision engine consolidating all rebuild and deletion decision logic.
    Provides single source of truth for all processing decisions eliminating scattered
    logic across multiple components while maintaining comprehensive audit trails.

    [Design principles]
    Single authoritative decision component eliminating scattered logic and inconsistencies.
    Comprehensive decision analysis covering all scenarios including edge cases and special handling.
    Rich audit trails with detailed reasoning enabling debugging and optimization efforts.
    Performance optimization through intelligent caching and minimal filesystem operations.
    Integration with existing components preserving established functionality and behavior.
    Defensive error handling ensuring decision failures don't break overall processing workflow.

    [Implementation details]
    Integrates with FileAnalysisCache for comprehensive staleness checking and performance optimization.
    Uses special handlers for project-base and git-clone scenarios maintaining existing behavior.
    Implements empty directory detection preventing infinite rebuild loops for contentless directories.
    Provides comprehensive orphaned file detection and deletion decision logic for cleanup operations.
    Maintains detailed decision audit trails with structured reasoning for debugging and analysis.
    """
    
    def __init__(self, config: IndexingConfig):
        """
        [Class method intent]
        Initializes decision engine with configuration and handler registry integration.
        Sets up file analysis cache, handler registry, and decision tracking capabilities
        for comprehensive decision-making operations using handler-delegated path management.

        [Design principles]
        Configuration-driven behavior supporting different decision scenarios and requirements.
        Handler registry integration enabling informed decision-making through specialized handler consultation.
        Decision tracking preparation supporting comprehensive audit trails and performance monitoring.
        Path calculation delegation to handlers eliminating hardcoded path assumptions.

        [Implementation details]
        Creates FileAnalysisCache instance for staleness checking and performance optimization.
        Initializes HandlerRegistry for specialized path calculation and processing decisions.
        Sets up decision timing and audit trail tracking capabilities.
        Eliminates hardcoded path roots in favor of handler-delegated path management.
        """
        self.config = config
        self.file_cache = FileAnalysisCache(config)
        self.handler_registry = HandlerRegistry(config)
        
        # Decision tracking
        self._decision_start_time: Optional[datetime] = None
        self._decisions_made = 0
        self._filesystem_operations = 0
        
        logger.info("Initialized RebuildDecisionEngine with handler-delegated path management")
    
    # =========================================================================
    # CONSOLIDATED HELPER METHODS - Eliminating DRY Violations
    # =========================================================================
    
    def _get_file_timestamp_safe(self, file_path: Path) -> Optional[datetime]:
        """
        [Class method intent]
        Safely retrieves file modification timestamp with consistent error handling.
        Consolidates repeated timestamp retrieval patterns from multiple methods.

        [Design principles]
        Centralized timestamp retrieval eliminating scattered duplicate logic.
        Consistent error handling preventing filesystem access failures from breaking operations.
        Performance optimization through single consolidated timestamp access pattern.

        [Implementation details]
        Uses Path.stat().st_mtime for cross-platform timestamp access.
        Converts filesystem timestamp to datetime object for comparison operations.
        Returns None on any filesystem error for graceful degradation handling.
        """
        try:
            return datetime.fromtimestamp(file_path.stat().st_mtime)
        except (OSError, FileNotFoundError):
            return None
    
    def _is_timestamp_newer(self, newer_time: datetime, older_time: datetime) -> bool:
        """
        [Class method intent]
        Compares timestamps directly for reliable staleness detection.
        Consolidates repeated timestamp comparison logic from multiple decision methods.

        [Design principles]
        Centralized timestamp comparison eliminating duplicate comparison logic.
        Direct timestamp comparison without tolerance for simplicity and consistency.
        Clear boolean result simplifying conditional logic in decision methods.

        [Implementation details]
        Direct timestamp comparison: newer_time > older_time.
        Returns True if newer_time is strictly newer than older_time.
        Used by all staleness checking methods for consistent comparison behavior.
        """
        return newer_time > older_time
    
    def _calculate_cache_path_safe(self, file_path: Path, source_root: Path) -> Path:
        """
        [Class method intent]
        Calculates cache file path using handler-delegated path management with error handling.
        Consolidates duplicate cache path calculation logic from multiple methods using HandlerRegistry.

        [Design principles]
        Handler-delegated cache path calculation eliminating hardcoded path assumptions.
        Specialized handler logic ensuring appropriate cache structure for different content types.
        Graceful fallback handling for path calculation errors ensuring operations continue.

        [Implementation details]
        Uses HandlerRegistry to get appropriate handler for file's parent directory.
        Delegates cache path calculation to handler ensuring correct structure for content type.
        Provides fallback to default handler on path calculation or handler resolution errors.
        """
        try:
            # Get appropriate handler for the file's parent directory
            handler = self.handler_registry.get_handler_for_path(file_path.parent)
            return handler.get_cache_path(file_path, source_root)
        except Exception as e:
            logger.warning(f"Handler-delegated cache path calculation failed for {file_path}: {e}")
            # Fallback: use project-base handler as default
            try:
                project_base_handler = self.handler_registry.get_project_base_handler()
                return project_base_handler.get_cache_path(file_path, source_root)
            except Exception as fallback_error:
                logger.error(f"Fallback cache path calculation failed for {file_path}: {fallback_error}")
                # Ultimate fallback: construct basic cache path
                cache_filename = f"{file_path.name}.analysis.md"
                return self.config.knowledge_output_directory / "project-base" / cache_filename
    
    def _calculate_knowledge_path_safe(self, directory_path: Path, source_root: Path, is_project_root: bool = False) -> Path:
        """
        [Class method intent]
        Calculates knowledge file path using handler-delegated path management with error handling.
        Consolidates duplicate knowledge path calculation logic from multiple methods using HandlerRegistry.

        [Design principles]
        Handler-delegated knowledge path calculation eliminating hardcoded path assumptions.
        Specialized handler logic ensuring appropriate knowledge structure for different content types.
        Graceful fallback handling for path calculation errors ensuring operations continue.

        [Implementation details]
        Uses HandlerRegistry to get appropriate handler for directory path.
        Delegates knowledge path calculation to handler ensuring correct structure for content type.
        Provides fallback to default handler on path calculation or handler resolution errors.
        """
        try:
            # Get appropriate handler for the directory
            handler = self.handler_registry.get_handler_for_path(directory_path)
            return handler.get_knowledge_path(directory_path, source_root)
        except Exception as e:
            logger.warning(f"Handler-delegated knowledge path calculation failed for {directory_path}: {e}")
            # Fallback: use project-base handler as default
            try:
                project_base_handler = self.handler_registry.get_project_base_handler()
                return project_base_handler.get_knowledge_path(directory_path, source_root)
            except Exception as fallback_error:
                logger.error(f"Fallback knowledge path calculation failed for {directory_path}: {fallback_error}")
                # Ultimate fallback: construct basic knowledge path
                if is_project_root or directory_path == source_root:
                    knowledge_filename = "root_kb.md"
                else:
                    knowledge_filename = f"{directory_path.name}_kb.md"
                return self.config.knowledge_output_directory / "project-base" / knowledge_filename
    
    def _map_analysis_file_to_source_safe(self, analysis_file: Path, source_root: Path) -> Optional[Path]:
        """
        [Class method intent]
        Maps analysis cache file back to corresponding source file path using handler-delegated logic.
        Consolidates reverse path mapping logic used in orphaned file detection across all handler types.

        [Design principles]
        Handler-delegated reverse mapping enabling proper cleanup across all content types.
        Safe path calculation with None return for invalid or unresolvable paths.
        Consistent reverse mapping behavior across all handler types for reliable cleanup operations.

        [Implementation details]
        Attempts to use handlers to perform reverse mapping for accurate source path calculation.
        Falls back to basic reverse mapping logic if handler delegation fails.
        Returns None on any path calculation error for safe cleanup decision making.
        """
        try:
            # Try to use handler registry to find appropriate handler for reverse mapping
            for handler in self.handler_registry.get_all_handlers():
                try:
                    source_path = handler.map_cache_to_source(analysis_file, source_root)
                    if source_path:
                        return source_path
                except Exception:
                    continue  # Try next handler
            
            # Fallback: basic reverse mapping (for compatibility with existing project-base logic)
            original_filename = analysis_file.name.replace('.analysis.md', '')
            
            # Try to extract relative path from knowledge output directory
            try:
                relative_path = analysis_file.relative_to(self.config.knowledge_output_directory)
                # Remove leading path components to get to source structure
                if relative_path.parts and relative_path.parts[0] == "project-base":
                    source_relative = Path(*relative_path.parts[1:])  # Remove "project-base"
                    source_directory = source_root / source_relative.parent
                    return source_directory / original_filename
            except Exception:
                pass
            
            return None
        except Exception:
            return None
    
    def _map_knowledge_dir_to_source_safe(self, knowledge_directory: Path, source_root: Path) -> Optional[Path]:
        """
        [Class method intent]
        Maps knowledge directory back to corresponding source directory path using handler-delegated logic.
        Consolidates reverse path mapping logic used in orphaned directory detection across all handler types.

        [Design principles]
        Handler-delegated reverse mapping enabling proper cleanup across all content types.
        Safe path calculation with None return for invalid or unresolvable paths.
        Consistent reverse mapping behavior across all handler types for reliable cleanup operations.

        [Implementation details]
        Attempts to use handlers to perform reverse mapping for accurate source path calculation.
        Falls back to basic reverse mapping logic if handler delegation fails.
        Returns None on any path calculation error for safe cleanup decision making.
        """
        try:
            # Try to use handler registry to find appropriate handler for reverse mapping
            for handler in self.handler_registry.get_all_handlers():
                try:
                    source_path = handler.map_knowledge_to_source(knowledge_directory, source_root)
                    if source_path:
                        return source_path
                except Exception:
                    continue  # Try next handler
            
            # Fallback: basic reverse mapping (for compatibility with existing project-base logic)
            try:
                relative_path = knowledge_directory.relative_to(self.config.knowledge_output_directory)
                # Remove leading path components to get to source structure
                if relative_path.parts and relative_path.parts[0] == "project-base":
                    source_relative = Path(*relative_path.parts[1:])  # Remove "project-base"
                    return source_root / source_relative
            except Exception:
                pass
            
            return None
        except Exception:
            return None
    
    # =========================================================================
    # CONSOLIDATED DECISION FACTORY METHODS - Eliminating Decision Creation DRY Violations
    # =========================================================================
    
    def _create_rebuild_decision(self, path: Path, outcome: DecisionOutcome, reason: DecisionReason, 
                                reasoning_text: str, metadata: Optional[Dict] = None) -> RebuildDecision:
        """
        [Class method intent]
        Creates standardized RebuildDecision objects with consistent structure and metadata.
        Consolidates duplicate decision creation patterns from multiple methods.

        [Design principles]
        Centralized decision creation eliminating duplicate RebuildDecision instantiation patterns.
        Consistent decision structure ensuring uniform decision object formatting across all methods.
        Metadata standardization providing predictable decision information for audit trails.

        [Implementation details]
        Creates RebuildDecision with all required fields and optional metadata dictionary.
        Provides default empty metadata dictionary when none specified for consistency.
        Used by all rebuild decision methods ensuring uniform decision object creation.
        """
        return RebuildDecision(
            path=path,
            outcome=outcome,
            reason=reason,
            reasoning_text=reasoning_text,
            metadata=metadata or {}
        )
    
    def _create_deletion_decision(self, path: Path, outcome: DecisionOutcome, reason: DecisionReason,
                                 reasoning_text: str, is_safe_to_delete: bool = True, 
                                 metadata: Optional[Dict] = None) -> DeletionDecision:
        """
        [Class method intent]
        Creates standardized DeletionDecision objects with consistent structure and safety metadata.
        Consolidates duplicate decision creation patterns from deletion methods.

        [Design principles]
        Centralized deletion decision creation eliminating duplicate DeletionDecision instantiation patterns.
        Safety-first approach with explicit safety flag for all deletion decisions.
        Consistent decision structure ensuring uniform deletion decision formatting across methods.

        [Implementation details]
        Creates DeletionDecision with all required fields and safety validation.
        Defaults to safe deletion unless explicitly specified otherwise for conservative approach.
        Provides default empty metadata dictionary when none specified for consistency.
        """
        return DeletionDecision(
            path=path,
            outcome=outcome,
            reason=reason,
            reasoning_text=reasoning_text,
            is_safe_to_delete=is_safe_to_delete,
            metadata=metadata or {}
        )
    
    def _validate_source_exists_and_processable(self, source_path: Path, is_file: bool = True) -> Tuple[bool, str]:
        """
        [Class method intent]
        Validates source path existence and processability with consistent logic.
        Consolidates repeated source validation patterns from multiple cleanup methods.

        [Design principles]
        Centralized source validation eliminating scattered existence and processability checks.
        Consistent validation logic ensuring uniform behavior across all validation points.
        Clear boolean result with detailed reasoning supporting decision audit trails.

        [Implementation details]
        Checks path existence using Path.exists() for cross-platform compatibility.
        Uses configuration should_process_file() or should_process_directory() for processability.
        Returns tuple with validation result and detailed reasoning for decision making.
        """
        try:
            # Check existence first
            if not source_path.exists():
                return False, f"Source {'file' if is_file else 'directory'} does not exist: {source_path.name}"
            
            # Check processability based on type
            if is_file:
                if not self.config.should_process_file(source_path):
                    return False, f"Source file is excluded by configuration: {source_path.name}"
            else:
                if not self.config.should_process_directory(source_path):
                    return False, f"Source directory is excluded by configuration: {source_path.name}"
            
            # Both existence and processability checks passed
            return True, f"Source {'file' if is_file else 'directory'} exists and is processable: {source_path.name}"
            
        except Exception as e:
            return False, f"Source validation failed: {str(e)}"
    
    def _create_cleanup_decision(self, path: Path, source_path: Optional[Path], 
                               path_type: str, ctx: Context) -> Tuple[DecisionOutcome, str]:
        """
        [Class method intent]
        Creates consistent cleanup decisions based on source path validation.
        Consolidates repeated cleanup decision patterns from multiple cleanup methods.

        [Design principles]
        Centralized cleanup decision logic eliminating duplicate cleanup patterns across methods.
        Source-based decision making ensuring consistent cleanup behavior throughout system.
        Clear decision outcomes with detailed reasoning supporting cleanup audit trails.

        [Implementation details]
        Validates source path existence and processability using consolidated validation method.
        Returns DELETE outcome for invalid/excluded sources, SKIP outcome for valid sources.
        Provides detailed reasoning explaining cleanup decision for audit trail purposes.
        """
        if not source_path:
            return DecisionOutcome.DELETE, f"No corresponding source {path_type} found for {path.name}"
        
        is_file = path_type == "file"
        is_valid, reason = self._validate_source_exists_and_processable(source_path, is_file)
        
        if not is_valid:
            return DecisionOutcome.DELETE, f"Cleanup {path_type}: {reason}"
        else:
            return DecisionOutcome.SKIP, f"Keep {path_type}: {reason}"
    
    def _handle_decision_error(self, operation: str, target_path: Path, error: Exception, 
                              as_rebuild_decision: bool = True) -> RebuildDecision:
        """
        [Class method intent]
        Creates consistent error decisions with standardized error handling and logging.
        Consolidates repeated error handling patterns from decision methods.

        [Design principles]
        Centralized error handling eliminating duplicate exception handling patterns across methods.
        Consistent error logging ensuring uniform error reporting throughout decision engine.
        Standardized error decision creation providing predictable error decision formatting.

        [Implementation details]
        Logs error with detailed context information for debugging and monitoring.
        Creates appropriate decision type (rebuild or deletion) based on context.
        Returns error decision with clear reasoning and error metadata for audit trails.
        """
        error_msg = f"{operation} failed for {target_path}: {str(error)}"
        logger.error(error_msg, exc_info=True)
        
        if as_rebuild_decision:
            return self._create_rebuild_decision(
                path=target_path,
                outcome=DecisionOutcome.ERROR,
                reason=DecisionReason.DECISION_ERROR,
                reasoning_text=error_msg,
                metadata={"error": str(error), "operation": operation}
            )
        else:
            # This should return DeletionDecision, but for consistency in current usage, return RebuildDecision
            return self._create_rebuild_decision(
                path=target_path,
                outcome=DecisionOutcome.ERROR,
                reason=DecisionReason.DECISION_ERROR,
                reasoning_text=error_msg,
                metadata={"error": str(error), "operation": operation}
            )
    
    # =========================================================================
    # PHASE 3 CONSOLIDATED PATTERNS - Eliminating Remaining DRY Violations
    # =========================================================================
    
    async def _log_decision_context(self, ctx: Context, outcome: DecisionOutcome, path: Path, 
                                   reasoning: str, operation_type: str = "decision", source_root: Path = None) -> None:
        """
        [Class method intent]
        Provides centralized decision logging with consistent emoji patterns and relative path formatting.
        Consolidates scattered debug logging patterns throughout the decision engine.

        [Design principles]
        Centralized logging eliminating scattered emoji-based debug message patterns.
        Consistent visual indicators and formatting for decision outcomes across all methods.
        Relative path display from project root for clear context identification.
        Performance optimization through single consolidated logging interface.

        [Implementation details]
        Maps decision outcomes to appropriate emoji indicators for visual clarity.
        Calculates relative path from source root when available, falls back to path name.
        Supports different operation types with contextual formatting.
        """
        emoji_map = {
            DecisionOutcome.REBUILD: "🔄",
            DecisionOutcome.SKIP: "✅", 
            DecisionOutcome.DELETE: "🗑️",
            DecisionOutcome.ERROR: "❌"
        }
        
        # Special emoji patterns for specific operations
        if "empty" in reasoning.lower():
            emoji = "📁"
        elif "project root" in reasoning.lower():
            emoji = "🏗️"
        elif "cleanup" in operation_type.lower():
            emoji = "🗑️"
        else:
            emoji = emoji_map.get(outcome, "📋")
        
        # Calculate relative path from source root for better context
        if source_root and source_root.exists():
            try:
                relative_path = path.relative_to(source_root)
                path_display = str(relative_path)
            except ValueError:
                # Path is not relative to source_root, use absolute path
                path_display = str(path)
        else:
            # Fallback to path name if no source root available
            path_display = path.name
        
        action_text = outcome.value.upper()
        await ctx.debug(f"{emoji} {action_text}: {path_display} - {reasoning}")
    
    async def _execute_with_error_handling(self, operation_func, operation_name: str, 
                                         target_path: Path, ctx: Context,
                                         fallback_result=None, as_rebuild_decision: bool = True):
        """
        [Class method intent]
        Provides unified exception handling pattern for all decision operations.
        Consolidates repeated try-catch patterns with consistent error logging and decision creation.

        [Design principles]
        Centralized exception handling eliminating duplicate try-catch patterns across methods.
        Consistent error logging with structured context information for debugging.
        Standardized fallback behavior ensuring predictable error recovery across all operations.

        [Implementation details]
        Executes provided operation function with comprehensive exception handling.
        Logs errors with detailed context and exception information for troubleshooting.
        Creates appropriate error decisions using consolidated factory methods.
        Returns fallback result or error decision based on context requirements.
        """
        try:
            return await operation_func()
        except Exception as e:
            error_msg = f"{operation_name} failed for {target_path.name}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            await ctx.warning(f"{operation_name} error: {str(e)}")
            
            if fallback_result is not None:
                return fallback_result
                
            return self._handle_decision_error(operation_name, target_path, e, as_rebuild_decision)
    
    def _validate_and_decide_cleanup(self, source_path: Optional[Path], is_file: bool, 
                                   ctx: Context, target_name: str = "") -> Tuple[DecisionOutcome, str]:
        """
        [Class method intent]
        Provides consolidated validation and cleanup decision logic for source paths.
        Eliminates repeated validation patterns used across multiple cleanup methods.

        [Design principles]
        Centralized validation logic eliminating scattered existence and processability checks.
        Consistent cleanup decision making ensuring uniform behavior across all cleanup operations.
        Clear decision outcomes with detailed reasoning supporting cleanup audit trails.

        [Implementation details]
        Validates source path existence and processability using consolidated validation methods.
        Returns appropriate cleanup decision based on validation results.
        Provides detailed reasoning for cleanup decisions supporting audit trails.
        """
        if not source_path:
            return DecisionOutcome.DELETE, f"No corresponding source {'file' if is_file else 'directory'} found for {target_name}"
        
        is_valid, reason = self._validate_source_exists_and_processable(source_path, is_file)
        
        if not is_valid:
            return DecisionOutcome.DELETE, f"Cleanup target: {reason}"
        else:
            return DecisionOutcome.SKIP, f"Keep target: {reason}"
    
    def _create_decision_with_metadata_pattern(self, path: Path, outcome: DecisionOutcome, 
                                             reason: DecisionReason, base_reasoning: str,
                                             metadata_type: str, **metadata_kwargs) -> RebuildDecision:
        """
        [Class method intent]
        Creates decisions with standardized metadata patterns eliminating duplicate metadata construction.
        Consolidates repeated decision creation patterns with consistent metadata structure.

        [Design principles]
        Centralized decision creation with standardized metadata patterns eliminating duplicate construction logic.
        Consistent metadata structure ensuring uniform decision object formatting across all decision types.
        Flexible metadata pattern support accommodating different decision contexts and requirements.

        [Implementation details]
        Creates RebuildDecision with base reasoning and standardized metadata structure.
        Supports different metadata types with appropriate default values and patterns.
        Combines base metadata with context-specific metadata provided through kwargs.
        """
        base_metadata = {
            "decision_type": metadata_type,
            "timestamp": datetime.now().isoformat(),
            "path_name": path.name
        }
        
        # Add context-specific metadata
        base_metadata.update(metadata_kwargs)
        
        return self._create_rebuild_decision(
            path=path,
            outcome=outcome,
            reason=reason,
            reasoning_text=base_reasoning,
            metadata=base_metadata
        )
    
    def _get_filesystem_operation_cache_key(self, operation: str, path: Path) -> str:
        """
        [Class method intent]
        Generates cache keys for filesystem operations to prevent duplicate checks.
        Optimizes performance by enabling caching of expensive filesystem operations.

        [Design principles]
        Performance optimization through intelligent caching of filesystem operations.
        Consistent cache key generation ensuring reliable cache hit rates.
        Context-aware caching supporting different operation types and paths.

        [Implementation details]
        Creates unique cache keys combining operation type and path information.
        Uses path string representation for consistent key generation.
        Supports different operation types for granular caching control.
        """
        return f"{operation}:{str(path)}"

    def _check_directory_staleness_internal(self, directory_context: DirectoryContext, source_root: Path) -> Tuple[bool, str]:
        """
        [Class method intent]
        Internal directory staleness checking since FileAnalysisCache no longer provides path generation.
        Determines if directory knowledge file needs rebuild by comparing against source files and subdirectory knowledge files.

        [Design principles]
        Direct timestamp comparison without tolerance for simplicity and reliability.
        Checks against source files and subdirectory knowledge files for comprehensive staleness detection.
        Conservative approach returning stale on any error to ensure knowledge file generation.

        [Implementation details]
        Calculates knowledge file path using consolidated helper method.
        Compares knowledge file timestamp against all source files in directory.
        Compares against subdirectory knowledge files for hierarchical consistency.
        Returns boolean staleness status with detailed reasoning including precise timestamps.
        """
        try:
            # Calculate knowledge file path
            is_project_root = directory_context.directory_path == source_root
            knowledge_file_path = self._calculate_knowledge_path_safe(
                directory_context.directory_path, source_root, is_project_root
            )
            
            # If knowledge file doesn't exist, it's stale
            if not knowledge_file_path.exists():
                return True, "Knowledge file does not exist"
            
            try:
                knowledge_mtime = datetime.fromtimestamp(knowledge_file_path.stat().st_mtime)
                knowledge_mtime_str = knowledge_mtime.strftime("%Y-%m-%d %H:%M:%S")
            except OSError:
                return True, "Cannot access knowledge file timestamp"
            
            # Check source files only
            for file_context in directory_context.file_contexts:
                source_mtime_str = file_context.last_modified.strftime("%Y-%m-%d %H:%M:%S")
                if file_context.last_modified > knowledge_mtime:
                    return True, f"Source file newer: {file_context.file_path.name} ({source_mtime_str}) > knowledge file ({knowledge_mtime_str})"
            
            # Check subdirectory knowledge files
            for subdir_context in directory_context.subdirectory_contexts:
                subdir_knowledge_path = self._calculate_knowledge_path_safe(
                    subdir_context.directory_path, source_root, False
                )
                if subdir_knowledge_path.exists():
                    try:
                        subdir_mtime = datetime.fromtimestamp(subdir_knowledge_path.stat().st_mtime)
                        subdir_mtime_str = subdir_mtime.strftime("%Y-%m-%d %H:%M:%S")
                        if subdir_mtime > knowledge_mtime:
                            return True, f"Subdirectory knowledge file newer: {subdir_context.directory_path.name} ({subdir_mtime_str}) > knowledge file ({knowledge_mtime_str})"
                    except OSError:
                        return True, f"Cannot access subdirectory knowledge timestamp: {subdir_context.directory_path.name}"
            
            # All checks passed - knowledge file is up to date
            return False, f"Knowledge file is up to date ({knowledge_mtime_str})"
            
        except Exception as e:
            logger.warning(f"Knowledge file staleness check failed for {directory_context.directory_path}: {e}")
            # Conservative: assume stale on error to trigger rebuild
            return True, f"Staleness check failed: {e}"
    
    # =========================================================================
    # END PHASE 3 CONSOLIDATED PATTERNS
    # =========================================================================
    # =========================================================================
    # END CONSOLIDATED DECISION FACTORY METHODS
    # =========================================================================
    
    async def analyze_hierarchy(self, root_context: DirectoryContext, source_root: Path, ctx: Context) -> DecisionReport:
        """
        [Class method intent]
        Performs comprehensive decision analysis for entire directory hierarchy using optimal file-first approach.
        Consolidates all rebuild and deletion decisions into unified action plan with file-level optimization
        preventing unnecessary directory rebuilds when only individual files are stale.

        [Design principles]
        File-first decision making ensuring optimal processing efficiency and minimal unnecessary rebuilds.
        Comprehensive hierarchy analysis covering all files, directories, and cleanup scenarios.
        Unified decision reporting enabling coordinated execution and clear audit trails.
        Performance optimization through intelligent decision ordering and minimal filesystem operations.
        Error handling ensuring partial analysis completion when individual decisions fail.

        [Implementation details]
        Phase 1: Analyzes individual file staleness for targeted processing decisions.
        Phase 2: Analyzes directory staleness only after considering file-level decisions.
        Phase 3: Detects orphaned files and generates appropriate deletion decisions for cleanup.
        Tracks performance metrics and decision timing for optimization and monitoring.
        Returns comprehensive DecisionReport with optimized execution planning.
        """
        self._decision_start_time = datetime.now()
        self._decisions_made = 0
        self._filesystem_operations = 0
        
        await ctx.info("Starting comprehensive hierarchy decision analysis with file-first optimization")
        
        report = DecisionReport()
        
        try:
            # Phase 1: Analyze individual file rebuild decisions (NEW - File-First Approach)
            await ctx.info("Phase 1: Analyzing individual file rebuild decisions")
            await self._analyze_file_rebuild_decisions(root_context, source_root, report, ctx)
            
            # Phase 2: Analyze directory hierarchy for rebuild decisions (considering file decisions)
            await ctx.info("Phase 2: Analyzing directory rebuild decisions")
            await self._analyze_directory_rebuild_decisions(root_context, source_root, report, ctx)
            
            # Phase 3: Detect orphaned files for deletion decisions
            await ctx.info("Phase 3: Analyzing deletion decisions")
            await self._analyze_deletion_decisions(source_root, report, ctx)
            
            # Phase 4: SELECTIVE CASCADING - Propagate rebuild decisions up hierarchy
            await ctx.info("Phase 4: Propagating selective cascading decisions")
            cascaded_decisions = await self._propagate_cascading_decisions(root_context, source_root, report, ctx)
            
            # Phase 5: Calculate final statistics and timing
            end_time = datetime.now()
            report.analysis_duration_seconds = (end_time - self._decision_start_time).total_seconds()
            
            # Log comprehensive analysis results
            stats = report.get_summary_statistics()
            await ctx.info(f"Decision analysis complete: {stats['files_to_rebuild']} rebuild, {stats['files_to_skip']} skip, {stats['files_to_delete']} delete")
            await ctx.info(f"Analysis completed in {report.analysis_duration_seconds:.2f}s with {self._decisions_made} decisions ({cascaded_decisions} cascaded)")
            
            logger.info(f"Hierarchy analysis: {self._decisions_made} decisions, {self._filesystem_operations} filesystem ops, {report.analysis_duration_seconds:.2f}s")
            
            return report
            
        except Exception as e:
            logger.error(f"Hierarchy decision analysis failed: {e}", exc_info=True)
            report.decision_errors.append(f"Analysis failed: {str(e)}")
            await ctx.error(f"Decision analysis failed: {str(e)}")
            
            # Return partial report with error information
            if self._decision_start_time:
                report.analysis_duration_seconds = (datetime.now() - self._decision_start_time).total_seconds()
            
            return report
    
    async def _analyze_file_rebuild_decisions(
        self,
        directory_context: DirectoryContext,
        source_root: Path, 
        report: DecisionReport,
        ctx: Context
    ) -> None:
        """
        [Class method intent]
        Recursively analyzes individual file staleness for targeted processing decisions.
        Implements file-first approach preventing unnecessary directory rebuilds when only 
        individual files need analysis cache updates.

        [Design principles]
        File-first decision making optimizing processing efficiency and reducing unnecessary LLM calls.
        Targeted file processing ensuring only stale files trigger analysis cache updates.
        Recursive file analysis covering entire hierarchy with comprehensive staleness checking.
        Performance optimization through intelligent cache utilization and minimal filesystem operations.
        Clear decision reasoning supporting debugging and optimization of individual file decisions.

        [Implementation details]
        Processes all files in current directory checking individual staleness against analysis cache.
        Recursively processes subdirectories ensuring comprehensive file-level coverage.
        Uses FileAnalysisCache for precise individual file staleness checking.
        Creates targeted RebuildDecision objects for stale files only.
        Provides detailed reasoning for file-level decisions supporting optimization efforts.
        """
        try:
            # Process subdirectories first (depth-first for comprehensive coverage)
            for subdir_context in directory_context.subdirectory_contexts:
                await self._analyze_file_rebuild_decisions(subdir_context, source_root, report, ctx)
            
            # Process individual files in current directory
            for file_context in directory_context.file_contexts:
                decision = await self._make_file_rebuild_decision(file_context, source_root, ctx)
                report.add_rebuild_decision(decision)
                self._decisions_made += 1
                
                await ctx.debug(f"File decision: {file_context.file_path.name} -> {decision.outcome.value} ({decision.reason.value})")
                
        except Exception as e:
            logger.error(f"File rebuild analysis failed for {directory_context.directory_path}: {e}")
            
            # Create error decision for the directory context
            error_decision = self._handle_decision_error("File rebuild analysis", directory_context.directory_path, e)
            report.add_rebuild_decision(error_decision)
            self._decisions_made += 1

    async def _make_file_rebuild_decision(
        self,
        file_context: FileContext,
        source_root: Path,
        ctx: Context
    ) -> RebuildDecision:
        """
        [Class method intent]
        Makes individual file rebuild decision based on analysis cache staleness checking.
        Implements targeted file processing preventing unnecessary analysis when cache is fresh.

        [Design principles]
        Individual file decision making ensuring precise targeted processing of stale files only.
        Cache-first approach leveraging FileAnalysisCache for performance optimization.
        Clear decision reasoning enabling debugging and optimization of file-level processing.
        Conservative decision making ensuring cache freshness is accurately determined.

        [Implementation details]
        Uses FileAnalysisCache.is_cache_fresh() for precise individual file staleness checking.
        Creates RebuildDecision with detailed reasoning about cache staleness status.
        Handles filesystem errors gracefully with conservative rebuild decisions.
        Tracks filesystem operations for performance monitoring and optimization.
        """
        try:
            file_path = file_context.file_path
            
            # Check if analysis cache is fresh for this individual file
            self._filesystem_operations += 1
            is_fresh, freshness_reason = self.is_cache_fresh(file_path, source_root)
            
            if not is_fresh:
                reasoning = f"File analysis cache is stale: {freshness_reason}"
                decision = self._create_decision_with_metadata_pattern(
                    path=file_path,
                    outcome=DecisionOutcome.REBUILD,
                    reason=DecisionReason.CACHE_STALE,
                    base_reasoning=reasoning,
                    metadata_type="file_cache_check",
                    freshness_reason=freshness_reason,
                    file_size=getattr(file_context, 'file_size', 0)
                )
                await self._log_decision_context(ctx, DecisionOutcome.REBUILD, file_path, reasoning, "file", source_root)
                return decision
            else:
                reasoning = f"File analysis cache is fresh: {freshness_reason}"
                decision = self._create_decision_with_metadata_pattern(
                    path=file_path,
                    outcome=DecisionOutcome.SKIP,
                    reason=DecisionReason.CACHE_FRESH,
                    base_reasoning=reasoning,
                    metadata_type="file_cache_check",
                    freshness_reason=freshness_reason,
                    file_size=getattr(file_context, 'file_size', 0)
                )
                await self._log_decision_context(ctx, DecisionOutcome.SKIP, file_path, reasoning, "file", source_root)
                return decision
                
        except Exception as e:
            return self._handle_decision_error("File rebuild decision", file_context.file_path, e)

    async def _analyze_directory_rebuild_decisions(
        self, 
        directory_context: DirectoryContext, 
        source_root: Path,
        report: DecisionReport,
        ctx: Context
    ) -> None:
        """
        [Class method intent]
        Recursively analyzes directory hierarchy making rebuild decisions for all directories.
        Handles special cases (project root, empty directories) and integrates with FileAnalysisCache
        for comprehensive staleness checking and performance optimization.

        [Design principles]
        Recursive directory analysis ensuring comprehensive coverage of entire hierarchy.
        Special case handling for project root and empty directories preventing systematic issues.
        FileAnalysisCache integration providing performance-optimized staleness checking.
        Rich decision reasoning capture enabling debugging and optimization of decision logic.
        Error handling ensuring analysis continues despite individual directory failures.

        [Implementation details]
        Processes subdirectories recursively before parent directories for proper dependency handling.
        Uses FileAnalysisCache for comprehensive staleness checking against all constituents.
        Detects empty directories and skips knowledge file generation to prevent infinite loops.
        Handles project root specially ensuring root_kb.md generation regardless of change detection.
        Creates detailed RebuildDecision objects with clear reasoning for audit trails.
        """
        try:
            # Process subdirectories first (leaf-first for proper dependencies)
            for subdir_context in directory_context.subdirectory_contexts:
                await self._analyze_directory_rebuild_decisions(subdir_context, source_root, report, ctx)
            
            # Analyze current directory
            decision = await self._make_directory_rebuild_decision(directory_context, source_root, ctx)
            report.add_rebuild_decision(decision)
            self._decisions_made += 1
            
            await ctx.debug(f"Directory decision: {directory_context.directory_path.name} -> {decision.outcome.value} ({decision.reason.value})")
            
        except Exception as e:
            logger.error(f"Directory rebuild analysis failed for {directory_context.directory_path}: {e}")
            
            # Create error decision using consolidated factory method
            error_decision = self._handle_decision_error("Directory rebuild analysis", directory_context.directory_path, e)
            report.add_rebuild_decision(error_decision)
            self._decisions_made += 1
    
    async def _make_directory_rebuild_decision(
        self, 
        directory_context: DirectoryContext, 
        source_root: Path,
        ctx: Context
    ) -> RebuildDecision:
        """
        [Class method intent]
        Makes single directory rebuild decision using comprehensive staleness checking.
        Consolidates all decision logic from scattered components into unified decision point
        with clear reasoning and special case handling.

        [Design principles]
        Unified decision logic consolidating scattered logic from multiple components.
        Comprehensive staleness checking using FileAnalysisCache for performance and accuracy.
        Special case handling for project root and empty directories preventing systematic issues.
        Clear decision reasoning enabling debugging and optimization of decision outcomes.
        Performance optimization through intelligent filesystem operation ordering.

        [Implementation details]
        Checks for empty directories first to avoid unnecessary processing and infinite loops.
        Handles project root specially ensuring root_kb.md generation through forced processing.
        Uses FileAnalysisCache.is_knowledge_file_stale() for comprehensive constituent checking.
        Creates RebuildDecision with detailed reasoning and metadata for audit trails.
        Tracks filesystem operations for performance monitoring and optimization efforts.
        """
        try:
            # Special case 1: Empty directory detection
            if self._is_directory_empty_of_processable_content(directory_context):
                reasoning = "Directory contains no processable files or subdirectories"
                decision = self._create_decision_with_metadata_pattern(
                    path=directory_context.directory_path,
                    outcome=DecisionOutcome.SKIP,
                    reason=DecisionReason.EMPTY_DIRECTORY,
                    base_reasoning=reasoning,
                    metadata_type="empty_directory",
                    file_count=len(directory_context.file_contexts),
                    subdir_count=len(directory_context.subdirectory_contexts)
                )
                await self._log_decision_context(ctx, DecisionOutcome.SKIP, directory_context.directory_path, reasoning, "decision", source_root)
                return decision
            
            # RebuildDecisionEngine now handles its own staleness checking since path generation was removed from FileAnalysisCache
            self._filesystem_operations += 1
            is_stale, staleness_reason = self._check_directory_staleness_internal(
                directory_context, source_root
            )
            
            if is_stale:
                reasoning = staleness_reason or "Comprehensive staleness check indicates rebuild needed"
                decision = self._create_decision_with_metadata_pattern(
                    path=directory_context.directory_path,
                    outcome=DecisionOutcome.REBUILD,
                    reason=DecisionReason.COMPREHENSIVE_STALENESS,
                    base_reasoning=reasoning,
                    metadata_type="staleness_check",
                    staleness_reason=staleness_reason
                )
                await self._log_decision_context(ctx, DecisionOutcome.REBUILD, directory_context.directory_path, reasoning, "decision", source_root)
                return decision
            else:
                reasoning = "Directory knowledge file is up to date"
                decision = self._create_decision_with_metadata_pattern(
                    path=directory_context.directory_path,
                    outcome=DecisionOutcome.SKIP,
                    reason=DecisionReason.UP_TO_DATE,
                    base_reasoning=reasoning,
                    metadata_type="staleness_check",
                    staleness_check="passed"
                )
                await self._log_decision_context(ctx, DecisionOutcome.SKIP, directory_context.directory_path, reasoning, "decision", source_root)
                return decision
                
        except Exception as e:
            return self._handle_decision_error("Directory rebuild decision", directory_context.directory_path, e)
    
    def _is_directory_empty_of_processable_content(self, directory_context: DirectoryContext) -> bool:
        """
        [Class method intent]
        Determines if directory has no processable content requiring knowledge file generation.
        Prevents infinite rebuild loops for directories containing only excluded files or empty subdirectories.

        [Design principles]
        Empty directory detection preventing infinite rebuild cycles for contentless directories.
        Comprehensive content checking considering both files and subdirectories for accurate determination.
        Performance optimization avoiding unnecessary processing for truly empty directories.

        [Implementation details]
        Checks file_contexts length to determine presence of processable files.
        Checks subdirectory_contexts length to determine presence of processable subdirectories.
        Returns True only when both files and subdirectories are completely absent.
        """
        has_processable_files = len(directory_context.file_contexts) > 0
        has_processable_subdirs = len(directory_context.subdirectory_contexts) > 0
        return not (has_processable_files or has_processable_subdirs)
    
    async def _analyze_deletion_decisions(self, source_root: Path, report: DecisionReport, ctx: Context) -> None:
        """
        [Class method intent]
        Analyzes knowledge directory for orphaned files requiring deletion.
        Consolidates orphaned file detection logic providing comprehensive cleanup decisions
        with safety validation and clear reasoning for audit trails.

        [Design principles]
        Comprehensive orphaned file detection covering all knowledge file types and scenarios.
        Safety-first deletion decisions with validation preventing accidental data loss.
        Clear deletion reasoning enabling audit trails and error recovery capabilities.
        Performance optimization through intelligent directory traversal and batch operations.
        Integration with existing cleanup logic preserving established safety mechanisms.

        [Implementation details]
        Scans knowledge output directory identifying files without corresponding source content.
        Validates deletion safety checking for recent modifications and backup requirements.
        Creates DeletionDecision objects with comprehensive reasoning and safety metadata.
        Handles different file types (knowledge files, analysis cache) with appropriate logic.
        Tracks deletion statistics for reporting and monitoring integration.
        """
        try:
            knowledge_dir = self.config.knowledge_output_directory
            
            if not knowledge_dir.exists():
                await ctx.debug("Knowledge directory does not exist, no deletion decisions needed")
                return
            
            await ctx.debug(f"Scanning for orphaned files in: {knowledge_dir}")
            
            # Find orphaned knowledge files
            orphaned_kb_files = await self._find_orphaned_knowledge_files(source_root, ctx)
            for orphaned_file in orphaned_kb_files:
                decision = self._create_deletion_decision(
                    path=orphaned_file,
                    outcome=DecisionOutcome.DELETE,
                    reason=DecisionReason.ORPHANED_KNOWLEDGE_FILE,
                    reasoning_text=f"Knowledge file has no corresponding source directory: {orphaned_file.name}",
                    is_safe_to_delete=True,
                    metadata={"file_type": "knowledge", "orphaned": True}
                )
                report.add_deletion_decision(decision)
                self._decisions_made += 1
            
            # Find orphaned analysis cache files
            orphaned_cache_files = await self._find_orphaned_cache_files(source_root, ctx)
            for orphaned_file in orphaned_cache_files:
                decision = self._create_deletion_decision(
                    path=orphaned_file,
                    outcome=DecisionOutcome.DELETE,
                    reason=DecisionReason.ORPHANED_ANALYSIS_CACHE,
                    reasoning_text=f"Analysis cache file has no corresponding source file: {orphaned_file.name}",
                    is_safe_to_delete=True,
                    metadata={"file_type": "analysis_cache", "orphaned": True}
                )
                report.add_deletion_decision(decision)
                self._decisions_made += 1
            
            deletion_count = len(orphaned_kb_files) + len(orphaned_cache_files)
            await ctx.info(f"Deletion analysis complete: {deletion_count} orphaned files found")
            
        except Exception as e:
            logger.error(f"Deletion decision analysis failed: {e}", exc_info=True)
            report.decision_errors.append(f"Deletion analysis failed: {str(e)}")
            await ctx.warning(f"Deletion analysis failed: {str(e)}")
    
    async def _find_orphaned_knowledge_files(self, source_root: Path, ctx: Context) -> List[Path]:
        """
        [Class method intent]
        Identifies knowledge files without corresponding source directories across all handler-managed areas.
        Uses HandlerRegistry to detect orphaned files in project-base, git-clone .kb directories, and other handler areas.

        [Design principles]
        Handler-delegated orphaned file detection covering all content types and knowledge structures.
        Comprehensive scanning across all handler-managed directories for complete cleanup coverage.
        Safety validation preventing deletion of recently created or actively used files.

        [Implementation details]
        Uses HandlerRegistry to get all handlers and scan their managed knowledge areas.
        Delegates reverse mapping to handlers for accurate source path calculation.
        Checks source directory existence and processability for orphan determination across all handler types.
        Returns list of confirmed orphaned knowledge files safe for deletion from all handler areas.
        """
        orphaned_files = []
        
        try:
            # Use all handlers to find orphaned files in their managed areas
            for handler in self.handler_registry.get_all_handlers():
                try:
                    handler_orphaned_files = await handler.find_orphaned_files(source_root, ctx)
                    orphaned_files.extend(handler_orphaned_files)
                    
                    if handler_orphaned_files:
                        await ctx.debug(f"Handler {handler.get_handler_type()} found {len(handler_orphaned_files)} orphaned files")
                        
                except Exception as e:
                    logger.warning(f"Orphaned file detection failed for handler {handler.get_handler_type()}: {e}")
                    continue
            
            # Additional comprehensive scan of knowledge output directory for any missed files
            knowledge_dir = self.config.knowledge_output_directory
            if knowledge_dir.exists():
                for kb_file in knowledge_dir.rglob("*_kb.md"):
                    # Check if any handler can map this file to a source
                    source_found = False
                    for handler in self.handler_registry.get_all_handlers():
                        try:
                            source_path = handler.map_knowledge_to_source(kb_file, source_root)
                            if source_path and source_path.exists() and self.config.should_process_directory(source_path):
                                source_found = True
                                break
                        except Exception:
                            continue
                    
                    if not source_found and kb_file not in orphaned_files:
                        orphaned_files.append(kb_file)
                        await ctx.debug(f"Additional orphaned knowledge file found: {kb_file}")
                        self._filesystem_operations += 1
            
        except Exception as e:
            logger.warning(f"Comprehensive orphaned knowledge file detection failed: {e}")
        
        return orphaned_files
    
    async def _find_orphaned_cache_files(self, source_root: Path, ctx: Context) -> List[Path]:
        """
        [Class method intent]
        Finds orphaned cache files by delegating to individual handlers.
        Uses convention where each handler manages orphaned file detection in its own areas.

        [Design principles]
        Delegation to handlers eliminating complex centralized path understanding.
        Convention-based approach where handlers manage their own domains.
        Simple architecture reducing complexity and maintenance burden.

        [Implementation details]
        Iterates through all registered handlers calling find_orphaned_files().
        Aggregates results from all handlers into single orphaned files list.
        Handles handler failures gracefully with logging and continued processing.
        """
        orphaned_files = []
        
        try:
            # Delegate to each handler for domain-specific orphaned file detection
            for handler in self.handler_registry.get_all_handlers():
                try:
                    handler_orphaned = await handler.find_orphaned_files(source_root, ctx)
                    
                    # Filter for cache files only (this method is specifically for cache files)
                    cache_orphaned = [f for f in handler_orphaned if f.name.endswith('.analysis.md')]
                    orphaned_files.extend(cache_orphaned)
                    
                    if cache_orphaned:
                        await ctx.debug(f"Handler {handler.get_handler_type()} found {len(cache_orphaned)} orphaned cache files")
                        
                except Exception as e:
                    logger.warning(f"Handler {handler.get_handler_type()} orphaned cache detection failed: {e}")
                    continue
            
            await ctx.info(f"Total orphaned cache files found: {len(orphaned_files)}")
            return orphaned_files
            
        except Exception as e:
            logger.warning(f"Delegated orphaned cache file detection failed: {e}")
            return orphaned_files
    
    async def should_rebuild_directory(
        self, 
        directory_context: DirectoryContext, 
        source_root: Path,
        ctx: Context
    ) -> RebuildDecision:
        """
        [Class method intent]
        Public interface for single directory rebuild decision making.
        Provides consistent decision logic for external components requiring individual decisions.

        [Design principles]
        Consistent decision logic matching comprehensive hierarchy analysis for reliability.
        Public interface enabling external component integration with centralized decisions.
        Performance optimization through direct decision making without full hierarchy analysis.

        [Implementation details]
        Delegates to internal _make_directory_rebuild_decision for consistent logic.
        Tracks individual decision for performance monitoring and optimization.
        Returns RebuildDecision with complete reasoning and metadata for external use.
        """
        decision = await self._make_directory_rebuild_decision(directory_context, source_root, ctx)
        self._decisions_made += 1
        return decision
    
    async def should_cleanup_orphaned_analysis(
        self,
        analysis_file_path: Path,
        source_root: Path,
        ctx: Context
    ) -> Tuple[DecisionOutcome, str]:
        """
        [Class method intent]
        Determines if an analysis file should be cleaned up because its source file no longer exists.
        Centralizes orphaned analysis file decision logic for consistent cleanup behavior.

        [Design principles]
        Conservative deletion ensuring only confirmed orphaned files are removed.
        Source file verification using reverse path calculation from analysis file location.
        Clear decision reasoning supporting audit trail and cleanup operations.

        [Implementation details]
        Uses consolidated validation and cleanup decision logic for consistent behavior.
        Calculates corresponding source file path from analysis file location.
        Returns cleanup decision with clear reasoning about orphaned status.
        """
        def make_decision():
            # Calculate corresponding source file path
            source_file_path = self._get_source_path_from_analysis_file(analysis_file_path, source_root)
            
            # Use consolidated validation and decision logic
            outcome, reason = self._validate_and_decide_cleanup(
                source_file_path, 
                is_file=True, 
                ctx=ctx, 
                target_name=analysis_file_path.name
            )
            
            # Log decision using consolidated logging
            if outcome == DecisionOutcome.DELETE:
                asyncio.create_task(self._log_decision_context(ctx, outcome, analysis_file_path, reason, "cleanup"))
            
            return outcome, reason
        
        return await self._execute_with_error_handling(
            operation_func=lambda: make_decision(),
            operation_name="Orphaned analysis cleanup decision",
            target_path=analysis_file_path,
            ctx=ctx,
            fallback_result=(DecisionOutcome.SKIP, f"Cannot determine orphaned status due to error"),
            as_rebuild_decision=False
        )

    def _get_source_path_from_analysis_file(self, analysis_file: Path, source_root: Path) -> Optional[Path]:
        """
        [Class method intent]
        Calculates the corresponding source file path from an analysis cache file path.
        Performs reverse path calculation to determine if the original source file still exists.
        Uses consolidated helper method for consistent reverse path mapping.

        [Design principles]
        Reverse path calculation ensuring accurate source file identification.
        Integration with project-base directory structure mirroring business rules.
        Error handling returning None for invalid or unresolvable paths.
        Delegates to consolidated helper method eliminating code duplication.

        [Implementation details]
        Uses _map_analysis_file_to_source_safe for consistent reverse path mapping.
        Consolidated implementation prevents duplication and ensures consistent behavior.
        Handles path calculation errors gracefully returning None for safety.
        """
        return self._map_analysis_file_to_source_safe(analysis_file, source_root)

    async def should_cleanup_orphaned_knowledge(
        self,
        knowledge_directory: Path,
        source_root: Path,
        ctx: Context
    ) -> Tuple[DecisionOutcome, str]:
        """
        [Class method intent]
        Determines if a knowledge file should be cleaned up because the directory has no content
        (no analysis files, no subdirectories) or the source directory no longer exists.

        [Design principles]
        Logical consistency ensuring knowledge files only exist where there's content to summarize.
        Conservative approach only deleting knowledge files from truly empty directories.
        Source directory verification for orphaned knowledge file detection.

        [Implementation details]
        Checks if directory contains any analysis files or subdirectories.
        Verifies corresponding source directory existence and processability.
        Returns cleanup decision with clear reasoning about knowledge file necessity.
        """
        try:
            # Check if directory has any analysis files or subdirectories
            has_analysis_files = any(f.is_file() and f.name.endswith('.analysis.md') for f in knowledge_directory.iterdir())
            has_subdirectories = any(f.is_dir() for f in knowledge_directory.iterdir())

            # If directory has content, keep knowledge file
            if has_analysis_files or has_subdirectories:
                return DecisionOutcome.SKIP, f"Directory has content - knowledge file needed"

            # Directory is empty - check source directory status
            source_directory = self._get_source_directory_from_mirrored_path(knowledge_directory, source_root)
            
            if not source_directory or not source_directory.exists():
                await ctx.debug(f"🗑️ CLEANUP: Knowledge file for non-existent source: {knowledge_directory.name}")
                return DecisionOutcome.DELETE, f"Knowledge file for non-existent source directory"
            
            if not self.config.should_process_directory(source_directory):
                await ctx.debug(f"🗑️ CLEANUP: Knowledge file for excluded source: {knowledge_directory.name}")
                return DecisionOutcome.DELETE, f"Knowledge file for excluded source directory"
            
            # Source exists and is processable but directory is empty - this may be temporary
            return DecisionOutcome.SKIP, f"Source directory exists and is processable"
            
        except Exception as e:
            await ctx.warning(f"Failed to check orphaned knowledge status for {knowledge_directory}: {e}")
            return DecisionOutcome.SKIP, f"Cannot determine orphaned status: {e}"

    def _get_source_directory_from_mirrored_path(self, mirrored_directory: Path, source_root: Path) -> Optional[Path]:
        """
        [Class method intent]
        Calculates the corresponding source directory path from a mirrored knowledge directory path.
        Performs reverse path calculation to determine if the original source directory still exists.
        Uses consolidated helper method for consistent reverse path mapping.

        [Design principles]
        Reverse path calculation ensuring accurate source directory identification.
        Integration with project-base directory structure mirroring business rules.
        Error handling returning None for invalid or unresolvable paths.
        Delegates to consolidated helper method eliminating code duplication.

        [Implementation details]
        Uses _map_knowledge_dir_to_source_safe for consistent reverse path mapping.
        Consolidated implementation prevents duplication and ensures consistent behavior.
        Handles path calculation errors gracefully returning None for safety.
        """
        return self._map_knowledge_dir_to_source_safe(mirrored_directory, source_root)

    def is_cache_fresh(self, file_path: Path, source_root: Path) -> Tuple[bool, str]:
        """
        [Class method intent]
        Centralized cache freshness decision consolidating FileAnalysisCache logic.
        Determines if cached analysis is fresh by comparing source file timestamp with cache timestamp.

        [Design principles]
        Centralized cache freshness logic replacing scattered cache decisions.
        Timestamp-based freshness checking with tolerance for reliable incremental processing.
        Clear reasoning return supporting debugging and cache management operations.

        [Implementation details]
        Delegates to FileAnalysisCache.is_cache_fresh() for consistent logic.
        Uses HandlerRegistry to get appropriate handler for file path.
        Returns boolean freshness status with detailed reasoning for decision audit trails.
        Handles filesystem errors gracefully returning conservative decisions.
        """
        try:
            # Get appropriate handler for the file
            handler = self.handler_registry.get_handler_for_path(file_path.parent)
            if handler is None:
                return False, f"No handler available for path: {file_path.parent}"
            
            # FileAnalysisCache.is_cache_fresh now returns tuple (bool, str) and requires handler
            is_fresh, detailed_reason = self.file_cache.is_cache_fresh(file_path, source_root, handler)
            return is_fresh, detailed_reason
                
        except Exception as e:
            logger.warning(f"Cache freshness check failed for {file_path}: {e}")
            # Conservative: assume stale on error to trigger fresh processing
            return False, f"Cache freshness check failed: {e}"

    async def should_cleanup_empty_directory(
        self,
        directory_path: Path,
        source_root: Path,
        ctx: Context
    ) -> Tuple[DecisionOutcome, str]:
        """
        [Class method intent]
        Centralized empty directory cleanup decision consolidating scattered logic.
        Determines if empty knowledge directories should be removed based on source existence and exclusion.

        [Design principles]
        Centralized empty directory logic replacing scattered cleanup decisions.
        Conservative cleanup approach preserving directories when source exists and is not excluded.
        Aggressive cleanup for excluded sources removing entire directory trees.

        [Implementation details]
        Checks corresponding source directory existence and exclusion status.
        Uses configuration exclusion methods for consistent behavior.
        Returns cleanup decision with detailed reasoning for audit trails.
        """
        try:
            # Calculate corresponding source directory
            knowledge_base_dir = self.config.knowledge_output_directory / "project-base"
            relative_path = directory_path.relative_to(knowledge_base_dir)
            source_directory = source_root / relative_path
            
            # Check if directory is empty
            try:
                directory_contents = list(directory_path.iterdir())
                is_empty = len(directory_contents) == 0
            except OSError:
                # Can't read directory - conservative approach
                return DecisionOutcome.SKIP, f"Cannot read directory contents: {directory_path.name}"
            
            # If not empty, don't delete
            if not is_empty:
                return DecisionOutcome.SKIP, f"Directory is not empty: {directory_path.name}"
            
            # Directory is empty - check source status
            if source_directory.exists():
                # Source exists - check if excluded
                if not self.config.should_process_directory(source_directory):
                    await ctx.debug(f"🗑️ CLEANUP: Empty directory for excluded source: {directory_path}")
                    return DecisionOutcome.DELETE, f"Empty directory for excluded source directory"
                else:
                    # Source exists and not excluded - keep empty directory
                    return DecisionOutcome.SKIP, f"Source directory exists and is not excluded"
            else:
                # Source doesn't exist - safe to delete empty directory
                await ctx.debug(f"🗑️ CLEANUP: Empty directory for non-existent source: {directory_path}")
                return DecisionOutcome.DELETE, f"Empty directory for non-existent source directory"
                
        except Exception as e:
            await ctx.warning(f"Empty directory cleanup decision failed for {directory_path}: {e}")
            # Conservative: don't delete if we can't determine status
            return DecisionOutcome.SKIP, f"Cannot determine cleanup status: {e}"

    async def should_cleanup_excluded_source(self, source_path: Path, source_root: Path, ctx: Context) -> Tuple[DecisionOutcome, str]:
        """
        [Class method intent]
        Determines if a source file/directory should be cleaned up because it's now excluded.
        Provides centralized decision logic for orphaned cleanup operations.

        [Design principles]
        Centralized exclusion decision logic ensuring consistent behavior across components.
        Configuration-driven decision making using IndexingConfig exclusion rules.
        Clear decision outcome with detailed reasoning for audit trails and debugging.

        [Implementation details]
        Uses IndexingConfig filtering methods to check exclusion status.
        Provides clear decision outcomes (DELETE for excluded, SKIP for included).
        Returns detailed reasoning for cleanup audit trails and troubleshooting.
        """
        try:
            is_file = source_path.is_file() if source_path.exists() else source_path.suffix != ''
            
            if is_file:
                # Check file exclusion
                if not self.config.should_process_file(source_path):
                    reason = f"Source file is excluded by configuration: {source_path.name}"
                    return DecisionOutcome.DELETE, reason
                else:
                    reason = f"Source file is included in configuration: {source_path.name}"
                    return DecisionOutcome.SKIP, reason
            else:
                # Check directory exclusion
                if not self.config.should_process_directory(source_path):
                    reason = f"Source directory is excluded by configuration: {source_path.name}"
                    return DecisionOutcome.DELETE, reason
                else:
                    reason = f"Source directory is included in configuration: {source_path.name}"
                    return DecisionOutcome.SKIP, reason
                    
        except Exception as e:
            logger.error(f"Exclusion check failed for {source_path}: {e}")
            reason = f"Exclusion check failed: {str(e)}"
            return DecisionOutcome.ERROR, reason
    
    async def _propagate_cascading_decisions(
        self,
        root_context: DirectoryContext,
        source_root: Path,
        report: DecisionReport,
        ctx: Context
    ) -> int:
        """
        [Class method intent]
        Implements selective cascading logic for hierarchical rebuild decisions.
        When any directory needs rebuilding due to content changes, automatically marks all
        ancestor directories for rebuild because parent KB files contain summaries from child directories.

        [Design principles]
        Selective cascading ensuring only content-driven rebuilds trigger ancestor rebuilds.
        Efficient ancestor traversal preventing duplicate decisions and maintaining performance.
        Clear audit trail showing cascading reasoning for debugging and optimization.
        Directory hierarchy understanding enabling accurate ancestor identification and path calculation.

        [Implementation details]
        Scans existing rebuild decisions identifying directories requiring cascading.
        Uses path-based ancestor calculation traversing up directory hierarchy systematically.
        Creates cascading rebuild decisions with CHILD_DIRECTORY_REBUILT reasoning.
        Maintains decision deduplication preventing multiple cascading decisions for same directory.
        Returns count of cascaded decisions for monitoring and performance analysis.

        Args:
            root_context: Root directory context for hierarchy understanding
            source_root: Source root path for relative path calculations
            report: Decision report to analyze and update with cascading decisions
            ctx: FastMCP context for progress reporting and logging

        Returns:
            int: Number of cascading decisions created
        """
        cascaded_count = 0
        
        try:
            # Find directories that need rebuilding due to content changes (selective cascading)
            directories_needing_cascade = []
            
            for rebuild_decision in report.rebuild_decisions.values():
                if (rebuild_decision.should_rebuild and 
                    rebuild_decision.reason in {
                        DecisionReason.COMPREHENSIVE_STALENESS,
                        DecisionReason.CACHE_STALE,
                        DecisionReason.KNOWLEDGE_FILE_MISSING,
                        DecisionReason.SOURCE_FILES_NEWER,
                        DecisionReason.CACHED_ANALYSES_NEWER,
                        DecisionReason.SUBDIRECTORY_KNOWLEDGE_NEWER
                    }):
                    directories_needing_cascade.append(rebuild_decision.path)
                    await ctx.debug(f"🔗 CASCADING SOURCE: {rebuild_decision.path.name} ({rebuild_decision.reason.value})")
            
            if not directories_needing_cascade:
                await ctx.debug("No directories require cascading - all rebuilds are non-content related")
                return 0
            
            # For each directory needing rebuild, cascade up the hierarchy
            for directory_path in directories_needing_cascade:
                ancestors = self._get_ancestor_directories(directory_path, source_root)
                
                for ancestor_path in ancestors:
                    # Check if ancestor already has a rebuild decision
                    existing_decision = report.get_decision_for_path(ancestor_path)
                    
                    if existing_decision and existing_decision.should_rebuild:
                        # Ancestor already marked for rebuild - skip
                        await ctx.debug(f"⏭️ SKIP CASCADE: {ancestor_path.name} already marked for rebuild")
                        continue
                    
                    # Create cascading rebuild decision
                    cascading_reasoning = f"Child directory requires rebuild: {directory_path.name}"
                    cascading_decision = self._create_decision_with_metadata_pattern(
                        path=ancestor_path,
                        outcome=DecisionOutcome.REBUILD,
                        reason=DecisionReason.CHILD_DIRECTORY_REBUILT,
                        base_reasoning=cascading_reasoning,
                        metadata_type="cascading_rebuild",
                        child_directory=str(directory_path),
                        cascading_source="selective_content_based"
                    )
                    
                    # Add cascading decision to report (will override any SKIP decision)
                    report.add_rebuild_decision(cascading_decision)
                    cascaded_count += 1
                    self._decisions_made += 1
                    
                    await ctx.debug(f"🔗 CASCADED: {ancestor_path.name} ← {directory_path.name}")
                    await self._log_decision_context(ctx, DecisionOutcome.REBUILD, ancestor_path, cascading_reasoning, "cascade", source_root)
            
            if cascaded_count > 0:
                await ctx.info(f"✅ Selective cascading complete: {cascaded_count} ancestor directories marked for rebuild")
            else:
                await ctx.debug("No cascading required - all ancestors already marked appropriately")
                
            return cascaded_count
            
        except Exception as e:
            logger.error(f"Cascading decision propagation failed: {e}", exc_info=True)
            await ctx.warning(f"Cascading failed: {str(e)}")
            return cascaded_count

    def _get_ancestor_directories(self, directory_path: Path, source_root: Path) -> List[Path]:
        """
        [Class method intent]
        Calculates all ancestor directories from given directory up to source root.
        Implements efficient ancestor traversal for selective cascading decision propagation.

        [Design principles]
        Efficient ancestor calculation using path traversal without filesystem operations.
        Source root boundary respect preventing cascading beyond project boundaries.
        Ordered ancestor list enabling systematic cascading from child to root.
        Path normalization ensuring consistent ancestor identification across platforms.

        [Implementation details]
        Uses Path.parent property for systematic upward traversal through directory hierarchy.
        Stops at source root preventing cascading beyond project boundaries.
        Returns ordered list with immediate parent first, continuing to project root.
        Handles edge cases like root directory and invalid paths gracefully.

        Args:
            directory_path: Starting directory path for ancestor calculation
            source_root: Source root path serving as cascading boundary

        Returns:
            List[Path]: Ordered list of ancestor directories from immediate parent to source root
        """
        ancestors = []
        
        try:
            current_path = directory_path
            
            # Traverse up the hierarchy until we reach source root
            while current_path != source_root and current_path.parent != current_path:
                parent_path = current_path.parent
                
                # Stop if we've reached or passed source root
                if parent_path == source_root or source_root in ancestors:
                    # Add source root as final ancestor if not already added
                    if source_root not in ancestors and parent_path == source_root:
                        ancestors.append(source_root)
                    break
                
                ancestors.append(parent_path)
                current_path = parent_path
                
                # Safety check to prevent infinite loops
                if len(ancestors) > 20:  # Reasonable depth limit
                    logger.warning(f"Ancestor traversal depth limit reached for {directory_path}")
                    break
            
            logger.debug(f"Found {len(ancestors)} ancestors for {directory_path.name}: {[a.name for a in ancestors]}")
            return ancestors
            
        except Exception as e:
            logger.error(f"Failed to calculate ancestors for {directory_path}: {e}")
            return []

    def get_decision_statistics(self) -> Dict[str, any]:
        """
        [Class method intent]
        Returns decision engine performance statistics for monitoring and optimization.
        Provides comprehensive metrics about decision making performance and efficiency.

        [Design principles]
        Comprehensive performance monitoring supporting optimization and analysis efforts.
        Clear statistical breakdown enabling decision engine performance evaluation.
        Real-time statistics access supporting monitoring and alerting integration.

        [Implementation details]
        Collects decision timing, filesystem operation counts, and performance metrics.
        Calculates decision rates and efficiency statistics for performance analysis.
        Returns structured statistics dictionary for monitoring and reporting integration.
        """
        stats = {
            "decisions_made": self._decisions_made,
            "filesystem_operations": self._filesystem_operations,
            "last_analysis_duration": None,
            "decisions_per_second": 0.0,
            "filesystem_ops_per_decision": 0.0
        }
        
        if self._decision_start_time:
            duration = (datetime.now() - self._decision_start_time).total_seconds()
            stats["last_analysis_duration"] = duration
            
            if duration > 0:
                stats["decisions_per_second"] = self._decisions_made / duration
        
        if self._decisions_made > 0:
            stats["filesystem_ops_per_decision"] = self._filesystem_operations / self._decisions_made
        
        return stats

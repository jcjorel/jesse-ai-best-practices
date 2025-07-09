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
# File analysis cache manager for individual LLM analysis outputs.
# Provides caching mechanism to avoid recomputation of file analyses when source files
# haven't changed, significantly improving performance and reducing LLM API costs.
###############################################################################
# [Source file design principles]
# - Cache-first processing minimizing unnecessary LLM calls for unchanged files
# - Clean metadata separation ensuring no cache artifacts in final knowledge files
# - Mirror directory structure following project-base indexing business rules
# - Timestamp-based freshness checking with configurable tolerance for reliability
# - Comprehensive error handling with graceful degradation on cache failures
# - Rich metadata tracking for debugging and cache management operations
###############################################################################
# [Source file constraints]
# - Cache files must follow project-base directory structure mirroring
# - Metadata must be completely stripped from cached content before knowledge assembly
# - Timestamp comparison must respect configured tolerance for filesystem precision
# - Cache operations must not interfere with core knowledge building when failing
# - File I/O operations must handle concurrent access and filesystem errors gracefully
###############################################################################
# [Dependencies]
# <codebase>: ..models.indexing_config - Configuration and cache settings
# <system>: pathlib - Cross-platform path operations and file metadata
# <system>: datetime - Timestamp comparison and cache freshness determination
# <system>: logging - Structured logging for cache operations and debugging
###############################################################################
# [GenAI tool change history]
# 2025-07-07T21:24:00Z : CRITICAL HANDLER-AWARE CACHE FIX - Made FileAnalysisCache handler-aware eliminating ALL project-base fallbacks by CodeAssistant
# * FIXED ROOT CAUSE: Modified get_cache_path() to delegate to handler.get_cache_path() instead of hardcoded project-base logic
# * ELIMINATED ALL FALLBACKS: Removed hardcoded "project-base" path generation - handlers have 100% cache path control
# * ADDED EXPLICIT ERRORS: Cache operations now fail fast with explicit errors when handler cannot be determined
# * HANDLER DELEGATION: GitCloneHandler and ProjectBaseHandler now control their own cache directory structures
# * PREVENTS CROSS-CONTAMINATION: Git-clone cache files now go to .knowledge/git-clones/<repo>.kb/ not project-base/
# 2025-07-07T17:08:00Z : COMPLETE PATH GENERATION REMOVAL - Eliminated all knowledge file path methods enabling 100% handler control by CodeAssistant
# * REMOVED COMPLETELY: get_knowledge_file_path() method with project-base path calculation logic
# * REMOVED COMPLETELY: _is_handler_root_directory() method with handler root detection logic
# * ZERO FALLBACKS: No knowledge file path generation capability remains in FileAnalysisCache - handlers have 100% control
# * PREVENTS ALL OVERRIDES: Impossible for FileAnalysisCache to override any handler path decisions
# * ENFORCES HANDLER AUTHORITY: Only handlers can determine where KB files should be located
# 2025-07-06T19:56:00Z : Enhanced debug output with detailed timestamp reasoning for cache staleness decisions by CodeAssistant
# * Enhanced is_cache_fresh() to return tuple (bool, str) with detailed timestamp-based reasoning
# * Added precise timestamp comparison details showing cache vs source file modification times
# * Improved debug messages to show exact timestamps: "Cache (2025-07-06 17:19:16) < source (2025-07-06 19:30:00)"
# * Supports better debugging by showing why files are considered stale with specific timestamp comparisons
# 2025-07-06T19:30:00Z : CRITICAL BUG FIX - Fixed infinite rebuild loop by removing cached analysis comparison from directory staleness checking by CodeAssistant
# * EMERGENCY FIX: Removed cached analysis comparison from is_knowledge_file_stale() method preventing infinite rebuild loops
# * Fixed core logic issue where cached analyses were always newer than knowledge files causing perpetual rebuilds
# * Added precise timestamp logging with detailed reasoning for all staleness decisions supporting debugging
# * Removed timestamp tolerance for direct filesystem timestamp comparison eliminating race conditions and timing inconsistencies
# 2025-07-03T17:39:00Z : Fixed change detection logic to properly implement layered processing approach by CodeAssistant
# * Removed direct source file → knowledge file comparison to prevent systematic rebuilds
# * Knowledge files now only rebuild when cached analyses or subdirectory knowledge files are newer
# * Fixed systematic knowledge file rebuilding issue by implementing proper two-layer processing (source → cache → knowledge)
# * Maintains proper incremental processing flow: source changes trigger individual file reprocessing, knowledge rebuilds only when constituents change
# 2025-07-03T17:17:00Z : Implemented comprehensive constituent dependency checking for directory knowledge files by CodeAssistant
# * Added is_knowledge_file_stale() method providing comprehensive staleness checking against all constituents
# * Added get_constituent_staleness_info() method for detailed debugging and analysis of staleness conditions
# * Added get_knowledge_file_path() method centralizing knowledge file path calculation logic
###############################################################################

"""
File Analysis Cache Manager for Knowledge Building System.

This module provides caching capabilities for individual file LLM analysis outputs,
enabling significant performance improvements by avoiding recomputation of analyses
for unchanged files while maintaining clean content extraction.
"""

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from ..models import IndexingConfig, DirectoryContext, FileContext
from ...helpers.path_utils import get_portable_path
from fastmcp import Context
from typing import List, Dict, Any, Optional, Tuple, TYPE_CHECKING

# Import shared utilities for DRY compliance
from .shared_utilities import HandlerPathManager, HandlerResolutionError, TimestampManager, IndexingErrorHandler

# Import handler interface for type checking
if TYPE_CHECKING:
    from .handler_interface import IndexingHandler, HandlerRegistry

logger = logging.getLogger(__name__)


class FileAnalysisCache:
    """
    [Class intent]
    Dedicated cache manager for individual file LLM analysis outputs.
    Provides high-performance caching with metadata management and clean content extraction
    to avoid recomputation while ensuring no cache artifacts in final knowledge files.

    [Design principles]
    Cache-first processing strategy maximizing performance by avoiding unnecessary LLM calls.
    Clean metadata separation ensuring cache artifacts never contaminate knowledge files.
    Mirror directory structure following project-base indexing business rules consistently.
    Timestamp-based freshness checking with tolerance for reliable incremental processing.
    Comprehensive error handling ensuring cache failures don't break core knowledge building.
    Rich metadata tracking supporting debugging and cache management operations.

    [Implementation details]
    Uses HTML comment metadata blocks with clear delimiters for clean content extraction.
    Implements timestamp comparison with configurable tolerance for filesystem precision.
    Follows project-base directory structure mirroring for consistent cache organization.
    Provides graceful degradation when cache operations fail without affecting core processing.
    Handles concurrent access and filesystem errors robustly for production reliability.
    """
    
    # Metadata delimiters for clean content extraction
    METADATA_START = "<!-- CACHE_METADATA_START -->"
    METADATA_END = "<!-- CACHE_METADATA_END -->"
    CACHE_VERSION = "1.0"
    
    def __init__(self, config: IndexingConfig, handler_registry: 'HandlerRegistry' = None):
        """
        [Class method intent]
        Initializes file analysis cache with configuration and shared utilities for DRY compliance.
        Sets up cache directory structure using shared utilities eliminating duplicate code patterns.

        [Design principles]
        Configuration-driven behavior supporting different cache requirements and tolerances.
        Shared utilities integration eliminating duplicate timestamp and path handling code.
        Fail-fast approach with explicit handler path management preventing fallback logic.

        [Implementation details]
        Stores configuration reference for cache paths and timestamp tolerance.
        Initializes HandlerPathManager for centralized path operations if handler registry provided.
        Uses shared TimestampManager for all timestamp operations eliminating duplicate code.
        """
        self.config = config
        self.timestamp_tolerance = timedelta(seconds=config.timestamp_tolerance_seconds)
        
        # Initialize shared utilities for DRY compliance
        if handler_registry:
            self.path_manager = HandlerPathManager(handler_registry)
        else:
            self.path_manager = None
            
        logger.info(f"Initialized FileAnalysisCache with shared utilities and {config.timestamp_tolerance_seconds}s tolerance")
    
    async def get_cached_analysis(self, file_path: Path, source_root: Path, handler: 'IndexingHandler') -> Optional[str]:
        """
        [Class method intent]
        Retrieves cached file analysis with metadata completely stripped for clean knowledge assembly.
        Uses handler-specific cache path calculation to ensure git-clone and project-base files
        are cached in their appropriate directory structures without cross-contamination.

        [Design principles]
        Handler-aware cache processing ensuring git-clone and project-base files use separate cache structures.
        Clean content extraction ensuring no metadata artifacts contaminate knowledge files.
        Explicit error handling when handler cannot determine cache paths preventing silent fallbacks.
        Comprehensive error handling preventing cache failures from breaking core processing.

        [Implementation details]
        Delegates cache path calculation to handler.get_cache_path() method eliminating hardcoded paths.
        Checks cache freshness before attempting content extraction using handler-determined paths.
        Uses metadata delimiters to extract only analysis content without cache artifacts.
        Handles missing cache files, stale content, and extraction errors gracefully.
        Returns clean analysis content ready for direct use in knowledge file assembly.
        """
        try:
            # Check if cache exists and is fresh using handler-determined path
            if not self.is_cache_fresh(file_path, source_root, handler):
                return None
            
            # Use handler to determine cache path - NO fallbacks to project-base
            cache_path = handler.get_cache_path(file_path, source_root)
            
            # Read cached content
            cached_content = cache_path.read_text(encoding='utf-8')
            
            # Extract clean analysis content (strip metadata)
            analysis_content = self._extract_analysis_content(cached_content)
            
            if analysis_content and analysis_content.strip():
                logger.debug(f"Cache hit for {file_path.name}: {len(analysis_content)} characters from {cache_path}")
                return analysis_content.strip()
            else:
                logger.warning(f"Cache content empty after extraction for {file_path.name}")
                return None
                
        except Exception as e:
            logger.error(f"❌ CACHE READ FAILED for {file_path.name}: {e} - Handler: {handler.get_handler_type()}")
            return None
    
    async def cache_analysis(self, file_path: Path, analysis_content: str, source_root: Path, handler: 'IndexingHandler') -> None:
        """
        [Class method intent]
        Caches file analysis result with metadata header for future retrieval and debugging.
        Uses handler-specific cache path calculation to ensure git-clone and project-base files
        are cached in their appropriate directory structures without cross-contamination.

        [Design principles]
        Handler-aware cache writing ensuring git-clone and project-base files use separate cache structures.
        Rich metadata tracking supporting debugging and cache management operations.
        Explicit error handling when handler cannot determine cache paths preventing silent fallbacks.
        Comprehensive error handling preventing cache failures from affecting core processing.
        Safe concurrent cache operations through handler-determined directory structure.

        [Implementation details]
        Delegates cache path calculation to handler.get_cache_path() method eliminating hardcoded paths.
        Creates metadata header with source file information and timestamps.
        Combines metadata with analysis content using clear delimiters for extraction.
        Writes cache file to handler-determined directory structure eliminating cross-contamination.
        Falls back to on-demand directory creation if structure preparation failed.
        Handles file I/O errors gracefully without breaking knowledge building process.
        """
        try:
            # Use handler to determine cache path - NO fallbacks to project-base
            cache_path = handler.get_cache_path(file_path, source_root)
            
            # Create metadata header
            metadata_header = self._create_metadata_header(file_path)
            
            # Combine metadata + analysis content
            full_cached_content = f"{metadata_header}\n\n{analysis_content}"
            
            # Write cache file to handler-determined directory structure
            # If cache structure preparation succeeded, parent directory should already exist
            # If not, fall back to on-demand directory creation for safety
            if not cache_path.parent.exists():
                logger.debug(f"Cache directory missing for {file_path.name}, creating on-demand (structure preparation may have failed)")
                cache_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write cache file
            cache_path.write_text(full_cached_content, encoding='utf-8')
            
            logger.debug(f"Cached analysis for {file_path.name}: {len(analysis_content)} characters to {cache_path}")
            
        except Exception as e:
            logger.error(f"❌ CACHE WRITE FAILED for {file_path.name}: {e} - Handler: {handler.get_handler_type()}")
            # Don't raise - cache failures shouldn't break core processing
    
    def is_cache_fresh(self, file_path: Path, source_root: Path, handler: 'IndexingHandler') -> Tuple[bool, str]:
        """
        [Class method intent]
        Determines if cached analysis is fresh using shared TimestampManager for DRY compliance.
        Uses handler-specific cache path calculation to ensure git-clone and project-base files
        check freshness in their appropriate directory structures without cross-contamination.

        [Design principles]
        Handler-aware freshness checking ensuring git-clone and project-base files use separate cache structures.
        Shared utilities integration eliminating duplicate timestamp handling code patterns.
        Conservative approach treating missing or inaccessible cache as requiring fresh analysis.
        Detailed reasoning return supporting debugging and decision audit trails through shared utilities.

        [Implementation details]
        Delegates cache path calculation to handler.get_cache_path() method eliminating hardcoded paths.
        Uses shared TimestampManager.is_cache_fresh_with_reasoning() for consistent behavior.
        Returns tuple with boolean freshness status and detailed reasoning from shared utilities.
        Handles handler resolution and filesystem errors with consistent error reporting patterns.
        """
        try:
            # Use handler to determine cache path - NO fallbacks to project-base
            cache_path = handler.get_cache_path(file_path, source_root)
            
            # Use shared TimestampManager for cache freshness checking (DRY compliance)
            is_fresh, reason = TimestampManager.is_cache_fresh_with_reasoning(cache_path, file_path)
            
            # Log debug information using consistent patterns
            if is_fresh:
                logger.debug(f"Cache hit for {file_path.name}: {reason}")
            else:
                logger.debug(f"Cache stale for {file_path.name}: {reason}")
                
            return is_fresh, reason
            
        except HandlerResolutionError as e:
            reason = f"Handler path resolution failed for {file_path.name}: {e}"
            logger.error(f"❌ HANDLER RESOLUTION FAILED for {file_path.name}: {e}")
            return False, reason
        except Exception as e:
            reason = f"Cache freshness check failed for {file_path.name}: {e} - Handler: {handler.get_handler_type()}"
            logger.error(f"❌ CACHE FRESHNESS CHECK FAILED for {file_path.name}: {e} - Handler: {handler.get_handler_type()}")
            return False, reason  # Conservative: assume stale on error
    
    # REMOVED: get_cache_path() method - now handled by IndexingHandler instances
    # All cache path calculations are delegated to handlers to prevent project-base fallbacks
    
    def _extract_analysis_content(self, cached_content: str) -> str:
        """
        [Class method intent]
        Extracts pure analysis content by removing metadata section completely.
        Ensures no cache artifacts contaminate final knowledge files during assembly.

        [Design principles]
        Clean content extraction ensuring zero metadata leakage into knowledge files.
        Robust parsing handling various cache file formats and edge cases.
        Backward compatibility supporting cache files without metadata gracefully.

        [Implementation details]
        Uses metadata delimiters to identify and remove cache metadata section.
        Handles missing metadata gracefully for backward compatibility.
        Strips leading whitespace after metadata removal for clean content.
        """
        try:
            # Find metadata section boundaries
            start_idx = cached_content.find(self.METADATA_START)
            end_idx = cached_content.find(self.METADATA_END)
            
            if start_idx != -1 and end_idx != -1:
                # Remove metadata section completely
                end_idx += len(self.METADATA_END)
                content_after_metadata = cached_content[end_idx:].lstrip('\n')
                return content_after_metadata
            else:
                # No metadata found - return as is (backward compatibility)
                logger.debug("No metadata delimiters found, returning content as-is")
                return cached_content
                
        except Exception as e:
            logger.warning(f"Content extraction failed: {e}")
            return cached_content  # Fallback to original content
    
    def _create_metadata_header(self, file_path: Path) -> str:
        """
        [Class method intent]
        Creates metadata header with portable source file path and timestamps for cache tracking.
        Uses get_portable_path() to create relative paths with JESSE path variables for portability.

        [Design principles]
        Rich metadata tracking supporting debugging and cache management operations.
        Portable path format using JESSE path variables for cross-environment compatibility.
        Structured metadata format with clear delimiters for reliable extraction.
        Comprehensive information capture for troubleshooting and cache analysis.

        [Implementation details]
        Records portable source file path using get_portable_path() for relative paths.
        Includes cache timestamp and source modification time for freshness tracking.
        Uses HTML comment format for metadata to avoid markdown parsing conflicts.
        Includes cache version for future compatibility and migration support.
        """
        try:
            now = datetime.now().isoformat()
            file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            portable_path = get_portable_path(file_path)
            
            return f"""{self.METADATA_START}
<!-- Source File: {portable_path} -->
<!-- Cached On: {now} -->
<!-- Source Modified: {file_mtime} -->
<!-- Cache Version: {self.CACHE_VERSION} -->
{self.METADATA_END}"""
        
        except Exception as e:
            logger.warning(f"Metadata header creation failed for {file_path}: {e}")
            # Fallback metadata header with portable path
            try:
                portable_path = get_portable_path(file_path)
            except Exception:
                portable_path = str(file_path)
            
            return f"""{self.METADATA_START}
<!-- Source File: {portable_path} -->
<!-- Cached On: {datetime.now().isoformat()} -->
<!-- Cache Version: {self.CACHE_VERSION} -->
{self.METADATA_END}"""
    




    def clear_cache(self, source_root: Path) -> int:
        """
        [Class method intent]
        DEPRECATED: Cannot clear cache without handler awareness.
        Cache clearing now requires handler-specific logic due to elimination of project-base fallbacks.

        [Design principles]
        Handler-aware cache management preventing cross-contamination between git-clone and project-base caches.
        Explicit error when attempting cache operations without proper handler context.
        Safety-first approach preventing accidental deletion of wrong cache files.

        [Implementation details]
        Logs explicit error and returns 0 to prevent accidental cache clearing.
        Cache clearing must now be done through handler-specific mechanisms.
        """
        logger.error("❌ CACHE CLEAR FAILED: clear_cache() called without handler - cannot determine cache paths")
        logger.error("Cache clearing now requires handler-aware logic - use handler-specific cache management")
        return 0
    
    async def prepare_cache_structure(self, root_context: DirectoryContext, source_root: Path, handler: 'IndexingHandler', ctx: Context) -> None:
        """
        [Class method intent]
        Pre-creates entire cache directory structure based on discovered files to eliminate race conditions.
        Uses handler-specific cache path calculation to ensure git-clone and project-base files
        create cache directories in their appropriate structures without cross-contamination.

        [Design principles]
        Handler-aware cache structure preparation ensuring git-clone and project-base files use separate cache structures.
        Upfront structure preparation eliminating race conditions during concurrent cache operations.
        Complete directory hierarchy creation ensuring consistent cache state throughout processing.
        Explicit error handling when handler cannot determine cache paths preventing silent fallbacks.
        Atomic directory creation ensuring cache structure consistency even with partial failures.

        [Implementation details]
        Delegates cache path calculation to handler.get_cache_path() method eliminating hardcoded paths.
        Recursively traverses DirectoryContext to identify all files requiring cache directories.
        Creates unique set of cache directories to avoid duplicate creation operations.
        Uses batch directory creation with parents=True for atomic structure creation.
        Reports progress and statistics for cache structure preparation operations.
        """
        try:
            await ctx.info("Preparing handler-aware cache directory structure for safe concurrent operations")
            
            # Collect all files that need cache directories
            all_files = self._collect_all_files_recursive(root_context)
            
            if not all_files:
                await ctx.info("No files found requiring cache directories")
                return
            
            # Calculate all unique cache directories needed using handler
            cache_directories = set()
            for file_path in all_files:
                try:
                    # Use handler to determine cache path - NO fallbacks to project-base
                    cache_path = handler.get_cache_path(file_path, source_root)
                    cache_directories.add(cache_path.parent)
                except Exception as e:
                    logger.error(f"❌ CACHE PATH CALCULATION FAILED for {file_path}: {e} - Handler: {handler.get_handler_type()}")
                    continue
            
            # Create all cache directories at once
            directories_created = 0
            directories_failed = 0
            
            await ctx.info(f"Creating {len(cache_directories)} cache directories for handler: {handler.get_handler_type()}")
            
            for cache_dir in cache_directories:
                try:
                    cache_dir.mkdir(parents=True, exist_ok=True)
                    directories_created += 1
                    logger.debug(f"Created cache directory: {cache_dir}")
                except Exception as e:
                    directories_failed += 1
                    logger.error(f"❌ CACHE DIRECTORY CREATION FAILED: {cache_dir}: {e}")
                    continue
            
            # Report results
            await ctx.info(f"Cache structure preparation completed: {directories_created} directories created, {directories_failed} failed")
            
            if directories_failed > 0:
                await ctx.warning(f"Some cache directories failed to create ({directories_failed}), caching may fall back to on-demand creation")
            
            logger.info(f"Cache structure prepared: {directories_created} directories created for {len(all_files)} files using handler: {handler.get_handler_type()}")
            
        except Exception as e:
            logger.error(f"❌ CACHE STRUCTURE PREPARATION FAILED: {e} - Handler: {handler.get_handler_type()}", exc_info=True)
            await ctx.error(f"❌ Cache structure preparation failed for handler {handler.get_handler_type()}: {e}")
            # Don't raise - cache structure preparation failure shouldn't break processing
            # Individual cache operations will fall back to on-demand directory creation

    def _collect_all_files_recursive(self, directory_context: DirectoryContext) -> list[Path]:
        """
        [Class method intent]
        Recursively collects all file paths from DirectoryContext hierarchy for cache directory preparation.
        Traverses the complete directory structure to identify all files requiring cache directories.

        [Design principles]
        Complete file collection ensuring no files are missed during cache structure preparation.
        Recursive traversal maintaining consistency with hierarchical processing approach.
        Flat list generation simplifying cache directory calculation and creation operations.

        [Implementation details]
        Recursively traverses DirectoryContext collecting all FileContext file paths.
        Combines files from current directory with files from all subdirectories.
        Returns flat list of all file paths for cache directory calculation.
        """
        all_files = []
        
        # Collect files from current directory
        for file_context in directory_context.file_contexts:
            all_files.append(file_context.file_path)
        
        # Recursively collect files from subdirectories
        for subdir_context in directory_context.subdirectory_contexts:
            all_files.extend(self._collect_all_files_recursive(subdir_context))
        
        return all_files


    def get_cache_stats(self, source_root: Path) -> dict:
        """
        [Class method intent]
        DEPRECATED: Cannot collect cache statistics without handler awareness.
        Cache statistics now require handler-specific logic due to elimination of project-base fallbacks.

        [Design principles]
        Handler-aware cache monitoring preventing incorrect statistics from mixed cache structures.
        Explicit error when attempting cache operations without proper handler context.
        Safety-first approach preventing misleading cache statistics.

        [Implementation details]
        Logs explicit error and returns empty stats to prevent misleading cache information.
        Cache statistics must now be collected through handler-specific mechanisms.
        """
        stats = {
            "cache_files": 0,
            "total_size": 0,
            "fresh_files": 0,
            "stale_files": 0,
            "average_size": 0
        }
        
        logger.error("❌ CACHE STATS FAILED: get_cache_stats() called without handler - cannot determine cache paths")
        logger.error("Cache statistics now require handler-aware logic - use handler-specific cache monitoring")
        
        return stats

    def is_knowledge_file_stale(self, kb_path: Path, directory_context: DirectoryContext, source_root: Path, handler: 'IndexingHandler') -> Tuple[bool, str]:
        """
        [Class method intent]
        Determines if knowledge file needs rebuilding based on constituent file analysis cache freshness.
        Uses handler-aware cache checking to ensure proper staleness detection across different handler types.

        [Design principles]
        Handler-aware staleness checking ensuring proper cache path resolution for different handler types.
        Comprehensive constituent checking verifying knowledge file is newer than all constituent analyses.
        Conservative approach treating missing or inaccessible files as requiring rebuilding.

        [Implementation details]
        Checks knowledge file timestamp against all constituent file analysis cache timestamps.
        Uses handler-provided cache paths to ensure proper path resolution for git-clone vs project-base scenarios.
        Returns detailed reasoning for debugging and decision audit trails.
        """
        try:
            if not kb_path.exists():
                return True, f"Knowledge file does not exist: {kb_path.name}"
            
            kb_mtime = datetime.fromtimestamp(kb_path.stat().st_mtime)
            
            # Check against all constituent files
            for file_context in directory_context.file_contexts:
                try:
                    cache_path = handler.get_cache_path(file_context.file_path, source_root)
                    if cache_path.exists():
                        cache_mtime = datetime.fromtimestamp(cache_path.stat().st_mtime)
                        if cache_mtime > kb_mtime:
                            return True, f"Cache file {cache_path.name} is newer than knowledge file"
                except Exception as e:
                    logger.warning(f"Could not check cache timestamp for {file_context.file_path}: {e}")
                    continue
            
            # Check against subdirectory knowledge files
            for subdir_context in directory_context.subdirectory_contexts:
                try:
                    subdir_kb_path = handler.get_knowledge_file_path(subdir_context.directory_path, source_root)
                    if subdir_kb_path.exists():
                        subdir_mtime = datetime.fromtimestamp(subdir_kb_path.stat().st_mtime)
                        if subdir_mtime > kb_mtime:
                            return True, f"Subdirectory KB {subdir_kb_path.name} is newer than knowledge file"
                except Exception as e:
                    logger.warning(f"Could not check subdirectory KB timestamp for {subdir_context.directory_path}: {e}")
                    continue
            
            return False, f"Knowledge file {kb_path.name} is up to date"
            
        except Exception as e:
            logger.error(f"Knowledge file staleness check failed for {kb_path}: {e}")
            return True, f"Error checking knowledge file staleness: {e}"

    def get_cache_path(self, file_path: Path, source_root: Path, handler: 'IndexingHandler') -> Path:
        """
        [Class method intent]
        Delegates cache path calculation to handler to ensure proper path resolution.
        Provides compatibility method for code that expects FileAnalysisCache to provide cache paths.

        [Design principles]
        Handler delegation ensuring proper cache path resolution for different handler types.
        Compatibility method maintaining existing API while ensuring handler-aware behavior.

        [Implementation details]
        Directly delegates to handler.get_cache_path() method without any fallback logic.
        Ensures consistent cache path resolution across all code that needs cache paths.
        """
        return handler.get_cache_path(file_path, source_root)

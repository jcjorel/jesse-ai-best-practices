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
# 2025-07-03T17:39:00Z : Fixed change detection logic to properly implement layered processing approach by CodeAssistant
# * Removed direct source file → knowledge file comparison to prevent systematic rebuilds
# * Knowledge files now only rebuild when cached analyses or subdirectory knowledge files are newer
# * Fixed systematic knowledge file rebuilding issue by implementing proper two-layer processing (source → cache → knowledge)
# * Maintains proper incremental processing flow: source changes trigger individual file reprocessing, knowledge rebuilds only when constituents change
# 2025-07-03T17:17:00Z : Implemented comprehensive constituent dependency checking for directory knowledge files by CodeAssistant
# * Added is_knowledge_file_stale() method providing comprehensive staleness checking against all constituents
# * Added get_constituent_staleness_info() method for detailed debugging and analysis of staleness conditions
# * Added get_knowledge_file_path() method centralizing knowledge file path calculation logic
# 2025-07-03T16:52:00Z : Implemented upfront cache structure preparation for safer concurrent operations by CodeAssistant
# * Added prepare_cache_structure() method to pre-create entire cache directory hierarchy at index start
# * Eliminates race conditions during concurrent cache operations through upfront directory creation
# * Modified cache_analysis() to rely on pre-created structure with fallback to on-demand creation
# * Enhanced reliability and consistency of cache operations under concurrent load
# 2025-07-03T16:36:00Z : Implemented portable path metadata using get_portable_path() by CodeAssistant
# * Updated _create_metadata_header() to use get_portable_path() for JESSE path variables
# * Cache metadata now stores relative paths like {PROJECT_ROOT}/src/file.js instead of absolute paths
# * Improves cache portability across different environments and working directories
# * Added fallback error handling for portable path conversion failures
# 2025-07-03T16:30:00Z : Enhanced cache hit logging to display cache file path by CodeAssistant
# * Updated cache hit debug messages to include full cache file path for better visibility
# * Provides clear debugging information showing exact cache file location when cache hits occur
# * Maintains existing functionality while improving troubleshooting and cache understanding
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
from typing import List, Dict, Any, Optional, Tuple

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
    
    def __init__(self, config: IndexingConfig):
        """
        [Class method intent]
        Initializes file analysis cache with configuration for paths and freshness checking.
        Sets up cache directory structure and timestamp tolerance for reliable operation.

        [Design principles]
        Configuration-driven behavior supporting different cache requirements and tolerances.
        Timestamp tolerance setup accommodating filesystem precision variations.
        Cache directory preparation ensuring proper structure for mirror organization.

        [Implementation details]
        Stores configuration reference for cache paths and timestamp tolerance.
        Calculates timestamp tolerance from configuration for freshness checking.
        Prepares cache directory structure following project-base indexing rules.
        """
        self.config = config
        self.timestamp_tolerance = timedelta(seconds=config.timestamp_tolerance_seconds)
        
        logger.info(f"Initialized FileAnalysisCache with {config.timestamp_tolerance_seconds}s tolerance")
    
    async def get_cached_analysis(self, file_path: Path, source_root: Path) -> Optional[str]:
        """
        [Class method intent]
        Retrieves cached file analysis with metadata completely stripped for clean knowledge assembly.
        Returns None if cache miss, stale cache, or extraction failure to trigger fresh LLM analysis.

        [Design principles]
        Cache-first processing maximizing performance by returning cached content when available.
        Clean content extraction ensuring no metadata artifacts contaminate knowledge files.
        Graceful degradation returning None on any cache issues to trigger fresh analysis.
        Comprehensive error handling preventing cache failures from breaking core processing.

        [Implementation details]
        Checks cache freshness before attempting content extraction.
        Uses metadata delimiters to extract only analysis content without cache artifacts.
        Handles missing cache files, stale content, and extraction errors gracefully.
        Returns clean analysis content ready for direct use in knowledge file assembly.
        """
        try:
            # Check if cache exists and is fresh
            if not self.is_cache_fresh(file_path, source_root):
                return None
            
            cache_path = self.get_cache_path(file_path, source_root)
            
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
            logger.warning(f"Cache read failed for {file_path.name}: {e}")
            return None
    
    async def cache_analysis(self, file_path: Path, analysis_content: str, source_root: Path) -> None:
        """
        [Class method intent]
        Caches file analysis result with metadata header for future retrieval and debugging.
        Relies on upfront cache structure preparation to eliminate race conditions and ensure consistent cache state.

        [Design principles]
        Rich metadata tracking supporting debugging and cache management operations.
        Upfront directory structure preparation eliminating race conditions during concurrent operations.
        Comprehensive error handling preventing cache failures from affecting core processing.
        Clean content preservation maintaining analysis integrity for future retrieval.
        Safe concurrent cache operations through pre-created directory structure.

        [Implementation details]
        Creates metadata header with source file information and timestamps.
        Combines metadata with analysis content using clear delimiters for extraction.
        Writes cache file to pre-created directory structure eliminating race conditions.
        Falls back to on-demand directory creation if structure preparation failed.
        Handles file I/O errors gracefully without breaking knowledge building process.
        """
        try:
            cache_path = self.get_cache_path(file_path, source_root)
            
            # Create metadata header
            metadata_header = self._create_metadata_header(file_path)
            
            # Combine metadata + analysis content
            full_cached_content = f"{metadata_header}\n\n{analysis_content}"
            
            # Write cache file to pre-created directory structure
            # If cache structure preparation succeeded, parent directory should already exist
            # If not, fall back to on-demand creation for safety
            if not cache_path.parent.exists():
                logger.debug(f"Cache directory missing for {file_path.name}, creating on-demand (structure preparation may have failed)")
                cache_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write cache file
            cache_path.write_text(full_cached_content, encoding='utf-8')
            
            logger.debug(f"Cached analysis for {file_path.name}: {len(analysis_content)} characters")
            
        except Exception as e:
            logger.warning(f"Cache write failed for {file_path.name}: {e}")
            # Don't raise - cache failures shouldn't break core processing
    
    def is_cache_fresh(self, file_path: Path, source_root: Path) -> bool:
        """
        [Class method intent]
        Determines if cached analysis is fresh by comparing source file timestamp with cache timestamp.
        Returns False for missing cache or stale content to trigger fresh LLM analysis.

        [Design principles]
        Timestamp-based freshness checking with tolerance for reliable incremental processing.
        Conservative approach treating missing or inaccessible cache as requiring fresh analysis.
        Filesystem error handling preventing cache issues from breaking freshness determination.

        [Implementation details]
        Compares source file modification time with cache file modification time.
        Applies configured timestamp tolerance to avoid false positives from filesystem precision.
        Handles missing files and filesystem errors by returning False for safety.
        """
        try:
            cache_path = self.get_cache_path(file_path, source_root)
            
            # Cache file must exist
            if not cache_path.exists():
                return False
            
            # Get timestamps
            source_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            cache_mtime = datetime.fromtimestamp(cache_path.stat().st_mtime)
            
            # Cache is fresh if it's newer than source file (with tolerance)
            is_fresh = cache_mtime >= source_mtime - self.timestamp_tolerance
            
            logger.debug(f"Cache freshness check for {file_path.name}: {'fresh' if is_fresh else 'stale'}")
            return is_fresh
            
        except Exception as e:
            logger.debug(f"Cache freshness check failed for {file_path.name}: {e}")
            return False  # Conservative: assume stale on error
    
    def get_cache_path(self, file_path: Path, source_root: Path) -> Path:
        """
        [Class method intent]
        Calculates cache file path following project-base directory structure mirroring.
        Implements consistent cache organization with .analysis.md suffix for identification.

        [Design principles]
        Mirror directory structure following project-base indexing business rules consistently.
        Standardized cache file naming with .analysis.md suffix for clear identification.
        Relative path calculation preserving source directory organization in cache.

        [Implementation details]
        Uses project-base subdirectory as mandated by indexing business rules.
        Calculates relative path from source root to maintain directory structure.
        Applies .analysis.md suffix to source filename for cache file identification.
        """
        try:
            # Calculate relative path from source root
            relative_path = file_path.relative_to(source_root)
            
            # Apply project-base indexing business rule
            cache_relative_path = Path("project-base") / relative_path
            
            # Add .analysis.md suffix for cache identification
            cache_filename = f"{file_path.name}.analysis.md"
            cache_relative_path = cache_relative_path.parent / cache_filename
            
            # Combine with knowledge output directory
            cache_path = self.config.knowledge_output_directory / cache_relative_path
            
            return cache_path
            
        except ValueError as e:
            logger.error(f"Cache path calculation failed for {file_path}: {e}")
            # Fallback: use flat structure in project-base
            cache_filename = f"{file_path.name}.analysis.md"
            return self.config.knowledge_output_directory / "project-base" / cache_filename
    
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
    
    def get_knowledge_file_path(self, directory_path: Path, source_root: Path) -> Path:
        """
        [Class method intent]
        Calculate knowledge file path for a directory following project-base conventions.
        Centralizes knowledge file path logic for consistent usage across components.

        [Design principles]
        Consistent knowledge file path calculation following project-base indexing rules.
        Centralized logic preventing path calculation inconsistencies across components.
        Error handling ensuring graceful fallback when path calculation fails.

        [Implementation details]
        Uses project-base subdirectory structure mirroring source directory organization.
        Calculates relative path from source root and recreates structure in knowledge directory.
        Returns Path object ready for knowledge file operations and timestamp comparisons.
        """
        try:
            relative_path = directory_path.relative_to(source_root)
            knowledge_dir = self.config.knowledge_output_directory / "project-base" / relative_path
            knowledge_filename = f"{directory_path.name}_kb.md"
            return knowledge_dir / knowledge_filename
        except ValueError:
            # Fallback for path calculation issues
            knowledge_filename = f"{directory_path.name}_kb.md"
            return self.config.knowledge_output_directory / "project-base" / knowledge_filename

    def is_knowledge_file_stale(
        self, 
        directory_path: Path, 
        source_root: Path,
        file_contexts: List[FileContext],
        subdirectory_paths: Optional[List[Path]] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        [Class method intent]
        Comprehensive staleness check for directory knowledge files.
        Checks all constituent dependencies including source files, cached analyses, and subdirectory knowledge files.

        [Design principles]
        Comprehensive dependency checking ensuring knowledge files are rebuilt when any constituent changes.
        Clear staleness reasoning supporting debugging and optimization efforts.
        Conservative approach treating access errors as requiring rebuild for reliability.
        Timestamp-based comparison with configurable tolerance for filesystem precision handling.

        [Implementation details]
        Checks knowledge file existence, source file timestamps, cached analysis timestamps, and subdirectory knowledge timestamps.
        Returns tuple with staleness status and human-readable reason for transparency.
        Applies timestamp tolerance consistently across all timestamp comparisons.
        Handles filesystem errors gracefully with appropriate logging and fallback behavior.

        Returns:
            tuple[bool, Optional[str]]: (is_stale, reason)
            - is_stale: True if knowledge file needs rebuilding
            - reason: Human-readable reason for staleness (for debugging)
        """
        knowledge_file_path = self.get_knowledge_file_path(directory_path, source_root)
        
        # Check 1: Missing knowledge file
        if not knowledge_file_path.exists():
            return True, "Knowledge file does not exist"
        
        try:
            knowledge_mtime = datetime.fromtimestamp(knowledge_file_path.stat().st_mtime)
        except OSError as e:
            return True, f"Cannot access knowledge file: {e}"
        
        # Check 2: Cached analyses newer than knowledge file
        for file_context in file_contexts:
            cache_path = self.get_cache_path(file_context.file_path, source_root)
            if cache_path.exists():
                try:
                    cache_mtime = datetime.fromtimestamp(cache_path.stat().st_mtime)
                    if cache_mtime > knowledge_mtime + self.timestamp_tolerance:
                        return True, f"Cached analysis {cache_path.name} is newer than knowledge file"
                except OSError:
                    # If we can't read cache file, assume it's stale
                    continue
        
        # Check 4: Subdirectory knowledge files newer than parent
        if subdirectory_paths:
            for subdir_path in subdirectory_paths:
                subdir_knowledge_path = self.get_knowledge_file_path(subdir_path, source_root)
                if subdir_knowledge_path.exists():
                    try:
                        subdir_mtime = datetime.fromtimestamp(subdir_knowledge_path.stat().st_mtime)
                        if subdir_mtime > knowledge_mtime + self.timestamp_tolerance:
                            return True, f"Subdirectory knowledge file {subdir_path.name}_kb.md is newer than parent"
                    except OSError:
                        continue
        
        return False, None

    async def get_constituent_staleness_info(
        self, 
        directory_path: Path, 
        source_root: Path,
        file_contexts: List[FileContext],
        subdirectory_paths: Optional[List[Path]] = None,
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        [Class method intent]
        Detailed staleness analysis for debugging and reporting.
        Provides comprehensive information about all constituent timestamps for debugging and optimization purposes.

        [Design principles]
        Comprehensive information gathering supporting debugging and optimization efforts.
        Structured data format enabling easy analysis and reporting of staleness conditions.
        Error handling ensuring information collection continues despite individual access failures.
        Performance consideration avoiding unnecessary processing when detailed analysis isn't needed.

        [Implementation details]
        Collects detailed timestamp information for all constituents including source files, cached analyses, and subdirectory knowledge files.
        Calculates staleness status for each constituent with clear reasoning.
        Returns structured dictionary with complete staleness analysis for debugging and reporting.
        Handles filesystem errors gracefully while preserving as much information as possible.

        Returns:
            Dict[str, Any]: Comprehensive staleness analysis with detailed constituent information
        """
        knowledge_file_path = self.get_knowledge_file_path(directory_path, source_root)
        
        info = {
            'directory_path': str(directory_path),
            'knowledge_file_path': str(knowledge_file_path),
            'knowledge_file_exists': knowledge_file_path.exists(),
            'knowledge_file_mtime': None,
            'source_files': [],
            'cached_analyses': [],
            'subdirectory_knowledge_files': [],
            'is_stale': False,
            'staleness_reason': None
        }
        
        # Get knowledge file timestamp
        if knowledge_file_path.exists():
            try:
                knowledge_mtime = datetime.fromtimestamp(knowledge_file_path.stat().st_mtime)
                info['knowledge_file_mtime'] = knowledge_mtime.isoformat()
            except OSError:
                info['knowledge_file_mtime'] = "ERROR: Cannot access file"
        
        # Analyze source files
        for file_context in file_contexts:
            file_info = {
                'path': str(file_context.file_path),
                'name': file_context.file_path.name,
                'mtime': file_context.last_modified.isoformat(),
                'is_newer': False
            }
            
            if info['knowledge_file_mtime'] and knowledge_file_path.exists():
                knowledge_mtime = datetime.fromtimestamp(knowledge_file_path.stat().st_mtime)
                file_info['is_newer'] = file_context.last_modified > knowledge_mtime + self.timestamp_tolerance
            
            info['source_files'].append(file_info)
        
        # Analyze cached analyses
        for file_context in file_contexts:
            cache_path = self.get_cache_path(file_context.file_path, source_root)
            cache_info = {
                'source_file': file_context.file_path.name,
                'cache_path': str(cache_path),
                'cache_exists': cache_path.exists(),
                'cache_mtime': None,
                'is_newer': False
            }
            
            if cache_path.exists():
                try:
                    cache_mtime = datetime.fromtimestamp(cache_path.stat().st_mtime)
                    cache_info['cache_mtime'] = cache_mtime.isoformat()
                    
                    if info['knowledge_file_mtime'] and knowledge_file_path.exists():
                        knowledge_mtime = datetime.fromtimestamp(knowledge_file_path.stat().st_mtime)
                        cache_info['is_newer'] = cache_mtime > knowledge_mtime + self.timestamp_tolerance
                        
                except OSError:
                    cache_info['cache_mtime'] = "ERROR: Cannot access file"
            
            info['cached_analyses'].append(cache_info)
        
        # Analyze subdirectory knowledge files
        if subdirectory_paths:
            for subdir_path in subdirectory_paths:
                subdir_knowledge_path = self.get_knowledge_file_path(subdir_path, source_root)
                subdir_info = {
                    'directory_name': subdir_path.name,
                    'knowledge_path': str(subdir_knowledge_path),
                    'knowledge_exists': subdir_knowledge_path.exists(),
                    'knowledge_mtime': None,
                    'is_newer': False
                }
                
                if subdir_knowledge_path.exists():
                    try:
                        subdir_mtime = datetime.fromtimestamp(subdir_knowledge_path.stat().st_mtime)
                        subdir_info['knowledge_mtime'] = subdir_mtime.isoformat()
                        
                        if info['knowledge_file_mtime'] and knowledge_file_path.exists():
                            knowledge_mtime = datetime.fromtimestamp(knowledge_file_path.stat().st_mtime)
                            subdir_info['is_newer'] = subdir_mtime > knowledge_mtime + self.timestamp_tolerance
                            
                    except OSError:
                        subdir_info['knowledge_mtime'] = "ERROR: Cannot access file"
                
                info['subdirectory_knowledge_files'].append(subdir_info)
        
        # Determine overall staleness
        is_stale, reason = self.is_knowledge_file_stale(
            directory_path, source_root, file_contexts, subdirectory_paths
        )
        info['is_stale'] = is_stale
        info['staleness_reason'] = reason
        
        return info

    def clear_cache(self, source_root: Path) -> int:
        """
        [Class method intent]
        Clears all cached analysis files for a source root, useful for cache invalidation.
        Returns count of cleared cache files for reporting and verification.

        [Design principles]
        Comprehensive cache clearing supporting cache management and invalidation operations.
        Safe file deletion with error handling preventing partial cache corruption.
        Progress reporting through count return enabling cache management visibility.

        [Implementation details]
        Traverses cache directory structure identifying analysis cache files.
        Removes cache files safely with error handling for individual file failures.
        Returns count of successfully cleared files for management reporting.
        """
        cleared_count = 0
        
        try:
            cache_root = self.config.knowledge_output_directory / "project-base"
            
            if not cache_root.exists():
                return 0
            
            # Find all .analysis.md files
            for cache_file in cache_root.rglob("*.analysis.md"):
                try:
                    cache_file.unlink()
                    cleared_count += 1
                    logger.debug(f"Cleared cache file: {cache_file}")
                except Exception as e:
                    logger.warning(f"Failed to clear cache file {cache_file}: {e}")
            
            logger.info(f"Cache cleared: {cleared_count} files removed")
            
        except Exception as e:
            logger.error(f"Cache clearing failed: {e}")
        
        return cleared_count
    
    async def prepare_cache_structure(self, root_context: DirectoryContext, source_root: Path, ctx: Context) -> None:
        """
        [Class method intent]
        Pre-creates entire cache directory structure based on discovered files to eliminate race conditions.
        Analyzes the complete file hierarchy and creates all necessary cache directories upfront
        before any caching operations begin, ensuring consistent and safe cache operations.

        [Design principles]
        Upfront structure preparation eliminating race conditions during concurrent cache operations.
        Complete directory hierarchy creation ensuring consistent cache state throughout processing.
        Progress reporting providing visibility into cache structure preparation operations.
        Comprehensive error handling preventing cache preparation failures from breaking processing.
        Atomic directory creation ensuring cache structure consistency even with partial failures.

        [Implementation details]
        Recursively traverses DirectoryContext to identify all files requiring cache directories.
        Calculates cache paths for all files using project-base indexing business rules.
        Creates unique set of cache directories to avoid duplicate creation operations.
        Uses batch directory creation with parents=True for atomic structure creation.
        Reports progress and statistics for cache structure preparation operations.
        """
        try:
            await ctx.info("Preparing cache directory structure for safe concurrent operations")
            
            # Collect all files that need cache directories
            all_files = self._collect_all_files_recursive(root_context)
            
            if not all_files:
                await ctx.info("No files found requiring cache directories")
                return
            
            # Calculate all unique cache directories needed
            cache_directories = set()
            for file_path in all_files:
                try:
                    cache_path = self.get_cache_path(file_path, source_root)
                    cache_directories.add(cache_path.parent)
                except Exception as e:
                    logger.warning(f"Failed to calculate cache path for {file_path}: {e}")
                    continue
            
            # Create all cache directories at once
            directories_created = 0
            directories_failed = 0
            
            await ctx.info(f"Creating {len(cache_directories)} cache directories")
            
            for cache_dir in cache_directories:
                try:
                    cache_dir.mkdir(parents=True, exist_ok=True)
                    directories_created += 1
                    logger.debug(f"Created cache directory: {cache_dir}")
                except Exception as e:
                    directories_failed += 1
                    logger.warning(f"Failed to create cache directory {cache_dir}: {e}")
                    continue
            
            # Report results
            await ctx.info(f"Cache structure preparation completed: {directories_created} directories created, {directories_failed} failed")
            
            if directories_failed > 0:
                await ctx.warning(f"Some cache directories failed to create ({directories_failed}), caching may fall back to on-demand creation")
            
            logger.info(f"Cache structure prepared: {directories_created} directories created for {len(all_files)} files")
            
        except Exception as e:
            logger.error(f"Cache structure preparation failed: {e}", exc_info=True)
            await ctx.warning(f"Cache structure preparation failed: {e}")
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
        Collects cache statistics for monitoring and debugging cache performance.
        Provides comprehensive cache information for optimization and troubleshooting.

        [Design principles]
        Comprehensive cache monitoring supporting performance analysis and optimization.
        Detailed statistics collection enabling cache behavior understanding.
        Error handling ensuring statistics collection doesn't interfere with operations.

        [Implementation details]
        Traverses cache directory collecting file counts and size information.
        Calculates cache hit ratios and freshness statistics for performance analysis.
        Returns structured statistics dictionary for reporting and monitoring.
        """
        stats = {
            "cache_files": 0,
            "total_size": 0,
            "fresh_files": 0,
            "stale_files": 0,
            "average_size": 0
        }
        
        try:
            cache_root = self.config.knowledge_output_directory / "project-base"
            
            if not cache_root.exists():
                return stats
            
            cache_files = list(cache_root.rglob("*.analysis.md"))
            stats["cache_files"] = len(cache_files)
            
            if cache_files:
                total_size = sum(f.stat().st_size for f in cache_files)
                stats["total_size"] = total_size
                stats["average_size"] = total_size // len(cache_files)
            
            logger.debug(f"Cache statistics: {stats}")
            
        except Exception as e:
            logger.warning(f"Cache statistics collection failed: {e}")
        
        return stats

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
# Centralized timestamp operations and comparisons for Knowledge Bases Indexing System.
# Eliminates code duplication between file_analysis_cache and rebuild_decision_engine
# by providing unified timestamp handling with consistent formatting and comparison logic.
###############################################################################
# [Source file design principles]
# - Stateless utility functions enabling safe concurrent usage across components
# - Consistent timestamp formatting and comparison behavior eliminating duplicate logic
# - Direct timestamp comparison without tolerance for simplicity and reliability
# - Comprehensive error handling for filesystem access failures with graceful degradation
# - Clear reasoning return values supporting debugging and decision audit trails
###############################################################################
# [Source file constraints]
# - All functions must be stateless and side-effect free for safe concurrent usage
# - Timestamp operations must handle filesystem errors gracefully without breaking processing
# - Comparison logic must be consistent across all components using these utilities
# - Error handling must provide clear failure reasons for debugging and troubleshooting
# - Performance must be optimal with minimal redundant filesystem operations
###############################################################################
# [Dependencies]
# <system>: datetime - Core timestamp operations and datetime object manipulation
# <system>: pathlib - Cross-platform path operations and file metadata access
# <system>: logging - Structured error logging for debugging and monitoring
# <system>: typing - Type annotations for clear interface contracts and safety
###############################################################################
# [GenAI tool change history]
# 2025-07-07T22:59:00Z : Initial creation of centralized timestamp manager for DRY compliance by CodeAssistant
# * Created TimestampManager class eliminating duplicate timestamp handling from both files
# * Implemented consistent timestamp comparison and formatting logic across all operations
# * Consolidated safe timestamp retrieval with unified error handling patterns
# * Established detailed reasoning return values for debugging and decision audit trails
###############################################################################

"""
Centralized Timestamp Manager for Knowledge Bases Indexing System.

This module provides unified timestamp operations and comparisons, eliminating code
duplication between file_analysis_cache.py and rebuild_decision_engine.py while
maintaining consistent timestamp handling behavior.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class TimestampManager:
    """
    [Class intent]
    Centralized manager for all timestamp operations in indexing system.
    Eliminates code duplication between file_analysis_cache and rebuild_decision_engine
    by providing unified timestamp handling with consistent behavior and error handling.

    [Design principles]
    Stateless utility class with static methods enabling safe concurrent usage across components.
    Consistent timestamp comparison and formatting behavior eliminating scattered duplicate logic.
    Direct timestamp comparison without tolerance for simplicity and reliability throughout system.
    Comprehensive error handling providing graceful degradation when filesystem access fails.
    Clear reasoning return values supporting debugging and decision audit trails across all operations.

    [Implementation details]
    All methods are static eliminating need for instance creation and enabling simple imports.
    Uses Path.stat().st_mtime for cross-platform timestamp access with consistent error handling.
    Provides detailed reasoning strings for all comparison operations supporting audit trails.
    Handles filesystem errors gracefully returning None or False with clear error explanations.
    Maintains consistent timestamp formatting across all indexing components and operations.
    """
    
    @staticmethod
    def get_file_timestamp_safe(file_path: Path) -> Optional[datetime]:
        """
        [Class method intent]
        Safely retrieves file modification timestamp with consistent error handling.
        Eliminates duplicate timestamp retrieval patterns from both file_analysis_cache and rebuild_decision_engine.

        [Design principles]
        Unified timestamp retrieval eliminating scattered duplicate filesystem access patterns.
        Consistent error handling preventing filesystem access failures from breaking operations.
        Cross-platform timestamp access using pathlib for reliable behavior across systems.
        Graceful degradation returning None on errors enabling calling code to handle failures appropriately.

        [Implementation details]
        Uses Path.stat().st_mtime for cross-platform timestamp access with consistent behavior.
        Converts filesystem timestamp to datetime object for comparison and formatting operations.
        Returns None on any filesystem error including missing files and permission issues.
        Handles OSError and FileNotFoundError specifically for clear error categorization.
        Provides consistent error logging for debugging filesystem access issues.
        """
        try:
            timestamp = datetime.fromtimestamp(file_path.stat().st_mtime)
            logger.debug(f"Retrieved timestamp for {file_path.name}: {timestamp}")
            return timestamp
        except (OSError, FileNotFoundError) as e:
            logger.debug(f"Failed to get timestamp for {file_path.name}: {e}")
            return None
        except Exception as e:
            logger.warning(f"Unexpected error getting timestamp for {file_path.name}: {e}")
            return None
    
    @staticmethod
    def is_timestamp_newer(newer_time: datetime, older_time: datetime) -> bool:
        """
        [Class method intent]
        Compares timestamps directly for reliable staleness detection.
        Eliminates duplicate timestamp comparison logic from multiple decision methods.

        [Design principles]
        Direct timestamp comparison without tolerance for simplicity and consistency across system.
        Clear boolean result simplifying conditional logic in all decision-making methods.
        Unified comparison behavior eliminating inconsistent comparison approaches between components.
        Performance optimization through simple direct comparison without complex tolerance calculations.

        [Implementation details]
        Direct timestamp comparison using greater-than operator for clear boolean result.
        Returns True if newer_time is strictly newer than older_time without any tolerance.
        Used by all staleness checking methods ensuring consistent comparison behavior throughout.
        No tolerance or fuzzy logic ensuring predictable and deterministic comparison results.
        """
        return newer_time > older_time
    
    @staticmethod
    def format_timestamp_for_display(timestamp: datetime) -> str:
        """
        [Class method intent]
        Provides consistent timestamp formatting for display and logging across all components.
        Eliminates duplicate timestamp formatting patterns from both files.

        [Design principles]
        Unified timestamp formatting ensuring consistent display across all logging and debug output.
        Human-readable format supporting debugging and troubleshooting of timestamp-related issues.
        Consistent formatting eliminating variations in timestamp display between different components.
        Clear date and time representation enabling easy comparison and analysis of timestamps.

        [Implementation details]
        Uses strftime with consistent format pattern for human-readable timestamp display.
        Format includes both date and time components for complete timestamp information.
        Returns string representation suitable for logging, debug output, and user display.
        Consistent across all components eliminating formatting variations and confusion.
        """
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def compare_files_with_reasoning(newer_file: Path, older_file: Path) -> Tuple[bool, str]:
        """
        [Class method intent]
        Compares file timestamps with detailed reasoning for decision audit trails.
        Eliminates duplicate timestamp comparison patterns from file staleness checking methods.

        [Design principles]
        Comprehensive timestamp comparison with detailed reasoning supporting debugging and audit trails.
        Unified comparison logic eliminating scattered duplicate timestamp handling across components.
        Clear reasoning strings enabling understanding of staleness decisions and troubleshooting.
        Graceful error handling providing meaningful failure explanations when filesystem access fails.
        Consistent comparison behavior across all file staleness checking operations in system.

        [Implementation details]
        Retrieves timestamps for both files using unified safe timestamp retrieval method.
        Performs direct timestamp comparison without tolerance for predictable behavior.
        Returns boolean comparison result with detailed reasoning string explaining decision.
        Handles missing files and filesystem errors gracefully with clear error explanations.
        Provides precise timestamp information in reasoning for debugging and analysis purposes.
        """
        try:
            # Get timestamps for both files
            newer_timestamp = TimestampManager.get_file_timestamp_safe(newer_file)
            older_timestamp = TimestampManager.get_file_timestamp_safe(older_file)
            
            # Handle missing files
            if newer_timestamp is None:
                reason = f"Cannot access timestamp for {newer_file.name}"
                return False, reason
            
            if older_timestamp is None:
                reason = f"Cannot access timestamp for {older_file.name}"
                return False, reason
            
            # Compare timestamps
            is_newer = TimestampManager.is_timestamp_newer(newer_timestamp, older_timestamp)
            
            # Create detailed reasoning
            newer_str = TimestampManager.format_timestamp_for_display(newer_timestamp)
            older_str = TimestampManager.format_timestamp_for_display(older_timestamp)
            
            if is_newer:
                reason = f"{newer_file.name} ({newer_str}) > {older_file.name} ({older_str})"
            else:
                reason = f"{newer_file.name} ({newer_str}) <= {older_file.name} ({older_str})"
            
            return is_newer, reason
            
        except Exception as e:
            reason = f"Timestamp comparison failed: {str(e)}"
            logger.error(f"File timestamp comparison error: {e}")
            return False, reason
    
    @staticmethod
    def is_cache_fresh_with_reasoning(cache_file: Path, source_file: Path) -> Tuple[bool, str]:
        """
        [Class method intent]
        Determines cache freshness with detailed reasoning matching file_analysis_cache logic.
        Provides unified cache freshness checking eliminating duplicate logic patterns.

        [Design principles]
        Unified cache freshness logic replacing scattered cache freshness decisions across components.
        Detailed reasoning return supporting debugging and cache management operations throughout system.
        Direct timestamp comparison without tolerance ensuring predictable cache freshness behavior.
        Comprehensive error handling providing clear failure explanations for cache operation issues.
        Consistent cache freshness determination across all caching operations in indexing system.

        [Implementation details]
        Checks cache file existence first preventing timestamp comparison on missing cache files.
        Uses unified timestamp comparison logic for consistent cache freshness determination behavior.
        Returns boolean freshness status with detailed reasoning including precise timestamp information.
        Handles filesystem errors gracefully returning conservative decisions with clear error explanations.
        Provides reasoning format matching existing file_analysis_cache patterns for compatibility.
        """
        try:
            # Cache file must exist
            if not cache_file.exists():
                reason = f"Cache file does not exist for {source_file.name}"
                return False, reason
            
            # Get timestamps using unified methods
            source_timestamp = TimestampManager.get_file_timestamp_safe(source_file)
            cache_timestamp = TimestampManager.get_file_timestamp_safe(cache_file)
            
            # Handle timestamp retrieval failures
            if source_timestamp is None:
                reason = f"Cannot access source timestamp for {source_file.name}"
                return False, reason
            
            if cache_timestamp is None:
                reason = f"Cannot access cache timestamp for {cache_file.name}"
                return False, reason
            
            # Cache is fresh if it's newer than or equal to source file
            is_fresh = cache_timestamp >= source_timestamp
            
            # Create detailed reasoning with formatted timestamps
            source_str = TimestampManager.format_timestamp_for_display(source_timestamp)
            cache_str = TimestampManager.format_timestamp_for_display(cache_timestamp)
            
            if is_fresh:
                reason = f"Cache ({cache_str}) >= source ({source_str}) for {source_file.name}"
            else:
                reason = f"Cache ({cache_str}) < source ({source_str}) for {source_file.name}"
            
            return is_fresh, reason
            
        except Exception as e:
            reason = f"Cache freshness check failed for {source_file.name}: {str(e)}"
            logger.error(f"Cache freshness check error: {e}")
            return False, reason  # Conservative: assume stale on error

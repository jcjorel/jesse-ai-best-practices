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
# Centralized handler-delegated path operations for Knowledge Bases Indexing System.
# Eliminates code duplication between file_analysis_cache and rebuild_decision_engine
# by providing unified handler path calculation with fail-fast behavior and no fallback logic.
###############################################################################
# [Source file design principles]
# - Fail-fast architecture with explicit errors instead of silent fallback logic
# - Single source of truth for all handler-delegated path operations
# - Clean separation between path calculation and error handling responsibilities
# - Consistent error reporting with structured exception types for different failure modes
# - Stateless operations enabling safe concurrent usage across multiple components
###############################################################################
# [Source file constraints]
# - NO fallback logic - all operations must succeed with correct handler or fail explicitly
# - Handler registry must be provided externally to prevent circular dependencies
# - All path operations must delegate to appropriate handlers without hardcoded assumptions
# - Error messages must be clear and actionable for debugging handler registry issues
# - Performance must be optimal with minimal filesystem operations and redundant checks
###############################################################################
# [Dependencies]
# <codebase>: ..handler_interface - HandlerRegistry for handler resolution and delegation
# <system>: pathlib - Cross-platform path operations and type safety
# <system>: logging - Structure error logging for debugging and monitoring
# <system>: typing - Type annotations for clear interface contracts
###############################################################################
# [GenAI tool change history]
# 2025-07-07T22:58:00Z : Initial creation of centralized handler path manager for DRY compliance by CodeAssistant
# * Created HandlerPathManager class eliminating duplicate handler delegation code from both files
# * Implemented fail-fast architecture with HandlerResolutionError for explicit error handling
# * Consolidated cache path, knowledge path, and reverse mapping operations into single component
# * Eliminated all fallback logic ensuring predictable behavior and easier debugging
###############################################################################

"""
Centralized Handler Path Manager for Knowledge Bases Indexing System.

This module provides unified handler-delegated path operations, eliminating code
duplication between file_analysis_cache.py and rebuild_decision_engine.py while
maintaining fail-fast behavior with no fallback logic.
"""

import logging
from pathlib import Path
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..handler_interface import HandlerRegistry

logger = logging.getLogger(__name__)


class HandlerResolutionError(Exception):
    """
    [Class intent]
    Specific exception for handler resolution failures in path operations.
    Provides clear error indication when handler registry cannot provide appropriate handler.

    [Design principles]
    Explicit error type enabling precise exception handling in calling code.
    Clear error messaging supporting debugging of handler registry configuration issues.
    Distinct from generic exceptions allowing targeted error recovery strategies.

    [Implementation details]
    Inherits from Exception providing standard exception interface.
    Used exclusively for handler resolution failures rather than path calculation errors.
    Enables calling code to distinguish between different types of path operation failures.
    """
    pass


class HandlerPathManager:
    """
    [Class intent]
    Centralized manager for all handler-delegated path operations in indexing system.
    Eliminates code duplication between file_analysis_cache and rebuild_decision_engine
    by providing unified handler path calculation with fail-fast behavior.

    [Design principles]
    Single source of truth for all handler-delegated path operations eliminating duplicate code.
    Fail-fast architecture with explicit errors instead of silent fallback logic for predictability.
    Clean delegation to HandlerRegistry avoiding hardcoded path assumptions or fallback paths.
    Stateless operations enabling safe concurrent usage across multiple indexing components.
    Structured error handling with specific exception types for different failure scenarios.

    [Implementation details]
    Requires HandlerRegistry injection to prevent circular dependencies and enable testing.
    All path operations delegate to appropriate handlers without any fallback logic.
    Raises HandlerResolutionError for handler resolution failures enabling targeted error handling.
    Provides both forward path calculation and reverse mapping operations for complete coverage.
    Maintains consistent error logging patterns for debugging and monitoring integration.
    """
    
    def __init__(self, handler_registry: 'HandlerRegistry'):
        """
        [Class method intent]
        Initializes handler path manager with required handler registry dependency.
        Sets up centralized path operations with fail-fast behavior and no fallback logic.

        [Design principles]
        Dependency injection pattern enabling testability and preventing circular dependencies.
        Fail-fast initialization ensuring handler registry is available for all operations.
        Clean initialization without complex setup or configuration requirements.

        [Implementation details]
        Stores handler registry reference for delegation to appropriate handlers.
        Validates handler registry is not None to prevent runtime errors.
        Sets up logging context for consistent error reporting across all operations.
        """
        if handler_registry is None:
            raise ValueError("HandlerRegistry is required - cannot be None")
        
        self.handler_registry = handler_registry
        logger.debug("Initialized HandlerPathManager with fail-fast handler delegation")
    
    def get_cache_path_strict(self, file_path: Path, source_root: Path) -> Path:
        """
        [Class method intent]
        Calculates cache file path using strict handler delegation with no fallback logic.
        Eliminates duplicate cache path calculation code from file_analysis_cache and rebuild_decision_engine.

        [Design principles]
        Fail-fast approach with explicit handler resolution and no silent fallback logic.
        Single source of truth for cache path calculation eliminating duplicate code patterns.
        Clean delegation to appropriate handler based on file path location and type.
        Explicit error handling enabling calling code to handle failures appropriately.

        [Implementation details]
        Uses handler registry to get appropriate handler for file's parent directory.
        Delegates cache path calculation to handler ensuring correct structure for content type.
        Raises HandlerResolutionError if no appropriate handler can be found.
        Returns Path object directly from handler without any modification or fallback logic.
        Provides consistent error logging for debugging handler resolution issues.
        """
        try:
            # Get appropriate handler for the file's parent directory
            handler = self.handler_registry.get_handler_for_path(file_path.parent)
            if handler is None:
                raise HandlerResolutionError(f"No handler found for file path: {file_path.parent}")
            
            # Delegate to handler - no fallback logic
            cache_path = handler.get_cache_path(file_path, source_root)
            logger.debug(f"Cache path calculated: {file_path.name} -> {cache_path}")
            return cache_path
            
        except HandlerResolutionError:
            # Re-raise handler resolution errors without modification
            raise
        except Exception as e:
            # Convert handler delegation errors to HandlerResolutionError for consistency
            error_msg = f"Cache path calculation failed for {file_path.name}: {str(e)}"
            logger.error(error_msg)
            raise HandlerResolutionError(error_msg) from e
    
    def get_knowledge_path_strict(self, directory_path: Path, source_root: Path) -> Path:
        """
        [Class method intent]
        Calculates knowledge file path using strict handler delegation with no fallback logic.
        Eliminates duplicate knowledge path calculation code from rebuild_decision_engine methods.

        [Design principles]
        Fail-fast approach with explicit handler resolution and no silent fallback logic.
        Single source of truth for knowledge path calculation eliminating duplicate code patterns.
        Clean delegation to appropriate handler based on directory path location and type.
        Explicit error handling enabling calling code to handle failures appropriately.

        [Implementation details]
        Uses handler registry to get appropriate handler for directory path.
        Delegates knowledge path calculation to handler ensuring correct structure for content type.
        Raises HandlerResolutionError if no appropriate handler can be found.
        Returns Path object directly from handler without any modification or fallback logic.
        Provides consistent error logging for debugging handler resolution issues.
        """
        try:
            # Get appropriate handler for the directory
            handler = self.handler_registry.get_handler_for_path(directory_path)
            if handler is None:
                raise HandlerResolutionError(f"No handler found for directory path: {directory_path}")
            
            # Delegate to handler - no fallback logic
            knowledge_path = handler.get_knowledge_path(directory_path, source_root)
            logger.debug(f"Knowledge path calculated: {directory_path.name} -> {knowledge_path}")
            return knowledge_path
            
        except HandlerResolutionError:
            # Re-raise handler resolution errors without modification
            raise
        except Exception as e:
            # Convert handler delegation errors to HandlerResolutionError for consistency
            error_msg = f"Knowledge path calculation failed for {directory_path.name}: {str(e)}"
            logger.error(error_msg)
            raise HandlerResolutionError(error_msg) from e
    
    def map_cache_to_source_strict(self, cache_file: Path, source_root: Path) -> Optional[Path]:
        """
        [Class method intent]
        Maps cache file back to corresponding source file using strict handler delegation.
        Eliminates duplicate reverse mapping code from rebuild_decision_engine methods.

        [Design principles]
        Fail-fast approach attempting handler-based reverse mapping with no fallback logic.
        Single source of truth for cache-to-source mapping eliminating duplicate code patterns.
        Explicit None return for unmappable files rather than fallback path construction.
        Clean error handling distinguishing between mapping failures and handler resolution failures.

        [Implementation details]
        Attempts reverse mapping using all registered handlers to find appropriate match.
        Returns first successful mapping result from handler-specific reverse mapping logic.
        Returns None if no handler can successfully map the cache file to source path.
        Raises HandlerResolutionError only for handler registry access failures, not mapping failures.
        Provides detailed logging for debugging reverse mapping operations and handler behavior.
        """
        try:
            # Try all handlers to find one that can perform reverse mapping
            for handler in self.handler_registry.get_all_handlers():
                try:
                    source_path = handler.map_cache_to_source(cache_file, source_root)
                    if source_path is not None:
                        logger.debug(f"Cache mapped to source: {cache_file.name} -> {source_path}")
                        return source_path
                except Exception as e:
                    # Log individual handler failures but continue trying other handlers
                    logger.debug(f"Handler {handler.get_handler_type()} failed to map cache {cache_file.name}: {e}")
                    continue
            
            # No handler could map the cache file
            logger.debug(f"No handler could map cache file to source: {cache_file.name}")
            return None
            
        except Exception as e:
            # Handler registry access failure
            error_msg = f"Handler registry access failed during cache mapping for {cache_file.name}: {str(e)}"
            logger.error(error_msg)
            raise HandlerResolutionError(error_msg) from e
    
    def map_knowledge_to_source_strict(self, knowledge_dir: Path, source_root: Path) -> Optional[Path]:
        """
        [Class method intent]
        Maps knowledge directory back to corresponding source directory using strict handler delegation.
        Eliminates duplicate reverse mapping code from rebuild_decision_engine methods.

        [Design principles]
        Fail-fast approach attempting handler-based reverse mapping with no fallback logic.
        Single source of truth for knowledge-to-source mapping eliminating duplicate code patterns.
        Explicit None return for unmappable directories rather than fallback path construction.
        Clean error handling distinguishing between mapping failures and handler resolution failures.

        [Implementation details]
        Attempts reverse mapping using all registered handlers to find appropriate match.
        Returns first successful mapping result from handler-specific reverse mapping logic.
        Returns None if no handler can successfully map the knowledge directory to source path.
        Raises HandlerResolutionError only for handler registry access failures, not mapping failures.
        Provides detailed logging for debugging reverse mapping operations and handler behavior.
        """
        try:
            # Try all handlers to find one that can perform reverse mapping
            for handler in self.handler_registry.get_all_handlers():
                try:
                    source_path = handler.map_knowledge_to_source(knowledge_dir, source_root)
                    if source_path is not None:
                        logger.debug(f"Knowledge mapped to source: {knowledge_dir.name} -> {source_path}")
                        return source_path
                except Exception as e:
                    # Log individual handler failures but continue trying other handlers
                    logger.debug(f"Handler {handler.get_handler_type()} failed to map knowledge {knowledge_dir.name}: {e}")
                    continue
            
            # No handler could map the knowledge directory
            logger.debug(f"No handler could map knowledge directory to source: {knowledge_dir.name}")
            return None
            
        except Exception as e:
            # Handler registry access failure
            error_msg = f"Handler registry access failed during knowledge mapping for {knowledge_dir.name}: {str(e)}"
            logger.error(error_msg)
            raise HandlerResolutionError(error_msg) from e

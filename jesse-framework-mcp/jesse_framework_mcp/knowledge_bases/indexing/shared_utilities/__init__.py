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
# Shared utilities package initialization for Knowledge Bases Indexing System.
# Provides centralized imports for all shared utility components eliminating
# code duplication between file_analysis_cache and rebuild_decision_engine.
###############################################################################
# [Source file design principles]
# - Centralized import structure providing clear access to shared utilities
# - DRY compliance ensuring single sources of truth for common operations
# - Fail-fast architecture with no fallback logic for predictable behavior
# - Clean separation of concerns with focused utility modules
# - Explicit error handling with no silent failures or degraded modes
###############################################################################
# [Source file constraints]
# - All utility modules must follow fail-fast principles with no fallback logic
# - Shared utilities must be stateless and side-effect free where possible
# - Error handling must be explicit and consistent across all utility modules
# - Dependencies between utility modules must be minimized to prevent circular imports
# - All utility functions must be thoroughly tested before deployment
###############################################################################
# [Dependencies]
# <codebase>: .handler_path_manager - Centralized handler-delegated path operations
# <codebase>: .timestamp_manager - Unified timestamp operations and comparisons
# <codebase>: .error_handler - Standardized error handling for indexing operations
###############################################################################
# [GenAI tool change history]
# 2025-07-07T22:57:00Z : Initial creation of shared utilities package for DRY compliance by CodeAssistant
# * Created shared utilities package to eliminate code duplication between file_analysis_cache and rebuild_decision_engine
# * Established fail-fast architecture principles with explicit error handling and no fallback logic
# * Designed clean import structure for centralized access to common operations
# * Set up foundation for handler path management, timestamp operations, and error handling utilities
###############################################################################

"""
Shared Utilities Package for Knowledge Bases Indexing System.

This package provides centralized utility components to eliminate code duplication
between file_analysis_cache.py and rebuild_decision_engine.py while maintaining
fail-fast behavior and explicit error handling.
"""

from .handler_path_manager import HandlerPathManager, HandlerResolutionError
from .timestamp_manager import TimestampManager
from .error_handler import IndexingErrorHandler

__all__ = [
    'HandlerPathManager',
    'HandlerResolutionError',
    'TimestampManager', 
    'IndexingErrorHandler'
]

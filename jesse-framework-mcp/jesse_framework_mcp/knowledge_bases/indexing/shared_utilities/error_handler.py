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
# Standardized error handling utilities for Knowledge Bases Indexing System.
# Eliminates duplicate error handling patterns between file_analysis_cache and rebuild_decision_engine
# by providing unified error logging, categorization, and recovery strategies.
###############################################################################
# [Source file design principles]
# - Consistent error handling behavior eliminating scattered duplicate error patterns
# - Structured error categorization enabling appropriate recovery strategies for different failure types
# - Unified error logging with consistent formatting and context information across components
# - Clear error messaging supporting debugging and troubleshooting of indexing operations
# - Stateless utility functions enabling safe concurrent usage across multiple components
###############################################################################
# [Source file constraints]
# - All error handling must be stateless and side-effect free for safe concurrent usage
# - Error messages must be clear and actionable for debugging and troubleshooting purposes
# - Error categorization must be consistent across all indexing components and operations
# - Logging patterns must be unified and structured for monitoring and analysis integration
# - Recovery strategies must be predictable and consistent across all failure scenarios
###############################################################################
# [Dependencies]
# <system>: logging - Structured error logging for debugging and monitoring
# <system>: pathlib - Cross-platform path operations for error context
# <system>: typing - Type annotations for clear interface contracts and safety
###############################################################################
# [GenAI tool change history]
# 2025-07-07T23:00:00Z : Initial creation of standardized error handler for DRY compliance by CodeAssistant
# * Created IndexingErrorHandler class eliminating duplicate error handling patterns from both files
# * Implemented consistent error logging and categorization across all indexing operations
# * Established unified error messaging and recovery strategy patterns
# * Provided structured error handling utilities for filesystem and handler operation failures
###############################################################################

"""
Standardized Error Handler for Knowledge Bases Indexing System.

This module provides unified error handling utilities, eliminating duplicate error
handling patterns between file_analysis_cache.py and rebuild_decision_engine.py
while maintaining consistent error logging and recovery strategies.
"""

import logging
from pathlib import Path
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


class IndexingErrorHandler:
    """
    [Class intent]
    Centralized error handler for all indexing system operations.
    Eliminates duplicate error handling patterns between file_analysis_cache and rebuild_decision_engine
    by providing unified error logging, categorization, and recovery strategies.

    [Design principles]
    Stateless utility class with static methods enabling safe concurrent usage across components.
    Consistent error handling behavior eliminating scattered duplicate error patterns throughout system.
    Structured error categorization enabling appropriate recovery strategies for different failure types.
    Unified error logging with consistent formatting and context information across all operations.
    Clear error messaging supporting debugging and troubleshooting of complex indexing operations.

    [Implementation details]
    All methods are static eliminating need for instance creation and enabling simple imports.
    Provides categorized error handling for filesystem, handler, and general indexing operations.
    Uses structured logging with consistent context information for debugging and monitoring.
    Returns standardized error information enabling consistent recovery strategies across components.
    Maintains clear separation between different error types and their appropriate handling approaches.
    """
    
    @staticmethod
    def handle_filesystem_error(operation: str, path: Path, error: Exception, 
                              context: str = "") -> Tuple[bool, str]:
        """
        [Class method intent]
        Handles filesystem operation errors with consistent logging and recovery information.
        Eliminates duplicate filesystem error handling patterns from both files.

        [Design principles]
        Unified filesystem error handling eliminating scattered duplicate error patterns.
        Consistent error logging with structured context information for debugging operations.
        Clear recovery information enabling calling code to handle failures appropriately.
        Categorized error handling distinguishing between different filesystem failure types.

        [Implementation details]
        Categorizes filesystem errors by type for appropriate recovery strategy determination.
        Provides structured error logging with operation context and path information.
        Returns boolean success/failure status with detailed error message for recovery decisions.
        Handles common filesystem errors like permission issues and missing files gracefully.
        """
        try:
            error_type = type(error).__name__
            path_info = f" for {path.name}" if path else ""
            context_info = f" ({context})" if context else ""
            
            error_message = f"{operation} failed{path_info}{context_info}: {str(error)}"
            
            # Categorize filesystem errors for appropriate handling
            if isinstance(error, (FileNotFoundError, OSError)):
                logger.warning(f"Filesystem access error: {error_message}")
                return False, f"Filesystem access failed: {str(error)}"
            elif isinstance(error, PermissionError):
                logger.error(f"Permission error: {error_message}")
                return False, f"Permission denied: {str(error)}"
            else:
                logger.error(f"Unexpected filesystem error ({error_type}): {error_message}")
                return False, f"Unexpected filesystem error: {str(error)}"
                
        except Exception as logging_error:
            # Fallback error handling if logging itself fails
            fallback_message = f"{operation} failed with error logging failure: {str(logging_error)}"
            return False, fallback_message
    
    @staticmethod
    def handle_handler_error(operation: str, handler_type: str, error: Exception,
                           context: str = "") -> Tuple[bool, str]:
        """
        [Class method intent]
        Handles handler operation errors with consistent logging and recovery information.
        Eliminates duplicate handler error handling patterns from both files.

        [Design principles]
        Unified handler error handling eliminating scattered duplicate error patterns.
        Handler-specific error context enabling targeted debugging of handler registry issues.
        Consistent error logging with structured handler information for troubleshooting operations.
        Clear recovery information enabling calling code to handle handler failures appropriately.

        [Implementation details]
        Provides handler-specific error context for debugging handler registry configuration issues.
        Uses structured error logging with handler type and operation context information.
        Returns boolean success/failure status with detailed error message for recovery decisions.
        Handles different handler error types with appropriate categorization and recovery strategies.
        """
        try:
            error_type = type(error).__name__
            context_info = f" ({context})" if context else ""
            
            error_message = f"{operation} failed for handler '{handler_type}'{context_info}: {str(error)}"
            
            # Log handler errors with appropriate severity
            if "resolution" in operation.lower() or "registry" in operation.lower():
                logger.error(f"Handler registry error: {error_message}")
                return False, f"Handler resolution failed: {str(error)}"
            else:
                logger.warning(f"Handler operation error ({error_type}): {error_message}")
                return False, f"Handler operation failed: {str(error)}"
                
        except Exception as logging_error:
            # Fallback error handling if logging itself fails
            fallback_message = f"{operation} failed for handler '{handler_type}' with logging failure: {str(logging_error)}"
            return False, fallback_message
    
    @staticmethod
    def log_indexing_error(component: str, operation: str, path: Optional[Path], 
                          error: Exception, recovery_action: str = ""):
        """
        [Class method intent]
        Provides standardized error logging for indexing operations with consistent patterns.
        Eliminates duplicate error logging patterns from both files.

        [Design principles]
        Unified error logging ensuring consistent error reporting across all indexing components.
        Structured context information enabling effective debugging and troubleshooting of issues.
        Component-specific error tracking supporting monitoring and analysis of indexing operations.
        Clear recovery action logging enabling audit trails of error handling decisions.

        [Implementation details]
        Uses structured logging with consistent component, operation, and path context information.
        Provides optional recovery action logging for audit trails of error handling decisions.
        Handles missing path information gracefully for operations not tied to specific files.
        Uses appropriate logging severity based on error context and recovery possibilities.
        """
        try:
            error_type = type(error).__name__
            path_info = f" for {path.name}" if path else ""
            recovery_info = f" - {recovery_action}" if recovery_action else ""
            
            log_message = f"{component}: {operation} failed{path_info} ({error_type}): {str(error)}{recovery_info}"
            
            # Use appropriate logging level based on recovery possibilities
            if recovery_action and "retry" in recovery_action.lower():
                logger.warning(log_message)
            elif recovery_action:
                logger.info(log_message)
            else:
                logger.error(log_message)
                
        except Exception as logging_error:
            # Fallback logging if structured logging fails
            logger.error(f"Error logging failed for {component}: {str(logging_error)}")
    
    @staticmethod
    def create_error_summary(component: str, operation: str, path: Optional[Path], 
                           error: Exception) -> str:
        """
        [Class method intent]
        Creates standardized error summary messages for consistent error reporting.
        Eliminates duplicate error message formatting patterns from both files.

        [Design principles]
        Unified error message formatting ensuring consistent error reporting across all components.
        Structured error information enabling clear understanding of failure context and details.
        Component and operation context supporting targeted debugging and troubleshooting efforts.
        Clear error summary format suitable for both logging and user-facing error messages.

        [Implementation details]
        Creates structured error summary with component, operation, and path context information.
        Handles missing path information gracefully for operations not tied to specific files.
        Provides consistent error message format across all indexing components and operations.
        Returns string suitable for both logging and user-facing error message display.
        """
        try:
            error_type = type(error).__name__
            path_info = f" for {path.name}" if path else ""
            
            return f"{component} {operation} failed{path_info} ({error_type}): {str(error)}"
            
        except Exception:
            # Fallback error summary if formatting fails  
            return f"{component} {operation} failed with error summary generation failure"

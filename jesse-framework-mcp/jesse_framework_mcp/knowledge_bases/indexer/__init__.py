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
# Public API exports for the new clean knowledge bases indexer.
# Provides clean interface for external usage while hiding internal complexity.
# Main entry point for users of the indexer system.
###############################################################################
# [Source file design principles]
# - Export only public APIs to maintain clean interface
# - Hide internal implementation details
# - Enable simple import patterns for users
# - Maintain backward compatibility when possible
###############################################################################
# [Source file constraints]
# - Must export all public interfaces required by users
# - Cannot break existing usage patterns
# - Must maintain clean separation between public and private APIs
###############################################################################
# [Dependencies]
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.core (when implemented)
###############################################################################
# [GenAI tool change history]
# 2025-07-09T13:27:00Z : Initial package initialization by CodeAssistant
# * Created public API exports for models module
# * Reserved imports for future core components
# * Established clean public interface pattern
###############################################################################

# Core data models and interfaces
from .models import (
    # Type definitions
    ProgressCallback,
    UpdateStatus,
    TaskStatus,
    
    # Tree-based data classes
    BaseIndexedFile,
    AnalysisFile,
    KnowledgeBaseFile,
    KnowledgeDirectory,
    KnowledgeTree,
    
    # Other data classes
    ValidationResult,
    ExecutionContext,
    TaskResult,
    ExecutionPlan,
    IndexingResult,
    
    # Abstract interfaces
    AtomicTask,
    
    # Type aliases
    TaskRegistry,
    TaskDependencyGraph,
    FileCollection,
)

# Main indexer components
from .core import CoreIndexer, index_project, validate_indexer_setup
from .discovery import DiscoveryEngine
from .planning import GenericPlanGenerator, TaskRegistry
from .execution import GenericExecutor
from .handlers import ProjectHandler, GitCloneHandler
from .knowledge import AnalyzeFileTask, BuildKnowledgeBaseTask, CleanupTask

# Public API
__all__ = [
    # Type definitions
    "ProgressCallback",
    "UpdateStatus",
    "TaskStatus",
    
    # Tree-based data classes
    "BaseIndexedFile",
    "AnalysisFile",
    "KnowledgeBaseFile",
    "KnowledgeDirectory",
    "KnowledgeTree",
    
    # Other data classes
    "ValidationResult",
    "ExecutionContext",
    "TaskResult",
    "ExecutionPlan",
    "IndexingResult",
    
    # Abstract interfaces
    "AtomicTask",
    
    # Type aliases
    "TaskRegistry",
    "TaskDependencyGraph",
    "FileCollection",
    
    # Main components
    "CoreIndexer",
    "DiscoveryEngine", 
    "GenericPlanGenerator",
    "GenericExecutor",
    "TaskRegistry",
    
    # Handlers
    "ProjectHandler",
    "GitCloneHandler",
    
    # Task implementations
    "AnalyzeFileTask",
    "BuildKnowledgeBaseTask", 
    "CleanupTask",
    
    # Convenience functions
    "index_project",
    "validate_indexer_setup",
]

# Version information
__version__ = "1.0.0"
__author__ = "JESSE Framework Development Team"
__description__ = "Clean knowledge bases indexer with two-subphase discovery and generic task execution"

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
# Models package initialization for Knowledge Bases Hierarchical Indexing System.
# Exports all data models, configuration classes, and context structures used
# throughout the hierarchical indexing workflow and FastMCP integration.
###############################################################################
# [Source file design principles]
# - Centralized model exports for clean dependency management
# - Type-safe data structures with comprehensive validation
# - Immutable configurations where possible for thread safety
# - Clear separation between configuration and runtime context models
###############################################################################
# [Source file constraints]
# - All models must be dataclasses or Pydantic models for serialization
# - Configuration validation must happen at initialization time
# - Runtime context models must support async operations
# - Model imports must not create circular dependencies
###############################################################################
# [Dependencies]
# <codebase>: .indexing_config - Configuration data models
# <codebase>: .knowledge_context - Runtime context data models
###############################################################################
# [GenAI tool change history]
# 2025-07-01T12:03:00Z : Initial models package creation by CodeAssistant
# * Set up models package structure
# * Established export pattern for data models
# * Created foundation for configuration and context models
###############################################################################

"""
Data Models for Knowledge Bases Hierarchical Indexing System

This package contains all data models used throughout the knowledge indexing
system, including configuration, runtime context, and processing state models.
"""

from .indexing_config import IndexingConfig, IndexingMode
from .knowledge_context import (
    DirectoryContext,
    FileContext,
    ChangeInfo,
    IndexingStatus,
    ProcessingStats,
    ProcessingStatus,
    ChangeType
)
from .rebuild_decisions import (
    DecisionReport,
    RebuildDecision,
    DeletionDecision,
    DecisionOutcome,
    DecisionReason
)
from .execution_plan import (
    ExecutionPlan,
    AtomicTask,
    TaskType,
    ExecutionResults
)

__all__ = [
    "IndexingConfig",
    "IndexingMode",
    "DirectoryContext", 
    "FileContext",
    "ChangeInfo",
    "IndexingStatus",
    "ProcessingStats",
    "ProcessingStatus",
    "ChangeType",
    "DecisionReport",
    "RebuildDecision",
    "DeletionDecision",
    "DecisionOutcome",
    "DecisionReason",
    "ExecutionPlan",
    "AtomicTask",
    "TaskType",
    "ExecutionResults"
]

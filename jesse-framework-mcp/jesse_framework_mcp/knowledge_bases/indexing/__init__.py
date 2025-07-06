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
# Indexing package initialization for Knowledge Bases Hierarchical Indexing System.
# Exports core indexing components, orchestrators, and processing utilities for
# hierarchical knowledge base maintenance and automated content summarization.
###############################################################################
# [Source file design principles]
# - Centralized component exports enabling clean dependency management
# - Clear separation between orchestration, detection, and building components
# - Async-first architecture supporting concurrent processing operations
# - Bottom-up hierarchical processing without parent-to-child context dependencies
###############################################################################
# [Source file constraints]
# - All exported components must follow JESSE_CODE_COMMENTS.md standards
# - Indexing components must integrate with strands_agent_driver for LLM operations
# - Component imports must not create circular dependencies
# - All operations must be async and use FastMCP Context patterns
###############################################################################
# [Dependencies]
# <codebase>: .hierarchical_indexer - Core indexing orchestrator
# <codebase>: .knowledge_builder - LLM-powered content summarization
# <codebase>: .special_handlers - Git-clone and project-base special handling
###############################################################################
# [GenAI tool change history]
# 2025-07-01T12:07:00Z : Initial indexing package creation by CodeAssistant
# * Set up indexing package structure
# * Established component export pattern
# * Created foundation for hierarchical indexing workflow
###############################################################################

"""
Indexing subsystem for Knowledge Bases Hierarchical Indexing System.

This package contains the core components for hierarchical knowledge base indexing,
including the main orchestrator, content building, and special handling for 
git-clones and project-base scenarios.
"""

from .hierarchical_indexer import HierarchicalIndexer
from .knowledge_builder import KnowledgeBuilder
from .special_handlers import GitCloneHandler, ProjectBaseHandler

__all__ = [
    "HierarchicalIndexer",
    "KnowledgeBuilder",
    "GitCloneHandler",
    "ProjectBaseHandler"
]

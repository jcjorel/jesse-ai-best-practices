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
# Package initialization for the JESSE Framework Knowledge Bases Hierarchical Indexing System.
# Provides FastMCP tool and resource registration for automated knowledge base maintenance
# throughout the .knowledge/ directory hierarchy using leaf-first processing strategy.
###############################################################################
# [Source file design principles]
# - FastMCP-first architecture with tool and resource registration
# - Hierarchical Semantic Context pattern implementation
# - Bottom-up assembly with no parent-to-child context flow
# - Defensive programming with comprehensive error handling
# - Async-first design following JESSE Framework standards
###############################################################################
# [Source file constraints]
# - Must register all FastMCP tools and resources at package import
# - Tool registration must follow JESSE_CODE_COMMENTS.md three-section pattern
# - All operations must be async and use FastMCP Context
# - Integration with existing strands_agent_driver for LLM operations
###############################################################################
# [Dependencies]
# <codebase>: jesse_framework_mcp.main - MCP server registration
# <codebase>: jesse_framework_mcp.llm.strands_agent_driver - LLM integration
# <system>: fastmcp - MCP framework integration
# <system>: pathlib - Cross-platform file operations
###############################################################################
# [GenAI tool change history]
# 2025-07-01T12:03:00Z : Initial package creation with FastMCP tool registration by CodeAssistant
# * Created knowledge-bases package structure
# * Set up tool and resource registration architecture
# * Established async-first design patterns
###############################################################################

"""
Knowledge Bases Hierarchical Indexing System

This package implements the Hierarchical Semantic Context pattern for automated
maintenance of structured knowledge files throughout the JESSE Framework's
.knowledge/ directory hierarchy.

Key Features:
- Leaf-first hierarchical processing
- FastMCP tool integration
- Strands Agent Driver LLM integration
- Change detection and incremental updates
- Special handling for git-clones and project-base
"""

from .tools import register_knowledge_bases_tools
from .resources import register_knowledge_bases_resources
from .indexing import HierarchicalIndexer
from .models import IndexingConfig, IndexingMode

__all__ = [
    "register_knowledge_bases_tools",
    "register_knowledge_bases_resources",
    "HierarchicalIndexer",
    "IndexingConfig",
    "IndexingMode"
]

__version__ = "1.0.0"

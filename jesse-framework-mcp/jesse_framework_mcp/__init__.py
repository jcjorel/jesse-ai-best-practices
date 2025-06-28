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
# Package initialization for JESSE Framework MCP Server, providing entry point
# and version information for the complete self-contained JESSE framework.
###############################################################################
# [Source file design principles]
# - Simple package initialization with clear version and entry point exports
# - Follows Python packaging standards for MCP server distribution
# - Provides async main entry point for FastMCP stdio transport
###############################################################################
# [Source file constraints]
# - Must maintain compatibility with Python 3.8+ for broad support
# - Entry point must be compatible with MCP stdio transport protocol
# - Package structure must support build-time embedded content
###############################################################################
# [Dependencies]
# codebase:main.py - Main FastMCP server implementation
# system:asyncio - Async event loop for MCP protocol
###############################################################################
# [GenAI tool change history]
# 2025-06-27T17:29:00Z : Fixed async main entry point wrapper for console script by CodeAssistant
# * Added synchronous main() wrapper that calls asyncio.run(async_main())
# * Fixed console script execution issue with coroutine not being awaited
# 2025-06-27T01:23:00Z : Initial package initialization by CodeAssistant
# * Created package __init__.py with version and entry point
# * Set up async main entry point for MCP server
###############################################################################

"""
JESSE Framework MCP Server

A Model Context Protocol (MCP) server that provides complete JESSE AI Framework
initialization including rules, workflows, and project knowledge management.

The server embeds all JESSE framework content at build time and provides:
- jesse_start_session: Complete framework initialization
- jesse_load_knowledge_base: Lazy loading of specific knowledge bases

Usage:
    Run as MCP server over stdio transport:
    $ jesse-framework-mcp

    Or programmatically:
    >>> import asyncio
    >>> from jesse_framework_mcp import main
    >>> asyncio.run(main())
"""

__version__ = "0.1.0"
__author__ = "JESSE Framework"
__email__ = "contact@jesse-framework.dev"

# Export main entry point for console script
from .main import main

__all__ = ["main", "__version__"]

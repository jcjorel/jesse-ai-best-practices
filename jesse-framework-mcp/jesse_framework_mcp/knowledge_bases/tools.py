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
# FastMCP tools integration for Knowledge Bases Hierarchical Indexing System.
# Provides MCP tool interface for manual indexing triggers, search capabilities,
# and system management through standardized FastMCP tool registration patterns.
###############################################################################
# [Source file design principles]
# - FastMCP tool integration following JESSE_CODE_COMMENTS.md three-section pattern
# - Comprehensive error handling with detailed progress reporting through FastMCP Context
# - Async-first architecture supporting concurrent operations and real-time feedback
# - Integration with core HierarchicalIndexer for consistent processing workflows
# - HTTP-formatted responses using existing http_formatter patterns for consistency
###############################################################################
# [Source file constraints]
# - All tools must follow JESSE_CODE_COMMENTS.md three-section documentation pattern
# - Tools must use FastMCP Context for progress reporting and user feedback
# - Error handling must provide detailed information for debugging and user guidance
# - Tool responses must use HTTP formatting for consistency with JESSE Framework patterns
# - Integration with HierarchicalIndexer must respect configuration and processing constraints
###############################################################################
# [Dependencies]
# <codebase>: .indexing.hierarchical_indexer - Core indexing orchestrator
# <codebase>: .models.indexing_config - Configuration and processing parameters
# <codebase>: ..helpers.http_formatter - HTTP response formatting for consistency
# <system>: fastmcp - MCP server framework and Context integration
# <system>: pathlib - Cross-platform path operations for tool parameters
# <system>: asyncio - Async programming patterns for tool execution
###############################################################################
# [GenAI tool change history]
# 2025-07-01T12:17:00Z : Initial FastMCP tools creation by CodeAssistant
# * Created knowledge bases indexing tools with comprehensive MCP integration
# * Implemented manual indexing trigger and status monitoring capabilities
# * Set up HTTP-formatted responses following JESSE Framework patterns
###############################################################################

"""
FastMCP Tools for Knowledge Bases Hierarchical Indexing System.

This module provides MCP tool interfaces for manual indexing operations,
system status monitoring, and search capabilities through standardized
FastMCP tool registration and execution patterns.
"""

import asyncio
import logging
from pathlib import Path
from typing import Optional, Dict, Any

from fastmcp import Context
from fastmcp.server import FastMCP

from .indexing import HierarchicalIndexer
from .models import IndexingConfig, IndexingMode
from ..helpers.async_http_formatter import format_http_response

logger = logging.getLogger(__name__)

# Global indexer instance for tool coordination
_current_indexer: Optional[HierarchicalIndexer] = None


def register_knowledge_bases_tools(server: FastMCP) -> None:
    """
    [Function intent]
    Registers all knowledge bases tools with the FastMCP server for MCP integration.
    Provides comprehensive tool registration enabling manual indexing operations
    and system management through standardized MCP tool interfaces.

    [Design principles]
    Centralized tool registration enabling clean MCP server integration.
    Comprehensive tool coverage supporting manual operations and system monitoring.
    JESSE Framework standards compliance with three-section documentation pattern.

    [Implementation details]
    Registers manual indexing trigger tool for user-initiated processing operations.
    Sets up status monitoring tool for real-time indexing operation tracking.
    Provides search capability tool for future knowledge base query functionality.
    """
    
    @server.tool("knowledge_bases_index_trigger", 
                description="Manually trigger knowledge base indexing for specified path or entire hierarchy with configurable options")
    async def knowledge_bases_index_trigger(
        ctx: Context,
        target_path: str = ".knowledge",
        indexing_mode: str = "incremental",
        enable_git_clone_indexing: bool = True,
        enable_project_base_indexing: bool = False
    ) -> str:
        """
        [Tool intent]
        Manually triggers knowledge base indexing for specified directory path with
        configurable processing options. Enables user-initiated indexing operations
        with customizable scope and processing behavior for targeted knowledge updates.

        [Design principles]
        User-controlled indexing operations supporting manual knowledge base maintenance.
        Configurable processing options enabling targeted indexing strategies.
        Comprehensive progress reporting through FastMCP Context for real-time feedback.
        Error handling providing detailed information for troubleshooting and user guidance.

        [Implementation details]
        Creates IndexingConfig based on provided parameters and system defaults.
        Initializes HierarchicalIndexer with configuration for processing coordination.
        Executes indexing operation with progress reporting through FastMCP Context.
        Returns HTTP-formatted response with operation results and status information.
        """
        global _current_indexer
        
        try:
            await ctx.info(f"Starting manual knowledge base indexing for: {target_path}")
            
            # Validate indexing mode
            try:
                mode = IndexingMode(indexing_mode)
            except ValueError:
                return format_http_response(
                    400, "Bad Request",
                    {"error": f"Invalid indexing mode: {indexing_mode}. Valid modes: full, full_kb_rebuild, incremental"}
                )
            
            # Check if indexing is already in progress
            if _current_indexer and _current_indexer.current_status.is_processing:
                return format_http_response(
                    409, "Conflict",
                    {"error": "Knowledge base indexing already in progress. Please wait for completion."}
                )
            
            # Resolve target path
            target_directory = Path(target_path).resolve()
            if not target_directory.exists():
                return format_http_response(
                    404, "Not Found",
                    {"error": f"Target directory does not exist: {target_directory}"}
                )
            
            if not target_directory.is_dir():
                return format_http_response(
                    400, "Bad Request",
                    {"error": f"Target path is not a directory: {target_directory}"}
                )
            
            # Create indexing configuration
            config = IndexingConfig(
                indexing_mode=mode,
                enable_git_clone_indexing=enable_git_clone_indexing,
                enable_project_base_indexing=enable_project_base_indexing
            )
            
            # Initialize and execute indexing
            _current_indexer = HierarchicalIndexer(config)
            indexing_status = await _current_indexer.index_hierarchy(target_directory, ctx)
            
            # Prepare response data
            response_data = {
                "status": "completed",
                "target_path": str(target_directory),
                "indexing_mode": indexing_mode,
                "statistics": indexing_status.processing_stats.to_dict(),
                "completion_percentage": indexing_status.completion_percentage,
                "operation_summary": {
                    "total_files_discovered": indexing_status.processing_stats.total_files_discovered,
                    "files_completed": indexing_status.processing_stats.files_completed,
                    "files_failed": indexing_status.processing_stats.files_failed,
                    "processing_duration": indexing_status.processing_stats.processing_duration
                }
            }
            
            if indexing_status.processing_stats.errors:
                response_data["errors"] = indexing_status.processing_stats.errors[:10]  # Limit error list
            
            await ctx.info("Knowledge base indexing completed successfully")
            
            return format_http_response(
                200, "OK",
                response_data,
                content_type="application/json"
            )
            
        except Exception as e:
            logger.error(f"Knowledge base indexing failed: {e}", exc_info=True)
            await ctx.error(f"Indexing operation failed: {str(e)}")
            
            return format_http_response(
                500, "Internal Server Error",
                {
                    "error": "Knowledge base indexing failed",
                    "details": str(e),
                    "target_path": target_path
                }
            )
    
    @server.tool("knowledge_bases_status",
                description="Get current status and statistics for knowledge base indexing operations")
    async def knowledge_bases_status(ctx: Context) -> str:
        """
        [Tool intent]
        Retrieves current status and comprehensive statistics for knowledge base indexing
        operations. Provides real-time monitoring capabilities for ongoing processing
        and historical information for completed operations.

        [Design principles]
        Real-time status monitoring enabling user feedback and operation coordination.
        Comprehensive statistics reporting supporting performance analysis and troubleshooting.
        HTTP-formatted responses maintaining consistency with JESSE Framework patterns.

        [Implementation details]
        Accesses global indexer instance for current operation status retrieval.
        Provides detailed processing statistics including progress and performance metrics.
        Returns HTTP-formatted response with comprehensive status and statistics information.
        """
        try:
            if not _current_indexer:
                return format_http_response(
                    200, "OK",
                    {
                        "status": "no_indexing_operations",
                        "message": "No knowledge base indexing operations have been initiated"
                    }
                )
            
            current_status = _current_indexer.current_status
            status_data = current_status.to_dict()
            
            # Add additional context information
            status_data["indexer_initialized"] = True
            status_data["last_updated"] = "real-time"
            
            await ctx.info("Retrieved knowledge base indexing status")
            
            return format_http_response(
                200, "OK",
                status_data,
                content_type="application/json"
            )
            
        except Exception as e:
            logger.error(f"Status retrieval failed: {e}", exc_info=True)
            await ctx.error(f"Status retrieval failed: {str(e)}")
            
            return format_http_response(
                500, "Internal Server Error",
                {
                    "error": "Failed to retrieve indexing status",
                    "details": str(e)
                }
            )
    
    @server.tool("knowledge_bases_search",
                description="Search across indexed knowledge bases using hierarchical context with natural language queries")
    async def knowledge_bases_search(
        ctx: Context,
        query: str,
        search_scope: str = "all",
        max_results: int = 10
    ) -> str:
        """
        [Tool intent]
        Searches across indexed knowledge bases using natural language queries with
        hierarchical context awareness. Provides comprehensive search capabilities
        for knowledge discovery and content retrieval across the knowledge base hierarchy.

        [Design principles]
        Natural language query processing enabling intuitive knowledge discovery.
        Hierarchical context awareness providing comprehensive search coverage.
        Configurable search scope supporting targeted and comprehensive search strategies.
        Future implementation placeholder maintaining tool interface consistency.

        [Implementation details]
        Placeholder implementation for future search functionality development.
        Returns HTTP-formatted response indicating future feature availability.
        Maintains tool interface consistency for seamless future integration.
        """
        await ctx.info(f"Knowledge base search requested: {query}")
        
        # Placeholder for future search implementation
        return format_http_response(
            501, "Not Implemented",
            {
                "message": "Knowledge base search functionality is planned for future implementation",
                "query": query,
                "search_scope": search_scope,
                "max_results": max_results,
                "status": "feature_planned"
            }
        )

    logger.info("Knowledge Bases tools registered successfully")

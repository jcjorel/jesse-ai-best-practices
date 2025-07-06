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
# FastMCP resources integration for Knowledge Bases Hierarchical Indexing System.
# Provides MCP resource interface for accessing knowledge base configuration,
# processing templates, and system documentation through standardized resource patterns.
###############################################################################
# [Source file design principles]
# - FastMCP resource integration following standardized resource registration patterns
# - Comprehensive configuration and documentation access through MCP resource interface
# - HTTP-formatted responses maintaining consistency with JESSE Framework patterns
# - Template and example provision supporting knowledge base system usage
# - Read-only resource access ensuring system configuration integrity
###############################################################################
# [Source file constraints]
# - Resources must provide read-only access to configuration and documentation
# - Resource responses must use HTTP formatting for JESSE Framework consistency
# - Configuration resources must reflect current system state accurately
# - Template resources must provide practical examples for system usage
# - Error handling must provide clear guidance for resource access issues
###############################################################################
# [Dependencies]
# <codebase>: .models.indexing_config - Configuration data models and defaults
# <codebase>: ..helpers.http_formatter - HTTP response formatting for consistency
# <system>: fastmcp - MCP server framework and resource registration
# <system>: json - JSON serialization for configuration data
# <system>: pathlib - Path operations for resource file access
###############################################################################
# [GenAI tool change history]
# 2025-07-01T12:19:00Z : Initial FastMCP resources creation by CodeAssistant
# * Created knowledge bases resource interfaces with configuration access
# * Implemented template and documentation resources for system usage guidance
# * Set up HTTP-formatted resource responses following JESSE Framework patterns
###############################################################################

"""
FastMCP Resources for Knowledge Bases Hierarchical Indexing System.

This module provides MCP resource interfaces for accessing system configuration,
processing templates, usage documentation, and example workflows through
standardized FastMCP resource registration patterns.
"""

import json
import logging
from typing import Dict, Any

from fastmcp import FastMCP

from .models import IndexingConfig
from ..helpers.async_http_formatter import format_http_response

logger = logging.getLogger(__name__)


def register_knowledge_bases_resources(server: FastMCP) -> None:
    """
    [Function intent]
    Registers all knowledge bases resources with the FastMCP server for MCP integration.
    Provides comprehensive resource registration enabling configuration access,
    template provision, and documentation through standardized MCP resource interfaces.

    [Design principles]
    Centralized resource registration enabling clean MCP server integration.
    Comprehensive resource coverage supporting configuration access and usage guidance.
    Read-only resource access maintaining system configuration integrity.

    [Implementation details]
    Registers configuration resource for current system parameters access.
    Sets up template resources providing practical usage examples and workflows.
    Provides documentation resources for comprehensive system usage guidance.
    """
    
    @server.resource("jesse://knowledge_bases/config/default")
    async def knowledge_bases_default_config() -> str:
        """
        [Resource intent]
        Provides access to default knowledge bases indexing configuration parameters.
        Returns comprehensive configuration data including processing limits,
        LLM settings, and operational parameters for system understanding and customization.

        [Design principles]
        Read-only configuration access enabling system understanding without modification.
        Comprehensive parameter exposure supporting configuration analysis and planning.
        HTTP-formatted response maintaining consistency with JESSE Framework patterns.

        [Implementation details]
        Creates default IndexingConfig instance for parameter extraction.
        Serializes configuration to JSON format for structured data access.
        Returns HTTP-formatted response with complete configuration information.
        """
        try:
            # Create default configuration
            default_config = IndexingConfig()
            config_data = default_config.to_dict()
            
            # Add additional metadata
            response_data = {
                "configuration": config_data,
                "description": "Default configuration for Knowledge Bases Hierarchical Indexing System",
                "usage": "These parameters control indexing behavior, LLM integration, and processing constraints",
                "customization": "Configuration can be customized through tool parameters when triggering indexing operations"
            }
            
            return format_http_response(
                200, "OK",
                response_data,
                content_type="application/json"
            )
            
        except Exception as e:
            logger.error(f"Default configuration resource failed: {e}", exc_info=True)
            return format_http_response(
                500, "Internal Server Error",
                {"error": "Failed to retrieve default configuration", "details": str(e)}
            )
    
    @server.resource("jesse://knowledge_bases/templates/usage_examples")
    async def knowledge_bases_usage_examples() -> str:
        """
        [Resource intent]
        Provides practical usage examples and workflow templates for knowledge bases system.
        Returns comprehensive examples demonstrating different indexing scenarios,
        configuration options, and integration patterns for effective system utilization.

        [Design principles]
        Practical example provision supporting effective system usage and integration.
        Comprehensive scenario coverage demonstrating different use cases and workflows.
        Clear documentation format enabling quick understanding and implementation.

        [Implementation details]
        Provides structured examples for common indexing scenarios and configurations.
        Includes workflow templates for different processing modes and special handling.
        Returns HTTP-formatted response with comprehensive usage guidance and examples.
        """
        try:
            examples_data = {
                "basic_indexing": {
                    "description": "Basic incremental indexing of .knowledge directory",
                    "tool_call": "knowledge_bases_index_trigger",
                    "parameters": {
                        "target_path": ".knowledge",
                        "indexing_mode": "incremental",
                        "enable_git_clone_indexing": True,
                        "enable_project_base_indexing": False
                    },
                    "use_case": "Regular maintenance of knowledge base with minimal processing overhead"
                },
                "full_reindex": {
                    "description": "Complete reindexing of entire knowledge hierarchy",
                    "tool_call": "knowledge_bases_index_trigger", 
                    "parameters": {
                        "target_path": ".knowledge",
                        "indexing_mode": "full",
                        "enable_git_clone_indexing": True,
                        "enable_project_base_indexing": False
                    },
                    "use_case": "Fresh knowledge base generation or after significant content changes"
                },
                "project_indexing": {
                    "description": "Whole project codebase indexing with comprehensive coverage",
                    "tool_call": "knowledge_bases_index_trigger",
                    "parameters": {
                        "target_path": ".",
                        "indexing_mode": "full", 
                        "enable_git_clone_indexing": False,
                        "enable_project_base_indexing": True
                    },
                    "use_case": "Complete project understanding and comprehensive knowledge base creation"
                },
                "status_monitoring": {
                    "description": "Real-time monitoring of indexing operations",
                    "tool_call": "knowledge_bases_status",
                    "parameters": {},
                    "use_case": "Progress tracking and performance analysis during indexing operations"
                }
            }
            
            response_data = {
                "examples": examples_data,
                "description": "Practical usage examples for Knowledge Bases Hierarchical Indexing System",
                "note": "Adapt parameters based on specific requirements and project structure"
            }
            
            return format_http_response(
                200, "OK",
                response_data,
                content_type="application/json"
            )
            
        except Exception as e:
            logger.error(f"Usage examples resource failed: {e}", exc_info=True)
            return format_http_response(
                500, "Internal Server Error",
                {"error": "Failed to retrieve usage examples", "details": str(e)}
            )
    
    @server.resource("jesse://knowledge_bases/documentation/system_overview")
    async def knowledge_bases_system_overview() -> str:
        """
        [Resource intent]
        Provides comprehensive system overview documentation for knowledge bases indexing.
        Returns detailed information about system architecture, processing patterns,
        and integration capabilities for complete system understanding.

        [Design principles]
        Comprehensive system documentation enabling complete understanding of capabilities.
        Architecture explanation supporting effective system integration and usage.
        Technical detail provision enabling informed decision-making and troubleshooting.

        [Implementation details]
        Provides structured documentation covering all major system components.
        Includes architecture overview, processing patterns, and integration guidance.
        Returns HTTP-formatted response with comprehensive system documentation.
        """
        try:
            documentation_data = {
                "system_overview": {
                    "purpose": "Automated hierarchical knowledge base maintenance and content indexing",
                    "architecture": "Leaf-first processing with bottom-up assembly of knowledge files",
                    "integration": "FastMCP tools and resources with Claude 4 Sonnet LLM processing"
                },
                "key_components": {
                    "HierarchicalIndexer": "Core orchestrator coordinating indexing workflow",
                    "KnowledgeBuilder": "LLM-powered content analysis and knowledge file generation",
                    "RebuildDecisionEngine": "Centralized decision-making for comprehensive change detection",
                    "SpecialHandlers": "Git-clone and project-base specialized processing"
                },
                "processing_patterns": {
                    "leaf_first": "Child directories processed before parents for dependency resolution",
                    "bottom_up_assembly": "Parent knowledge files aggregate child summaries",
                    "incremental_updates": "Timestamp-based change detection minimizes processing overhead",
                    "concurrent_processing": "Configurable concurrency for performance optimization"
                },
                "special_scenarios": {
                    "git_clones": "Read-only processing with mirrored knowledge structure",
                    "project_base": "Whole codebase indexing with systematic exclusions"
                },
                "configuration": {
                    "processing_limits": "File size, chunk size, and batch processing configuration",
                    "llm_integration": "Claude 4 Sonnet model configuration and prompt templates",
                    "error_handling": "Graceful degradation and comprehensive error tracking"
                }
            }
            
            return format_http_response(
                200, "OK",
                documentation_data,
                content_type="application/json"
            )
            
        except Exception as e:
            logger.error(f"System overview resource failed: {e}", exc_info=True)
            return format_http_response(
                500, "Internal Server Error",
                {"error": "Failed to retrieve system overview", "details": str(e)}
            )

    logger.info("Knowledge Bases resources registered successfully")

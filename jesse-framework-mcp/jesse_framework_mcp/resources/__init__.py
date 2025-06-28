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
# Resources package initialization for JESSE Framework MCP Server,
# providing modern resource-first architecture with individual resource access patterns.
###############################################################################
# [Source file design principles]
# - Resource-first architecture with individual resource handlers
# - FastMCP auto-registration through decorators for modern transport
# - HTTP formatting applied consistently across all resources
# - Modular organization for maintainability and extensibility
###############################################################################
# [Source file constraints]
# - Must register remaining resource handlers after heavy resource removal
# - Maintains compatibility with existing FastMCP server setup
# - HTTP formatting must be applied consistently across all resources
###############################################################################
# [Dependencies]
# codebase:resources.workflows - HTTP-formatted workflow resources for Cline integration
# codebase:resources.knowledge - Knowledge base resource handlers with HTTP formatting
# codebase:resources.wip_tasks - WIP tasks resource handlers
###############################################################################
# [GenAI tool change history]
# 2025-06-28T08:14:00Z : Added session initialization meta-resource for comprehensive context loading by CodeAssistant
# * Added session_init import and registration for jesse://session/init-context resource
# * Updated __all__ exports to include new session_init module
# * Enhanced resource package with comprehensive session initialization capability
# * Maintains existing resource-first architecture patterns while adding meta-resource functionality
# 2025-06-28T06:52:50Z : Removed heavy resource pattern for modern resource-first architecture by CodeAssistant
# * Eliminated project_context heavy resource registration and import
# * Updated for individual resource architecture preparation
# * Simplified registration focusing on working resource handlers
# * Prepared structure for individual JESSE rule resources in Phase 3
# 2025-06-28T01:06:45Z : Updated for simplified MCP server architecture by CodeAssistant
# * Removed obsolete rules.py and session.py resource imports
# * Added project_context.py and wip_tasks.py resource imports
# * Updated to reflect HTTP-formatted resource architecture
# 2025-06-27T20:24:50Z : Initial resources package creation by CodeAssistant
# * Created modular resources package structure
# * Set up centralized import system for resource handlers
###############################################################################

"""
JESSE Framework MCP Server Resources Package

This package contains all FastMCP resource handlers organized by functionality:
- workflows: HTTP-formatted workflow resources for Cline slash command integration
- knowledge: Project knowledge base resources with lazy loading
- wip_tasks: WIP tasks inventory and individual task resources
- framework_rules: Individual JESSE rule resources (Phase 3 - Complete)
- project_resources: Project-specific resource handlers (Phase 3 - Complete)
- session_init: Session initialization meta-resource combining all essential contexts
"""

def register_all_resources():
    """
    [Function intent]
    Register all resource handlers with modern resource-first architecture.
    
    [Design principles]
    Individual resource access patterns with FastMCP auto-registration.
    HTTP-formatted resource delivery for consistent AI assistant processing.
    
    [Implementation details]
    Registers individual JESSE rules, project resources, workflows, knowledge bases, and WIP tasks.
    Resources auto-register via FastMCP decorators for modern transport.
    """
    from .framework_rules import register_framework_rules_resources  # Individual JESSE rules
    from .project_resources import register_project_resources       # Project context resources
    from .workflows import register_workflows_resources            # Workflow resources
    from .knowledge import register_knowledge_resources            # Knowledge base resources  
    from .wip_tasks import register_wip_tasks_resources           # WIP task resources
    from .session_init import register_session_init_resources     # Session initialization meta-resource
    
    # Register all resource handlers
    register_framework_rules_resources()  # Individual JESSE rule resources
    register_project_resources()          # Project context resources
    register_workflows_resources()        # Workflow resources (Cline integration)
    register_knowledge_resources()        # External knowledge base resources
    register_wip_tasks_resources()        # WIP task resources
    register_session_init_resources()     # Session initialization meta-resource

# Call registration function on import
register_all_resources()

__all__ = [
    'framework_rules',
    'project_resources',
    'session_init',
    'workflows', 
    'knowledge',
    'wip_tasks'
]

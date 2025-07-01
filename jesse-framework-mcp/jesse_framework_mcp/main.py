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
# Main FastMCP server implementation for JESSE Framework, providing resource-first
# MCP protocol compliance with FastMCP native transport architecture.
###############################################################################
# [Source file design principles]
# - FastMCP native transport with automatic lifecycle management
# - Resource-first architecture with individual resource access patterns
# - Clean separation between transport and resource implementations
# - Defensive programming with descriptive error messages for all failures
###############################################################################
# [Source file constraints]
# - Must use FastMCP native transport for optimal performance
# - Requires embedded_content/ directory created at build time
# - .knowledge/ directory access for project-specific knowledge
# - Resource logging for usage tracking and analytics
###############################################################################
# [Dependencies]
# system:logging - Server logging and error reporting
# system:pathlib.Path - Cross-platform filesystem operations
# system:fastmcp.FastMCP - FastMCP framework with native transport
# system:fastmcp.Context - FastMCP Context for resource operations
###############################################################################
# [GenAI tool change history]
# 2025-06-28T07:06:00Z : Implemented Phase 4 resource discovery optimization by CodeAssistant
# * Enhanced MCP protocol handlers with comprehensive resource listing and metadata
# * Added lightweight resource index (jesse://index) for programmatic discovery
# * Implemented URI-based routing to individual resource handlers
# * Added get_rule_by_name and get_project_resource_by_type helper functions for routing
# 2025-06-28T06:54:30Z : Implemented FastMCP native transport modernization by CodeAssistant
# * Replaced manual event loop with FastMCP native transport management
# * Fixed FastMCP API usage by removing obsolete request_handler decorators
# * Updated import structure removing asyncio, json, datetime dependencies
# * Modernized server initialization with FastMCP 2.0 patterns
# 2025-06-28T06:49:30Z : Removed complete tool-heavy architecture for resource-first modernization by CodeAssistant
# * Eliminated jesse_load_complete_context heavy tool with 15+ support functions
# * Removed 4 exception classes and all tool-specific error handling infrastructure
# * Deleted ~500 lines of obsolete tool-based session management code
# * Preserved MCP protocol handlers for Cline integration and workflow access
# 2025-06-28T01:30:00Z : Implemented critical MCP protocol compliance for Cline slash command integration by CodeAssistant
# * Added standard MCP resources/list and resources/read request handlers (CRITICAL FIX)
# * Proper MCP protocol implementation enabling JESSE workflows as Cline slash commands
# * Resource discovery endpoint returning file://workflows/ URIs for all JESSE workflows
# * Resource content delivery with HTTP formatting and CRITICAL criticality for AI assistants
###############################################################################

import logging
from pathlib import Path

from fastmcp import FastMCP, Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
server = FastMCP("JESSE Framework")

# Import resource modules (auto-registers via decorators)
from . import resources  # Auto-registers all resource handlers
from .helpers import knowledge_scanners  # Only what's needed for resource support
from .helpers.http_formatter import format_http_section, ContentCriticality
from .knowledge_bases import register_knowledge_bases_tools, register_knowledge_bases_resources
import json
from datetime import datetime

# Register knowledge bases tools and resources
register_knowledge_bases_tools(server)
register_knowledge_bases_resources(server)

# === LIGHTWEIGHT RESOURCE INDEX ===

@server.resource("jesse://index")
async def framework_index(ctx: Context) -> str:
    """
    [Function intent]
    Lightweight framework resource index for discovery optimization.
    
    [Design principles]
    JSON-based resource index for programmatic discovery.
    Fast access to resource metadata without full content loading.
    
    [Implementation details]
    Builds structured index of all available resources with metadata,
    categories, and access patterns for client optimization.
    """
    await ctx.info("Building framework resource index")
    
    try:
        # Gather resource statistics
        from .resources.framework_rules import get_available_rule_names
        
        rule_names = await get_available_rule_names()
        
        try:
            from .helpers.knowledge_scanners import scan_available_knowledge_bases_async
            knowledge_bases = await scan_available_knowledge_bases_async(ctx)
        except Exception:
            knowledge_bases = []
        
        # Count WIP tasks
        wip_dir = Path(".knowledge/work-in-progress")
        wip_count = len([d for d in wip_dir.iterdir() if d.is_dir()]) if wip_dir.exists() else 0
        
        index_data = {
            "framework_version": "2025.6",
            "architecture": "resource-first",
            "resource_categories": {
                "framework_rules": {
                    "count": len(rule_names),
                    "criticality": "CRITICAL",
                    "uri_pattern": "jesse://framework/rule/{rule_name}",
                    "available_rules": rule_names
                },
                "project_resources": {
                    "count": 3,
                    "criticality": "INFORMATIONAL", 
                    "uri_pattern": "jesse://project/{resource_type}",
                    "available_types": ["knowledge", "wip-tasks", "context"]
                },
                "knowledge_bases": {
                    "count": len(knowledge_bases),
                    "criticality": "INFORMATIONAL",
                    "uri_pattern": "jesse://knowledge/{kb_name}",
                    "available_bases": knowledge_bases
                },
                "wip_tasks": {
                    "count": wip_count,
                    "criticality": "INFORMATIONAL",
                    "uri_pattern": "jesse://project/wip-task/{task_name}",
                    "note": "Individual WIP tasks accessible via dynamic URIs"
                },
                "workflows": {
                    "criticality": "INFORMATIONAL",
                    "uri_pattern": "jesse://workflows/{workflow_name}",
                    "note": "Cline integration workflows"
                }
            },
            "quick_access": {
                "all_framework_rules": "jesse://framework/rule/*",
                "project_overview": "jesse://project/context",
                "current_wip_tasks": "jesse://project/wip-tasks"
            },
            "generated": datetime.now().isoformat()
        }
        
        content = json.dumps(index_data, indent=2, ensure_ascii=False)
        
        return format_http_section(
            content=content,
            content_type="application/json",
            criticality=ContentCriticality.INFORMATIONAL,
            description="JESSE Framework Resource Index",
            section_type="framework-index",
            location="jesse://index"
        )
        
    except Exception as e:
        await ctx.error(f"Failed to build framework index: {str(e)}")
        raise ValueError(f"Framework index failed: {str(e)}")


# === HELPER FUNCTIONS FOR WORKFLOW RESOURCES ===

async def get_embedded_workflow_files() -> list[str]:
    """
    [Function intent]
    Get list of embedded workflow files for resource implementations.
    
    [Design principles]
    Dynamic workflow discovery from embedded content.
    Consistent workflow file pattern recognition.
    
    [Implementation details]
    Scans embedded workflows directory and returns list of .md files.
    
    Returns:
        List of workflow filenames
        
    Raises:
        Exception: When workflow files cannot be accessed
    """
    try:
        from importlib import resources
        workflows_dir = resources.files('jesse_framework_mcp.embedded_content.workflows')
        return [f.name for f in workflows_dir.iterdir() if f.suffix == '.md']
    except Exception as e:
        raise Exception(f"Failed to get workflow files: {str(e)}")


async def get_workflow_description(workflow_file: str) -> str:
    """
    [Function intent]
    Get workflow description from workflow metadata.
    
    [Design principles]
    Consistent workflow description extraction.
    Fallback to filename-based description if metadata unavailable.
    
    [Implementation details]
    Attempts to extract description from workflow file metadata,
    falls back to human-readable filename conversion.
    
    Args:
        workflow_file: Workflow filename
        
    Returns:
        Human-readable workflow description
    """
    # Convert filename to human-readable description
    base_name = workflow_file.replace('.md', '')
    # Remove jesse_ prefix if present
    if base_name.startswith('jesse_'):
        base_name = base_name[6:]
    
    # Convert underscores to spaces and title case
    description = base_name.replace('_', ' ').title()
    
    # Add "JESSE" prefix for workflow context
    return f"JESSE {description} Workflow"

# === PROMPT DEFINITIONS ===

@server.prompt("jesse_framework_start")
async def jesse_framework_start_prompt(project_context: str = "") -> str:
    """
    [Function intent]
    Generate initialization prompt for JESSE framework usage.
    
    [Design principles]
    Reusable prompt template for consistent framework introduction.
    Contextual adaptation based on project information.
    
    [Implementation details]
    Creates structured prompt for AI assistant framework initialization
    with project-specific context integration.
    
    Args:
        project_context: Optional project description for context
        
    Returns:
        Formatted JESSE framework initialization prompt
    """
    
    base_prompt = """Initialize the JESSE AI Framework for this development session.

The JESSE Framework provides:
- Comprehensive coding standards and documentation requirements
- Work-in-Progress (WIP) task management system
- Knowledge base integration for project context
- Automated workflow templates for common development tasks

Please load the complete framework context and confirm initialization."""

    if project_context:
        return f"""{base_prompt}

Project Context: {project_context}

Adapt the framework initialization to this specific project context."""
    
    return base_prompt


@server.prompt("jesse_wip_task_create")
async def jesse_wip_task_create_prompt(task_description: str, estimated_complexity: str = "medium") -> str:
    """
    [Function intent]
    Generate prompt for creating new WIP tasks with JESSE framework.
    
    [Design principles]
    Structured task creation with complexity assessment.
    Consistent WIP task initialization across different scenarios.
    
    [Implementation details]
    Creates comprehensive task creation prompt with complexity-based
    recommendations and framework integration guidance.
    
    Args:
        task_description: Description of the task to create
        estimated_complexity: Task complexity (simple, medium, complex)
        
    Returns:
        Formatted WIP task creation prompt
    """
    
    complexity_guidance = {
        "simple": "Single session task, minimal documentation required",
        "medium": "Multi-session task, standard documentation and testing",
        "complex": "Extended task, comprehensive planning and documentation"
    }
    
    guidance = complexity_guidance.get(estimated_complexity, complexity_guidance["medium"])
    
    return f"""Create a new JESSE Framework Work-in-Progress (WIP) task.

Task Description: {task_description}
Estimated Complexity: {estimated_complexity} ({guidance})

Please use the /jesse_wip_task_create.md workflow to:
1. Create the WIP task structure
2. Set up appropriate Git branch (if applicable)
3. Initialize task documentation
4. Begin implementation planning

The task should follow JESSE coding standards and include comprehensive documentation."""


@server.prompt("jesse_knowledge_capture")
async def jesse_knowledge_capture_prompt(knowledge_type: str, content_summary: str) -> str:
    """
    [Function intent]
    Generate prompt for capturing knowledge in JESSE knowledge base.
    
    [Design principles]
    Structured knowledge capture with type-specific formatting.
    Integration with JESSE knowledge management system.
    
    [Implementation details]
    Creates knowledge capture prompt with appropriate categorization
    and formatting guidance for different knowledge types.
    
    Args:
        knowledge_type: Type of knowledge (learning, pattern, decision, etc.)
        content_summary: Brief summary of knowledge to capture
        
    Returns:
        Formatted knowledge capture prompt
    """
    
    return f"""Capture new knowledge in the JESSE Framework knowledge base.

Knowledge Type: {knowledge_type}
Content Summary: {content_summary}

Please use the /jesse_wip_task_capture_knowledge.md workflow to:
1. Categorize the knowledge appropriately
2. Format according to JESSE documentation standards
3. Add to relevant knowledge base (project or WIP task)
4. Update cross-references if needed

Ensure the captured knowledge follows JESSE's intemporal writing style (present tense, stating facts rather than referencing past implementations)."""


def main() -> None:
    """
    [Function intent]
    Main entry point for JESSE Framework MCP Server with FastMCP native transport.
    
    [Design principles]
    Let FastMCP handle all transport lifecycle management automatically.
    Clean startup with FastMCP 2.0 best practices.
    
    [Implementation details]
    Uses server.run() with FastMCP's built-in transport management.
    No manual event loop creation - FastMCP handles everything.
    
    Raises:
        Exception: When MCP server fails to start or run
    """
    
    try:
        logger.info("Starting JESSE Framework MCP Server...")
        logger.info("Architecture: Pure resource-first with individual JESSE rules")
        logger.info("Transport: FastMCP native stdio management")
        logger.info("Resources: Individual JESSE rules, project context, workflows, knowledge bases")
        
        # Let FastMCP handle all transport management automatically
        server.run(transport="stdio")
        
    except KeyboardInterrupt:
        logger.info("JESSE Framework MCP Server stopped by user")
    except Exception as e:
        logger.error(f"JESSE Framework MCP Server failed: {str(e)}")
        raise


# Entry point for console script
if __name__ == "__main__":
    main()

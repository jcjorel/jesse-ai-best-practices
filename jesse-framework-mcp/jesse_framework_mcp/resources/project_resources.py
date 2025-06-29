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
# Project-specific resources for JESSE Framework development project context.
# Provides individual access to project knowledge, WIP tasks, and context summary.
###############################################################################
# [Source file design principles]
# - Individual resources for different project aspects
# - INFORMATIONAL criticality for project context (not framework rules)
# - HTTP formatting preserved for consistency
# - Graceful handling of missing project files
###############################################################################
# [Source file constraints]
# - Must access .knowledge/ directory structure
# - Project knowledge files may not exist (graceful handling required)
# - WIP task directory structure must be validated
# - HTTP formatting must match existing patterns
###############################################################################
# [Dependencies]
# codebase:jesse_framework_mcp.main.server - FastMCP server instance
# codebase:jesse_framework_mcp.helpers.http_formatter - HTTP section formatting
# codebase:jesse_framework_mcp.helpers.session_management - WIP task functions
# codebase:jesse_framework_mcp.helpers.knowledge_scanners - Knowledge base scanning
# system:pathlib.Path - File system operations
# system:json - JSON formatting for structured data
###############################################################################
# [GenAI tool change history]
# 2025-06-28T11:44:07Z : Fixed Content-Location headers in gitignore resource to use portable paths by CodeAssistant
# * Fixed get_project_gitignore_files() to pass HttpPath objects to format_http_section() location parameter
# * Corrected both mandatory and error section location parameters to use gitignore_path instead of location_path
# * Content-Location headers now correctly show file://{PROJECT_ROOT}/... format instead of missing file:// prefix
# * Maintains consistent portable path format across all MCP resource Content-Location headers
# 2025-06-28T11:32:43Z : Updated gitignore resource to show only mandatory and existing optional files by CodeAssistant
# * Modified get_project_gitignore_files() to distinguish mandatory vs optional .gitignore files
# * Added .knowledge/git-clones/.gitignore as mandatory location alongside PROJECT_ROOT
# * Mandatory missing files now show CRITICAL warnings requiring immediate action
# * Optional files only included in output if they exist (no placeholders for missing)
# 2025-06-28T07:55:32Z : Added gitignore files resource with multi-file HTTP sections by CodeAssistant
# * Implemented get_project_gitignore_files() resource at jesse://project/gitignore-files
# * Scans PROJECT_ROOT, .coding_assistant, .knowledge, .clinerules for .gitignore files
# * Returns multi-part HTTP response with each .gitignore as writable section
# * Graceful handling of missing files with appropriate placeholder content
# 2025-06-28T06:58:10Z : Initial project resources implementation by CodeAssistant
# * Created individual project knowledge resource with HTTP formatting
# * Implemented WIP task inventory resource with JSON formatting
# * Added project context summary resource for overview information
# * Established graceful handling for missing project files
###############################################################################

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from fastmcp import Context
from ..main import server
from ..helpers.http_formatter import format_http_section, ContentCriticality, HttpPath, format_multi_section_response
from ..helpers.session_management import get_current_wip_task_name_async
from ..helpers.knowledge_scanners import scan_git_clone_knowledge_bases_async, scan_pdf_knowledge_bases_async


# === PROJECT RESOURCES ===

@server.resource("jesse://project/knowledge")
async def get_project_knowledge(ctx: Context) -> str:
    """
    [Function intent]
    Individual project knowledge resource with HTTP formatting.
    
    [Design principles]
    Project-specific knowledge classified as INFORMATIONAL content.
    Graceful handling when project knowledge is not available.
    
    [Implementation details]
    Loads project knowledge base from .knowledge/persistent-knowledge/KNOWLEDGE_BASE.md
    and applies HTTP formatting with INFORMATIONAL criticality.
    
    Args:
        ctx: FastMCP Context for progress reporting and logging
        
    Returns:
        HTTP-formatted project knowledge content
        
    Raises:
        ValueError: When project knowledge exists but cannot be processed
    """
    await ctx.info("Loading project knowledge base")
    
    try:
        kb_path = Path(".knowledge/persistent-knowledge/KNOWLEDGE_BASE.md")
        
        if not kb_path.exists():
            await ctx.info("No project knowledge base found")
            content = "# Project Knowledge Base\n\nNo project knowledge base found. Create .knowledge/persistent-knowledge/KNOWLEDGE_BASE.md to add project-specific knowledge."
        else:
            with open(kb_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                await ctx.info("Project knowledge base is empty")
                content = "# Project Knowledge Base\n\nProject knowledge base exists but is empty."
        
        return format_http_section(
            content=content,
            content_type="text/markdown",
            criticality=ContentCriticality.INFORMATIONAL,
            description="Project Knowledge Base Content",
            section_type="project-knowledge",
            location="file://{PROJECT_ROOT}/.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md",
            writable=True
        )
        
    except Exception as e:
        await ctx.error(f"Failed to load project knowledge: {str(e)}")
        raise ValueError(f"Project knowledge loading failed: {str(e)}")


@server.resource("jesse://project/context")
async def get_project_context_summary(ctx: Context) -> str:
    """
    [Function intent]
    Project context summary resource with overview information.
    
    [Design principles]
    High-level project overview with INFORMATIONAL criticality.
    Combines multiple project aspects into coherent summary.
    
    [Implementation details]
    Gathers project overview, knowledge base summary, WIP task status,
    and external knowledge sources into unified context summary.
    
    Args:
        ctx: FastMCP Context for progress reporting and logging
        
    Returns:
        HTTP-formatted project context summary
        
    Raises:
        ValueError: When project context cannot be assembled
    """
    await ctx.info("Building project context summary")
    
    try:
        # Gather project information
        current_task = await get_current_wip_task_name_async(ctx)
        
        # Count knowledge sources
        kb_path = Path(".knowledge/persistent-knowledge/KNOWLEDGE_BASE.md")
        has_project_kb = kb_path.exists() and kb_path.stat().st_size > 0
        
        # Count WIP tasks
        wip_dir = Path(".knowledge/work-in-progress")
        wip_count = len([d for d in wip_dir.iterdir() if d.is_dir()]) if wip_dir.exists() else 0
        
        # Count external knowledge bases
        try:
            git_clones = await scan_git_clone_knowledge_bases_async(ctx)
            pdf_kbs = await scan_pdf_knowledge_bases_async(ctx)
            external_kb_count = len(git_clones) + len(pdf_kbs)
        except Exception:
            external_kb_count = 0
        
        # Build summary content
        summary_lines = [
            "# Project Context Summary",
            "",
            "## JESSE Framework Development Project",
            "This project develops the JESSE AI Best Practices Framework using the framework itself (meta-development).",
            "",
            "## Project Status",
            f"- **Current WIP Task**: {current_task or 'None active'}",
            f"- **Active WIP Tasks**: {wip_count}",
            f"- **Project Knowledge Base**: {'Available' if has_project_kb else 'Not configured'}",
            f"- **External Knowledge Sources**: {external_kb_count}",
            "",
            "## Framework Architecture",
            "- **Building**: Components in `artifacts/` directory (framework under development)",
            "- **Using**: Global installation (`${HOME}/Cline/Rules/`) + project `.knowledge/` files",
            "",
            "## Resource Access",
            "- Individual JESSE rules: `jesse://framework/rule/{rule_name}`",
            "- Project knowledge: `jesse://project/knowledge`",
            "- WIP tasks: `jesse://project/wip-tasks`",
            "- External knowledge: `jesse://knowledge/{kb_name}`",
            "- Workflows: `file://workflows/{workflow_name}` (Cline integration)",
            "",
            f"Generated: {datetime.now().isoformat()}"
        ]
        
        content = "\n".join(summary_lines)
        
        return format_http_section(
            content=content,
            content_type="text/markdown",
            criticality=ContentCriticality.INFORMATIONAL,
            description="Project Context Summary and Overview",
            section_type="project-context",
            location="file://{PROJECT_ROOT}/",
            additional_headers={
                "WIP-Tasks": str(wip_count),
                "Current-Task": current_task or "None",
                "External-Knowledge": str(external_kb_count)
            }
        )
        
    except Exception as e:
        await ctx.error(f"Failed to build project context summary: {str(e)}")
        raise ValueError(f"Project context summary failed: {str(e)}")


@server.resource("jesse://project/wip-tasks")
async def get_wip_tasks_inventory(ctx: Context) -> str:
    """
    [Function intent]
    WIP tasks inventory resource with JSON formatting.
    
    [Design principles]
    Structured WIP task information with INFORMATIONAL criticality.
    JSON format for programmatic access to task data.
    
    [Implementation details]
    Scans .knowledge/work-in-progress directory and builds comprehensive
    task inventory with status, metadata, and access information.
    
    Args:
        ctx: FastMCP Context for progress reporting and logging
        
    Returns:
        HTTP-formatted WIP tasks inventory as JSON
        
    Raises:
        ValueError: When WIP task inventory cannot be built
    """
    await ctx.info("Building WIP tasks inventory")
    
    try:
        wip_dir = Path(".knowledge/work-in-progress")
        
        if not wip_dir.exists():
            await ctx.info("No WIP tasks directory found")
            inventory = {
                "current_task": None,
                "active_tasks": [],
                "task_count": 0,
                "directory_status": "not_found",
                "message": "No WIP tasks directory found. Create .knowledge/work-in-progress/ to start using WIP tasks."
            }
        else:
            # Get current task
            current_task = await get_current_wip_task_name_async(ctx)
            
            # Scan WIP tasks
            tasks = []
            for task_dir in wip_dir.iterdir():
                if task_dir.is_dir():
                    task_info = {
                        "name": task_dir.name,
                        "is_current": task_dir.name == current_task,
                        "has_wip_file": (task_dir / "WIP_TASK.md").exists(),
                        "has_progress": (task_dir / "PROGRESS.md").exists(),
                        "uri": f"jesse://project/wip-task/{task_dir.name}"
                    }
                    
                    # Add modification time if available
                    try:
                        wip_file = task_dir / "WIP_TASK.md"
                        if wip_file.exists():
                            task_info["modified"] = datetime.fromtimestamp(wip_file.stat().st_mtime).isoformat()
                    except Exception:
                        pass
                    
                    tasks.append(task_info)
            
            # Sort tasks: current first, then by modification time
            tasks.sort(key=lambda t: (not t["is_current"], t.get("modified", "")), reverse=True)
            
            inventory = {
                "current_task": current_task,
                "active_tasks": tasks,
                "task_count": len(tasks),
                "directory_status": "available",
                "quick_access": {
                    "current_task_uri": f"jesse://project/wip-task/{current_task}" if current_task else None,
                    "create_new_task": "Use /jesse_wip_task_create.md workflow",
                    "switch_tasks": "Use /jesse_wip_task_switch.md workflow"
                }
            }
        
        content = json.dumps(inventory, indent=2, ensure_ascii=False)
        
        return format_http_section(
            content=content,
            content_type="application/json",
            criticality=ContentCriticality.INFORMATIONAL,
            description="WIP Tasks Inventory and Status",
            section_type="wip-inventory",
            location="file://{PROJECT_ROOT}/.knowledge/work-in-progress/",
            additional_headers={
                "Current-Task": current_task or "None",
                "Task-Count": str(len(tasks) if 'tasks' in locals() else 0)
            }
        )
        
    except Exception as e:
        await ctx.error(f"Failed to build WIP tasks inventory: {str(e)}")
        raise ValueError(f"WIP tasks inventory failed: {str(e)}")


# Note: get_project_gitignore_files function moved to gitignore.py for better organization


# === HELPER FUNCTIONS ===

async def get_project_resource_by_type(resource_type: str, ctx: Context) -> str:
    """
    [Function intent]
    Route project resource requests to appropriate handler.
    
    [Design principles]
    Centralized routing for project resource access.
    Maintains consistency with individual resource patterns.
    
    [Implementation details]
    Maps resource types to specific handler functions,
    delegates to appropriate handler with Context propagation.
    
    Args:
        resource_type: Resource type (e.g., 'knowledge', 'wip-tasks', 'context')
        ctx: FastMCP Context for progress reporting and logging
        
    Returns:
        HTTP-formatted project resource content
        
    Raises:
        ValueError: When resource type is not recognized
    """
    handlers = {
        'knowledge': get_project_knowledge,
        'wip-tasks': get_wip_tasks_inventory,
        'context': get_project_context_summary
    }
    
    handler = handlers.get(resource_type)
    if not handler:
        raise ValueError(f"Unknown project resource type: {resource_type}")
    
    return await handler(ctx)


def register_project_resources():
    """
    [Function intent]
    Register all project resource handlers with the server.
    
    [Design principles]
    FastMCP auto-registration through decorators for modern transport.
    Manual registration function for compatibility with existing patterns.
    
    [Implementation details]
    Resources are auto-registered via @server.resource decorators.
    This function provides explicit registration point if needed.
    """
    # Resources auto-register via FastMCP decorators
    # This function exists for explicit registration compatibility
    pass

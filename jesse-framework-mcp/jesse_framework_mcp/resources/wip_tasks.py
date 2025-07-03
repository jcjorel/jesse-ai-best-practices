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
# WIP tasks resource handlers for JESSE Framework MCP server providing comprehensive
# task management through HTTP-formatted resources including task inventory,
# individual task access, and project management context.
###############################################################################
# [Source file design principles]
# Centralized WIP task information for project management and development context
# All WIP task content classified as INFORMATIONAL for helpful context delivery
# JSON format for structured task data with HTTP wrapper for consistent parsing
# Individual task access for focused development work with combined task/progress info
###############################################################################
# [Source file constraints]
# Must maintain byte-perfect HTTP formatting for all task content sections
# All WIP tasks must be classified as INFORMATIONAL criticality
# Resource loading must handle missing tasks gracefully with descriptive errors
# Task directory scanning must be efficient and not impact performance
###############################################################################
# [Dependencies]
# <codebase>: jesse_framework_mcp.helpers.http_formatter for HTTP section formatting
# <system>: fastmcp Context for async progress reporting and logging
# <system>: pathlib for cross-platform path operations
# <system>: json for structured task data serialization
###############################################################################
# [GenAI tool change history]
# 2025-06-28T07:37:00Z : Updated to use new HttpFile-based API with writable flags by CodeAssistant
# * Added HttpPath import for new HTTP formatter API compatibility
# * Added writable=True parameter to both format_http_section calls for editable WIP task content
# * Enhanced HTTP formatting with Content-Writable headers for Cline integration
# * Maintained INFORMATIONAL criticality while enabling content editing capabilities for WIP tasks
# 2025-06-28T00:37:10Z : Initial WIP tasks resource implementation by CodeAssistant
# * Created jesse://wip-tasks inventory resource with JSON format
# * Implemented jesse://wip-task/{task_name} for individual task access
# * Added comprehensive task scanning and metadata extraction
# * Established task status tracking and Git branch integration
###############################################################################

import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path

from fastmcp import Context
from ..main import server
from ..helpers.http_formatter import (
    format_http_section,
    ContentCriticality,
    HttpPath
)
from ..helpers.path_utils import get_project_root
from ..helpers.project_setup import get_project_setup_guidance
import os


def register_wip_tasks_resources():
    """
    [Function intent]
    Register WIP tasks resources with HTTP formatting for comprehensive task management.
    
    [Design principles]
    Single registration function for all WIP task resources.
    Clear separation of resource registration from implementation logic.
    
    [Implementation details]
    Registers both inventory and individual task resources with FastMCP server.
    """
    # Main resource registration handled by decorators


@server.resource("jesse://wip-tasks")
async def get_wip_tasks_inventory(ctx: Context) -> str:
    """
    [Function intent]
    Provide complete WIP tasks inventory and current task context in HTTP format.
    
    [Design principles]
    Centralized WIP task information for project management and context.
    All WIP task content classified as INFORMATIONAL for helpful guidance.
    JSON format for structured data with HTTP wrapper for consistent parsing.
    Project root detection ensures resources work regardless of MCP server launch method.
    
    [Implementation details]
    Checks project root availability first, returns setup guidance if missing.
    Scans .knowledge/work-in-progress/ directory, builds task inventory,
    includes current task details, formats as HTTP section with JSON content.
    
    Args:
        ctx: FastMCP Context for logging and progress reporting
        
    Returns:
        HTTP-formatted WIP tasks inventory as JSON
        
    Raises:
        ValueError: When WIP tasks directory cannot be accessed or processed
    """
    
    await ctx.info("Loading WIP tasks inventory...")
    
    # === PROJECT ROOT DETECTION ===
    project_root = get_project_root()
    if not project_root:
        await ctx.error("No JESSE Framework project root detected for WIP tasks")
        return get_project_setup_guidance()
    
    # Set working directory to project root for all operations
    original_cwd = os.getcwd()
    try:
        os.chdir(project_root)
        await ctx.info(f"WIP tasks working directory set to project root: {project_root}")
    except Exception as e:
        await ctx.error(f"Failed to change to project root directory: {str(e)}")
        return get_project_setup_guidance()
    
    try:
        # Build WIP tasks inventory
        await ctx.report_progress(25, 100, "Scanning WIP tasks directory...")
        
        # Get task information with proper None handling
        current_task_info = await get_current_wip_task_info()
        active_tasks_list = await get_active_wip_tasks_list()
        completed_tasks_list = await get_recently_completed_tasks()
        task_stats = await get_wip_task_statistics()
        
        wip_data = {
            "current_task": current_task_info or {"name": "None", "status": "No active task"},
            "active_tasks": active_tasks_list or [],
            "completed_tasks": completed_tasks_list or [],
            "task_statistics": task_stats or {},
            "last_updated": datetime.now().isoformat()
        }
        
        await ctx.report_progress(75, 100, "Formatting task inventory...")
        
        # Convert to JSON
        wip_json = json.dumps(wip_data, indent=2, ensure_ascii=False)
        
        # Safe header extraction with None checks
        current_task = wip_data.get("current_task") or {}
        current_task_name = current_task.get("name", "None") if isinstance(current_task, dict) else "None"
        active_tasks = wip_data.get("active_tasks") or []
        
        # Format as HTTP section
        formatted_wip = format_http_section(
            content=wip_json,
            content_type="application/json",
            criticality=ContentCriticality.INFORMATIONAL,
            description="WIP Tasks Inventory and Status",
            section_type="wip-inventory",
            location="file://{PROJECT_ROOT}/.knowledge/work-in-progress/",
            additional_headers={
                "Tasks-Count": str(len(active_tasks)),
                "Current-Task": current_task_name,
                "Last-Updated": wip_data["last_updated"]
            },
            writable=True
        )
        
        await ctx.report_progress(100, 100, "WIP tasks inventory ready")
        await ctx.info(f"WIP tasks inventory loaded: {len(wip_data.get('active_tasks', []))} active tasks")
        
        return formatted_wip
        
    except Exception as e:
        error_msg = f"Failed to load WIP tasks inventory: {str(e)}"
        await ctx.error(error_msg)
        raise ValueError(error_msg)
    
    finally:
        # Restore original working directory
        try:
            os.chdir(original_cwd)
        except Exception as e:
            await ctx.warning(f"Failed to restore original working directory: {str(e)}")


@server.resource("jesse://wip-task/{task_name}")
async def get_specific_wip_task(task_name: str, ctx: Context) -> str:
    """
    [Function intent]
    Provide specific WIP task content including WIP_TASK.md and PROGRESS.md.
    
    [Design principles]
    Individual task access for focused development work.
    Combined task and progress information in single HTTP-formatted resource.
    INFORMATIONAL criticality for helpful project context.
    
    [Implementation details]
    Loads both WIP_TASK.md and PROGRESS.md for specified task,
    combines into single HTTP response with comprehensive task metadata.
    
    Args:
        task_name: Name of the WIP task to load
        ctx: FastMCP Context for logging and progress reporting
        
    Returns:
        HTTP-formatted WIP task content with both task and progress sections
        
    Raises:
        ValueError: When WIP task cannot be found or loaded
    """
    
    await ctx.info(f"Loading WIP task: {task_name}")
    
    try:
        # Verify task exists
        task_dir = Path.cwd() / ".knowledge" / "work-in-progress" / task_name
        if not task_dir.exists():
            raise ValueError(f"WIP task directory not found: {task_name}")
        
        await ctx.report_progress(25, 100, f"Loading task definition...")
        # Load task content
        task_content = await load_wip_task_content(task_name)
        
        await ctx.report_progress(50, 100, f"Loading progress tracking...")
        progress_content = await load_wip_progress_content(task_name)
        
        await ctx.report_progress(75, 100, f"Gathering task metadata...")
        # Get task metadata
        task_status = await get_task_status(task_name)
        git_branch = await get_task_git_branch(task_name)
        last_updated = await get_task_last_updated(task_name)
        
        # Combine task and progress content
        combined_content = f"""# WIP Task: {task_name}

## Task Metadata
- **Status**: {task_status}
- **Git Branch**: {git_branch}
- **Last Updated**: {last_updated}

## Task Definition
{task_content}

## Progress Tracking
{progress_content}"""
        
        # Format as HTTP section
        formatted_task = format_http_section(
            content=combined_content,
            content_type="text/markdown",
            criticality=ContentCriticality.INFORMATIONAL,
            description=f"WIP Task: {task_name}",
            section_type="wip-task",
            location=f"file://{{PROJECT_ROOT}}/.knowledge/work-in-progress/{task_name}/",
            additional_headers={
                "Task-Name": task_name,
                "Task-Status": task_status,
                "Git-Branch": git_branch,
                "Last-Updated": last_updated
            },
            writable=True
        )
        
        await ctx.report_progress(100, 100, f"WIP task loaded")
        await ctx.info(f"WIP task loaded: {task_name}")
        
        return formatted_task
        
    except Exception as e:
        error_msg = f"Failed to load WIP task {task_name}: {str(e)}"
        await ctx.error(error_msg)
        raise ValueError(error_msg)


async def get_current_wip_task_info() -> Optional[Dict[str, Any]]:
    """
    [Function intent]
    Extract current WIP task information from project knowledge base.
    
    [Design principles]
    Parse project knowledge to identify current active WIP task.
    Return structured data for task inventory integration.
    
    [Implementation details]
    Reads project knowledge base file, parses for current WIP task section,
    extracts task name, status, and metadata into dictionary.
    
    Returns:
        Dictionary with current WIP task information, None if no current task
        
    Raises:
        ValueError: When project knowledge exists but cannot be parsed
    """
    
    try:
        # Load project knowledge base
        kb_path = Path.cwd() / ".knowledge" / "persistent-knowledge" / "KNOWLEDGE_BASE.md"
        
        if not kb_path.exists():
            return None
        
        with open(kb_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for current WIP task section
        lines = content.split('\n')
        current_task = None
        
        for i, line in enumerate(lines):
            if line.strip().startswith("**Active Task**:") and "None" not in line:
                # Extract task name
                task_line = line.strip()
                if ":" in task_line:
                    task_name = task_line.split(":", 1)[1].strip()
                    if task_name and task_name != "None":
                        current_task = {"name": task_name}
                        
                        # Look for additional task info in following lines
                        for j in range(i + 1, min(i + 5, len(lines))):
                            if lines[j].strip().startswith("**Status**:"):
                                current_task["status"] = lines[j].split(":", 1)[1].strip()
                            elif lines[j].strip().startswith("**Phase**:"):
                                current_task["phase"] = lines[j].split(":", 1)[1].strip()
                            elif lines[j].strip().startswith("**Last Updated**:"):
                                current_task["last_updated"] = lines[j].split(":", 1)[1].strip()
                        
                        break
        
        return current_task
        
    except Exception as e:
        raise ValueError(f"Failed to parse current WIP task info: {str(e)}")


async def get_active_wip_tasks_list() -> List[Dict[str, Any]]:
    """
    [Function intent]
    Get list of all active WIP tasks by scanning work-in-progress directory.
    
    [Design principles]
    Directory-based task discovery with metadata extraction.
    Structured data for easy processing and display.
    
    [Implementation details]
    Scans .knowledge/work-in-progress/ for task directories,
    extracts metadata from each task for inventory display.
    
    Returns:
        List of dictionaries with task information
        
    Raises:
        ValueError: When work-in-progress directory cannot be accessed
    """
    
    try:
        wip_dir = Path.cwd() / ".knowledge" / "work-in-progress"
        
        if not wip_dir.exists():
            return []
        
        active_tasks = []
        
        for task_dir in wip_dir.iterdir():
            if task_dir.is_dir():
                task_info = {
                    "name": task_dir.name,
                    "status": await get_task_status(task_dir.name),
                    "git_branch": await get_task_git_branch(task_dir.name),
                    "last_updated": await get_task_last_updated(task_dir.name),
                    "has_task_file": (task_dir / "WIP_TASK.md").exists(),
                    "has_progress_file": (task_dir / "PROGRESS.md").exists()
                }
                active_tasks.append(task_info)
        
        # Sort by last updated (most recent first)
        active_tasks.sort(key=lambda x: x.get("last_updated", ""), reverse=True)
        
        return active_tasks
        
    except Exception as e:
        raise ValueError(f"Failed to scan active WIP tasks: {str(e)}")


async def get_recently_completed_tasks() -> List[Dict[str, Any]]:
    """
    [Function intent]
    Get list of recently completed tasks from project knowledge base.
    
    [Design principles]
    Extract completed task information from persistent knowledge.
    Limited to recent completions for relevant context.
    
    [Implementation details]
    Parses project knowledge base for "Recently Completed" section,
    extracts task completion information.
    
    Returns:
        List of recently completed task information
        
    Raises:
        ValueError: When project knowledge cannot be parsed
    """
    
    try:
        kb_path = Path.cwd() / ".knowledge" / "persistent-knowledge" / "KNOWLEDGE_BASE.md"
        
        if not kb_path.exists():
            return []
        
        with open(kb_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for "Recently Completed" section
        lines = content.split('\n')
        completed_tasks = []
        in_completed_section = False
        
        for line in lines:
            if line.strip().startswith("## Recently Completed"):
                in_completed_section = True
                continue
            elif line.startswith("##") and in_completed_section:
                break
            elif in_completed_section and line.strip().startswith("-"):
                # Parse completed task line
                task_line = line.strip()[1:].strip()  # Remove bullet point
                if " - Completed " in task_line:
                    parts = task_line.split(" - Completed ", 1)
                    if len(parts) == 2:
                        completed_tasks.append({
                            "name": parts[0].strip(),
                            "completed_date": parts[1].split(",")[0].strip(),
                            "notes": parts[1].split(",", 1)[1].strip() if "," in parts[1] else ""
                        })
        
        return completed_tasks
        
    except Exception as e:
        raise ValueError(f"Failed to parse completed tasks: {str(e)}")


async def get_wip_task_statistics() -> Dict[str, Any]:
    """
    [Function intent]
    Generate statistics about WIP tasks for project overview.
    
    [Design principles]
    Aggregate task data for project management insights.
    Useful metrics for tracking development progress.
    
    [Implementation details]
    Calculates various metrics from active and completed tasks.
    
    Returns:
        Dictionary with task statistics and metrics
        
    Raises:
        ValueError: When task statistics cannot be calculated
    """
    
    try:
        active_tasks = await get_active_wip_tasks_list()
        completed_tasks = await get_recently_completed_tasks()
        
        statistics = {
            "total_active": len(active_tasks),
            "total_completed": len(completed_tasks),
            "tasks_with_git_branch": len([t for t in active_tasks if t.get("git_branch") and t["git_branch"] != "Unknown"]),
            "tasks_with_progress": len([t for t in active_tasks if t.get("has_progress_file", False)]),
            "tasks_with_definition": len([t for t in active_tasks if t.get("has_task_file", False)]),
            "completion_rate": len(completed_tasks) / (len(active_tasks) + len(completed_tasks)) * 100 if (len(active_tasks) + len(completed_tasks)) > 0 else 0
        }
        
        return statistics
        
    except Exception as e:
        raise ValueError(f"Failed to calculate task statistics: {str(e)}")


async def load_wip_task_content(task_name: str) -> str:
    """
    [Function intent]
    Load WIP_TASK.md content for specified task.
    
    [Design principles]
    Direct file access for WIP task definition content.
    Graceful handling of missing task files with placeholder content.
    
    [Implementation details]
    Reads WIP_TASK.md from task directory, returns content or informative placeholder.
    
    Args:
        task_name: Name of the WIP task
        
    Returns:
        Content of WIP_TASK.md file or placeholder message
    """
    
    try:
        task_file = Path.cwd() / ".knowledge" / "work-in-progress" / task_name / "WIP_TASK.md"
        
        if task_file.exists():
            with open(task_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                return content if content else f"WIP_TASK.md exists but is empty for task: {task_name}"
        else:
            return f"**WIP_TASK.md not found for task: {task_name}**\n\nThis task may be incomplete or created outside the standard workflow."
            
    except Exception:
        return f"**Failed to load WIP_TASK.md for task: {task_name}**\n\nFile access error occurred during task loading."


async def load_wip_progress_content(task_name: str) -> str:
    """
    [Function intent]
    Load PROGRESS.md content for specified task.
    
    [Design principles]
    Direct file access for WIP task progress tracking content.
    Graceful handling of missing progress files with placeholder content.
    
    [Implementation details]
    Reads PROGRESS.md from task directory, returns content or informative placeholder.
    
    Args:
        task_name: Name of the WIP task
        
    Returns:
        Content of PROGRESS.md file or placeholder message
    """
    
    try:
        progress_file = Path.cwd() / ".knowledge" / "work-in-progress" / task_name / "PROGRESS.md"
        
        if progress_file.exists():
            with open(progress_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                return content if content else f"PROGRESS.md exists but is empty for task: {task_name}"
        else:
            return f"**PROGRESS.md not found for task: {task_name}**\n\nProgress tracking has not been initialized for this task."
            
    except Exception:
        return f"**Failed to load PROGRESS.md for task: {task_name}**\n\nFile access error occurred during progress loading."


async def get_task_status(task_name: str) -> str:
    """
    [Function intent]
    Extract task status from WIP_TASK.md or PROGRESS.md files.
    
    [Design principles]
    Parse task files for status information with fallback to "Unknown".
    Consistent status extraction across different task formats.
    
    [Implementation details]
    Searches task files for status indicators, returns parsed status or default.
    
    Args:
        task_name: Name of the WIP task
        
    Returns:
        Task status string or "Unknown" if not found
    """
    
    try:
        # Check WIP_TASK.md first
        task_file = Path.cwd() / ".knowledge" / "work-in-progress" / task_name / "WIP_TASK.md"
        if task_file.exists():
            with open(task_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Look for status patterns
                lines = content.split('\n')
                for line in lines:
                    if "**Status**:" in line or "Status:" in line:
                        return line.split(":", 1)[1].strip()
        
        # Check PROGRESS.md
        progress_file = Path.cwd() / ".knowledge" / "work-in-progress" / task_name / "PROGRESS.md"
        if progress_file.exists():
            with open(progress_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Look for status patterns
                lines = content.split('\n')
                for line in lines:
                    if "**Status**:" in line or "Status:" in line:
                        return line.split(":", 1)[1].strip()
        
        return "Unknown"
        
    except Exception:
        return "Unknown"


async def get_task_git_branch(task_name: str) -> str:
    """
    [Function intent]
    Extract Git branch information from task files.
    
    [Design principles]
    Parse task files for Git integration information with fallback.
    Support for various Git branch documentation formats.
    
    [Implementation details]
    Searches task files for Git branch references, returns branch name or default.
    
    Args:
        task_name: Name of the WIP task
        
    Returns:
        Git branch name or "Unknown" if not found
    """
    
    try:
        # Check WIP_TASK.md for Git integration section
        task_file = Path.cwd() / ".knowledge" / "work-in-progress" / task_name / "WIP_TASK.md"
        if task_file.exists():
            with open(task_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Look for Git branch patterns
                lines = content.split('\n')
                for line in lines:
                    if "**Branch**:" in line or "Git Branch:" in line or "Branch Name:" in line:
                        return line.split(":", 1)[1].strip()
        
        return "Unknown"
        
    except Exception:
        return "Unknown"


async def get_task_last_updated(task_name: str) -> str:
    """
    [Function intent]
    Get last modification time for task directory or files.
    
    [Design principles]
    File system based timestamp for task activity tracking.
    Fallback to directory modification time if files not available.
    
    [Implementation details]
    Checks modification times of task files, returns most recent in ISO format.
    
    Args:
        task_name: Name of the WIP task
        
    Returns:
        Last updated timestamp in ISO format or "Unknown"
    """
    
    try:
        task_dir = Path.cwd() / ".knowledge" / "work-in-progress" / task_name
        
        if not task_dir.exists():
            return "Unknown"
        
        # Get modification times of key files
        timestamps = []
        
        for file_name in ["WIP_TASK.md", "PROGRESS.md"]:
            file_path = task_dir / file_name
            if file_path.exists():
                timestamps.append(file_path.stat().st_mtime)
        
        # Fallback to directory modification time
        if not timestamps:
            timestamps.append(task_dir.stat().st_mtime)
        
        # Return most recent timestamp
        most_recent = max(timestamps)
        return datetime.fromtimestamp(most_recent).isoformat()
        
    except Exception:
        return "Unknown"

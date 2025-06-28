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
# Session management helper functions for JESSE Framework MCP Server,
# focusing on resource access logging and WIP task context utilities.
###############################################################################
# [Source file design principles]
# - Resource-focused logging for analytics and usage tracking
# - Simple WIP task context utilities for resource implementations
# - Lightweight operations without heavy session management overhead
###############################################################################
# [Source file constraints]
# - Must access .knowledge/work-in-progress/ directory structure
# - Resource logging requires .coding_assistant/jesse/ directory creation
# - FastMCP Context integration for async operations
###############################################################################
# [Dependencies]
# system:json - JSON handling for resource access logging
# system:datetime - Timestamp generation for resource access tracking
# system:pathlib.Path - Cross-platform filesystem operations
# system:fastmcp.Context - FastMCP Context for async operations
###############################################################################
# [GenAI tool change history]
# 2025-06-28T06:51:30Z : Removed tool-specific session management for resource-first architecture by CodeAssistant
# * Eliminated 7 tool-specific functions (prepare_session_context_async, validate directories, session logging variants)
# * Preserved 2 WIP task utilities useful for resource implementations
# * Added simplified log_resource_access function for resource analytics
# * Reduced file complexity by ~220 lines focusing on resource support only
# 2025-06-28T00:50:00Z : Added functions for single tool architecture support by CodeAssistant
# * Added generate_session_id() function for UUID-based session tracking
# * Added prepare_session_context_async() function for session context validation
# * Updated log_session_start_async() signature for single tool architecture compatibility
# * Added session context validation functions for resource-based architecture
# 2025-06-27T23:16:06Z : Removed non-async legacy functions by CodeAssistant
# * Removed sync versions of load_wip_task_context, get_current_wip_task_name, log_session_start
# * Simplified to async-only implementation with FastMCP Context integration
# * Removed logging dependency used only by sync functions
# 2025-06-27T20:28:53Z : Initial session management module creation by CodeAssistant
# * Extracted WIP task and session logging functions from main.py
# * Modularized session management functionality with async/sync support
###############################################################################

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastmcp import Context

# === WIP TASK UTILITIES FOR RESOURCE IMPLEMENTATIONS ===

async def load_wip_task_context_async(ctx: Context) -> str:
    """
    [Function intent]
    Load current WIP task context for resource implementations.
    
    [Design principles]
    Current task focus loading based on Essential Knowledge Base configuration.
    Uses Context for progress reporting and error logging.
    
    [Implementation details]
    Reads current task from KNOWLEDGE_BASE.md, loads corresponding WIP_TASK.md
    and PROGRESS.md files from work-in-progress directory.
    Reports progress during loading operations.
    
    Args:
        ctx: FastMCP Context for logging and progress reporting
        
    Returns:
        Current WIP task context or placeholder message
    """
    
    try:
        # First, determine current WIP task from knowledge base
        await ctx.info("Checking for current WIP task...")
        current_task = await get_current_wip_task_name_async(ctx)
        
        if not current_task:
            await ctx.info("No current WIP task configured")
            return "No current WIP task configured in project knowledge base."
        
        await ctx.info(f"Loading WIP task: {current_task}")
        
        # Load WIP task files
        wip_dir = Path(f".knowledge/work-in-progress/{current_task}")
        
        if not wip_dir.exists():
            await ctx.error(f"WIP task directory not found: {wip_dir}")
            return f"WIP task directory not found: {wip_dir}"
        
        wip_content_parts = []
        
        # Load WIP_TASK.md
        wip_task_file = wip_dir / "WIP_TASK.md"
        if wip_task_file.exists():
            await ctx.info(f"Loading WIP_TASK.md for {current_task}")
            with open(wip_task_file, "r", encoding="utf-8") as f:
                content = f.read()
                wip_content_parts.append(f"=== WIP TASK: {current_task.upper()} ===\n{content}")
        
        # Load PROGRESS.md
        progress_file = wip_dir / "PROGRESS.md"
        if progress_file.exists():
            await ctx.info(f"Loading PROGRESS.md for {current_task}")
            with open(progress_file, "r", encoding="utf-8") as f:
                content = f.read()
                wip_content_parts.append(f"=== WIP TASK PROGRESS: {current_task.upper()} ===\n{content}")
        
        if not wip_content_parts:
            await ctx.info(f"No WIP task files found in {wip_dir}")
            return f"No WIP task files found in {wip_dir}"
        
        await ctx.info(f"Successfully loaded WIP task context for {current_task}")
        return "\n\n".join(wip_content_parts)
        
    except Exception as e:
        await ctx.error(f"Failed to load WIP task context: {str(e)}")
        return f"WIP task context error: {str(e)}"


async def get_current_wip_task_name_async(ctx: Context) -> Optional[str]:
    """
    [Function intent]
    Extract current WIP task name for resource implementations.
    
    [Design principles]
    Simple parsing of knowledge base to identify active task.
    Uses Context for error reporting instead of logger warnings.
    
    [Implementation details]
    Scans KNOWLEDGE_BASE.md for "Current Work-in-Progress Task" section,
    extracts task name from "Active Task" field.
    
    Args:
        ctx: FastMCP Context for error reporting
        
    Returns:
        Current WIP task name if configured, None otherwise
    """
    
    try:
        knowledge_file = Path(".knowledge/persistent-knowledge/KNOWLEDGE_BASE.md")
        
        if not knowledge_file.exists():
            await ctx.info("Knowledge base file not found")
            return None
        
        with open(knowledge_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Simple parsing for current task (could be enhanced with regex)
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "**Active Task**:" in line:
                task_line = line.split("**Active Task**:")[-1].strip()
                if task_line and task_line.lower() != "none":
                    await ctx.info(f"Found current WIP task: {task_line}")
                    return task_line
        
        await ctx.info("No active WIP task found in knowledge base")
        return None
        
    except Exception as e:
        await ctx.error(f"Failed to get current WIP task name: {str(e)}")
        return None

# === RESOURCE ACCESS LOGGING ===

async def log_resource_access(resource_uri: str, ctx: Context) -> None:
    """
    [Function intent]
    Simple logging for resource access analytics and usage tracking.
    
    [Design principles]
    Lightweight resource access logging without session overhead.
    Privacy-conscious logging with no sensitive content capture.
    
    [Implementation details]
    Creates timestamped log entry for resource access patterns,
    helps track framework usage and resource popularity.
    
    Args:
        resource_uri: URI of the accessed resource
        ctx: FastMCP Context for logging
        
    Raises:
        None: Logging failure doesn't break resource access
    """
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "resource_access",
            "resource_uri": resource_uri
        }
        
        log_dir = Path(".coding_assistant/jesse")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / "resource_access.log"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
            
        await ctx.info(f"Resource access logged: {resource_uri}")
    except Exception as e:
        await ctx.error(f"Resource logging failed: {str(e)}")
        # Don't raise - logging failure shouldn't break resource access

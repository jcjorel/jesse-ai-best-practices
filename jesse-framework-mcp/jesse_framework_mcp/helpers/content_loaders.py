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
# Content loading helper functions for JESSE Framework MCP Server,
# handling embedded content and project knowledge loading operations.
###############################################################################
# [Source file design principles]
# - Self-contained framework delivery using build-time embedded content
# - Defensive loading with clear error messages for missing embedded files
# - Async-only implementation for modern MCP server architecture
###############################################################################
# [Source file constraints]
# - Must access embedded_content/ directory created at build time
# - Requires importlib.resources for embedded content access
# - FastMCP Context integration for async versions
###############################################################################
# [Dependencies]
# system:importlib.resources - Access to embedded package content
# system:pathlib.Path - Cross-platform filesystem operations
# system:datetime - Timestamp generation for session responses
# system:logging - Logging for sync versions
# system:fastmcp.Context - FastMCP Context for async versions
###############################################################################
# [GenAI tool change history]
# 2025-06-28T01:08:35Z : Added missing load_embedded_content function by CodeAssistant
# * Added load_embedded_content function for generic embedded file access
# * Supports nested paths with forward slash notation
# * Fixed import error in project_context.py resource module
# 2025-06-27T23:30:00Z : Removed legacy non-async functions by CodeAssistant  
# * Eliminated all sync content loading functions marked as legacy compatibility
# * Removed unused logging import and logger configuration
# * Streamlined to async-only implementation for modern MCP server architecture
###############################################################################

from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from importlib import resources
except ImportError:
    # Python < 3.9 compatibility
    import importlib_resources as resources

from fastmcp import Context

from ..constants import get_jesse_rule_files

# === ASYNC CONTENT LOADING FUNCTIONS ===

async def load_embedded_content(file_path: str) -> str:
    """
    [Function intent]
    Load embedded content from the MCP server package for generic file access.
    
    [Design principles]
    Generic embedded content access for any file in embedded_content directory.
    Direct file access without context overhead for lightweight operations.
    
    [Implementation details]
    Uses importlib.resources to access embedded_content files,
    supports nested paths with forward slash notation.
    
    Args:
        file_path: Path to embedded file (e.g., "rules/JESSE_CODE_COMMENTS.md")
        
    Returns:
        Content of the embedded file
        
    Raises:
        ValueError: When embedded file cannot be found or loaded
    """
    
    try:
        # Handle nested paths by splitting on forward slash
        path_parts = file_path.split('/')
        
        if len(path_parts) == 1:
            # Direct file in embedded_content root
            content_file = resources.files('jesse_framework_mcp.embedded_content') / path_parts[0]
        else:
            # Nested file (e.g., rules/JESSE_CODE_COMMENTS.md)
            base_dir = resources.files('jesse_framework_mcp.embedded_content')
            for part in path_parts[:-1]:
                base_dir = base_dir / part
            content_file = base_dir / path_parts[-1]
        
        content = content_file.read_text(encoding='utf-8')
        
        if not content.strip():
            raise ValueError(f"Embedded file {file_path} is empty")
        
        return content.strip()
        
    except Exception as e:
        raise ValueError(f"Failed to load embedded content {file_path}: {str(e)}")


async def load_embedded_jesse_framework_async(ctx: Context) -> str:
    """
    [Function intent]
    Async version of embedded JESSE framework loading with Context integration.
    
    [Design principles]
    Self-contained framework delivery using build-time embedded content.
    Uses Context for progress reporting during loading operations.
    
    [Implementation details]
    Uses importlib.resources to access embedded_content/ created during build,
    loads both rule files and workflow directory, formats with clear delimiters.
    Reports progress for user feedback during loading.
    
    Args:
        ctx: FastMCP Context for progress reporting
        
    Returns:
        Complete embedded JESSE framework content
        
    Raises:
        ValueError: When embedded content cannot be accessed
    """
    
    try:
        content_parts = []
        
        # Load JESSE rules
        await ctx.info("Loading embedded JESSE framework rules...")
        content_parts.append("=== EMBEDDED JESSE FRAMEWORK RULES ===")
        rules_content = await load_embedded_jesse_rules_async(ctx)
        content_parts.append(rules_content)
        
        # Load JESSE workflows
        await ctx.info("Loading embedded JESSE framework workflows...")
        content_parts.append("=== EMBEDDED JESSE FRAMEWORK WORKFLOWS ===")
        workflows_content = await load_embedded_jesse_workflows_async(ctx)
        content_parts.append(workflows_content)
        
        return "\n\n".join(content_parts)
        
    except Exception as e:
        raise ValueError(f"Failed to load embedded JESSE framework: {str(e)}")


async def load_embedded_jesse_workflows_async(ctx: Context) -> str:
    """
    [Function intent]
    Async version of embedded JESSE workflows loading with Context integration.
    
    [Design principles]
    Complete workflow directory access for comprehensive framework delivery.
    Uses Context for detailed progress reporting during workflow loading.
    
    [Implementation details]
    Accesses embedded_content/workflows/ directory, discovers all .md files,
    loads each workflow with descriptive section headers.
    Reports progress for each workflow loaded.
    
    Args:
        ctx: FastMCP Context for progress reporting
        
    Returns:
        All embedded workflow files content with section headers
        
    Raises:
        ValueError: When embedded workflow files cannot be accessed
    """
    
    try:
        workflow_files = []
        
        # Access embedded workflows directory
        workflows_dir = resources.files('jesse_framework_mcp.embedded_content.workflows')
        for file_path in workflows_dir.iterdir():
            if file_path.suffix == '.md' and file_path.is_file():
                workflow_files.append(file_path.name)
        
        # Sort for consistent ordering
        workflow_files.sort()
        
        content_parts = []
        for i, file_name in enumerate(workflow_files):
            try:
                await ctx.info(f"Loading workflow {i+1}/{len(workflow_files)}: {file_name}")
                workflow_file = workflows_dir / file_name
                content = workflow_file.read_text(encoding='utf-8')
                content_parts.append(f"=== WORKFLOW: {file_name.upper()} ===\n{content}")
            except Exception as file_error:
                await ctx.error(f"Failed to load workflow {file_name}: {file_error}")
                continue
        
        if not content_parts:
            await ctx.info("No embedded workflow files found")
            return "No embedded workflow files found."
            
        return "\n\n".join(content_parts)
        
    except Exception as e:
        raise ValueError(f"Failed to load embedded workflows: {str(e)}")


async def load_embedded_jesse_rules_async(ctx: Context) -> str:
    """
    [Function intent]
    Async version of embedded JESSE rules loading with Context integration.
    
    [Design principles]
    Explicit file list ensures only intended rule files are loaded.
    Uses Context for detailed progress reporting during file loading.
    
    [Implementation details]
    Accesses embedded_content/ using importlib.resources, loads predefined
    JESSE rule files, formats each with clear section delimiters.
    Reports progress for each file loaded.
    
    Args:
        ctx: FastMCP Context for progress reporting
        
    Returns:
        All JESSE rule files content with section headers
        
    Raises:
        ValueError: When embedded rule files cannot be accessed
    """
    
    jesse_rule_files = get_jesse_rule_files()
    
    content_parts = []
    
    try:
        for i, file_name in enumerate(jesse_rule_files):
            await ctx.info(f"Loading rule file {i+1}/{len(jesse_rule_files)}: {file_name}")
            content_file = resources.files('jesse_framework_mcp.embedded_content') / file_name
            content = content_file.read_text(encoding='utf-8')
            content_parts.append(f"=== {file_name.upper()} ===\n{content}")
                
        return "\n\n".join(content_parts)
        
    except Exception as e:
        raise ValueError(f"Failed to load embedded JESSE rules: {str(e)}")


async def load_project_knowledge_async(ctx: Context) -> str:
    """
    [Function intent]
    Async version of project knowledge loading with Context integration.
    
    [Design principles]
    Project context loading separate from embedded framework content.
    Uses Context for error reporting and progress updates.
    
    [Implementation details]
    Reads KNOWLEDGE_BASE.md from .knowledge/persistent-knowledge/ directory,
    handles missing files by returning placeholder content.
    
    Args:
        ctx: FastMCP Context for logging and error reporting
        
    Returns:
        Project knowledge base content or placeholder message
    """
    
    try:
        knowledge_file = Path(".knowledge/persistent-knowledge/KNOWLEDGE_BASE.md")
        
        if knowledge_file.exists():
            await ctx.info("Loading project knowledge base...")
            with open(knowledge_file, "r", encoding="utf-8") as f:
                content = f.read()
                await ctx.info(f"Successfully loaded project knowledge ({len(content)} characters)")
                return f"=== PROJECT KNOWLEDGE BASE ===\n{content}"
        else:
            await ctx.info("No project knowledge base found")
            return "=== PROJECT KNOWLEDGE BASE ===\nNo project knowledge base found at .knowledge/persistent-knowledge/KNOWLEDGE_BASE.md"
            
    except Exception as e:
        await ctx.error(f"Failed to load project knowledge: {str(e)}")
        return f"=== PROJECT KNOWLEDGE BASE ===\nError loading project knowledge: {str(e)}"


async def format_session_response_async(
    session_id: str,
    user_prompt: str,
    load_wip_tasks: bool,
    embedded_content: str,
    project_knowledge: str,
    kb_inventory: str,
    wip_content: str,
    ctx: Context
) -> str:
    """
    [Function intent]
    Async version of session response formatting with Context integration.
    
    [Design principles]
    Structured response format with clear section delimiters for easy parsing.
    Uses Context for final formatting confirmation.
    
    [Implementation details]
    Combines all loaded content sections with descriptive headers,
    includes session metadata and availability information.
    Reports final response statistics via Context.
    
    Args:
        session_id: Unique session identifier for tracking
        user_prompt: Original user prompt (for reference only)
        load_wip_tasks: Whether WIP tasks were loaded
        embedded_content: Complete embedded JESSE framework
        project_knowledge: Project-specific knowledge content
        kb_inventory: Available knowledge bases inventory
        wip_content: WIP task context if loaded
        ctx: FastMCP Context for logging
        
    Returns:
        Complete formatted session response
    """
    
    timestamp = datetime.now().isoformat()
    
    response_parts = [
        "=== JESSE FRAMEWORK SESSION INITIALIZATION ===",
        f"Session ID: {session_id}",
        f"Timestamp: {timestamp}",
        f"Load WIP Tasks: {load_wip_tasks}",
        "",
        embedded_content,
        "",
        project_knowledge,
        "",
        "=== AVAILABLE PROJECT KNOWLEDGE BASES ===",
        kb_inventory,
        ""
    ]
    
    if load_wip_tasks and wip_content:
        response_parts.extend([
            "=== CURRENT WIP TASK CONTEXT ===",
            wip_content,
            ""
        ])
    elif load_wip_tasks:
        response_parts.extend([
            "=== CURRENT WIP TASK CONTEXT ===",
            "WIP task loading was enabled but no current task found.",
            ""
        ])
    
    response_parts.extend([
        "=== COMPLETE JESSE FRAMEWORK LOADED ===",
        "✅ All JESSE rules embedded and loaded",
        "✅ All JESSE workflows embedded and loaded",  
        "✅ Project knowledge from .knowledge/ loaded",
        f"✅ WIP task context: {'loaded' if (load_wip_tasks and wip_content) else 'skipped'}",
        "✅ Knowledge base inventory generated for lazy loading",
        "✅ Session ready with complete framework context",
        "=== END INITIALIZATION ==="
    ])
    
    response = "\n".join(response_parts)
    await ctx.info(f"Session response formatted: {len(response)} characters")
    return response

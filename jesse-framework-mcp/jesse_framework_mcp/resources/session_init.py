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
# Session initialization meta-resource for JESSE Framework MCP server providing
# comprehensive Cline session context through combined multi-section HTTP response.
# Delivers all essential resources needed for productive JESSE Framework development.
###############################################################################
# [Source file design principles]
# - Single comprehensive resource for session initialization efficiency
# - Multi-section HTTP response combining all essential contexts
# - Sequential loading with progress reporting for transparency
# - Graceful error handling with individual section failure isolation
# - Maintains existing criticality levels and HTTP formatting patterns
# - Optimized for Cline session startup and development context
###############################################################################
# [Source file constraints]
# - Must maintain byte-perfect HTTP formatting for all included sections
# - Individual section failures must not break entire resource loading
# - Progress reporting must be accurate and informative throughout process
# - Resource size must be manageable while providing comprehensive context
# - All existing resource handler patterns and APIs must be preserved
###############################################################################
# [Dependencies]
# codebase:jesse_framework_mcp.main.server - FastMCP server instance
# codebase:jesse_framework_mcp.helpers.http_formatter - Multi-section HTTP formatting
# codebase:jesse_framework_mcp.resources.framework_rules - Individual JESSE rules
# codebase:jesse_framework_mcp.resources.project_resources - Project context resources
# codebase:jesse_framework_mcp.resources.wip_tasks - WIP task inventory
# codebase:jesse_framework_mcp.resources.knowledge - Knowledge base indexes
# codebase:jesse_framework_mcp.resources.workflows - Workflow catalog functions
# system:fastmcp.Context - Progress reporting and logging
###############################################################################
# [GenAI tool change history]
# 2025-06-28T08:12:00Z : Initial session initialization meta-resource implementation by CodeAssistant
# * Created comprehensive jesse://session/init-context resource with 7 HTTP sections
# * Implemented sequential loading: Framework Rules → Project Context → WIP Tasks → Workflows → Knowledge → Gitignore
# * Added graceful error handling with individual section failure isolation
# * Established progress reporting throughout multi-section loading process
###############################################################################

import json
from datetime import datetime
from typing import List, Dict, Any

from fastmcp import Context
from ..main import server
from ..helpers.http_formatter import (
    format_multi_section_response, 
    format_http_section, 
    ContentCriticality, 
    HttpPath,
    extract_http_sections_from_multi_response
)
from ..helpers.path_utils import get_project_root
from ..helpers.project_setup import get_project_setup_guidance
from .framework_rules import get_rule_by_name, get_available_rule_names
from .project_resources import get_project_context_summary, get_project_knowledge
from .gitignore import get_project_gitignore_files, get_gitignore_compliance_status
from .knowledge import get_git_clones_readme, get_pdf_knowledge_readme
from .workflows import get_embedded_workflow_files, get_workflow_description, get_workflow_category
from .wip_tasks import get_wip_tasks_inventory

# Import the FastMCP function unwrapper utility
import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils import unwrap_fastmcp_function


@server.resource("jesse://session/init-context")
async def get_session_init_context(ctx: Context) -> str:
    """
    [Function intent]
    Comprehensive session initialization meta-resource combining all essential contexts.
    Provides complete JESSE Framework development context in single multi-section HTTP response.
    
    [Design principles]
    Sequential loading of essential resources with transparent progress reporting.
    Individual section failure isolation prevents complete session initialization failure.
    Multi-section HTTP response maintains existing formatting and criticality patterns.
    Project root detection ensures resources work regardless of MCP server launch method.
    
    [Implementation details]
    Checks project root availability first, returns setup guidance if missing.
    Loads 7 distinct resource sections: Framework Rules, Project Context, WIP Tasks,
    Workflow Index, Knowledge Indexes, and Gitignore Files. Uses comprehensive error
    handling and progress reporting throughout the multi-section loading process.
    
    Args:
        ctx: FastMCP Context for progress reporting and logging
        
    Returns:
        Multi-section HTTP response with complete session initialization context
        
    Raises:
        ValueError: When critical sections fail and session context cannot be established
    """
    
    await ctx.info("Starting comprehensive session initialization...")
    
    # === PROJECT ROOT DETECTION ===
    await ctx.info("Detecting project root...")
    project_root = get_project_root()
    
    if not project_root:
        await ctx.error("No JESSE Framework project root detected")
        return get_project_setup_guidance()
    
    await ctx.info(f"Project root detected: {project_root}")
    
    # Set working directory to project root for all subsequent operations
    original_cwd = os.getcwd()
    try:
        os.chdir(project_root)
        await ctx.info(f"Working directory set to project root: {project_root}")
    except Exception as e:
        await ctx.error(f"Failed to change to project root directory: {str(e)}")
        return get_project_setup_guidance()
    sections = []
    total_sections = 7
    current_section = 0
    
    try:
        # === SECTION 1: JESSE FRAMEWORK RULES (CRITICAL) ===
        current_section += 1
        await ctx.report_progress((current_section - 1) * 100 // total_sections, 100, f"Loading JESSE Framework Rules ({current_section}/{total_sections})")
        
        try:
            framework_rules_sections = await load_framework_rules_sections(ctx)
            sections.extend(framework_rules_sections)
            await ctx.info(f"✓ Loaded {len(framework_rules_sections)} JESSE Framework Rules")
        except Exception as e:
            await ctx.error(f"Failed to load Framework Rules: {str(e)}")
            # Framework rules are CRITICAL - add error section but continue
            error_section = create_error_section("JESSE Framework Rules", str(e), ContentCriticality.CRITICAL)
            sections.append(error_section)
        
        # === SECTION 2: PROJECT CONTEXT SUMMARY ===
        current_section += 1
        await ctx.report_progress((current_section - 1) * 100 // total_sections, 100, f"Loading Project Context ({current_section}/{total_sections})")
        
        try:
            # Unwrap FastMCP function before calling
            project_context_func = unwrap_fastmcp_function(get_project_context_summary)
            project_context = await project_context_func(ctx)
            sections.append(project_context)
            await ctx.info("✓ Loaded Project Context Summary")
        except Exception as e:
            await ctx.error(f"Failed to load Project Context: {str(e)}")
            error_section = create_error_section("Project Context Summary", str(e), ContentCriticality.INFORMATIONAL)
            sections.append(error_section)
        
        # === SECTION 3: PROJECT KNOWLEDGE BASE ===
        current_section += 1
        await ctx.report_progress((current_section - 1) * 100 // total_sections, 100, f"Loading Project Knowledge ({current_section}/{total_sections})")
        
        try:
            # Unwrap FastMCP function before calling
            project_knowledge_func = unwrap_fastmcp_function(get_project_knowledge)
            project_knowledge = await project_knowledge_func(ctx)
            sections.append(project_knowledge)
            await ctx.info("✓ Loaded Project Knowledge Base")
        except Exception as e:
            await ctx.error(f"Failed to load Project Knowledge: {str(e)}")
            error_section = create_error_section("Project Knowledge Base", str(e), ContentCriticality.INFORMATIONAL)
            sections.append(error_section)
        
        # === SECTION 4: WIP TASKS INVENTORY ===
        current_section += 1
        await ctx.report_progress((current_section - 1) * 100 // total_sections, 100, f"Loading WIP Tasks ({current_section}/{total_sections})")
        
        try:
            # Unwrap FastMCP function before calling
            wip_tasks_func = unwrap_fastmcp_function(get_wip_tasks_inventory)
            wip_tasks = await wip_tasks_func(ctx)
            sections.append(wip_tasks)
            await ctx.info("✓ Loaded WIP Tasks Inventory")
        except Exception as e:
            await ctx.error(f"Failed to load WIP Tasks: {str(e)}")
            error_section = create_error_section("WIP Tasks Inventory", str(e), ContentCriticality.INFORMATIONAL)
            sections.append(error_section)
        
        # === SECTION 5: AVAILABLE WORKFLOWS INDEX ===
        current_section += 1
        await ctx.report_progress((current_section - 1) * 100 // total_sections, 100, f"Loading Workflows Index ({current_section}/{total_sections})")
        
        try:
            workflows_index = await create_workflows_index_section(ctx)
            sections.append(workflows_index)
            await ctx.info("✓ Loaded Available Workflows Index")
        except Exception as e:
            await ctx.error(f"Failed to load Workflows Index: {str(e)}")
            error_section = create_error_section("Available Workflows Index", str(e), ContentCriticality.INFORMATIONAL)
            sections.append(error_section)
        
        # === SECTION 6: KNOWLEDGE BASE INDEXES ===
        current_section += 1
        await ctx.report_progress((current_section - 1) * 100 // total_sections, 100, f"Loading Knowledge Indexes ({current_section}/{total_sections})")
        
        try:
            knowledge_sections = await load_knowledge_indexes_sections(ctx)
            sections.extend(knowledge_sections)
            await ctx.info(f"✓ Loaded {len(knowledge_sections)} Knowledge Base Indexes")
        except Exception as e:
            await ctx.error(f"Failed to load Knowledge Indexes: {str(e)}")
            error_section = create_error_section("Knowledge Base Indexes", str(e), ContentCriticality.INFORMATIONAL)
            sections.append(error_section)
        
        # === SECTION 7: GITIGNORE COMPLIANCE (CONDITIONAL) ===
        current_section += 1
        await ctx.report_progress((current_section - 1) * 100 // total_sections, 100, f"Checking Gitignore Compliance ({current_section}/{total_sections})")
        
        try:
            # Use smart compliance checking - only outputs when issues need attention
            compliance_func = unwrap_fastmcp_function(get_gitignore_compliance_status)
            compliance_response = await compliance_func(ctx)
            
            # Only add section if there are compliance issues to address
            if compliance_response.strip():  # Non-empty response means issues found
                # Extract clean HTTP sections without how_to wrapper
                clean_sections, preambule = extract_http_sections_from_multi_response(compliance_response)
                sections.append(clean_sections)
                await ctx.info("⚠️ Gitignore compliance issues found - guidance included")
            else:
                await ctx.info("✓ Gitignore compliance verified - no issues")
                # Major context reduction: no section added when compliant
        except Exception as e:
            await ctx.error(f"Failed to check Gitignore Compliance: {str(e)}")
            # Fallback to traditional gitignore files display on compliance check failure
            try:
                gitignore_func = unwrap_fastmcp_function(get_project_gitignore_files)
                gitignore_response = await gitignore_func(ctx)
                # Extract clean HTTP sections without how_to wrapper
                clean_sections, preambule = extract_http_sections_from_multi_response(gitignore_response)
                sections.append(clean_sections)
                await ctx.info("✓ Fallback: Loaded Project Gitignore Files")
            except Exception as fallback_error:
                await ctx.error(f"Fallback also failed: {str(fallback_error)}")
                error_section = create_error_section("Gitignore Compliance & Files", f"Primary: {str(e)}, Fallback: {str(fallback_error)}", ContentCriticality.INFORMATIONAL)
                sections.append(error_section)
        
        # === FINALIZE MULTI-SECTION RESPONSE ===
        await ctx.report_progress(100, 100, "Finalizing session initialization context...")
        
        if not sections:
            raise ValueError("No sections were successfully loaded for session initialization")
        
        # Combine all sections into comprehensive response
        session_context = format_multi_section_response(*sections)
        
        await ctx.info(f"✓ Session initialization complete: {len(sections)} sections loaded")
        return session_context
        
    except Exception as e:
        error_msg = f"Critical failure in session initialization: {str(e)}"
        await ctx.error(error_msg)
        raise ValueError(error_msg)
    
    finally:
        # Restore original working directory
        try:
            os.chdir(original_cwd)
            await ctx.info("Restored original working directory")
        except Exception as e:
            await ctx.warning(f"Failed to restore original working directory: {str(e)}")


async def load_framework_rules_sections(ctx: Context) -> List[str]:
    """
    [Function intent]
    Load all 6 JESSE Framework Rules as individual HTTP sections.
    
    [Design principles]
    Maintains CRITICAL criticality for all framework rules.
    Individual rule loading with failure isolation per rule.
    
    [Implementation details]
    Iterates through available rule names, loads each rule via existing handlers,
    collects successful loads and reports individual failures.
    
    Args:
        ctx: FastMCP Context for progress reporting and logging
        
    Returns:
        List of HTTP-formatted framework rule sections
        
    Raises:
        Exception: When no framework rules can be loaded successfully
    """
    
    await ctx.info("Loading individual JESSE Framework Rules...")
    
    rule_sections = []
    rule_names = await get_available_rule_names()
    
    # Preferred logical order for framework rules
    preferred_order = [
        'knowledge_management',
        'hints', 
        'code_generation',
        'code_comments',
        'markdown',
        'scratchpad'
    ]
    
    # Reorder rule names according to preferred logical sequence
    ordered_rules = []
    for rule in preferred_order:
        if rule in rule_names:
            ordered_rules.append(rule)
    
    # Add any additional rules not in preferred order
    for rule in rule_names:
        if rule not in ordered_rules:
            ordered_rules.append(rule)
    
    # Load each rule individually
    for rule_name in ordered_rules:
        try:
            rule_section = await get_rule_by_name(rule_name, ctx)
            rule_sections.append(rule_section)
            await ctx.info(f"✓ Loaded JESSE rule: {rule_name}")
        except Exception as e:
            await ctx.error(f"Failed to load JESSE rule {rule_name}: {str(e)}")
            # Add error section for failed rule
            error_section = create_error_section(f"JESSE Rule: {rule_name}", str(e), ContentCriticality.CRITICAL)
            rule_sections.append(error_section)
    
    if not rule_sections:
        raise Exception("No JESSE Framework Rules could be loaded")
    
    return rule_sections


async def create_workflows_index_section(ctx: Context) -> str:
    """
    [Function intent]
    Create workflows index section with catalog of available JESSE workflows.
    
    [Design principles]
    Workflow catalog only (not full content) for manageable resource size.
    Categorized workflow organization for easy discovery and access.
    
    [Implementation details]
    Scans embedded workflows, builds structured catalog with descriptions,
    categories, and access URIs for Cline slash command integration.
    
    Args:
        ctx: FastMCP Context for progress reporting and logging
        
    Returns:
        HTTP-formatted workflows index section
        
    Raises:
        Exception: When workflows index cannot be created
    """
    
    await ctx.info("Building workflows index catalog...")
    
    try:
        # Get available workflow files
        workflow_files = await get_embedded_workflow_files()
        
        # Build workflow catalog
        workflows_by_category = {}
        
        for workflow_file in workflow_files:
            category = get_workflow_category(workflow_file)
            description = get_workflow_description(workflow_file)
            
            # Clean name for slash command
            clean_name = workflow_file.replace('.md', '') if workflow_file.endswith('.md') else workflow_file
            
            workflow_info = {
                "file": workflow_file,
                "description": description,
                "slash_command": f"/{clean_name}",
                "resource_uri": f"file://workflows/{workflow_file}"
            }
            
            if category not in workflows_by_category:
                workflows_by_category[category] = []
            
            workflows_by_category[category].append(workflow_info)
        
        # Build markdown catalog content
        catalog_lines = [
            "# JESSE Framework Workflows Index",
            "",
            f"**Total Available Workflows**: {len(workflow_files)}",
            f"**Generated**: {datetime.now().isoformat()}",
            "",
            "## Workflow Categories",
            ""
        ]
        
        # Add categorized workflows
        for category, workflows in sorted(workflows_by_category.items()):
            catalog_lines.append(f"### {category}")
            catalog_lines.append("")
            
            for workflow in workflows:
                catalog_lines.append(f"- **{workflow['slash_command']}** - {workflow['description']}")
                catalog_lines.append(f"  - File: `{workflow['file']}`")
                catalog_lines.append(f"  - Resource: `{workflow['resource_uri']}`")
                catalog_lines.append("")
        
        # Add usage instructions
        catalog_lines.extend([
            "## Usage Instructions",
            "",
            "### In Cline Chat",
            "Use workflows as slash commands:",
            "```",
            "/jesse_wip_task_create",
            "/jesse_capture_our_chat", 
            "```",
            "",
            "### Via MCP Resource",
            "Access individual workflows:",
            "```",
            "file://workflows/jesse_wip_task_create.md",
            "file://workflows/jesse_capture_our_chat.md",
            "```",
            ""
        ])
        
        catalog_content = "\n".join(catalog_lines)
        
        # Format as HTTP section
        return format_http_section(
            content=catalog_content,
            content_type="text/markdown",
            criticality=ContentCriticality.INFORMATIONAL,
            description="JESSE Framework Workflows Index and Catalog",
            section_type="workflows-index",
            location="file://{CLINE_WORKFLOWS}/",
            additional_headers={
                "Workflows-Count": str(len(workflow_files)),
                "Categories-Count": str(len(workflows_by_category)),
                "Generated": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        await ctx.error(f"Failed to create workflows index: {str(e)}")
        raise Exception(f"Workflows index creation failed: {str(e)}")


async def load_knowledge_indexes_sections(ctx: Context) -> List[str]:
    """
    [Function intent]
    Load knowledge base index sections for external resource access.
    
    [Design principles]
    Supports lazy loading strategy by providing index access.
    Individual index loading with failure isolation per knowledge type.
    
    [Implementation details]
    Loads git-clones and pdf-knowledge README indexes,
    handles missing knowledge directories gracefully.
    
    Args:
        ctx: FastMCP Context for progress reporting and logging
        
    Returns:
        List of HTTP-formatted knowledge index sections
        
    Raises:
        Exception: When no knowledge indexes can be loaded
    """
    
    await ctx.info("Loading knowledge base indexes...")
    
    knowledge_sections = []
    
    # Load git clones README index
    try:
        # These are already unwrapped functions (not decorated with FastMCP)
        git_clones_readme = await get_git_clones_readme(ctx)
        knowledge_sections.append(git_clones_readme)
        await ctx.info("✓ Loaded git clones README index")
    except Exception as e:
        await ctx.error(f"Failed to load git clones README: {str(e)}")
        error_section = create_error_section("Git Clones Knowledge Index", str(e), ContentCriticality.INFORMATIONAL)
        knowledge_sections.append(error_section)
    
    # Load PDF knowledge README index
    try:
        # These are already unwrapped functions (not decorated with FastMCP)
        pdf_knowledge_readme = await get_pdf_knowledge_readme(ctx)
        knowledge_sections.append(pdf_knowledge_readme)
        await ctx.info("✓ Loaded PDF knowledge README index")
    except Exception as e:
        await ctx.error(f"Failed to load PDF knowledge README: {str(e)}")
        error_section = create_error_section("PDF Knowledge Index", str(e), ContentCriticality.INFORMATIONAL)
        knowledge_sections.append(error_section)
    
    if not knowledge_sections:
        raise Exception("No knowledge indexes could be loaded")
    
    return knowledge_sections


def create_error_section(section_name: str, error_message: str, criticality: ContentCriticality) -> str:
    """
    [Function intent]
    Create error section for failed resource loading with appropriate metadata.
    
    [Design principles]
    Consistent error reporting format across all section types.
    Maintains criticality level of failed section for proper context.
    
    [Implementation details]
    Formats error information as HTTP section with error-specific headers
    and descriptive content for debugging and user awareness.
    
    Args:
        section_name: Name of the failed section
        error_message: Detailed error message
        criticality: Criticality level of the failed section
        
    Returns:
        HTTP-formatted error section
    """
    
    error_content = f"""# Error Loading {section_name}

**Error Type**: Resource Loading Failure  
**Error Message**: {error_message}  
**Timestamp**: {datetime.now().isoformat()}

This section failed to load during session initialization. The error has been logged and other sections may still be available.

## Troubleshooting
1. Check file permissions and path accessibility
2. Verify resource dependencies are available
3. Review MCP server logs for detailed error information
4. Try reloading the session initialization resource
"""
    
    return format_http_section(
        content=error_content,
        content_type="text/markdown",
        criticality=criticality,
        description=f"Error Loading {section_name}",
        section_type="error-section",
        location="error://session-init/",
        additional_headers={
            "Error-Section": section_name,
            "Error-Type": "ResourceLoadingFailure",
            "Error-Timestamp": datetime.now().isoformat()
        }
    )


def register_session_init_resources():
    """
    [Function intent]
    Register session initialization meta-resource with the server.
    
    [Design principles]
    FastMCP auto-registration through decorators for modern transport.
    Manual registration function for compatibility with existing patterns.
    
    [Implementation details]
    Resource is auto-registered via @server.resource decorator.
    This function provides explicit registration point if needed.
    """
    # Resource auto-registers via FastMCP decorator
    # This function exists for explicit registration compatibility
    pass

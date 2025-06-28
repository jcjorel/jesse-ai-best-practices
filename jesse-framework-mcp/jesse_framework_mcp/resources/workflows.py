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
# JESSE Framework workflow resource handlers for MCP server providing individual
# JESSE workflow files as HTTP-formatted resources for Cline slash command integration.
# Each workflow becomes accessible as a Cline slash command through resource delivery.
###############################################################################
# [Source file design principles]
# Resource-based workflow access with standardized HTTP formatting for Cline integration
# All workflows classified as CRITICAL content for strict adherence by AI assistants
# Workflow categorization and metadata for enhanced organization and discovery
# Portable file paths and extensible header system for future enhancements
###############################################################################
# [Source file constraints]
# Must maintain byte-perfect HTTP formatting for all workflow content sections
# All workflows must be classified as CRITICAL criticality for AI assistant enforcement
# Resource loading must handle missing workflows gracefully with descriptive errors
# Cline slash command headers must be accurate for proper integration
###############################################################################
# [Dependencies]
# system:importlib.resources - Access to embedded package content
# system:fastmcp.FastMCP - FastMCP server instance and Context
# codebase:../main - FastMCP server instance
###############################################################################
# [GenAI tool change history]
# 2025-06-28T07:34:00Z : Updated to use new HttpFile-based API with writable flags by CodeAssistant
# * Added HttpPath import for new HTTP formatter API compatibility
# * Added writable=False parameter to format_http_section call for readonly workflows
# * Enhanced HTTP formatting with Content-Writable headers for Cline integration
# * Maintained CRITICAL criticality and existing functionality while modernizing API usage
# 2025-06-28T01:28:00Z : Fixed MCP protocol compliance for Cline slash command integration by CodeAssistant
# * Added resources/list request handler for workflow discovery (CRITICAL fix)
# * Updated URI pattern from workflow:// to file://workflows/ for Cline compatibility
# * Added get_embedded_workflow_files() function for dynamic workflow discovery
# * Implemented proper MCP protocol patterns for slash command integration
# 2025-06-28T00:36:03Z : Updated workflows to HTTP formatting for Cline integration by CodeAssistant
# * Added HTTP formatting for all workflow resources with CRITICAL criticality
# * Implemented Cline slash command compatibility with metadata headers
# * Added workflow categorization and description mapping
# * Changed resource URI pattern to workflow:// for Cline integration
###############################################################################

try:
    from importlib import resources
except ImportError:
    # Python < 3.9 compatibility
    import importlib_resources as resources

from fastmcp import Context
from ..helpers.http_formatter import format_http_section, ContentCriticality, HttpPath

async def get_embedded_workflow_files() -> list[str]:
    """
    [Function intent]
    Get list of embedded workflow files for resource discovery.
    
    [Design principles]
    Dynamic workflow discovery from embedded content directory.
    Consistent workflow file pattern recognition for .md files.
    
    [Implementation details]
    Scans embedded workflows directory and returns list of .md workflow files
    for Cline slash command integration and resource listing.
    
    Returns:
        List of workflow filenames ending with .md
        
    Raises:
        Exception: When workflow files cannot be accessed from embedded content
    """
    try:
        workflows_dir = resources.files('jesse_framework_mcp.embedded_content.workflows')
        return [f.name for f in workflows_dir.iterdir() if f.suffix == '.md']
    except Exception as e:
        raise Exception(f"Failed to get embedded workflow files: {str(e)}")

def register_workflows_resources():
    """
    [Function intent]
    Register workflow resources with HTTP formatting for Cline slash command integration.
    
    [Design principles]
    Standard MCP protocol implementation for workflow discovery and access.  
    Clear separation of resource listing from individual resource content delivery.
    
    [Implementation details]
    Implements MCP resources/list and resources/read endpoints for Cline integration.
    Individual workflow resources accessible via file://workflows/ URIs.
    """
    from ..main import server
    
    @server.resource("file://workflows/{workflow_name}")
    async def get_jesse_workflow(workflow_name: str, ctx: Context) -> str:
        """
        [Function intent]
        Provide individual JESSE workflow files in HTTP format for Cline slash commands.
        Each workflow becomes a Cline slash command through resource integration.
        
        [Design principles]
        HTTP-formatted workflow delivery for consistent Cline integration.
        All workflows classified as CRITICAL for strict adherence by AI assistants.
        Workflow metadata and categorization for enhanced organization.
        
        [Implementation details]
        Loads workflow from embedded content, applies HTTP formatting with
        CRITICAL criticality and workflow-specific metadata for Cline integration.
        
        Args:
            workflow_name: Workflow name (with or without .md extension)
            ctx: FastMCP Context for logging and progress reporting
            
        Returns:
            HTTP-formatted workflow content ready for Cline slash command usage
            
        Raises:
            ValueError: When workflow file cannot be found or loaded
        """
        
        # Ensure .md extension for file loading
        workflow_file = workflow_name if workflow_name.endswith('.md') else f"{workflow_name}.md"
        # Clean name for slash command (remove .md extension)
        clean_name = workflow_name.replace('.md', '') if workflow_name.endswith('.md') else workflow_name
        
        await ctx.info(f"Loading JESSE workflow: {workflow_file}")
        
        try:
            # Load workflow content from embedded files
            with resources.open_text('jesse_framework_mcp.embedded_content.workflows', workflow_file) as f:
                workflow_content = f.read()
            
            if not workflow_content.strip():
                raise ValueError(f"Workflow file {workflow_file} is empty or contains only whitespace")
            
            # Get workflow description and category
            description = get_workflow_description(workflow_file)
            category = get_workflow_category(workflow_file)
            
            # Format as HTTP section for Cline integration
            formatted_workflow = format_http_section(
                content=workflow_content.strip(),
                content_type="text/markdown",
                criticality=ContentCriticality.CRITICAL,
                description=description,
                section_type="workflow",
                location=f"file://{{CLINE_WORKFLOWS}}/{workflow_file}",
                additional_headers={
                    "Cline-Slash-Command": f"/{clean_name}",
                    "Workflow-Category": category,
                    "Workflow-File": workflow_file
                },
                writable=False
            )
            
            await ctx.info(f"Workflow loaded: {len(workflow_content)} characters, formatted for Cline")
            return formatted_workflow
            
        except Exception as e:
            error_msg = f"Failed to load JESSE workflow {workflow_file}: {str(e)}"
            await ctx.error(error_msg)
            raise ValueError(error_msg)


def get_workflow_description(workflow_file: str) -> str:
    """
    [Function intent]
    Get human-readable description for JESSE workflow file.
    
    [Design principles]
    Centralized mapping of workflow files to user-friendly descriptions.
    Fallback to generic description for unknown workflow files.
    
    [Implementation details]
    Uses dictionary lookup with pattern matching for workflow descriptions.
    
    Args:
        workflow_file: Name of the JESSE workflow file
        
    Returns:
        Human-readable description of the workflow purpose
    """
    
    descriptions = {
        'jesse_wip_task_create.md': 'Create New Work-in-Progress Task',
        'jesse_wip_task_switch.md': 'Switch Between WIP Tasks',
        'jesse_wip_task_complete.md': 'Complete Current WIP Task',
        'jesse_wip_task_archive.md': 'Archive WIP Task Without Completion',
        'jesse_wip_task_capture_knowledge.md': 'Capture and Structure Knowledge',
        'jesse_wip_task_check_consistency.md': 'Verify Knowledge Consistency',
        'jesse_wip_task_process_large_file.md': 'Process Large Files from Git Clones',
        'jesse_wip_task_disable.md': 'Disable WIP Task Auto-Loading',
        'jesse_wip_task_commit.md': 'Commit WIP Task Changes with Standards',
        'jesse_wip_task_new_session.md': 'Force Knowledge Management System Initialization',
        'jesse_wip_kb_git_clone_import.md': 'Import External Git Repository',
        'jesse_wip_kb_pdf_import.md': 'Import and Index PDF Documents',
        'jesse_capture_our_chat.md': 'Capture Current Chat Session',
        'jesse_amazon_pr_faq_coach.md': 'Amazon PR/FAQ Document Coach'
    }
    
    # Try exact match first
    if workflow_file in descriptions:
        return descriptions[workflow_file]
    
    # Try pattern matching for custom workflows
    if workflow_file.startswith('jesse_wip_task_'):
        return f'WIP Task Workflow: {workflow_file}'
    elif workflow_file.startswith('jesse_capture_'):
        return f'Knowledge Capture Workflow: {workflow_file}'
    elif workflow_file.startswith('jesse_amazon_'):
        return f'Amazon Integration Workflow: {workflow_file}'
    elif workflow_file.startswith('jesse_framework_'):
        return f'Framework Management Workflow: {workflow_file}'
    
    return f'JESSE Workflow: {workflow_file}'


def get_workflow_category(workflow_file: str) -> str:
    """
    [Function intent]
    Classify workflow by category for organization and discovery.
    
    [Design principles]
    Pattern-based categorization with fallback to general category.
    Categories align with JESSE framework functional areas.
    
    [Implementation details]
    Uses prefix matching to determine workflow category.
    
    Args:
        workflow_file: Name of the JESSE workflow file
        
    Returns:
        Category classification for the workflow
    """
    
    categories = {
        'jesse_wip_task_': 'Task Management',
        'jesse_wip_kb_': 'Knowledge Management', 
        'jesse_capture_': 'Knowledge Capture',
        'jesse_amazon_': 'Amazon Integration',
        'jesse_framework_': 'Framework Management'
    }
    
    for prefix, category in categories.items():
        if workflow_file.startswith(prefix):
            return category
    
    return 'General Workflow'

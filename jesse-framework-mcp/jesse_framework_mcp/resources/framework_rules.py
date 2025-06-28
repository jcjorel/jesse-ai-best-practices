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
# Individual JESSE framework rule resources for modern FastMCP resource-first architecture.
# Provides granular access to each JESSE rule with HTTP formatting preservation.
###############################################################################
# [Source file design principles]
# - Individual resource per JESSE rule for granular access
# - HTTP formatting preserved exactly as current implementation
# - FastMCP Context integration for progress reporting and logging
# - CRITICAL criticality for all framework rules to ensure AI assistant compliance
###############################################################################
# [Source file constraints]
# - Must access embedded content from build-time copying
# - HTTP formatting must match existing format_http_section patterns
# - All JESSE rules classified as CRITICAL content for AI assistants
# - Resource URIs must follow jesse://framework/rule/{rule_name} pattern
###############################################################################
# [Dependencies]
# codebase:jesse_framework_mcp.main.server - FastMCP server instance for decoration
# codebase:jesse_framework_mcp.helpers.content_loaders - Embedded content access
# codebase:jesse_framework_mcp.helpers.http_formatter - HTTP section formatting
# codebase:jesse_framework_mcp.constants - JESSE rule file definitions
# system:fastmcp.Context - Progress reporting and logging
###############################################################################
# [GenAI tool change history]
# 2025-06-28T07:33:00Z : Updated to use new HttpFile-based API with writable flags by CodeAssistant
# * Added HttpPath import for new HTTP formatter API compatibility
# * Added writable=False parameter to all format_http_section calls for readonly framework rules
# * Enhanced HTTP formatting with Content-Writable headers for Cline integration
# * Maintained CRITICAL criticality and existing functionality while modernizing API usage
# 2025-06-28T06:57:00Z : Initial individual JESSE rule resources implementation by CodeAssistant
# * Created 6 individual resource handlers for each JESSE framework rule
# * Implemented HTTP formatting preservation with CRITICAL criticality classification
# * Added FastMCP Context integration for progress reporting and error handling
# * Established jesse://framework/rule/{rule_name} URI pattern for individual access
###############################################################################

from fastmcp import Context
from ..main import server
from ..helpers.content_loaders import load_embedded_content
from ..helpers.http_formatter import format_http_section, ContentCriticality, HttpPath
from ..constants import get_jesse_rule_files, get_jesse_rule_mapping


# === INDIVIDUAL JESSE RULE RESOURCES ===

@server.resource("jesse://framework/rule/knowledge_management")
async def get_knowledge_management_rule(ctx: Context) -> str:
    """
    [Function intent]
    Individual JESSE Knowledge Management rule resource with HTTP formatting.
    
    [Design principles]
    Granular access to knowledge management rules for AI assistant processing.
    CRITICAL criticality ensures strict adherence to framework requirements.
    
    [Implementation details]
    Loads embedded JESSE_KNOWLEDGE_MANAGEMENT.md content and applies HTTP formatting
    with portable path resolution and CRITICAL criticality classification.
    
    Args:
        ctx: FastMCP Context for progress reporting and logging
        
    Returns:
        HTTP-formatted JESSE Knowledge Management rule content
        
    Raises:
        ValueError: When rule content cannot be loaded or processed
    """
    await ctx.info("Loading JESSE Knowledge Management rule")
    
    try:
        content = await load_embedded_content("JESSE_KNOWLEDGE_MANAGEMENT.md")
        
        return format_http_section(
            content=content,
            content_type="text/markdown",
            criticality=ContentCriticality.CRITICAL,
            description="Knowledge Management System Rules and Directives",
            section_type="framework-rule",
            location="file://{CLINE_RULES}/JESSE_KNOWLEDGE_MANAGEMENT.md",
            writable=False
        )
        
    except Exception as e:
        await ctx.error(f"Failed to load Knowledge Management rule: {str(e)}")
        raise ValueError(f"Knowledge Management rule loading failed: {str(e)}")


@server.resource("jesse://framework/rule/hints")
async def get_hints_rule(ctx: Context) -> str:
    """
    [Function intent]
    Individual JESSE Hints rule resource with AI assistant enforcement directives.
    
    [Design principles]
    Critical enforcement rules for AI assistant behavior and compliance.
    CRITICAL criticality ensures mandatory adherence to framework directives.
    
    [Implementation details]
    Loads embedded JESSE_HINTS.md content with enforcement rules and applies
    HTTP formatting for AI assistant processing with maximum criticality.
    
    Args:
        ctx: FastMCP Context for progress reporting and logging
        
    Returns:
        HTTP-formatted JESSE Hints rule content
        
    Raises:
        ValueError: When rule content cannot be loaded or processed
    """
    await ctx.info("Loading JESSE Hints and Enforcement rules")
    
    try:
        content = await load_embedded_content("JESSE_HINTS.md")
        
        return format_http_section(
            content=content,
            content_type="text/markdown",
            criticality=ContentCriticality.CRITICAL,
            description="AI Assistant Enforcement Rules and Directives",
            section_type="framework-rule",
            location="file://{CLINE_RULES}/JESSE_HINTS.md",
            writable=False
        )
        
    except Exception as e:
        await ctx.error(f"Failed to load Hints rule: {str(e)}")
        raise ValueError(f"Hints rule loading failed: {str(e)}")


@server.resource("jesse://framework/rule/code_comments")
async def get_code_comments_rule(ctx: Context) -> str:
    """
    [Function intent]
    Individual JESSE Code Comments rule resource with documentation standards.
    
    [Design principles]
    Comprehensive code documentation requirements for consistent codebase quality.
    CRITICAL criticality ensures strict adherence to documentation standards.
    
    [Implementation details]
    Loads embedded JESSE_CODE_COMMENTS.md content and applies HTTP formatting
    with documentation standards and mandatory compliance requirements.
    
    Args:
        ctx: FastMCP Context for progress reporting and logging
        
    Returns:
        HTTP-formatted JESSE Code Comments rule content
        
    Raises:
        ValueError: When rule content cannot be loaded or processed
    """
    await ctx.info("Loading JESSE Code Comments documentation standards")
    
    try:
        content = await load_embedded_content("JESSE_CODE_COMMENTS.md")
        
        return format_http_section(
            content=content,
            content_type="text/markdown",
            criticality=ContentCriticality.CRITICAL,
            description="Code Documentation Standards and Requirements",
            section_type="framework-rule",
            location="file://{CLINE_RULES}/JESSE_CODE_COMMENTS.md",
            writable=False
        )
        
    except Exception as e:
        await ctx.error(f"Failed to load Code Comments rule: {str(e)}")
        raise ValueError(f"Code Comments rule loading failed: {str(e)}")


@server.resource("jesse://framework/rule/code_generation")
async def get_code_generation_rule(ctx: Context) -> str:
    """
    [Function intent]
    Individual JESSE Code Generation rule resource with development standards.
    
    [Design principles]
    Comprehensive code generation and development best practices enforcement.
    CRITICAL criticality ensures strict adherence to development standards.
    
    [Implementation details]
    Loads embedded JESSE_CODE_GENERATION.md content and applies HTTP formatting
    with development standards and quality enforcement requirements.
    
    Args:
        ctx: FastMCP Context for progress reporting and logging
        
    Returns:
        HTTP-formatted JESSE Code Generation rule content
        
    Raises:
        ValueError: When rule content cannot be loaded or processed
    """
    await ctx.info("Loading JESSE Code Generation development standards")
    
    try:
        content = await load_embedded_content("JESSE_CODE_GENERATION.md")
        
        return format_http_section(
            content=content,
            content_type="text/markdown",
            criticality=ContentCriticality.CRITICAL,
            description="Code Generation Standards and Best Practices",
            section_type="framework-rule",
            location="file://{CLINE_RULES}/JESSE_CODE_GENERATION.md",
            writable=False
        )
        
    except Exception as e:
        await ctx.error(f"Failed to load Code Generation rule: {str(e)}")
        raise ValueError(f"Code Generation rule loading failed: {str(e)}")


@server.resource("jesse://framework/rule/markdown")
async def get_markdown_rule(ctx: Context) -> str:
    """
    [Function intent]
    Individual JESSE Markdown rule resource with file management standards.
    
    [Design principles]
    Comprehensive markdown file management and formatting requirements.
    CRITICAL criticality ensures strict adherence to markdown standards.
    
    [Implementation details]
    Loads embedded JESSE_MARKDOWN.md content and applies HTTP formatting
    with markdown management standards and compliance requirements.
    
    Args:
        ctx: FastMCP Context for progress reporting and logging
        
    Returns:
        HTTP-formatted JESSE Markdown rule content
        
    Raises:
        ValueError: When rule content cannot be loaded or processed
    """
    await ctx.info("Loading JESSE Markdown file management standards")
    
    try:
        content = await load_embedded_content("JESSE_MARKDOWN.md")
        
        return format_http_section(
            content=content,
            content_type="text/markdown",
            criticality=ContentCriticality.CRITICAL,
            description="Markdown File Management Standards",
            section_type="framework-rule",
            location="file://{CLINE_RULES}/JESSE_MARKDOWN.md",
            writable=False
        )
        
    except Exception as e:
        await ctx.error(f"Failed to load Markdown rule: {str(e)}")
        raise ValueError(f"Markdown rule loading failed: {str(e)}")


@server.resource("jesse://framework/rule/scratchpad")
async def get_scratchpad_rule(ctx: Context) -> str:
    """
    [Function intent]
    Individual JESSE Scratchpad rule resource with directory management standards.
    
    [Design principles]
    Comprehensive scratchpad directory usage and management requirements.
    CRITICAL criticality ensures strict adherence to scratchpad standards.
    
    [Implementation details]
    Loads embedded JESSE_SCRATCHPAD.md content and applies HTTP formatting
    with scratchpad management standards and compliance requirements.
    
    Args:
        ctx: FastMCP Context for progress reporting and logging
        
    Returns:
        HTTP-formatted JESSE Scratchpad rule content
        
    Raises:
        ValueError: When rule content cannot be loaded or processed
    """
    await ctx.info("Loading JESSE Scratchpad directory management standards")
    
    try:
        content = await load_embedded_content("JESSE_SCRATCHPAD.md")
        
        return format_http_section(
            content=content,
            content_type="text/markdown",
            criticality=ContentCriticality.CRITICAL,
            description="Scratchpad Directory Management Standards",
            section_type="framework-rule",
            location="file://{CLINE_RULES}/JESSE_SCRATCHPAD.md",
            writable=False
        )
        
    except Exception as e:
        await ctx.error(f"Failed to load Scratchpad rule: {str(e)}")
        raise ValueError(f"Scratchpad rule loading failed: {str(e)}")


# === HELPER FUNCTIONS ===

async def get_available_rule_names() -> list[str]:
    """
    [Function intent]
    Get list of available JESSE rule names for resource discovery.
    
    [Design principles]
    Dynamic rule discovery for resource listing and validation.
    Consistent naming pattern for individual rule access.
    
    [Implementation details]
    Converts JESSE rule file names to resource-friendly short names
    by removing JESSE_ prefix and .md suffix.
    
    Returns:
        List of JESSE rule names for resource URIs
    """
    rule_files = get_jesse_rule_files()
    rule_names = []
    
    for rule_file in rule_files:
        if rule_file.startswith("JESSE_") and rule_file.endswith(".md"):
            # Convert JESSE_KNOWLEDGE_MANAGEMENT.md -> knowledge_management
            rule_name = rule_file[6:-3].lower()  # Remove JESSE_ prefix and .md suffix
            rule_names.append(rule_name)
    
    return rule_names


def get_rule_description(rule_name: str) -> str:
    """
    [Function intent]
    Get human-readable description for JESSE framework rule.
    
    [Design principles]
    Centralized mapping of rule names to user-friendly descriptions.
    Fallback to generic description for unknown rule names.
    
    [Implementation details]
    Uses dictionary lookup with fallback pattern for rule descriptions.
    
    Args:
        rule_name: Short rule name (e.g., 'knowledge_management')
        
    Returns:
        Human-readable description of the rule purpose
    """
    descriptions = {
        'knowledge_management': 'Knowledge Management System Rules and Directives',
        'hints': 'AI Assistant Enforcement Rules and Directives',
        'code_comments': 'Code Documentation Standards and Requirements',
        'code_generation': 'Code Generation Standards and Best Practices',
        'markdown': 'Markdown File Management Standards',
        'scratchpad': 'Scratchpad Directory Management Standards'
    }
    
    return descriptions.get(rule_name, f'JESSE Framework Rule: {rule_name}')


async def get_rule_by_name(rule_name: str, ctx: Context) -> str:
    """
    [Function intent]
    Route individual rule requests to appropriate resource handler.
    
    [Design principles]
    Centralized routing for individual JESSE rule access.
    Maintains consistency with existing resource handler patterns.
    
    [Implementation details]
    Maps rule names to specific resource handler functions,
    delegates to appropriate handler with Context propagation.
    Uses FastMCP function unwrapping to handle decorated resource functions.
    
    Args:
        rule_name: Short rule name (e.g., 'knowledge_management')
        ctx: FastMCP Context for progress reporting and logging
        
    Returns:
        HTTP-formatted JESSE rule content
        
    Raises:
        ValueError: When rule name is not recognized
    """
    # Import the unwrapper utility
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from utils import unwrap_fastmcp_function
    
    handlers = {
        'knowledge_management': get_knowledge_management_rule,
        'hints': get_hints_rule,
        'code_comments': get_code_comments_rule,
        'code_generation': get_code_generation_rule,
        'markdown': get_markdown_rule,
        'scratchpad': get_scratchpad_rule
    }
    
    handler = handlers.get(rule_name)
    if not handler:
        raise ValueError(f"Unknown JESSE rule: {rule_name}")
    
    # Unwrap the FastMCP decorated function before calling
    unwrapped_handler = unwrap_fastmcp_function(handler)
    return await unwrapped_handler(ctx)


def register_framework_rules_resources():
    """
    [Function intent]
    Register all framework rule resources with the server.
    
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

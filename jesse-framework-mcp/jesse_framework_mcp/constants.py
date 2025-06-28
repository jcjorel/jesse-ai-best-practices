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
# Central configuration constants for JESSE Framework MCP Server,
# eliminating hardcoded rule filenames across the codebase.
###############################################################################
# [Source file design principles]
# - Single source of truth for JESSE rule file definitions
# - Dynamic discovery support for embedded content at runtime
# - Mapping generation from core rule list to avoid duplication
###############################################################################
# [Source file constraints]
# - Must maintain compatibility with existing importlib.resources usage
# - Rule file names must match actual embedded content files
# - Supports both build-time and runtime usage patterns
###############################################################################
# [Dependencies]
# system:importlib.resources - For dynamic rule discovery at runtime
# system:typing - Type hints for better code documentation
###############################################################################
# [GenAI tool change history]
# 2025-06-28T00:30:40Z : Added HTTP formatting constants for resource standardization by CodeAssistant
# * Added HTTP boundary markers and content type definitions
# * Created section type classifications and rule criticality mapping
# * Established foundation for universal HTTP-style resource formatting
# 2025-06-27T20:58:50Z : Initial constants module creation by CodeAssistant
# * Created central JESSE rule file configuration
# * Eliminated hardcoded rule filenames across codebase
# * Added dynamic discovery support for embedded content
###############################################################################

from typing import List, Dict, Optional

try:
    from importlib import resources
except ImportError:
    # Python < 3.9 compatibility
    import importlib_resources as resources

# === HTTP FORMATTING CONSTANTS ===

# HTTP-style formatting boundary marker
HTTP_BOUNDARY = "ASYNC-HTTP-SECTION-START-v20250628"
HTTP_BOUNDARY_MARKER = f"--- {HTTP_BOUNDARY}"

# Content type definitions for MCP resources
CONTENT_TYPES = {
    'markdown': 'text/markdown',
    'json': 'application/json',
    'text': 'text/plain',
    'yaml': 'application/yaml',
    'workflow': 'text/markdown'  # Workflows are markdown format
}

# Section type classifications for resource organization
SECTION_TYPES = {
    'framework-rule': 'JESSE Framework Rule',
    'workflow': 'JESSE Workflow',
    'project-knowledge': 'Project Knowledge',
    'knowledge-base': 'External Knowledge Base',
    'wip-task': 'Work-in-Progress Task',
    'knowledge-inventory': 'Knowledge Base Inventory',
    'project-context': 'Project Context Overview'
}

# Rule file criticality mapping for AI assistant processing
RULE_CRITICALITY_MAP = {
    'JESSE_KNOWLEDGE_MANAGEMENT.md': 'CRITICAL',
    'JESSE_HINTS.md': 'CRITICAL',
    'JESSE_CODE_COMMENTS.md': 'CRITICAL',
    'JESSE_CODE_GENERATION.md': 'CRITICAL',
    'JESSE_MARKDOWN.md': 'CRITICAL',
    'JESSE_SCRATCHPAD.md': 'CRITICAL'
}

# Default criticality for different content types
DEFAULT_CRITICALITY = {
    'framework-rule': 'CRITICAL',
    'workflow': 'CRITICAL',
    'project-knowledge': 'INFORMATIONAL',
    'knowledge-base': 'INFORMATIONAL',
    'wip-task': 'INFORMATIONAL',
    'knowledge-inventory': 'INFORMATIONAL',
    'project-context': 'INFORMATIONAL'
}

# === JESSE RULE FILES CONFIGURATION ===

# Central list of JESSE rule files - SINGLE SOURCE OF TRUTH
JESSE_RULE_FILES: List[str] = [
    "JESSE_KNOWLEDGE_MANAGEMENT.md",
    "JESSE_HINTS.md", 
    "JESSE_CODE_COMMENTS.md",
    "JESSE_CODE_GENERATION.md",
    "JESSE_MARKDOWN.md",
    "JESSE_SCRATCHPAD.md"
]

def get_jesse_rule_files() -> List[str]:
    """
    [Function intent]
    Get the complete list of JESSE rule files from central configuration.
    
    [Design principles]
    Single access point for JESSE rule file list across entire codebase.
    Enables easy modification of rule files without touching multiple files.
    
    [Implementation details]
    Returns copy of central JESSE_RULE_FILES list to prevent modification.
    Can be extended with dynamic discovery if needed.
    
    Returns:
        Complete list of JESSE rule file names
    """
    return JESSE_RULE_FILES.copy()


def get_jesse_rule_mapping() -> Dict[str, str]:
    """
    [Function intent]
    Generate mapping from short rule names to full JESSE rule file names.
    
    [Design principles]
    Automatically derives mapping from central rule file list.
    Eliminates need to maintain separate mapping configuration.
    
    [Implementation details]
    Converts JESSE_*.md files to short names by removing prefix/suffix,
    creates bidirectional mapping for flexible rule access.
    
    Returns:
        Dictionary mapping short names to full JESSE rule file names
    """
    mapping = {}
    
    for file_name in JESSE_RULE_FILES:
        if file_name.startswith("JESSE_") and file_name.endswith(".md"):
            # Extract short name: JESSE_CODE_COMMENTS.md -> code_comments
            short_name = file_name[6:-3].lower()  # Remove "JESSE_" prefix and ".md" suffix
            mapping[short_name] = file_name
    
    return mapping


def discover_jesse_rule_files() -> Optional[List[str]]:
    """
    [Function intent]
    Dynamically discover JESSE rule files from embedded content at runtime.
    
    [Design principles]
    Runtime discovery as fallback or verification mechanism.
    Graceful failure handling when embedded content cannot be accessed.
    
    [Implementation details]
    Uses importlib.resources to scan embedded_content directory,
    filters for JESSE_*.md files, returns sorted list for consistency.
    
    Returns:
        List of discovered JESSE rule files, None if discovery fails
    """
    try:
        # Access embedded content directory
        embedded_files = resources.files('jesse_framework_mcp.embedded_content')
        
        discovered_files = []
        for file_path in embedded_files.iterdir():
            if (file_path.is_file() and 
                file_path.name.startswith("JESSE_") and 
                file_path.name.endswith(".md")):
                discovered_files.append(file_path.name)
        
        return sorted(discovered_files)
        
    except Exception:
        # Graceful failure - return None to indicate discovery failed
        return None


def validate_jesse_rule_files() -> bool:
    """
    [Function intent]
    Validate that configured JESSE rule files match embedded content.
    
    [Design principles]
    Runtime validation to catch configuration/embedding mismatches.
    Non-blocking validation that returns success/failure status.
    
    [Implementation details]
    Compares configured rule files with discovered embedded files,
    returns True if they match, False otherwise.
    
    Returns:
        True if configuration matches embedded content, False otherwise
    """
    discovered = discover_jesse_rule_files()
    
    if discovered is None:
        # Discovery failed - assume configuration is correct
        return True
    
    configured = sorted(get_jesse_rule_files())
    
    return configured == discovered


# === MODULE INFORMATION FUNCTIONS ===

def get_rule_files_info() -> Dict[str, any]:
    """
    [Function intent]
    Get comprehensive information about JESSE rule files configuration.
    
    [Design principles]
    Debugging and monitoring support for rule file management.
    Structured information for diagnostic purposes.
    
    [Implementation details]
    Combines configured files, discovered files, mapping, and validation
    into single information dictionary.
    
    Returns:
        Dictionary with rule files configuration information
    """
    return {
        "configured_files": get_jesse_rule_files(),
        "discovered_files": discover_jesse_rule_files(),
        "rule_mapping": get_jesse_rule_mapping(),
        "validation_passed": validate_jesse_rule_files(),
        "total_configured": len(JESSE_RULE_FILES)
    }

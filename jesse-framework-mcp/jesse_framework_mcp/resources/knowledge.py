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
# JESSE Framework knowledge base resource handlers for MCP server,
# providing project knowledge bases as MCP resources with HTTP formatting.
###############################################################################
# [Source file design principles]
# - Resource-based knowledge delivery for lazy loading functionality
# - HTTP-formatted content for consistent parsing and metadata extraction
# - Direct access to specific knowledge bases without tool overhead
# - Supports both git clone and PDF knowledge base types
###############################################################################
# [Source file constraints]
# - Must access .knowledge/ directory for project-specific knowledge
# - Requires proper error handling for missing knowledge bases
# - FastMCP Context integration for logging and error reporting
# - HTTP formatting must include portable file paths and proper criticality
###############################################################################
# [Dependencies]
# system:fastmcp.FastMCP - FastMCP server instance and Context
# codebase:../main - FastMCP server instance
# codebase:../helpers.knowledge_scanners - Knowledge base loading functions
# codebase:../helpers.http_formatter - HTTP section formatting utilities
# codebase:../constants - Content criticality and path constants
###############################################################################
# [GenAI tool change history]
# 2025-06-28T07:42:00Z : Added writable resources for git-clones and pdf-knowledge README.md files by CodeAssistant
# * Added get_git_clones_readme resource handler for .knowledge/git-clones/README.md
# * Added get_pdf_knowledge_readme resource handler for .knowledge/pdf-knowledge/README.md
# * Implemented graceful handling when PDF knowledge directory doesn't exist
# * Both resources return HTTP-formatted content with writable=True for editing capability
# 2025-06-28T07:35:00Z : Updated to use new HttpFile-based API with writable flags by CodeAssistant
# * Added HttpPath import for new HTTP formatter API compatibility
# * Added writable=True parameter to format_http_section call for editable knowledge bases
# * Enhanced HTTP formatting with Content-Writable headers for Cline integration
# * Maintained INFORMATIONAL criticality while enabling content editing capabilities
# 2025-06-28T01:03:45Z : Updated knowledge resource to HTTP formatting by CodeAssistant
# * Implemented HTTP-formatted knowledge base resources
# * Added knowledge base info determination and metadata
# * Integrated portable path resolution and criticality classification
###############################################################################

import os
import json
from datetime import datetime
from pathlib import Path
from fastmcp import Context

# Import dependencies at module level for function availability
from ..helpers.async_http_formatter import format_http_section, XAsyncContentCriticality, XAsyncHttpPath
from ..helpers.path_utils import get_project_root

async def get_git_clones_readme(ctx: Context) -> str:
        """
        [Function intent]
        Provide git clones README.md content in HTTP format for knowledge base index access.
        
        [Design principles]
        Direct access to git clone knowledge base index for repository management.
        HTTP-formatted content with writable capability for index updates.
        Graceful error handling for missing files.
        
        [Implementation details]
        Loads .knowledge/git-clones/README.md file content,
        applies HTTP formatting with appropriate metadata and portable paths.
        
        Args:
            ctx: FastMCP Context for logging and progress reporting
            
        Returns:
            HTTP-formatted git clones README content
            
        Raises:
            ValueError: When README file cannot be found or loaded
        """
        
        await ctx.info("Loading git clones README.md")
        
        try:
            # Get project root and build absolute path
            project_root = get_project_root()
            if not project_root:
                raise ValueError("Project root not found - cannot locate knowledge bases")
            
            readme_path = ".knowledge/git-clones/README.md"
            absolute_readme_path = os.path.join(project_root, readme_path)
            
            if not os.path.exists(absolute_readme_path):
                error_msg = f"Git clones README not found: {readme_path}"
                await ctx.error(error_msg)
                raise ValueError(error_msg)
            
            # Load README content
            with open(absolute_readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
            
            # Format as HTTP section
            formatted_readme = format_http_section(
                content=readme_content,
                content_type="text/markdown",
                criticality=XAsyncContentCriticality.INFORMATIONAL,
                description="Git Clone Knowledge Bases Index",
                section_type="knowledge-index",
                location=f"file://{{PROJECT_ROOT}}/{readme_path}",
                additional_headers={
                    "Knowledge-Type": "git-clone-index",
                    "Last-Updated": get_file_modification_time(absolute_readme_path)
                },
                writable=True
            )
            
            await ctx.info(f"Git clones README loaded: {len(readme_content)} characters")
            return formatted_readme
            
        except Exception as e:
            error_msg = f"Failed to load git clones README: {str(e)}"
            await ctx.error(error_msg)
            raise ValueError(error_msg)
    
async def get_pdf_knowledge_readme(ctx: Context) -> str:
        """
        [Function intent]
        Provide PDF knowledge README.md content in HTTP format for PDF knowledge base index access.
        
        [Design principles]
        Direct access to PDF knowledge base index for document management.
        HTTP-formatted content with writable capability for index updates.
        Graceful handling when PDF knowledge directory doesn't exist.
        
        [Implementation details]
        Loads .knowledge/pdf-knowledge/README.md file content,
        applies HTTP formatting with appropriate metadata and portable paths,
        handles missing directory/file scenarios gracefully.
        
        Args:
            ctx: FastMCP Context for logging and progress reporting
            
        Returns:
            HTTP-formatted PDF knowledge README content or appropriate error message
            
        Raises:
            ValueError: When README file cannot be found or loaded
        """
        
        await ctx.info("Loading PDF knowledge README.md")
        
        try:
            # Get project root and build absolute paths
            project_root = get_project_root()
            if not project_root:
                raise ValueError("Project root not found - cannot locate knowledge bases")
            
            readme_path = ".knowledge/pdf-knowledge/README.md"
            pdf_dir_path = ".knowledge/pdf-knowledge"
            absolute_pdf_dir = os.path.join(project_root, pdf_dir_path)
            absolute_readme_path = os.path.join(project_root, readme_path)
            
            if not os.path.exists(absolute_pdf_dir):
                error_msg = "PDF knowledge directory does not exist: .knowledge/pdf-knowledge/"
                await ctx.warning(error_msg)
                
                # Return formatted empty content with creation guidance
                empty_content = """# PDF Knowledge Bases Index

This directory will contain knowledge bases extracted from PDF documents that provide context and patterns relevant to the JESSE Framework development.

## Directory Structure
```
.knowledge/pdf-knowledge/
├── README.md                                    # This index file
├── [pdf-name]/                                 # PDF document directory
│   ├── [pdf-name]_kb.md                       # Knowledge base extracted from PDF (tracked)
│   └── pdf_chunks/                             # Chunked PDF content for processing
└── [another-pdf]/                              # Additional PDF knowledge bases
```

## Available Knowledge Bases
*No PDF knowledge bases imported yet*

## How to Add PDF Knowledge Bases
Use the PDF Import workflow to add PDF documents:

```bash
/jesse_wip_kb_pdf_import.md
```

This workflow will:
1. Prompt for PDF file path and processing requirements
2. Create directory structure in `.knowledge/pdf-knowledge/[pdf-name]/`
3. Process PDF into chunks in `pdf_chunks/` subdirectory
4. Create knowledge base file `[pdf-name]_kb.md`
5. Index important content and patterns
6. Update main knowledge base with reference
"""
                
                formatted_readme = format_http_section(
                    content=empty_content,
                    content_type="text/markdown",
                    criticality=XAsyncContentCriticality.INFORMATIONAL,
                    description="PDF Knowledge Bases Index (Directory Not Found)",
                    section_type="knowledge-index",
                    location=f"file://{{PROJECT_ROOT}}/{readme_path}",
                    additional_headers={
                        "Knowledge-Type": "pdf-index",
                        "Directory-Status": "missing",
                        "Last-Updated": datetime.now().isoformat() + 'Z'
                    },
                    writable=True
                )
                
                return formatted_readme
            
            if not os.path.exists(absolute_readme_path):
                error_msg = f"PDF knowledge README not found: {readme_path}"
                await ctx.error(error_msg)
                raise ValueError(error_msg)
            
            # Load README content
            with open(absolute_readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
            
            # Format as HTTP section
            formatted_readme = format_http_section(
                content=readme_content,
                content_type="text/markdown",
                criticality=XAsyncContentCriticality.INFORMATIONAL,
                description="PDF Knowledge Bases Index",
                section_type="knowledge-index",
                location=f"file://{{PROJECT_ROOT}}/{readme_path}",
                additional_headers={
                    "Knowledge-Type": "pdf-index",
                    "Last-Updated": get_file_modification_time(absolute_readme_path)
                },
                writable=True
            )
            
            await ctx.info(f"PDF knowledge README loaded: {len(readme_content)} characters")
            return formatted_readme
            
        except Exception as e:
            error_msg = f"Failed to load PDF knowledge README: {str(e)}"
            await ctx.error(error_msg)
            raise ValueError(error_msg)
    
async def get_knowledge_base(kb_name: str, ctx: Context) -> str:
        """
        [Function intent]
        Provide individual knowledge base content in HTTP format for lazy loading.
        
        [Design principles]
        On-demand knowledge base loading for specific AI assistant requirements.
        All knowledge bases classified as INFORMATIONAL content.
        Supports both git clone and PDF knowledge base types.
        
        [Implementation details]
        Determines knowledge base type and location, loads content,
        applies HTTP formatting with appropriate metadata and portable paths.
        
        Args:
            kb_name: Knowledge base name (e.g., 'cline_kb', 'fastmcp_kb')
            ctx: FastMCP Context for logging and progress reporting
            
        Returns:
            HTTP-formatted knowledge base content
            
        Raises:
            ValueError: When knowledge base cannot be found or loaded
        """
        
        await ctx.info(f"Loading knowledge base: {kb_name}")
        
        try:
            # Determine knowledge base type and location
            kb_info = await determine_knowledge_base_info(kb_name, ctx)
            
            # Load knowledge base content
            kb_content = await load_specific_knowledge_base_async(kb_name, ctx)
            
            # Format as HTTP section
            formatted_kb = format_http_section(
                content=kb_content,
                content_type="text/markdown",
                criticality=XAsyncContentCriticality.INFORMATIONAL,
                description=f"Knowledge Base: {kb_info['display_name']}",
                section_type="knowledge-base",
                location=f"file://{{PROJECT_ROOT}}/{kb_info['file_path']}",
                additional_headers={
                    "Knowledge-Type": kb_info['type'],  # 'git-clone' or 'pdf'
                    "Source-URL": kb_info.get('source_url', ''),
                    "Last-Updated": kb_info.get('last_updated', '')
                },
                writable=True
            )
            
            await ctx.info(f"Knowledge base loaded: {len(kb_content)} characters")
            return formatted_kb
            
        except Exception as e:
            error_msg = f"Failed to load knowledge base {kb_name}: {str(e)}"
            await ctx.error(error_msg)
            raise ValueError(error_msg)


def register_knowledge_resources():
    """
    [Function intent]
    Register knowledge base resources with HTTP formatting for lazy loading.
    
    [Design principles]
    HTTP-formatted resource delivery for consistent AI assistant processing.
    On-demand knowledge base loading for specific requirements.
    Proper metadata inclusion for knowledge base context.
    
    [Implementation details]
    Registers individual knowledge base resource handler with HTTP formatting,
    supports both git clone and PDF knowledge base types,
    includes portable paths and appropriate criticality classification.
    """
    from ..main import server
    from ..helpers.knowledge_scanners import load_specific_knowledge_base_async
    
    # Register the resource handlers using the functions defined above
    server.resource("jesse://knowledge/git-clones-readme")(get_git_clones_readme)
    server.resource("jesse://knowledge/pdf-knowledge-readme")(get_pdf_knowledge_readme)
    server.resource("jesse://knowledge/{kb_name}")(get_knowledge_base)


async def determine_knowledge_base_info(kb_name: str, ctx: Context) -> dict:
    """
    [Function intent]
    Determine knowledge base type, location, and metadata information.
    
    [Design principles]
    Centralized knowledge base metadata determination for consistent handling.
    Support for multiple knowledge base types with extensible design.
    
    [Implementation details]
    Checks for git clone and PDF knowledge base files, extracts metadata
    from file system and knowledge base content headers.
    
    Args:
        kb_name: Knowledge base name to analyze
        ctx: FastMCP Context for logging
        
    Returns:
        Dictionary with knowledge base metadata
        
    Raises:
        ValueError: When knowledge base cannot be found or analyzed
    """
    
    await ctx.info(f"Determining knowledge base info for: {kb_name}")
    
    # Normalize knowledge base name
    if not kb_name.endswith('_kb'):
        kb_name_with_suffix = f"{kb_name}_kb"
    else:
        kb_name_with_suffix = kb_name
    
    # Check for git clone knowledge base
    git_clone_path = f".knowledge/git-clones/{kb_name_with_suffix}.md"
    if os.path.exists(git_clone_path):
        return await extract_git_clone_kb_info(git_clone_path, kb_name_with_suffix, ctx)
    
    # Check for PDF knowledge base
    pdf_kb_path = f".knowledge/pdf-knowledge/{kb_name_with_suffix}/{kb_name_with_suffix}.md"
    if os.path.exists(pdf_kb_path):
        return await extract_pdf_kb_info(pdf_kb_path, kb_name_with_suffix, ctx)
    
    # Check for essential knowledge base
    if kb_name_with_suffix == "KNOWLEDGE_BASE" or kb_name == "essential":
        essential_path = ".knowledge/persistent-knowledge/KNOWLEDGE_BASE.md"
        if os.path.exists(essential_path):
            return {
                "type": "essential",
                "display_name": "Essential Project Knowledge Base",
                "file_path": essential_path,
                "source_url": "",
                "last_updated": get_file_modification_time(essential_path)
            }
    
    raise ValueError(f"Knowledge base not found: {kb_name}")

async def extract_git_clone_kb_info(file_path: str, kb_name: str, ctx: Context) -> dict:
    """
    [Function intent]
    Extract metadata from git clone knowledge base file.
    
    [Design principles]
    Parse knowledge base headers for repository metadata.
    Consistent metadata structure for all git clone knowledge bases.
    
    [Implementation details]
    Reads knowledge base file headers to extract repository URL,
    clone date, and other metadata information.
    
    Args:
        file_path: Path to git clone knowledge base file
        kb_name: Knowledge base name
        ctx: FastMCP Context for logging
        
    Returns:
        Dictionary with git clone knowledge base metadata
    """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract repository information from content
        source_url = ""
        last_updated = ""
        
        # Parse header information
        lines = content.split('\n')
        for line in lines[:20]:  # Check first 20 lines for metadata
            if line.startswith("**Clone URL**:") or line.startswith("**Repository**:"):
                source_url = line.split(':', 1)[1].strip()
            elif line.startswith("*Last Updated:"):
                last_updated = line.split(':', 1)[1].strip()
        
        # Generate display name from kb_name
        display_name = kb_name.replace('_kb', '').replace('_', ' ').title()
        
        return {
            "type": "git-clone",
            "display_name": f"{display_name} Knowledge Base",
            "file_path": file_path,
            "source_url": source_url,
            "last_updated": last_updated or get_file_modification_time(file_path)
        }
        
    except Exception as e:
        await ctx.error(f"Failed to extract git clone KB info from {file_path}: {str(e)}")
        raise ValueError(f"Git clone KB info extraction failed: {str(e)}")

async def extract_pdf_kb_info(file_path: str, kb_name: str, ctx: Context) -> dict:
    """
    [Function intent]
    Extract metadata from PDF knowledge base file.
    
    [Design principles]
    Parse PDF knowledge base headers for document metadata.
    Consistent metadata structure for all PDF knowledge bases.
    
    [Implementation details]
    Reads PDF knowledge base file headers to extract source document,
    processing date, and other metadata information.
    
    Args:
        file_path: Path to PDF knowledge base file
        kb_name: Knowledge base name
        ctx: FastMCP Context for logging
        
    Returns:
        Dictionary with PDF knowledge base metadata
    """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract PDF information from content
        source_url = ""
        last_updated = ""
        
        # Parse header information
        lines = content.split('\n')
        for line in lines[:20]:  # Check first 20 lines for metadata
            if line.startswith("**Source PDF**:") or line.startswith("**Document**:"):
                source_url = line.split(':', 1)[1].strip()
            elif line.startswith("*Last Updated:") or line.startswith("*Processed:"):
                last_updated = line.split(':', 1)[1].strip()
        
        # Generate display name from kb_name
        display_name = kb_name.replace('_kb', '').replace('_', ' ').title()
        
        return {
            "type": "pdf",
            "display_name": f"{display_name} PDF Knowledge Base",
            "file_path": file_path,
            "source_url": source_url,
            "last_updated": last_updated or get_file_modification_time(file_path)
        }
        
    except Exception as e:
        await ctx.error(f"Failed to extract PDF KB info from {file_path}: {str(e)}")
        raise ValueError(f"PDF KB info extraction failed: {str(e)}")

def get_file_modification_time(file_path: str) -> str:
    """
    [Function intent]
    Get file modification time as ISO formatted string.
    
    [Design principles]
    Consistent timestamp format for all knowledge base metadata.
    
    [Implementation details]
    Uses file system modification time, formats as ISO string.
    
    Args:
        file_path: Path to file
        
    Returns:
        ISO formatted modification timestamp
    """
    
    try:
        stat = os.stat(file_path)
        return datetime.fromtimestamp(stat.st_mtime).isoformat() + 'Z'
    except Exception:
        return datetime.now().isoformat() + 'Z'

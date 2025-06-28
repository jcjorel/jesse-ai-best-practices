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
# Knowledge base scanning and loading helper functions for JESSE Framework MCP Server,
# handling discovery and loading of git clone and PDF knowledge bases.
###############################################################################
# [Source file design principles]
# - Discovery-based approach to find available knowledge bases with metadata
# - Flexible knowledge base loading supporting multiple storage locations
# - Async-only architecture with FastMCP Context integration
###############################################################################
# [Source file constraints]
# - Must access .knowledge/ directory structure (git-clones/, pdf-knowledge/)
# - Requires proper error handling for missing knowledge bases
# - FastMCP Context integration for all operations
###############################################################################
# [Dependencies]
# system:pathlib.Path - Cross-platform filesystem operations
# system:fastmcp.Context - FastMCP Context for async operations
###############################################################################
# [GenAI tool change history]
# 2025-06-27T21:22:00Z : Removed legacy non-async functions by CodeAssistant
# * Removed all sync functions: generate_knowledge_base_inventory, scan_git_clone_knowledge_bases, scan_pdf_knowledge_bases, load_specific_knowledge_base
# * Updated async functions to use async scan functions internally
# * Removed unused logging dependency
# * Updated design principles to reflect async-only architecture
# 2025-06-27T20:30:06Z : Initial knowledge scanners module creation by CodeAssistant
# * Extracted knowledge base scanning and loading functions from main.py
# * Modularized knowledge discovery functionality with async/sync support
###############################################################################

from pathlib import Path
from typing import List

from fastmcp import Context

# === ASYNC KNOWLEDGE SCANNING FUNCTIONS ===

async def scan_git_clone_knowledge_bases_async(ctx: Context) -> List[str]:
    """
    [Function intent]
    Async scan of .knowledge/git-clones/ directory for available repository knowledge bases.
    
    [Design principles]
    Discovery-based approach to find available git clone knowledge files.
    Descriptive naming to help LLM selection of relevant repositories.
    Uses Context for progress reporting during directory scanning.
    
    [Implementation details]
    Scans for *_kb.md files in git-clones directory, extracts repository names
    from filenames, provides basic metadata for selection.
    
    Args:
        ctx: FastMCP Context for progress reporting
        
    Returns:
        List of git clone knowledge base descriptions
    """
    
    git_clones = []
    git_clones_dir = Path(".knowledge/git-clones")
    
    if git_clones_dir.exists():
        await ctx.info(f"Scanning directory: {git_clones_dir}")
        for kb_file in git_clones_dir.glob("*_kb.md"):
            repo_name = kb_file.stem.replace("_kb", "")
            file_size = kb_file.stat().st_size if kb_file.exists() else 0
            size_desc = "large" if file_size > 50000 else "medium" if file_size > 10000 else "small"
            git_clones.append(f"{repo_name}_kb: Repository knowledge (size: {size_desc})")
    else:
        await ctx.info(f"Directory not found: {git_clones_dir}")
    
    return git_clones


async def scan_pdf_knowledge_bases_async(ctx: Context) -> List[str]:
    """
    [Function intent]
    Async scan of .knowledge/pdf-knowledge/ directory for available PDF knowledge bases.
    
    [Design principles]
    Discovery-based approach to find available PDF-derived knowledge files.
    Size-based metadata to help with context window management.
    Uses Context for progress reporting during directory scanning.
    
    [Implementation details]
    Scans for *_kb.md files in pdf-knowledge directory, extracts document names
    from filenames, provides size estimates for selection.
    
    Args:
        ctx: FastMCP Context for progress reporting
        
    Returns:
        List of PDF knowledge base descriptions
    """
    
    pdf_knowledge = []
    pdf_dir = Path(".knowledge/pdf-knowledge")
    
    if pdf_dir.exists():
        await ctx.info(f"Scanning directory: {pdf_dir}")
        for kb_file in pdf_dir.glob("*_kb.md"):
            doc_name = kb_file.stem.replace("_kb", "")
            file_size = kb_file.stat().st_size if kb_file.exists() else 0
            size_desc = "large" if file_size > 50000 else "medium" if file_size > 10000 else "small"
            pdf_knowledge.append(f"{doc_name}_kb: PDF knowledge (size: {size_desc})")
    else:
        await ctx.info(f"Directory not found: {pdf_dir}")
    
    return pdf_knowledge


async def generate_knowledge_base_inventory_async(ctx: Context) -> str:
    """
    [Function intent]
    Async version of knowledge base inventory generation with Context integration.
    
    [Design principles]
    Comprehensive discovery of available knowledge bases with metadata.
    Uses Context for progress reporting during directory scanning.
    
    [Implementation details]
    Scans .knowledge/ subdirectories for git clones and PDF knowledge,
    generates structured inventory with names and descriptions.
    
    Args:
        ctx: FastMCP Context for progress reporting
        
    Returns:
        Formatted inventory of available knowledge bases
    """
    
    try:
        inventory_parts = []
        
        # Scan git clone knowledge bases
        await ctx.info("Scanning git clone knowledge bases...")
        git_clones = await scan_git_clone_knowledge_bases_async(ctx)
        if git_clones:
            inventory_parts.append("Git Clone Knowledge Bases:")
            for kb_info in git_clones:
                inventory_parts.append(f"  - {kb_info}")
            await ctx.info(f"Found {len(git_clones)} git clone knowledge bases")
        else:
            inventory_parts.append("Git Clone Knowledge Bases: None available")
            await ctx.info("No git clone knowledge bases found")
        
        # Scan PDF knowledge bases
        await ctx.info("Scanning PDF knowledge bases...")
        pdf_knowledge = await scan_pdf_knowledge_bases_async(ctx)
        if pdf_knowledge:
            inventory_parts.append("\nPDF Knowledge Bases:")
            for kb_info in pdf_knowledge:
                inventory_parts.append(f"  - {kb_info}")
            await ctx.info(f"Found {len(pdf_knowledge)} PDF knowledge bases")
        else:
            inventory_parts.append("\nPDF Knowledge Bases: None available")
            await ctx.info("No PDF knowledge bases found")
        
        # Add lazy loading instructions
        inventory_parts.append("\nLazy Loading Instructions:")
        inventory_parts.append("To load specific knowledge bases, call:")
        inventory_parts.append("jesse_load_knowledge_base(kb_names=[\"kb_name1\", \"kb_name2\"])")
        
        return "\n".join(inventory_parts)
        
    except Exception as e:
        await ctx.error(f"Failed to generate KB inventory: {str(e)}")
        return f"Knowledge base inventory error: {str(e)}"


async def load_specific_knowledge_base_async(kb_name: str, ctx: Context) -> str:
    """
    [Function intent]
    Async version of specific knowledge base loading with Context integration.
    
    [Design principles]
    Flexible knowledge base loading supporting multiple storage locations.
    Uses Context for detailed error reporting and progress updates.
    
    [Implementation details]
    Searches git-clones and pdf-knowledge directories for specified KB file,
    loads content with proper encoding handling and Context logging.
    
    Args:
        kb_name: Name of knowledge base to load (with or without _kb suffix)
        ctx: FastMCP Context for logging and error reporting
        
    Returns:
        Knowledge base content
        
    Raises:
        FileNotFoundError: When specified knowledge base cannot be found
    """
    
    # Normalize KB name (ensure _kb suffix)
    if not kb_name.endswith("_kb"):
        kb_name = f"{kb_name}_kb"
    
    kb_filename = f"{kb_name}.md"
    
    # Search locations
    search_paths = [
        Path(".knowledge/git-clones") / kb_filename,
        Path(".knowledge/pdf-knowledge") / kb_filename
    ]
    
    await ctx.info(f"Searching for knowledge base: {kb_name}")
    
    for kb_path in search_paths:
        if kb_path.exists():
            try:
                await ctx.info(f"Found knowledge base at: {kb_path}")
                with open(kb_path, "r", encoding="utf-8") as f:
                    content = f.read()
                await ctx.info(f"Successfully loaded {len(content)} characters from {kb_name}")
                return content
            except Exception as e:
                error_msg = f"Failed to read knowledge base {kb_name}: {str(e)}"
                await ctx.error(error_msg)
                raise ValueError(error_msg)
    
    # KB not found in any location
    error_msg = f"Knowledge base '{kb_name}' not found in .knowledge/ directories"
    await ctx.error(error_msg)
    raise FileNotFoundError(error_msg)

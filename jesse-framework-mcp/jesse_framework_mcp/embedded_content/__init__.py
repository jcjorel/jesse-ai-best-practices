"""
JESSE Framework Embedded Content Module

This module contains all JESSE framework rules and workflows embedded at build time
for MCP server distribution. Content is copied from artifacts/ directory during build.
"""

import os
from pathlib import Path
from typing import Dict, List

# Module path for accessing embedded content files
_CONTENT_DIR = Path(__file__).parent


def get_embedded_file_content(filename: str) -> str:
    """
    Get content of an embedded file.
    
    Args:
        filename: Name of the embedded file (e.g., 'JESSE_KNOWLEDGE_MANAGEMENT.md')
        
    Returns:
        File content as string
        
    Raises:
        FileNotFoundError: When requested file is not found in embedded content
    """
    file_path = _CONTENT_DIR / filename
    
    if not file_path.exists():
        available_files = list_embedded_files()
        raise FileNotFoundError(
            f"Embedded file not found: {filename}. "
            f"Available files: {available_files}"
        )
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def get_embedded_workflow_content(workflow_filename: str) -> str:
    """
    Get content of an embedded workflow file.
    
    Args:
        workflow_filename: Name of the workflow file (e.g., 'jesse_wip_task_create.md')
        
    Returns:
        Workflow content as string
        
    Raises:
        FileNotFoundError: When requested workflow is not found
    """
    workflow_path = _CONTENT_DIR / "workflows" / workflow_filename
    
    if not workflow_path.exists():
        available_workflows = list_embedded_workflows()
        raise FileNotFoundError(
            f"Embedded workflow not found: {workflow_filename}. "
            f"Available workflows: {available_workflows}"
        )
    
    with open(workflow_path, 'r', encoding='utf-8') as f:
        return f.read()


def list_embedded_files() -> List[str]:
    """
    List all embedded JESSE rule files.
    
    Returns:
        List of embedded JESSE rule filenames
    """
    if not _CONTENT_DIR.exists():
        return []
    
    return [f.name for f in _CONTENT_DIR.iterdir() 
            if f.is_file() and f.name.endswith('.md')]


def list_embedded_workflows() -> List[str]:
    """
    List all embedded workflow files.
    
    Returns:
        List of embedded workflow filenames
    """
    workflows_dir = _CONTENT_DIR / "workflows"
    if not workflows_dir.exists():
        return []
    
    return [f.name for f in workflows_dir.iterdir() 
            if f.is_file() and f.name.endswith('.md')]


def get_embedded_content_info() -> Dict[str, any]:
    """
    Get information about embedded content.
    
    Returns:
        Dictionary with embedded content statistics and file lists
    """
    rules = list_embedded_files()
    workflows = list_embedded_workflows()
    
    return {
        "content_directory": str(_CONTENT_DIR),
        "rules_count": len(rules),
        "workflows_count": len(workflows),
        "rules": rules,
        "workflows": workflows,
        "total_files": len(rules) + len(workflows)
    }

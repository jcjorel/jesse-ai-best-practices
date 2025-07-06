"""
JESSE Framework Embedded Content Module

This module contains the embedded JESSE framework rules and workflows
copied from the artifacts/ directory during the build process.
"""

import os
from pathlib import Path
from typing import List, Dict

# Path to this embedded content directory
EMBEDDED_CONTENT_DIR = Path(__file__).parent


def get_jesse_rule_content(rule_name: str) -> str:
    """
    Get the content of a JESSE rule file.
    
    Args:
        rule_name: Name of the rule (e.g., 'knowledge_management', 'hints')
        
    Returns:
        Content of the rule file
        
    Raises:
        FileNotFoundError: If the rule file doesn't exist
    """
    rule_file = EMBEDDED_CONTENT_DIR / f"JESSE_{rule_name.upper()}.md"
    
    if not rule_file.exists():
        raise FileNotFoundError(f"JESSE rule file not found: {rule_file}")
    
    return rule_file.read_text(encoding='utf-8')


def get_workflow_content(workflow_name: str) -> str:
    """
    Get the content of a workflow file.
    
    Args:
        workflow_name: Name of the workflow file (with or without .md extension)
        
    Returns:
        Content of the workflow file
        
    Raises:
        FileNotFoundError: If the workflow file doesn't exist
    """
    if not workflow_name.endswith('.md'):
        workflow_name += '.md'
    
    workflow_file = EMBEDDED_CONTENT_DIR / "workflows" / workflow_name
    
    if not workflow_file.exists():
        raise FileNotFoundError(f"Workflow file not found: {workflow_file}")
    
    return workflow_file.read_text(encoding='utf-8')


def list_jesse_rules() -> List[str]:
    """List all available JESSE rule names."""
    rules = []
    for file_path in EMBEDDED_CONTENT_DIR.glob("JESSE_*.md"):
        # Extract rule name from filename (e.g., "JESSE_KNOWLEDGE_MANAGEMENT.md" -> "knowledge_management")
        rule_name = file_path.stem.replace("JESSE_", "").lower()
        rules.append(rule_name)
    return sorted(rules)


def list_workflows() -> List[str]:
    """List all available workflow files."""
    workflows_dir = EMBEDDED_CONTENT_DIR / "workflows"
    if not workflows_dir.exists():
        return []
    
    workflows = []
    for file_path in workflows_dir.glob("*.md"):
        workflows.append(file_path.name)
    return sorted(workflows)


def get_all_embedded_files() -> Dict[str, str]:
    """Get a dictionary of all embedded files and their content."""
    files = {}
    
    # Add JESSE rules
    for rule_name in list_jesse_rules():
        files[f"JESSE_{rule_name.upper()}.md"] = get_jesse_rule_content(rule_name)
    
    # Add workflows
    for workflow_name in list_workflows():
        files[f"workflows/{workflow_name}"] = get_workflow_content(workflow_name)
    
    return files

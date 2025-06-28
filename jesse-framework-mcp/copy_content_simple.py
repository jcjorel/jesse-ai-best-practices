#!/usr/bin/env python3
"""
Simple script to copy JESSE content for testing - no hatchling dependencies
"""

import os
import shutil
from pathlib import Path
from typing import Optional
import sys

# Import centralized rule configuration
sys.path.insert(0, str(Path(__file__).parent / "jesse_framework_mcp"))
from constants import get_jesse_rule_files


def copy_jesse_content() -> None:
    """Copy complete JESSE framework (rules + workflows) from artifacts/ to embedded_content/."""
    
    # Find the JESSE framework project root
    current_dir = Path.cwd()
    jesse_project_root = find_jesse_project_root(current_dir)
    
    if not jesse_project_root:
        raise ValueError(
            "Could not locate JESSE project with artifacts/ directory. "
            "Ensure this build is run from within the JESSE framework project hierarchy."
        )
    
    print(f"Found JESSE project root: {jesse_project_root}")
    
    # Source: artifacts/.clinerules/
    source_dir = jesse_project_root / "artifacts" / ".clinerules"
    
    if not source_dir.exists():
        raise FileNotFoundError(
            f"JESSE artifacts directory not found: {source_dir}. "
            "Ensure artifacts/.clinerules/ exists in project root."
        )
    
    # Destination: embedded_content/
    dest_dir = Path("jesse_framework_mcp") / "embedded_content"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Copying JESSE content from {source_dir} to {dest_dir}")
    
    # Copy JESSE rules
    copy_jesse_rules(source_dir, dest_dir)
    
    # Copy all workflows
    copy_jesse_workflows(source_dir, dest_dir)
    
    print("JESSE framework content copying completed successfully")


def copy_jesse_rules(source_dir: Path, dest_dir: Path) -> None:
    """Copy all JESSE_*.md rule files from source to destination directory."""
    
    jesse_rule_files = get_jesse_rule_files()
    
    print(f"Copying {len(jesse_rule_files)} JESSE rule files...")
    
    for file_name in jesse_rule_files:
        source_file = source_dir / file_name
        dest_file = dest_dir / file_name
        
        if source_file.exists():
            shutil.copy2(source_file, dest_file)
            print(f"  ✓ Copied {file_name}")
        else:
            raise FileNotFoundError(
                f"Required JESSE rule file not found: {source_file}. "
                f"Ensure {file_name} exists in artifacts/.clinerules/"
            )
    
    print(f"Successfully copied all {len(jesse_rule_files)} JESSE rule files")


def copy_jesse_workflows(source_dir: Path, dest_dir: Path) -> None:
    """Copy entire workflows/ directory from source to destination with all .md files."""
    
    source_workflows = source_dir / "workflows"
    dest_workflows = dest_dir / "workflows"
    
    if source_workflows.exists() and source_workflows.is_dir():
        # Copy entire workflows directory
        shutil.copytree(source_workflows, dest_workflows, dirs_exist_ok=True)
        
        # Count copied workflow files for verification
        workflow_files = list(dest_workflows.glob("*.md"))
        workflow_count = len(workflow_files)
        
        print(f"  ✓ Copied {workflow_count} workflow files to embedded_content/workflows/")
        
        # List copied workflows for verification
        for workflow_file in sorted(workflow_files):
            print(f"    - {workflow_file.name}")
            
    else:
        raise FileNotFoundError(
            f"Workflows directory not found: {source_workflows}. "
            "Ensure artifacts/.clinerules/workflows/ exists with workflow .md files."
        )
    
    print("Successfully copied all JESSE workflow files")


def find_jesse_project_root(start_path: Path) -> Optional[Path]:
    """Locate JESSE project root by searching for artifacts/.clinerules/ directory structure."""
    
    current = start_path.resolve()
    
    # Traverse upward through directory hierarchy
    while current != current.parent:  # Stop at filesystem root
        artifacts_dir = current / "artifacts" / ".clinerules"
        
        if artifacts_dir.exists() and artifacts_dir.is_dir():
            return current
            
        current = current.parent
    
    return None


if __name__ == "__main__":
    print("Testing JESSE content copying...")
    copy_jesse_content()
    print("Test completed successfully")

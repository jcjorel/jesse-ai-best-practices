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
# Build-time script to copy complete JESSE framework (rules + workflows) from 
# artifacts/ directory to embedded_content/ for MCP server packaging.
###############################################################################
# [Source file design principles]
# - Single source of truth: copies from artifacts/ at build time only
# - Defensive programming with descriptive error messages on failure
# - Complete framework copying: both rules and workflows included
# - Build system integration via hatch build hook
###############################################################################
# [Source file constraints]
# - Must locate JESSE project root containing artifacts/ directory
# - Requires artifacts/.clinerules/ structure with JESSE_*.md files
# - Must handle missing files or directories with clear error messages
# - Creates embedded_content/ structure for runtime access
###############################################################################
# [Dependencies]
# system:os - Operating system interface for path operations
# system:shutil - High-level file operations for copying
# system:pathlib.Path - Object-oriented filesystem paths
# codebase:../artifacts/.clinerules/ - Source JESSE framework files
###############################################################################
# [GenAI tool change history]
# 2025-06-27T21:02:00Z : Eliminated hardcoded JESSE rule filenames by CodeAssistant
# * Replaced hardcoded jesse_rule_files list with get_jesse_rule_files() import
# * Added sys.path manipulation to import from constants module
# * Centralized rule configuration for build process
# 2025-06-27T01:22:00Z : Initial build script implementation by CodeAssistant
# * Created complete JESSE framework copying logic
# * Implemented defensive error handling for missing files
# * Added support for both rules and workflows copying
###############################################################################

import os
import shutil
from pathlib import Path
from typing import Optional, Any, Dict

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

# Import centralized rule configuration
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "jesse_framework_mcp"))
from constants import get_jesse_rule_files


def copy_jesse_content() -> None:
    """
    [Function intent]
    Copy complete JESSE framework (rules + workflows) from artifacts/ to embedded_content/.
    
    [Design principles]
    Single source of truth approach - copies from artifacts/ at build time only.
    Defensive programming with clear error messages for any missing components.
    
    [Implementation details]
    Locates JESSE project root, copies JESSE_*.md rules and entire workflows/ directory
    to embedded_content/ structure for runtime embedding in MCP server package.
    
    Raises:
        ValueError: When JESSE project root cannot be located
        FileNotFoundError: When required JESSE files or directories are missing
    """
    
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
    """
    [Function intent]
    Copy all JESSE_*.md rule files from source to destination directory.
    
    [Design principles]
    Explicit file list ensures only intended rule files are copied.
    Defensive error handling for each individual file with descriptive messages.
    
    [Implementation details]
    Iterates through predefined list of JESSE rule files, copies each with
    metadata preservation, reports success/failure for each file.
    
    Args:
        source_dir: Source directory containing JESSE_*.md files
        dest_dir: Destination directory for embedded content
        
    Raises:
        FileNotFoundError: When any required JESSE rule file is missing
    """
    
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
    """
    [Function intent]
    Copy entire workflows/ directory from source to destination with all .md files.
    
    [Design principles]
    Complete workflow directory copying to ensure no workflow files are missed.
    Preserves directory structure and file metadata during copying process.
    
    [Implementation details]
    Uses shutil.copytree to recursively copy workflows/ directory, counts
    resulting .md files for verification, handles directory creation.
    
    Args:
        source_dir: Source directory containing workflows/ subdirectory
        dest_dir: Destination directory for embedded content
        
    Raises:
        FileNotFoundError: When workflows/ directory is missing from source
    """
    
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
    """
    [Function intent]
    Locate JESSE project root by searching for artifacts/.clinerules/ directory structure.
    
    [Design principles]
    Traverses directory hierarchy upward to find project root marker.
    Returns None rather than raising exception to allow caller error handling.
    
    [Implementation details]
    Starts from given path, checks each parent directory for artifacts/.clinerules/
    existence, stops at filesystem root to prevent infinite recursion.
    
    Args:
        start_path: Starting directory path for upward search
        
    Returns:
        Path to JESSE project root if found, None otherwise
    """
    
    current = start_path.resolve()
    
    # Traverse upward through directory hierarchy
    while current != current.parent:  # Stop at filesystem root
        artifacts_dir = current / "artifacts" / ".clinerules"
        
        if artifacts_dir.exists() and artifacts_dir.is_dir():
            return current
            
        current = current.parent
    
    return None


class JesseBuildHook(BuildHookInterface):
    """
    [Class intent]
    Hatchling build hook to copy JESSE framework content during package build.
    
    [Design principles]
    Integrates with Hatchling build process as custom hook.
    Provides clear separation between build logic and hook interface.
    
    [Implementation details]
    Implements BuildHookInterface for Hatchling integration, delegates to
    copy_jesse_content() for actual copying logic during build process.
    """
    
    PLUGIN_NAME = "jesse_build_hook"
    
    def initialize(self, version: str, build_data: Dict[str, Any]) -> None:
        """
        [Function intent]
        Initialize the build hook and copy JESSE framework content.
        
        [Design principles]
        Called by Hatchling during build initialization phase.
        Delegates to copy_jesse_content() for actual work.
        
        [Implementation details]
        Hatchling calls this method during build process, we use it to
        trigger JESSE content copying from artifacts/ directory.
        
        Args:
            version: Build version information
            build_data: Build metadata from Hatchling
        """
        
        print("=== JESSE Framework MCP Server Build Hook ===")
        print("Copying JESSE framework content from artifacts/ directory...")
        
        try:
            copy_jesse_content()
            print("=== Build hook completed successfully ===")
        except Exception as e:
            print(f"=== Build hook failed: {str(e)} ===")
            raise


# Legacy entry point for backward compatibility
def hatch_build_hook(build_data: dict, **kwargs) -> None:
    """
    [Function intent]
    Legacy entry point for Hatchling build system hook compatibility.
    
    [Design principles]
    Maintains backward compatibility with older Hatchling versions.
    Delegates to copy_jesse_content() for actual copying logic.
    
    [Implementation details]
    Called by older Hatchling versions during build process, delegates to
    copy_jesse_content() for actual copying logic.
    
    Args:
        build_data: Build metadata from Hatchling build system
        **kwargs: Additional build system parameters
    """
    
    print("=== JESSE Framework MCP Server Build Hook (Legacy) ===")
    print("Copying JESSE framework content from artifacts/ directory...")
    
    try:
        copy_jesse_content()
        print("=== Build hook completed successfully ===")
    except Exception as e:
        print(f"=== Build hook failed: {str(e)} ===")
        raise


# Direct execution for testing
if __name__ == "__main__":
    print("Testing JESSE content copying...")
    copy_jesse_content()
    print("Test completed successfully")

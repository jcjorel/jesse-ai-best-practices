###############################################################################
# [GenAI coding tool directive] 
# - Standard header with intent, design principles, constraints
# - Track all modifications in history section
###############################################################################
# [Source file intent]
# Dedicated gitignore compliance management for JESSE Framework MCP server.
# Provides intelligent compliance checking and context-optimized session initialization.
###############################################################################
# [Source file design principles]  
# - Smart feature detection (only validate patterns for active features)
# - Conditional output (no content when compliant, detailed guidance when issues found)
# - Precise remediation (exact copy-paste solutions for non-compliance)
# - Separation of concerns (all gitignore logic centralized)
###############################################################################
# [Source file constraints]
# - Must maintain backward compatibility with existing jesse://project/gitignore-files resource
# - Compliance detection must be efficient (no heavy file system operations)
# - Pattern matching must be exact (byte-perfect validation against requirements)
# - HTTP formatting must match existing MCP response patterns
###############################################################################
# [Source file history]
# - 2025-06-29 22:33:30 UTC - Initial creation with smart compliance system
###############################################################################

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Set
from enum import Enum

from fastmcp import Context
from ..main import server
from ..helpers.http_formatter import format_http_section, format_multi_section_response, ContentCriticality, HttpPath
from ..helpers.project_root import get_project_root, ensure_project_root, get_project_relative_path


class ComplianceIssueType(Enum):
    """Types of gitignore compliance issues that can be detected."""
    MISSING_FILE = "missing_file"
    MISSING_PATTERNS = "missing_patterns" 
    CONFLICTING_PATTERNS = "conflicting_patterns"
    INVALID_CONTENT = "invalid_content"


@dataclass
class ComplianceIssue:
    """Represents a specific gitignore compliance issue."""
    file_path: str
    issue_type: ComplianceIssueType
    description: str
    required_patterns: List[str]
    current_patterns: List[str]
    remediation_action: str


@dataclass
class GitignoreComplianceResult:
    """Results of gitignore compliance assessment."""
    is_compliant: bool
    active_features: Set[str]  # {'git-clones', 'pdf-knowledge'}
    issues: List[ComplianceIssue]
    remediation_guidance: Optional[str] = None
    
    @property
    def has_issues(self) -> bool:
        return len(self.issues) > 0


class FeatureDetector:
    """Detects which JESSE Framework features are active and require gitignore patterns."""
    
    @staticmethod
    def detect_active_features() -> Set[str]:
        """Detect all active features requiring gitignore compliance."""
        features = set()
        
        # Get project root for proper path resolution
        project_root = get_project_root()
        if not project_root:
            # No project root found - no features can be active
            return features
        
        # Git clones: check for subdirectories in .knowledge/git-clones/
        if FeatureDetector.is_git_clones_active(project_root):
            features.add('git-clones')
            
        # PDF knowledge: check for .pdf files in .knowledge/pdf-knowledge/
        if FeatureDetector.is_pdf_knowledge_active(project_root):
            features.add('pdf-knowledge')
        
        return features
    
    @staticmethod
    def is_git_clones_active(project_root: Path) -> bool:
        """Check if .knowledge/git-clones/ contains repositories."""
        git_clones_dir = project_root / ".knowledge" / "git-clones"
        if not git_clones_dir.exists():
            return False
            
        # Check for subdirectories (actual git clones)
        try:
            for item in git_clones_dir.iterdir():
                if (item.is_dir() and 
                    not item.name.startswith('.') and 
                    item.name != 'README.md'):
                    return True
        except (OSError, PermissionError):
            pass
        
        return False
        
    @staticmethod
    def is_pdf_knowledge_active(project_root: Path) -> bool:
        """Check if .knowledge/pdf-knowledge/ contains PDF files."""
        pdf_dir = project_root / ".knowledge" / "pdf-knowledge"
        if not pdf_dir.exists():
            return False
            
        # Check for .pdf files
        try:
            for item in pdf_dir.iterdir():
                if item.is_file() and item.suffix.lower() == '.pdf':
                    return True
        except (OSError, PermissionError):
            pass
        
        return False


class GitignoreValidator:
    """Validates gitignore files against JESSE Framework compliance requirements."""
    
    def __init__(self):
        self.expected_patterns = {
            'git-clones': GIT_CLONES_PATTERNS,
            'pdf-knowledge': PDF_KNOWLEDGE_PATTERNS
        }
        self.mandatory_files = MANDATORY_FILES
        
        # Get project root for proper path resolution
        self.project_root = get_project_root()
    
    def validate_compliance(self) -> GitignoreComplianceResult:
        """Main compliance assessment method."""
        issues = []
        active_features = FeatureDetector.detect_active_features()
        
        # If no project root, we can't validate anything
        if not self.project_root:
            issues.append(ComplianceIssue(
                file_path="project-root",
                issue_type=ComplianceIssueType.MISSING_FILE,
                description="No project root detected - cannot validate gitignore compliance",
                required_patterns=[],
                current_patterns=[],
                remediation_action="Set JESSE_PROJECT_ROOT environment variable or work in a Git repository"
            ))
            return GitignoreComplianceResult(
                is_compliant=False,
                active_features=active_features,
                issues=issues,
                remediation_guidance="Project root must be detected before gitignore compliance can be validated."
            )
        
        # Check mandatory files exist (using project root context)
        for relative_file_path, description in self.mandatory_files:
            absolute_file_path = self.project_root / relative_file_path
            if not absolute_file_path.exists():
                issues.append(ComplianceIssue(
                    file_path=relative_file_path,
                    issue_type=ComplianceIssueType.MISSING_FILE,
                    description=f"Mandatory gitignore file missing: {description}",
                    required_patterns=[],
                    current_patterns=[],
                    remediation_action=f"Create file: {absolute_file_path}"
                ))
        
        # Check patterns for active features (using project root context)
        for feature in active_features:
            if feature in self.expected_patterns:
                required_patterns = self.expected_patterns[feature]
                
                # Check main .gitignore file for feature patterns
                if feature == 'git-clones' or feature == 'pdf-knowledge':
                    gitignore_path = self.project_root / ".gitignore"
                    issues.extend(self.check_file_patterns(
                        str(gitignore_path), 
                        required_patterns,
                        ".gitignore"  # display name
                    ))
        
        # Generate remediation guidance if issues found
        remediation_guidance = None
        if issues:
            remediation_guidance = self.generate_remediation_guidance(issues)
        
        return GitignoreComplianceResult(
            is_compliant=len(issues) == 0,
            active_features=active_features,
            issues=issues,
            remediation_guidance=remediation_guidance
        )
    
    def check_file_patterns(self, file_path: str, required_patterns: List[str], display_name: str = None) -> List[ComplianceIssue]:
        """Check specific file for required patterns with enhanced diagnostics."""
        issues = []
        display_path = display_name or file_path
        
        if not Path(file_path).exists():
            issues.append(ComplianceIssue(
                file_path=display_path,
                issue_type=ComplianceIssueType.MISSING_FILE,
                description=f"Required gitignore file missing: {display_path}",
                required_patterns=required_patterns,
                current_patterns=[],
                remediation_action=f"Create file: {file_path}"
            ))
            return issues
        
        try:
            current_patterns = self.parse_gitignore_file(file_path)
            missing_patterns = []
            
            # Enhanced pattern matching with debugging
            for pattern in required_patterns:
                if pattern not in current_patterns:
                    missing_patterns.append(pattern)
            
            if missing_patterns:
                # Generate detailed diagnostic information
                diagnostic_info = self.generate_pattern_diagnostic(
                    file_path, current_patterns, required_patterns, missing_patterns
                )
                
                issues.append(ComplianceIssue(
                    file_path=display_path,
                    issue_type=ComplianceIssueType.MISSING_PATTERNS,
                    description=f"Missing required patterns in {display_path}.\n\nDiagnostic:\n{diagnostic_info}",
                    required_patterns=missing_patterns,
                    current_patterns=current_patterns,
                    remediation_action=f"Add missing patterns to {display_path}"
                ))
        
        except Exception as e:
            issues.append(ComplianceIssue(
                file_path=display_path,
                issue_type=ComplianceIssueType.INVALID_CONTENT,
                description=f"Error reading {display_path}: {str(e)}",
                required_patterns=required_patterns,
                current_patterns=[],
                remediation_action=f"Fix file encoding/permissions: {file_path}"
            ))
        
        return issues
    
    def parse_gitignore_file(self, file_path: str) -> List[str]:
        """Parse gitignore file into clean pattern list."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        
        # Split into lines and normalize
        lines = []
        for line in content.splitlines():
            # Preserve original line (including comments) for exact matching
            lines.append(line)
        
        return lines
    
    def generate_pattern_diagnostic(self, file_path: str, current_patterns: List[str], 
                                    required_patterns: List[str], missing_patterns: List[str]) -> str:
        """Generate detailed diagnostic information for pattern matching issues."""
        diagnostic_lines = []
        
        diagnostic_lines.append(f"File checked: {file_path}")
        diagnostic_lines.append(f"Total lines in file: {len(current_patterns)}")
        diagnostic_lines.append(f"Required patterns: {len(required_patterns)}")
        diagnostic_lines.append(f"Missing patterns: {len(missing_patterns)}")
        diagnostic_lines.append("")
        
        # Show what patterns are missing
        diagnostic_lines.append("MISSING PATTERNS:")
        for i, pattern in enumerate(missing_patterns, 1):
            diagnostic_lines.append(f"  {i}. '{pattern}'")
        diagnostic_lines.append("")
        
        # Show similar patterns that might be close matches
        diagnostic_lines.append("SIMILAR PATTERNS FOUND (potential matches):")
        similar_found = False
        for missing_pattern in missing_patterns:
            for line_num, current_pattern in enumerate(current_patterns, 1):
                # Check for similar patterns (case insensitive, whitespace tolerant)
                if (missing_pattern.lower().strip() in current_pattern.lower().strip() or 
                    current_pattern.lower().strip() in missing_pattern.lower().strip()):
                    diagnostic_lines.append(f"  Line {line_num}: '{current_pattern}' (similar to '{missing_pattern}')")
                    similar_found = True
        
        if not similar_found:
            diagnostic_lines.append("  No similar patterns found")
        
        diagnostic_lines.append("")
        diagnostic_lines.append("CURRENT FILE CONTENT (first 10 lines):")
        for i, line in enumerate(current_patterns[:10], 1):
            diagnostic_lines.append(f"  {i:2d}: '{line}'")
        
        if len(current_patterns) > 10:
            diagnostic_lines.append(f"  ... ({len(current_patterns) - 10} more lines)")
        
        return "\n".join(diagnostic_lines)
    
    def generate_remediation_guidance(self, issues: List[ComplianceIssue]) -> str:
        """Generate precise remediation instructions."""
        guidance_sections = []
        
        for issue in issues:
            if issue.issue_type == ComplianceIssueType.MISSING_FILE:
                guidance_sections.append(f"""
### Missing File: {issue.file_path}

**Issue**: {issue.description}

**Action Required**: Create the file with the following content:

```
{chr(10).join(issue.required_patterns)}
```
""")
            elif issue.issue_type == ComplianceIssueType.MISSING_PATTERNS:
                guidance_sections.append(f"""
### Missing Patterns: {issue.file_path}

**Issue**: {issue.description}

**Action Required**: Add the following lines to {issue.file_path}:

```
{chr(10).join(issue.required_patterns)}
```
""")
            elif issue.issue_type == ComplianceIssueType.INVALID_CONTENT:
                guidance_sections.append(f"""
### Invalid Content: {issue.file_path}

**Issue**: {issue.description}

**Action Required**: {issue.remediation_action}
""")
        
        return "\n".join(guidance_sections)


# === PATTERN DEFINITIONS ===

GIT_CLONES_PATTERNS = [
    "# JESSE AI Framework - Knowledge Management System",
    "# Ignore actual git clone directories but keep knowledge base files",
    ".knowledge/git-clones/*/",
    "!.knowledge/git-clones/*.md", 
    "!.knowledge/git-clones/README.md"
]

PDF_KNOWLEDGE_PATTERNS = [
    "# Knowledge Management System - PDF Documents",
    "# Ignore actual PDF files but keep knowledge base files", 
    ".knowledge/pdf-knowledge/*.pdf",
    "!.knowledge/pdf-knowledge/*.md",
    "!.knowledge/pdf-knowledge/README.md"
]

MANDATORY_FILES = [
    (".gitignore", "Project Root Directory"),
    (".knowledge/git-clones/.gitignore", "Git Clones Knowledge Management")
]


# === MCP RESOURCES ===

@server.resource("jesse://project/gitignore-compliance")
async def get_gitignore_compliance_status(ctx: Context) -> str:
    """
    Smart compliance resource - only outputs when issues require attention.
    
    Returns:
        - Empty string when fully compliant (major context reduction)
        - Detailed guidance when non-compliances found
        - Error information when validation fails
    """
    try:
        validator = GitignoreValidator()
        result = validator.validate_compliance()
        
        if result.is_compliant:
            # Fully compliant - return empty string for massive context reduction
            return ""
        
        # Non-compliant - provide detailed guidance
        sections = []
        
        # Compliance status section
        sections.append(format_http_section(
            status_code=241,
            status_message="Gitignore Compliance Issues Found",
            location=HttpPath("jesse://project/gitignore-compliance"),
            content_type="text/markdown",
            criticality=ContentCriticality.CRITICAL,
            description="Gitignore Compliance Issues Requiring Attention",
            section_type="gitignore-compliance",
            writable=False,
            content=f"""# Gitignore Compliance Issues

## Active Features Detected
{', '.join(sorted(result.active_features)) if result.active_features else 'None'}

## Issues Found
{len(result.issues)} compliance issue(s) detected.

{result.remediation_guidance or 'No specific remediation guidance available.'}

## Next Steps
1. Review the remediation guidance above
2. Apply the suggested changes to your gitignore files
3. Re-run session initialization to verify compliance
"""
        ))
        
        return format_multi_section_response(*sections)
    
    except Exception as e:
        # Error in compliance checking - provide fallback
        sections = []
        sections.append(format_http_section(
            status_code=500,
            status_message="Gitignore Compliance Check Failed",
            location=HttpPath("jesse://project/gitignore-compliance"),
            content_type="text/markdown",
            criticality=ContentCriticality.INFORMATIONAL,
            description="Error During Compliance Validation",
            section_type="gitignore-compliance-error",
            writable=False,
            content=f"""# Gitignore Compliance Check Error

An error occurred while checking gitignore compliance:

```
{str(e)}
```

Falling back to basic gitignore file display for this session.
"""
        ))
        
        return format_multi_section_response(sections)


@server.resource("jesse://project/gitignore-files")
async def get_project_gitignore_files(ctx: Context) -> str:
    """
    Legacy gitignore files resource (moved from project_resources.py).
    Maintains backward compatibility for direct file access.
    Returns mandatory and existing optional .gitignore contents as HTTP sections.
    """
    await ctx.info("Scanning project .gitignore files")
    
    try:
        # Define mandatory vs optional .gitignore locations
        mandatory_locations = [
            ("file://{PROJECT_ROOT}/.gitignore", "Project Root Directory"),
            ("file://{PROJECT_ROOT}/.knowledge/git-clones/.gitignore", "Git Clones Knowledge Management")
        ]
        
        optional_locations = [
            ("file://{PROJECT_ROOT}/.coding_assistant/.gitignore", "Coding Assistant Artifacts"),
            ("file://{PROJECT_ROOT}/.knowledge/.gitignore", "Knowledge Management System"),
            ("file://{PROJECT_ROOT}/.clinerules/.gitignore", "Project-Specific Rules")
        ]
        
        sections = []
        
        # Process mandatory locations (always included)
        for location_path, description in mandatory_locations:
            await ctx.info(f"Checking mandatory .gitignore at {location_path}")
            
            # Create HttpPath for this location
            gitignore_path = HttpPath(location_path, writable=True)
            
            try:
                if gitignore_path.exists() and gitignore_path.is_file():
                    # File exists, read its content
                    content = gitignore_path.read_text(encoding='utf-8')
                    if not content.strip():
                        # File exists but is empty
                        content = f"# Empty .gitignore file at {location_path}\n# Add patterns here to ignore files and directories"
                    
                    await ctx.info(f"Found mandatory .gitignore at {description}: {len(content)} characters")
                    criticality = ContentCriticality.INFORMATIONAL
                    file_status = "exists"
                else:
                    # Mandatory file does not exist - CRITICAL warning
                    content = f"""# 🚨 CRITICAL: MANDATORY .gitignore FILE MISSING 🚨
# Location: {location_path}
# Status: REQUIRED FILE NOT FOUND
# Action Required: CREATE THIS FILE IMMEDIATELY
# Impact: Project may commit sensitive files without proper ignore patterns
# 
# This is a mandatory .gitignore file that must exist for proper project management.
# Please create this file and add appropriate ignore patterns."""
                    
                    await ctx.info(f"Missing mandatory .gitignore at {description}")
                    criticality = ContentCriticality.CRITICAL
                    file_status = "missing-critical"
                
                # Format as HTTP section with appropriate criticality
                section = format_http_section(
                    content=content,
                    content_type="text/plain",
                    criticality=criticality,
                    description=f"Mandatory .gitignore File from {description}",
                    section_type="gitignore-mandatory",
                    location=gitignore_path,
                    writable=True,
                    additional_headers={
                        "File-Status": file_status,
                        "Directory-Context": description,
                        "File-Type": "mandatory"
                    }
                )
                
                sections.append(section)
                
            except Exception as e:
                # Handle individual mandatory file errors gracefully
                await ctx.error(f"Error accessing mandatory .gitignore at {location_path}: {str(e)}")
                
                error_content = f"""# 🚨 CRITICAL: ERROR ACCESSING MANDATORY .gitignore FILE 🚨
# Location: {location_path}
# Error: {str(e)}
# Action Required: FIX FILE ACCESS ISSUE IMMEDIATELY
# Please check file permissions and path accessibility for this mandatory file."""
                
                section = format_http_section(
                    content=error_content,
                    content_type="text/plain",
                    criticality=ContentCriticality.CRITICAL,
                    description=f"Mandatory .gitignore File Error from {description}",
                    section_type="gitignore-error-critical",
                    location=gitignore_path,
                    writable=True,
                    additional_headers={
                        "File-Status": "error-critical",
                        "Error-Type": type(e).__name__,
                        "Directory-Context": description,
                        "File-Type": "mandatory"
                    }
                )
                
                sections.append(section)
        
        # Process optional locations (only if they exist)
        for location_path, description in optional_locations:
            await ctx.info(f"Checking optional .gitignore at {location_path}")
            
            # Create HttpPath for this location
            gitignore_path = HttpPath(location_path, writable=True)
            
            try:
                if gitignore_path.exists() and gitignore_path.is_file():
                    # Optional file exists, include it
                    content = gitignore_path.read_text(encoding='utf-8')
                    if not content.strip():
                        # File exists but is empty
                        content = f"# Empty .gitignore file at {location_path}\n# Add patterns here to ignore files and directories"
                    
                    await ctx.info(f"Found optional .gitignore at {description}: {len(content)} characters")
                    
                    # Format as HTTP section with INFORMATIONAL criticality
                    section = format_http_section(
                        content=content,
                        content_type="text/plain",
                        criticality=ContentCriticality.INFORMATIONAL,
                        description=f"Optional .gitignore File from {description}",
                        section_type="gitignore-optional",
                        location=gitignore_path,
                        writable=True,
                        additional_headers={
                            "File-Status": "exists",
                            "Directory-Context": description,
                            "File-Type": "optional"
                        }
                    )
                    
                    sections.append(section)
                else:
                    # Optional file does not exist - skip it (don't include in output)
                    await ctx.info(f"Skipping non-existent optional .gitignore at {description}")
                    
            except Exception as e:
                # Handle individual optional file errors gracefully (still skip, but log)
                await ctx.error(f"Error accessing optional .gitignore at {location_path}: {str(e)}")
                # Don't add error section for optional files - just skip them
        
        # Combine all sections into multi-part response
        if not sections:
            raise ValueError("No .gitignore file sections could be generated")
        
        await ctx.info(f"Generated {len(sections)} .gitignore file sections")
        
        return format_multi_section_response(*sections)
        
    except Exception as e:
        await ctx.error(f"Failed to build gitignore files resource: {str(e)}")
        raise ValueError(f"Gitignore files resource failed: {str(e)}")

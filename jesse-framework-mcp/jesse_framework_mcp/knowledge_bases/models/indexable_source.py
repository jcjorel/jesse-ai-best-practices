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
# Indexable source abstraction models for unified discovery framework.
# Defines structured representations of indexable content sources with associated
# handlers and metadata, enabling unified discovery and processing coordination.
###############################################################################
# [Source file design principles]
# - Clear separation between indexable sources and processing contexts
# - Handler abstraction hiding technical discovery implementation details  
# - Configuration-driven filtering supporting flexible indexing run customization
# - Metadata-driven processing enabling inconsistency detection and remediation
# - Immutable source definitions ensuring thread-safe discovery operations
###############################################################################
# [Source file constraints]
# - All source models must be serializable for debugging and persistence
# - Source identification must be unique and stable across discovery runs
# - Handler type mapping must be extensible for new content type support
# - Metadata structure must support various inconsistency types and remediation needs
###############################################################################
# [Dependencies]
# <system>: dataclasses - Immutable data structure definitions
# <system>: pathlib - Cross-platform path operations
# <system>: typing - Type annotations and generics support
# <system>: enum - Source type enumeration definitions
###############################################################################
# [GenAI tool change history]
# 2025-07-09T09:00:00Z : Initial indexable source abstraction models by CodeAssistant
# * Created IndexableSource dataclass for unified source representation
# * Added SourceType enum for standardized source type classification
# * Implemented SourceMetadata for inconsistency tracking and remediation planning
# * Designed extensible architecture supporting new content types and handlers
###############################################################################

"""
Indexable Source Abstraction Models.

This module defines the core abstractions for representing indexable content sources
in a unified discovery framework. It separates the concept of "what can be indexed"
from "how to process it", enabling clean orchestration and extensible architecture.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from enum import Enum


class SourceType(str, Enum):
    """
    [Enum intent]
    Standardized source types for indexable content classification.
    Enables handler routing and processing strategy selection based on content type.

    [Design principles]
    Extensible enumeration supporting new content types without breaking existing code.
    Clear type classification enabling automatic handler selection and routing.
    String-based enum for serialization compatibility and debugging clarity.

    [Implementation details]
    Each source type maps to a specific handler implementation.
    Source type detection drives discovery logic and processing strategy selection.
    Types are hierarchical (git-clone is a specialized form of directory processing).
    """
    PROJECT_BASE = "project-base"  # Whole project codebase indexing
    GIT_CLONE = "git-clone"        # Read-only git repository mirroring
    PDF_DOCUMENT = "pdf-document"   # PDF document processing
    MARKDOWN_DOC = "markdown-doc"   # Standalone markdown document
    WIP_TASK = "wip-task"          # Work-in-progress task directory
    GENERIC_DIR = "generic-dir"     # Generic directory processing


@dataclass(frozen=True)
class SourceMetadata:
    """
    [Class intent]
    Metadata about indexable source state and processing requirements.
    Tracks inconsistencies, missing files, orphaned content, and other
    remediation needs for metadata-driven execution planning.

    [Design principles]
    Immutable metadata ensuring consistent state during planning and execution phases.
    Comprehensive inconsistency tracking supporting automated remediation planning.
    Clear separation between source identification and source health status.
    Extensible metadata structure supporting various inconsistency types.

    [Implementation details]
    Missing files indicate content requiring initial processing or updates.
    Orphaned files indicate cleanup requirements for removed source content.
    Processing hints guide handler selection and optimization strategies.
    Health status enables filtering and prioritization during execution planning.
    """
    
    # Source health indicators
    is_healthy: bool = True
    last_discovered: Optional[str] = None  # ISO timestamp
    
    # Inconsistency tracking
    missing_files: List[Path] = field(default_factory=list)
    orphaned_files: List[Path] = field(default_factory=list)
    stale_files: List[Path] = field(default_factory=list)
    
    # Processing optimization hints
    estimated_file_count: int = 0
    estimated_size_mb: float = 0.0
    requires_llm_processing: bool = True
    
    # Handler-specific metadata
    handler_metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def needs_remediation(self) -> bool:
        """
        [Class method intent]
        Determines if source requires remediation based on detected inconsistencies.
        Used for execution planning and prioritization of processing operations.

        [Design principles]
        Clear remediation need identification enabling automated execution planning.
        Comprehensive inconsistency checking covering all tracked inconsistency types.
        Boolean decision simplifying conditional logic in orchestration workflows.

        [Implementation details]
        Checks for any non-empty inconsistency lists indicating remediation requirements.
        Missing files require creation, orphaned files require cleanup, stale files require updates.
        Returns True if any inconsistency type requires attention during execution.
        """
        return bool(self.missing_files or self.orphaned_files or self.stale_files)
    
    @property
    def remediation_summary(self) -> Dict[str, int]:
        """
        [Class method intent]
        Provides summary of remediation requirements for planning and reporting.
        Returns counts of each inconsistency type for execution plan sizing.

        [Design principles]
        Quantified remediation requirements enabling resource estimation and planning.
        Summary format compatible with execution plan generation and progress reporting.
        Clear categorization supporting different remediation strategies.

        [Implementation details]
        Counts each inconsistency type providing execution plan sizing information.
        Summary used in dry-run reporting and resource estimation calculations.
        Categories align with execution task types for consistent planning.
        """
        return {
            'missing_files': len(self.missing_files),
            'orphaned_files': len(self.orphaned_files),
            'stale_files': len(self.stale_files)
        }


@dataclass(frozen=True)
class IndexableSource:
    """
    [Class intent]
    Immutable representation of an indexable content source with associated handler.
    Provides unified abstraction over different content types enabling clean discovery
    and processing orchestration without exposing handler implementation details.

    [Design principles]
    Immutable source definition ensuring thread-safe discovery and planning operations.
    Handler abstraction hiding technical implementation details from orchestration layer.
    Unique source identification supporting consistent processing across discovery runs.
    Metadata integration enabling inconsistency detection and remediation planning.
    Extensible design supporting new content types without breaking existing orchestration.

    [Implementation details]
    Source ID uniquely identifies content across discovery runs for consistency.
    Source type enables automatic handler selection and processing strategy routing.
    Source path provides filesystem location for handler processing operations.
    Handler type string enables dynamic handler instantiation and capability routing.
    Metadata drives execution planning and processing optimization decisions.
    """
    
    # Source identification
    source_id: str          # Unique identifier (e.g., "git-clone:cline", "project-base:root")
    source_type: SourceType # Content type classification
    source_path: Path       # Filesystem location
    
    # Handler association
    handler_type: str       # Handler class identifier (e.g., "git-clone", "project-base")
    
    # Source metadata and state
    metadata: SourceMetadata = field(default_factory=SourceMetadata)
    
    # Configuration and filtering
    tags: Set[str] = field(default_factory=set)        # For filtering and categorization
    priority: int = 0                                   # For processing order (higher = first)
    enabled: bool = True                                # For configuration-based filtering
    
    @property
    def display_name(self) -> str:
        """
        [Class method intent]
        Provides human-readable display name for logging and user interface presentation.
        Combines source type and path information for clear source identification.

        [Design principles]
        Clear source identification supporting debugging and user feedback operations.
        Consistent naming format across different source types and content categories.
        Informative display supporting progress reporting and error identification.

        [Implementation details]
        Combines source type and source path name for human-readable identification.
        Format consistent across different source types for unified user experience.
        Used in logging messages, progress reports, and error identification.
        """
        return f"{self.source_type.value}:{self.source_path.name}"
    
    @property
    def needs_processing(self) -> bool:
        """
        [Class method intent]
        Determines if source requires processing based on metadata and configuration.
        Used for filtering and execution planning to optimize processing operations.

        [Design principles]
        Clear processing need determination enabling execution optimization and filtering.
        Multi-criteria evaluation considering both health status and remediation requirements.
        Boolean decision simplifying conditional logic in orchestration workflows.

        [Implementation details]
        Requires source to be enabled and either need remediation or be healthy for processing.
        Disabled sources are skipped regardless of remediation needs or health status.
        Health check ensures source is in processable state for successful execution.
        """
        return self.enabled and (self.metadata.needs_remediation or self.metadata.is_healthy)
    
    def with_metadata(self, metadata: SourceMetadata) -> 'IndexableSource':
        """
        [Class method intent]
        Creates new IndexableSource with updated metadata preserving immutability.
        Enables metadata updates during discovery and health checking operations.

        [Design principles]
        Immutable update pattern preserving thread safety and consistent source definitions.
        Metadata update capability supporting discovery refinement and health status updates.
        Method chaining support enabling fluent metadata update operations.

        [Implementation details]
        Creates new IndexableSource instance with updated metadata and preserved other fields.
        Maintains immutability while enabling metadata refinement during discovery operations.
        Used during health checking and inconsistency detection phases of discovery.
        """
        from dataclasses import replace
        return replace(self, metadata=metadata)
    
    def with_tags(self, *tags: str) -> 'IndexableSource':
        """
        [Class method intent]
        Creates new IndexableSource with additional tags preserving immutability.
        Enables tag-based filtering and categorization during configuration-based selection.

        [Design principles]
        Immutable update pattern supporting flexible categorization and filtering operations.
        Tag-based categorization enabling configuration-driven processing customization.
        Method chaining support for fluent source configuration and customization.

        [Implementation details]
        Creates new IndexableSource instance with additional tags merged into existing tag set.
        Maintains immutability while enabling flexible categorization during discovery operations.
        Used for configuration-based filtering and processing customization requirements.
        """
        from dataclasses import replace
        return replace(self, tags=self.tags.union(set(tags)))
    
    def to_dict(self) -> Dict[str, Any]:
        """
        [Class method intent]
        Serializes IndexableSource to dictionary format for debugging and persistence.
        Provides comprehensive source information for external monitoring and analysis.

        [Design principles]
        Complete source serialization preserving all identification and metadata information.
        Dictionary format compatible with JSON serialization and external system integration.
        Path serialization using string format for cross-platform compatibility.

        [Implementation details]
        Converts all source fields to dictionary format with descriptive keys.
        Handles Path objects with string conversion for serialization compatibility.
        Includes metadata serialization providing complete source state information.
        """
        return {
            'source_id': self.source_id,
            'source_type': self.source_type.value,
            'source_path': str(self.source_path),
            'handler_type': self.handler_type,
            'display_name': self.display_name,
            'needs_processing': self.needs_processing,
            'tags': list(self.tags),
            'priority': self.priority,
            'enabled': self.enabled,
            'metadata': {
                'is_healthy': self.metadata.is_healthy,
                'last_discovered': self.metadata.last_discovered,
                'needs_remediation': self.metadata.needs_remediation,
                'remediation_summary': self.metadata.remediation_summary,
                'estimated_file_count': self.metadata.estimated_file_count,
                'estimated_size_mb': self.metadata.estimated_size_mb,
                'requires_llm_processing': self.metadata.requires_llm_processing,
                'handler_metadata': self.metadata.handler_metadata
            }
        }


@dataclass
class SourceFilter:
    """
    [Class intent]
    Configuration-based filtering criteria for indexable source selection.
    Enables flexible runtime filtering based on source types, tags, paths, and metadata.

    [Design principles]
    Flexible filtering configuration supporting various indexing run customization scenarios.
    Multi-criteria filtering enabling precise source selection and processing control.
    Extensible filter structure supporting new filtering criteria without breaking compatibility.
    Clear filtering logic enabling predictable and debuggable source selection behavior.

    [Implementation details]
    Include/exclude patterns provide positive and negative filtering capabilities.
    Source type filtering enables handler-specific processing runs and testing scenarios.
    Tag-based filtering supports categorization and custom processing workflows.
    Path pattern matching enables directory-specific and location-based filtering.
    """
    
    # Source type filtering
    include_source_types: Optional[Set[SourceType]] = None
    exclude_source_types: Optional[Set[SourceType]] = None
    
    # Tag-based filtering
    require_all_tags: Optional[Set[str]] = None      # Source must have ALL these tags
    require_any_tags: Optional[Set[str]] = None      # Source must have ANY of these tags
    exclude_tags: Optional[Set[str]] = None          # Source must NOT have these tags
    
    # Path-based filtering
    include_path_patterns: Optional[List[str]] = None  # Glob patterns for inclusion
    exclude_path_patterns: Optional[List[str]] = None  # Glob patterns for exclusion
    
    # Metadata-based filtering
    only_needs_remediation: bool = False             # Only sources needing remediation
    only_healthy: bool = False                       # Only healthy sources
    min_file_count: Optional[int] = None             # Minimum estimated file count
    max_file_count: Optional[int] = None             # Maximum estimated file count
    
    def matches(self, source: IndexableSource) -> bool:
        """
        [Class method intent]
        Determines if IndexableSource matches all filtering criteria.
        Applies comprehensive filtering logic for runtime source selection.

        [Design principles]
        Comprehensive filtering logic covering all configured filtering criteria.
        Boolean decision enabling simple integration with source selection workflows.
        Defensive filtering ensuring missing criteria are handled gracefully.

        [Implementation details]
        Evaluates each filtering criterion independently for clear logic flow.
        Returns False immediately when any exclusion criterion matches for efficiency.
        Requires all inclusion criteria to match for positive filtering result.
        Handles None/missing criteria as "no restriction applied" for flexibility.
        """
        # Source type filtering
        if self.include_source_types and source.source_type not in self.include_source_types:
            return False
        if self.exclude_source_types and source.source_type in self.exclude_source_types:
            return False
        
        # Tag-based filtering
        if self.require_all_tags and not self.require_all_tags.issubset(source.tags):
            return False
        if self.require_any_tags and not any(tag in source.tags for tag in self.require_any_tags):
            return False
        if self.exclude_tags and any(tag in source.tags for tag in self.exclude_tags):
            return False
        
        # Path-based filtering (simplified - could use fnmatch for glob patterns)
        if self.include_path_patterns:
            import fnmatch
            if not any(fnmatch.fnmatch(str(source.source_path), pattern) 
                      for pattern in self.include_path_patterns):
                return False
        
        if self.exclude_path_patterns:
            import fnmatch
            if any(fnmatch.fnmatch(str(source.source_path), pattern) 
                  for pattern in self.exclude_path_patterns):
                return False
        
        # Metadata-based filtering
        if self.only_needs_remediation and not source.metadata.needs_remediation:
            return False
        if self.only_healthy and not source.metadata.is_healthy:
            return False
        if self.min_file_count and source.metadata.estimated_file_count < self.min_file_count:
            return False
        if self.max_file_count and source.metadata.estimated_file_count > self.max_file_count:
            return False
        
        return True

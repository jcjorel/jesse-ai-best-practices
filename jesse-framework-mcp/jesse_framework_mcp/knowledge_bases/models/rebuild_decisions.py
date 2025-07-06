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
# Decision models for rebuild and deletion operations in Knowledge Bases Hierarchical Indexing System.
# Provides structured data models for decision-making outcomes, reasoning, and comprehensive action plans
# enabling centralized decision logic and clear audit trails for all indexing operations.
###############################################################################
# [Source file design principles]
# - Immutable decision objects providing clear outcomes and reasoning for audit trails
# - Comprehensive action plans covering rebuild, deletion, and creation operations
# - Rich reasoning capture enabling debugging and optimization of decision logic
# - Type-safe decision outcomes preventing ambiguous or incorrect decision interpretation
# - Extensible decision types supporting future decision categories and scenarios
###############################################################################
# [Source file constraints]
# - Decision objects must be immutable once created for audit trail integrity
# - Reasoning must be human-readable for debugging and troubleshooting purposes
# - Action plans must be comprehensive covering all required filesystem operations
# - Decision types must be clearly defined with no ambiguous outcomes
# - Performance considerations for decision object creation and storage
###############################################################################
# [Dependencies]
# <system>: pathlib - Cross-platform path operations and file metadata
# <system>: datetime - Timestamp tracking for decision timing and audit trails
# <system>: enum - Type-safe decision outcome enumeration
# <system>: dataclasses - Immutable decision object creation with validation
# <system>: typing - Type annotations for decision object integrity
###############################################################################
# [GenAI tool change history]
# 2025-07-06T17:09:00Z : Added file-level decision reasons for file-first optimization by CodeAssistant
# * Added CACHE_STALE and CACHE_FRESH decision reasons supporting individual file-level decisions
# * Enhanced DecisionReason enum to support file-first approach preventing unnecessary directory rebuilds
# * Added granular file staleness checking reasons improving decision granularity and audit trails
# * Supporting implementation of file-first decision algorithm optimizing processing efficiency
# 2025-07-06T14:21:00Z : Initial creation of unified decision models by CodeAssistant
# * Created RebuildDecision, DeletionDecision, and DecisionReport models for centralized decision logic
# * Implemented comprehensive action planning with rebuild, deletion, and creation operations
# * Added rich reasoning capture for debugging and optimization of decision outcomes
# * Designed immutable decision objects ensuring audit trail integrity and type safety
###############################################################################

"""
Decision Models for Rebuild and Deletion Operations.

This module provides structured data models for decision-making outcomes in the
Knowledge Bases Hierarchical Indexing System, enabling centralized decision logic
with clear audit trails and comprehensive action planning.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set


class DecisionOutcome(Enum):
    """
    [Class intent]
    Enumeration of possible decision outcomes for rebuild and deletion operations.
    Provides type-safe decision results preventing ambiguous decision interpretation.

    [Design principles]
    Clear decision outcome enumeration with unambiguous meaning for each value.
    Extensible design supporting future decision outcome types and scenarios.
    Type safety ensuring decision outcomes are properly validated and interpreted.

    [Implementation details]
    Defines core decision outcomes used throughout the decision engine system.
    Each outcome has clear meaning and specific handling requirements.
    """
    REBUILD = "rebuild"           # File/directory needs to be rebuilt
    SKIP = "skip"                # File/directory is up to date, skip processing
    DELETE = "delete"            # File/directory should be deleted (orphaned)
    CREATE = "create"            # Directory needs to be created
    ERROR = "error"              # Decision could not be made due to error


class DecisionReason(Enum):
    """
    [Class intent]
    Enumeration of decision reasoning categories for audit trails and debugging.
    Provides structured reasoning capture enabling decision analysis and optimization.

    [Design principles]
    Comprehensive reasoning categories covering all decision scenarios and edge cases.
    Clear reasoning classification supporting debugging and decision optimization.
    Extensible design accommodating future reasoning categories and special cases.

    [Implementation details]
    Defines standard reasoning categories used by decision engine for outcome justification.
    Each reason provides specific context for why decisions were made.
    """
    # Rebuild reasons
    KNOWLEDGE_FILE_MISSING = "knowledge_file_missing"
    SOURCE_FILES_NEWER = "source_files_newer"
    CACHED_ANALYSES_NEWER = "cached_analyses_newer"
    SUBDIRECTORY_KNOWLEDGE_NEWER = "subdirectory_knowledge_newer"
    PROJECT_ROOT_FORCED = "project_root_forced"
    COMPREHENSIVE_STALENESS = "comprehensive_staleness"
    CACHE_STALE = "cache_stale"
    CHILD_DIRECTORY_REBUILT = "child_directory_rebuilt"
    
    # Skip reasons
    UP_TO_DATE = "up_to_date"
    EMPTY_DIRECTORY = "empty_directory"
    NO_PROCESSABLE_CONTENT = "no_processable_content"
    CACHE_FRESH = "cache_fresh"
    
    # Delete reasons
    ORPHANED_KNOWLEDGE_FILE = "orphaned_knowledge_file"
    ORPHANED_ANALYSIS_CACHE = "orphaned_analysis_cache"
    EXCLUDED_SOURCE = "excluded_source"
    CONFIGURATION_CHANGE = "configuration_change"
    
    # Create reasons
    MISSING_CACHE_DIRECTORY = "missing_cache_directory"
    MISSING_KNOWLEDGE_DIRECTORY = "missing_knowledge_directory"
    
    # Error reasons
    FILESYSTEM_ERROR = "filesystem_error"
    ACCESS_DENIED = "access_denied"
    DECISION_ERROR = "decision_error"


@dataclass(frozen=True)
class RebuildDecision:
    """
    [Class intent]
    Immutable decision outcome for file or directory rebuild operations.
    Captures decision outcome, reasoning, and metadata for audit trails and debugging.

    [Design principles]
    Immutable decision object ensuring audit trail integrity and preventing modification.
    Rich metadata capture supporting debugging and decision analysis requirements.
    Clear outcome specification preventing ambiguous decision interpretation.
    Timestamp tracking enabling decision timing analysis and performance optimization.

    [Implementation details]
    Uses frozen dataclass ensuring immutability after creation for audit integrity.
    Captures comprehensive decision information including outcome, reasoning, and timing.
    Provides optional metadata dictionary for additional decision context and debugging.
    """
    path: Path
    outcome: DecisionOutcome
    reason: DecisionReason
    reasoning_text: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, any] = field(default_factory=dict)
    
    @property
    def should_rebuild(self) -> bool:
        """Returns True if this decision indicates rebuild is needed."""
        return self.outcome == DecisionOutcome.REBUILD
    
    @property
    def should_skip(self) -> bool:
        """Returns True if this decision indicates processing should be skipped."""
        return self.outcome == DecisionOutcome.SKIP
    
    @property
    def is_error(self) -> bool:
        """Returns True if this decision represents an error condition."""
        return self.outcome == DecisionOutcome.ERROR


@dataclass(frozen=True)
class DeletionDecision:
    """
    [Class intent]
    Immutable decision outcome for file or directory deletion operations.
    Captures deletion rationale and safety information for audit trails and rollback.

    [Design principles]
    Immutable deletion decision ensuring audit trail integrity and preventing modification.
    Safety-focused design with clear deletion rationale and rollback information.
    Comprehensive metadata capture supporting deletion analysis and error recovery.
    Timestamp tracking enabling deletion timing analysis and audit trail construction.

    [Implementation details]
    Uses frozen dataclass ensuring immutability after creation for audit integrity.
    Captures deletion outcome, reasoning, and safety metadata for rollback capabilities.
    Provides optional backup information supporting deletion error recovery scenarios.
    """
    path: Path
    outcome: DecisionOutcome
    reason: DecisionReason
    reasoning_text: str
    is_safe_to_delete: bool = True
    backup_recommended: bool = False
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, any] = field(default_factory=dict)
    
    @property
    def should_delete(self) -> bool:
        """Returns True if this decision indicates deletion is needed."""
        return self.outcome == DecisionOutcome.DELETE and self.is_safe_to_delete


@dataclass
class DecisionReport:
    """
    [Class intent]
    Comprehensive action plan containing all rebuild and deletion decisions for a hierarchy.
    Provides complete filesystem operation planning with audit trails and execution coordination.

    [Design principles]
    Comprehensive action planning covering all required filesystem operations and decisions.
    Clear separation of operation types enabling targeted execution and error handling.
    Rich audit trail capture supporting debugging and decision analysis requirements.
    Performance statistics collection enabling optimization and monitoring capabilities.
    Execution coordination support through organized operation lists and dependencies.

    [Implementation details]
    Contains separate lists for different operation types enabling targeted execution.
    Provides decision lookup capabilities for debugging and analysis requirements.
    Calculates summary statistics for monitoring and performance analysis purposes.
    Supports both dry-run analysis and actual execution coordination scenarios.
    """
    # Core decision lists
    rebuild_decisions: Dict[Path, RebuildDecision] = field(default_factory=dict)
    deletion_decisions: Dict[Path, DeletionDecision] = field(default_factory=dict)
    
    # Organized action lists for execution
    files_to_rebuild: Set[Path] = field(default_factory=set)
    files_to_delete: Set[Path] = field(default_factory=set)
    directories_to_create: Set[Path] = field(default_factory=set)
    directories_to_delete: Set[Path] = field(default_factory=set)
    
    # Analysis metadata
    total_decisions: int = 0
    analysis_timestamp: datetime = field(default_factory=datetime.now)
    analysis_duration_seconds: float = 0.0
    
    # Error tracking
    decision_errors: List[str] = field(default_factory=list)
    
    def add_rebuild_decision(self, decision: RebuildDecision) -> None:
        """
        [Class method intent]
        Adds rebuild decision to report and updates corresponding action lists.
        Maintains consistency between decision records and execution action lists.

        [Design principles]
        Consistent decision tracking ensuring decision records match action lists.
        Automatic action list updates preventing manual synchronization errors.
        Decision deduplication preventing duplicate operations and conflicts.

        [Implementation details]
        Stores decision in rebuild_decisions dictionary with path as key.
        Updates files_to_rebuild set based on decision outcome automatically.
        Increments total decision count for reporting and analysis purposes.
        """
        self.rebuild_decisions[decision.path] = decision
        
        if decision.should_rebuild:
            self.files_to_rebuild.add(decision.path)
        
        self.total_decisions += 1
    
    def add_deletion_decision(self, decision: DeletionDecision) -> None:
        """
        [Class method intent]
        Adds deletion decision to report and updates corresponding action lists.
        Maintains consistency between decision records and deletion action lists.

        [Design principles]
        Consistent deletion tracking ensuring decision records match action lists.
        Safety validation ensuring only safe deletions are added to action lists.
        Decision deduplication preventing duplicate deletion operations and conflicts.

        [Implementation details]
        Stores decision in deletion_decisions dictionary with path as key.
        Updates files_to_delete set only for safe deletion decisions.
        Increments total decision count for comprehensive reporting and analysis.
        """
        self.deletion_decisions[decision.path] = decision
        
        if decision.should_delete:
            self.files_to_delete.add(decision.path)
        
        self.total_decisions += 1
    
    def get_decision_for_path(self, path: Path) -> Optional[RebuildDecision | DeletionDecision]:
        """
        [Class method intent]
        Retrieves decision for specific path from either rebuild or deletion decisions.
        Provides unified decision lookup for debugging and analysis purposes.

        [Design principles]
        Unified decision lookup abstracting decision type differences for convenience.
        Clear return value handling for missing decisions and error conditions.
        Type safety ensuring proper decision object handling and validation.

        [Implementation details]
        Checks rebuild decisions first, then deletion decisions for path lookup.
        Returns None if no decision found for the specified path.
        Maintains type information for proper decision handling and processing.
        """
        if path in self.rebuild_decisions:
            return self.rebuild_decisions[path]
        elif path in self.deletion_decisions:
            return self.deletion_decisions[path]
        return None
    
    def get_summary_statistics(self) -> Dict[str, int]:
        """
        [Class method intent]
        Calculates comprehensive summary statistics for decision report analysis.
        Provides decision outcome counts and operation statistics for monitoring.

        [Design principles]
        Comprehensive statistics calculation covering all decision outcomes and operations.
        Clear statistical breakdown enabling decision analysis and optimization.
        Performance monitoring support through timing and operation count statistics.

        [Implementation details]
        Counts decisions by outcome type for comprehensive statistical analysis.
        Calculates operation counts for execution planning and resource estimation.
        Returns structured dictionary enabling easy reporting and monitoring integration.
        """
        rebuild_count = len([d for d in self.rebuild_decisions.values() if d.should_rebuild])
        skip_count = len([d for d in self.rebuild_decisions.values() if d.should_skip])
        delete_count = len([d for d in self.deletion_decisions.values() if d.should_delete])
        error_count = len([d for d in self.rebuild_decisions.values() if d.is_error])
        
        return {
            "total_decisions": self.total_decisions,
            "files_to_rebuild": rebuild_count,
            "files_to_skip": skip_count,
            "files_to_delete": delete_count,
            "directories_to_create": len(self.directories_to_create),
            "directories_to_delete": len(self.directories_to_delete),
            "decision_errors": error_count,
            "analysis_duration": self.analysis_duration_seconds
        }
    
    def has_errors(self) -> bool:
        """
        [Class method intent]
        Determines if decision report contains any errors requiring attention.
        Provides quick error status check for decision validation and error handling.

        [Design principles]
        Quick error detection enabling fast decision validation and error handling.
        Comprehensive error checking covering all error sources and decision types.
        Boolean result simplifying error handling logic and decision validation.

        [Implementation details]
        Checks decision_errors list for recorded error conditions.
        Checks individual decisions for error outcomes and status.
        Returns True if any errors detected requiring attention or handling.
        """
        if self.decision_errors:
            return True
        
        # Check for error decisions
        error_decisions = [d for d in self.rebuild_decisions.values() if d.is_error]
        return len(error_decisions) > 0
    
    def get_reasoning_summary(self) -> Dict[str, List[str]]:
        """
        [Class method intent]
        Groups decision reasoning by category for analysis and debugging purposes.
        Provides structured reasoning breakdown enabling decision pattern analysis.

        [Design principles]
        Structured reasoning analysis enabling decision pattern identification and optimization.
        Clear categorization supporting debugging and decision logic improvement.
        Comprehensive reasoning capture covering all decision types and outcomes.

        [Implementation details]
        Groups decisions by reasoning category for pattern analysis and optimization.
        Collects reasoning text for each category enabling detailed decision analysis.
        Returns organized reasoning summary supporting debugging and improvement efforts.
        """
        reasoning_by_category = {}
        
        # Group rebuild decision reasoning
        for decision in self.rebuild_decisions.values():
            category = decision.reason.value
            if category not in reasoning_by_category:
                reasoning_by_category[category] = []
            reasoning_by_category[category].append(f"{decision.path}: {decision.reasoning_text}")
        
        # Group deletion decision reasoning
        for decision in self.deletion_decisions.values():
            category = decision.reason.value
            if category not in reasoning_by_category:
                reasoning_by_category[category] = []
            reasoning_by_category[category].append(f"{decision.path}: {decision.reasoning_text}")
        
        return reasoning_by_category

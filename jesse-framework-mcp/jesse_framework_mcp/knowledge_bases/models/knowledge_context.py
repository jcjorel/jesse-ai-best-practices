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
# Runtime context data models for Knowledge Bases Hierarchical Indexing System.
# Defines context structures for directory processing, file analysis, change tracking,
# and indexing operation status throughout the hierarchical processing workflow.
###############################################################################
# [Source file design principles]
# - Immutable context structures for thread-safe operations
# - Clear separation between processing state and configuration
# - Comprehensive tracking of indexing operations and statistics
# - Type-safe models supporting async operations and serialization
# - Bottom-up hierarchical context assembly without parent-to-child dependencies
###############################################################################
# [Source file constraints]
# - All models must be serializable for debugging and persistence
# - Context models must support async operations without blocking
# - Processing statistics must be accurate and efficiently calculable
# - Change tracking must be timestamp-based for reliable detection
###############################################################################
# [Dependencies]
# <system>: dataclasses - Data structure definition
# <system>: datetime - Timestamp handling and comparison
# <system>: pathlib - Path operations and validation
# <system>: typing - Type annotations and Optional types
# <system>: enum - Status enumeration definitions
###############################################################################
# [GenAI tool change history]
# 2025-07-01T12:05:00Z : Initial context models creation by CodeAssistant
# * Created runtime context models for hierarchical indexing
# * Set up processing state tracking and statistics
# * Established immutable context pattern for thread safety
###############################################################################

"""
Runtime context models for Knowledge Bases Hierarchical Indexing System.

This module defines the context structures used throughout the indexing process
to track processing state, file analysis results, change detection, and overall
indexing operation status and statistics.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
from enum import Enum


class ProcessingStatus(str, Enum):
    """
    [Enum intent]
    Defines the processing status states for files and directories during indexing.
    Tracks the current state of each processing unit throughout the indexing workflow.

    [Design principles]
    Comprehensive status tracking enabling accurate progress reporting and error handling.
    Clear state transitions supporting both successful and failed processing scenarios.
    String-based enum for serialization compatibility and debugging clarity.

    [Implementation details]
    Status values correspond to distinct processing phases in HierarchicalIndexer.
    Error states distinguish between recoverable and non-recoverable failures.
    Completion states indicate successful processing and knowledge file generation.
    """
    PENDING = "pending"  # Not yet processed
    PROCESSING = "processing"  # Currently being processed
    COMPLETED = "completed"  # Successfully processed
    FAILED = "failed"  # Processing failed
    SKIPPED = "skipped"  # Skipped due to configuration or constraints


class ChangeType(str, Enum):
    """
    [Enum intent]
    Defines the types of changes detected during incremental indexing operations.
    Enables efficient processing by identifying specific change categories.

    [Design principles]
    Granular change classification supporting targeted processing strategies.
    Clear distinction between content changes and structural modifications.
    Change types map to specific processing requirements and update strategies.

    [Implementation details]
    Change detection based on filesystem timestamps and content analysis.
    New files trigger complete processing while modified files enable incremental updates.
    Deleted files require knowledge base cleanup and dependency updates.
    """
    NEW = "new"  # New file or directory
    MODIFIED = "modified"  # Content changed since last indexing
    DELETED = "deleted"  # File or directory removed
    MOVED = "moved"  # File or directory relocated


@dataclass(frozen=True)
class FileContext:
    """
    [Class intent]
    Immutable context information for individual file processing during indexing.
    Tracks file metadata, processing state, raw LLM analysis content, and error information
    for comprehensive file-level operation tracking and debugging.

    [Design principles]
    Frozen dataclass ensuring context immutability during concurrent processing.
    Complete file processing state capture for accurate progress reporting.
    Error information preservation enabling detailed failure analysis and recovery.
    Raw LLM content storage supporting direct insertion into hierarchical knowledge files.

    [Implementation details]
    File size and timestamp information cached for efficient change detection.
    Processing status tracking enables accurate progress calculation and error handling.
    Raw LLM analysis content stored as-is without parsing or transformation.
    Error details preserved for debugging and retry decision making.
    """
    
    file_path: Path
    file_size: int
    last_modified: datetime
    processing_status: ProcessingStatus = ProcessingStatus.PENDING
    knowledge_content: Optional[str] = None  # Raw LLM analysis content stored as-is
    error_message: Optional[str] = None
    processing_start_time: Optional[datetime] = None
    processing_end_time: Optional[datetime] = None
    
    @property
    def processing_duration(self) -> Optional[float]:
        """
        [Class method intent]
        Calculates the processing duration in seconds for performance analysis.
        Returns None if processing has not completed or timing information is missing.

        [Design principles]
        Accurate performance measurement supporting processing optimization and debugging.
        Safe handling of incomplete timing information preventing calculation errors.
        Duration calculation in seconds providing standard performance metrics.

        [Implementation details]
        Checks for both start and end timestamps before calculating duration.
        Returns floating-point seconds for precise performance measurement.
        None return value indicates incomplete or missing timing information.
        """
        if self.processing_start_time and self.processing_end_time:
            return (self.processing_end_time - self.processing_start_time).total_seconds()
        return None
    
    @property
    def is_completed(self) -> bool:
        """
        [Class method intent]
        Checks if file processing has completed successfully with knowledge content generated.
        Used for progress calculation and dependency resolution in hierarchical processing.

        [Design principles]
        Clear completion criteria enabling accurate progress reporting and workflow control.
        Knowledge content requirement ensures completed files contribute to parent directory processing.
        Boolean return value simplifies conditional logic in processing workflows.

        [Implementation details]
        Requires both COMPLETED status and non-None knowledge content for true completion.
        Status check ensures processing workflow completion while content check validates output.
        Used in parent directory processing to determine child processing readiness.
        """
        return (self.processing_status == ProcessingStatus.COMPLETED and 
                self.knowledge_content is not None)


@dataclass(frozen=True)
class DirectoryContext:
    """
    [Class intent]
    Immutable context information for directory processing during hierarchical indexing.
    Tracks directory metadata, child file contexts, subdirectory relationships,
    and aggregated processing statistics for comprehensive directory-level operation tracking.

    [Design principles]
    Frozen dataclass ensuring context immutability during concurrent directory processing.
    Bottom-up hierarchical context assembly without parent-to-child dependencies.
    Complete child context aggregation supporting parent directory knowledge generation.
    Processing statistics calculation enabling accurate progress reporting and performance analysis.

    [Implementation details]
    Child file contexts stored as list maintaining processing order and completeness tracking.
    Subdirectory contexts enable recursive processing and hierarchical summary generation.
    Processing statistics calculated from child contexts for accurate progress reporting.
    Knowledge file path determination supports both regular and special handling scenarios.
    """
    
    directory_path: Path
    file_contexts: List[FileContext] = field(default_factory=list)
    subdirectory_contexts: List['DirectoryContext'] = field(default_factory=list)
    processing_status: ProcessingStatus = ProcessingStatus.PENDING
    knowledge_file_path: Optional[Path] = None
    directory_summary: Optional[str] = None
    error_message: Optional[str] = None
    processing_start_time: Optional[datetime] = None
    processing_end_time: Optional[datetime] = None
    
    @property
    def total_files(self) -> int:
        """
        [Class method intent]
        Calculates the total number of files in this directory and all subdirectories.
        Provides complete file count for progress calculation and statistics reporting.

        [Design principles]
        Recursive file counting supporting accurate progress calculation across directory hierarchy.
        Efficient calculation using list comprehension and sum aggregation.
        Complete file count including both direct children and subdirectory descendants.

        [Implementation details]
        Counts direct file contexts plus recursive subdirectory file counts.
        Uses generator expression for memory efficiency with large directory trees.
        Return value used in progress calculation and processing statistics.
        """
        return len(self.file_contexts) + sum(subdir.total_files for subdir in self.subdirectory_contexts)
    
    @property
    def completed_files(self) -> int:
        """
        [Class method intent]
        Calculates the number of successfully completed files in this directory and subdirectories.
        Supports progress reporting and completion percentage calculation.

        [Design principles]
        Accurate completion tracking using FileContext.is_completed property for consistency.
        Recursive completion counting matching total_files calculation for accurate percentages.
        Completion criteria alignment with file processing requirements and quality standards.

        [Implementation details]
        Counts completed file contexts plus recursive subdirectory completed counts.
        Uses FileContext.is_completed property ensuring consistent completion criteria.
        Return value used in progress percentage calculation and status reporting.
        """
        completed_direct = sum(1 for fc in self.file_contexts if fc.is_completed)
        completed_subdirs = sum(subdir.completed_files for subdir in self.subdirectory_contexts)
        return completed_direct + completed_subdirs
    
    @property
    def completion_percentage(self) -> float:
        """
        [Class method intent]
        Calculates the completion percentage for this directory and all subdirectories.
        Returns 0.0 for empty directories and 100.0 for fully completed directories.

        [Design principles]
        Safe percentage calculation handling empty directories and division by zero.
        Accurate progress reporting using consistent completion criteria across hierarchy.
        Floating-point percentage enabling precise progress tracking and display.

        [Implementation details]
        Handles empty directory case by returning 0.0 to prevent division by zero.
        Calculates percentage using completed_files and total_files properties for consistency.
        Returns value between 0.0 and 100.0 for standard percentage representation.
        """
        total = self.total_files
        if total == 0:
            return 0.0
        return (self.completed_files / total) * 100.0
    
    @property
    def is_ready_for_summary(self) -> bool:
        """
        [Class method intent]
        Checks if directory is ready for knowledge file generation by verifying
        all child files and subdirectories have completed processing successfully.
        Accepts both completed and skipped files as ready for summary generation.

        [Design principles]
        Bottom-up processing readiness ensuring complete child context availability.
        Comprehensive readiness check including both files and subdirectories.
        Readiness criteria alignment with hierarchical processing requirements.
        Skipped files treated as ready since they don't require processing.

        [Implementation details]
        Requires all file contexts to be completed or skipped for summary readiness.
        Requires all subdirectory contexts to have completed processing with summaries.
        Boolean return value simplifies conditional logic in hierarchical processing workflow.
        """
        files_ready = all(
            fc.is_completed or fc.processing_status == ProcessingStatus.SKIPPED 
            for fc in self.file_contexts
        )
        subdirs_ready = all(
            subdir.processing_status == ProcessingStatus.COMPLETED and subdir.directory_summary
            for subdir in self.subdirectory_contexts
        )
        return files_ready and subdirs_ready


@dataclass(frozen=True)
class ChangeInfo:
    """
    [Class intent]
    Immutable information about detected changes during incremental indexing operations.
    Tracks change type, timestamps, and affected paths for efficient incremental processing
    and accurate change detection across the knowledge base hierarchy.

    [Design principles]
    Frozen dataclass ensuring change information immutability during processing.
    Comprehensive change tracking supporting incremental processing strategies.
    Timestamp-based change detection providing reliable and accurate change identification.
    Path tracking enabling targeted processing of only affected files and directories.

    [Implementation details]
    Change type classification supports different processing strategies for each change category.
    Timestamp information enables accurate change detection and processing decision making.
    Old and new path tracking supports move operations and dependency updates.
    Detection timestamp provides audit trail and processing coordination information.
    """
    
    path: Path
    change_type: ChangeType
    old_timestamp: Optional[datetime] = None
    new_timestamp: Optional[datetime] = None
    old_path: Optional[Path] = None  # For moved files
    detected_at: datetime = field(default_factory=datetime.now)
    
    @property
    def is_content_change(self) -> bool:
        """
        [Class method intent]
        Determines if the change affects file content requiring LLM processing.
        Distinguishes between content changes and structural modifications.

        [Design principles]
        Clear distinction between content and structural changes for processing optimization.
        Content change identification enables targeted LLM processing and resource optimization.
        Processing strategy differentiation based on change impact and requirements.

        [Implementation details]
        Content changes include NEW and MODIFIED change types requiring LLM analysis.
        Structural changes like MOVED and DELETED require different processing strategies.
        Boolean return value simplifies conditional logic in change processing workflows.
        """
        return self.change_type in (ChangeType.NEW, ChangeType.MODIFIED)


@dataclass
class ProcessingStats:
    """
    [Class intent]
    Mutable statistics tracker for indexing operations providing comprehensive
    performance metrics, error tracking, and progress reporting throughout
    the hierarchical indexing process.

    [Design principles]
    Mutable statistics enabling real-time updates during processing operations.
    Comprehensive metric tracking supporting performance analysis and optimization.
    Error tracking and categorization enabling detailed failure analysis and recovery.
    Progress reporting integration supporting real-time user feedback and monitoring.

    [Implementation details]
    Counter fields track processing volumes and performance metrics.
    Error tracking includes both counts and detailed error information.
    Processing time tracking enables performance analysis and optimization.
    Statistics updates occur throughout processing workflow for accurate reporting.
    """
    
    # File processing statistics
    total_files_discovered: int = 0
    files_processed: int = 0
    files_completed: int = 0
    files_failed: int = 0
    files_skipped: int = 0
    
    # Directory processing statistics
    total_directories_discovered: int = 0
    directories_processed: int = 0
    directories_completed: int = 0
    directories_failed: int = 0
    
    # Content processing statistics
    total_content_bytes: int = 0
    total_llm_requests: int = 0
    total_llm_tokens: int = 0
    
    # Performance statistics
    processing_start_time: Optional[datetime] = None
    processing_end_time: Optional[datetime] = None
    
    # Error tracking
    errors: List[str] = field(default_factory=list)
    
    @property
    def processing_duration(self) -> Optional[float]:
        """
        [Class method intent]
        Calculates the total processing duration in seconds for performance analysis.
        Returns None if processing has not completed or timing information is missing.

        [Design principles]
        Accurate performance measurement supporting processing optimization and analysis.
        Safe handling of incomplete timing information preventing calculation errors.
        Duration calculation in seconds providing standard performance metrics.

        [Implementation details]
        Checks for both start and end timestamps before calculating duration.
        Returns floating-point seconds for precise performance measurement.
        None return value indicates incomplete or missing timing information.
        """
        if self.processing_start_time and self.processing_end_time:
            return (self.processing_end_time - self.processing_start_time).total_seconds()
        return None
    
    @property
    def files_completion_rate(self) -> float:
        """
        [Class method intent]
        Calculates the file processing completion rate as a percentage.
        Returns 0.0 if no files have been discovered for processing.

        [Design principles]
        Safe completion rate calculation handling zero file scenarios.
        Accurate progress reporting using consistent completion criteria.
        Floating-point percentage enabling precise progress tracking and display.

        [Implementation details]
        Handles zero files case by returning 0.0 to prevent division by zero.
        Calculates percentage using files_completed and total_files_discovered.
        Returns value between 0.0 and 100.0 for standard percentage representation.
        """
        if self.total_files_discovered == 0:
            return 0.0
        return (self.files_completed / self.total_files_discovered) * 100.0
    
    @property
    def error_rate(self) -> float:
        """
        [Class method intent]
        Calculates the error rate as a percentage of total files processed.
        Returns 0.0 if no files have been processed yet.

        [Design principles]
        Accurate error rate calculation supporting quality monitoring and process improvement.
        Safe calculation handling zero processing scenarios.
        Error rate measurement enabling process reliability assessment.

        [Implementation details]
        Handles zero processing case by returning 0.0 to prevent division by zero.
        Calculates percentage using files_failed and files_processed counts.
        Returns value between 0.0 and 100.0 for standard percentage representation.
        """
        if self.files_processed == 0:
            return 0.0
        return (self.files_failed / self.files_processed) * 100.0
    
    def add_error(self, error_message: str) -> None:
        """
        [Class method intent]
        Adds an error message to the error tracking list for detailed failure analysis.
        Supports comprehensive error logging and debugging throughout processing operations.

        [Design principles]
        Comprehensive error tracking enabling detailed failure analysis and recovery.
        Error message preservation supporting debugging and process improvement.
        Thread-safe error addition supporting concurrent processing operations.

        [Implementation details]
        Appends error message to errors list maintaining chronological error order.
        Error message format should include context information for effective debugging.
        Error tracking supports both individual file errors and system-level failures.
        """
        self.errors.append(error_message)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        [Class method intent]
        Serializes processing statistics to dictionary format for reporting and persistence.
        Provides comprehensive statistics data for external monitoring and analysis systems.

        [Design principles]
        Complete statistics serialization preserving all processing metrics and error information.
        Dictionary format compatible with JSON serialization and external system integration.
        Timestamp serialization using ISO format for standard compatibility.

        [Implementation details]
        Converts all statistics fields to dictionary format with descriptive keys.
        Handles optional datetime fields with None checking and ISO format conversion.
        Includes calculated properties like completion rate and error rate for convenience.
        """
        return {
            'total_files_discovered': self.total_files_discovered,
            'files_processed': self.files_processed,
            'files_completed': self.files_completed,
            'files_failed': self.files_failed,
            'files_skipped': self.files_skipped,
            'total_directories_discovered': self.total_directories_discovered,
            'directories_processed': self.directories_processed,
            'directories_completed': self.directories_completed,
            'directories_failed': self.directories_failed,
            'total_content_bytes': self.total_content_bytes,
            'total_llm_requests': self.total_llm_requests,
            'total_llm_tokens': self.total_llm_tokens,
            'processing_start_time': self.processing_start_time.isoformat() if self.processing_start_time else None,
            'processing_end_time': self.processing_end_time.isoformat() if self.processing_end_time else None,
            'processing_duration': self.processing_duration,
            'files_completion_rate': self.files_completion_rate,
            'error_rate': self.error_rate,
            'error_count': len(self.errors),
            'errors': self.errors
        }


@dataclass
class IndexingStatus:
    """
    [Class intent]
    Mutable overall status tracker for hierarchical indexing operations.
    Provides comprehensive operation status, progress tracking, and coordination
    information for the entire indexing workflow and external monitoring systems.

    [Design principles]
    Mutable status enabling real-time updates during indexing operations.
    Comprehensive operation tracking supporting coordination and monitoring.
    Progress reporting integration providing detailed status information.
    Current operation tracking enabling accurate progress reporting and debugging.

    [Implementation details]
    Overall status tracking using ProcessingStatus enum for consistency.
    Current operation description provides real-time progress information.
    Statistics integration providing comprehensive operation metrics.
    Directory context tracking enabling hierarchical progress reporting.
    """
    
    overall_status: ProcessingStatus = ProcessingStatus.PENDING
    current_operation: str = "Initializing"
    root_directory_context: Optional[DirectoryContext] = None
    processing_stats: ProcessingStats = field(default_factory=ProcessingStats)
    
    @property
    def is_processing(self) -> bool:
        """
        [Class method intent]
        Checks if indexing operation is currently active and processing files.
        Used for coordination and preventing concurrent indexing operations.

        [Design principles]
        Clear processing state identification enabling operation coordination.
        Simple boolean check simplifying conditional logic in workflow management.
        Processing state tracking supporting concurrency control and resource management.

        [Implementation details]
        Checks overall_status for PROCESSING value indicating active operations.
        Used in FastMCP tools to prevent concurrent indexing operations.
        Boolean return value simplifies conditional logic in coordination workflows.
        """
        return self.overall_status == ProcessingStatus.PROCESSING
    
    @property
    def completion_percentage(self) -> float:
        """
        [Class method intent]
        Calculates the overall completion percentage for the entire indexing operation.
        Returns root directory completion percentage or 0.0 if no root context exists.

        [Design principles]
        Hierarchical completion percentage calculation using root directory context.
        Safe percentage calculation handling missing root context scenarios.
        Accurate progress reporting using consistent completion criteria.

        [Implementation details]
        Delegates to root_directory_context.completion_percentage for hierarchical calculation.
        Returns 0.0 if root_directory_context is None to prevent errors.
        Percentage value used in progress reporting and user interface updates.
        """
        if self.root_directory_context:
            return self.root_directory_context.completion_percentage
        return 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """
        [Class method intent]
        Serializes indexing status to dictionary format for reporting and monitoring.
        Provides comprehensive status information for external systems and user interfaces.

        [Design principles]
        Complete status serialization preserving all operation state and progress information.
        Dictionary format compatible with JSON serialization and external system integration.
        Hierarchical information inclusion supporting detailed progress reporting.

        [Implementation details]
        Includes overall status, current operation, and completion percentage.
        Integrates processing statistics using ProcessingStats.to_dict() method.
        Provides comprehensive status information for monitoring and debugging.
        """
        return {
            'overall_status': self.overall_status.value,
            'current_operation': self.current_operation,
            'completion_percentage': self.completion_percentage,
            'processing_stats': self.processing_stats.to_dict()
        }

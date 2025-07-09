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
# Tree-based knowledge management models for the clean knowledge bases indexer.
# Implements single source of truth pattern with KnowledgeTree containing complete
# filesystem state. Eliminates redundant filesystem operations and enables perfect
# dry-run simulation through status updates without actual file operations.
###############################################################################
# [Source file design principles]
# - Tree-based single source of truth architecture
# - Inheritance hierarchy for file types with shared base class
# - Directory-based staleness detection using directory mtime
# - Status-driven execution with unified success/failure tracking
# - Dry-run simulation through metadata updates without file operations
# - No backward compatibility - clean architectural break
###############################################################################
# [Source file constraints]
# - Tree structure must be single source of truth for all phases
# - Only discovery phase may perform filesystem operations
# - All other phases consume/update tree without filesystem access
# - Directory mtime used for staleness detection
# - Status updates must work for both real and dry-run execution
###############################################################################
# [Dependencies]
# <system>:pathlib.Path
# <system>:dataclasses.dataclass
# <system>:dataclasses.field
# <system>:abc.ABC
# <system>:abc.abstractmethod
# <system>:typing.Callable
# <system>:typing.Optional
# <system>:typing.List
# <system>:typing.Dict
# <system>:typing.Iterator
# <system>:typing.Any
# <system>:typing.Union
# <system>:enum.Enum
# <system>:time.time
###############################################################################
# [GenAI tool change history]
# 2025-07-09T17:50:00Z : Tree-based architecture implementation by CodeAssistant
# * Implemented KnowledgeTree as single source of truth with directory hierarchy
# * Created BaseIndexedFile with AnalysisFile and KnowledgeBaseFile subclasses
# * Added UpdateStatus enum with execution success/failure tracking
# * Implemented directory-based staleness detection using mtime
# * Added dry-run simulation support through status updates without file operations
###############################################################################

from pathlib import Path
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Callable, Optional, List, Dict, Iterator, Any, Union
from enum import Enum
import time


# Progress callback type - no FastMCP dependency
ProgressCallback = Callable[[str], None]


class UpdateStatus(Enum):
    """Status enumeration for file update tracking"""
    FRESH = "fresh"                    # File is current with source
    STALE = "stale"                    # File exists but needs updating  
    MISSING = "missing"                # File doesn't exist (would be created)
    ORPHANED = "orphaned"              # Source no longer exists
    UPDATED_SUCCESS = "updated_success" # Task completed successfully
    UPDATED_FAILED = "updated_failed"  # Task failed


class TaskStatus(Enum):
    """Status enumeration for task execution"""
    PENDING = "pending"
    RUNNING = "running" 
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class BaseIndexedFile(ABC):
    """
    [Class intent]
    Abstract base class for all indexed files in the knowledge tree.
    Provides common properties and behavior shared between analysis files
    and knowledge base files with inheritance-based specialization.

    [Design principles]
    Inheritance hierarchy for file type specialization.
    Directory reference for tree navigation and staleness detection.
    Status-driven execution with unified tracking.
    Dry-run simulation through metadata updates.

    [Implementation details]
    Abstract base ensures consistent interface across file types.
    Parent directory reference enables tree navigation.
    Status field tracks execution state transitions.
    Simulated metadata supports dry-run mode.
    """
    path: Path
    handler_type: str                           # "project" or "gitclone"
    parent_directory: 'KnowledgeDirectory'      # Reference to containing directory
    
    # File metadata
    file_size: Optional[int] = None
    last_modified: Optional[float] = None
    
    # Status tracking
    update_status: UpdateStatus = UpdateStatus.MISSING
    is_orphaned: bool = True
    
    # Execution tracking
    execution_error: Optional[str] = None
    simulated_size: Optional[int] = None        # For dry-run mode
    
    @abstractmethod
    def is_stale(self) -> bool:
        """
        [Class method intent]
        Determine if file is stale compared to its source.

        [Design principles]
        Subclass-specific staleness logic.
        Directory mtime-based detection.
        
        [Implementation details]
        Must be implemented by concrete subclasses.
        Uses parent directory mtime for comparison.
        """
        pass
    
    @abstractmethod
    def get_source_info(self) -> Dict[str, Any]:
        """
        [Class method intent]
        Return source information for this file.

        [Design principles]
        Subclass-specific source tracking.
        Debugging and validation support.
        
        [Implementation details]
        Returns dict with source paths, timestamps, etc.
        Used for decision making and validation.
        """
        pass


@dataclass
class AnalysisFile(BaseIndexedFile):
    """
    [Class intent]
    Analysis cache files: <indexed_file>.analysis.md
    Represents cached analysis of individual source files with
    source-to-analysis timestamp comparison for staleness detection.

    [Design principles]
    Individual file analysis caching.
    Source file timestamp comparison.
    Directory mtime integration for consistency.

    [Implementation details]
    Inherits common properties from BaseIndexedFile.
    Tracks source file path and modification time.
    Implements staleness detection against source file.
    """
    source_file: Optional[Path] = None
    source_last_modified: Optional[float] = None
    
    def is_stale(self) -> bool:
        """
        [Class method intent]
        Check if analysis is stale compared to source file.

        [Design principles]
        Source file timestamp comparison.
        Directory mtime fallback for consistency.
        
        [Implementation details]
        Compares source file mtime vs analysis file mtime.
        Falls back to directory mtime if source unavailable.
        """
        if not self.source_file or not self.source_last_modified:
            return True
        
        # Use directory mtime if analysis file doesn't exist yet
        analysis_time = self.last_modified or 0
        
        # Stale if source is newer than analysis OR directory is newer than analysis
        return (self.source_last_modified > analysis_time or 
                self.parent_directory.last_modified > analysis_time)
    
    def get_source_info(self) -> Dict[str, Any]:
        """
        [Class method intent]
        Return source file information for debugging and validation.

        [Design principles]
        Comprehensive source tracking.
        Debugging support.
        
        [Implementation details]
        Returns source file path and timestamp information.
        """
        return {
            "source_file": self.source_file,
            "source_last_modified": self.source_last_modified,
            "is_stale": self.is_stale()
        }


@dataclass  
class KnowledgeBaseFile(BaseIndexedFile):
    """
    [Class intent]
    Knowledge base files: <directory>_kb.md
    Represents aggregated knowledge from entire source directories with
    directory timestamp comparison for staleness detection.

    [Design principles]
    Directory-based knowledge aggregation.
    Directory mtime staleness detection.
    Source directory tracking.

    [Implementation details]
    Inherits common properties from BaseIndexedFile.
    Tracks source directory path.  
    Uses directory mtime for staleness detection.
    """
    source_directory: Optional[Path] = None
    
    def is_stale(self) -> bool:
        """
        [Class method intent]
        Check if KB is stale compared to source directory.

        [Design principles]
        Directory mtime comparison.
        Simple and reliable staleness detection.
        
        [Implementation details]
        Compares source directory mtime vs KB file mtime.
        Directory mtime reflects any changes within directory.
        """
        if not self.source_directory:
            return True
        
        # Use directory mtime for KB staleness detection
        kb_time = self.last_modified or 0
        return self.parent_directory.last_modified > kb_time
    
    def get_source_info(self) -> Dict[str, Any]:
        """
        [Class method intent]
        Return source directory information for debugging and validation.

        [Design principles]
        Comprehensive source tracking.
        Debugging support.
        
        [Implementation details]
        Returns source directory path and staleness status.
        """
        return {
            "source_directory": self.source_directory,
            "is_stale": self.is_stale()
        }


@dataclass
class KnowledgeDirectory:
    """
    [Class intent]
    Represents a directory in the knowledge tree with contained files and subdirectories.
    Tracks directory metadata and provides tree navigation capabilities.
    Uses directory mtime for staleness detection of contained files.

    [Design principles]
    Hierarchical tree structure.
    Directory mtime-based staleness detection.
    Type-safe file collections.
    Tree navigation support.

    [Implementation details]
    Contains separate collections for analysis and KB files.
    Supports recursive subdirectory structure.
    Provides iteration methods for tree traversal.
    """
    path: Path
    handler_type: str                           # "project" or "gitclone"
    last_modified: float                        # Directory mtime for staleness detection
    
    # Child collections - separate by type for type safety
    analysis_files: Dict[str, AnalysisFile] = field(default_factory=dict)
    knowledge_base_files: Dict[str, KnowledgeBaseFile] = field(default_factory=dict)
    subdirectories: Dict[str, 'KnowledgeDirectory'] = field(default_factory=dict)
    
    def get_all_files(self) -> Iterator[BaseIndexedFile]:
        """
        [Class method intent]
        Yield all files in this directory and subdirectories recursively.

        [Design principles]
        Recursive tree traversal.
        Unified file iteration.
        
        [Implementation details]
        Yields analysis files, then KB files, then recurses into subdirectories.
        """
        yield from self.analysis_files.values()
        yield from self.knowledge_base_files.values()
        for subdir in self.subdirectories.values():
            yield from subdir.get_all_files()
    
    def get_files_by_status(self, status: UpdateStatus) -> List[BaseIndexedFile]:
        """
        [Class method intent]
        Return all files with specified status in this directory tree.

        [Design principles]
        Status-based filtering.
        Tree-wide search capability.
        
        [Implementation details]
        Recursively searches tree for files matching status.
        """
        matching_files = []
        for file in self.get_all_files():
            if file.update_status == status:
                matching_files.append(file)
        return matching_files
    
    def find_file(self, file_path: Path) -> Optional[BaseIndexedFile]:
        """
        [Class method intent]
        Find a specific file in this directory tree by path.

        [Design principles]
        Path-based file lookup.
        Tree navigation support.
        
        [Implementation details]
        Recursively searches tree for file with matching path.
        """
        for file in self.get_all_files():
            if file.path == file_path:
                return file
        return None


@dataclass
class KnowledgeTree:
    """
    [Class intent]
    Root of the complete knowledge structure representing entire .knowledge/ directory.
    Single source of truth for all knowledge files and directories.
    Provides unified interface for tree operations and navigation.

    [Design principles]
    Single source of truth architecture.
    Handler-based organization.
    Tree-wide operations support.
    No filesystem dependencies after creation.

    [Implementation details]
    Contains handler-specific root directories.
    Provides methods for tree-wide operations.
    Supports file lookup and status tracking.
    """
    root_path: Path
    project_handler: Optional[KnowledgeDirectory] = None
    gitclone_handler: Optional[KnowledgeDirectory] = None
    
    def get_all_directories(self) -> Iterator[KnowledgeDirectory]:
        """
        [Class method intent]
        Yield all directories in the entire knowledge tree.

        [Design principles]
        Complete tree traversal.
        Handler-agnostic iteration.
        
        [Implementation details]
        Iterates through both handler trees recursively.
        """
        if self.project_handler:
            yield from self._iterate_directories(self.project_handler)
        if self.gitclone_handler:
            yield from self._iterate_directories(self.gitclone_handler)
    
    def get_all_files(self) -> Iterator[BaseIndexedFile]:
        """
        [Class method intent]
        Yield all files in the entire knowledge tree.

        [Design principles]
        Complete file iteration.
        Unified access across handlers.
        
        [Implementation details]
        Delegates to directory get_all_files methods.
        """
        for directory in self.get_all_directories():
            yield from directory.get_all_files()
    
    def get_files_by_status(self, status: UpdateStatus) -> List[BaseIndexedFile]:
        """
        [Class method intent]
        Return all files with specified status across entire tree.

        [Design principles]
        Tree-wide status filtering.
        Execution tracking support.
        
        [Implementation details]
        Searches entire tree for files with matching status.
        """
        matching_files = []
        for file in self.get_all_files():
            if file.update_status == status:
                matching_files.append(file)
        return matching_files
    
    def find_file(self, file_path: Path) -> Optional[BaseIndexedFile]:
        """
        [Class method intent]
        Find a specific file anywhere in the knowledge tree.

        [Design principles]
        Tree-wide file lookup.
        Path-based navigation.
        
        [Implementation details]
        Searches both handler trees for file with matching path.
        """
        if self.project_handler:
            file = self.project_handler.find_file(file_path)
            if file:
                return file
        
        if self.gitclone_handler:
            file = self.gitclone_handler.find_file(file_path)
            if file:
                return file
        
        return None
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """
        [Class method intent]
        Return summary statistics for the entire knowledge tree.

        [Design principles]
        Tree-wide statistics.
        Status distribution tracking.
        
        [Implementation details]
        Counts files by type and status across entire tree.
        """
        stats = {
            "total_files": 0,
            "analysis_files": 0,
            "knowledge_base_files": 0,
            "status_distribution": {status.value: 0 for status in UpdateStatus}
        }
        
        for file in self.get_all_files():
            stats["total_files"] += 1
            
            if isinstance(file, AnalysisFile):
                stats["analysis_files"] += 1
            elif isinstance(file, KnowledgeBaseFile):
                stats["knowledge_base_files"] += 1
            
            stats["status_distribution"][file.update_status.value] += 1
        
        return stats
    
    def _iterate_directories(self, root_dir: KnowledgeDirectory) -> Iterator[KnowledgeDirectory]:
        """
        [Class method intent]
        Recursively iterate through directory tree starting from root.

        [Design principles]
        Recursive tree traversal.
        Depth-first iteration.
        
        [Implementation details]
        Yields current directory then recurses into subdirectories.
        """
        yield root_dir
        for subdir in root_dir.subdirectories.values():
            yield from self._iterate_directories(subdir)


@dataclass
class ValidationResult:
    """
    [Class intent]
    Result of source validation performed during discovery phase.
    Provides clear determination of source existence, staleness, and
    reasoning for validation decisions.

    [Design principles]
    Explicit validation outcomes with human-readable reasoning.
    Separate fields for different validation aspects.
    Immutable result object for clear data flow.

    [Implementation details]
    source_exists determines orphaned status.
    is_stale triggers rebuild decisions.
    validation_reason provides debugging context.
    """
    source_exists: bool
    source_path: Optional[Path]
    is_stale: bool
    validation_reason: str


@dataclass
class ExecutionContext:
    """
    [Class intent]
    Context environment passed to task execution providing all necessary
    dependencies and configuration for atomic task operations.

    [Design principles]
    Dependency injection pattern for testability.
    Shared data dictionary for inter-task communication.
    Simple callback mechanism for progress reporting.
    Knowledge tree integration for single source of truth.

    [Implementation details]
    source_root provides project context for path resolution.
    progress_callback enables decoupled progress reporting.
    llm_driver injected for LLM-dependent tasks.
    knowledge_tree provides access to complete file structure.
    shared_data enables task coordination and caching.
    """
    source_root: Path
    progress_callback: ProgressCallback
    knowledge_tree: KnowledgeTree           # NEW: Tree access for tasks
    llm_driver: Any = None
    shared_data: Dict[str, Any] = field(default_factory=dict)
    dry_run: bool = False


@dataclass 
class TaskResult:
    """
    [Class intent]
    Result of atomic task execution with comprehensive outcome information.
    Captures success status, execution details, and error information
    for debugging and progress tracking.

    [Design principles]
    Clear success/failure indication with detailed context.
    Structured error information for debugging.
    Execution metrics for performance monitoring.

    [Implementation details]
    success boolean provides immediate status check.
    task_type enables result categorization and processing.
    error_message captures failure reasons for debugging.
    execution_time enables performance analysis.
    """
    success: bool
    task_type: str
    task_id: str
    error_message: Optional[str] = None
    execution_time: Optional[float] = None
    files_processed: int = 0
    output_files: List[Path] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class AtomicTask(ABC):
    """
    [Class intent]
    Generic abstract interface for all atomic indexing tasks.
    Defines contract for task execution, dependency management,
    and concurrency control within the indexer system.

    [Design principles]
    Single responsibility - each task performs one atomic operation.
    Dependency declaration enables proper execution ordering.
    Concurrency control allows parallel execution where safe.
    Precondition validation prevents invalid execution attempts.
    Knowledge tree integration for single source of truth.

    [Implementation details]
    Abstract methods enforce implementation of all required behaviors.
    Task types enable registry-based task creation and management.
    Dependencies support topological sorting for execution planning.
    Concurrency compatibility enables performance optimization.
    """
    
    @abstractmethod
    def get_task_type(self) -> str:
        """
        [Class method intent]
        Return the string identifier for this task type.

        [Design principles]
        Enables task registry and factory pattern implementation.
        
        [Implementation details]
        Must return consistent string identifier for task type.
        """
        pass
    
    @abstractmethod
    def get_task_id(self) -> str:
        """
        [Class method intent]  
        Return unique identifier for this specific task instance.

        [Design principles]
        Enables dependency tracking and result correlation.
        
        [Implementation details]
        Must return unique ID for this task instance.
        """
        pass
    
    @abstractmethod
    def get_dependencies(self) -> List[str]:
        """
        [Class method intent]
        Return list of task IDs that must complete before this task.

        [Design principles]
        Enables dependency resolution and execution ordering.
        
        [Implementation details]
        Returns empty list if no dependencies exist.
        Task IDs must match other tasks' get_task_id() returns.
        """
        pass
    
    @abstractmethod
    async def execute(self, context: ExecutionContext) -> TaskResult:
        """
        [Class method intent]
        Execute the atomic task operation with provided context.

        [Design principles]
        Fail-fast execution - throw exceptions for errors.
        Use context for all external dependencies and configuration.
        Update knowledge tree status based on execution results.
        
        [Implementation details]
        Must return TaskResult with execution outcome.
        Must update knowledge tree file status appropriately.
        In dry-run mode: update status without file operations.
        Exceptions indicate task failure requiring attention.
        """
        pass
    
    @abstractmethod
    def can_run_concurrently_with(self, other: 'AtomicTask') -> bool:
        """
        [Class method intent]
        Determine if this task can run concurrently with another task.

        [Design principles]
        Enables performance optimization through parallel execution.
        Conservative approach - default to false unless proven safe.
        
        [Implementation details]
        Returns True only if tasks can safely run simultaneously.
        Consider file access, resource conflicts, and data dependencies.
        """
        pass
    
    @abstractmethod
    def validate_preconditions(self, context: ExecutionContext) -> bool:
        """
        [Class method intent]
        Validate that all preconditions are met for task execution.

        [Design principles]
        Defensive programming - catch issues before execution.
        Clear validation failure with descriptive exceptions.
        
        [Implementation details]
        Returns True if task can execute safely.
        Throws exception with specific failure reason if invalid.
        """
        pass


@dataclass
class ExecutionPlan:
    """
    [Class intent]
    Complete execution plan with dependency-resolved task ordering.
    Represents the final execution strategy after discovery, decision
    making, and planning phases.

    [Design principles]
    Immutable plan object for consistent execution.
    Clear separation of sequential and concurrent task groups.
    Comprehensive plan validation before execution.

    [Implementation details]
    tasks list contains all tasks in dependency-resolved order.
    concurrent_groups identifies tasks that can run in parallel.
    validation_errors capture plan construction issues.
    """
    tasks: List[AtomicTask] = field(default_factory=list)
    concurrent_groups: List[List[str]] = field(default_factory=list)
    validation_errors: List[str] = field(default_factory=list)
    estimated_duration: Optional[float] = None
    
    @property
    def is_valid(self) -> bool:
        """
        [Class method intent]
        Check if execution plan is valid and ready for execution.

        [Design principles]
        Clear validation status for execution safety.
        
        [Implementation details]
        Returns True if no validation errors exist.
        """
        return len(self.validation_errors) == 0
    
    @property
    def task_count(self) -> int:
        """
        [Class method intent]
        Return total number of tasks in execution plan.

        [Design principles]
        Convenient access to plan size for reporting.
        
        [Implementation details]
        Returns length of tasks list.
        """
        return len(self.tasks)


@dataclass
class IndexingResult:
    """
    [Class intent]
    Final result of complete indexing operation with comprehensive
    outcome information, statistics, and error details.

    [Design principles]
    Complete outcome reporting for user and system feedback.
    Structured error information for debugging and improvement.
    Performance metrics for monitoring and optimization.
    Knowledge tree integration for enhanced reporting.

    [Implementation details]
    success_rate provides overall operation assessment.
    detailed_results enables specific task outcome analysis.
    Comprehensive statistics for reporting and monitoring.
    """
    files_analyzed: int = 0
    kbs_built: int = 0
    cache_files_created: int = 0
    orphaned_files_cleaned: int = 0
    task_results: List[TaskResult] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    execution_time: Optional[float] = None
    discovery_time: Optional[float] = None
    planning_time: Optional[float] = None
    
    # NEW: Knowledge tree for enhanced reporting
    final_tree_state: Optional[KnowledgeTree] = None
    
    @property
    def success_rate(self) -> float:
        """
        [Class method intent]
        Calculate success rate as ratio of successful to total tasks.

        [Design principles]
        Simple success metric for operation assessment.
        
        [Implementation details]
        Returns 1.0 for perfect success, 0.0 for complete failure.
        Handles division by zero for empty task lists.
        """
        if not self.task_results:
            return 1.0
        
        successful_tasks = sum(1 for result in self.task_results if result.success)
        return successful_tasks / len(self.task_results)
    
    @property
    def total_files_processed(self) -> int:
        """
        [Class method intent]
        Return total number of files processed across all tasks.

        [Design principles]
        Aggregate metric for operation scope assessment.
        
        [Implementation details]
        Sums files_processed from all task results.
        """
        return sum(result.files_processed for result in self.task_results)


# Type aliases for common patterns
TaskRegistry = Dict[str, type]
TaskDependencyGraph = Dict[str, List[str]]
FileCollection = Union[List[AnalysisFile], List[KnowledgeBaseFile], List[BaseIndexedFile]]

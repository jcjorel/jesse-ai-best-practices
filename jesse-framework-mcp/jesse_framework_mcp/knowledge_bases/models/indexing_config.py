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
# Configuration data model for Knowledge Bases Hierarchical Indexing System.
# Defines all configurable parameters for indexing operations, LLM integration,
# file processing constraints, and special handling requirements.
###############################################################################
# [Source file design principles]
# - Immutable configuration with validation at initialization
# - Type-safe parameter definitions with sensible defaults
# - Clear separation between file processing and LLM configuration
# - Integration with strands_agent_driver Claude 4 Sonnet configuration
# - Defensive parameter validation preventing runtime errors
###############################################################################
# [Source file constraints]
# - Must use Claude 4 Sonnet model ID from strands_agent_driver
# - All file size limits must be reasonable for LLM context windows
# - Configuration must be serializable for persistence and debugging
# - Parameter validation must fail fast with descriptive error messages
###############################################################################
# [Dependencies]
# <codebase>: jesse_framework_mcp.llm.strands_agent_driver.models - Claude 4 Sonnet model configuration
# <system>: dataclasses - Data structure definition
# <system>: pathlib - Path validation and manipulation
# <system>: typing - Type annotations and validation
###############################################################################
# [GenAI tool change history]
# 2025-07-03T15:38:00Z : Set default knowledge_output_directory to {PROJECT_ROOT}/.knowledge/ by CodeAssistant
# * Added get_project_root import for project root detection integration
# * Modified __post_init__ to set knowledge_output_directory default to project_root/.knowledge when None
# * Updated documentation to reflect new default behavior following JESSE Framework conventions
# * Maintained backward compatibility with graceful fallback when project root cannot be detected
# 2025-07-01T12:04:00Z : Initial configuration model creation by CodeAssistant
# * Created IndexingConfig with Claude 4 Sonnet integration
# * Set up comprehensive parameter validation
# * Established immutable configuration pattern
###############################################################################

"""
Configuration models for Knowledge Bases Hierarchical Indexing System.

This module defines the IndexingConfig class that controls all aspects of the
hierarchical indexing process, including file processing, LLM integration,
and special handling requirements.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Set, Optional, Dict, Any
from enum import Enum
import sys
import os

from jesse_framework_mcp.llm.strands_agent_driver.models import Claude4SonnetModel
from jesse_framework_mcp.helpers.path_utils import get_project_root


class IndexingMode(str, Enum):
    """
    [Enum intent]
    Defines the indexing operation modes for different processing scenarios.
    Controls the scope and behavior of knowledge base indexing operations.

    [Design principles]
    Single responsibility for indexing mode configuration with clear semantics.
    Each mode represents a distinct processing strategy with specific constraints.

    [Implementation details]
    String-based enum for serialization compatibility and configuration persistence.
    Mode values map directly to processing strategies in HierarchicalIndexer.
    """
    FULL = "full"  # Complete re-indexing of entire hierarchy
    INCREMENTAL = "incremental"  # Update only changed files and dependencies
    SELECTIVE = "selective"  # Index specific paths only


@dataclass(frozen=True)
class IndexingConfig:
    """
    [Class intent]
    Immutable configuration for Knowledge Bases Hierarchical Indexing System operations.
    Controls all aspects of file processing, LLM integration, change detection,
    and special handling for git-clones and project-base indexing.

    [Design principles]
    Frozen dataclass ensuring configuration immutability after initialization.
    Comprehensive validation at creation time prevents runtime configuration errors.
    Clear separation between file processing and LLM operational parameters.
    Integration with existing strands_agent_driver Claude 4 Sonnet configuration.

    [Implementation details]
    Uses Claude 4 Sonnet model ID from strands_agent_driver for consistency.
    File size and processing limits designed for optimal LLM context usage.
    Validation occurs in __post_init__ with descriptive error messages.
    """
    
    # File Processing Configuration
    max_file_size: int = 2 * 1024 * 1024  # 2MB max per file (increased for better coverage)
    chunk_size: int = 8000  # 8k chars (optimized for Claude 4 context)
    chunk_overlap: int = 400  # Overlap between chunks for context preservation
    
    # Batch Processing Configuration  
    batch_size: int = 7  # Files per LLM batch (cost/performance balance)
    max_concurrent_operations: int = 3  # Async concurrency limit
    
    # Content Filtering Configuration
    excluded_extensions: Set[str] = field(default_factory=lambda: {
        '.pyc', '.pyo', '.git', '__pycache__', 
        '.DS_Store', '.env', '.log', '.tmp',
        '.cache', '.pytest_cache', '.mypy_cache'
    })
    
    excluded_directories: Set[str] = field(default_factory=lambda: {
        '.git', '__pycache__', '.pytest_cache', 
        '.mypy_cache', 'node_modules', '.venv', 'venv'
    })
    
    # LLM Configuration (Claude 4 Sonnet)
    llm_model: str = Claude4SonnetModel.CLAUDE_4_SONNET  # Official Claude 4 Sonnet model ID
    temperature: float = 0.3  # Low temperature for consistent summarization
    max_tokens: int = 2000  # Response length limit
    
    # Change Detection Configuration
    indexing_mode: IndexingMode = IndexingMode.INCREMENTAL
    timestamp_tolerance_seconds: int = 2  # Tolerance for filesystem timestamp comparison
    
    # Special Handling Configuration
    enable_git_clone_indexing: bool = True
    enable_project_base_indexing: bool = True
    respect_gitignore: bool = True  # Honor .gitignore patterns in project-base indexing
    
    # Performance Configuration
    enable_progress_reporting: bool = True
    progress_update_interval: int = 5  # Seconds between progress updates
    
    # Error Handling Configuration
    max_retries: int = 3
    retry_delay_seconds: float = 1.0
    continue_on_file_errors: bool = True  # Continue processing when individual files fail
    
    # Knowledge File Output Configuration
    knowledge_output_directory: Optional[Path] = None  # Directory for generated knowledge files (if None, defaults to {PROJECT_ROOT}/.knowledge/)
    
    # Debug Configuration
    debug_mode: bool = False  # Enable debug mode for LLM output persistence and replay
    debug_output_directory: Optional[Path] = None  # Directory for debug artifacts (if None, uses temp directory)
    enable_llm_replay: bool = False  # Use saved LLM outputs instead of making new calls
    
    def __post_init__(self):
        """
        [Class method intent]
        Validates all configuration parameters after initialization to ensure
        consistent and safe operation throughout the indexing process.
        Sets default knowledge_output_directory to {PROJECT_ROOT}/.knowledge/ when not specified.

        [Design principles]
        Fail-fast validation preventing runtime errors from invalid configuration.
        Comprehensive parameter checking with descriptive error messages.
        Default knowledge directory setting following JESSE Framework conventions.
        Validation occurs once at initialization for performance optimization.

        [Implementation details]
        Sets knowledge_output_directory to project_root/.knowledge when None.
        Validates file sizes, batch parameters, concurrency limits, and LLM settings.
        Checks that file processing parameters are within reasonable bounds.
        Ensures LLM configuration is compatible with Claude 4 Sonnet constraints.
        """
        # Set default knowledge output directory to {PROJECT_ROOT}/.knowledge/
        if self.knowledge_output_directory is None:
            try:
                project_root = get_project_root()
                if project_root:
                    # Use object.__setattr__ to modify frozen dataclass
                    object.__setattr__(self, 'knowledge_output_directory', project_root / '.knowledge')
                # If project_root is None, keep knowledge_output_directory as None (fallback to old behavior)
            except Exception:
                # If project root detection fails, keep knowledge_output_directory as None
                pass
        
        # Validate file processing parameters
        if self.max_file_size <= 0:
            raise ValueError(f"max_file_size must be positive, got {self.max_file_size}")
        
        if self.chunk_size <= 0:
            raise ValueError(f"chunk_size must be positive, got {self.chunk_size}")
        
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(f"chunk_overlap ({self.chunk_overlap}) must be less than chunk_size ({self.chunk_size})")
        
        # Validate batch processing parameters
        if self.batch_size <= 0:
            raise ValueError(f"batch_size must be positive, got {self.batch_size}")
        
        if self.max_concurrent_operations <= 0:
            raise ValueError(f"max_concurrent_operations must be positive, got {self.max_concurrent_operations}")
        
        # Validate LLM parameters
        if not (0.0 <= self.temperature <= 1.0):
            raise ValueError(f"temperature must be between 0.0 and 1.0, got {self.temperature}")
        
        if self.max_tokens <= 0:
            raise ValueError(f"max_tokens must be positive, got {self.max_tokens}")
        
        # Validate performance parameters
        if self.progress_update_interval <= 0:
            raise ValueError(f"progress_update_interval must be positive, got {self.progress_update_interval}")
        
        if self.max_retries < 0:
            raise ValueError(f"max_retries must be non-negative, got {self.max_retries}")
        
        if self.retry_delay_seconds < 0:
            raise ValueError(f"retry_delay_seconds must be non-negative, got {self.retry_delay_seconds}")
    
    def should_process_file(self, file_path: Path) -> bool:
        """
        [Class method intent]
        Determines whether a given file should be processed based on extension,
        size constraints, and configuration filtering rules.

        [Design principles]
        Single source of truth for file filtering decisions across the indexing system.
        Defensive checks preventing processing of unsuitable or problematic files.
        Clear separation of concerns between file identification and processing logic.

        [Implementation details]
        Checks file extension against excluded_extensions set for performance.
        Validates file size against max_file_size to prevent context overflow.
        Returns boolean decision for use in file discovery and processing loops.
        """
        # Check if file extension is excluded
        if file_path.suffix.lower() in self.excluded_extensions:
            return False
        
        # Check file size constraints
        try:
            if file_path.stat().st_size > self.max_file_size:
                return False
        except (OSError, FileNotFoundError):
            # File doesn't exist or is inaccessible
            return False
        
        return True
    
    def should_process_directory(self, directory_path: Path) -> bool:
        """
        [Class method intent]
        Determines whether a given directory should be processed based on
        directory name filtering rules and special handling requirements.

        [Design principles]
        Centralized directory filtering logic preventing processing of system directories.
        Integration with special handling requirements for git-clones and project-base.
        Performance optimization by early exclusion of large unnecessary directories.

        [Implementation details]
        Checks directory name against excluded_directories set for fast filtering.
        Directory name comparison is case-sensitive for precise control.
        Returns boolean decision for use in directory traversal algorithms.
        """
        # Check if directory name is excluded
        if directory_path.name in self.excluded_directories:
            return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """
        [Class method intent]
        Serializes configuration to dictionary format for persistence, debugging,
        and integration with external systems requiring configuration data.

        [Design principles]
        Complete serialization preserving all configuration state for reproducible operations.
        Dictionary format compatible with JSON serialization and configuration persistence.
        Handles complex types like sets and enums with appropriate conversion.

        [Implementation details]
        Converts sets to lists for JSON compatibility while preserving semantics.
        Enum values converted to string representation for serialization safety.
        All primitive and collection types handled with explicit type conversion.
        """
        return {
            'max_file_size': self.max_file_size,
            'chunk_size': self.chunk_size,
            'chunk_overlap': self.chunk_overlap,
            'batch_size': self.batch_size,
            'max_concurrent_operations': self.max_concurrent_operations,
            'excluded_extensions': list(self.excluded_extensions),
            'excluded_directories': list(self.excluded_directories),
            'llm_model': self.llm_model,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'indexing_mode': self.indexing_mode.value,
            'timestamp_tolerance_seconds': self.timestamp_tolerance_seconds,
            'enable_git_clone_indexing': self.enable_git_clone_indexing,
            'enable_project_base_indexing': self.enable_project_base_indexing,
            'respect_gitignore': self.respect_gitignore,
            'enable_progress_reporting': self.enable_progress_reporting,
            'progress_update_interval': self.progress_update_interval,
            'max_retries': self.max_retries,
            'retry_delay_seconds': self.retry_delay_seconds,
            'continue_on_file_errors': self.continue_on_file_errors,
            'knowledge_output_directory': str(self.knowledge_output_directory) if self.knowledge_output_directory else None,
            'debug_mode': self.debug_mode,
            'debug_output_directory': str(self.debug_output_directory) if self.debug_output_directory else None,
            'enable_llm_replay': self.enable_llm_replay
        }

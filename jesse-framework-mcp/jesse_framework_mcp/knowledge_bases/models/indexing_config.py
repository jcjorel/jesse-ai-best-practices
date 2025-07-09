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
# 2025-07-06T10:59:00Z : Fixed should_process_directory to actually check project_base_exclusions by CodeAssistant
# * Enhanced should_process_directory to check project_base_exclusions when they exist
# * Fixes issue where .clinerules, .coding_assistant, .knowledge directories were indexed despite being excluded
# * Ensures proper directory exclusion for project-base handler type following hierarchical exclusion rules
# * Complete fix for directory-level exclusion functionality ensuring cleanup works for all excluded directories
# 2025-07-05T15:58:00Z : Added configuration manager integration and new parameters by CodeAssistant
# * Added project_base_exclusions parameter for hierarchical exclusion system
# * Added load_for_handler class method for configuration manager integration
# * Added from_dict class method for Pydantic model conversion support
# * Enhanced should_process_directory to support project-base specific exclusions
# 2025-07-03T15:38:00Z : Set default knowledge_output_directory to {PROJECT_ROOT}/.knowledge/ by CodeAssistant
# * Added get_project_root import for project root detection integration
# * Modified __post_init__ to set knowledge_output_directory default to project_root/.knowledge when None
# * Updated documentation to reflect new default behavior following JESSE Framework conventions
# * Maintained backward compatibility with graceful fallback when project root cannot be detected
###############################################################################

"""
Configuration models for Knowledge Bases Hierarchical Indexing System.

This module defines the IndexingConfig class that controls all aspects of the
hierarchical indexing process, including file processing, LLM integration,
and special handling requirements.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Set, Optional, Dict, Any, List
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
    FULL = "full"  # Nuclear - Complete regeneration of everything from scratch (no cache)
    FULL_KB_REBUILD = "full_kb_rebuild"  # Hybrid - Rebuild all KB files but use file analysis cache  
    INCREMENTAL = "incremental"  # Smart - Update only changed files and dependencies


@dataclass(frozen=True)
class FileProcessingConfig:
    """
    [Class intent]
    Configuration for file processing limits and batch operations.
    Controls file size constraints, batching parameters, and concurrency limits.

    [Design principles]
    Focused configuration group for file processing concerns.
    Clear separation from other configuration aspects for maintainability.
    """
    max_file_size: int = 2 * 1024 * 1024  # 2MB max per file
    batch_size: int = 7                    # Files per LLM batch (cost/performance balance)
    max_concurrent_operations: int = 3     # Async concurrency limit


@dataclass(frozen=True)
class ContentFilteringConfig:
    """
    [Class intent]
    Configuration for content filtering and exclusion rules.
    Controls which files and directories are excluded from processing.

    [Design principles]
    Centralized filtering logic with hierarchical exclusion support.
    Separate concerns for different types of exclusions.
    """
    excluded_extensions: Set[str] = field(default_factory=lambda: {
        '.pyc', '.pyo', '.git', '__pycache__', 
        '.DS_Store', '.env', '.log', '.tmp',
        '.cache', '.pytest_cache', '.mypy_cache'
    })
    excluded_directories: Set[str] = field(default_factory=lambda: {
        '.git', '__pycache__', '.pytest_cache', 
        '.mypy_cache', 'node_modules', '.venv', 'venv'
    })
    project_base_exclusions: Optional[Set[str]] = None  # Project-base specific exclusions


@dataclass(frozen=True)
class LLMConfig:
    """
    [Class intent]
    Configuration for LLM integration and behavior.
    Controls Claude 4 Sonnet model parameters and response generation.

    [Design principles]
    Focused LLM configuration with model-specific parameters.
    Integration with strands_agent_driver Claude 4 Sonnet configuration.
    """
    llm_model: str = Claude4SonnetModel.CLAUDE_4_SONNET  # Official Claude 4 Sonnet model ID
    temperature: float = 0.3                              # Low temperature for consistent summarization
    max_tokens: int = 20000                              # Response length limit


@dataclass(frozen=True)
class ChangeDetectionConfig:
    """
    [Class intent]
    Configuration for change detection and processing mode.
    Controls indexing strategy and timestamp comparison behavior.

    [Design principles]
    Focused configuration for change detection logic.
    Clear separation of timing and mode concerns.
    """
    indexing_mode: IndexingMode = IndexingMode.INCREMENTAL
    timestamp_tolerance_seconds: int = 2  # Tolerance for filesystem timestamp comparison


@dataclass(frozen=True)
class ErrorHandlingConfig:
    """
    [Class intent]
    Configuration for error handling and resilience.
    Controls retry behavior and error recovery strategies.

    [Design principles]
    Centralized error handling configuration.
    Separate concerns for different types of error handling.
    """
    max_retries: int = 3
    retry_delay_seconds: float = 1.0
    continue_on_file_errors: bool = True  # Continue processing when individual files fail


@dataclass(frozen=True)
class OutputConfig:
    """
    [Class intent]
    Configuration for output generation and storage.
    Controls where knowledge files are generated and stored.

    [Design principles]
    Focused configuration for output management.
    Clear separation of output concerns from processing logic.
    """
    knowledge_output_directory: Optional[Path] = None  # Directory for generated knowledge files


@dataclass(frozen=True)
class DebugConfig:
    """
    [Class intent]
    Configuration for debug and development features.
    Controls debug mode, output persistence, replay functionality, and dry-run operations.

    [Design principles]
    Isolated debug configuration to avoid interfering with production settings.
    Clear separation of debug concerns from operational configuration.
    Dry-run mode integration enabling plan-only execution for testing and validation.
    """
    debug_mode: bool = False                            # Enable debug mode for LLM output persistence
    debug_output_directory: Optional[Path] = None      # Directory for debug artifacts
    enable_llm_replay: bool = False                    # Use saved LLM outputs instead of making new calls
    dry_run: bool = False                              # Enable dry-run mode (discovery + planning only, no execution)


@dataclass(frozen=True)
class CleanupConfig:
    """
    [Class intent]
    Configuration for cleanup operations during indexing.
    Controls test scenarios requiring file cleanup while maintaining framework integration.

    [Design principles]
    Test-focused cleanup configuration enabling rebuild scenarios through atomic execution.
    Handler-scoped cleanup ensuring each handler only cleans its own files.
    Framework integration through Plan-then-Execute architecture rather than direct operations.
    """
    cleanup_mode_enabled: bool = False                    # Enable cleanup operations
    cleanup_types: List[str] = field(default_factory=list)  # Types of cleanup: ["kb_files", "analysis_files"]


@dataclass(frozen=True)
class IndexingConfig:
    """
    [Class intent]
    Hierarchical immutable configuration for Knowledge Bases Hierarchical Indexing System operations.
    Controls all aspects of file processing, LLM integration, change detection,
    and special handling for git-clones and project-base indexing.

    [Design principles]
    Frozen dataclass ensuring configuration immutability after initialization.
    Hierarchical organization with focused configuration groups for maintainability.
    Comprehensive validation at creation time prevents runtime configuration errors.
    Integration with existing strands_agent_driver Claude 4 Sonnet configuration.

    [Implementation details]
    Uses hierarchical configuration groups for logical organization.
    Each configuration group handles its specific domain concerns.
    Provides convenient access properties for backward compatibility during transition.
    """
    
    # Handler Identification
    handler_type: str = "project-base"
    description: str = "Hierarchical indexing configuration"
    
    # Hierarchical Configuration Groups
    file_processing: FileProcessingConfig = field(default_factory=FileProcessingConfig)
    content_filtering: ContentFilteringConfig = field(default_factory=ContentFilteringConfig)
    llm_config: LLMConfig = field(default_factory=LLMConfig)
    change_detection: ChangeDetectionConfig = field(default_factory=ChangeDetectionConfig)
    error_handling: ErrorHandlingConfig = field(default_factory=ErrorHandlingConfig)
    output_config: OutputConfig = field(default_factory=OutputConfig)
    debug_config: DebugConfig = field(default_factory=DebugConfig)
    cleanup_config: CleanupConfig = field(default_factory=CleanupConfig)
    
    # Convenience Properties for Backward Compatibility Access
    @property
    def max_file_size(self) -> int:
        return self.file_processing.max_file_size
    
    @property
    def batch_size(self) -> int:
        return self.file_processing.batch_size
    
    @property
    def max_concurrent_operations(self) -> int:
        return self.file_processing.max_concurrent_operations
    
    @property
    def excluded_extensions(self) -> Set[str]:
        return self.content_filtering.excluded_extensions
    
    @property
    def excluded_directories(self) -> Set[str]:
        return self.content_filtering.excluded_directories
    
    @property
    def project_base_exclusions(self) -> Optional[Set[str]]:
        return self.content_filtering.project_base_exclusions
    
    @property
    def llm_model(self) -> str:
        return self.llm_config.llm_model
    
    @property
    def temperature(self) -> float:
        return self.llm_config.temperature
    
    @property
    def max_tokens(self) -> int:
        return self.llm_config.max_tokens
    
    @property
    def indexing_mode(self) -> IndexingMode:
        return self.change_detection.indexing_mode
    
    @property
    def timestamp_tolerance_seconds(self) -> int:
        return self.change_detection.timestamp_tolerance_seconds
    
    @property
    def max_retries(self) -> int:
        return self.error_handling.max_retries
    
    @property
    def retry_delay_seconds(self) -> float:
        return self.error_handling.retry_delay_seconds
    
    @property
    def continue_on_file_errors(self) -> bool:
        return self.error_handling.continue_on_file_errors
    
    @property
    def knowledge_output_directory(self) -> Optional[Path]:
        return self.output_config.knowledge_output_directory
    
    @property
    def debug_mode(self) -> bool:
        return self.debug_config.debug_mode
    
    @property
    def debug_output_directory(self) -> Optional[Path]:
        return self.debug_config.debug_output_directory
    
    @property
    def enable_llm_replay(self) -> bool:
        return self.debug_config.enable_llm_replay
    
    @property
    def dry_run(self) -> bool:
        return self.debug_config.dry_run
    
    @property
    def cleanup_mode_enabled(self) -> bool:
        return self.cleanup_config.cleanup_mode_enabled
    
    @property
    def cleanup_types(self) -> List[str]:
        return self.cleanup_config.cleanup_types
    
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
        if self.output_config.knowledge_output_directory is None:
            try:
                project_root = get_project_root()
                if project_root:
                    # Create new OutputConfig with the default knowledge directory
                    new_output_config = OutputConfig(knowledge_output_directory=project_root / '.knowledge')
                    # Use object.__setattr__ to modify frozen dataclass
                    object.__setattr__(self, 'output_config', new_output_config)
                # If project_root is None, keep knowledge_output_directory as None (fallback to old behavior)
            except Exception:
                # If project root detection fails, keep knowledge_output_directory as None
                pass
        
        # Validate file processing parameters
        if self.max_file_size <= 0:
            raise ValueError(f"max_file_size must be positive, got {self.max_file_size}")
        
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
        
        # Validate error handling parameters
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
        For project-base handlers, also checks against project_base_exclusions.
        Directory name comparison is case-sensitive for precise control.
        Returns boolean decision for use in directory traversal algorithms.
        """
        # Check if directory name is excluded in base exclusions
        if directory_path.name in self.excluded_directories:
            return False
        
        # Check if directory name is excluded in project-base specific exclusions
        if self.project_base_exclusions and directory_path.name in self.project_base_exclusions:
            return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """
        [Class method intent]
        Serializes hierarchical configuration to dictionary format for persistence, debugging,
        and integration with external systems requiring configuration data.

        [Design principles]
        Complete serialization preserving all configuration state for reproducible operations.
        Hierarchical dictionary format matching the new configuration structure.
        Handles complex types like sets and enums with appropriate conversion.

        [Implementation details]
        Converts sets to lists for JSON compatibility while preserving semantics.
        Enum values converted to string representation for serialization safety.
        All nested configuration groups serialized with proper structure.
        """
        return {
            'handler_type': self.handler_type,
            'description': self.description,
            'file_processing': {
                'max_file_size': self.file_processing.max_file_size,
                'batch_size': self.file_processing.batch_size,
                'max_concurrent_operations': self.file_processing.max_concurrent_operations
            },
            'content_filtering': {
                'excluded_extensions': list(self.content_filtering.excluded_extensions),
                'excluded_directories': list(self.content_filtering.excluded_directories),
                'project_base_exclusions': list(self.content_filtering.project_base_exclusions) if self.content_filtering.project_base_exclusions else None
            },
            'llm_config': {
                'llm_model': self.llm_config.llm_model,
                'temperature': self.llm_config.temperature,
                'max_tokens': self.llm_config.max_tokens
            },
            'change_detection': {
                'indexing_mode': self.change_detection.indexing_mode.value,
                'timestamp_tolerance_seconds': self.change_detection.timestamp_tolerance_seconds
            },
            'error_handling': {
                'max_retries': self.error_handling.max_retries,
                'retry_delay_seconds': self.error_handling.retry_delay_seconds,
                'continue_on_file_errors': self.error_handling.continue_on_file_errors
            },
            'output_config': {
                'knowledge_output_directory': str(self.output_config.knowledge_output_directory) if self.output_config.knowledge_output_directory else None
            },
            'debug_config': {
                'debug_mode': self.debug_config.debug_mode,
                'debug_output_directory': str(self.debug_config.debug_output_directory) if self.debug_config.debug_output_directory else None,
                'enable_llm_replay': self.debug_config.enable_llm_replay,
                'dry_run': self.debug_config.dry_run
            },
            'cleanup_config': {
                'cleanup_mode_enabled': self.cleanup_config.cleanup_mode_enabled,
                'cleanup_types': self.cleanup_config.cleanup_types
            }
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'IndexingConfig':
        """
        [Class method intent]
        Creates IndexingConfig instance from hierarchical validated dictionary.
        Enables configuration loading from JSON files through configuration manager.

        [Design principles]
        Type-safe configuration creation from external hierarchical data sources.
        Proper handling of complex types requiring conversion from JSON-compatible formats.
        Validation through normal dataclass validation ensuring configuration consistency.

        [Implementation details]
        Processes hierarchical configuration groups into appropriate dataclass instances.
        Converts list parameters back to sets for excluded_extensions and excluded_directories.
        Handles optional parameters with proper None value processing.
        Creates IndexingConfig using standard dataclass constructor with full validation.
        """
        # Create a copy to avoid modifying the original dictionary
        config_data = config_dict.copy()
        
        # Extract handler identification
        handler_type = config_data.get('handler_type', 'project-base')
        description = config_data.get('description', 'Hierarchical indexing configuration')
        
        # Process file_processing configuration
        file_processing_data = config_data.get('file_processing', {})
        file_processing = FileProcessingConfig(
            max_file_size=file_processing_data.get('max_file_size', 2 * 1024 * 1024),
            batch_size=file_processing_data.get('batch_size', 7),
            max_concurrent_operations=file_processing_data.get('max_concurrent_operations', 3)
        )
        
        # Process content_filtering configuration
        content_filtering_data = config_data.get('content_filtering', {})
        excluded_extensions = content_filtering_data.get('excluded_extensions', [])
        if excluded_extensions:
            excluded_extensions = set(excluded_extensions)
        else:
            excluded_extensions = {
                '.pyc', '.pyo', '.git', '__pycache__', 
                '.DS_Store', '.env', '.log', '.tmp',
                '.cache', '.pytest_cache', '.mypy_cache'
            }
        
        excluded_directories = content_filtering_data.get('excluded_directories', [])
        if excluded_directories:
            excluded_directories = set(excluded_directories)
        else:
            excluded_directories = {
                '.git', '__pycache__', '.pytest_cache', 
                '.mypy_cache', 'node_modules', '.venv', 'venv'
            }
        
        project_base_exclusions_list = content_filtering_data.get('project_base_exclusions')
        project_base_exclusions = set(project_base_exclusions_list) if project_base_exclusions_list else None
        
        content_filtering = ContentFilteringConfig(
            excluded_extensions=excluded_extensions,
            excluded_directories=excluded_directories,
            project_base_exclusions=project_base_exclusions
        )
        
        # Process llm_config configuration
        llm_config_data = config_data.get('llm_config', {})
        llm_config = LLMConfig(
            llm_model=llm_config_data.get('llm_model', Claude4SonnetModel.CLAUDE_4_SONNET),
            temperature=llm_config_data.get('temperature', 0.3),
            max_tokens=llm_config_data.get('max_tokens', 20000)
        )
        
        # Process change_detection configuration
        change_detection_data = config_data.get('change_detection', {})
        indexing_mode_str = change_detection_data.get('indexing_mode', 'incremental')
        if isinstance(indexing_mode_str, str):
            indexing_mode = IndexingMode(indexing_mode_str)
        else:
            indexing_mode = indexing_mode_str
        
        change_detection = ChangeDetectionConfig(
            indexing_mode=indexing_mode,
            timestamp_tolerance_seconds=change_detection_data.get('timestamp_tolerance_seconds', 2)
        )
        
        # Process error_handling configuration
        error_handling_data = config_data.get('error_handling', {})
        error_handling = ErrorHandlingConfig(
            max_retries=error_handling_data.get('max_retries', 3),
            retry_delay_seconds=error_handling_data.get('retry_delay_seconds', 1.0),
            continue_on_file_errors=error_handling_data.get('continue_on_file_errors', True)
        )
        
        # Process output_config configuration
        output_config_data = config_data.get('output_config', {})
        knowledge_output_directory_str = output_config_data.get('knowledge_output_directory')
        knowledge_output_directory = Path(knowledge_output_directory_str) if knowledge_output_directory_str else None
        
        output_config = OutputConfig(
            knowledge_output_directory=knowledge_output_directory
        )
        
        # Process debug_config configuration
        debug_config_data = config_data.get('debug_config', {})
        debug_output_directory_str = debug_config_data.get('debug_output_directory')
        debug_output_directory = Path(debug_output_directory_str) if debug_output_directory_str else None
        
        debug_config = DebugConfig(
            debug_mode=debug_config_data.get('debug_mode', False),
            debug_output_directory=debug_output_directory,
            enable_llm_replay=debug_config_data.get('enable_llm_replay', False),
            dry_run=debug_config_data.get('dry_run', False)
        )
        
        # Process cleanup_config configuration
        cleanup_config_data = config_data.get('cleanup_config', {})
        cleanup_config = CleanupConfig(
            cleanup_mode_enabled=cleanup_config_data.get('cleanup_mode_enabled', False),
            cleanup_types=cleanup_config_data.get('cleanup_types', [])
        )
        
        # Create IndexingConfig instance with hierarchical configuration groups
        return cls(
            handler_type=handler_type,
            description=description,
            file_processing=file_processing,
            content_filtering=content_filtering,
            llm_config=llm_config,
            change_detection=change_detection,
            error_handling=error_handling,
            output_config=output_config,
            debug_config=debug_config,
            cleanup_config=cleanup_config
        )
    
    @classmethod
    def load_for_handler(cls, handler_type: str, knowledge_dir: Optional[Path] = None) -> 'IndexingConfig':
        """
        [Class method intent]
        Convenience method to load configuration for specified handler type.
        Integrates with IndexingConfigManager for auto-generation and validation.

        [Design principles]
        Simple interface for handler-specific configuration loading.
        Auto-generation of missing configurations using centralized defaults.
        Integration with project root detection for knowledge directory location.

        [Implementation details]
        Uses project root detection when knowledge_dir is not provided.
        Creates IndexingConfigManager instance for configuration loading.
        Returns validated IndexingConfig ready for indexing operations.
        """
        # Import here to avoid circular imports
        from ..indexing.config_manager import IndexingConfigManager
        
        # Determine knowledge directory
        if knowledge_dir is None:
            project_root = get_project_root()
            if project_root:
                knowledge_dir = project_root / '.knowledge'
            else:
                raise ValueError("Could not determine knowledge directory - please provide knowledge_dir parameter")
        
        # Load configuration using manager
        manager = IndexingConfigManager(knowledge_dir)
        return manager.load_config(handler_type)

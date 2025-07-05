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
# Configuration manager for Knowledge Bases Hierarchical Indexing System.
# Handles JSON configuration file loading, auto-generation from Python defaults,
# and Pydantic validation for type-safe configuration management.
###############################################################################
# [Source file design principles]
# - Auto-generation of missing JSON configuration files from centralized defaults
# - Pydantic-based validation ensuring type safety and configuration consistency
# - JSON-based runtime configuration enabling user customization without code changes
# - Immutable configuration loading preventing runtime configuration modifications
# - Comprehensive error handling with descriptive validation messages
###############################################################################
# [Source file constraints]
# - All JSON configurations must pass Pydantic validation before use
# - Configuration files must be auto-generated when missing using centralized defaults
# - Handler type validation must prevent unsupported configuration loading
# - File system operations must handle permission errors and missing directories gracefully
# - Configuration loading must be thread-safe for concurrent indexing operations
###############################################################################
# [Dependencies]
# <codebase>: .defaults - Centralized default configuration templates
# <codebase>: ..models.indexing_config - IndexingConfig class and Pydantic models
# <system>: json - JSON serialization and deserialization
# <system>: pathlib - Cross-platform path operations
# <system>: pydantic - Configuration validation and type safety
# <system>: logging - Structured logging for configuration operations
###############################################################################
# [GenAI tool change history]
# 2025-07-05T15:56:00Z : Initial configuration manager creation by CodeAssistant
# * Created IndexingConfigManager with JSON config loading and auto-generation
# * Implemented Pydantic validation for type-safe configuration management
# * Added comprehensive error handling for file operations and validation
# * Integrated with centralized defaults for missing configuration auto-generation
###############################################################################

"""
Configuration Manager for Knowledge Bases Indexing System.

This module provides configuration management capabilities including:
- Auto-generation of JSON configuration files from Python defaults
- Pydantic validation for type-safe configuration loading
- Handler-specific configuration loading and validation
- User-customizable JSON configuration files

The manager bridges between centralized Python defaults and runtime JSON configurations,
enabling user customization while maintaining type safety and sensible defaults.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError
from enum import Enum

from .defaults import get_default_config, validate_handler_type, get_supported_handler_types
from ..models.indexing_config import IndexingConfig

logger = logging.getLogger(__name__)


class HandlerType(str, Enum):
    """
    [Enum intent]
    Defines supported indexing handler types for configuration management.
    Provides type-safe enumeration of available handler configurations.

    [Design principles]
    String-based enum enabling JSON serialization and human-readable configuration.
    Comprehensive coverage of all supported indexing handler scenarios.

    [Implementation details]
    Enum values match handler type keys in default configuration registry.
    String inheritance enables direct JSON serialization without custom encoders.
    """
    PROJECT_BASE = "project-base"
    GIT_CLONES = "git-clones"
    PDF_KNOWLEDGE = "pdf-knowledge"


class FileProcessingConfigModel(BaseModel):
    """Pydantic model for file processing configuration validation."""
    max_file_size: int = Field(gt=0, description="Maximum file size in bytes")
    batch_size: int = Field(gt=0, description="Files per LLM batch")
    max_concurrent_operations: int = Field(gt=0, description="Async concurrency limit")


class ContentFilteringConfigModel(BaseModel):
    """Pydantic model for content filtering configuration validation."""
    excluded_extensions: list = Field(default_factory=list, description="File extensions to exclude")
    excluded_directories: list = Field(default_factory=list, description="Directory names to exclude")
    project_base_exclusions: Optional[list] = Field(default=None, description="Project-base specific exclusions")


class LLMConfigModel(BaseModel):
    """Pydantic model for LLM configuration validation."""
    llm_model: str = Field(..., description="LLM model identifier")
    temperature: float = Field(ge=0.0, le=1.0, description="LLM temperature setting")
    max_tokens: int = Field(gt=0, description="Maximum response tokens")


class ChangeDetectionConfigModel(BaseModel):
    """Pydantic model for change detection configuration validation."""
    indexing_mode: str = Field(..., description="Indexing mode: full or incremental")
    timestamp_tolerance_seconds: int = Field(ge=0, description="Timestamp comparison tolerance")
    
    @field_validator('indexing_mode')
    @classmethod
    def validate_indexing_mode(cls, v):
        """Validate indexing mode is supported."""
        valid_modes = ['full', 'full_kb_rebuild', 'incremental']
        if v not in valid_modes:
            raise ValueError(f"indexing_mode must be one of {valid_modes}, got {v}")
        return v


class ErrorHandlingConfigModel(BaseModel):
    """Pydantic model for error handling configuration validation."""
    max_retries: int = Field(ge=0, description="Maximum retry attempts")
    retry_delay_seconds: float = Field(ge=0.0, description="Delay between retries")
    continue_on_file_errors: bool = Field(description="Continue processing on file errors")


class OutputConfigModel(BaseModel):
    """Pydantic model for output configuration validation."""
    knowledge_output_directory: Optional[str] = Field(default=None, description="Knowledge output directory path")


class DebugConfigModel(BaseModel):
    """Pydantic model for debug configuration validation."""
    debug_mode: bool = Field(description="Enable debug mode")
    debug_output_directory: Optional[str] = Field(default=None, description="Debug output directory path")
    enable_llm_replay: bool = Field(description="Enable LLM response replay")


class IndexingConfigModel(BaseModel):
    """
    [Class intent]
    Hierarchical Pydantic model for JSON configuration validation and type safety.
    Provides comprehensive validation for indexing configuration parameters
    with handler-specific validation rules and constraints.

    [Design principles]
    Hierarchical structure matching the new configuration organization.
    Handler-specific validation ensuring configuration consistency and correctness.
    Type-safe parameter validation preventing runtime configuration errors.
    Descriptive validation messages enabling user-friendly error reporting.

    [Implementation details]
    Uses nested Pydantic models for hierarchical configuration validation.
    Implements custom validators for handler-specific configuration requirements.
    Supports optional parameters with sensible defaults for flexible configuration.
    Validates interdependent parameters ensuring configuration consistency.
    """
    
    # Handler identification
    handler_type: HandlerType = Field(..., description="Indexing handler type")
    description: Optional[str] = Field(None, description="Configuration description")
    
    # Hierarchical Configuration Groups
    file_processing: FileProcessingConfigModel = Field(..., description="File processing configuration")
    content_filtering: ContentFilteringConfigModel = Field(..., description="Content filtering configuration")
    llm_config: LLMConfigModel = Field(..., description="LLM configuration")
    change_detection: ChangeDetectionConfigModel = Field(..., description="Change detection configuration")
    error_handling: ErrorHandlingConfigModel = Field(..., description="Error handling configuration")
    output_config: OutputConfigModel = Field(..., description="Output configuration")
    debug_config: DebugConfigModel = Field(..., description="Debug configuration")
    
    @field_validator('content_filtering')
    @classmethod
    def validate_project_base_exclusions(cls, v, info):
        """Validate project_base_exclusions for project-base handler."""
        if info.data and 'handler_type' in info.data:
            handler_type = info.data['handler_type']
            if handler_type == HandlerType.PROJECT_BASE and v.project_base_exclusions is None:
                raise ValueError("project_base_exclusions required for project-base handler")
            if handler_type != HandlerType.PROJECT_BASE and v.project_base_exclusions is not None:
                logger.warning(f"project_base_exclusions ignored for {handler_type} handler")
        return v


class IndexingConfigManager:
    """
    [Class intent]
    Manages indexing configuration loading, validation, and auto-generation.
    Bridges between centralized Python defaults and runtime JSON configurations
    with comprehensive error handling and type-safe validation.

    [Design principles]
    Auto-generation of missing configurations ensuring zero-configuration startup.
    Pydantic validation providing type safety and comprehensive error reporting.
    JSON-based configuration enabling user customization without code modification.
    Immutable configuration loading preventing runtime configuration corruption.
    Comprehensive logging and error handling for operational visibility.

    [Implementation details]
    Uses centralized defaults module for configuration template generation.
    Implements Pydantic validation for type-safe configuration processing.
    Handles file system operations with graceful error recovery and logging.
    Provides configuration caching for performance optimization in repeated loads.
    Integrates with IndexingConfig class for seamless configuration consumption.
    """
    
    def __init__(self, knowledge_directory: Path):
        """
        [Class method intent]
        Initializes configuration manager with knowledge directory for JSON config storage.
        Sets up configuration file location and validates directory accessibility.

        [Design principles]
        Directory-based configuration management supporting project-specific configurations.
        Early validation of directory accessibility preventing runtime failures.
        Comprehensive logging setup for configuration operation visibility.

        [Implementation details]
        Validates knowledge directory existence and accessibility.
        Creates knowledge directory if missing with appropriate permissions.
        Sets up logging context for configuration operation tracking.
        """
        self.knowledge_directory = Path(knowledge_directory)
        self._config_cache: Dict[str, IndexingConfig] = {}
        
        # Ensure knowledge directory exists
        try:
            self.knowledge_directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Initialized IndexingConfigManager with directory: {self.knowledge_directory}")
        except Exception as e:
            logger.error(f"Failed to create knowledge directory {self.knowledge_directory}: {e}")
            raise
    
    def load_config(self, handler_type: str) -> IndexingConfig:
        """
        [Class method intent]
        Loads configuration for specified handler type with auto-generation and caching.
        Returns validated IndexingConfig instance ready for indexing operations.

        [Design principles]
        Auto-generation of missing configurations using centralized defaults.
        Comprehensive validation ensuring type safety and configuration consistency.
        Configuration caching for performance optimization in repeated loads.
        Immutable configuration return preventing runtime configuration modification.

        [Implementation details]
        Validates handler type against supported handler registry.
        Auto-generates JSON configuration from defaults when missing.
        Loads and validates JSON configuration using Pydantic models.
        Converts validated configuration to IndexingConfig instance.
        Caches loaded configuration for performance optimization.
        """
        # Validate handler type
        if not validate_handler_type(handler_type):
            supported_types = get_supported_handler_types()
            raise ValueError(f"Unsupported handler type: {handler_type}. Supported types: {supported_types}")
        
        # Check cache first
        if handler_type in self._config_cache:
            logger.debug(f"Returning cached configuration for handler: {handler_type}")
            return self._config_cache[handler_type]
        
        # Determine configuration file path
        config_file = self.knowledge_directory / f"{handler_type}.indexing-config.json"
        
        # Auto-generate configuration if missing
        if not config_file.exists():
            logger.info(f"Configuration file missing, auto-generating: {config_file}")
            self._generate_default_config(handler_type, config_file)
        
        # Load and validate configuration
        try:
            config = self._load_json_config(config_file)
            self._config_cache[handler_type] = config
            logger.info(f"Successfully loaded configuration for handler: {handler_type}")
            return config
            
        except Exception as e:
            logger.error(f"Failed to load configuration for handler {handler_type}: {e}")
            raise
    
    def _generate_default_config(self, handler_type: str, config_file: Path) -> None:
        """
        [Class method intent]
        Generates default JSON configuration file from centralized Python defaults.
        Creates human-readable JSON configuration enabling user customization.

        [Design principles]
        Template-based configuration generation using centralized defaults.
        Human-readable JSON formatting supporting user customization workflows.
        Comprehensive error handling for file system operations and permissions.
        Atomic file operations preventing partial configuration generation.

        [Implementation details]
        Retrieves default configuration template from centralized defaults module.
        Writes JSON configuration with proper formatting and indentation.
        Handles file system errors with graceful fallback and error reporting.
        Logs configuration generation for operational visibility and debugging.
        """
        try:
            # Get default configuration template
            default_config = get_default_config(handler_type)
            
            # Ensure parent directory exists
            config_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Write JSON configuration with proper formatting
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Generated default configuration: {config_file}")
            
        except Exception as e:
            logger.error(f"Failed to generate default configuration {config_file}: {e}")
            raise
    
    def _load_json_config(self, config_file: Path) -> IndexingConfig:
        """
        [Class method intent]
        Loads and validates JSON configuration file using Pydantic validation.
        Converts validated configuration to IndexingConfig instance.

        [Design principles]
        Comprehensive validation using Pydantic models for type safety.
        Descriptive error messages enabling user-friendly configuration debugging.
        Immutable configuration conversion preventing runtime modification.
        JSON parsing with proper encoding support for international content.

        [Implementation details]
        Loads JSON configuration with UTF-8 encoding support.
        Validates configuration using Pydantic IndexingConfigModel.
        Converts validated Pydantic model to IndexingConfig instance.
        Provides detailed error reporting for validation failures and file errors.
        """
        try:
            # Load JSON configuration
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Validate using Pydantic model
            try:
                config_model = IndexingConfigModel(**config_data)
            except ValidationError as e:
                logger.error(f"Configuration validation failed for {config_file}:")
                for error in e.errors():
                    logger.error(f"  {error['loc']}: {error['msg']}")
                raise ValueError(f"Invalid configuration in {config_file}: {e}")
            
            # Convert to IndexingConfig
            return self._convert_to_indexing_config(config_model)
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file {config_file}: {e}")
            raise ValueError(f"Invalid JSON format in {config_file}: {e}")
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_file}")
            raise
        except Exception as e:
            logger.error(f"Failed to load configuration from {config_file}: {e}")
            raise
    
    def _convert_to_indexing_config(self, config_model: IndexingConfigModel) -> IndexingConfig:
        """
        [Class method intent]
        Converts validated hierarchical Pydantic model to IndexingConfig instance.
        Handles type conversion and optional parameter processing from hierarchical structure.

        [Design principles]
        Type-safe conversion ensuring parameter compatibility between hierarchical and flat models.
        Proper handling of optional parameters and default value assignment.
        Immutable configuration creation preventing post-creation modification.

        [Implementation details]
        Extracts parameters from hierarchical Pydantic model structure.
        Handles set conversion for excluded_extensions and excluded_directories.
        Processes optional parameters with appropriate default value assignment.
        Creates IndexingConfig instance using IndexingConfig.from_dict() method.
        """
        # Convert hierarchical Pydantic model to flat dictionary structure
        config_dict = config_model.model_dump()
        
        # Use IndexingConfig.from_dict() which handles hierarchical structure conversion
        return IndexingConfig.from_dict(config_dict)
    
    def get_config_file_path(self, handler_type: str) -> Path:
        """
        [Class method intent]
        Returns path to JSON configuration file for specified handler type.
        Enables external access to configuration file locations.

        [Design principles]
        Path abstraction enabling external configuration file operations.
        Handler type validation ensuring only supported configurations are accessed.

        [Implementation details]
        Validates handler type against supported handler registry.
        Returns Path object for configuration file location.
        """
        if not validate_handler_type(handler_type):
            supported_types = get_supported_handler_types()
            raise ValueError(f"Unsupported handler type: {handler_type}. Supported types: {supported_types}")
        
        return self.knowledge_directory / f"{handler_type}.indexing-config.json"
    
    def clear_cache(self) -> None:
        """
        [Class method intent]
        Clears configuration cache forcing reload on next access.
        Enables configuration refresh after external configuration changes.

        [Design principles]
        Cache invalidation supporting dynamic configuration updates.
        Simple interface for configuration refresh operations.

        [Implementation details]
        Clears internal configuration cache dictionary.
        Logs cache clearing for operational visibility.
        """
        self._config_cache.clear()
        logger.debug("Configuration cache cleared")

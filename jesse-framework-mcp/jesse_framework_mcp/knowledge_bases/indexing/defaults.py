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
# Centralized default configurations for Knowledge Bases Hierarchical Indexing System.
# Provides reasonable defaults for project-base, git-clones, and pdf-knowledge indexing handlers
# used to auto-generate JSON configuration files when they don't exist.
###############################################################################
# [Source file design principles]
# - Handler-specific optimized configurations with sensible defaults
# - Hierarchical exclusion system with base and handler-specific exclusions
# - Template-based configuration supporting user customization via JSON files
# - Type-safe configuration generation with comprehensive parameter coverage
# - Clear separation between Python defaults and runtime JSON configurations
###############################################################################
# [Source file constraints]
# - All configurations must include complete IndexingConfig parameter coverage
# - Handler-specific exclusions must be clearly separated from base exclusions
# - Default values must be production-ready and performance-optimized
# - Configuration templates must support Pydantic validation requirements
# - Must maintain backward compatibility with existing IndexingConfig structure
###############################################################################
# [Dependencies]
# <codebase>: jesse_framework_mcp.llm.strands_agent_driver.models - Claude model configuration
# <system>: typing - Type annotations for configuration templates
# <system>: copy - Deep copying for configuration template generation
###############################################################################
# [GenAI tool change history]
# 2025-07-05T17:32:00Z : Configuration structure hierarchical reorganization by CodeAssistant
# * Restructured all three configuration templates with logical grouping (file_processing, content_filtering, llm_config, etc.)
# * Maintained backward compatibility by keeping all existing configuration keys and values
# * Improved maintainability and discoverability through clear hierarchical organization
# * Enhanced documentation with grouped comments explaining configuration sections
# 2025-07-05T15:55:00Z : Initial centralized defaults creation by CodeAssistant
# * Created PROJECT_BASE_DEFAULT_CONFIG with comprehensive exclusion rules
# * Created GIT_CLONES_DEFAULT_CONFIG optimized for git clone processing
# * Created PDF_KNOWLEDGE_DEFAULT_CONFIG with document-specific optimizations
###############################################################################

"""
Centralized Default Configurations for Knowledge Bases Indexing Handlers.

This module provides default configuration templates for the three primary indexing handlers:
- project-base: Whole codebase indexing with system directory exclusions
- git-clones: Read-only git clone processing with mirrored structure
- pdf-knowledge: PDF document processing and knowledge extraction

These defaults are used to auto-generate JSON configuration files when they don't exist,
enabling user customization while providing sensible production-ready defaults.
"""

import copy
from typing import Dict, Any, List, Set
from jesse_framework_mcp.llm.strands_agent_driver.models import Claude4SonnetModel


# Base exclusions applied to all indexing handlers
BASE_EXCLUDED_EXTENSIONS: Set[str] = {
    '.pyc', '.pyo', '.git', '__pycache__', 
    '.DS_Store', '.env', '.log', '.tmp',
    '.cache', '.pytest_cache', '.mypy_cache',
    '.tox', '.coverage', '.swp', '.swo',
    '.bak', '.orig', '.rej'
}

BASE_EXCLUDED_DIRECTORIES: Set[str] = {
    '.git', '__pycache__', '.pytest_cache', 
    '.mypy_cache', 'node_modules', '.venv', 'venv',
    '.tox', 'dist', 'build', '.cache',
    '.coverage', '.nyc_output', 'coverage',
    'target', 'bin', 'obj'  # Common build output directories
}

# Project-base specific exclusions (in addition to base exclusions)
PROJECT_BASE_EXCLUSIONS: Set[str] = {
    '.knowledge',       # Knowledge base output directory
    '.coding_assistant', # AI assistant workspace
    '.clinerules'       # Cline configuration rules
}

# Configuration templates for each handler type
PROJECT_BASE_DEFAULT_CONFIG: Dict[str, Any] = {
    # Handler Identification
    "handler_type": "project-base",
    "description": "Whole project codebase indexing with system directory exclusions",
    
    # File Processing Limits
    "file_processing": {
        "max_file_size": 2 * 1024 * 1024,  # 2MB max per file
        "batch_size": 7,                    # Files per LLM batch (cost/performance balance)
        "max_concurrent_operations": 3      # Async concurrency limit
    },
    
    # Content Filtering Rules
    "content_filtering": {
        "excluded_extensions": list(BASE_EXCLUDED_EXTENSIONS),
        "excluded_directories": list(BASE_EXCLUDED_DIRECTORIES),
        "project_base_exclusions": list(PROJECT_BASE_EXCLUSIONS)
    },
    
    # LLM Configuration
    "llm_config": {
        "llm_model": Claude4SonnetModel.CLAUDE_4_SONNET,
        "temperature": 0.3,  # Low temperature for consistent summarization
        "max_tokens": 20000  # Response length limit
    },
    
    # Change Detection & Processing Mode
    "change_detection": {
        "indexing_mode": "incremental",          # "full" | "incremental"
        "timestamp_tolerance_seconds": 2         # Filesystem timestamp comparison tolerance
    },
    
    # Error Handling & Resilience
    "error_handling": {
        "max_retries": 3,
        "retry_delay_seconds": 1.0,
        "continue_on_file_errors": True  # Continue processing when individual files fail
    },
    
    # Output Configuration
    "output_config": {
        "knowledge_output_directory": None  # Defaults to {PROJECT_ROOT}/.knowledge/ when None
    },
    
    # Debug & Development
    "debug_config": {
        "debug_mode": False,
        "debug_output_directory": None,  # Directory for debug artifacts (defaults to temp when None)
        "enable_llm_replay": False
    }
}

GIT_CLONES_DEFAULT_CONFIG: Dict[str, Any] = {
    # Handler Identification
    "handler_type": "git-clones",
    "description": "Read-only git clone processing with mirrored knowledge structure",
    
    # File Processing Limits
    "file_processing": {
        "max_file_size": 1 * 1024 * 1024,  # 1MB max (smaller for git clones)
        "batch_size": 5,                    # Smaller batches for varied content
        "max_concurrent_operations": 2      # Conservative for read-only processing
    },
    
    # Content Filtering Rules (no project-base exclusions)
    "content_filtering": {
        "excluded_extensions": list(BASE_EXCLUDED_EXTENSIONS),
        "excluded_directories": list(BASE_EXCLUDED_DIRECTORIES)
        # No project_base_exclusions for git clones
    },
    
    # LLM Configuration
    "llm_config": {
        "llm_model": Claude4SonnetModel.CLAUDE_4_SONNET,
        "temperature": 0.4,  # Slightly higher for diverse content
        "max_tokens": 15000  # Smaller responses for git content
    },
    
    # Change Detection & Processing Mode
    "change_detection": {
        "indexing_mode": "full_kb_rebuild",  # Git clones rebuild KB files but use file analysis cache
        "timestamp_tolerance_seconds": 5     # More tolerance for git timestamps
    },
    
    # Error Handling & Resilience
    "error_handling": {
        "max_retries": 2,        # Fewer retries for read-only content
        "retry_delay_seconds": 0.5,
        "continue_on_file_errors": True
    },
    
    # Output Configuration
    "output_config": {
        "knowledge_output_directory": None  # Defaults to {PROJECT_ROOT}/.knowledge/ when None
    },
    
    # Debug & Development
    "debug_config": {
        "debug_mode": False,
        "debug_output_directory": None,  # Directory for debug artifacts (defaults to temp when None)
        "enable_llm_replay": False
    }
}

PDF_KNOWLEDGE_DEFAULT_CONFIG: Dict[str, Any] = {
    # Handler Identification
    "handler_type": "pdf-knowledge",
    "description": "PDF document processing and knowledge extraction",
    
    # File Processing Limits
    "file_processing": {
        "max_file_size": 10 * 1024 * 1024,  # 10MB max for PDF documents
        "batch_size": 3,                     # Smaller batches for document processing
        "max_concurrent_operations": 2       # Conservative for document extraction
    },
    
    # Content Filtering Rules (PDF-specific)
    "content_filtering": {
        "excluded_extensions": list(BASE_EXCLUDED_EXTENSIONS),  # Use base exclusions for documents too
        "excluded_directories": list(BASE_EXCLUDED_DIRECTORIES)  # Use base exclusions for documents too
        # No project_base_exclusions for PDF processing
    },
    
    # LLM Configuration
    "llm_config": {
        "llm_model": Claude4SonnetModel.CLAUDE_4_SONNET,
        "temperature": 0.2,  # Lower temperature for document analysis
        "max_tokens": 25000  # Larger responses for document summaries
    },
    
    # Change Detection & Processing Mode
    "change_detection": {
        "indexing_mode": "incremental",      # Process new/changed documents
        "timestamp_tolerance_seconds": 10    # More tolerance for document timestamps
    },
    
    # Error Handling & Resilience
    "error_handling": {
        "max_retries": 5,        # More retries for document extraction
        "retry_delay_seconds": 2.0,
        "continue_on_file_errors": True
    },
    
    # Output Configuration
    "output_config": {
        "knowledge_output_directory": None  # Defaults to {PROJECT_ROOT}/.knowledge/ when None
    },
    
    # Debug & Development
    "debug_config": {
        "debug_mode": False,
        "debug_output_directory": None,  # Directory for debug artifacts (defaults to temp when None)
        "enable_llm_replay": False
    }
}

# Configuration registry for handler types
DEFAULT_CONFIGS: Dict[str, Dict[str, Any]] = {
    "project-base": PROJECT_BASE_DEFAULT_CONFIG,
    "git-clones": GIT_CLONES_DEFAULT_CONFIG,
    "pdf-knowledge": PDF_KNOWLEDGE_DEFAULT_CONFIG
}

def get_default_config(handler_type: str) -> Dict[str, Any]:
    """
    [Function intent]
    Retrieves default configuration template for specified handler type.
    Returns deep copy to prevent modification of template defaults.

    [Design principles]
    Immutable template access preventing accidental default modification.
    Handler type validation ensuring only supported configurations are returned.
    Deep copying ensuring template integrity across multiple configuration generations.

    [Implementation details]
    Validates handler type against supported configuration registry.
    Returns deep copy of configuration template for safe customization.
    Raises ValueError for unsupported handler types with clear error messaging.
    """
    if handler_type not in DEFAULT_CONFIGS:
        supported_types = list(DEFAULT_CONFIGS.keys())
        raise ValueError(f"Unsupported handler type: {handler_type}. Supported types: {supported_types}")
    
    return copy.deepcopy(DEFAULT_CONFIGS[handler_type])

def get_supported_handler_types() -> List[str]:
    """
    [Function intent]
    Returns list of supported indexing handler types for configuration generation.
    Provides programmatic access to available handler configurations.

    [Design principles]
    Centralized handler type registry enabling dynamic configuration discovery.
    Immutable list return preventing accidental registry modification.

    [Implementation details]
    Returns sorted list of handler types from configuration registry.
    Enables validation and UI generation for handler type selection.
    """
    return sorted(DEFAULT_CONFIGS.keys())

def validate_handler_type(handler_type: str) -> bool:
    """
    [Function intent]
    Validates if handler type is supported by the configuration system.
    Provides boolean validation for handler type checking.

    [Design principles]
    Simple validation interface supporting configuration validation workflows.
    Clear boolean return enabling straightforward conditional logic.

    [Implementation details]
    Checks handler type against configuration registry keys.
    Returns boolean result for use in validation and error handling.
    """
    return handler_type in DEFAULT_CONFIGS

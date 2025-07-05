<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/config_manager.py -->
<!-- Cached On: 2025-07-05T20:32:35.253495 -->
<!-- Source Modified: 2025-07-05T20:01:57.484013 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

The `config_manager.py` file serves as the central configuration management system for the Jesse Framework MCP's knowledge base indexing operations, providing auto-generation of missing JSON configuration files from centralized Python defaults and comprehensive `Pydantic` validation for type-safe configuration management. This module enables user-customizable JSON configuration files while maintaining immutable configuration loading that prevents runtime modifications, evidenced by the `IndexingConfigManager` class with its `load_config()` method and configuration caching via `_config_cache`. Key semantic entities include `HandlerType` enum with values `PROJECT_BASE`, `GIT_CLONES`, and `PDF_KNOWLEDGE`, hierarchical `Pydantic` models like `FileProcessingConfigModel`, `ContentFilteringConfigModel`, and `LLMConfigModel`, plus integration with `.defaults` module through `get_default_config()` and `validate_handler_type()` functions. The system bridges centralized Python defaults with runtime JSON configurations through the `IndexingConfigModel` class that validates handler-specific parameters and converts to `IndexingConfig` instances via `from_dict()` method.

##### Main Components

The file contains the `IndexingConfigManager` class as the primary configuration orchestrator, seven specialized `Pydantic` validation models (`FileProcessingConfigModel`, `ContentFilteringConfigModel`, `LLMConfigModel`, `ChangeDetectionConfigModel`, `ErrorHandlingConfigModel`, `OutputConfigModel`, `DebugConfigModel`), the comprehensive `IndexingConfigModel` that aggregates all validation models, and the `HandlerType` enum defining supported indexing handler types. The manager provides core methods including `load_config()` for configuration loading with auto-generation, `_generate_default_config()` for JSON file creation, `_load_json_config()` for validation and loading, and `_convert_to_indexing_config()` for model transformation.

###### Architecture & Design

The architecture follows a hierarchical validation pattern with nested `Pydantic` models that mirror the configuration structure, enabling comprehensive type safety and validation at each level. The design implements an auto-generation strategy where missing JSON configuration files are created from centralized defaults, combined with immutable configuration loading that prevents runtime modifications through caching and conversion to `IndexingConfig` instances. The system uses a bridge pattern between Python defaults and JSON runtime configurations, with the `IndexingConfigManager` serving as the facade that coordinates between the defaults module, file system operations, and validation models.

####### Implementation Approach

The implementation employs `Pydantic` model validation with custom field validators like `validate_indexing_mode()` and `validate_project_base_exclusions()` that enforce handler-specific constraints and cross-field validation rules. Configuration loading uses a multi-stage approach: handler type validation, cache checking, auto-generation of missing files, JSON loading with UTF-8 encoding, `Pydantic` validation, and conversion to `IndexingConfig` instances. The system implements configuration caching through the `_config_cache` dictionary to optimize repeated loads, and uses atomic file operations with proper error handling for configuration generation and loading operations.

######## External Dependencies & Integration Points

**→ Inbound:** [configuration management dependencies]
- `.defaults:get_default_config` - centralized configuration template retrieval
- `.defaults:validate_handler_type` - handler type validation logic
- `..models.indexing_config:IndexingConfig` - target configuration class for conversion
- `json` (external library) - JSON serialization and parsing operations
- `pathlib` (external library) - cross-platform file system path operations
- `pydantic` (external library) - configuration validation and type safety

**← Outbound:** [configuration consumers]
- `knowledge_bases/indexing/` - indexing operations consuming validated configurations
- `*.indexing-config.json` - generated JSON configuration files for user customization
- `IndexingConfig` instances - validated configuration objects for indexing workflows

**⚡ System role and ecosystem integration:**
- **System Role**: Central configuration hub that bridges Python defaults with JSON runtime configurations for the knowledge base indexing system, ensuring type-safe configuration management across all indexing operations
- **Ecosystem Position**: Core infrastructure component that enables zero-configuration startup while supporting user customization through JSON files
- **Integration Pattern**: Used by indexing handlers during initialization to load validated configurations, with auto-generation ensuring seamless deployment and user customization through standard JSON editing workflows

######### Edge Cases & Error Handling

The system handles JSON parsing errors through `JSONDecodeError` catching with descriptive error messages, `Pydantic` validation failures with detailed field-level error reporting via `ValidationError.errors()`, and file system permission errors during configuration generation and loading. Handler type validation prevents unsupported configuration loading with comprehensive error messages listing supported types from `get_supported_handler_types()`. The manager handles missing configuration files through automatic generation, directory creation failures with graceful error propagation, and provides configuration cache clearing via `clear_cache()` for dynamic configuration updates.

########## Internal Implementation Details

The `_config_cache` dictionary provides performance optimization for repeated configuration loads, keyed by handler type strings. Configuration file naming follows the pattern `{handler_type}.indexing-config.json` within the knowledge directory structure. The `_convert_to_indexing_config()` method handles hierarchical to flat dictionary conversion using `model_dump()` and delegates to `IndexingConfig.from_dict()` for final object creation. File operations use UTF-8 encoding with proper exception handling, and JSON generation includes indentation and ASCII escaping configuration for human-readable output. The validation system supports cross-field validation through `field_validator` decorators with access to other field values via the `info` parameter.

########### Code Usage Examples

This example demonstrates initializing the configuration manager and loading a validated configuration for project-base indexing operations:

```python
from pathlib import Path
from jesse_framework_mcp.knowledge_bases.indexing.config_manager import IndexingConfigManager

# Initialize configuration manager with knowledge directory
config_manager = IndexingConfigManager(Path("./knowledge_bases"))

# Load configuration for project-base handler (auto-generates if missing)
config = config_manager.load_config("project-base")

# Access validated configuration parameters
print(f"Max file size: {config.max_file_size}")
print(f"Batch size: {config.batch_size}")
print(f"LLM model: {config.llm_model}")
```

This example shows how to clear the configuration cache and reload updated configurations:

```python
# Clear cache to force reload of updated configurations
config_manager.clear_cache()

# Get configuration file path for manual editing
config_path = config_manager.get_config_file_path("pdf-knowledge")
print(f"Edit configuration at: {config_path}")

# Reload configuration after manual changes
updated_config = config_manager.load_config("pdf-knowledge")
```
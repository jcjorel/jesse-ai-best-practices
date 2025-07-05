<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/models/indexing_config.py -->
<!-- Cached On: 2025-07-05T20:36:27.966058 -->
<!-- Source Modified: 2025-07-05T19:59:47.807652 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

The `indexing_config.py` file serves as the comprehensive configuration data model for the Jesse Framework MCP's knowledge base hierarchical indexing system, providing immutable type-safe configuration management with validation at initialization through frozen dataclasses. This module enables centralized control of all indexing parameters including file processing constraints, LLM integration settings, and specialized handling requirements, evidenced by the main `IndexingConfig` class with hierarchical configuration groups and the `IndexingMode` enum with values `FULL`, `FULL_KB_REBUILD`, and `INCREMENTAL`. Key semantic entities include configuration dataclasses like `FileProcessingConfig`, `ContentFilteringConfig`, `LLMConfig`, `ChangeDetectionConfig`, `ErrorHandlingConfig`, `OutputConfig`, and `DebugConfig`, integration with `Claude4SonnetModel.CLAUDE_4_SONNET` for LLM configuration, utility methods `should_process_file()` and `should_process_directory()` for filtering decisions, and serialization methods `to_dict()` and `from_dict()` for persistence and configuration manager integration. The system implements automatic default knowledge directory setting to `{PROJECT_ROOT}/.knowledge/` through `get_project_root()` integration and provides backward compatibility through property accessors for flat configuration access patterns.

##### Main Components

The file contains the primary `IndexingConfig` frozen dataclass with seven hierarchical configuration groups, six specialized configuration dataclasses (`FileProcessingConfig`, `ContentFilteringConfig`, `LLMConfig`, `ChangeDetectionConfig`, `ErrorHandlingConfig`, `OutputConfig`, `DebugConfig`) that organize related parameters, and the `IndexingMode` enum defining processing strategies. Core methods include `__post_init__()` for validation and default setting, filtering methods `should_process_file()` and `should_process_directory()` for processing decisions, serialization methods `to_dict()` and `from_dict()` for configuration persistence, and the class method `load_for_handler()` for configuration manager integration. The class provides comprehensive property accessors for backward compatibility, enabling flat access to hierarchically organized configuration parameters.

###### Architecture & Design

The architecture follows a hierarchical frozen dataclass pattern with specialized configuration groups that organize related parameters into logical domains, enabling maintainable configuration management while preserving immutability after initialization. The design implements a composition pattern where the main `IndexingConfig` class contains focused configuration objects for different concerns, combined with property accessors that provide backward compatibility during the transition from flat to hierarchical configuration structures. The system uses defensive validation through `__post_init__()` that checks all parameters at creation time, integrated with automatic default setting for the knowledge output directory using project root detection. Each configuration group follows the frozen dataclass pattern ensuring immutability while providing clear separation of concerns between file processing, content filtering, LLM integration, change detection, error handling, output management, and debug functionality.

####### Implementation Approach

The implementation employs frozen dataclasses with `field(default_factory=...)` for complex default values like sets and nested configuration objects, ensuring proper initialization without shared mutable state between instances. Configuration validation uses comprehensive parameter checking in `__post_init__()` with descriptive error messages for invalid values, including range validation for temperature (0.0-1.0), positive value validation for file sizes and batch parameters, and non-negative validation for retry settings. The filtering system implements efficient set-based membership testing for excluded extensions and directories, with specialized logic for project-base exclusions through optional `project_base_exclusions` parameter. Serialization handles complex type conversion including sets to lists for JSON compatibility, enum values to strings, and Path objects to string representations, with corresponding deserialization logic in `from_dict()` that reconstructs proper types from JSON-compatible formats.

######## External Dependencies & Integration Points

**→ Inbound:** [configuration model dependencies]
- `jesse_framework_mcp.llm.strands_agent_driver.models:Claude4SonnetModel` - LLM model constants for configuration defaults
- `jesse_framework_mcp.helpers.path_utils:get_project_root` - project root detection for default knowledge directory
- `dataclasses` (external library) - frozen dataclass implementation for immutable configuration
- `pathlib` (external library) - path handling and validation for directory configuration
- `typing` (external library) - type annotations for configuration parameters
- `enum` (external library) - IndexingMode enumeration for processing strategies

**← Outbound:** [configuration consumers]
- `../indexing/config_manager.py:IndexingConfigManager` - configuration loading and validation through from_dict method
- `knowledge_bases/indexing/` - indexing operations consuming configuration parameters through property accessors
- `*.indexing-config.json` - JSON configuration files generated through to_dict serialization
- `hierarchical_indexer.py` - indexing operations using filtering methods and processing parameters

**⚡ System role and ecosystem integration:**
- **System Role**: Central configuration model that defines all parameters for knowledge base indexing operations, serving as the single source of truth for indexing behavior across the Jesse Framework MCP system
- **Ecosystem Position**: Core data model that bridges between configuration management, indexing operations, and LLM integration, enabling type-safe configuration with validation
- **Integration Pattern**: Used by indexing handlers through property access, configuration managers through serialization methods, and validation systems through filtering methods, with automatic integration to project structure through default directory setting

######### Edge Cases & Error Handling

The system handles invalid configuration parameters through comprehensive validation in `__post_init__()` that raises `ValueError` with descriptive messages for out-of-range values, negative parameters, and invalid LLM settings. File and directory filtering methods include defensive checks for file system errors, handling `OSError` and `FileNotFoundError` exceptions gracefully by returning `False` for inaccessible files. Configuration serialization handles optional parameters through proper None checking, converting Path objects to strings safely, and managing complex type conversions between sets/lists and enums/strings. The `from_dict()` method provides robust deserialization with fallback defaults for missing parameters, proper type conversion from JSON-compatible formats, and validation through normal dataclass initialization. Project root detection failures are handled gracefully by maintaining `None` values for knowledge directory configuration, enabling fallback behavior in consuming systems.

########## Internal Implementation Details

The configuration groups use `field(default_factory=...)` with lambda functions to create fresh instances of sets and configuration objects, preventing shared mutable state between `IndexingConfig` instances. Default knowledge directory setting uses `object.__setattr__()` to modify the frozen dataclass during `__post_init__()`, creating a new `OutputConfig` instance with the resolved project root path. Property accessors provide direct access to nested configuration parameters without exposing the hierarchical structure, maintaining backward compatibility during the transition period. The filtering system uses set membership testing for O(1) performance on excluded extensions and directories, with case-sensitive directory name comparison and lowercase extension comparison for consistent behavior. Serialization preserves all configuration state through complete dictionary representation, handling complex types like `IndexingMode.value` for enum serialization and conditional string conversion for optional Path parameters.

########### Code Usage Examples

This example demonstrates creating and validating a basic indexing configuration with custom parameters. The code shows how to initialize the configuration with hierarchical groups and access parameters through both hierarchical and flat property access patterns.

```python
from pathlib import Path
from jesse_framework_mcp.knowledge_bases.models.indexing_config import (
    IndexingConfig, FileProcessingConfig, LLMConfig, IndexingMode
)

# Create configuration with custom file processing settings
file_config = FileProcessingConfig(max_file_size=1024*1024, batch_size=5)
llm_config = LLMConfig(temperature=0.2, max_tokens=15000)

config = IndexingConfig(
    handler_type="git-clones",
    file_processing=file_config,
    llm_config=llm_config
)

# Access through both hierarchical and flat patterns
print(f"Max file size: {config.file_processing.max_file_size}")
print(f"Max file size (flat): {config.max_file_size}")
print(f"LLM model: {config.llm_model}")
```

This example shows configuration serialization and deserialization for persistence and configuration management integration. The code demonstrates the complete round-trip process for configuration storage and loading.

```python
# Serialize configuration to dictionary for JSON storage
config_dict = config.to_dict()
print(f"Serialized config: {config_dict['handler_type']}")

# Deserialize configuration from dictionary (e.g., from JSON file)
loaded_config = IndexingConfig.from_dict(config_dict)
print(f"Loaded handler: {loaded_config.handler_type}")

# Use filtering methods for file processing decisions
test_file = Path("example.py")
if loaded_config.should_process_file(test_file):
    print(f"Will process: {test_file}")

# Load configuration for specific handler using convenience method
project_config = IndexingConfig.load_for_handler("project-base")
print(f"Project config mode: {project_config.indexing_mode}")
```
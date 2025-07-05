<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/models/indexing_config.py -->
<!-- Cached On: 2025-07-05T16:21:50.925160 -->
<!-- Source Modified: 2025-07-05T16:04:02.868441 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This configuration data model provides immutable, type-safe configuration management for the Jesse Framework MCP knowledge base hierarchical indexing system, controlling all aspects of file processing, LLM integration, and special handling requirements. The module defines comprehensive configuration parameters through the `IndexingConfig` frozen dataclass with validation at initialization, supporting three distinct indexing modes (`FULL`, `INCREMENTAL`, `SELECTIVE`) via the `IndexingMode` enum. Key semantic entities include `IndexingConfig` frozen dataclass for immutable configuration, `IndexingMode` string-based enum for processing strategies, `Claude4SonnetModel.CLAUDE_4_SONNET` LLM model integration, `get_project_root()` function for automatic knowledge directory detection, `should_process_file()` and `should_process_directory()` filtering methods, `to_dict()` and `from_dict()` serialization methods, `load_for_handler()` class method for configuration manager integration, `__post_init__()` validation method, `dataclasses.dataclass` with `frozen=True` for immutability, `pathlib.Path` for file system operations, and comprehensive parameter validation with descriptive error messages. The system enables zero-configuration startup by defaulting `knowledge_output_directory` to `{PROJECT_ROOT}/.knowledge/` while supporting full customization through JSON configuration files and configuration manager integration.

##### Main Components

The module contains two primary classes: `IndexingMode` string-based enum defining three processing strategies (`FULL` for complete re-indexing, `INCREMENTAL` for changed files only, `SELECTIVE` for specific paths), and `IndexingConfig` frozen dataclass with 23 configuration parameters organized into categories including file processing configuration (`max_file_size`, `chunk_size`, `chunk_overlap`), batch processing configuration (`batch_size`, `max_concurrent_operations`), content filtering configuration (`excluded_extensions`, `excluded_directories`, `project_base_exclusions`), LLM configuration (`llm_model`, `temperature`, `max_tokens`), change detection configuration (`indexing_mode`, `timestamp_tolerance_seconds`), special handling flags (`enable_git_clone_indexing`, `enable_project_base_indexing`, `respect_gitignore`), performance configuration (`enable_progress_reporting`, `progress_update_interval`), error handling configuration (`max_retries`, `retry_delay_seconds`, `continue_on_file_errors`), knowledge output configuration (`knowledge_output_directory`), and debug configuration (`debug_mode`, `debug_output_directory`, `enable_llm_replay`). Supporting methods include `__post_init__()` for validation, `should_process_file()` and `should_process_directory()` for filtering, `to_dict()` and `from_dict()` for serialization, and `load_for_handler()` for configuration manager integration.

###### Architecture & Design

The architecture implements an immutable configuration pattern using `@dataclass(frozen=True)` to prevent runtime configuration modifications, with comprehensive validation occurring once at initialization through `__post_init__()` for performance optimization. The design separates concerns through distinct configuration categories with clear parameter grouping, while integrating with the existing `strands_agent_driver` Claude 4 Sonnet configuration for LLM consistency. Configuration management follows a hierarchical exclusion system with base exclusions applied universally and handler-specific exclusions (`project_base_exclusions`) applied conditionally. The system implements automatic default resolution for `knowledge_output_directory` using project root detection, falling back gracefully when project root cannot be determined. Serialization support enables configuration persistence and debugging through dictionary conversion with proper handling of complex types like sets and enums.

####### Implementation Approach

The implementation uses frozen dataclass with field factories for mutable default values like sets, ensuring each instance gets independent collections while maintaining immutability after initialization. Parameter validation employs comprehensive bounds checking in `__post_init__()` with descriptive error messages for debugging, including validation of file sizes, batch parameters, concurrency limits, LLM settings, and performance parameters. File and directory filtering uses set-based lookups for performance optimization in `should_process_file()` and `should_process_directory()` methods. Serialization handling converts sets to lists for JSON compatibility while preserving semantics, with enum values converted to string representation for safe serialization. The `from_dict()` class method implements reverse conversion with proper type handling for sets, enums, and Path objects. Configuration loading integrates with `IndexingConfigManager` through `load_for_handler()` class method, supporting auto-generation of missing configurations from centralized defaults.

######## External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.llm.strands_agent_driver.models:Claude4SonnetModel` - LLM model configuration providing `CLAUDE_4_SONNET` constant
- `jesse_framework_mcp.helpers.path_utils:get_project_root` - project root detection for automatic knowledge directory configuration
- `dataclasses` (external library) - dataclass decorator and field factory for immutable configuration structure
- `pathlib.Path` (external library) - cross-platform path operations and validation
- `typing` (external library) - type annotations for `Set`, `Optional`, `Dict`, `Any` type hints
- `enum.Enum` (external library) - enumeration base class for `IndexingMode` string enum

**← Outbound:**
- `../indexing/config_manager.py:IndexingConfigManager` - configuration manager consuming `IndexingConfig` instances for validation and loading
- `../indexing/hierarchical_indexer.py` - hierarchical indexer consuming configuration for processing parameters and filtering rules
- JSON configuration files serialized through `to_dict()` method for user customization and persistence
- Knowledge base processing components consuming file and directory filtering methods

**⚡ System role and ecosystem integration:**
- **System Role**: Core configuration foundation defining all operational parameters for the Jesse Framework knowledge base indexing system, serving as the single source of truth for processing constraints and LLM integration settings
- **Ecosystem Position**: Central infrastructure component that all indexing operations depend on for validated configuration parameters, bridging between user-customizable JSON configurations and runtime processing requirements
- **Integration Pattern**: Used by indexing components during initialization for parameter access, configuration managers for validation and auto-generation, and serialization systems for configuration persistence and debugging workflows

######### Edge Cases & Error Handling

The system handles missing project root detection gracefully in `__post_init__()` by catching exceptions and maintaining `knowledge_output_directory` as `None` for backward compatibility. File access errors in `should_process_file()` are handled through try-catch blocks, returning `False` for inaccessible files to prevent processing failures. Parameter validation provides comprehensive bounds checking with descriptive error messages: `max_file_size` must be positive, `chunk_overlap` must be less than `chunk_size`, `temperature` must be between 0.0 and 1.0, and all count parameters must be non-negative. Configuration loading through `load_for_handler()` raises `ValueError` when project root cannot be determined and no `knowledge_dir` is provided. Serialization edge cases include handling `None` values for optional parameters and proper conversion of complex types like sets and Path objects. The frozen dataclass prevents accidental configuration modification after initialization, with `object.__setattr__()` used only during `__post_init__()` for default value assignment.

########## Internal Implementation Details

The frozen dataclass uses `object.__setattr__()` in `__post_init__()` to modify the immutable `knowledge_output_directory` field when setting the default value to `project_root / '.knowledge/'`. Default factory functions for sets use lambda expressions to ensure each instance gets independent collections: `excluded_extensions` defaults to 11 common file extensions, `excluded_directories` defaults to 7 common directory names. Parameter validation occurs in specific order: file processing parameters first, then batch processing, LLM parameters, and performance parameters, with early failure preventing invalid configuration creation. The `to_dict()` method handles complex type conversion: sets converted to lists, enums converted to string values, Path objects converted to string representation, with `None` values preserved for optional parameters. The `from_dict()` method implements reverse conversion with defensive copying to avoid modifying input dictionaries, proper set reconstruction from lists, enum conversion from string values, and Path object creation from string paths. Configuration manager integration uses dynamic imports to avoid circular dependencies.

########### Code Usage Examples

**Basic configuration creation with validation:**

This example demonstrates creating an IndexingConfig instance with custom parameters and automatic validation. The frozen dataclass ensures immutability while providing comprehensive parameter validation at initialization.

```python
from jesse_framework_mcp.knowledge_bases.models.indexing_config import IndexingConfig, IndexingMode
from pathlib import Path

# Create configuration with custom parameters
config = IndexingConfig(
    max_file_size=1024 * 1024,  # 1MB limit
    batch_size=5,
    indexing_mode=IndexingMode.INCREMENTAL,
    knowledge_output_directory=Path("/custom/knowledge/path"),
    debug_mode=True
)

# Configuration is immutable after creation
print(f"Batch size: {config.batch_size}")
print(f"Knowledge directory: {config.knowledge_output_directory}")
```

**File and directory filtering with configuration rules:**

This pattern shows how to use the configuration's filtering methods for file and directory processing decisions. The methods provide centralized filtering logic based on configuration parameters.

```python
from pathlib import Path

# Use configuration for file filtering decisions
test_file = Path("src/main.py")
test_dir = Path("node_modules/")

if config.should_process_file(test_file):
    print(f"Processing file: {test_file}")

if config.should_process_directory(test_dir):
    print(f"Processing directory: {test_dir}")
else:
    print(f"Skipping excluded directory: {test_dir}")
```

**Configuration serialization and loading from handler type:**

This example demonstrates configuration serialization for persistence and loading configurations for specific handler types. The serialization maintains all configuration state while the class method provides convenient handler-specific loading.

```python
# Serialize configuration to dictionary for persistence
config_dict = config.to_dict()
print(f"Serialized config keys: {list(config_dict.keys())}")

# Load configuration for specific handler type
project_config = IndexingConfig.load_for_handler("project-base")
git_config = IndexingConfig.load_for_handler("git-clones")

# Create configuration from dictionary (e.g., from JSON file)
restored_config = IndexingConfig.from_dict(config_dict)
```
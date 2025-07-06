<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/models/indexing_config.py -->
<!-- Cached On: 2025-07-06T11:36:40.757438 -->
<!-- Source Modified: 2025-07-06T10:59:57.750775 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file provides the comprehensive configuration data model for the Jesse Framework MCP's Knowledge Bases Hierarchical Indexing System, enabling type-safe parameter management for indexing operations, LLM integration, and specialized handler support. The system delivers immutable configuration with validation at initialization through the `IndexingConfig` frozen dataclass, hierarchical configuration groups (`FileProcessingConfig`, `ContentFilteringConfig`, `LLMConfig`, `ChangeDetectionConfig`, `ErrorHandlingConfig`, `OutputConfig`, `DebugConfig`), and integration with `Claude4SonnetModel` from `strands_agent_driver`. Key semantic entities include `IndexingMode` enum with values `FULL`, `FULL_KB_REBUILD`, and `INCREMENTAL`, configuration serialization via `to_dict()` and `from_dict()` methods, filtering logic through `should_process_file()` and `should_process_directory()` methods, automatic knowledge directory defaulting to `{PROJECT_ROOT}/.knowledge/` via `get_project_root()` integration, and convenience factory method `load_for_handler()` supporting three handler types: `project-base`, `git-clones`, and `pdf-knowledge` with comprehensive parameter coverage including file processing limits, content filtering rules, LLM parameters, change detection settings, error handling configuration, output management, and debug capabilities.

##### Main Components

The file contains the `IndexingMode` enum defining three processing strategies, seven specialized configuration dataclasses (`FileProcessingConfig`, `ContentFilteringConfig`, `LLMConfig`, `ChangeDetectionConfig`, `ErrorHandlingConfig`, `OutputConfig`, `DebugConfig`) for hierarchical organization, and the primary `IndexingConfig` frozen dataclass serving as the comprehensive configuration container. Core methods include `__post_init__()` for validation and default setting, `should_process_file()` and `should_process_directory()` for filtering logic, `to_dict()` and `from_dict()` for serialization support, and the class method `load_for_handler()` for configuration manager integration. The configuration system provides backward compatibility through property accessors for all configuration parameters while maintaining the new hierarchical structure.

###### Architecture & Design

The architecture implements a hierarchical frozen dataclass pattern with focused configuration groups for logical organization and maintainability. The design uses immutable configuration ensuring thread safety and preventing runtime modifications, comprehensive validation at initialization time through `__post_init__()`, and clear separation of concerns across seven configuration domains. The system employs composition patterns with specialized configuration classes handling their specific domains, property-based backward compatibility access preserving existing API contracts, and integration patterns with external systems through serialization methods. The architecture includes defensive parameter validation preventing runtime errors, automatic default setting for knowledge output directory following JESSE Framework conventions, and type-safe configuration creation from external data sources.

####### Implementation Approach

The implementation uses frozen dataclasses with `field(default_factory=...)` for complex default values, comprehensive parameter validation in `__post_init__()` with descriptive error messages, and hierarchical configuration group instantiation for logical organization. Configuration serialization employs dictionary conversion with proper handling of complex types like sets and enums, while deserialization processes hierarchical data into appropriate dataclass instances with type conversion. The filtering system implements performance-optimized checks using set membership for excluded extensions and directories, file size validation through `Path.stat()` with error handling, and hierarchical exclusion support for project-base specific filtering. The system uses `object.__setattr__()` for modifying frozen dataclass fields during initialization and integrates with project root detection for automatic knowledge directory configuration.

######## External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.llm.strands_agent_driver.models:Claude4SonnetModel` - official Claude 4 Sonnet model ID for LLM configuration
- `jesse_framework_mcp.helpers.path_utils:get_project_root` - project root detection for automatic knowledge directory defaulting
- `dataclasses` (external library) - frozen dataclass implementation for immutable configuration
- `pathlib.Path` (external library) - path validation and manipulation for file system operations
- `typing` (external library) - type annotations and validation for configuration parameters
- `enum.Enum` (external library) - enumeration support for `IndexingMode` values

**← Outbound:**
- `knowledge_bases/indexing/hierarchical_indexer.py:HierarchicalIndexer` - consumes configuration for orchestration behavior
- `knowledge_bases/indexing/change_detector.py:ChangeDetector` - uses configuration for timestamp tolerance and processing mode
- `knowledge_bases/indexing/knowledge_builder.py:KnowledgeBuilder` - consumes LLM configuration and processing parameters
- `knowledge_bases/indexing/config_manager.py:IndexingConfigManager` - uses `from_dict()` and `to_dict()` for configuration persistence
- `*.indexing-config.json` - serialized configuration files generated from this model

**⚡ System role and ecosystem integration:**
- **System Role**: Central configuration foundation for the Jesse Framework MCP knowledge base indexing system, serving as the authoritative parameter source for all indexing operations and LLM integration
- **Ecosystem Position**: Core infrastructure component that enables type-safe configuration management across the entire indexing architecture, essential for consistent behavior and validation
- **Integration Pattern**: Used by all indexing components through dependency injection, consumed by configuration managers for persistence, and integrated with external systems through serialization interfaces

######### Edge Cases & Error Handling

The system handles comprehensive validation scenarios including negative or zero values for file sizes, batch parameters, and concurrency limits with descriptive `ValueError` exceptions. Temperature validation ensures LLM parameters remain within valid 0.0-1.0 range, while retry configuration validates non-negative values for resilient operation. File processing edge cases include handling `OSError` and `FileNotFoundError` during file size checks, returning `False` for inaccessible files to prevent processing failures. Configuration serialization handles `None` values for optional paths, converts sets to lists for JSON compatibility, and processes enum values to string representation. The `from_dict()` method provides robust handling of missing configuration sections with sensible defaults, proper type conversion for complex parameters, and validation through standard dataclass initialization ensuring configuration consistency.

########## Internal Implementation Details

The configuration system uses `object.__setattr__()` to modify the frozen `output_config` field during `__post_init__()` when setting the default knowledge directory. Property accessors provide backward compatibility by delegating to hierarchical configuration group attributes while maintaining the new structure. Serialization employs comprehensive dictionary conversion with proper handling of `Path` objects through `str()` conversion and set-to-list conversion for JSON compatibility. The `from_dict()` method processes hierarchical configuration data by extracting nested dictionaries, creating appropriate dataclass instances, and handling optional parameters with proper `None` value processing. File filtering uses `Path.suffix.lower()` for case-insensitive extension comparison and `Path.stat().st_size` for file size validation with exception handling. Directory filtering implements hierarchical exclusion checking by first validating against base exclusions then checking project-base specific exclusions when available.

########### Code Usage Examples

This example demonstrates basic configuration creation with validation and automatic knowledge directory setting:

```python
# Basic configuration instantiation with automatic validation and default knowledge directory
config = IndexingConfig(
    handler_type="project-base",
    file_processing=FileProcessingConfig(max_file_size=5*1024*1024, batch_size=10),
    llm_config=LLMConfig(temperature=0.2, max_tokens=15000)
)
# Automatically sets knowledge_output_directory to {PROJECT_ROOT}/.knowledge/
print(f"Knowledge directory: {config.knowledge_output_directory}")
```

This example shows configuration serialization and deserialization for persistence:

```python
# Configuration serialization for JSON persistence and external system integration
config_dict = config.to_dict()
# Save to JSON file or send to external system

# Configuration deserialization from hierarchical dictionary data
loaded_config = IndexingConfig.from_dict(config_dict)
# Maintains all validation and type safety
```

This example demonstrates file and directory filtering using configuration rules:

```python
# File and directory filtering using configuration-driven exclusion rules
should_process_py = config.should_process_file(Path("src/module.py"))  # True
should_process_cache = config.should_process_file(Path("file.pyc"))    # False
should_process_src = config.should_process_directory(Path("src/"))     # True
should_process_git = config.should_process_directory(Path(".git/"))    # False
```

This example shows handler-specific configuration loading with auto-generation:

```python
# Handler-specific configuration loading with automatic JSON generation
git_config = IndexingConfig.load_for_handler("git-clones")
pdf_config = IndexingConfig.load_for_handler("pdf-knowledge", Path("/custom/knowledge"))
# Automatically generates missing configuration files from centralized defaults
```
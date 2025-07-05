<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/models/indexing_config.py -->
<!-- Cached On: 2025-07-04T22:06:13.892084 -->
<!-- Source Modified: 2025-07-04T21:59:54.149163 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

Immutable configuration data model for Knowledge Bases Hierarchical Indexing System within Jesse Framework MCP server ecosystem, providing comprehensive parameter control for indexing operations, LLM integration, and file processing constraints. Features include `IndexingConfig` frozen dataclass with validation at initialization, `IndexingMode` enum for processing strategy control, automatic default setting of `knowledge_output_directory` to `{PROJECT_ROOT}/.knowledge/`, and integration with `Claude4SonnetModel` for consistent LLM configuration. Enables developers to configure hierarchical indexing operations through type-safe parameter definitions with sensible defaults, defensive parameter validation preventing runtime errors, and serialization support for persistence and debugging. Key semantic entities include `IndexingConfig`, `IndexingMode`, `Claude4SonnetModel.CLAUDE_4_SONNET`, `get_project_root()`, `__post_init__()`, `should_process_file()`, `should_process_directory()`, `to_dict()`, `knowledge_output_directory`, `max_file_size`, `chunk_size`, `batch_size`, `max_concurrent_operations`, `excluded_extensions`, `excluded_directories`, `temperature`, `max_tokens`, `timestamp_tolerance_seconds`, `enable_git_clone_indexing`, `enable_project_base_indexing`, `debug_mode`, `enable_llm_replay`, and comprehensive validation with descriptive error messages for fail-fast configuration checking.

##### Main Components

Primary `IndexingConfig` frozen dataclass containing comprehensive configuration parameters for file processing, LLM integration, batch processing, content filtering, change detection, special handling, performance tuning, error handling, knowledge file output, and debug configuration. `IndexingMode` string-based enum defining processing strategies including `FULL`, `INCREMENTAL`, and `SELECTIVE` modes for different indexing scenarios. Core validation methods including `__post_init__()` for parameter validation and default setting, `should_process_file()` for file filtering decisions, `should_process_directory()` for directory filtering logic, and `to_dict()` for configuration serialization. Configuration parameter groups including file processing constraints with `max_file_size` and `chunk_size`, batch processing settings with `batch_size` and `max_concurrent_operations`, content filtering with `excluded_extensions` and `excluded_directories` sets, and LLM configuration with Claude 4 Sonnet model integration.

###### Architecture & Design

Frozen dataclass architecture ensuring configuration immutability after initialization with comprehensive validation at creation time preventing runtime configuration errors. Enum-based mode selection architecture providing clear semantics for different processing strategies with string values for serialization compatibility. Default value architecture using factory functions for mutable collections and automatic project root detection for knowledge output directory setting. Validation architecture implementing fail-fast parameter checking with descriptive error messages in `__post_init__()` method. Integration architecture with `strands_agent_driver` Claude 4 Sonnet configuration ensuring consistency across LLM operations. Serialization architecture supporting dictionary conversion with proper handling of complex types like sets and enums for JSON compatibility and configuration persistence.

####### Implementation Approach

Immutable configuration strategy using frozen dataclass with `object.__setattr__()` for default value setting during initialization. Comprehensive parameter validation algorithm checking file sizes, batch parameters, concurrency limits, LLM settings, and performance parameters with specific error messages. Default knowledge directory resolution strategy using `get_project_root()` with graceful fallback when project root detection fails. File and directory filtering strategy using set-based lookups for performance optimization with extension and directory name checking. Configuration serialization strategy converting complex types to JSON-compatible formats with explicit type conversion for sets to lists and enum values to strings. Claude 4 Sonnet integration strategy using official model ID from `strands_agent_driver` for consistency across the system.

######## External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.llm.strands_agent_driver.models:Claude4SonnetModel` - Official Claude 4 Sonnet model ID for LLM configuration consistency
- `jesse_framework_mcp.helpers.path_utils:get_project_root` - Project root detection for automatic knowledge directory default setting
- `dataclasses` (standard library) - Data structure definition with frozen dataclass support
- `pathlib.Path` (standard library) - Path validation and manipulation for file system operations
- `typing` (standard library) - Type annotations and validation for parameter safety
- `enum.Enum` (standard library) - Enumeration support for indexing mode definitions

**← Outbound:**
- `jesse_framework_mcp.knowledge_bases.indexing.hierarchical_indexer:HierarchicalIndexer` - Primary consumer using configuration for indexing operations
- `jesse_framework_mcp.knowledge_bases.indexing.knowledge_builder:KnowledgeBuilder` - LLM integration consumer using configuration parameters
- `jesse_framework_mcp.knowledge_bases.indexing.file_analysis_cache:FileAnalysisCache` - Caching system consumer using configuration for performance settings
- Configuration persistence systems consuming serialized dictionary format for storage and debugging
- Debug and replay systems using configuration parameters for development workflow support

**⚡ System role and ecosystem integration:**
- **System Role**: Central configuration authority for Jesse Framework hierarchical indexing system, defining all operational parameters and constraints for knowledge base generation workflow
- **Ecosystem Position**: Core configuration model serving as the single source of truth for indexing behavior, consumed by all major indexing system components including hierarchical indexer, knowledge builder, and caching systems
- **Integration Pattern**: Instantiated once per indexing operation and passed throughout the system hierarchy, ensuring consistent behavior across file processing, LLM integration, and knowledge generation components

######### Edge Cases & Error Handling

Parameter validation edge cases including negative values for file sizes and batch parameters with specific error messages preventing invalid configuration. File size constraint edge cases with 2MB maximum per file designed for optimal LLM context usage and processing efficiency. Chunk overlap validation ensuring overlap is less than chunk size to prevent invalid content chunking scenarios. Temperature parameter validation ensuring values between 0.0 and 1.0 for proper LLM behavior control. Project root detection failure scenarios with graceful fallback keeping `knowledge_output_directory` as None when automatic detection fails. File and directory accessibility edge cases in filtering methods with exception handling for missing or inaccessible filesystem entries. Serialization edge cases handling None values and complex types with proper conversion to JSON-compatible formats for persistence and debugging support.

########## Internal Implementation Details

Frozen dataclass implementation using `@dataclass(frozen=True)` decorator preventing modification after initialization with `object.__setattr__()` for default value setting during `__post_init__()`. Default factory functions using lambda expressions for mutable collections ensuring each instance gets separate collection objects. Parameter validation implementation using explicit range checking with descriptive ValueError messages for each validation failure. File filtering implementation using suffix-based extension checking and stat-based size validation with exception handling for filesystem errors. Directory filtering implementation using name-based exclusion checking against predefined sets for performance optimization. Serialization implementation using explicit type conversion with list conversion for sets and value extraction for enums ensuring JSON compatibility and proper persistence support.

########### Code Usage Examples

Basic configuration instantiation demonstrates default parameter usage with automatic knowledge directory setting. This pattern enables developers to create indexing configurations with sensible defaults while maintaining flexibility for customization.

```python
# Create basic indexing configuration with defaults
config = IndexingConfig()
# knowledge_output_directory automatically set to {PROJECT_ROOT}/.knowledge/
# Uses Claude 4 Sonnet model with optimized parameters for analysis
```

Custom configuration creation shows parameter override capabilities for specific indexing requirements. This approach enables fine-tuning of processing parameters for different project sizes and performance requirements.

```python
# Create custom configuration for large project indexing
config = IndexingConfig(
    max_file_size=5 * 1024 * 1024,  # 5MB for larger files
    batch_size=10,  # Larger batches for better throughput
    max_concurrent_operations=5,  # Higher concurrency
    indexing_mode=IndexingMode.FULL,  # Complete re-indexing
    debug_mode=True,  # Enable debug output
    knowledge_output_directory=Path("/custom/knowledge/path")
)
```

Configuration validation and usage pattern demonstrates file filtering and serialization capabilities. This pattern shows how to use configuration methods for file processing decisions and persistence requirements.

```python
# Use configuration for file processing decisions and serialization
if config.should_process_file(Path("src/main.py")):
    print("File will be processed")
if config.should_process_directory(Path("src/")):
    print("Directory will be traversed")
config_dict = config.to_dict()  # Serialize for persistence
```
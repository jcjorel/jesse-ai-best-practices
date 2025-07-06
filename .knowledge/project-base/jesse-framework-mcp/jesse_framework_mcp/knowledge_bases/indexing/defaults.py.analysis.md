<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/defaults.py -->
<!-- Cached On: 2025-07-06T11:34:26.708505 -->
<!-- Source Modified: 2025-07-06T10:27:57.901556 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file provides centralized default configurations for the Jesse Framework MCP's Knowledge Bases Hierarchical Indexing System, specifically supporting three handler types: `project-base`, `git-clones`, and `pdf-knowledge`. The module enables automatic JSON configuration file generation when configurations don't exist, featuring the `get_default_config()`, `get_supported_handler_types()`, and `validate_handler_type()` functions. Key semantic entities include `PROJECT_BASE_DEFAULT_CONFIG`, `GIT_CLONES_DEFAULT_CONFIG`, `PDF_KNOWLEDGE_DEFAULT_CONFIG`, `BASE_EXCLUDED_EXTENSIONS`, `BASE_EXCLUDED_DIRECTORIES`, `Claude4SonnetModel`, and the `DEFAULT_CONFIGS` registry. The configuration templates provide production-ready defaults with hierarchical exclusion systems, LLM integration via `Claude4SonnetModel.CLAUDE_4_SONNET`, and comprehensive parameter coverage including `file_processing`, `content_filtering`, `llm_config`, `change_detection`, `error_handling`, `output_config`, and `debug_config` sections.

##### Main Components

The file contains three primary configuration dictionaries (`PROJECT_BASE_DEFAULT_CONFIG`, `GIT_CLONES_DEFAULT_CONFIG`, `PDF_KNOWLEDGE_DEFAULT_CONFIG`), base exclusion sets (`BASE_EXCLUDED_EXTENSIONS`, `BASE_EXCLUDED_DIRECTORIES`), project-specific exclusions (`PROJECT_BASE_EXCLUSIONS`), a configuration registry (`DEFAULT_CONFIGS`), and three utility functions (`get_default_config()`, `get_supported_handler_types()`, `validate_handler_type()`). Each configuration template includes seven hierarchical sections covering handler identification, file processing limits, content filtering rules, LLM configuration, change detection settings, error handling parameters, output configuration, and debug options.

###### Architecture & Design

The architecture implements a template-based configuration system with handler-specific optimization and hierarchical exclusion inheritance. The design separates base exclusions (applied universally) from handler-specific exclusions (applied selectively), enabling configuration reuse while maintaining handler specialization. The configuration registry pattern provides centralized access to all handler types through the `DEFAULT_CONFIGS` dictionary, while deep copying ensures template immutability. The hierarchical structure groups related configuration parameters into logical sections (`file_processing`, `content_filtering`, etc.) for improved maintainability and discoverability.

####### Implementation Approach

The implementation uses dictionary-based configuration templates with type annotations and deep copying for safe template access. Each handler configuration optimizes parameters for specific use cases: `project-base` uses larger batch sizes (7 files) and higher file size limits (2MB), `git-clones` uses conservative settings with smaller batches (5 files) and 1MB limits, while `pdf-knowledge` supports larger documents (10MB) with smaller batches (3 files). The exclusion system combines base exclusions with handler-specific additions, and the `copy.deepcopy()` approach prevents accidental template modification during configuration generation.

######## External Dependencies & Integration Points

**→ Inbound:** [dependencies this file requires]
- `jesse_framework_mcp.llm.strands_agent_driver.models:Claude4SonnetModel` - LLM model configuration for all handler types
- `typing` (external library) - type annotations for configuration templates and function signatures
- `copy` (external library) - deep copying functionality for template immutability

**← Outbound:** [systems that consume this file's configurations]
- `knowledge_bases/indexing/` - indexing handlers consume these default configurations
- `*.json` - generated configuration files based on these templates
- Configuration validation systems that use `validate_handler_type()` and `get_supported_handler_types()`

**⚡ System role and ecosystem integration:**
- **System Role**: Central configuration provider for the Jesse Framework MCP's indexing system, serving as the authoritative source for handler default configurations
- **Ecosystem Position**: Core infrastructure component that enables the indexing system's configuration management and auto-generation capabilities
- **Integration Pattern**: Used by indexing handlers during initialization to generate missing JSON configurations, and by validation systems to ensure handler type compliance

######### Edge Cases & Error Handling

The `get_default_config()` function raises `ValueError` for unsupported handler types with clear error messaging including the list of supported types. The configuration templates include comprehensive error handling parameters: `max_retries` (2-5 depending on handler), `retry_delay_seconds` (0.5-2.0), and `continue_on_file_errors: True` for resilient processing. Edge cases addressed include filesystem timestamp comparison tolerance (2-10 seconds), concurrent operation limits (2-3), and file size constraints (1-10MB) tailored to each handler's processing characteristics.

########## Internal Implementation Details

The module maintains backward compatibility with existing `IndexingConfig` structure through complete parameter coverage in all templates. The `BASE_EXCLUDED_DIRECTORIES` includes system directories (`.git`, `__pycache__`, `node_modules`) and the `scratchpad` directory added for universal exclusion. Configuration templates use nested dictionary structures with consistent key naming patterns, and the `DEFAULT_CONFIGS` registry enables O(1) lookup for handler type validation. The deep copying mechanism in `get_default_config()` prevents template pollution while maintaining reference efficiency for read-only operations.

########### Code Usage Examples

This example demonstrates retrieving and customizing a default configuration for the project-base handler. The deep copy ensures template safety while allowing configuration customization.

```python
from jesse_framework_mcp.knowledge_bases.indexing.defaults import get_default_config

# Get default configuration for project-base handler
config = get_default_config("project-base")
config["file_processing"]["batch_size"] = 10  # Customize batch size
config["llm_config"]["temperature"] = 0.5     # Adjust LLM temperature
```

This example shows handler type validation and supported types discovery for configuration management workflows.

```python
from jesse_framework_mcp.knowledge_bases.indexing.defaults import validate_handler_type, get_supported_handler_types

# Validate handler type before processing
if validate_handler_type("git-clones"):
    config = get_default_config("git-clones")

# Get all supported handler types for UI generation
supported_handlers = get_supported_handler_types()  # Returns ['git-clones', 'pdf-knowledge', 'project-base']
```
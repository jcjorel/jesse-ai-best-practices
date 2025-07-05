<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/defaults.py -->
<!-- Cached On: 2025-07-05T20:35:23.215314 -->
<!-- Source Modified: 2025-07-05T20:02:16.420071 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

The `defaults.py` file serves as the centralized configuration template repository for the Jesse Framework MCP's knowledge base indexing system, providing production-ready default configurations for three specialized indexing handlers: `project-base`, `git-clones`, and `pdf-knowledge`. This module enables zero-configuration startup by auto-generating JSON configuration files when they don't exist, evidenced by the `get_default_config()` function that returns deep copies of handler-specific templates and the `DEFAULT_CONFIGS` registry containing complete `IndexingConfig` parameter coverage. Key semantic entities include configuration dictionaries like `PROJECT_BASE_DEFAULT_CONFIG`, `GIT_CLONES_DEFAULT_CONFIG`, and `PDF_KNOWLEDGE_DEFAULT_CONFIG`, exclusion sets such as `BASE_EXCLUDED_EXTENSIONS` and `PROJECT_BASE_EXCLUSIONS`, and utility functions `validate_handler_type()` and `get_supported_handler_types()` for configuration management. The system implements a hierarchical exclusion strategy combining base exclusions with handler-specific exclusions, integrated with `Claude4SonnetModel.CLAUDE_4_SONNET` for LLM configuration and structured into logical groups like `file_processing`, `content_filtering`, `llm_config`, `change_detection`, `error_handling`, `output_config`, and `debug_config`.

##### Main Components

The file contains three primary configuration templates (`PROJECT_BASE_DEFAULT_CONFIG`, `GIT_CLONES_DEFAULT_CONFIG`, `PDF_KNOWLEDGE_DEFAULT_CONFIG`) with handler-specific optimizations, exclusion rule sets including `BASE_EXCLUDED_EXTENSIONS`, `BASE_EXCLUDED_DIRECTORIES`, and `PROJECT_BASE_EXCLUSIONS` for content filtering, and the `DEFAULT_CONFIGS` registry that maps handler types to their respective configurations. Core utility functions include `get_default_config()` for template retrieval with deep copying, `get_supported_handler_types()` for handler discovery, and `validate_handler_type()` for configuration validation. Each configuration template contains seven hierarchical sections covering file processing limits, content filtering rules, LLM configuration, change detection settings, error handling parameters, output configuration, and debug options.

###### Architecture & Design

The architecture follows a template-based configuration pattern with handler-specific specialization, where each indexing handler receives optimized defaults tailored to its processing characteristics and use cases. The design implements a hierarchical exclusion system that combines universal base exclusions with handler-specific exclusions, enabling shared filtering rules while allowing customization for specialized processing needs. The configuration structure uses a registry pattern through `DEFAULT_CONFIGS` that maps handler type strings to configuration dictionaries, combined with immutable template access through deep copying to prevent accidental modification of default values. Each configuration template follows a consistent hierarchical organization with logical groupings that mirror the `IndexingConfig` structure for seamless integration.

####### Implementation Approach

The implementation uses dictionary-based configuration templates with nested structures that organize parameters into logical groups like `file_processing`, `content_filtering`, and `llm_config` for maintainability and discoverability. Configuration generation employs `copy.deepcopy()` to ensure template immutability while allowing safe customization of returned configurations. The exclusion system uses Python sets for efficient membership testing, converted to lists in configuration templates for JSON serialization compatibility. Handler-specific optimizations include different `max_file_size` limits (2MB for project-base, 1MB for git-clones, 10MB for PDF), varying `batch_size` parameters (7, 5, 3 respectively), and specialized `indexing_mode` settings (`incremental`, `full_kb_rebuild`, `incremental`) tailored to each handler's processing characteristics.

######## External Dependencies & Integration Points

**→ Inbound:** [configuration template dependencies]
- `jesse_framework_mcp.llm.strands_agent_driver.models:Claude4SonnetModel` - LLM model constants for configuration templates
- `copy` (external library) - deep copying for immutable template access
- `typing` (external library) - type annotations for configuration structures

**← Outbound:** [configuration consumers]
- `config_manager.py:IndexingConfigManager` - consumes default configurations for auto-generation
- `*.indexing-config.json` - generated JSON configuration files based on these templates
- `knowledge_bases/indexing/` - indexing handlers consuming validated configurations

**⚡ System role and ecosystem integration:**
- **System Role**: Central configuration template repository that enables zero-configuration startup for the Jesse Framework MCP indexing system by providing production-ready defaults for all supported indexing handlers
- **Ecosystem Position**: Core infrastructure component that bridges between hardcoded Python defaults and user-customizable JSON configurations
- **Integration Pattern**: Used by configuration management during initialization to auto-generate missing JSON files, with templates consumed by indexing handlers through the configuration loading pipeline

######### Edge Cases & Error Handling

The system handles unsupported handler types through `get_default_config()` validation that raises `ValueError` with clear error messages listing supported handler types from the registry. Configuration template integrity is protected through `copy.deepcopy()` usage that prevents accidental modification of default values during configuration generation and customization. The exclusion system handles edge cases through comprehensive base exclusions covering common development artifacts (`.pyc`, `__pycache__`, `.git`, `.DS_Store`) and build outputs (`dist/`, `build/`, `target/`), with handler-specific exclusions like `PROJECT_BASE_EXCLUSIONS` adding specialized filtering for knowledge base outputs and AI assistant workspaces. Missing or invalid configuration parameters are handled through complete parameter coverage in each template, ensuring all `IndexingConfig` fields have appropriate default values.

########## Internal Implementation Details

The configuration templates use specific optimization values tailored to each handler's characteristics: project-base uses `batch_size: 7` and `max_concurrent_operations: 3` for balanced cost/performance, git-clones uses smaller batches (`batch_size: 5`) and conservative concurrency (`max_concurrent_operations: 2`) for read-only processing, while PDF processing uses `batch_size: 3` and higher `max_file_size: 10MB` for document handling. Temperature settings vary by handler with project-base using `0.3` for consistent summarization, git-clones using `0.4` for diverse content, and PDF using `0.2` for document analysis precision. The exclusion system converts Python sets to lists for JSON serialization compatibility while maintaining efficient set-based operations during development. Configuration registry uses string keys matching handler type identifiers for direct lookup and validation operations.

########### Code Usage Examples

This example demonstrates retrieving and customizing a default configuration template for project-base indexing operations. The code shows how to safely obtain a configuration template and modify it without affecting the original defaults.

```python
from jesse_framework_mcp.knowledge_bases.indexing.defaults import get_default_config, validate_handler_type

# Validate handler type before configuration retrieval
if validate_handler_type("project-base"):
    # Get deep copy of default configuration template
    config = get_default_config("project-base")
    
    # Safely customize configuration without affecting defaults
    config["file_processing"]["batch_size"] = 10
    config["debug_config"]["debug_mode"] = True
    print(f"Handler: {config['handler_type']}")
    print(f"Batch size: {config['file_processing']['batch_size']}")
```

This example shows how to discover available handler types and access their configuration templates programmatically. The code demonstrates the registry pattern for dynamic configuration discovery and validation.

```python
from jesse_framework_mcp.knowledge_bases.indexing.defaults import get_supported_handler_types, get_default_config

# Discover all supported handler types
supported_handlers = get_supported_handler_types()
print(f"Supported handlers: {supported_handlers}")

# Access configuration templates for all handlers
for handler_type in supported_handlers:
    config = get_default_config(handler_type)
    print(f"{handler_type}: {config['description']}")
    print(f"  Max file size: {config['file_processing']['max_file_size']}")
    print(f"  Indexing mode: {config['change_detection']['indexing_mode']}")
```
<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/defaults.py -->
<!-- Cached On: 2025-07-05T16:18:30.832793 -->
<!-- Source Modified: 2025-07-05T16:01:50.512265 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This module provides centralized default configuration templates for the Jesse Framework MCP knowledge base indexing system, serving as the foundation for auto-generating JSON configuration files when they don't exist. The module defines production-ready defaults for three distinct indexing handlers: `project-base` for whole codebase indexing, `git-clones` for read-only git repository processing, and `pdf-knowledge` for PDF document extraction. Key semantic entities include `PROJECT_BASE_DEFAULT_CONFIG`, `GIT_CLONES_DEFAULT_CONFIG`, `PDF_KNOWLEDGE_DEFAULT_CONFIG` dictionaries, `BASE_EXCLUDED_EXTENSIONS` and `BASE_EXCLUDED_DIRECTORIES` sets for common exclusions, `PROJECT_BASE_EXCLUSIONS` set for project-specific exclusions, `DEFAULT_CONFIGS` registry mapping handler types to configurations, `get_default_config()` factory function, `get_supported_handler_types()` enumeration function, `validate_handler_type()` validation function, `copy.deepcopy()` for template immutability, and `Claude4SonnetModel.CLAUDE_4_SONNET` LLM model integration. The system enables zero-configuration startup while supporting user customization through JSON file generation and maintains type safety through comprehensive parameter coverage matching `IndexingConfig` structure.

##### Main Components

The module contains three primary configuration dictionaries: `PROJECT_BASE_DEFAULT_CONFIG` with 2MB file size limits, 8000-character chunks, batch size of 7, and comprehensive exclusions including `.knowledge/`, `.coding_assistant/`, and `.clinerules/` directories; `GIT_CLONES_DEFAULT_CONFIG` optimized for git repositories with 1MB file limits, 6000-character chunks, batch size of 5, and no project-base exclusions; and `PDF_KNOWLEDGE_DEFAULT_CONFIG` for document processing with 10MB file limits, 4000-character chunks, batch size of 3, and document-specific optimizations. Supporting components include `BASE_EXCLUDED_EXTENSIONS` set with 15 common file extensions like `.pyc`, `.log`, `.cache`, `BASE_EXCLUDED_DIRECTORIES` set with 16 common directories like `__pycache__/`, `node_modules/`, `.git/`, and `PROJECT_BASE_EXCLUSIONS` set with 3 project-specific directories. Utility functions include `get_default_config()`, `get_supported_handler_types()`, and `validate_handler_type()` for configuration management.

###### Architecture & Design

The architecture implements a template-based configuration system with hierarchical exclusion patterns, separating base exclusions applied to all handlers from handler-specific exclusions. The design uses immutable template access through `copy.deepcopy()` to prevent accidental modification of default configurations, while maintaining a centralized registry pattern through `DEFAULT_CONFIGS` dictionary mapping handler types to their respective configurations. Configuration templates follow a comprehensive parameter coverage strategy, ensuring all `IndexingConfig` parameters are represented with production-ready values. The system implements handler-specific optimization strategies: project-base configurations prioritize comprehensive exclusions and larger batch sizes, git-clones configurations use smaller file limits and conservative processing, and pdf-knowledge configurations accommodate larger documents with specialized processing parameters.

####### Implementation Approach

The implementation uses dictionary-based configuration templates with explicit parameter specification for all indexing configuration options including file processing (max_file_size, chunk_size, chunk_overlap), batch processing (batch_size, max_concurrent_operations), content filtering (excluded_extensions, excluded_directories, project_base_exclusions), LLM configuration (llm_model, temperature, max_tokens), change detection (indexing_mode, timestamp_tolerance_seconds), special handling flags, performance settings, error handling parameters, and debug configuration. Set-based exclusion management uses `BASE_EXCLUDED_EXTENSIONS` and `BASE_EXCLUDED_DIRECTORIES` converted to lists for JSON serialization compatibility. The factory function `get_default_config()` implements deep copying to ensure template immutability and handler type validation against the `DEFAULT_CONFIGS` registry. Configuration values are optimized for each handler type: project-base uses larger chunks and batches for comprehensive processing, git-clones uses smaller limits for diverse content, and pdf-knowledge uses document-specific parameters.

######## External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.llm.strands_agent_driver.models:Claude4SonnetModel` - LLM model configuration for `CLAUDE_4_SONNET` constant
- `copy` (external library) - deep copying functionality for immutable template access
- `typing` (external library) - type annotations for `Dict`, `Any`, `List`, `Set` type hints

**← Outbound:**
- `config_manager.py:IndexingConfigManager` - consumes default configurations for auto-generation of missing JSON files
- `config_manager.py:get_default_config` - factory function called during configuration loading and validation
- JSON configuration files generated in knowledge directories for user customization
- Pydantic validation models consuming configuration templates for type safety

**⚡ System role and ecosystem integration:**
- **System Role**: Core configuration foundation providing centralized default templates for the Jesse Framework knowledge base indexing system, enabling auto-generation of JSON configurations and zero-configuration startup
- **Ecosystem Position**: Central infrastructure component that all indexing handlers depend on for default configuration values, serving as the bridge between hardcoded defaults and user-customizable JSON configurations
- **Integration Pattern**: Used by configuration managers during initialization to auto-generate missing JSON files, with templates consumed by validation systems and indexing components requiring production-ready default parameters

######### Edge Cases & Error Handling

The system handles unsupported handler types through `get_default_config()` validation, raising `ValueError` with descriptive messages listing supported handler types from the `DEFAULT_CONFIGS` registry. Template immutability is enforced through `copy.deepcopy()` to prevent accidental modification of default configurations during multiple access operations. Handler type validation provides boolean checking through `validate_handler_type()` for use in conditional logic and error prevention. Configuration completeness is maintained through comprehensive parameter coverage matching `IndexingConfig` structure requirements, ensuring no missing parameters during JSON generation. The exclusion system handles hierarchical patterns with base exclusions applied to all handlers and handler-specific exclusions added only where appropriate, preventing configuration inconsistencies.

########## Internal Implementation Details

The configuration dictionaries use explicit parameter specification with production-optimized values: `max_file_size` ranges from 1MB for git-clones to 10MB for PDF documents, `chunk_size` varies from 4000 for documents to 8000 for project-base processing, `batch_size` ranges from 3 for documents to 7 for project-base, and `temperature` settings range from 0.2 for document analysis to 0.4 for diverse git content. Exclusion sets use specific patterns: `BASE_EXCLUDED_EXTENSIONS` includes build artifacts and temporary files, `BASE_EXCLUDED_DIRECTORIES` covers common build and cache directories, and `PROJECT_BASE_EXCLUSIONS` targets project-specific directories like `.knowledge/`, `.coding_assistant/`, and `.clinerules/`. The `DEFAULT_CONFIGS` registry uses string keys matching handler type identifiers for direct lookup operations. List conversion from sets ensures JSON serialization compatibility while maintaining set-based operations during template generation.

########### Code Usage Examples

**Basic configuration template retrieval with validation:**

This example demonstrates the standard pattern for retrieving default configurations with automatic validation and deep copying. The function ensures template immutability while providing handler-specific optimized configurations.

```python
from jesse_framework_mcp.knowledge_bases.indexing.defaults import get_default_config

# Retrieve project-base configuration template
project_config = get_default_config("project-base")
print(f"Max file size: {project_config['max_file_size']}")  # 2097152 (2MB)
print(f"Batch size: {project_config['batch_size']}")  # 7

# Retrieve git-clones configuration with different optimizations
git_config = get_default_config("git-clones")
print(f"Max file size: {git_config['max_file_size']}")  # 1048576 (1MB)
print(f"Batch size: {git_config['batch_size']}")  # 5
```

**Handler type validation and enumeration:**

This pattern shows how to validate handler types and enumerate supported configurations for dynamic configuration management. The validation functions provide safe access to configuration templates.

```python
from jesse_framework_mcp.knowledge_bases.indexing.defaults import (
    validate_handler_type, get_supported_handler_types
)

# Validate handler type before configuration access
if validate_handler_type("project-base"):
    config = get_default_config("project-base")

# Enumerate all supported handler types
supported_types = get_supported_handler_types()
print(f"Supported handlers: {supported_types}")  # ['git-clones', 'pdf-knowledge', 'project-base']
```

**Configuration customization with exclusion patterns:**

This example demonstrates accessing and customizing exclusion patterns from default configurations. The hierarchical exclusion system provides base exclusions plus handler-specific additions.

```python
# Access exclusion patterns from default configurations
project_config = get_default_config("project-base")
base_exclusions = set(project_config['excluded_directories'])
project_exclusions = set(project_config['project_base_exclusions'])

# Combine exclusions for comprehensive filtering
all_exclusions = base_exclusions.union(project_exclusions)
print(f"Total excluded directories: {len(all_exclusions)}")

# Git-clones configuration has no project-base exclusions
git_config = get_default_config("git-clones")
print(f"Git exclusions: {git_config.get('project_base_exclusions')}")  # None
```
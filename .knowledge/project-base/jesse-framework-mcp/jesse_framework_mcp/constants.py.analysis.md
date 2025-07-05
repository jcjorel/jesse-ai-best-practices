<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/constants.py -->
<!-- Cached On: 2025-07-05T14:43:29.087331 -->
<!-- Source Modified: 2025-06-29T00:23:42.233779 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements central configuration constants for the Jesse Framework MCP Server, providing a single source of truth for JESSE rule file definitions and HTTP formatting standards while eliminating hardcoded rule filenames across the codebase. The module enables dynamic discovery support for embedded content at runtime and comprehensive validation of rule file configurations against actual embedded resources. Key semantic entities include the core constant `JESSE_RULE_FILES` list containing six framework rule files, HTTP formatting constants `HTTP_BOUNDARY`, `HTTP_BOUNDARY_MARKER`, and `CONTENT_TYPES` dictionary for MCP resource standardization, section type classifications in `SECTION_TYPES` dictionary, criticality mappings `RULE_CRITICALITY_MAP` and `DEFAULT_CRITICALITY` for AI assistant processing, primary functions `get_jesse_rule_files()`, `get_jesse_rule_mapping()`, `discover_jesse_rule_files()`, `validate_jesse_rule_files()`, and `get_rule_files_info()` for rule management, `importlib.resources` import with Python < 3.9 compatibility fallback to `importlib_resources`, and comprehensive type hints using `typing.List`, `typing.Dict`, and `typing.Optional` for better code documentation. The system implements runtime discovery as fallback mechanism with graceful failure handling when embedded content cannot be accessed while maintaining compatibility with existing importlib.resources usage patterns.

##### Main Components

The file contains five primary functions, six constant definitions, and four dictionary configurations providing comprehensive rule file management and HTTP formatting standardization. The `get_jesse_rule_files()` function returns the complete list of JESSE rule files from central configuration with copy protection. The `get_jesse_rule_mapping()` function generates mapping from short rule names to full JESSE rule file names by automatically deriving from the central rule file list. The `discover_jesse_rule_files()` function dynamically discovers JESSE rule files from embedded content at runtime using importlib.resources scanning. The `validate_jesse_rule_files()` function validates configured JESSE rule files against embedded content for configuration consistency. The `get_rule_files_info()` function provides comprehensive information about JESSE rule files configuration for debugging and monitoring. Constant definitions include `JESSE_RULE_FILES` as the central list, `HTTP_BOUNDARY` and `HTTP_BOUNDARY_MARKER` for HTTP-style formatting, and dictionary configurations for `CONTENT_TYPES`, `SECTION_TYPES`, `RULE_CRITICALITY_MAP`, and `DEFAULT_CRITICALITY`.

###### Architecture & Design

The architecture implements a centralized configuration pattern with single source of truth for JESSE rule file definitions, following dynamic discovery support with runtime validation and graceful failure handling mechanisms. The design emphasizes elimination of hardcoded values through central constant management, automatic mapping generation from core rule lists to avoid duplication, and comprehensive HTTP formatting standardization for MCP resource delivery. Key design patterns include the single source of truth pattern centralizing all JESSE rule file definitions in one location, dynamic discovery pattern using importlib.resources for runtime content scanning, validation pattern comparing configured files with discovered embedded files, mapping generation pattern automatically deriving short names from full file names, and graceful degradation pattern handling embedded content access failures without breaking functionality. The system uses defensive programming with optional return types and exception handling, modular function design for specific responsibilities, and comprehensive type hints for better code documentation and IDE support.

####### Implementation Approach

The implementation uses list-based central configuration with `JESSE_RULE_FILES` containing six framework rule files as the authoritative source. Rule mapping generation employs string manipulation with prefix/suffix removal using `file_name[6:-3].lower()` to convert `JESSE_*.md` files to short names. Dynamic discovery utilizes `importlib.resources.files()` with directory iteration and file filtering for `JESSE_*.md` pattern matching. The approach implements validation through sorted list comparison between configured and discovered files, comprehensive error handling with try-catch blocks returning None for graceful failure scenarios, and dictionary-based configuration for HTTP formatting constants including content types, section types, and criticality mappings. Function design follows single responsibility principle with clear separation between configuration access, mapping generation, discovery, validation, and information gathering. Type hints employ `List[str]`, `Dict[str, str]`, `Optional[List[str]]`, and `Dict[str, any]` for comprehensive type safety and documentation.

######## External Dependencies & Integration Points

**→ Inbound:**
- `importlib.resources` (external library) - dynamic rule discovery from embedded content with directory scanning and file filtering
- `importlib_resources` (external library) - Python < 3.9 compatibility fallback for resource access functionality
- `typing` (external library) - type hints including List, Dict, Optional for better code documentation and IDE support
- `jesse_framework_mcp.embedded_content/` - embedded content directory containing JESSE rule files accessed through importlib.resources

**← Outbound:**
- Framework rule resource handlers - consuming `get_jesse_rule_files()` and `get_jesse_rule_mapping()` for rule access and routing
- HTTP formatter modules - using HTTP formatting constants for boundary markers, content types, and section classifications
- Resource validation systems - consuming `validate_jesse_rule_files()` for configuration consistency checking
- MCP server initialization - using rule file constants for resource registration and embedded content validation
- Debugging and monitoring tools - accessing `get_rule_files_info()` for comprehensive configuration diagnostics

**⚡ System role and ecosystem integration:**
- **System Role**: Central configuration hub for Jesse Framework MCP Server ecosystem, providing authoritative source for JESSE rule file definitions and HTTP formatting standards with dynamic discovery and validation capabilities
- **Ecosystem Position**: Core infrastructure component serving as foundation for all rule-based functionality, eliminating hardcoded values and providing consistent configuration access across the entire framework
- **Integration Pattern**: Used by framework components through function imports for rule file access, consumed by HTTP formatters for standardized resource delivery, integrated with embedded content system through importlib.resources for runtime discovery, and coordinated with validation systems for configuration consistency checking

######### Edge Cases & Error Handling

The system handles missing embedded content through graceful failure in `discover_jesse_rule_files()` returning None when importlib.resources access fails. Import compatibility manages Python version differences through try-catch import patterns with `importlib_resources` fallback for Python < 3.9 environments. File discovery handles non-existent embedded content directories through exception catching with None return values preventing system failures. Validation logic manages discovery failures by assuming configuration correctness when embedded content cannot be accessed. Rule mapping handles malformed file names through conditional checks ensuring files start with `JESSE_` and end with `.md` before processing. Configuration access provides copy protection in `get_jesse_rule_files()` preventing external modification of central rule list. Comprehensive error handling uses try-catch blocks with graceful degradation rather than exception propagation for non-critical operations.

########## Internal Implementation Details

The module uses central list definition with `JESSE_RULE_FILES` containing six specific rule files: `JESSE_KNOWLEDGE_MANAGEMENT.md`, `JESSE_HINTS.md`, `JESSE_CODE_COMMENTS.md`, `JESSE_CODE_GENERATION.md`, `JESSE_MARKDOWN.md`, and `JESSE_SCRATCHPAD.md`. HTTP formatting employs specific boundary marker `HTTP_BOUNDARY = "ASYNC-HTTP-SECTION-START-v20250628"` with formatted marker string. Content type mapping includes `text/markdown`, `application/json`, `text/plain`, `application/yaml` with workflow-specific markdown classification. Rule mapping implements string slicing with `file_name[6:-3].lower()` removing `JESSE_` prefix and `.md` suffix for short name generation. Discovery uses `resources.files('jesse_framework_mcp.embedded_content')` with `iterdir()` and conditional filtering for JESSE rule pattern matching. Validation employs sorted list comparison with `configured == discovered` for exact match verification. Information gathering combines all functions into comprehensive dictionary with configured files, discovered files, rule mapping, validation status, and total count for debugging support.

########### Code Usage Examples

Central rule file access demonstrates the primary usage pattern for obtaining JESSE framework rule definitions. This approach provides consistent access to rule files across the entire codebase while maintaining single source of truth.

```python
# Access central JESSE rule file configuration for framework resource handlers
# Provides single source of truth eliminating hardcoded rule filenames across codebase
from jesse_framework_mcp.constants import get_jesse_rule_files, get_jesse_rule_mapping

# Get complete list of JESSE rule files
rule_files = get_jesse_rule_files()
# Returns: ['JESSE_KNOWLEDGE_MANAGEMENT.md', 'JESSE_HINTS.md', ...]

# Get mapping from short names to full file names
rule_mapping = get_jesse_rule_mapping()
# Returns: {'knowledge_management': 'JESSE_KNOWLEDGE_MANAGEMENT.md', ...}
```

HTTP formatting constants showcase the standardization pattern for MCP resource delivery with consistent boundary markers and content types. This pattern ensures uniform HTTP-style formatting across all framework resources.

```python
# Use HTTP formatting constants for standardized MCP resource delivery
# Provides consistent boundary markers and content type definitions
from jesse_framework_mcp.constants import HTTP_BOUNDARY_MARKER, CONTENT_TYPES, DEFAULT_CRITICALITY

# Apply HTTP boundary marker for resource sections
section_header = f"{HTTP_BOUNDARY_MARKER}\nContent-Type: {CONTENT_TYPES['markdown']}"

# Use default criticality for resource classification
criticality = DEFAULT_CRITICALITY['framework-rule']  # Returns 'CRITICAL'

# Validate configuration consistency
from jesse_framework_mcp.constants import validate_jesse_rule_files
is_valid = validate_jesse_rule_files()  # Returns True if configuration matches embedded content
```
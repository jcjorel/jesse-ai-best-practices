<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/resources/framework_rules.py -->
<!-- Cached On: 2025-07-05T14:32:57.269653 -->
<!-- Source Modified: 2025-07-05T12:55:58.587214 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements individual JESSE Framework rule resource handlers for the MCP server, providing granular access to each framework rule through HTTP-formatted resources with CRITICAL criticality classification to ensure strict AI assistant compliance. The module enables MCP clients to access specific JESSE rules through dedicated resource URIs following the `jesse://framework/rule/{rule_name}` pattern, supporting comprehensive framework enforcement and development standards adherence. Key semantic entities include six individual resource handler functions `get_knowledge_management_rule()`, `get_hints_rule()`, `get_code_comments_rule()`, `get_code_generation_rule()`, `get_markdown_rule()`, and `get_scratchpad_rule()` decorated with `@server.resource()`, utility functions `get_available_rule_names()`, `get_rule_description()`, and `get_rule_by_name()` for rule discovery and routing, `load_embedded_content()` from content loaders for accessing build-time embedded rule files, `format_http_section()` from `async_http_formatter` with `XAsyncContentCriticality.CRITICAL` classification, `Context` from `fastmcp` for async progress reporting, `get_jesse_rule_files()` and `get_jesse_rule_mapping()` from constants module, `unwrap_fastmcp_function()` utility for decorated function handling, and `writable=False` parameters ensuring read-only access to framework rules. The system implements resource-first architecture with FastMCP Context integration for progress reporting and maintains HTTP formatting preservation exactly matching existing implementation patterns for consistent AI assistant processing.

##### Main Components

The file contains six primary resource handler functions and three utility functions providing comprehensive JESSE Framework rule access capabilities. The individual resource handlers include `get_knowledge_management_rule()` for knowledge system directives, `get_hints_rule()` for AI assistant enforcement rules, `get_code_comments_rule()` for documentation standards, `get_code_generation_rule()` for development best practices, `get_markdown_rule()` for file management standards, and `get_scratchpad_rule()` for directory management requirements. Supporting utility functions include `get_available_rule_names()` for dynamic rule discovery converting file names to resource-friendly identifiers, `get_rule_description()` for human-readable rule descriptions with centralized mapping, and `get_rule_by_name()` for centralized routing to appropriate resource handlers with FastMCP function unwrapping. The `register_framework_rules_resources()` function provides explicit registration compatibility while leveraging FastMCP decorator auto-registration patterns.

###### Architecture & Design

The architecture implements a resource-oriented design pattern with individual resource handlers for each JESSE Framework rule, following FastMCP server integration patterns with decorator-based resource registration and CRITICAL criticality classification for mandatory AI assistant compliance. The design emphasizes granular access through dedicated resource URIs, HTTP formatting preservation matching existing implementation patterns, and embedded content access from build-time copying for consistent rule delivery. Key design patterns include the individual resource pattern providing dedicated handlers for each framework rule, HTTP formatting preservation pattern maintaining existing format_http_section patterns, CRITICAL criticality pattern ensuring AI assistant enforcement, embedded content access pattern using build-time copied rule files, and function unwrapping pattern for FastMCP compatibility with decorated resource handlers. The system uses composition over inheritance with utility functions for rule discovery and routing, centralized error handling with descriptive error messages, and read-only access control through writable=False parameters for framework rule integrity.

####### Implementation Approach

The implementation uses async function patterns with FastMCP Context integration for progress reporting and structured logging throughout rule loading operations. Embedded content access employs `load_embedded_content()` function for accessing build-time copied JESSE rule files with consistent file naming patterns. HTTP formatting applies `format_http_section()` with CRITICAL criticality classification, portable path resolution using `{CLINE_RULES}` placeholders, and read-only access control through `writable=False` parameters. The approach implements rule name conversion from file names to resource identifiers by removing `JESSE_` prefix and `.md` suffix with lowercase transformation. Centralized routing uses dictionary mapping of rule names to handler functions with FastMCP function unwrapping for decorated resource compatibility. Error handling employs try-catch blocks with specific ValueError exceptions and detailed error context for debugging support. Rule discovery implements dynamic enumeration from constants module with consistent naming pattern recognition for resource URI generation.

######## External Dependencies & Integration Points

**→ Inbound:**
- `fastmcp:Context` - async progress reporting and structured logging for rule loading operations
- `..main:server` - FastMCP server instance for resource registration with decorator patterns
- `..helpers.content_loaders:load_embedded_content` - embedded content access for build-time copied JESSE rule files
- `..helpers.async_http_formatter:format_http_section` - HTTP section formatting with criticality classification and portable paths
- `..helpers.async_http_formatter:XAsyncContentCriticality` - content criticality enumeration for CRITICAL classification
- `..helpers.async_http_formatter:XAsyncHttpPath` - HTTP path handling for portable resource location specification
- `..constants:get_jesse_rule_files` - JESSE rule file enumeration for dynamic discovery
- `..constants:get_jesse_rule_mapping` - rule file mapping for consistent access patterns
- `utils:unwrap_fastmcp_function` - FastMCP function compatibility utility for decorated resource handler unwrapping

**← Outbound:**
- AI assistants - consuming individual JESSE framework rules through `jesse://framework/rule/{rule_name}` URIs with CRITICAL criticality
- MCP clients - accessing granular framework rule content through dedicated resource endpoints
- Development environments - using framework rules for development standards enforcement and compliance checking
- Session initialization systems - consuming framework rules through `get_rule_by_name()` for comprehensive context delivery
- Rule discovery systems - using `get_available_rule_names()` for dynamic rule enumeration and resource listing

**⚡ System role and ecosystem integration:**
- **System Role**: Individual JESSE Framework rule provider within Jesse Framework MCP Server ecosystem, delivering granular access to framework rules with CRITICAL criticality for AI assistant enforcement and development standards compliance
- **Ecosystem Position**: Core framework component serving as authoritative source for JESSE development rules, integrating with session initialization and providing foundation for AI assistant behavior enforcement
- **Integration Pattern**: Used by AI assistants through individual resource URI requests with CRITICAL criticality enforcement, consumed by session initialization for comprehensive rule delivery, and integrated with embedded content system for build-time rule access with read-only integrity protection

######### Edge Cases & Error Handling

The system handles missing embedded rule content through try-catch blocks with specific ValueError exceptions and detailed error context when rule files cannot be loaded from build-time embedded content. Unknown rule names in `get_rule_by_name()` trigger ValueError exceptions with descriptive error messages for invalid rule requests. FastMCP function unwrapping handles decorated resource handler compatibility through `unwrap_fastmcp_function()` utility managing parameter extraction for proper function invocation. Content loading failures are managed through exception propagation with Context logging for debugging support and error tracking. Rule name conversion handles edge cases in file name processing with consistent pattern matching for `JESSE_` prefix and `.md` suffix removal. Progress reporting uses FastMCP Context with structured logging for rule loading operations and error conditions. HTTP formatting failures are handled through exception propagation maintaining error context for debugging and troubleshooting support.

########## Internal Implementation Details

The module uses embedded content access through `load_embedded_content()` function for accessing build-time copied JESSE rule files including `JESSE_KNOWLEDGE_MANAGEMENT.md`, `JESSE_HINTS.md`, `JESSE_CODE_COMMENTS.md`, `JESSE_CODE_GENERATION.md`, `JESSE_MARKDOWN.md`, and `JESSE_SCRATCHPAD.md`. HTTP formatting employs `format_http_section()` with specific parameters including `content_type="text/markdown"`, `criticality=XAsyncContentCriticality.CRITICAL`, portable location paths using `{CLINE_RULES}` placeholders, and `writable=False` for read-only access control. Rule name conversion implements string processing with `rule_file[6:-3].lower()` for removing `JESSE_` prefix and `.md` suffix with lowercase transformation. Centralized routing uses dictionary mapping with handler function references and FastMCP function unwrapping through `unwrap_fastmcp_function()` for decorated resource compatibility. Error handling implements specific exception types with detailed error messages including rule names and operation context. Resource registration uses FastMCP decorator auto-registration with `@server.resource()` patterns and explicit registration compatibility through `register_framework_rules_resources()` function.

########### Code Usage Examples

Individual rule access demonstrates the primary consumption pattern for specific JESSE Framework rules with CRITICAL criticality enforcement. This approach provides granular access to framework rules for AI assistant processing and development standards compliance.

```python
# Access specific JESSE Framework rule through dedicated resource URI
# Returns HTTP-formatted rule content with CRITICAL criticality for AI assistant enforcement
rule_content = await mcp_client.read_resource("jesse://framework/rule/knowledge_management")
# Content includes comprehensive knowledge management directives with mandatory compliance
```

Rule discovery and routing showcases the utility function pattern for dynamic rule access and enumeration. This pattern enables systematic rule loading and centralized routing for session initialization and comprehensive rule delivery.

```python
# Discover available JESSE rules and access through centralized routing
# Provides dynamic rule enumeration and consistent access patterns
available_rules = await get_available_rule_names()
# Returns list of rule names: ['knowledge_management', 'hints', 'code_comments', ...]

# Access rule through centralized routing with FastMCP compatibility
rule_content = await get_rule_by_name('code_generation', ctx)
# Returns HTTP-formatted rule content with proper function unwrapping and error handling
```
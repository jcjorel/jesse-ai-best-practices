<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/helpers/async_http_formatter.py -->
<!-- Cached On: 2025-07-05T14:05:16.149596 -->
<!-- Source Modified: 2025-07-05T12:19:32.321876 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements universal HTTP-style formatting infrastructure for all Jesse Framework MCP resources, providing standardized formatting with criticality awareness, portable path resolution, and consistent boundary markers for parseable multi-part content delivery with comprehensive error handling and status code management. The module enables consistent HTTP/1.1-like protocol structure across all MCP resource types while supporting cross-platform portable path variable resolution for environment independence. Key semantic entities include `XAsyncHttpStatus` class for HTTP status code constants and utilities, `XAsyncHttpErrorHandler` class for standard error content generation and exception mapping, `XAsyncContentCriticality` class for AI assistant processing priority classification, `XAsyncHttpPath` class for dual-path storage maintaining portable variables and resolved filesystem paths, `format_http_section()` function for universal content formatting with HTTP headers, `format_http_response()` function for simple HTTP response creation, `format_multi_section_response()` function for combining multiple sections with protocol definition, `_detect_status_and_content()` internal function for automatic error detection, `X-ASYNC-HTTP/1.1` protocol implementation, portable path variables `{PROJECT_ROOT}`, `{HOME}`, `{CLINE_RULES}`, `{CLINE_WORKFLOWS}`, HTTP status codes including custom `240` Context Dependent Content and `241` Context Dependent Content requiring IMMEDIATE attention, `ASYNC-HTTP-SECTION-START` boundary markers, RFC 7231 timestamp formatting, and `resolve_portable_path()` integration for cross-platform compatibility. The system implements single responsibility for HTTP-style content formatting with byte-perfect content-length calculation for semi-binary support and defensive programming with comprehensive validation.

##### Main Components

The file contains four primary classes and four main functions providing comprehensive HTTP formatting infrastructure. The `XAsyncHttpStatus` class defines HTTP status code constants including custom codes 240 and 241 with `get_default_message()` method for standard message mapping. The `XAsyncHttpErrorHandler` class provides error template generation with `generate_error_content()` and `detect_error_from_exception()` methods for automatic error classification. The `XAsyncContentCriticality` class implements two-level criticality system with `CRITICAL` and `INFORMATIONAL` constants plus `validate()` method for input validation. The `XAsyncHttpPath` class maintains dual-path storage with original portable paths and resolved filesystem paths, supporting file operations through delegation and writable flag management. The `format_http_section()` function serves as the universal formatter for all MCP resource content with automatic error detection and HTTP header generation. The `format_http_response()` function creates simple HTTP responses for API integration. The `format_multi_section_response()` function combines multiple sections with optional preambule and protocol definition. The `_detect_status_and_content()` internal function handles automatic error detection with complete override capabilities.

###### Architecture & Design

The architecture implements single responsibility principle with dedicated focus on HTTP-style content formatting across all MCP resource types, using composition patterns for path handling and template-based error generation. The design follows HTTP/1.1 protocol conventions with Jesse Framework-specific extensions including custom status codes, criticality headers, and portable path variables. Key design patterns include the class constant pattern for status codes and criticality levels, template-based error handling pattern with format string substitution, dual-path composition pattern maintaining both portable and resolved paths, automatic error detection pattern with complete override capability, and boundary marker pattern for multi-part content separation. The system uses defensive programming with comprehensive validation, throw-on-failure error handling without fallbacks, and extensible header system supporting additional custom headers while maintaining consistent structure with Content-Location and Content-Length prioritized for improved parsing.

####### Implementation Approach

The implementation uses class-based organization for related constants and utilities with static methods for stateless operations. HTTP status handling employs dictionary-based message mapping with fallback for unknown codes and automatic error detection through exception type checking. Path handling implements composition over inheritance with `XAsyncHttpPath` containing `pathlib.Path` objects while preserving original portable path strings for headers. Content formatting uses precise UTF-8 byte length calculation for Content-Length accuracy and RFC 7231 timestamp formatting for Last-Modified headers. The approach implements automatic error detection with priority system: manual overrides, auto-detection from exceptions, then default success responses. Multi-section formatting uses XML tag wrapping for preambule content and comprehensive protocol definition documentation. Error handling follows throw-on-failure patterns with descriptive error messages and comprehensive validation for all input parameters.

######## External Dependencies & Integration Points

**→ Inbound:**
- `os` (external library) - environment variable access and system-level operations for cross-platform compatibility
- `datetime` (external library) - RFC 7231 timestamp formatting for Last-Modified headers and UTC timezone handling
- `pathlib.Path` (external library) - cross-platform filesystem operations and path resolution for file handling
- `typing` (external library) - type annotations including Dict, Optional, Union, Any for comprehensive type safety
- `.path_utils:resolve_portable_path` - portable path variable resolution for cross-platform environment independence
- `..constants:HTTP_BOUNDARY_MARKER` - consistent boundary marker constants for multi-part content separation

**← Outbound:**
- Jesse Framework MCP resource implementations - consuming HTTP formatting functions for standardized content delivery
- MCP server response generation - using format_http_response for API tool integration and direct responses
- Resource error handling workflows - consuming error detection and generation capabilities for consistent error responses
- Multi-section content assembly - using format_multi_section_response for complex resource combinations
- Path resolution systems - consuming XAsyncHttpPath for dual-path management and portable variable preservation

**⚡ System role and ecosystem integration:**
- **System Role**: Core HTTP formatting infrastructure for Jesse Framework MCP server, providing universal content formatting with standardized headers, error handling, and multi-part response capabilities for all MCP resource types
- **Ecosystem Position**: Central formatting component serving as the foundation for all MCP resource content delivery, enabling consistent HTTP/1.1-like protocol implementation across the framework
- **Integration Pattern**: Used by all MCP resource implementations for content formatting, consumed by server response generation for API integration, and integrated with error handling workflows for comprehensive exception management and status code mapping

######### Edge Cases & Error Handling

The system handles invalid content types through comprehensive type checking with TypeError exceptions for unsupported content parameter types. Empty content scenarios are managed with ValueError exceptions unless status code overrides are provided for error responses. File access errors are automatically detected and mapped to appropriate HTTP status codes through exception type analysis including FileNotFoundError to 404 and PermissionError to 403. Path resolution failures are handled with OSError exceptions containing descriptive error messages and original path context. Invalid criticality levels trigger ValueError exceptions with clear guidance on valid CRITICAL and INFORMATIONAL values. URL handling distinguishes between `file://`, `http://`, and `https://` protocols with appropriate filesystem operation support or restrictions. Windows absolute path detection handles cross-platform scenarios by recognizing `C:\\` patterns and preserving original path formats. Last-Modified header generation handles missing files and permission errors with specific exception types and detailed error context.

########## Internal Implementation Details

The HTTP status system uses class constants with dictionary-based message lookup and fallback handling for unknown status codes. Error template system employs format string substitution with predefined templates for common error scenarios and flexible parameter substitution. Path handling implements dual storage with `_original_path` for headers and `_resolved_path` for filesystem operations, using composition to delegate Path methods to internal resolved path objects. Content length calculation uses UTF-8 encoding with `len(content_bytes)` for byte-perfect accuracy supporting semi-binary content. Header ordering prioritizes Content-Location and Content-Length first for improved parsing efficiency. RFC 7231 timestamp formatting uses `datetime.fromtimestamp()` with UTC timezone and `strftime()` for HTTP-compatible format. Multi-section response assembly uses list-based content building with double newline separation and XML tag wrapping for preambule content. Protocol definition includes comprehensive documentation of X-ASYNC-HTTP/1.1 format structure, headers, status codes, and parsing guidelines.

########### Code Usage Examples

Basic HTTP section formatting demonstrates the universal content formatting pattern for MCP resources. This approach provides standardized HTTP headers with automatic error detection and portable path preservation for cross-platform compatibility.

```python
# Format content with standardized HTTP headers and automatic error detection
from jesse_framework_mcp.helpers.async_http_formatter import format_http_section, XAsyncContentCriticality

formatted_section = format_http_section(
    content="# Workflow Content\nThis is a critical workflow.",
    content_type="text/markdown",
    criticality=XAsyncContentCriticality.CRITICAL,
    description="Development workflow for feature implementation",
    section_type="workflow",
    location="file://{PROJECT_ROOT}/.clinerules/workflows/feature-development.md"
)
```

Multi-section response assembly showcases the pattern for combining multiple HTTP-formatted sections with protocol definition. This pattern enables complex resource responses with optional contextual preambule and comprehensive protocol documentation for parsing guidance.

```python
# Combine multiple HTTP sections with optional preambule and protocol definition
from jesse_framework_mcp.helpers.async_http_formatter import format_multi_section_response

multi_response = format_multi_section_response(
    section1,  # Pre-formatted HTTP section
    section2,  # Pre-formatted HTTP section
    preambule="This response contains critical workflow information for immediate implementation."
)

# Extract sections for processing
http_sections, preambule_content = extract_http_sections_from_multi_response(multi_response)
```
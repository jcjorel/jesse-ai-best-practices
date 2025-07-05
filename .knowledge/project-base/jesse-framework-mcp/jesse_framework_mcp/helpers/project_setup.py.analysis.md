<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/helpers/project_setup.py -->
<!-- Cached On: 2025-07-05T14:01:37.767193 -->
<!-- Source Modified: 2025-07-05T12:56:17.535216 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements project setup guidance utilities for the Jesse Framework MCP server, providing standardized HTTP-formatted guidance for missing project setup scenarios with clear, actionable instructions for users to resolve configuration issues. The module enables consistent error response delivery across all Jesse Framework MCP resources when project root detection fails, ensuring users receive comprehensive setup guidance without circular import dependencies. Key semantic entities include `get_project_setup_guidance()` function for standardized guidance generation, `format_http_section()` for HTTP response formatting, `XAsyncContentCriticality.CRITICAL` for visibility prioritization, `JESSE_PROJECT_ROOT` environment variable configuration, `.git` directory detection patterns, `.knowledge/` directory structure references, `work-in-progress/` subdirectory management, setup location identifier `setup://project-root-missing`, additional HTTP headers including `Setup-Required`, `Setup-Methods`, and `Documentation`, and comprehensive setup instructions covering both Git repository and environment variable approaches. The system implements single responsibility design for project setup error responses with no dependencies on other project modules to avoid circular imports.

##### Main Components

The file contains a single primary function `get_project_setup_guidance()` that generates comprehensive HTTP-formatted setup guidance for missing project root scenarios. The function returns structured markdown content explaining the current status, solution options, enabled features, and next steps for proper Jesse Framework configuration. The guidance content includes detailed setup instructions for both Git repository approach and environment variable configuration, comprehensive feature descriptions for properly configured systems, and clear next steps for users to resolve setup issues. The implementation uses `format_http_section()` with `XAsyncContentCriticality.CRITICAL` to ensure visibility in AI assistant processing and includes additional HTTP headers for setup metadata and documentation references.

###### Architecture & Design

The architecture implements single responsibility principle with dedicated focus on project setup guidance generation, avoiding circular import dependencies through independent operation without project root detection. The design follows HTTP-formatted response patterns for consistent MCP resource integration using `format_http_section()` utility with structured content organization. Key design patterns include the utility function pattern for reusable guidance generation, HTTP response formatting pattern for consistent MCP integration, critical content prioritization pattern using `XAsyncContentCriticality.CRITICAL`, and comprehensive instruction pattern covering multiple setup approaches. The system uses structured markdown content with clear sections, actionable instructions, and feature descriptions to guide users through setup resolution.

####### Implementation Approach

The implementation uses static content generation with embedded markdown providing comprehensive setup instructions and feature descriptions. The approach employs `format_http_section()` utility with specific parameters including content type `text/markdown`, critical criticality level, descriptive section information, and custom location identifier `setup://project-root-missing`. Content organization follows structured markdown patterns with status indicators, solution options, feature descriptions, and step-by-step instructions. The system includes additional HTTP headers for setup metadata including required status, available methods, and documentation references. Error guidance covers both primary setup methods with detailed command examples for different operating systems and clear explanations of enabled features.

######## External Dependencies & Integration Points

**→ Inbound:**
- `..helpers.async_http_formatter:format_http_section` - HTTP section formatting utility for consistent MCP response patterns
- `..helpers.async_http_formatter:XAsyncContentCriticality` - content criticality enumeration for visibility prioritization
- `typing` (external library) - type hints for function return value documentation

**← Outbound:**
- Jesse Framework MCP resource endpoints - consuming setup guidance for missing project root error responses
- MCP server error handling workflows - using guidance function for consistent setup error messaging
- Project initialization workflows - referencing setup guidance for user onboarding and configuration
- Development tools - accessing setup instructions for Jesse Framework configuration

**⚡ System role and ecosystem integration:**
- **System Role**: Dedicated utility component for Jesse Framework MCP server setup guidance, providing consistent error response generation for missing project root scenarios without circular dependencies
- **Ecosystem Position**: Peripheral support component serving MCP resource endpoints and error handling workflows, ensuring consistent user guidance across the framework
- **Integration Pattern**: Used by MCP resource endpoints when project root detection fails, consumed by error handling workflows for consistent messaging, and referenced by development tools for setup instruction delivery

######### Edge Cases & Error Handling

The system handles missing project root scenarios by providing comprehensive guidance covering both Git repository and environment variable setup approaches. The implementation avoids circular import issues by operating independently without project root detection dependencies. Content delivery handles different operating systems by providing platform-specific command examples for environment variable configuration. The guidance addresses both temporary and permanent setup solutions with clear explanations of trade-offs and recommendations. Error scenarios are prevented through static content generation and independent operation without external project dependencies. The system ensures visibility through critical content prioritization preventing setup guidance from being overlooked in AI assistant processing.

########## Internal Implementation Details

The guidance content uses static markdown string with embedded setup instructions, status indicators, and feature descriptions organized in clear sections. HTTP formatting employs `format_http_section()` with specific parameters including `content_type="text/markdown"`, `criticality=XAsyncContentCriticality.CRITICAL`, custom section type and location identifiers. Additional headers include setup metadata with boolean flags, method specifications, and documentation URL references. Content structure follows hierarchical markdown organization with status section, solution options, feature descriptions, and next steps. The implementation maintains independence from other project modules through direct content generation without external project state dependencies.

########### Code Usage Examples

Basic setup guidance generation demonstrates the standard pattern for missing project root error responses. This approach provides consistent HTTP-formatted guidance across all Jesse Framework MCP resources when project setup is incomplete.

```python
# Generate standardized project setup guidance for missing project root scenarios
guidance_response = get_project_setup_guidance()
# Returns HTTP-formatted markdown with comprehensive setup instructions
# Includes both Git repository and environment variable configuration methods
```

Integration with MCP resource error handling showcases the usage pattern for consistent setup guidance delivery. This pattern ensures users receive actionable setup instructions when accessing Jesse Framework resources without proper configuration.

```python
# Integrate setup guidance into MCP resource error handling workflows
def handle_missing_project_root():
    if not project_root_detected():
        return get_project_setup_guidance()
    # Provides consistent error response with actionable setup instructions
    # Ensures critical visibility through XAsyncContentCriticality.CRITICAL
```
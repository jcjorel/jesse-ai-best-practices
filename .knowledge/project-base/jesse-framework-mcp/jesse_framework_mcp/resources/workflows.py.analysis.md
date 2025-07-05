<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/resources/workflows.py -->
<!-- Cached On: 2025-07-05T14:30:12.302291 -->
<!-- Source Modified: 2025-07-05T12:54:52.403188 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements JESSE Framework workflow resource handlers for the MCP server, providing individual JESSE workflow files as HTTP-formatted resources specifically designed for Cline slash command integration within AI-assisted development environments. The module enables MCP clients to access embedded workflow content through standardized resource URIs, transforming each workflow into an accessible Cline slash command for streamlined development operations. Key semantic entities include `get_jesse_workflow()` function decorated with `@server.resource("file://workflows/{workflow_name}")`, `get_embedded_workflow_files()` function for dynamic workflow discovery, `register_workflows_resources()` registration function, utility functions `get_workflow_description()` and `get_workflow_category()` for metadata extraction, `format_http_section()` from `async_http_formatter` module with `XAsyncContentCriticality.CRITICAL` classification, `Context` from `fastmcp` for async progress reporting, `importlib.resources` for embedded content access, workflow categories including `Task Management`, `Knowledge Management`, `Knowledge Capture`, `Amazon Integration`, and `Framework Management`, specific workflow files like `jesse_wip_task_create.md`, `jesse_wip_task_switch.md`, `jesse_capture_our_chat.md`, and `jesse_amazon_pr_faq_coach.md`, and HTTP headers including `Cline-Slash-Command`, `Workflow-Category`, and `Workflow-File` for enhanced Cline integration. The system implements HTTP-formatted resource delivery with `writable=False` parameters ensuring read-only workflow access while maintaining CRITICAL criticality classification for strict AI assistant adherence.

##### Main Components

The file contains four primary functions providing comprehensive workflow resource management and discovery capabilities. The `get_jesse_workflow()` function serves individual workflow resources through FastMCP decorator registration, handling workflow loading from embedded content with HTTP formatting and Cline-specific metadata. The `get_embedded_workflow_files()` function provides dynamic workflow discovery by scanning the embedded workflows directory and returning markdown file listings for resource enumeration. The `register_workflows_resources()` function coordinates resource registration with the FastMCP server instance. Supporting utility functions include `get_workflow_description()` for human-readable workflow descriptions using dictionary mapping with pattern matching fallbacks, and `get_workflow_category()` for workflow classification using prefix-based categorization aligned with JESSE framework functional areas.

###### Architecture & Design

The architecture implements a resource-oriented design pattern with clear separation between workflow discovery, content delivery, and metadata management, following FastMCP server integration patterns with decorator-based resource registration. The design emphasizes HTTP-formatted content delivery through `format_http_section()` with consistent CRITICAL criticality classification and read-only access flags for workflow integrity. Key design patterns include the resource handler pattern with FastMCP decorators for endpoint registration, embedded content access pattern using `importlib.resources` for package-bundled workflows, metadata mapping pattern with dictionary-based descriptions and prefix-based categorization, content formatting pattern with HTTP section wrapping for Cline integration, and graceful error handling pattern with descriptive error messages and proper exception propagation. The system uses composition over inheritance with utility functions for specific workflow operations, centralized metadata management through mapping dictionaries, and standardized HTTP formatting for consistent Cline slash command integration.

####### Implementation Approach

The implementation uses async function patterns with FastMCP Context integration for progress reporting and structured logging throughout workflow processing operations. Workflow discovery employs `importlib.resources` for embedded content access with directory iteration and file extension filtering for markdown workflow identification. Content delivery combines embedded file loading with HTTP formatting using `format_http_section()` with CRITICAL criticality and workflow-specific metadata headers. The approach implements filename normalization with extension handling for both `.md` and extensionless workflow names, metadata extraction through dictionary mapping with pattern-based fallbacks for unknown workflows, and error handling with try-catch blocks and descriptive error messages. Data structures use dictionaries for workflow descriptions and categories with prefix-based pattern matching, while content loading employs UTF-8 text reading with whitespace validation and empty content detection.

######## External Dependencies & Integration Points

**→ Inbound:**
- `importlib.resources` (external library) - embedded content access for workflow file loading from package-bundled content
- `importlib_resources` (external library) - Python < 3.9 compatibility fallback for resource access functionality
- `fastmcp:Context` - async progress reporting and structured logging for workflow processing operations
- `..helpers.async_http_formatter:format_http_section` - HTTP section formatting with content type and criticality classification
- `..helpers.async_http_formatter:XAsyncContentCriticality` - content criticality enumeration for CRITICAL classification
- `..helpers.async_http_formatter:XAsyncHttpPath` - HTTP path handling for resource location specification
- `..main:server` - FastMCP server instance for resource registration with decorator patterns
- `jesse_framework_mcp.embedded_content.workflows/` - embedded workflow directory containing markdown workflow files

**← Outbound:**
- Cline AI assistant - consuming workflow resources as slash commands through `file://workflows/{workflow_name}` URIs
- MCP clients - accessing individual workflow content through standardized resource protocol
- Development environments - using HTTP-formatted workflow content with CRITICAL criticality for strict adherence
- AI coding assistants - consuming workflow metadata through Cline-Slash-Command headers for command integration
- Workflow management systems - using workflow categorization and description metadata for organization

**⚡ System role and ecosystem integration:**
- **System Role**: Workflow resource provider within Jesse Framework MCP Server ecosystem, delivering embedded workflow content as HTTP-formatted resources with CRITICAL criticality for AI assistant integration and Cline slash command functionality
- **Ecosystem Position**: Core resource component serving AI-assisted development workflows with embedded content delivery, integrating with Cline through standardized MCP resource protocol and slash command headers
- **Integration Pattern**: Used by Cline AI assistant through resource URI requests with slash command integration, consumed by MCP clients for workflow access, and coordinated with HTTP formatter helpers for consistent content delivery with read-only access control

######### Edge Cases & Error Handling

The system handles missing embedded workflow files through try-catch blocks with descriptive error messages and proper exception propagation when workflows cannot be accessed from package content. Filename normalization manages both `.md` and extensionless workflow names through conditional extension handling and clean name extraction for slash command compatibility. Empty workflow content is detected through `.strip()` validation with specific error messages for whitespace-only files. Resource discovery handles missing embedded content directories through exception catching with detailed error context. Workflow metadata extraction provides fallback descriptions and categories through pattern matching when exact dictionary matches unavailable. Import compatibility manages Python version differences through try-catch import patterns with `importlib_resources` fallback for older Python versions. Progress reporting uses FastMCP Context with structured logging for debugging workflow processing issues and resource loading failures.

########## Internal Implementation Details

The module uses embedded content access through `importlib.resources.files()` with directory iteration and suffix filtering for `.md` file identification in workflow discovery. Workflow loading employs `resources.open_text()` with UTF-8 encoding and content validation through `.strip()` for empty file detection. Filename processing implements conditional extension handling with `.endswith('.md')` checks and clean name extraction through `.replace('.md', '')` for slash command compatibility. Metadata mapping uses dictionary lookups with exact matching followed by prefix-based pattern matching for workflow descriptions and categories. HTTP formatting includes specific additional headers like `Cline-Slash-Command`, `Workflow-Category`, and `Workflow-File` for enhanced Cline integration metadata. Error handling implements specific exception types with detailed error messages including workflow file names and operation context. Content delivery uses `writable=False` parameter for read-only access control while maintaining CRITICAL criticality classification for strict AI assistant adherence to workflow instructions.

########### Code Usage Examples

Basic workflow resource access demonstrates the primary consumption pattern for Cline slash command integration. This approach provides HTTP-formatted workflow content with CRITICAL criticality for strict AI assistant adherence.

```python
# Access JESSE workflow through MCP resource URI for Cline slash command integration
# Returns HTTP-formatted workflow content with CRITICAL criticality and Cline metadata
workflow_content = await mcp_client.read_resource("file://workflows/jesse_wip_task_create")
# Content includes Cline-Slash-Command header for /jesse_wip_task_create integration
```

Workflow discovery showcases the embedded content enumeration pattern for dynamic resource listing. This pattern enables MCP clients to discover available workflows without hardcoded file lists.

```python
# Discover available workflow files from embedded content for resource enumeration
# Scans embedded workflows directory and returns markdown file listings
workflow_files = await get_embedded_workflow_files()
# Returns list of .md workflow files for MCP resource discovery and Cline integration
```
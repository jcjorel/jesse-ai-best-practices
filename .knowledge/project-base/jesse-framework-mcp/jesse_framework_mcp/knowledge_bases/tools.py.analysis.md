<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/tools.py -->
<!-- Cached On: 2025-07-05T20:39:52.063209 -->
<!-- Source Modified: 2025-07-05T20:01:39.759968 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

The `tools.py` file serves as the FastMCP tools integration layer for the Jesse Framework MCP's knowledge base hierarchical indexing system, providing standardized MCP tool interfaces for manual indexing operations, system status monitoring, and search capabilities through the FastMCP server framework. This module enables user-initiated knowledge base operations through MCP protocol integration, evidenced by the `register_knowledge_bases_tools()` function that registers three tools with the FastMCP server and the global `_current_indexer` variable for operation coordination. Key semantic entities include `FastMCP` server integration, `@server.tool()` decorators for tool registration, `Context` parameter for progress reporting, `HierarchicalIndexer` for core processing operations, `IndexingConfig` and `IndexingMode` for configuration management, `format_http_response()` for consistent response formatting, tool functions `knowledge_bases_index_trigger()`, `knowledge_bases_status()`, and `knowledge_bases_search()`, and comprehensive error handling with HTTP status codes (400, 404, 409, 500, 501). The system implements async-first architecture supporting concurrent operations with real-time feedback through FastMCP Context integration and HTTP-formatted responses following JESSE Framework patterns.

##### Main Components

The file contains the primary `register_knowledge_bases_tools()` function that serves as the central tool registration point, three MCP tool implementations as nested functions within the registration function, and a global `_current_indexer` variable for operation state management. The `knowledge_bases_index_trigger()` tool provides manual indexing capabilities with configurable parameters including `target_path`, `indexing_mode`, `enable_git_clone_indexing`, and `enable_project_base_indexing`. The `knowledge_bases_status()` tool offers real-time status monitoring and statistics retrieval for ongoing and completed indexing operations. The `knowledge_bases_search()` tool serves as a placeholder for future search functionality with parameters for `query`, `search_scope`, and `max_results`. Each tool implements comprehensive error handling, progress reporting through FastMCP Context, and HTTP-formatted response generation for consistency with JESSE Framework patterns.

###### Architecture & Design

The architecture follows a centralized tool registration pattern where all MCP tools are defined as nested functions within the `register_knowledge_bases_tools()` function, enabling clean encapsulation and shared access to the global indexer state. The design implements async-first patterns throughout with all tool functions declared as async and using await for I/O operations and progress reporting. The system uses a global state management approach through the `_current_indexer` variable to coordinate operations and prevent concurrent indexing conflicts. Each tool follows a consistent three-section documentation pattern as specified in JESSE_CODE_COMMENTS.md, with tool intent, design principles, and implementation details clearly separated. The architecture integrates HTTP response formatting through the `format_http_response()` helper function, ensuring consistent response structures across all tools with appropriate HTTP status codes and content types.

####### Implementation Approach

The implementation uses FastMCP's `@server.tool()` decorator pattern for tool registration with descriptive names and documentation strings that appear in MCP client interfaces. Tool parameter validation employs early validation patterns with immediate HTTP error responses for invalid inputs, including IndexingMode validation and path existence checking. The system implements conflict detection through global state checking, preventing concurrent indexing operations by returning HTTP 409 Conflict responses when operations are already in progress. Progress reporting uses FastMCP Context methods (`ctx.info()`, `ctx.error()`) for real-time user feedback during long-running operations. Response generation follows a consistent pattern using `format_http_response()` with appropriate HTTP status codes, structured data payloads, and JSON content types for successful operations, while error responses include detailed error information and debugging context.

######## External Dependencies & Integration Points

**→ Inbound:** [MCP tools integration dependencies]
- `fastmcp:Context` - progress reporting and user feedback during tool execution
- `fastmcp.server:FastMCP` - MCP server framework for tool registration and execution
- `.indexing:HierarchicalIndexer` - core indexing orchestrator for processing operations
- `.models:IndexingConfig` - configuration data model for indexing parameters
- `.models:IndexingMode` - enumeration for processing mode validation
- `..helpers.async_http_formatter:format_http_response` - HTTP response formatting for consistency
- `pathlib` (external library) - cross-platform path operations for tool parameters
- `asyncio` (external library) - async programming patterns for concurrent operations
- `logging` (external library) - structured logging for tool operation tracking

**← Outbound:** [MCP tools consumers]
- `FastMCP server instances` - consume registered tools through MCP protocol integration
- `MCP clients` - invoke tools through standardized MCP tool interface protocol
- `Jesse Framework MCP server` - integrates tools into broader MCP server functionality
- `User interfaces` - access tools through MCP-compatible clients and applications

**⚡ System role and ecosystem integration:**
- **System Role**: MCP protocol bridge that exposes knowledge base indexing functionality through standardized tool interfaces, enabling user-initiated operations and system monitoring within the Jesse Framework MCP ecosystem
- **Ecosystem Position**: Interface layer component that connects FastMCP server infrastructure with core indexing functionality, serving as the primary user interaction point for knowledge base operations
- **Integration Pattern**: Used by MCP server during initialization through tool registration, consumed by MCP clients through protocol-standard tool invocation, and integrated with core indexing system through HierarchicalIndexer coordination

######### Edge Cases & Error Handling

The system handles invalid indexing mode parameters through `IndexingMode` enum validation, returning HTTP 400 Bad Request responses with detailed error messages listing valid modes. Concurrent operation conflicts are managed through global indexer state checking, preventing multiple simultaneous indexing operations by returning HTTP 409 Conflict responses. File system validation includes path existence checking and directory validation, returning HTTP 404 Not Found for missing paths and HTTP 400 Bad Request for non-directory targets. Exception handling uses comprehensive try-catch blocks with structured logging through the logger instance and detailed error responses including exception details and context information. The search tool handles future functionality through HTTP 501 Not Implemented responses, maintaining interface consistency while indicating planned feature status. Tool execution failures result in HTTP 500 Internal Server Error responses with detailed error information and debugging context for troubleshooting.

########## Internal Implementation Details

The global `_current_indexer` variable uses Optional typing to handle uninitialized states and provides thread-safe access patterns for operation coordination. Tool registration uses FastMCP's decorator pattern with nested function definitions, enabling shared access to the global indexer state while maintaining clean encapsulation. Response data structures follow consistent patterns with status fields, operation metadata, statistics dictionaries, and error arrays limited to 10 entries for response size management. Progress reporting integrates FastMCP Context methods throughout tool execution, providing real-time feedback during long-running indexing operations. HTTP response formatting uses the `format_http_response()` helper with consistent status codes, structured payloads, and appropriate content type headers. Error handling includes comprehensive exception logging with stack traces and structured error responses containing error messages, details, and context information for debugging and user guidance.

########### Code Usage Examples

This example demonstrates the tool registration process and integration with a FastMCP server instance. The code shows how to register all knowledge base tools with proper server configuration and logging setup.

```python
from fastmcp.server import FastMCP
from jesse_framework_mcp.knowledge_bases.tools import register_knowledge_bases_tools

# Initialize FastMCP server and register knowledge base tools
server = FastMCP("Jesse Framework MCP")
register_knowledge_bases_tools(server)

# Tools are now available for MCP client invocation
# - knowledge_bases_index_trigger
# - knowledge_bases_status  
# - knowledge_bases_search
```

This example shows how MCP clients would invoke the indexing trigger tool with various configuration options. The code demonstrates the parameter structure and expected response format for successful indexing operations.

```python
# MCP client tool invocation example (conceptual)
response = await mcp_client.call_tool(
    "knowledge_bases_index_trigger",
    {
        "target_path": "./src/",
        "indexing_mode": "incremental", 
        "enable_git_clone_indexing": True,
        "enable_project_base_indexing": False
    }
)

# Expected response structure
{
    "status": "completed",
    "target_path": "/absolute/path/to/src/",
    "indexing_mode": "incremental",
    "statistics": {...},
    "completion_percentage": 100.0,
    "operation_summary": {
        "total_files_discovered": 150,
        "files_completed": 145,
        "files_failed": 5
    }
}
```
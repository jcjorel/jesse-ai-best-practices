<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/tools.py -->
<!-- Cached On: 2025-07-05T13:56:09.268333 -->
<!-- Source Modified: 2025-07-05T12:56:57.111246 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements FastMCP tools integration for the Jesse Framework MCP Knowledge Bases Hierarchical Indexing System, providing standardized MCP tool interfaces for manual indexing operations, system status monitoring, and search capabilities through async tool execution patterns. The module enables external MCP clients to trigger knowledge base indexing operations, monitor processing status, and access search functionality through well-defined tool interfaces following Jesse Framework patterns. Key semantic entities include `register_knowledge_bases_tools()` function for centralized tool registration, `FastMCP` server integration with `@server.tool()` decorators, tool implementations `knowledge_bases_index_trigger`, `knowledge_bases_status`, and `knowledge_bases_search`, `HierarchicalIndexer` integration for core processing coordination, `IndexingConfig` and `IndexingMode` for configuration management, `Context` for progress reporting and user feedback, `format_http_response()` utility for consistent HTTP formatting, global `_current_indexer` variable for tool coordination, comprehensive error handling with structured HTTP responses, and async-first architecture supporting concurrent operations with real-time progress reporting through FastMCP Context integration.

##### Main Components

The file contains the primary `register_knowledge_bases_tools()` function that registers three core MCP tools with the FastMCP server. The `knowledge_bases_index_trigger` tool enables manual indexing operations with configurable parameters including `target_path`, `indexing_mode`, `enable_git_clone_indexing`, and `enable_project_base_indexing`, providing comprehensive validation, progress reporting, and result statistics. The `knowledge_bases_status` tool delivers real-time monitoring capabilities for ongoing indexing operations, accessing the global `_current_indexer` instance to provide detailed processing statistics and operation status information. The `knowledge_bases_search` tool serves as a placeholder for future search functionality, maintaining tool interface consistency while indicating planned feature availability. Each tool implements comprehensive error handling with structured HTTP responses, detailed logging through `logger.error()`, and progress reporting through `FastMCP Context` integration for real-time user feedback.

###### Architecture & Design

The architecture follows FastMCP tool registration patterns with centralized tool management through a single registration function that decorates async tool handlers with `@server.tool()`. The design implements global state management through `_current_indexer` variable enabling tool coordination and status sharing across multiple tool invocations. Key design patterns include the tool decorator pattern for MCP integration, async-first architecture supporting non-blocking tool execution, comprehensive parameter validation pattern with HTTP error responses, progress reporting pattern through FastMCP Context integration, and structured error handling pattern with detailed HTTP responses and logging. The system uses HTTP response formatting through `format_http_response()` utility maintaining consistency with Jesse Framework patterns and enabling proper MCP client integration with standardized response structures.

####### Implementation Approach

The implementation uses async tool handlers registered through FastMCP decorators with comprehensive parameter validation including `IndexingMode` enum validation, path existence checking, and concurrent operation prevention. Tool execution employs `HierarchicalIndexer` instantiation with `IndexingConfig` based on provided parameters, progress reporting through `FastMCP Context` with `ctx.info()` and `ctx.error()` methods, and detailed result compilation including processing statistics and operation summaries. Status monitoring uses global indexer instance access with real-time status retrieval through `current_status` property and comprehensive statistics serialization. Error handling implements try-catch blocks with structured HTTP error responses including status codes, error messages, and detailed exception information for debugging support. The approach maintains tool interface consistency through standardized parameter patterns and response formatting across all tool implementations.

######## External Dependencies & Integration Points

**→ Inbound:**
- `.indexing:HierarchicalIndexer` - core indexing orchestrator providing hierarchical processing capabilities and status tracking
- `.models:IndexingConfig` - configuration data model providing processing parameters and validation
- `.models:IndexingMode` - enumeration defining indexing strategies for tool parameter validation
- `..helpers.async_http_formatter:format_http_response` - HTTP response formatting utility for consistent Jesse Framework response patterns
- `fastmcp:Context` - MCP context providing progress reporting and user interaction capabilities
- `fastmcp.server:FastMCP` - MCP server framework providing tool registration and management capabilities
- `pathlib` (external library) - cross-platform path operations for tool parameter validation and processing
- `asyncio` (external library) - async programming patterns for non-blocking tool execution
- `logging` (external library) - structured logging for error tracking and debugging support

**← Outbound:**
- MCP clients - consume registered tools through FastMCP protocol for manual indexing operations and status monitoring
- Jesse Framework MCP server - integrates registered tools into overall MCP server tool catalog
- External automation systems - trigger indexing operations through MCP tool interfaces for automated knowledge base maintenance
- Development tools - access indexing capabilities and status monitoring for development workflow integration

**⚡ System role and ecosystem integration:**
- **System Role**: MCP tool provider for the Jesse Framework knowledge base indexing system, exposing manual indexing operations and system monitoring through standardized FastMCP tool interfaces
- **Ecosystem Position**: Peripheral interface component bridging the knowledge base indexing system with external MCP clients and automation systems requiring manual control and monitoring capabilities
- **Integration Pattern**: Registered with FastMCP server during system initialization, consumed by MCP clients through tool invocation requests, and integrated with core HierarchicalIndexer for processing coordination while maintaining global state for tool coordination

######### Edge Cases & Error Handling

The system handles invalid indexing mode parameters through `IndexingMode` enum validation returning HTTP 400 responses with specific error messages listing valid mode options. Concurrent operation prevention uses global indexer state checking with `is_processing` property returning HTTP 409 conflict responses when indexing is already in progress. Path validation implements existence and directory checking with HTTP 404 and 400 responses for missing or invalid target paths. Configuration instantiation failures are managed through comprehensive try-catch blocks with detailed error logging and HTTP 500 responses. Tool execution exceptions are caught and converted to structured HTTP error responses including error details and technical information for debugging support. Status retrieval handles missing indexer instances gracefully with informative HTTP 200 responses indicating no operations have been initiated. Search tool placeholder implementation returns HTTP 501 responses indicating planned feature availability while maintaining tool interface consistency.

########## Internal Implementation Details

The tool registration uses FastMCP decorator pattern with async function definitions enabling non-blocking tool execution and proper MCP protocol integration. Global state management employs `_current_indexer` variable with Optional typing for tool coordination and status sharing across multiple invocations. Parameter validation implements specific checks for each tool parameter including enum validation, path resolution, and type checking with descriptive error messages. Progress reporting uses FastMCP Context methods with `await ctx.info()` and `await ctx.error()` for real-time user feedback during tool execution. Error logging uses structured logging with `exc_info=True` parameter for complete exception stack trace capture and debugging support. HTTP response formatting delegates to `format_http_response()` utility with status codes, response data, and content type specification for consistent Jesse Framework integration. Tool response data structures use nested dictionaries with comprehensive information organization supporting both programmatic access and human readability.

########### Code Usage Examples

Basic tool registration demonstrates the integration pattern for FastMCP server setup with knowledge base tools. This approach enables comprehensive manual indexing operations and system monitoring through standardized MCP tool interfaces.

```python
# Register knowledge base tools with FastMCP server for MCP client access
from fastmcp.server import FastMCP
from jesse_framework_mcp.knowledge_bases.tools import register_knowledge_bases_tools

# Initialize FastMCP server and register knowledge base tools
server = FastMCP("jesse-framework-mcp")
register_knowledge_bases_tools(server)

# Tools are now available for MCP client invocation:
# - knowledge_bases_index_trigger
# - knowledge_bases_status  
# - knowledge_bases_search
```

Manual indexing trigger demonstrates the tool invocation pattern for user-initiated knowledge base processing. This pattern enables targeted indexing operations with configurable scope and processing behavior for specific knowledge base maintenance requirements.

```python
# MCP client tool invocation pattern for manual indexing operations
import asyncio
from mcp_client import MCPClient

async def trigger_knowledge_base_indexing():
    client = MCPClient("jesse-framework-mcp")
    
    # Trigger incremental indexing for .knowledge directory
    result = await client.call_tool("knowledge_bases_index_trigger", {
        "target_path": ".knowledge",
        "indexing_mode": "incremental",
        "enable_git_clone_indexing": True,
        "enable_project_base_indexing": False
    })
    
    # Monitor indexing status during operation
    status = await client.call_tool("knowledge_bases_status", {})
    
    return result, status
```
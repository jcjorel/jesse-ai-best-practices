<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/main.py -->
<!-- Cached On: 2025-07-05T14:41:57.406862 -->
<!-- Source Modified: 2025-07-05T12:53:13.631186 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements the main FastMCP server for the Jesse Framework MCP Server, providing resource-first MCP protocol compliance with FastMCP native transport architecture for AI-assisted development workflows. The module serves as the central entry point orchestrating all framework resources including individual JESSE rules, project context, workflows, knowledge bases, and WIP tasks through standardized MCP resource endpoints. Key semantic entities include `FastMCP` server instance initialized as `server = FastMCP("JESSE Framework")`, primary resource handler `framework_index()` decorated with `@server.resource("jesse://index")` for lightweight resource discovery, prompt handlers `jesse_framework_start_prompt()`, `jesse_wip_task_create_prompt()`, and `jesse_knowledge_capture_prompt()` decorated with `@server.prompt()`, utility functions `get_embedded_workflow_files()` and `get_workflow_description()` for workflow metadata extraction, main entry point `main()` function using `server.run(transport="stdio")` for FastMCP native transport, resource registration through `from . import resources` auto-importing all resource handlers, knowledge base integration via `register_knowledge_bases_tools()` and `register_knowledge_bases_resources()`, HTTP formatting through `format_http_section()` with `XAsyncContentCriticality.INFORMATIONAL`, logging configuration using `logging.basicConfig(level=logging.INFO)`, and comprehensive resource index generation with JSON serialization including framework rules, project resources, knowledge bases, WIP tasks, and workflows. The system implements FastMCP 2.0 patterns with automatic lifecycle management eliminating manual event loop creation while providing comprehensive resource discovery and programmatic access to all framework components.

##### Main Components

The file contains one primary resource handler, three prompt handlers, two utility functions, and one main entry point providing comprehensive MCP server functionality. The `framework_index()` resource handler serves the `jesse://index` endpoint delivering lightweight JSON-based resource discovery with metadata for all framework components. The prompt handlers include `jesse_framework_start_prompt()` for framework initialization, `jesse_wip_task_create_prompt()` for WIP task creation with complexity assessment, and `jesse_knowledge_capture_prompt()` for structured knowledge capture workflows. Utility functions include `get_embedded_workflow_files()` for dynamic workflow discovery from embedded content and `get_workflow_description()` for human-readable workflow metadata extraction. The `main()` function serves as the primary entry point implementing FastMCP native transport with stdio communication and comprehensive error handling. Resource registration occurs through module imports including `from . import resources` for auto-registration of all resource handlers and explicit registration of knowledge base tools and resources.

###### Architecture & Design

The architecture implements a resource-first design with FastMCP native transport management, following clean separation between transport layer and resource implementations with automatic lifecycle management. The design emphasizes lightweight resource discovery through JSON-based indexing, comprehensive prompt template system for consistent AI assistant interaction, and modular resource organization with auto-registration patterns. Key design patterns include the resource-first pattern with individual resource access through dedicated URIs, auto-registration pattern leveraging FastMCP decorators for automatic resource handler discovery, lightweight indexing pattern providing fast metadata access without full content loading, prompt template pattern for reusable AI assistant interaction workflows, and native transport pattern using FastMCP's built-in stdio management eliminating manual event loop handling. The system uses composition over inheritance with modular resource imports, centralized server instance shared across all components, and defensive programming with descriptive error messages for all failure scenarios.

####### Implementation Approach

The implementation uses FastMCP native transport with `server.run(transport="stdio")` eliminating manual event loop management and leveraging FastMCP 2.0 automatic lifecycle handling. Resource discovery employs dynamic scanning of available components including framework rules enumeration through `get_available_rule_names()`, knowledge base scanning via `scan_available_knowledge_bases_async()`, and WIP task counting through directory iteration. Content delivery combines JSON serialization for structured metadata with HTTP formatting using `format_http_section()` for consistent MCP response patterns. The approach implements auto-registration through module imports with `from . import resources` triggering decorator-based resource handler registration, explicit knowledge base registration through dedicated functions, and comprehensive error handling with try-catch blocks and descriptive error messages. Prompt generation uses template-based patterns with parameter substitution and complexity-based guidance for different workflow scenarios. Logging employs standard Python logging with INFO level configuration for operational visibility and debugging support.

######## External Dependencies & Integration Points

**→ Inbound:**
- `fastmcp:FastMCP` - FastMCP framework providing native transport and MCP protocol compliance with automatic lifecycle management
- `fastmcp:Context` - FastMCP Context for resource operations with progress reporting and logging capabilities
- `logging` (external library) - server logging and error reporting with configurable log levels and structured output
- `pathlib.Path` (external library) - cross-platform filesystem operations for directory scanning and file access
- `json` (external library) - JSON serialization for resource index generation and structured data delivery
- `datetime` (external library) - timestamp generation for resource metadata and index generation
- `.resources` - auto-registration of all resource handlers through module import triggering decorator-based registration
- `.helpers.knowledge_scanners` - knowledge base scanning functionality for resource discovery and metadata extraction
- `.helpers.async_http_formatter:format_http_section` - HTTP section formatting with criticality classification for MCP responses
- `.knowledge_bases:register_knowledge_bases_tools` - knowledge base tool registration for MCP tool endpoints
- `.knowledge_bases:register_knowledge_bases_resources` - knowledge base resource registration for MCP resource endpoints

**← Outbound:**
- MCP clients - consuming framework resources through standardized MCP protocol with resource and prompt endpoints
- AI assistants - accessing framework initialization prompts and resource discovery through MCP transport
- Development environments - using Jesse Framework resources for AI-assisted development workflows and context delivery
- Cline AI assistant - consuming workflow resources as slash commands and framework prompts for development guidance
- FastMCP transport layer - receiving server instance configuration and resource handler registrations for protocol compliance
- Console applications - using main entry point for server startup and lifecycle management

**⚡ System role and ecosystem integration:**
- **System Role**: Central MCP server orchestrator for Jesse Framework ecosystem, providing FastMCP native transport with comprehensive resource discovery and prompt template system for AI-assisted development workflows
- **Ecosystem Position**: Core infrastructure component serving as primary MCP protocol interface, coordinating all framework resources and providing unified access point for AI assistants and development tools
- **Integration Pattern**: Used by MCP clients through stdio transport for resource and prompt access, consumed by AI assistants for framework initialization and workflow guidance, integrated with FastMCP framework through native transport patterns, and coordinated with all framework components through auto-registration and centralized server instance management

######### Edge Cases & Error Handling

The system handles FastMCP server startup failures through comprehensive exception handling in `main()` function with descriptive error logging and proper exception propagation. Resource index generation manages individual component failures through try-catch blocks preventing complete index failure when specific resources unavailable. Knowledge base scanning handles missing directories and access permissions through exception handling with empty list fallbacks. Workflow file discovery manages missing embedded content through exception propagation with detailed error context. WIP task counting handles non-existent directories through existence checking with zero count fallbacks. Prompt generation handles missing or invalid parameters through default value assignment and parameter validation. Server lifecycle management includes KeyboardInterrupt handling for graceful shutdown and comprehensive error logging for debugging support. Resource registration failures are managed through individual module error handling preventing complete server startup failure.

########## Internal Implementation Details

The module uses FastMCP native transport with `server = FastMCP("JESSE Framework")` initialization and `server.run(transport="stdio")` for automatic lifecycle management eliminating manual event loop creation. Resource index generation employs dynamic component discovery including rule enumeration through `await get_available_rule_names()`, knowledge base scanning with exception handling, and WIP task directory iteration using `Path(".knowledge/work-in-progress").iterdir()`. JSON serialization uses `json.dumps(index_data, indent=2, ensure_ascii=False)` for structured metadata delivery with Unicode support. HTTP formatting applies `format_http_section()` with `XAsyncContentCriticality.INFORMATIONAL` classification and `application/json` content type. Logging configuration uses `logging.basicConfig(level=logging.INFO)` with named logger `logger = logging.getLogger(__name__)` for structured output. Auto-registration leverages Python import system with `from . import resources` triggering decorator-based resource handler discovery. Prompt templates use f-string formatting with parameter substitution and conditional content based on input parameters. Error handling implements specific exception types with detailed error messages including component names and operation context for comprehensive debugging support.

########### Code Usage Examples

FastMCP server initialization demonstrates the primary startup pattern for Jesse Framework MCP server with native transport. This approach provides complete MCP protocol compliance with automatic lifecycle management and comprehensive resource registration.

```python
# Initialize and run Jesse Framework MCP server with FastMCP native transport
# Provides automatic lifecycle management and stdio transport for MCP protocol compliance
from jesse_framework_mcp.main import main

# Start server with comprehensive resource registration and error handling
main()
# Server runs with FastMCP native transport managing all protocol communication
```

Resource index access showcases the lightweight discovery pattern for programmatic framework exploration. This pattern enables efficient resource metadata access without full content loading for client optimization and resource enumeration.

```python
# Access lightweight framework resource index for programmatic discovery
# Returns JSON-structured metadata for all available framework resources
import json
from fastmcp import Context

# Framework index provides comprehensive resource metadata
index_response = await framework_index(Context())
index_data = json.loads(index_response)

# Access resource categories and metadata
framework_rules = index_data["resource_categories"]["framework_rules"]
available_rules = framework_rules["available_rules"]
uri_pattern = framework_rules["uri_pattern"]

# Use metadata for dynamic resource access
for rule_name in available_rules:
    rule_uri = uri_pattern.format(rule_name=rule_name)
    print(f"Framework rule: {rule_uri}")
```
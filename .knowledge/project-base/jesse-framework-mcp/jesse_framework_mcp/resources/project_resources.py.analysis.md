<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/resources/project_resources.py -->
<!-- Cached On: 2025-07-05T14:34:27.952209 -->
<!-- Source Modified: 2025-07-05T12:54:31.443198 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements project-specific resource handlers for the Jesse Framework MCP Server, providing individual access to project knowledge, WIP tasks, and context summaries through HTTP-formatted resources with INFORMATIONAL criticality classification for development context delivery. The module enables MCP clients to access project-specific information through dedicated resource URIs including `jesse://project/knowledge`, `jesse://project/context`, and `jesse://project/wip-tasks`, supporting comprehensive project development workflow management and context awareness. Key semantic entities include three primary resource handler functions `get_project_knowledge()`, `get_project_context_summary()`, and `get_wip_tasks_inventory()` decorated with `@server.resource()`, utility functions `get_project_resource_by_type()` and `register_project_resources()` for routing and registration, `format_http_section()` from `async_http_formatter` with `XAsyncContentCriticality.INFORMATIONAL` classification, `Context` from `fastmcp` for async progress reporting, `get_current_wip_task_name_async()` from session management for WIP task status, knowledge scanner functions `scan_git_clone_knowledge_bases_async()` and `scan_pdf_knowledge_bases_async()` for external knowledge enumeration, `pathlib.Path` for file system operations, `json` module for structured data serialization, and `writable=True` parameters enabling content editing capabilities for project files. The system implements graceful handling of missing project files with appropriate placeholder content and maintains HTTP formatting consistency across all project resource types.

##### Main Components

The file contains three primary resource handler functions and two utility functions providing comprehensive project-specific resource access capabilities. The `get_project_knowledge()` function serves project knowledge base content from `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md` with graceful handling for missing files. The `get_project_context_summary()` function builds comprehensive project overview combining WIP task status, knowledge base availability, external knowledge sources count, and framework architecture information. The `get_wip_tasks_inventory()` function scans `.knowledge/work-in-progress/` directory and builds structured JSON inventory with task metadata, status information, and access URIs. Supporting utility functions include `get_project_resource_by_type()` for centralized routing to appropriate resource handlers and `register_project_resources()` for explicit registration compatibility while leveraging FastMCP decorator auto-registration patterns.

###### Architecture & Design

The architecture implements a resource-oriented design pattern with individual resource handlers for different project aspects, following FastMCP server integration patterns with decorator-based resource registration and INFORMATIONAL criticality classification for project context delivery. The design emphasizes graceful handling of missing project files through existence checking and placeholder content generation, HTTP formatting preservation matching existing implementation patterns, and structured data organization for programmatic access. Key design patterns include the individual resource pattern providing dedicated handlers for each project aspect, graceful degradation pattern with placeholder content for missing files, structured data pattern using JSON formatting for WIP task inventory, context aggregation pattern combining multiple project information sources, and HTTP formatting preservation pattern maintaining existing format_http_section patterns. The system uses composition over inheritance with utility functions for resource routing, centralized error handling with descriptive error messages, and writable access control enabling content editing for project files.

####### Implementation Approach

The implementation uses async function patterns with FastMCP Context integration for progress reporting and structured logging throughout project resource loading operations. File system access employs `pathlib.Path` for cross-platform compatibility with existence checking and graceful handling of missing project files. Content loading implements UTF-8 encoding with empty content detection and placeholder generation for missing or empty files. The approach implements structured data organization using JSON serialization for WIP task inventory with metadata extraction including modification times and file availability status. Context aggregation combines multiple information sources including current WIP task status, knowledge base availability, external knowledge source counts, and project architecture overview. Error handling employs try-catch blocks with specific ValueError exceptions and detailed error context for debugging support. Resource routing uses dictionary mapping of resource types to handler functions for centralized access patterns.

######## External Dependencies & Integration Points

**→ Inbound:**
- `fastmcp:Context` - async progress reporting and structured logging for project resource loading operations
- `..main:server` - FastMCP server instance for resource registration with decorator patterns
- `..helpers.async_http_formatter:format_http_section` - HTTP section formatting with criticality classification and portable paths
- `..helpers.async_http_formatter:XAsyncContentCriticality` - content criticality enumeration for INFORMATIONAL classification
- `..helpers.async_http_formatter:XAsyncHttpPath` - HTTP path handling for portable resource location specification
- `..helpers.async_http_formatter:format_multi_section_response` - multi-section HTTP response formatting for complex resources
- `..helpers.session_management:get_current_wip_task_name_async` - current WIP task status retrieval for context building
- `..helpers.knowledge_scanners:scan_git_clone_knowledge_bases_async` - git clone knowledge base enumeration for external source counting
- `..helpers.knowledge_scanners:scan_pdf_knowledge_bases_async` - PDF knowledge base enumeration for external source counting
- `json` (external library) - structured data serialization for WIP task inventory JSON formatting
- `datetime` (external library) - timestamp generation for content metadata and modification tracking
- `pathlib.Path` (external library) - cross-platform file system operations for project file access

**← Outbound:**
- MCP clients - consuming project-specific resources through `jesse://project/{resource_type}` URIs for development context
- Development environments - using project knowledge and WIP task information for context-aware development workflows
- Session initialization systems - consuming project resources for comprehensive development context delivery
- AI assistants - accessing project context summaries and knowledge bases for project-aware assistance
- Project management tools - using WIP task inventory and project status information for development oversight

**⚡ System role and ecosystem integration:**
- **System Role**: Project-specific resource provider within Jesse Framework MCP Server ecosystem, delivering individual access to project knowledge, WIP tasks, and context summaries with INFORMATIONAL criticality for development context awareness
- **Ecosystem Position**: Core project component serving as primary interface for project-specific information, integrating with session initialization and providing foundation for project-aware development workflows
- **Integration Pattern**: Used by MCP clients through individual resource URI requests for project context, consumed by session initialization for comprehensive project information delivery, and integrated with knowledge management system for external source enumeration and project overview generation

######### Edge Cases & Error Handling

The system handles missing project knowledge base files through existence checking with placeholder content generation when `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md` unavailable. Empty project knowledge files are detected through content stripping with appropriate placeholder messages for empty but existing files. Missing WIP tasks directory is managed through existence checking with structured JSON response indicating directory status and setup guidance. WIP task scanning handles directory iteration errors with graceful degradation and empty task list fallbacks. External knowledge source counting implements try-catch blocks around scanner functions with fallback to zero counts when scanning fails. File modification time extraction handles permission errors and missing files with graceful omission from task metadata. Context aggregation manages individual component failures with partial context delivery and error isolation. Progress reporting uses FastMCP Context with structured logging for resource loading operations and error conditions.

########## Internal Implementation Details

The module uses file system access through `pathlib.Path` operations with existence checking using `.exists()` and size validation using `.stat().st_size` for content availability determination. Project knowledge loading implements UTF-8 encoding with `open(kb_path, 'r', encoding='utf-8')` and content validation through `.strip()` for empty file detection. WIP task inventory builds structured data using dictionary comprehensions with metadata extraction including task names, current task status, file availability flags, and modification timestamps. Context summary generation combines multiple information sources with formatted markdown content including project status, framework architecture, and resource access patterns. HTTP formatting employs `format_http_section()` with specific parameters including `content_type="text/markdown"` or `"application/json"`, `criticality=XAsyncContentCriticality.INFORMATIONAL`, portable location paths using `{PROJECT_ROOT}` placeholders, and `writable=True` for editable project content. Error handling implements specific exception types with detailed error messages including resource types and operation context. Resource routing uses dictionary mapping with handler function references for centralized access patterns and consistent error handling.

########### Code Usage Examples

Project knowledge access demonstrates the primary consumption pattern for project-specific knowledge base content with graceful handling of missing files. This approach provides project knowledge with INFORMATIONAL criticality for development context awareness.

```python
# Access project knowledge base through dedicated resource URI
# Returns HTTP-formatted knowledge content with graceful handling of missing files
knowledge_content = await mcp_client.read_resource("jesse://project/knowledge")
# Content includes project-specific knowledge or placeholder guidance for missing files
```

Project context and WIP task inventory showcases the structured data access pattern for comprehensive project information. This pattern enables project overview and task management through JSON-formatted responses with metadata and access information.

```python
# Access project context summary and WIP task inventory for comprehensive project overview
# Returns structured project information with current status and resource access patterns
context_summary = await mcp_client.read_resource("jesse://project/context")
wip_inventory = await mcp_client.read_resource("jesse://project/wip-tasks")

# Parse JSON inventory for programmatic task access
import json
task_data = json.loads(wip_inventory_content)
current_task = task_data.get("current_task")
active_tasks = task_data.get("active_tasks", [])
```
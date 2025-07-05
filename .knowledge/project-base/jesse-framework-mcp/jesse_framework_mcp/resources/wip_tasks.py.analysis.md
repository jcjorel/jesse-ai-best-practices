<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/resources/wip_tasks.py -->
<!-- Cached On: 2025-07-05T14:28:58.070917 -->
<!-- Source Modified: 2025-07-05T12:55:40.795217 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements WIP (Work-In-Progress) task resource handlers for the Jesse Framework MCP Server, providing comprehensive task management capabilities through HTTP-formatted resources including task inventory access, individual task retrieval, and project management context integration. The module enables MCP clients to access structured WIP task information through `jesse://wip-tasks` inventory resource and `jesse://wip-task/{task_name}` individual task resources, supporting project development workflow management and task tracking within the broader Jesse Framework ecosystem. Key semantic entities include `get_wip_tasks_inventory()` function decorated with `@server.resource("jesse://wip-tasks")`, `get_specific_wip_task()` function with `@server.resource("jesse://wip-task/{task_name}")` decorator, `register_wip_tasks_resources()` registration function, task metadata extraction functions `get_current_wip_task_info()`, `get_active_wip_tasks_list()`, `get_recently_completed_tasks()`, and `get_wip_task_statistics()`, content loading functions `load_wip_task_content()` and `load_wip_progress_content()`, utility functions `get_task_status()`, `get_task_git_branch()`, and `get_task_last_updated()`, `format_http_section()` from `async_http_formatter` module with `XAsyncContentCriticality.INFORMATIONAL` classification, `Context` from `fastmcp` for async progress reporting, `pathlib.Path` for cross-platform file operations, and `json` module for structured data serialization. The system implements HTTP-formatted resource delivery with `writable=True` parameters enabling content editing capabilities while maintaining INFORMATIONAL criticality classification for helpful project context delivery.

##### Main Components

The file contains two primary resource handler functions and nine supporting utility functions providing comprehensive WIP task management capabilities. The `get_wip_tasks_inventory()` function serves the main inventory resource with JSON-formatted task data including current task information, active tasks list, completed tasks, and task statistics. The `get_specific_wip_task()` function handles individual task access by combining WIP_TASK.md and PROGRESS.md content with task metadata. Supporting functions include `get_current_wip_task_info()` for parsing project knowledge base, `get_active_wip_tasks_list()` for directory-based task discovery, `get_recently_completed_tasks()` for completion tracking, `get_wip_task_statistics()` for project metrics, `load_wip_task_content()` and `load_wip_progress_content()` for file content retrieval, and metadata extraction functions `get_task_status()`, `get_task_git_branch()`, and `get_task_last_updated()` for comprehensive task information gathering. The `register_wip_tasks_resources()` function provides centralized resource registration coordination.

###### Architecture & Design

The architecture implements a resource-oriented design pattern with clear separation between HTTP resource endpoints and underlying task management logic, following FastMCP server integration patterns with decorator-based resource registration. The design emphasizes HTTP-formatted content delivery through `format_http_section()` with consistent INFORMATIONAL criticality classification and writable content flags for editing capabilities. Key design patterns include the resource handler pattern with FastMCP decorators for endpoint registration, async context manager pattern for progress reporting and logging, directory scanning pattern for task discovery from `.knowledge/work-in-progress/` structure, content aggregation pattern combining multiple file sources into unified responses, and graceful degradation pattern with placeholder content for missing files. The system uses composition over inheritance with utility functions for specific task operations, centralized error handling with descriptive error messages, and project root detection with working directory management for consistent file access across different MCP server launch contexts.

####### Implementation Approach

The implementation uses async function patterns with FastMCP Context integration for progress reporting and structured logging throughout task processing operations. Task discovery employs directory scanning of `.knowledge/work-in-progress/` with metadata extraction from WIP_TASK.md and PROGRESS.md files using pathlib for cross-platform compatibility. Content aggregation combines JSON serialization for inventory data with markdown formatting for individual task content, utilizing `format_http_section()` with specific content types and additional headers for metadata delivery. The approach implements working directory management with `os.chdir()` to project root for consistent file access, graceful error handling with try-catch blocks and descriptive error messages, and file system timestamp tracking for task activity monitoring. Data structures use dictionaries for task information with optional field handling and None-safe operations, while content loading employs UTF-8 encoding with fallback placeholder content for missing or inaccessible files.

######## External Dependencies & Integration Points

**→ Inbound:**
- `fastmcp:Context` - async progress reporting and structured logging for task processing operations
- `..main:server` - FastMCP server instance for resource registration with decorator patterns
- `..helpers.async_http_formatter:format_http_section` - HTTP section formatting with content type and criticality classification
- `..helpers.async_http_formatter:XAsyncContentCriticality` - content criticality enumeration for INFORMATIONAL classification
- `..helpers.async_http_formatter:XAsyncHttpPath` - HTTP path handling for resource location specification
- `..helpers.path_utils:get_project_root` - project root detection for consistent file access across launch contexts
- `..helpers.project_setup:get_project_setup_guidance` - fallback guidance when project root unavailable
- `json` (external library) - structured data serialization for task inventory JSON formatting
- `pathlib.Path` (external library) - cross-platform file system operations for task directory scanning
- `datetime` (external library) - timestamp generation and ISO format conversion for task metadata
- `os` (external library) - working directory management for consistent file access

**← Outbound:**
- MCP clients - consuming `jesse://wip-tasks` inventory resource for project task overview and management context
- MCP clients - accessing `jesse://wip-task/{task_name}` individual task resources for focused development work
- Development tools - using HTTP-formatted task content with writable flags for task editing and progress tracking
- Project management workflows - consuming task statistics and completion tracking for development oversight
- Git integration workflows - using task branch information for development workflow coordination

**⚡ System role and ecosystem integration:**
- **System Role**: WIP task resource provider within Jesse Framework MCP Server ecosystem, delivering structured task management capabilities through HTTP-formatted resources with comprehensive metadata and content aggregation
- **Ecosystem Position**: Core resource component serving project development workflows with task inventory and individual task access, integrating with project knowledge base and file system structure for comprehensive task management
- **Integration Pattern**: Used by MCP clients through resource URI requests, integrated with Jesse Framework project structure through `.knowledge/work-in-progress/` directory scanning, and coordinated with HTTP formatter helpers for consistent content delivery with editing capabilities

######### Edge Cases & Error Handling

The system handles missing project root through `get_project_root()` validation with fallback to `get_project_setup_guidance()` for setup instructions when project structure unavailable. Working directory management includes try-finally blocks with `os.chdir()` restoration to prevent directory state corruption across resource requests. File access errors are managed through try-catch blocks with descriptive error messages and graceful degradation to placeholder content for missing WIP_TASK.md or PROGRESS.md files. Task directory scanning handles non-existent `.knowledge/work-in-progress/` directories with empty list returns rather than exceptions. Content parsing implements None-safe operations for task metadata extraction with fallback to "Unknown" values when information unavailable. JSON serialization includes `ensure_ascii=False` for Unicode content support and structured error handling for malformed task data. Progress reporting uses FastMCP Context with percentage-based updates and error logging for debugging task processing issues.

########## Internal Implementation Details

The module uses working directory management with `os.getcwd()` preservation and `os.chdir(project_root)` for consistent file access regardless of MCP server launch location. Task metadata extraction employs line-by-line parsing of markdown files searching for specific patterns like "**Status**:" and "**Branch**:" with colon-based value extraction. File timestamp tracking uses `pathlib.Path.stat().st_mtime` with `datetime.fromtimestamp().isoformat()` conversion for standardized timestamp formatting. Content loading implements UTF-8 encoding with `.strip()` for whitespace handling and conditional content validation with placeholder generation for empty files. Task statistics calculation uses list comprehensions with conditional filtering for metrics like completion rates and file availability tracking. HTTP formatting includes specific additional headers like "Tasks-Count", "Current-Task", and "Last-Updated" for enhanced metadata delivery. Progress reporting implements percentage-based updates at 25%, 50%, 75%, and 100% completion stages with descriptive status messages for user feedback during task processing operations.

########### Code Usage Examples

Basic WIP tasks inventory access demonstrates the primary resource consumption pattern for project task overview. This approach provides comprehensive task management context through structured JSON data with HTTP formatting.

```python
# Access WIP tasks inventory through MCP resource URI for project task overview
# Returns HTTP-formatted JSON with current task, active tasks, completed tasks, and statistics
inventory_content = await mcp_client.read_resource("jesse://wip-tasks")
# Content includes task counts, current task information, and completion metrics
```

Individual task access showcases focused task content retrieval combining definition and progress tracking. This pattern enables detailed task examination with comprehensive metadata and combined content from multiple sources.

```python
# Access specific WIP task content through parameterized resource URI
# Combines WIP_TASK.md and PROGRESS.md with task metadata in single HTTP response
task_content = await mcp_client.read_resource("jesse://wip-task/feature-implementation")
# Returns markdown content with task definition, progress tracking, and Git branch information
```
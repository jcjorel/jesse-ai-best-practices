<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/helpers/content_loaders.py -->
<!-- Cached On: 2025-07-05T13:59:08.591220 -->
<!-- Source Modified: 2025-06-28T01:08:51.041174 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements content loading helper functions for the Jesse Framework MCP Server, providing async-first embedded content access and project knowledge loading operations with comprehensive progress reporting through FastMCP Context integration. The module enables self-contained framework delivery using build-time embedded content while supporting dynamic project knowledge loading from the `.knowledge/` directory structure. Key semantic entities include `load_embedded_content()` for generic embedded file access, `load_embedded_jesse_framework_async()` for complete framework loading, `load_embedded_jesse_workflows_async()` for workflow directory access, `load_embedded_jesse_rules_async()` for rule file loading, `load_project_knowledge_async()` for project-specific knowledge base access, `format_session_response_async()` for structured response formatting, `importlib.resources` for embedded content access, `FastMCP Context` for progress reporting, `get_jesse_rule_files()` constant integration, `embedded_content/` directory structure, nested path support with forward slash notation, and comprehensive error handling with descriptive ValueError exceptions. The system implements async-only architecture for modern MCP server integration with defensive loading patterns and clear error messages for missing embedded files.

##### Main Components

The file contains six primary async functions providing comprehensive content loading capabilities. The `load_embedded_content()` function offers generic embedded file access with nested path support using forward slash notation. The `load_embedded_jesse_framework_async()` function combines rules and workflows into complete framework delivery with Context progress reporting. The `load_embedded_jesse_workflows_async()` function discovers and loads all `.md` files from the `embedded_content/workflows/` directory with sorted ordering. The `load_embedded_jesse_rules_async()` function loads predefined JESSE rule files using `get_jesse_rule_files()` constant integration. The `load_project_knowledge_async()` function reads project-specific knowledge from `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md` with fallback handling. The `format_session_response_async()` function combines all loaded content sections with structured delimiters, session metadata, and availability information for complete session initialization responses.

###### Architecture & Design

The architecture implements async-first design patterns with comprehensive FastMCP Context integration for progress reporting and error handling throughout all loading operations. The design follows self-contained framework delivery principles using build-time embedded content accessed through `importlib.resources` with fallback compatibility for Python versions before 3.9. Key design patterns include the async function pattern for non-blocking operations, defensive loading pattern with clear error messages and fallback content, structured response formatting pattern with consistent section delimiters, and modular content loading pattern separating embedded framework content from project-specific knowledge. The system uses nested path support for embedded content organization and comprehensive error handling with descriptive ValueError exceptions for debugging and troubleshooting.

####### Implementation Approach

The implementation uses `importlib.resources` for embedded content access with dynamic path construction supporting nested directory structures through forward slash notation parsing. Content loading employs try-catch error handling with descriptive error messages and Context integration for progress reporting during multi-file operations. The approach implements sorted file discovery for consistent ordering in workflow loading and explicit file list processing for rule loading using `get_jesse_rule_files()` constant. Session response formatting uses structured content assembly with clear section delimiters and metadata inclusion for session tracking. Error handling provides fallback content for missing project knowledge files and comprehensive exception wrapping with detailed error context for debugging support.

######## External Dependencies & Integration Points

**→ Inbound:**
- `importlib.resources` (external library) - embedded content access with Python 3.9+ compatibility and importlib_resources fallback
- `importlib_resources` (external library) - Python < 3.9 compatibility fallback for embedded content access
- `fastmcp:Context` - FastMCP context providing progress reporting and error logging capabilities
- `..constants:get_jesse_rule_files` - constant function providing predefined JESSE rule file list
- `datetime` (external library) - timestamp generation for session response metadata
- `pathlib.Path` (external library) - cross-platform filesystem operations for project knowledge loading

**← Outbound:**
- MCP server session initialization - consuming formatted session responses with complete framework context
- Jesse Framework resource endpoints - using embedded content loading for resource delivery
- Project context loading workflows - consuming project knowledge loading for dynamic content access
- Development tools - accessing embedded workflows and rules for framework delivery

**⚡ System role and ecosystem integration:**
- **System Role**: Core content loading infrastructure for Jesse Framework MCP server, providing embedded framework delivery and project knowledge access with comprehensive progress reporting
- **Ecosystem Position**: Central helper component supporting MCP server initialization and resource delivery, bridging embedded build-time content with runtime project knowledge loading
- **Integration Pattern**: Used by MCP server during session initialization for complete framework context loading, consumed by resource endpoints for embedded content delivery, and integrated with project knowledge workflows for dynamic content access

######### Edge Cases & Error Handling

The system handles missing embedded files through comprehensive try-catch blocks with descriptive ValueError exceptions including specific file paths and error context. Empty embedded files are detected and raise ValueError with clear error messages for debugging. Nested path parsing handles malformed paths gracefully with fallback to direct file access patterns. Project knowledge loading handles missing `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md` files by returning placeholder content with informative messages. Workflow directory access handles empty directories by returning appropriate messages and continues processing despite individual file loading failures. Rule file loading handles missing files by raising descriptive errors while maintaining processing context. Session response formatting handles missing content sections by including appropriate status messages and availability indicators.

########## Internal Implementation Details

The embedded content access uses dynamic path construction with `resources.files()` and iterative directory traversal for nested paths through forward slash splitting. File loading employs UTF-8 encoding with content stripping for clean text processing and empty content validation. Progress reporting uses Context methods with detailed file counting and status updates during multi-file operations. Error handling implements exception chaining with original error preservation and descriptive message construction. Session response formatting uses list-based content assembly with join operations for efficient string building and structured delimiter patterns. The system maintains consistent section header formatting with uppercase file names and clear content boundaries for parsing and display purposes.

########### Code Usage Examples

Basic embedded content loading demonstrates the generic file access pattern for any embedded resource. This approach provides flexible content access with nested path support for organized embedded content structures.

```python
# Load generic embedded content with nested path support
content = await load_embedded_content("rules/JESSE_CODE_COMMENTS.md")
# Supports both direct files and nested directory structures
workflow_content = await load_embedded_content("workflows/development.md")
```

Complete framework loading showcases the comprehensive session initialization pattern with progress reporting. This pattern provides complete Jesse Framework context with structured content organization and user feedback.

```python
# Load complete Jesse Framework with progress reporting
async def initialize_session(ctx: Context):
    # Load complete embedded framework
    framework_content = await load_embedded_jesse_framework_async(ctx)
    
    # Load project-specific knowledge
    project_knowledge = await load_project_knowledge_async(ctx)
    
    # Format complete session response
    session_response = await format_session_response_async(
        session_id="session_123",
        user_prompt="Initialize framework",
        load_wip_tasks=True,
        embedded_content=framework_content,
        project_knowledge=project_knowledge,
        kb_inventory="Available knowledge bases...",
        wip_content="Current WIP tasks...",
        ctx=ctx
    )
    
    return session_response
```
<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/helpers/knowledge_scanners.py -->
<!-- Cached On: 2025-07-05T14:00:22.675696 -->
<!-- Source Modified: 2025-06-27T23:23:19.776833 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements knowledge base scanning and loading helper functions for the Jesse Framework MCP Server, providing discovery-based approaches to find and load available git clone and PDF knowledge bases from the `.knowledge/` directory structure with comprehensive FastMCP Context integration. The module enables flexible knowledge base management through async-only architecture supporting multiple storage locations with detailed progress reporting and error handling. Key semantic entities include `scan_git_clone_knowledge_bases_async()` for git repository knowledge discovery, `scan_pdf_knowledge_bases_async()` for PDF-derived knowledge scanning, `generate_knowledge_base_inventory_async()` for comprehensive knowledge base cataloging, `load_specific_knowledge_base_async()` for targeted knowledge base loading, `FastMCP Context` for progress reporting and error logging, `pathlib.Path` for cross-platform filesystem operations, `.knowledge/git-clones/` and `.knowledge/pdf-knowledge/` directory structures, `*_kb.md` file pattern matching, size-based metadata classification, and lazy loading instruction generation. The system implements discovery-based knowledge base management with descriptive naming patterns to help LLM selection of relevant repositories and documents.

##### Main Components

The file contains four primary async functions providing comprehensive knowledge base discovery and loading capabilities. The `scan_git_clone_knowledge_bases_async()` function scans the `.knowledge/git-clones/` directory for `*_kb.md` files, extracting repository names and providing size-based metadata classification. The `scan_pdf_knowledge_bases_async()` function performs similar scanning for the `.knowledge/pdf-knowledge/` directory, discovering PDF-derived knowledge files with size estimates. The `generate_knowledge_base_inventory_async()` function combines both scanning operations to create structured inventories with lazy loading instructions and comprehensive progress reporting. The `load_specific_knowledge_base_async()` function provides targeted knowledge base loading with flexible name normalization, multi-location searching, and detailed error reporting through FastMCP Context integration.

###### Architecture & Design

The architecture implements async-only design patterns with comprehensive FastMCP Context integration for progress reporting and error handling throughout all knowledge base operations. The design follows discovery-based principles using filesystem scanning to identify available knowledge bases rather than maintaining static configurations. Key design patterns include the async function pattern for non-blocking operations, discovery-based scanning pattern using glob patterns for file matching, flexible loading pattern supporting multiple storage locations, and structured inventory generation pattern with descriptive metadata. The system uses size-based classification for context window management and normalized naming conventions for consistent knowledge base identification across different storage locations.

####### Implementation Approach

The implementation uses `pathlib.Path` operations with glob pattern matching (`*_kb.md`) for knowledge base discovery across multiple directory locations. Knowledge base scanning employs file size analysis with threshold-based classification (large >50KB, medium >10KB, small ≤10KB) for context management guidance. The approach implements flexible name normalization ensuring `_kb` suffix consistency and multi-location search patterns covering both git-clones and PDF knowledge directories. Inventory generation uses structured text formatting with clear section delimiters and lazy loading instructions for user guidance. Error handling provides comprehensive exception management with detailed Context logging and appropriate exception types for different failure scenarios.

######## External Dependencies & Integration Points

**→ Inbound:**
- `pathlib.Path` (external library) - cross-platform filesystem operations for directory scanning and file access
- `fastmcp:Context` - FastMCP context providing progress reporting, error logging, and user interaction capabilities
- `typing.List` (external library) - type annotations for function return values and parameter specifications

**← Outbound:**
- Jesse Framework MCP server tools - consuming knowledge base inventory and loading functions for dynamic content access
- MCP resource endpoints - using knowledge base scanning for resource discovery and availability reporting
- Knowledge base management workflows - consuming scanning results for automated knowledge base maintenance
- LLM context management systems - using size-based metadata for context window optimization

**⚡ System role and ecosystem integration:**
- **System Role**: Core knowledge base discovery and loading infrastructure for Jesse Framework MCP server, providing dynamic knowledge base management with comprehensive scanning and loading capabilities
- **Ecosystem Position**: Central helper component supporting MCP server knowledge base operations, bridging filesystem-based knowledge storage with runtime knowledge access patterns
- **Integration Pattern**: Used by MCP server tools for knowledge base discovery and loading, consumed by resource endpoints for availability reporting, and integrated with knowledge management workflows for automated maintenance and optimization

######### Edge Cases & Error Handling

The system handles missing knowledge base directories by checking directory existence before scanning and providing informative Context logging when directories are not found. File access errors during knowledge base loading are caught and converted to appropriate exception types with detailed error messages including file paths and failure context. Empty knowledge base files are handled gracefully with size reporting and appropriate metadata classification. Invalid knowledge base names are normalized through suffix handling and multi-location searching to maximize discovery success. Directory permission issues are managed through comprehensive exception handling with Context error reporting. Knowledge base inventory generation handles empty directories by providing clear "None available" messages and appropriate user guidance for lazy loading operations.

########## Internal Implementation Details

The knowledge base scanning uses `glob("*_kb.md")` pattern matching for consistent file discovery across different directory structures. File size analysis employs `stat().st_size` operations with threshold-based classification using hardcoded size limits for consistent metadata generation. Name normalization implements suffix checking and automatic `_kb` appending for flexible knowledge base identification. Multi-location searching uses list-based search path definitions covering both git-clones and PDF knowledge directories with sequential checking. Progress reporting uses Context methods with detailed file counting and status updates during scanning operations. Error handling implements exception chaining with original error preservation and descriptive message construction for debugging support.

########### Code Usage Examples

Basic knowledge base inventory generation demonstrates the discovery pattern for available knowledge bases. This approach provides comprehensive scanning with progress reporting and structured inventory formatting for user guidance.

```python
# Generate comprehensive knowledge base inventory with progress reporting
async def get_available_knowledge_bases(ctx: Context):
    inventory = await generate_knowledge_base_inventory_async(ctx)
    return inventory
    # Returns structured inventory with git clone and PDF knowledge bases
    # Includes size metadata and lazy loading instructions
```

Specific knowledge base loading showcases the flexible loading pattern with multi-location searching and error handling. This pattern enables targeted knowledge base access with comprehensive error reporting and Context integration.

```python
# Load specific knowledge base with flexible name handling and error reporting
async def load_repository_knowledge(repo_name: str, ctx: Context):
    try:
        # Supports both "repo_name" and "repo_name_kb" formats
        content = await load_specific_knowledge_base_async(repo_name, ctx)
        return content
    except FileNotFoundError as e:
        await ctx.error(f"Knowledge base not found: {e}")
        return None
    except ValueError as e:
        await ctx.error(f"Failed to load knowledge base: {e}")
        return None
```
<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/resources/knowledge.py -->
<!-- Cached On: 2025-07-05T14:35:53.618547 -->
<!-- Source Modified: 2025-07-05T12:55:09.599174 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements JESSE Framework knowledge base resource handlers for the MCP server, providing project knowledge bases as HTTP-formatted MCP resources with lazy loading functionality and direct access to specific knowledge bases without tool overhead. The module enables MCP clients to access various knowledge base types including git clone repositories, PDF documents, and project-specific knowledge through dedicated resource URIs supporting both index access and individual knowledge base retrieval. Key semantic entities include primary resource handler functions `get_git_clones_readme()`, `get_pdf_knowledge_readme()`, and `get_knowledge_base()` for knowledge access, metadata extraction functions `determine_knowledge_base_info()`, `extract_git_clone_kb_info()`, and `extract_pdf_kb_info()` for knowledge base analysis, utility functions `register_knowledge_resources()` and `get_file_modification_time()` for registration and file operations, `format_http_section()` from `async_http_formatter` with `XAsyncContentCriticality.INFORMATIONAL` classification, `Context` from `fastmcp` for async progress reporting, `get_project_root()` from path utilities for project location detection, knowledge base directory paths including `.knowledge/git-clones/`, `.knowledge/pdf-knowledge/`, and `.knowledge/persistent-knowledge/`, resource URIs `jesse://knowledge/git-clones-readme`, `jesse://knowledge/pdf-knowledge-readme`, and `jesse://knowledge/{kb_name}`, and `writable=True` parameters enabling content editing capabilities for knowledge base management. The system implements resource-based knowledge delivery with HTTP-formatted content for consistent parsing and metadata extraction across different knowledge base types.

##### Main Components

The file contains three primary resource handler functions, three metadata extraction functions, and two utility functions providing comprehensive knowledge base resource management capabilities. The `get_git_clones_readme()` function serves git clone knowledge base index from `.knowledge/git-clones/README.md` with HTTP formatting and writable capability. The `get_pdf_knowledge_readme()` function handles PDF knowledge base index from `.knowledge/pdf-knowledge/README.md` with graceful handling for missing directories and placeholder content generation. The `get_knowledge_base()` function provides individual knowledge base access supporting both git clone and PDF knowledge base types with metadata determination and content loading. Supporting metadata functions include `determine_knowledge_base_info()` for knowledge base type and location analysis, `extract_git_clone_kb_info()` for git repository metadata extraction, and `extract_pdf_kb_info()` for PDF document metadata extraction. Utility functions include `register_knowledge_resources()` for MCP resource registration and `get_file_modification_time()` for timestamp formatting.

###### Architecture & Design

The architecture implements a resource-oriented design pattern with individual resource handlers for different knowledge base types, following HTTP-formatted content delivery for consistent AI assistant processing and lazy loading functionality for on-demand knowledge base access. The design emphasizes graceful handling of missing knowledge bases through existence checking and placeholder content generation, portable path resolution using project root detection, and metadata extraction from knowledge base content headers. Key design patterns include the resource handler pattern with dedicated functions for each knowledge base type, lazy loading pattern for on-demand knowledge base retrieval, metadata extraction pattern parsing knowledge base headers for repository and document information, graceful degradation pattern with placeholder content for missing files, and HTTP formatting pattern maintaining consistent content delivery with appropriate criticality classification. The system uses composition over inheritance with utility functions for metadata operations, centralized error handling with descriptive error messages, and writable access control enabling knowledge base content editing.

####### Implementation Approach

The implementation uses async function patterns with FastMCP Context integration for progress reporting and structured logging throughout knowledge base loading operations. File system access employs absolute path construction using `os.path.join()` with project root detection for consistent file access across different deployment contexts. Content loading implements UTF-8 encoding with existence checking and graceful handling of missing files through placeholder content generation. The approach implements metadata extraction through content parsing of knowledge base headers searching for specific patterns like repository URLs, source documents, and modification timestamps. Knowledge base type determination uses file path pattern matching checking for git clone and PDF knowledge base locations with extensible design for additional types. Error handling employs try-catch blocks with specific ValueError exceptions and detailed error context for debugging support. HTTP formatting applies `format_http_section()` with INFORMATIONAL criticality, portable path placeholders, and additional headers for knowledge base metadata.

######## External Dependencies & Integration Points

**→ Inbound:**
- `fastmcp:Context` - async progress reporting and structured logging for knowledge base loading operations
- `..helpers.async_http_formatter:format_http_section` - HTTP section formatting with criticality classification and portable paths
- `..helpers.async_http_formatter:XAsyncContentCriticality` - content criticality enumeration for INFORMATIONAL classification
- `..helpers.async_http_formatter:XAsyncHttpPath` - HTTP path handling for portable resource location specification
- `..helpers.path_utils:get_project_root` - project root detection for consistent file access across deployment contexts
- `..main:server` - FastMCP server instance for resource registration with decorator patterns
- `..helpers.knowledge_scanners:load_specific_knowledge_base_async` - knowledge base content loading for individual knowledge bases
- `os` (external library) - file system operations for path construction and file existence checking
- `json` (external library) - structured data serialization for knowledge base metadata
- `datetime` (external library) - timestamp generation and ISO format conversion for file modification times
- `pathlib.Path` (external library) - cross-platform path operations for file system compatibility

**← Outbound:**
- MCP clients - consuming knowledge base resources through `jesse://knowledge/{resource_type}` URIs for AI assistant context
- Session initialization systems - consuming knowledge base indexes for comprehensive development context delivery
- AI assistants - accessing individual knowledge bases for project-specific context and repository information
- Development environments - using knowledge base content for context-aware development workflows and documentation access
- Knowledge management workflows - consuming knowledge base indexes for repository and document management

**⚡ System role and ecosystem integration:**
- **System Role**: Knowledge base resource provider within Jesse Framework MCP Server ecosystem, delivering HTTP-formatted access to git clone repositories, PDF documents, and project knowledge with lazy loading functionality for AI assistant context delivery
- **Ecosystem Position**: Core knowledge component serving as primary interface for external knowledge sources, integrating with session initialization and providing foundation for project-aware AI assistance through structured knowledge base access
- **Integration Pattern**: Used by MCP clients through individual resource URI requests for knowledge base access, consumed by session initialization for knowledge base enumeration, and integrated with knowledge management workflows for repository and document indexing with writable content editing capabilities

######### Edge Cases & Error Handling

The system handles missing project root through `get_project_root()` validation with ValueError exceptions when project structure unavailable for knowledge base access. Missing knowledge base directories are managed through existence checking with placeholder content generation for PDF knowledge directory when `.knowledge/pdf-knowledge/` unavailable. Missing README files trigger ValueError exceptions with descriptive error messages including file paths and operation context. Knowledge base type determination handles unknown knowledge base names through systematic checking of git clone, PDF, and essential knowledge base locations with fallback error handling. Metadata extraction manages missing or malformed knowledge base headers through graceful parsing with fallback to file modification timestamps. File system permission errors are handled through try-catch blocks with appropriate error logging and exception propagation. Content loading failures implement UTF-8 encoding error handling with detailed error context for debugging support.

########## Internal Implementation Details

The module uses absolute path construction through `os.path.join(project_root, relative_path)` for consistent file access across different deployment contexts and working directories. Knowledge base type determination implements systematic checking with file path patterns including `.knowledge/git-clones/{kb_name}_kb.md` for git repositories, `.knowledge/pdf-knowledge/{kb_name}/{kb_name}_kb.md` for PDF documents, and `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md` for essential project knowledge. Metadata extraction employs content parsing of first 20 lines searching for specific header patterns including `**Clone URL**:`, `**Repository**:`, `**Source PDF**:`, and `*Last Updated:` with fallback to file modification timestamps. HTTP formatting uses `format_http_section()` with specific parameters including `content_type="text/markdown"`, `criticality=XAsyncContentCriticality.INFORMATIONAL`, portable location paths using `{PROJECT_ROOT}` placeholders, and additional headers for knowledge type, source URLs, and modification timestamps. File modification time extraction uses `os.stat()` with ISO format conversion through `datetime.fromtimestamp().isoformat() + 'Z'` for consistent timestamp formatting. Resource registration employs direct server decoration with `server.resource()` calls for each knowledge base resource handler.

########### Code Usage Examples

Knowledge base index access demonstrates the primary consumption pattern for git clone and PDF knowledge base indexes with HTTP formatting. This approach provides knowledge base overview and management capabilities through dedicated resource endpoints.

```python
# Access knowledge base indexes through dedicated resource URIs
# Returns HTTP-formatted index content with metadata and writable capability
git_clones_index = await mcp_client.read_resource("jesse://knowledge/git-clones-readme")
pdf_knowledge_index = await mcp_client.read_resource("jesse://knowledge/pdf-knowledge-readme")
# Content includes knowledge base listings, directory structure, and management guidance
```

Individual knowledge base access showcases the lazy loading pattern for specific knowledge base retrieval with metadata extraction. This pattern enables on-demand knowledge base loading with comprehensive metadata and content delivery for AI assistant context.

```python
# Access individual knowledge base through parameterized resource URI
# Returns HTTP-formatted knowledge base content with metadata headers
knowledge_base = await mcp_client.read_resource("jesse://knowledge/cline_kb")
# Content includes full knowledge base with repository information and modification timestamps

# Knowledge base metadata available through HTTP headers
metadata = knowledge_base.headers
kb_type = metadata.get("Knowledge-Type")  # 'git-clone', 'pdf', or 'essential'
source_url = metadata.get("Source-URL")   # Repository or document source
last_updated = metadata.get("Last-Updated")  # ISO timestamp
```
<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/simple_template_generator.py -->
<!-- Cached On: 2025-07-04T17:01:07.027120 -->
<!-- Source Modified: 2025-07-04T15:48:55.042932 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

The `SimpleTemplateGenerator` class implements a full rebuild approach for knowledge base file generation using template-based content assembly and three-trigger timestamp change detection. This component provides complete knowledge file generation capabilities through `generate_complete_knowledge_file()`, comprehensive change detection via `directory_needs_rebuild()`, and alphabetical content sorting for consistent output structure. Key semantic entities include `FileContext`, `DirectoryContext`, `get_portable_path()`, `_generate_warning_header()`, `_generate_subdirectory_section()`, `_generate_file_section()`, `_generate_metadata_footer()`, and `_should_process_file()` for selective file filtering. The system eliminates complex incremental updates by generating complete knowledge files from templates on every change, using `st_mtime` filesystem timestamps for efficient change detection across directory structures, source files, and subdirectory knowledge bases.

##### Main Components

The system contains core template generation components: `SimpleTemplateGenerator` main class orchestrating complete file generation, `directory_needs_rebuild()` implementing three-trigger change detection, `generate_complete_knowledge_file()` creating structured knowledge content, and specialized section generators including `_generate_warning_header()`, `_generate_subdirectory_section()`, `_generate_file_section()`, and `_generate_metadata_footer()`. Supporting utilities include `_generate_timestamp()` for ISO 8601 formatted timestamps, `_should_process_file()` for extension-based file filtering, and `_get_kb_path()` for consistent knowledge base file naming. The template system processes `FileContext` objects with knowledge content and `DirectoryContext` structures with subdirectory summaries, generating complete markdown files with alphabetical sorting and portable path formatting.

###### Architecture & Design

The architecture follows a template-based full rebuild pattern eliminating complex incremental update logic in favor of complete file regeneration. The three-trigger change detection system compares directory `st_mtime`, individual source file timestamps, and subdirectory knowledge base modification times against existing knowledge base files. Template generation uses string concatenation with predefined section structures: warning headers, global summaries, subdirectory knowledge integration, file knowledge integration, and metadata footers. The design enforces alphabetical sorting through `sorted()` operations on file contexts and subdirectory summaries using case-insensitive key functions. Content preservation maintains LLM formatting through direct insertion without transformation, while portable path conversion ensures cross-platform compatibility through `get_portable_path()` integration.

####### Implementation Approach

The implementation uses filesystem `stat()` operations for efficient timestamp-based change detection, comparing `st_mtime` values across three triggers: directory structure changes, source file modifications, and subdirectory knowledge base updates. Template generation employs string list concatenation with `"\n".join(content_parts)` for predictable output assembly. File filtering uses extension-based detection with a comprehensive set of processable extensions including source code formats (`.py`, `.js`, `.ts`, `.java`, `.cpp`), documentation formats (`.md`, `.txt`, `.json`, `.yaml`), and configuration formats (`.toml`, `.cfg`, `.ini`). Content sorting applies `key=lambda f: f.file_path.name.lower()` for case-insensitive alphabetical ordering. Error handling uses try-catch blocks with fallback content generation and detailed logging for debugging template generation failures.

######## External Dependencies & Integration Points

**→ Inbound:**
- `..models.knowledge_context.FileContext` - File processing state with knowledge content and metadata
- `..models.knowledge_context.DirectoryContext` - Directory processing state with file and subdirectory contexts
- `...helpers.path_utils.get_portable_path` - Cross-platform path normalization for template headers
- `pathlib.Path` (external library) - Filesystem operations and path manipulation
- `datetime.datetime` (external library) - ISO 8601 timestamp generation for content tracking
- `typing.List` (external library) - Type hints for template parameters and content structures

**← Outbound:**
- `knowledge_output_directory/{directory_name}_kb.md` - Generated knowledge base files with complete template structure
- `../knowledge_builder.py:KnowledgeBuilder` - Consumes template generation for directory knowledge assembly
- Filesystem through `Path.stat()` - Timestamp queries for change detection triggers
- Logging system through `logger` - Template generation progress and error reporting

**⚡ System role and ecosystem integration:**
- **System Role**: Core template engine within the Jesse Framework MCP knowledge base generation pipeline, serving as the primary content assembly mechanism for hierarchical knowledge files
- **Ecosystem Position**: Central component bridging LLM-generated content with structured markdown output, critical for the full rebuild approach replacing complex incremental updates
- **Integration Pattern**: Used by `KnowledgeBuilder` for complete knowledge file generation, consumed by filesystem for persistent knowledge storage, and integrated with change detection systems for efficient rebuild decisions

######### Edge Cases & Error Handling

The system handles missing knowledge base files by returning `True` for rebuild decisions with reason "KB file doesn't exist". Filesystem errors during timestamp comparison trigger rebuild with error reason logging through `logger.error()`. Portable path conversion failures fall back to directory name with appropriate warning logging. Template generation errors use fallback content with error messages embedded in sections, such as `*Error generating section: {e}*` for individual section failures. File extension detection handles case-insensitive comparison through `.suffix.lower()` for cross-platform compatibility. Empty content scenarios generate placeholder text like `*No content available*` or `*No analysis available*` to maintain template structure integrity. Change detection exceptions default to rebuild decisions with error reason reporting to ensure knowledge base freshness over optimization.

########## Internal Implementation Details

The three-trigger system iterates through `directory_path.iterdir()` for comprehensive file and subdirectory scanning, using `source_file.stat().st_mtime` comparisons against `kb_timestamp` for precise change detection. Template section generation uses list comprehension with conditional content insertion: `f"\n\n{subdir_summary.strip()}" if subdir_summary.strip() else "\n\n*No content available*"`. File extension filtering maintains a comprehensive set of 40+ processable extensions stored in a set for O(1) lookup performance. Timestamp generation uses `datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")` for consistent ISO 8601 formatting. Knowledge base path generation follows the pattern `{directory_path.name}_kb.md` placed in the parent directory for adjacent discovery. Content sorting applies stable sort algorithms ensuring consistent output across multiple generations with identical input data.

########### Code Usage Examples

**Initialize template generator and check rebuild requirements:**
```python
generator = SimpleTemplateGenerator()
needs_rebuild, reason = generator.directory_needs_rebuild(
    directory_path=Path("src/components"),
    kb_file_path=Path("src/components_kb.md")
)
if needs_rebuild:
    print(f"Rebuild needed: {reason}")
```

**Generate complete knowledge file with sorted content:**
```python
file_contexts = [FileContext(file_path=Path("module.py"), knowledge_content="Analysis...")]
subdir_summaries = [(Path("utils/"), "Utility functions summary")]
complete_content = generator.generate_complete_knowledge_file(
    directory_path=Path("src/"),
    global_summary="Directory contains core application modules",
    file_contexts=file_contexts,
    subdirectory_summaries=subdir_summaries,
    kb_file_path=Path("src_kb.md")
)
```

**Check file processing eligibility with extension filtering:**
```python
should_process = generator._should_process_file(Path("script.py"))  # Returns True
should_skip = generator._should_process_file(Path("binary.exe"))   # Returns False
processable_types = {'.py', '.js', '.md', '.json', '.yaml'}  # Subset of supported extensions
```
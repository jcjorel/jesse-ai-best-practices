<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/knowledge_file_generator.py -->
<!-- Cached On: 2025-07-05T11:32:07.092677 -->
<!-- Source Modified: 2025-07-04T22:38:52.808986 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This module provides template-based knowledge file generation for the JESSE Framework's hierarchical indexing system, implementing a full rebuild approach with alphabetical sorting and comprehensive timestamp-based change detection. The `KnowledgeFileGenerator` class enables complete knowledge base file creation from directory contexts, replacing complex incremental updates with straightforward template generation. Key semantic entities include `KnowledgeFileGenerator` class, `FileContext` and `DirectoryContext` models, `get_portable_path` utility, three-trigger change detection system (`directory_needs_rebuild`), template generation methods (`generate_complete_knowledge_file`, `_generate_warning_header`, `_generate_subdirectory_section`, `_generate_file_section`, `_generate_metadata_footer`), file filtering logic (`_should_process_file`), and CommonMark-compliant markdown output. The system provides deterministic knowledge file generation with cross-platform path compatibility, preserving LLM-generated content formatting without transformation while ensuring consistent alphabetical ordering across all generated knowledge base files.

##### Main Components

The module contains the `KnowledgeFileGenerator` class as the primary component, implementing template-based knowledge file generation. Core methods include `directory_needs_rebuild()` for three-trigger timestamp-based change detection, `generate_complete_knowledge_file()` for complete knowledge base file creation from components, and private helper methods `_generate_warning_header()`, `_generate_subdirectory_section()`, `_generate_file_section()`, and `_generate_metadata_footer()` for template section generation. Supporting methods include `_should_process_file()` for file type filtering based on processable extensions, `_get_kb_path()` for knowledge base file path generation, and `_generate_timestamp()` for consistent ISO 8601 timestamp formatting. The class operates with minimal initialization requirements and focuses on string template generation rather than complex parsing operations.

###### Architecture & Design

The architecture follows a full rebuild design pattern, generating complete knowledge files from templates on every change rather than implementing complex incremental updates. The system employs a three-trigger timestamp comparison system checking directory structure changes, individual file modifications, and subdirectory knowledge base updates. Template generation uses string concatenation with alphabetical sorting of all content components before assembly. The design emphasizes simplicity and reliability through deterministic template generation, avoiding complex parsing dependencies and section replacement logic. Cross-platform compatibility is achieved through portable path conversion and case-insensitive file extension filtering. The architecture preserves LLM-generated content formatting through direct insertion without transformation, ensuring knowledge content integrity throughout the generation process.

####### Implementation Approach

The implementation uses filesystem timestamp comparison (`st_mtime`) for efficient change detection across three triggers: directory modification time, source file modification times, and subdirectory knowledge base modification times. Template generation employs list-based content assembly with alphabetical sorting using `sorted()` with case-insensitive key functions. String template approach builds complete knowledge files through section concatenation, including warning headers, directory summaries, subdirectory integration sections, file knowledge sections, and metadata footers. File filtering implements extension-based processing using a comprehensive set of processable file extensions covering source code, documentation, and configuration files. Error handling provides graceful degradation with fallback content generation and detailed logging for debugging. The system generates portable paths for cross-platform compatibility and maintains consistent markdown formatting following CommonMark specifications.

######## External Dependencies & Integration Points

**→ Inbound:**
- `..models.knowledge_context:FileContext` - file metadata and knowledge content structure
- `..models.knowledge_context:DirectoryContext` - directory context and summary information
- `...helpers.path_utils:get_portable_path` - cross-platform path conversion utility
- `pathlib.Path` (standard library) - filesystem path operations and metadata access
- `datetime.datetime` (standard library) - timestamp generation for content tracking
- `logging` (standard library) - debug and error logging throughout generation process

**← Outbound:**
- `knowledge_base_files/*.md` - generated markdown knowledge base files consumed by indexing system
- `hierarchical_indexer.py` - knowledge file generator used by directory processing workflow
- `knowledge_base_manager.py` - template generation integrated into knowledge base management operations
- External markdown parsers - CommonMark-compliant output for standard markdown processing

**⚡ System role and ecosystem integration:**
- **System Role**: Core template generation engine for the JESSE Framework's knowledge base indexing system, responsible for converting processed directory contexts into structured markdown knowledge files
- **Ecosystem Position**: Central component in the knowledge base generation pipeline, serving as the final output stage after content analysis and context building
- **Integration Pattern**: Used by hierarchical indexers and knowledge base managers for automated knowledge file generation, with output consumed by markdown processors and knowledge base consumers

######### Edge Cases & Error Handling

The system handles missing knowledge base files by triggering automatic rebuild with appropriate logging. Filesystem access errors during timestamp comparison default to rebuild decisions with error reason logging. Portable path conversion failures fall back to directory name with warning logging. Template generation errors are caught and wrapped in `RuntimeError` with detailed error context. File processing handles non-existent files, permission errors, and invalid file types through extension filtering and existence checks. Empty content scenarios generate placeholder text rather than failing, ensuring consistent knowledge file structure. The three-trigger change detection system handles edge cases where filesystem timestamps may be unreliable by defaulting to rebuild decisions. Error logging provides detailed context including file paths, timestamps, and operation context for debugging and maintenance.

########## Internal Implementation Details

The class maintains no internal state between operations, relying on method parameters for all generation context. Timestamp comparison uses floating-point precision with two decimal places for logging clarity. File extension filtering uses a comprehensive set covering 40+ file types including source code, documentation, configuration, and script files. Template generation uses list-based content assembly with join operations for efficient string building. Portable path generation includes trailing slash detection and platform-specific path separator handling. Knowledge base file naming follows `{directory_name}_kb.md` convention with placement in parent directory. Metadata footer generation includes accurate file and subdirectory counts with generation timestamps. The system preserves original content formatting through direct string insertion without parsing or transformation operations.

########### Code Usage Examples

**Basic knowledge file generation from directory context:**
```python
generator = KnowledgeFileGenerator()
kb_path = Path("project_kb.md")
content = generator.generate_complete_knowledge_file(
    directory_path=Path("src/"),
    global_summary="Project source code directory",
    file_contexts=[file_context1, file_context2],
    subdirectory_summaries=[(Path("utils/"), "Utility functions")],
    kb_file_path=kb_path
)
```

**Change detection for rebuild decisions:**
```python
needs_rebuild, reason = generator.directory_needs_rebuild(
    directory_path=Path("src/"),
    kb_file_path=Path("src_kb.md")
)
if needs_rebuild:
    logger.info(f"Rebuilding knowledge base: {reason}")
```

**File processing filter usage:**
```python
processable_files = [
    f for f in directory_path.iterdir() 
    if generator._should_process_file(f)
]
```
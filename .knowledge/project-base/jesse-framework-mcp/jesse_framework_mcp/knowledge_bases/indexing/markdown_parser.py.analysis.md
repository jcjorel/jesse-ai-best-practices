<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/markdown_parser.py -->
<!-- Cached On: 2025-07-04T17:15:56.135774 -->
<!-- Source Modified: 2025-07-03T00:12:24.833355 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements AST-based markdown parsing and manipulation using `mistletoe` for reliable document structure understanding and safe content editing without fragile placeholder-based approaches. It provides header-based section identification, content insertion, replacement, and spacing preservation capabilities for existing markdown files. The system enables safe editing of knowledge base files through structural manipulation rather than text-based search and replace. Key semantic entities include `MarkdownParser` class, `mistletoe.Document` AST representation, `mistletoe.block_token.Heading` for header detection, `mistletoe.markdown_renderer.MarkdownRenderer` for output generation, `enhance_tokens_with_blank_lines` spacing helper, `render_with_spacing_preservation` formatting utility, and integration with `...helpers.mistletoe_spacing` module. The parser leverages `mistletoe` line_number attributes for spacing-aware document manipulation preserving original LLM formatting patterns.

##### Main Components

The file contains the `MarkdownParser` class as the primary component providing comprehensive markdown document manipulation capabilities. Core methods include `parse_file` and `parse_content` for document loading, `parse_content_with_spacing_enhancement` for LLM content processing, `find_header_by_text` for header location, `get_section_content` for content extraction, `insert_content_after_header` and `replace_section_content` for content modification, `replace_multiple_sections` for batch operations, `extract_section_content_as_text` for content inspection, and rendering methods `render_to_markdown` and `render_to_markdown_with_spacing`. Supporting methods include `find_available_headers` for document analysis, `analyze_spacing_patterns` for formatting preservation, and `validate_document_structure` for integrity checking.

###### Architecture & Design

The architecture follows AST-based parsing principles using `mistletoe` for reliable markdown structure understanding and manipulation. The design separates parsing logic from content generation through clean interfaces supporting maintainable markdown editing operations. It implements header-based section identification enabling precise content targeting without fragile text matching. The system uses token-level manipulation preserving document structure and formatting during modifications. Error handling provides graceful fallbacks preventing document corruption during parsing failures. The design incorporates spacing-aware rendering using line_number attributes for original formatting preservation. Content manipulation operates at the AST level ensuring valid markdown structure and CommonMark compliance.

####### Implementation Approach

The implementation uses `mistletoe.Document` parsing for complete AST representation enabling structural content manipulation. Header detection traverses document children searching for `Heading` tokens with text content matching. Section boundary detection identifies content scope by finding next header of same or higher level. Content insertion and replacement operate through AST token manipulation maintaining proper parent-child relationships. Spacing preservation analyzes `line_number` attributes calculating blank line patterns from line gaps between consecutive tokens. Batch section updates process multiple replacements maintaining document indexing consistency. Text extraction renders section tokens to markdown for content inspection and validation. The system implements token-by-token rendering with manual spacing insertion for precise formatting control.

######## External Dependencies & Integration Points

**→ Inbound:**
- `mistletoe` (external library) - AST-based markdown parsing and rendering library
- `mistletoe.Document` (external library) - Complete document AST representation
- `mistletoe.block_token.Heading` (external library) - Header token structure for section identification
- `mistletoe.block_token.Paragraph` (external library) - Paragraph token handling for content manipulation
- `mistletoe.block_token.BlockToken` (external library) - Base block token interface
- `mistletoe.span_token.RawText` (external library) - Text content extraction from tokens
- `mistletoe.markdown_renderer.MarkdownRenderer` (external library) - AST to markdown conversion
- `...helpers.mistletoe_spacing:enhance_tokens_with_blank_lines` - Spacing enhancement for LLM content
- `...helpers.mistletoe_spacing:render_with_spacing_preservation` - Spacing-aware rendering utility
- `...helpers.mistletoe_spacing:preserve_llm_spacing` - LLM formatting preservation helper
- `pathlib.Path` (external library) - Cross-platform file operations
- `logging` (external library) - Error reporting and debugging information

**← Outbound:**
- Knowledge base generation systems - Provides markdown parsing and manipulation for content editing
- Template engines - Supplies document structure analysis and section replacement capabilities
- Content validation systems - Offers section extraction and document integrity checking
- Spacing preservation workflows - Delivers formatting-aware rendering for LLM-generated content

**⚡ System role and ecosystem integration:**
- **System Role**: Core markdown processing engine for the Jesse Framework MCP knowledge base system, enabling safe structural editing of existing markdown files without placeholder dependencies
- **Ecosystem Position**: Central to knowledge base maintenance workflows, providing the foundation for content updates, section replacements, and document structure preservation
- **Integration Pattern**: Used by knowledge builders and template generators requiring reliable markdown manipulation, while consuming mistletoe parsing capabilities and spacing preservation helpers for comprehensive document processing

######### Edge Cases & Error Handling

The system handles file reading errors through `FileNotFoundError` catching and graceful None returns enabling fallback processing strategies. Parsing exceptions during `mistletoe.Document` creation are caught with detailed error logging preventing workflow disruption. Header search operations return None when target headers are not found supporting conditional processing logic. Section boundary detection handles documents without proper header hierarchy through empty list returns. Content insertion failures are isolated preventing document corruption through transaction-like error handling. Spacing analysis handles tokens without `line_number` attributes through default spacing fallbacks. Token text extraction handles various token structures including nested formatting through multiple extraction strategies. Document structure validation checks parent-child relationships and header level constraints preventing invalid AST manipulation. Rendering failures fall back to standard markdown output ensuring content is never lost during processing.

########## Internal Implementation Details

The `MarkdownParser` class maintains no persistent state, operating as a stateless service for document manipulation operations. The `_extract_text_from_token` method directly accesses `_children[0].content` for headers containing single `RawText` children, with fallback approaches for complex token structures. Spacing analysis in `analyze_spacing_patterns` creates gap mappings from consecutive token `line_number` differences calculating blank line positions. The `_calculate_appropriate_spacing` method uses token type analysis determining context-aware spacing between headers, paragraphs, and other block elements. Section replacement in `replace_section_content` removes existing tokens in reverse order maintaining proper indexing during AST modification. Multiple section updates process replacements in document order preventing index corruption during batch operations. Document validation checks token parent relationships and header level constraints ensuring AST integrity. Rendering with spacing preservation manually calculates blank lines from line number gaps inserting appropriate newlines between rendered tokens.

########### Code Usage Examples

**Basic document parsing and header detection:**
```python
# Parse markdown file and find specific header for content manipulation
parser = MarkdownParser()
doc = parser.parse_file(Path("knowledge_base.md"))
header = parser.find_header_by_text(doc, "Implementation Details")
```

**Section content replacement with spacing preservation:**
```python
# Replace section content while preserving original LLM formatting patterns
new_content = "## Updated Implementation\nNew content with proper formatting"
updated_doc = parser.replace_section_content(doc, "Implementation Details", new_content)
markdown_output = parser.render_to_markdown_with_spacing(updated_doc)
```

**Batch section updates for multiple content changes:**
```python
# Update multiple sections in single operation maintaining document structure
section_updates = {
    "Architecture Overview": "## New Architecture\nUpdated architectural description",
    "Usage Examples": "## Updated Examples\nNew code examples and patterns"
}
updated_doc = parser.replace_multiple_sections(doc, section_updates)
```

**Content extraction and document analysis:**
```python
# Extract section content for validation and analyze document structure
section_text = parser.extract_section_content_as_text(doc, "Error Handling")
available_headers = parser.find_available_headers(doc)
is_valid = parser.validate_document_structure(doc)
```
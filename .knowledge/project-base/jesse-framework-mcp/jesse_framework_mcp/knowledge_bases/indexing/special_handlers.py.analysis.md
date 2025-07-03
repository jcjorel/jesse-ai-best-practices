<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/special_handlers.py -->
<!-- Cached On: 2025-07-04T00:53:59.920144 -->
<!-- Source Modified: 2025-07-01T12:17:43.646230 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements an AST-based markdown parser using the `mistletoe` library for reliable document structure manipulation and header-based editing capabilities within the JESSE Framework MCP knowledge base system. The parser provides safe content editing of existing markdown files without relying on fragile placeholder-based approaches, enabling precise section identification and content replacement while preserving document formatting and structure. Key semantic entities include `MarkdownParser` class for document manipulation, `mistletoe.Document` for AST representation, `mistletoe.block_token.Heading` for header detection, `MarkdownRenderer` for content output, `enhance_tokens_with_blank_lines()` function for spacing preservation, `render_with_spacing_preservation()` function for enhanced rendering, `parse_file()` and `parse_content()` methods for document parsing, `find_header_by_text()` method for section targeting, `replace_section_content()` method for content replacement, and comprehensive spacing analysis methods evidenced by `analyze_spacing_patterns()` and `_calculate_appropriate_spacing()` implementations.

##### Main Components

Contains `MarkdownParser` class as the primary document manipulation orchestrator with initialization, parsing, and editing methods. Implements core parsing methods including `parse_file()` for file-based document loading, `parse_content()` for string-based parsing, and `parse_content_with_spacing_enhancement()` for LLM content processing. Provides header manipulation methods including `find_header_by_text()` for section targeting, `find_available_headers()` for document structure analysis, and `_extract_text_from_token()` for content extraction. Includes content manipulation methods such as `replace_section_content()` for section replacement, `insert_content_after_header()` for content addition, and `replace_multiple_sections()` for batch operations. Implements spacing analysis capabilities through `analyze_spacing_patterns()` and `_calculate_appropriate_spacing()` methods for formatting preservation.

###### Architecture & Design

Implements AST-based parsing architecture using `mistletoe` library for robust document structure understanding and manipulation without string-based fragility. Uses header-based section identification pattern enabling precise content targeting through document structure rather than placeholder markers. Employs spacing-aware rendering system leveraging `line_number` attributes from `mistletoe` tokens for original formatting preservation. Integrates with spacing enhancement utilities from `mistletoe_spacing` helper module for consistent blank line handling across the knowledge base system. Follows separation of concerns design with distinct methods for parsing, manipulation, and rendering operations enabling modular usage patterns.

####### Implementation Approach

Uses `mistletoe.Document` parsing for complete AST representation enabling structural manipulation without text-based parsing fragility. Implements header traversal algorithms using token iteration and type checking for precise section boundary detection. Employs line-number-aware spacing analysis calculating blank line patterns from `line_number` attribute differences between consecutive tokens. Uses token-by-token rendering approach with manual spacing insertion for precise formatting control during document reconstruction. Implements defensive programming patterns with comprehensive error handling and graceful fallbacks preventing document corruption during manipulation operations.

######## Code Usage Examples

Parse markdown content and manipulate document structure using AST-based operations. This demonstrates the fundamental parsing and manipulation workflow:

```python
parser = MarkdownParser()
doc = parser.parse_content("# Header\nContent here")
if doc:
    updated_doc = parser.replace_section_content(doc, "Header", "New content")
    result = parser.render_to_markdown(updated_doc)
```

Find and analyze document headers for section-based content management. This shows header detection and structure analysis capabilities:

```python
headers = parser.find_available_headers(doc)
for header in headers:
    print(f"Level {header['level']}: {header['text']}")
    section_content = parser.extract_section_content_as_text(doc, header['text'])
```

Perform spacing-aware content replacement preserving original document formatting. This demonstrates advanced formatting preservation during content manipulation:

```python
enhanced_doc = parser.parse_content_with_spacing_enhancement(llm_content)
spacing_map = parser.analyze_spacing_patterns(doc)
updated_doc = parser.replace_section_content(doc, "Section", new_content)
final_markdown = parser.render_to_markdown_with_spacing(updated_doc)
```

######### External Dependencies & Integration Points

**→ Inbound:**

- `mistletoe` (external library) - AST-based markdown parsing and rendering library for document structure manipulation
- `mistletoe.Document` (external library) - core document AST representation for markdown structure
- `mistletoe.block_token.Heading` (external library) - header token representation for section identification
- `mistletoe.markdown_renderer.MarkdownRenderer` (external library) - AST-to-markdown conversion for output generation
- `helpers.mistletoe_spacing.enhance_tokens_with_blank_lines` - spacing enhancement utilities for formatting preservation
- `helpers.mistletoe_spacing.render_with_spacing_preservation` - enhanced rendering with spacing awareness
- `pathlib.Path` (standard library) - cross-platform file operations and path handling
- `typing.List, Dict, Any, Optional, Union` (standard library) - type annotations for method signatures
- `logging` (standard library) - error reporting and debugging information

**← Outbound:**

- `markdown_template_engine.MarkdownTemplateEngine` - consumes parser for template-based content manipulation
- `knowledge_builder.KnowledgeBuilder` - uses parser for LLM content processing and document assembly
- Knowledge base processing workflows - systems that manipulate markdown documents through parser interface
- Template rendering systems - components that use parser for structured content generation

**⚡ Integration:**

- Protocol: Direct Python imports with class-based interface and method calls
- Interface: Class methods returning `mistletoe.Document` objects and markdown strings
- Coupling: Tight coupling with `mistletoe` library, loose coupling with knowledge base components through clean interfaces

########## Edge Cases & Error Handling

Handles malformed markdown documents through comprehensive parsing error catching with graceful fallbacks returning `None` for failed operations. Addresses missing headers during section operations by logging warnings and returning appropriate default values preventing processing failures. Manages complex token structures during text extraction through multiple fallback strategies accessing different token attributes and child collections. Handles spacing analysis failures during line number processing by providing safe default spacing values and continuing document processing. Addresses rendering failures through fallback to standard `mistletoe` rendering when spacing-aware rendering encounters errors.

########### Internal Implementation Details

Uses `mistletoe.Document` constructor for AST parsing with automatic token hierarchy creation and parent-child relationship establishment. Implements direct token attribute access through `_children[0].content` pattern for efficient header text extraction from `RawText` tokens. Maintains spacing information through `line_number` attribute analysis calculating blank line positions from consecutive token line number differences. Uses temporary document creation for individual token rendering enabling precise control over output formatting and spacing preservation. Implements token position tracking through document children list indexing for accurate section boundary detection and content replacement operations.
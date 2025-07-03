<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/markdown_parser.py -->
<!-- Cached On: 2025-07-04T00:55:09.085977 -->
<!-- Source Modified: 2025-07-03T00:12:24.833355 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements an AST-based markdown parser using the `mistletoe` library for reliable document structure manipulation and header-based editing capabilities within the JESSE Framework MCP knowledge base system. The parser provides safe content editing of existing markdown files without relying on fragile placeholder-based approaches, enabling precise section identification and content replacement while preserving document formatting and structure. Key semantic entities include `MarkdownParser` class for document manipulation, `mistletoe.Document` for AST representation, `mistletoe.block_token.Heading` for header detection, `MarkdownRenderer` for content output, `enhance_tokens_with_blank_lines()` function for spacing preservation, `render_with_spacing_preservation()` function for enhanced rendering, `parse_file()` and `parse_content()` methods for document parsing, `find_header_by_text()` method for section targeting, `replace_section_content()` method for content replacement, and comprehensive spacing analysis methods evidenced by `analyze_spacing_patterns()` and `_calculate_appropriate_spacing()`.

##### Main Components

Contains `MarkdownParser` class as the primary document manipulation orchestrator with initialization, parsing, and editing methods. Implements core parsing methods including `parse_file()` for file-based parsing, `parse_content()` for string-based parsing, and `parse_content_with_spacing_enhancement()` for LLM content processing. Provides header manipulation methods including `find_header_by_text()` for section targeting, `get_section_content()` for content extraction, and `find_available_headers()` for document structure analysis. Includes content modification methods including `insert_content_after_header()`, `replace_section_content()`, `replace_multiple_sections()`, and `extract_section_content_as_text()`. Implements rendering methods including `render_to_markdown()` and `render_to_markdown_with_spacing()` for document output with spacing preservation capabilities.

###### Architecture & Design

Implements AST-based parsing architecture using `mistletoe` library for robust document structure understanding and manipulation without string-based fragile approaches. Uses header-based section identification enabling precise content targeting through `Heading` token analysis and text matching algorithms. Employs spacing-aware document manipulation leveraging `line_number` attributes from `mistletoe` tokens for original formatting preservation. Integrates with spacing enhancement utilities through `enhance_tokens_with_blank_lines()` and `render_with_spacing_preservation()` functions for consistent formatting. Follows separation of concerns with distinct methods for parsing, manipulation, and rendering operations enabling clean integration with template engines and content generation systems.

####### Implementation Approach

Uses `mistletoe.Document` parsing for complete AST representation enabling reliable structure manipulation through token-based operations. Implements header traversal algorithms using `isinstance(token, Heading)` checks and text extraction through `_extract_text_from_token()` method for precise section identification. Employs line-number-aware spacing analysis through `analyze_spacing_patterns()` method calculating gaps between consecutive tokens using `line_number` attributes. Uses section boundary detection through header level comparison ensuring proper content scope identification during replacement operations. Implements batch processing capabilities through `replace_multiple_sections()` method optimizing performance for multiple content updates while maintaining document integrity.

######## Code Usage Examples

Parse markdown content and manipulate document structure using AST-based operations. This demonstrates the fundamental parsing and document manipulation workflow:

```python
parser = MarkdownParser()
doc = parser.parse_content(markdown_content)
if doc:
    # Find and manipulate specific sections
    header = parser.find_header_by_text(doc, "Architecture & Design")
    section_content = parser.get_section_content(doc, header)
```

Replace section content while preserving original formatting and spacing patterns. This shows advanced content replacement with spacing-aware rendering:

```python
updated_doc = parser.replace_section_content(
    doc, "Implementation Details", new_content
)
if updated_doc:
    final_markdown = parser.render_to_markdown_with_spacing(updated_doc)
```

Perform batch section updates for efficient document modification operations. This demonstrates multiple section replacement in a single operation:

```python
section_updates = {
    "Overview": "Updated overview content",
    "Technical Details": "Updated technical content"
}
updated_doc = parser.replace_multiple_sections(doc, section_updates)
```

######### External Dependencies & Integration Points

**→ Inbound:**

- `mistletoe` (external library) - AST-based markdown parsing and rendering with complete document structure support
- `mistletoe.Document` (external library) - document AST representation for structure manipulation
- `mistletoe.block_token.Heading` (external library) - header token identification and level analysis
- `mistletoe.span_token.RawText` (external library) - text content extraction from token structures
- `mistletoe.markdown_renderer.MarkdownRenderer` (external library) - AST-to-markdown conversion
- `helpers.mistletoe_spacing.enhance_tokens_with_blank_lines` - spacing enhancement for LLM content
- `helpers.mistletoe_spacing.render_with_spacing_preservation` - spacing-aware rendering utilities
- `pathlib.Path` (standard library) - cross-platform file operations and path handling
- `typing.List, Dict, Any, Optional, Union` (standard library) - type annotations for method signatures
- `logging` (standard library) - error reporting and debugging information

**← Outbound:**

- `markdown_template_engine.MarkdownTemplateEngine` - consumes parser for template-based content manipulation
- `knowledge_builder.KnowledgeBuilder` - uses parser for LLM content integration and formatting
- Knowledge base maintenance systems - tools that leverage parser for document structure analysis
- Content validation workflows - systems that use parser for markdown structure verification

**⚡ Integration:**

- Protocol: Direct Python imports with class instantiation and method calls
- Interface: Class methods returning `Document` objects and markdown strings with error handling
- Coupling: Tight coupling with `mistletoe` library, loose coupling with knowledge base components

########## Edge Cases & Error Handling

Handles parsing failures gracefully through comprehensive exception catching returning `None` for failed operations enabling fallback processing strategies. Addresses malformed markdown documents through `mistletoe` parser error handling and document structure validation preventing corruption during manipulation. Manages missing headers during section operations through `find_header_by_text()` returning `None` and appropriate error logging for debugging. Handles complex token structures during text extraction through multiple fallback approaches in `_extract_text_from_token()` method ensuring content accessibility. Addresses spacing analysis failures through defensive programming in `analyze_spacing_patterns()` with empty dictionary fallback preventing rendering issues.

########### Internal Implementation Details

Uses `mistletoe.Document` constructor for AST parsing with automatic token hierarchy creation and parent-child relationship establishment. Implements direct token access through `_children[0].content` pattern for header text extraction avoiding complex recursion that could cause reference issues. Maintains spacing information through `line_number` attribute analysis calculating gaps between consecutive tokens for blank line preservation. Uses token position tracking through `doc.children.index()` operations for precise content insertion and replacement operations. Implements temporary document creation for individual token rendering through `type(doc)([])` pattern enabling isolated content processing without affecting main document structure.
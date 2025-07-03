<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/file_analysis_cache.py -->
<!-- Cached On: 2025-07-04T00:43:39.023668 -->
<!-- Source Modified: 2025-07-03T17:40:33.712319 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements enhanced LLM prompts for the JESSE Framework MCP knowledge base system, providing specialized prompt templates for hierarchical semantic tree generation with architectural analysis focus. The system delivers structured prompts for file analysis, directory analysis, and global summary generation while emphasizing design patterns, technical implementation details, and token-efficient content generation. Key semantic entities include `EnhancedPrompts` class for prompt orchestration, `SEMANTIC_ENTITY_USAGE_SPEC` specification for technical entity highlighting, `LEVEL_9_FORMATTING_SPEC` for dependency formatting standardization, `file_analysis_prompt` template for individual file processing, `directory_analysis_prompt` template for hierarchical directory analysis, `global_summary_prompt` template for system-wide synthesis, reviewer prompt templates for structural compliance validation, and `get_portable_path()` integration for cross-platform compatibility evidenced by methods like `get_file_analysis_prompt()`, `get_directory_analysis_prompt()`, and comprehensive reviewer prompt generation methods.

##### Main Components

Contains `EnhancedPrompts` class as the primary prompt container with initialization and prompt generation methods. Includes class variables `SEMANTIC_ENTITY_USAGE_SPEC` and `LEVEL_9_FORMATTING_SPEC` providing reusable specifications following DRY principles. Implements core prompt templates including `file_analysis_prompt`, `directory_analysis_prompt`, and `global_summary_prompt` for content generation. Provides reviewer prompt templates including `file_analysis_reviewer_prompt`, `directory_analysis_reviewer_prompt`, and `global_summary_reviewer_prompt` for structural compliance validation. Implements getter methods for each prompt type with portable path support and error handling capabilities.

###### Architecture & Design

Implements template-based prompt architecture with reusable specification components and DRY principle adherence. Uses f-string interpolation for dynamic content insertion and specification integration across all prompt templates. Employs structured response format requirements ensuring compatibility with `FileAnalysis` and `DirectorySummary` dataclasses. Integrates portable path utilities through `get_portable_path()` function for cross-platform compatibility. Follows separation of concerns with distinct prompt types for different analysis scenarios and dedicated reviewer prompts for quality assurance.

####### Implementation Approach

Uses comprehensive prompt templates with embedded hierarchical semantic tree specifications and formatting requirements. Implements reusable specification variables preventing duplication and ensuring consistency across all prompt types. Employs structured template formatting with clear section delineation and mandatory response validation requirements. Uses defensive programming with comprehensive error handling and fallback mechanisms for portable path conversion. Implements token efficiency optimization through focused analysis prompts and structured response formats.

######## Code Usage Examples

Initialize the enhanced prompts system for comprehensive LLM prompt generation. This establishes the foundation for all prompt template operations:

```python
prompts = EnhancedPrompts()
```

Generate a file analysis prompt with architectural focus and portable path support. This creates structured prompts for individual file processing with technical depth requirements:

```python
file_prompt = prompts.get_file_analysis_prompt(
    file_path=Path("/project/src/module.py"),
    file_content="class Example: pass",
    file_size=1024
)
```

Generate a directory analysis prompt for hierarchical processing with child content integration. This demonstrates comprehensive directory analysis with architectural emphasis:

```python
directory_prompt = prompts.get_directory_analysis_prompt(
    directory_path=Path("/project/src/"),
    file_count=15,
    subdirectory_count=3,
    child_content_summary="Module contains core classes and utilities"
)
```

######### External Dependencies & Integration Points

**→ Inbound:**

- `helpers.path_utils.get_portable_path` - cross-platform path conversion for prompt compatibility
- `pathlib.Path` (standard library) - cross-platform path operations and metadata handling
- `typing.Dict, Any, List` (standard library) - type hints for prompt parameters and structures
- `logging` (standard library) - structured logging for prompt generation operations

**← Outbound:**

- `knowledge_builder.KnowledgeBuilder` - consumes enhanced prompts for LLM-powered content generation
- `markdown_template_engine.FileAnalysis` - dataclass structure compatibility for prompt responses
- `markdown_template_engine.DirectorySummary` - dataclass structure compatibility for directory analysis
- LLM processing systems - consume generated prompts for hierarchical semantic tree generation
- Quality assurance workflows - use reviewer prompts for structural compliance validation

**⚡ Integration:**

- Protocol: Direct Python imports and method calls with structured prompt templates
- Interface: Class methods returning formatted prompt strings with embedded specifications
- Coupling: Loose coupling through string template interfaces and portable path utilities

########## Edge Cases & Error Handling

Handles portable path conversion failures through comprehensive fallback mechanisms using original paths with detailed logging. Addresses prompt generation failures with structured error handling and informative exception messages. Manages missing or invalid file content scenarios through defensive programming and parameter validation. Implements comprehensive error logging throughout all prompt generation methods preventing silent failures. Provides graceful degradation when portable path utilities are unavailable while maintaining core functionality.

########### Internal Implementation Details

Uses f-string interpolation for dynamic specification integration maintaining single source of truth for formatting rules. Implements class variables for reusable specifications following DRY principle and preventing specification drift. Maintains comprehensive prompt templates with embedded hierarchical semantic tree requirements and validation rules. Uses structured error handling with specific exception types and detailed error messages for debugging. Implements consistent logging patterns across all prompt generation methods for operational monitoring and troubleshooting.
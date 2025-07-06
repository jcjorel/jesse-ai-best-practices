<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/knowledge_prompts.py -->
<!-- Cached On: 2025-07-06T11:30:41.397671 -->
<!-- Source Modified: 2025-07-05T11:28:34.701108 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file provides specialized LLM prompt templates for generating hierarchical semantic trees within the Jesse Framework MCP's knowledge base indexing system, focusing on architectural analysis and technical implementation details. The file implements comprehensive prompt engineering for different content types with token-efficient structure and programmatic content extraction capabilities. Key semantic entities include `EnhancedPrompts` class for prompt orchestration, `file_analysis_prompt` for individual file analysis, `directory_analysis_prompt` for module architecture analysis, `global_summary_prompt` for system-wide synthesis, reviewer prompts for structural compliance validation, `SEMANTIC_ENTITY_USAGE_SPEC` for technical terminology standardization, `LEVEL_8_FORMATTING_SPEC` for dependency formatting, and `get_portable_path` integration for cross-platform compatibility. The implementation emphasizes architectural focus over generic functionality descriptions, ensuring comprehensive coverage of design patterns, implementation strategies, and technical decision-making insights.

##### Main Components

The file contains the `EnhancedPrompts` class as the primary prompt container with specialized templates for different analysis scenarios. Core prompt templates include `file_analysis_prompt` for comprehensive file analysis with architectural emphasis, `directory_analysis_prompt` for module organization and design relationships, and `global_summary_prompt` for system-wide architectural synthesis. Supporting components include three reviewer prompts (`file_analysis_reviewer_prompt`, `directory_analysis_reviewer_prompt`, `global_summary_reviewer_prompt`) for structural compliance validation, shared specifications (`SEMANTIC_ENTITY_USAGE_SPEC`, `LEVEL_8_FORMATTING_SPEC`) for consistent formatting requirements, and utility methods for prompt generation with portable path support and error handling.

###### Architecture & Design

The architecture implements a template-based prompt generation system with content-type specialization and structured response format requirements. The design separates concerns through specialized prompt templates for different analysis contexts while maintaining consistent hierarchical semantic tree structure across all generated content. The component uses composition patterns with shared specification constants (`SEMANTIC_ENTITY_USAGE_SPEC`, `LEVEL_8_FORMATTING_SPEC`) to ensure DRY principles and consistent formatting requirements. The architecture includes comprehensive reviewer prompt integration for automated structural compliance checking, enabling quality assurance without manual intervention. The design emphasizes architectural analysis focus through specialized prompt engineering that prioritizes design patterns, implementation strategies, and technical depth over generic descriptions.

####### Implementation Approach

The implementation uses template string formatting with placeholder substitution for dynamic prompt generation, incorporating file metadata, content, and portable path conversion for cross-platform compatibility. The approach employs hierarchical semantic tree specification with 8 distinct levels (4-11) using markdown headers, ensuring progressive completeness without information redundancy between levels. Technical strategies include semantic entity usage specification requiring backquote formatting for technical terms, external dependencies formatting with standardized visual symbols (→, ←, ⚡), and comprehensive error handling with logging integration. The system implements reviewer prompt patterns for structural compliance validation, supporting both compliance verification and automatic correction in single operations through binary output formats.

######## External Dependencies & Integration Points

**→ Inbound:**
- `...helpers.path_utils:get_portable_path` - cross-platform path conversion for LLM prompt compatibility
- `logging` (external library) - structured logging for prompt generation operations and debugging
- `typing` (external library) - type hints for prompt template parameters and response structures
- `pathlib.Path` (external library) - modern path handling for file and directory operations

**← Outbound:**
- `jesse_framework_mcp.knowledge_bases.indexing.knowledge_file_generator` - knowledge file generator consuming prompt templates for content generation
- LLM processing systems - structured prompts for hierarchical semantic tree generation
- Knowledge base storage systems - generated analysis content following hierarchical semantic tree structure
- Template engine operations - programmatic content extraction and markdown integration

**⚡ System role and ecosystem integration:**

- **System Role**: This component serves as the prompt engineering foundation for the Jesse Framework MCP knowledge base system, providing specialized LLM templates that generate structured architectural analysis content
- **Ecosystem Position**: Core infrastructure component within the knowledge indexing architecture, essential for generating consistent, high-quality technical documentation through LLM processing
- **Integration Pattern**: Used by knowledge file generators and indexing workflows to create structured prompts for LLM analysis, with reviewer prompts ensuring consistent formatting compliance across all generated knowledge base content

######### Edge Cases & Error Handling

The prompt generation system handles comprehensive error scenarios including portable path conversion failures with fallback to original paths, prompt template formatting errors with detailed exception logging, and reviewer prompt generation failures with runtime error propagation. Error handling implements individual operation isolation through try-catch blocks around each prompt generation method, preventing single failures from affecting overall prompt system functionality. The system manages edge cases like missing file content, invalid directory structures, and malformed assembled content through defensive programming patterns and comprehensive logging. Recovery mechanisms include graceful degradation for path conversion failures, detailed error messages for debugging prompt generation issues, and comprehensive exception handling with proper error propagation for integration debugging.

########## Internal Implementation Details

Internal mechanisms include template string formatting with named placeholders for dynamic content insertion, portable path conversion integration using `get_portable_path()` for cross-platform compatibility, and comprehensive logging integration for debugging and monitoring prompt generation operations. The `EnhancedPrompts` class initializes with all prompt templates as instance attributes, enabling efficient reuse and consistent formatting across multiple prompt generation calls. Prompt templates include extensive specification sections for hierarchical semantic tree structure, semantic entity usage requirements, and external dependencies formatting with standardized visual symbols. The implementation uses f-string formatting for specification injection into prompt templates, ensuring DRY principles and consistent formatting requirements across all generated prompts.

########### Code Usage Examples

Basic prompt generation demonstrates comprehensive file analysis with architectural focus. This pattern shows how to initialize the prompt system and generate structured analysis prompts for LLM processing.

```python
# Initialize enhanced prompts with architectural analysis templates
prompts = EnhancedPrompts()

# Generate file analysis prompt with portable path support
file_prompt = prompts.get_file_analysis_prompt(
    file_path=Path("src/module.py"),
    file_content=file_content,
    file_size=1024
)

# Process with LLM for hierarchical semantic tree generation
analysis_result = await llm_client.generate(file_prompt)
```

Directory analysis prompt generation shows module architecture focus. This approach enables comprehensive analysis of directory structures and component relationships within the codebase.

```python
# Generate directory analysis prompt with child content synthesis
directory_prompt = prompts.get_directory_analysis_prompt(
    directory_path=Path("src/components/"),
    file_count=15,
    subdirectory_count=3,
    child_content_summary=assembled_child_content
)

# Process for comprehensive module architecture analysis
directory_analysis = await llm_client.generate(directory_prompt)
```

Reviewer prompt integration enables automated structural compliance checking. This pattern ensures consistent formatting across all generated knowledge base content through automated validation and correction.

```python
# Generate reviewer prompt for structural compliance validation
reviewer_prompt = prompts.get_file_analysis_reviewer_prompt(generated_output)

# Process for automatic formatting correction
review_result = await llm_client.generate(reviewer_prompt)

# Handle compliance result (either "COMPLIANT" or corrected version)
if review_result == "COMPLIANT":
    final_content = generated_output
else:
    final_content = review_result
```
<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/enhanced_prompts.py -->
<!-- Cached On: 2025-07-05T13:04:05.657682 -->
<!-- Source Modified: 2025-07-05T11:28:34.701108 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file provides specialized LLM prompt templates for generating hierarchical semantic trees within the JESSE Framework Knowledge Bases Hierarchical Indexing System, focusing on architectural analysis and design pattern extraction. The file enables structured knowledge base generation through the `EnhancedPrompts` class which contains prompt templates for file analysis, directory analysis, global summaries, and structural compliance review. Key semantic entities include `EnhancedPrompts` class for prompt management, `file_analysis_prompt` template for individual file processing, `directory_analysis_prompt` template for module organization analysis, `global_summary_prompt` template for system-wide synthesis, reviewer prompt templates for quality assurance, `get_portable_path()` function for cross-platform path compatibility, `logging` module for operational tracking, and `pathlib.Path` for modern path handling. The technical architecture implements a hierarchical semantic tree specification with 8 levels (headers 4-11) ensuring progressive knowledge loading from high-level purpose to detailed implementation specifics.

##### Main Components

The file contains the `EnhancedPrompts` class with six primary prompt template attributes: `file_analysis_prompt` for individual file architectural analysis, `directory_analysis_prompt` for module organization and design relationships, `global_summary_prompt` for system-wide architectural synthesis, `file_analysis_reviewer_prompt` for structural compliance checking, `directory_analysis_reviewer_prompt` for directory analysis validation, and `global_summary_reviewer_prompt` for global summary compliance verification. The class includes two shared specification constants: `SEMANTIC_ENTITY_USAGE_SPEC` defining technical entity naming requirements and `LEVEL_8_FORMATTING_SPEC` standardizing external dependency documentation format. Six public methods provide formatted prompt generation: `get_file_analysis_prompt()`, `get_directory_analysis_prompt()`, `get_global_summary_prompt()`, and three corresponding reviewer prompt methods for quality assurance validation.

###### Architecture & Design

The architecture follows a template-based prompt generation pattern with shared specification components ensuring consistency across all prompt types. The design implements a hierarchical semantic tree specification with strict level organization (4-11) and no-redundancy rules between levels, enabling progressive knowledge loading based on developer needs. The class uses composition over inheritance with shared specification constants (`SEMANTIC_ENTITY_USAGE_SPEC`, `LEVEL_8_FORMATTING_SPEC`) applied across all prompt templates through string formatting. The reviewer pattern implements structural compliance checking with binary output (COMPLIANT/corrected version) for automated quality assurance. The portable path integration ensures cross-platform compatibility through `get_portable_path()` function usage in all path-related prompt generation.

####### Implementation Approach

The implementation uses Python string formatting with template placeholders (`{file_path}`, `{file_content}`, `{directory_path}`, `{assembled_content}`) for dynamic prompt generation. Error handling employs try-catch blocks with fallback to original paths when portable path conversion fails, ensuring robust operation across different environments. The prompt templates include comprehensive formatting specifications with markdown header requirements (####-###########), code snippet formatting rules with language identifiers, and directory name trailing slash requirements. The class initialization logs successful setup and each method logs debug information for operational tracking. The reviewer prompts implement structural-only validation with explicit scope limitations preventing semantic assessment while ensuring formatting compliance.

######## External Dependencies & Integration Points

**→ Inbound:**
- `jesse_framework_mcp.helpers.path_utils:get_portable_path` - cross-platform path conversion for prompt compatibility
- `logging` (external library) - operational tracking and debug information for prompt generation
- `typing.Dict` (external library) - type hints for method parameters and return values
- `typing.Any` (external library) - flexible type annotations for prompt template parameters
- `typing.List` (external library) - type annotations for collection parameters
- `pathlib.Path` (external library) - modern path handling for file and directory operations

**← Outbound:**
- `jesse_framework_mcp.knowledge_bases.indexing.knowledge_builder:KnowledgeBuilder` - consumes generated prompts for LLM processing
- `jesse_framework_mcp.knowledge_bases.indexing.hierarchical_indexer:HierarchicalIndexer` - uses prompts for directory structure analysis
- `LLM processing systems` - consume formatted prompts for hierarchical semantic tree generation
- `knowledge base files` - generated content follows prompt specifications for structured knowledge storage

**⚡ System role and ecosystem integration:**
- **System Role**: Core prompt template provider for JESSE Framework Knowledge Bases Hierarchical Indexing System, defining the structured analysis approach for all knowledge generation
- **Ecosystem Position**: Central component that standardizes knowledge extraction methodology across file analysis, directory analysis, and global summary generation workflows
- **Integration Pattern**: Used by knowledge building components during indexing operations, LLM processing systems for structured analysis, and quality assurance systems for compliance validation

######### Edge Cases & Error Handling

Error handling includes portable path conversion failures with graceful fallback to original paths and warning logging, ensuring prompt generation continues even when cross-platform path conversion encounters issues. The implementation handles missing or invalid file content through template parameter validation and comprehensive error logging with specific failure context. Prompt generation failures raise `RuntimeError` with detailed error context for debugging and operational monitoring. The reviewer prompts handle truncation detection through mandatory end-of-output markers, returning "TRUNCATED" when output is incomplete. Template formatting errors are caught and re-raised with enhanced context information including the specific prompt type and parameters that caused the failure.

########## Internal Implementation Details

The class uses class-level constants for shared specifications to implement DRY principles and ensure consistency across all prompt templates. String formatting employs Python's `str.format()` method with named placeholders for clear parameter mapping and maintainable template structure. The logging implementation uses module-level logger with debug-level messages for operational tracking without performance impact in production. Error handling uses chained exceptions (`raise ... from e`) to preserve original error context while providing enhanced debugging information. The portable path integration includes exception handling with fallback behavior, ensuring robust operation when path conversion utilities encounter filesystem or permission issues. Template validation occurs during formatting with immediate error reporting for missing or invalid parameters.

########### Code Usage Examples

Basic file analysis prompt generation demonstrates the standard workflow for creating structured analysis prompts. This pattern provides the foundation for all file-based knowledge extraction in the indexing system.

```python
# Generate file analysis prompt with portable path support
enhanced_prompts = EnhancedPrompts()
file_path = Path("src/components/Button.tsx")
file_content = "export default function Button() { return <button>Click</button>; }"
file_size = len(file_content.encode('utf-8'))

prompt = enhanced_prompts.get_file_analysis_prompt(
    file_path=file_path,
    file_content=file_content,
    file_size=file_size
)
# Returns formatted prompt ready for LLM processing with hierarchical structure requirements
```

Directory analysis prompt generation enables module-level architectural analysis with child content integration. This approach supports bottom-up knowledge building from individual files to complete system understanding.

```python
# Generate directory analysis prompt with child content summary
directory_path = Path("src/components/")
file_count = 15
subdirectory_count = 3
child_content_summary = "React components with TypeScript definitions and styling"

prompt = enhanced_prompts.get_directory_analysis_prompt(
    directory_path=directory_path,
    file_count=file_count,
    subdirectory_count=subdirectory_count,
    child_content_summary=child_content_summary
)
# Returns structured prompt for hierarchical directory analysis
```

Quality assurance workflow demonstrates the reviewer pattern for ensuring structural compliance. This pattern enables automated validation and correction of generated content without manual intervention.

```python
# Quality assurance workflow with automatic compliance checking
generated_analysis = "#### Functional Intent & Features\nFile analysis content..."
reviewer_prompt = enhanced_prompts.get_file_analysis_reviewer_prompt(generated_analysis)

# LLM processes reviewer prompt and returns either "COMPLIANT" or corrected version
review_result = llm_process(reviewer_prompt)
if review_result != "COMPLIANT":
    corrected_content = review_result  # Use corrected version
```
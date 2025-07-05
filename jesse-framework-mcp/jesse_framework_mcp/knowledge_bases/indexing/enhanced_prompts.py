###############################################################################
# IMPORTANT: This header comment is designed for GenAI code review and maintenance
# Any GenAI tool working with this file MUST preserve and update this header
###############################################################################
# [GenAI coding tool directive]
# - Maintain this header with all modifications
# - Update History section with each change
# - Keep only the 4 most recent records in the history section. Sort from newer to older.
# - Preserve Intent, Design, and Constraints sections
# - Use this header as context for code reviews and modifications
# - Ensure all changes align with the design principles
# - Respect system prompt directives at all times
###############################################################################
# [Source file intent]
# Enhanced LLM prompts for Knowledge Bases Hierarchical Indexing System focusing on
# architectural analysis, design patterns, and technical implementation details.
# Provides specialized prompts for different content types with token-efficient structure.
###############################################################################
# [Source file design principles]
# - Architectural focus emphasizing design patterns, implementation strategies, and technical decisions
# - Structured response format enabling programmatic content extraction and template integration
# - Content-type specialization providing targeted analysis for different file types and contexts
# - Token efficiency through focused analysis prompts reducing unnecessary verbose generation
# - Technical depth ensuring comprehensive coverage of implementation details and architectural insights
###############################################################################
# [Source file constraints]
# - All prompts must generate raw markdown content ready for direct insertion into knowledge files
# - Response format optimized for direct template insertion without parsing complexity
# - Prompts must emphasize architectural and technical aspects over generic functionality descriptions
# - Content must be written in present tense for intemporal knowledge representation
# - Analysis depth must be comprehensive enough for technical decision-making and code understanding
###############################################################################
# [Dependencies]
# <codebase>: .knowledge_file_generator - Knowledge file generator for template operations
# <system>: typing - Type hints for prompt template parameters and response structures
###############################################################################
# [GenAI tool change history]
# 2025-07-04T13:26:00Z : Reordered hierarchical levels moving code snippets from Level 8 to Level 11 and shifting other levels by CodeAssistant
# * Moved current Level 8 (Code snippets and usage examples) to new Level 11 for better knowledge progression
# * Shifted Level 9 (External dependencies) to Level 8, Level 10 (Edge cases) to Level 9, Level 11 (Internal implementation) to Level 10
# * Updated all prompt templates, specifications, and references to reflect new level ordering
# * Renamed LEVEL_9_FORMATTING_SPEC to LEVEL_8_FORMATTING_SPEC to match new external dependencies level
# 2025-07-04T08:36:00Z : Renamed Integration section to "System role and ecosystem integration" with enhanced consumer analysis by CodeAssistant
# * Updated Level 9 section header from "Integration" to "System role and ecosystem integration" for clearer positioning context
# * Enhanced Integration Pattern to focus on "Who is using this file and how" including humans, external processes, and codebase parts
# * Added Ecosystem Position element to identify whether components are central/core, peripheral/support, or auxiliary
# * Updated visual symbol description and all formatting specifications to reflect system role and ecosystem integration focus
# 2025-07-04T08:20:00Z : Enhanced Level 9 Integration section to require context-specific system role analysis by CodeAssistant
# * Added comprehensive Integration section requirements to eliminate generic boilerplate content
# * Enhanced LEVEL_9_FORMATTING_SPEC with context-specific content guidelines and developer actionability focus
# * Updated Integration format from generic "how connections work" to "system role and integration significance" 
# * Added explicit guidance to avoid generic statements and prefer specific system context and integration patterns
# 2025-07-04T07:23:00Z : Enhanced Level 4 to include one key technical aspect requirement using semantic entity names by CodeAssistant  
# * Updated Level 4 definition to include "and one key technical aspect (using semantic entity names)" for enhanced technical depth
# * Modified main specification in HIERARCHY DESIGN PRINCIPLES to reflect enhanced Level 4 requirement
# * Updated all three prompts (file analysis, directory analysis, global summary) header descriptions to include key technical aspect
# * Enhanced content-type guidelines for both code files and non-code files to include technical aspect requirement
# 2025-07-03T21:26:00Z : Added backquote highlighting requirement for technical entity names by CodeAssistant
# * Enhanced SEMANTIC_ENTITY_USAGE_SPEC to require backquotes (`) around all technical entity names for highlighting
# * Updated fundamental principle to mandate backquote formatting for improved visual distinction
# * Modified all examples to demonstrate proper backquote usage around technical entities
# * Applied to all hierarchical preference levels ensuring consistent technical entity highlighting
###############################################################################

"""
Enhanced LLM Prompts for Hierarchical Semantic Tree Generation.

HIERARCHICAL SEMANTIC TREE SPECIFICATION:

This module implements LLM prompts that generate hierarchical semantic trees to support
progressive knowledge loading based on developer needs. The system creates structured
content with distinct levels of detail that can be programmatically parsed and selectively
loaded depending on the required depth of knowledge.

HIERARCHY DESIGN PRINCIPLES:
---------------------------
1. **Hierarchical Structure**: Content organized in semantic levels from high-level purpose 
   to detailed implementation specifics using markdown headers 4-11 (####-###########). Headers contain
   only generic section purpose (i.e. no information about the file or directory itself). Do not follow
   markdown rules that specify that no more than 6 levels exist.

2. **No Redundancy**: Each level (n-1) contains NO overlapping information with level (n)
   - Level 4: Functional intent (WHY), features (WHAT), usage value, key semantic entities, and one key technical aspect (using semantic entity names)
   - Level 5: Main components and responsibilities  
   - Level 6: Architecture and design patterns
   - Level 7: Implementation approach, usage patterns and key algorithms
   - Level 8: External dependencies and integration points (both inbound and outbound)
   - Level 9: Edge cases, error handling, and debugging
   - Level 10: Internal implementation details and maintenance notes
   - Level 11: Code snippets and usage examples (for code files)

3. **Content-Type Differentiation**:
   - **Code Files**: Hierarchy based on developer needs from "why exists" to "code snippets 
     for essential features" to complete implementation understanding
   - **Non-Code Files**: Hierarchy based on logical information depth and contextual relevance

4. **Programmatic Parsing**: Output structured for automated parsing tools to extract specific
   detail levels based on knowledge requirements

5. **Progressive Loading**: Each level provides complete context at its depth without requiring
   higher detail levels, enabling selective knowledge loading
   
6. **Intemporal Representation**: Content written in present tense to represent knowledge

7. Global Summary prompt must follow the same hierarchical structure and rules 

8. **Never state the obvious!**: Avoid stating information and best practices known by any modern AI LLM. Focus on
   providing unique, valuable insights at each level without redundancy.

9. Do not judge or propose enhancement about the current implementation. Focus on providing
   structured, detailed analysis without subjective opinions or suggestions.

10. **Code Snippet Formatting**: All code snippets generated in responses must be systematically
    wrapped in markdown code blocks using triple backticks (```). Language identifiers must be
    included when known (e.g., ```python, ```javascript, ```bash, ```yaml, etc.) to ensure
    proper syntax highlighting and consistent formatting across all generated knowledge bases.

11. **Code Snippet Intent Documentation**: Every code snippet must be prepended with a short 2-sentence
    explanation of its intent and expected benefit. This explanation should clarify what the code
    accomplishes, why it's relevant to the current context, and what value it provides to developers
    understanding or working with the codebase.

12. Ensure there is always a blank line after each header level

13. **Code Quote and Comment Formatting**: Special care must be performed regarding quotes coming from 
    files or generated code snippets. As they can contain comments and lines starting with '#' character, 
    once inserted in LLM output they can be confused with structural standardized markdown headers. Both LLM prompts 
    generating outputs and associated reviewer prompts must ensure that these quotes or generated code snippets 
    are **ALWAYS** properly enclosed in markdown code blocks to prevent structural parsing conflicts with 
    hierarchical semantic tree headers.

14. **Truncation Detection**: All LLM prompt generated outputs (main and reviewer) must finish with exactly 
    this single line to detect LLM output truncation:
    ```
    --END OF LLM OUTPUT--
    ```
    Reviewer prompts will return "TRUNCATED" if this line is not detected. When LLM output truncation is 
    detected, the system will retry the LLM call once before failing the analysis completely. This marker 
    line will be removed when inserting content into the final knowledge base file.

15. **Level 8 External Dependencies Formatting Specification**: Level 8 must follow a standardized format
    for external dependencies and integration points. This specification ensures consistent, actionable
    dependency information across all generated knowledge bases.

**LEVEL 8 REQUIRED FORMAT STRUCTURE:**

**For Code Files:**
```
**→ Inbound:** [what this file depends on]
- `identifier` - description of dependency and usage
- `path/to/file.py:function` - specific function dependency
- `external_library` (external library) - library usage pattern

**← Outbound:** [what depends on this file]
- `dependent/file.py:Class` - class that uses this file's exports
- `external_system` - system that consumes this file's output
- `generated/artifact.ext` - output consumed elsewhere

**⚡ Integration:** [how connections work]
- Protocol: REST/GraphQL/gRPC/Event-driven/Direct-import
- Interface: Class.method(), API endpoint, data format
- Coupling: tight/loose, sync/async, required/optional
```

**For Non-Code Files:**
```
**→ References:** [what this content relies on]
- `external/doc.md` - referenced documentation
- `data/source.json` - required data input
- `https://external-api.com/spec` - external specification

**← Referenced By:** [what uses this content]
- `consumer/system.py` - system that processes this content
- `build/generated.html` - generated output from this content
- `workflow/process.yml` - workflow that depends on this content

**⚡ Integration:** [relationship mechanisms]
- Format: JSON/XML/Markdown/YAML/Binary
- Access: File/API/Database/Manual/Automated
- Sync: Real-time/Batch/Manual/Event-driven
```

**LOCATION IDENTIFIER FORMATTING RULES:**
- **Internal Files**: `relative/path/to/file.ext:symbol` (with file extension and optional symbol)
- **External Libraries**: `library_name` (external library) (with explicit external marker)
- **Configuration**: `config/file.ext:KEY_NAME` (with specific key when applicable)
- **APIs**: `domain.com/endpoint` or `https://full-url.com/path`
- **Generated Files**: `generated/output.ext` or `build/artifact.ext`
- **Directories**: `path/to/directory/` (with trailing slash)

**VISUAL SYMBOLS MEANINGS:**
- `→` indicates inbound dependencies (what this file/content depends on)
- `←` indicates outbound dependencies (what depends on this file/content)
- `⚡` indicates system role and ecosystem integration (core vs peripheral positioning and integration significance)

**MANDATORY REQUIREMENTS:**
- Each subsection (Inbound, Outbound, Integration) must be present even if empty
- All identifiers must include location information when available
- Descriptions must be concise but actionable (focus on "what" and "how")
- Integration section must specify protocol, interface, and coupling characteristics
- Use consistent formatting with backticks for all identifiers
- Follow the exact visual symbol format (→, ←, ⚡) for immediate recognition

REVIEWER PROMPT SCOPE AND LIMITATIONS:
--------------------------------------
**STRUCTURAL COMPLIANCE ONLY**: Reviewer prompts focus exclusively on structural and formatting
compliance rules. They operate at the **STRUCTURAL LEVEL ONLY**, never at the semantic level.

**REVIEWER PROMPTS MUST NOT:**
- Assess whether the content of each semantic level is semantically relevant or appropriate
- Enforce a precise number of semantic levels (content may have fewer levels if appropriate)
- Check if each level header description matches the original intent of the prompt that generated the LLM output
- Make judgments about content quality, completeness, or semantic accuracy
- Evaluate whether the content properly addresses the original analysis requirements

**REVIEWER PROMPTS ONLY VALIDATE:**
- Correct markdown header formatting (####, #####, etc.)
- Proper blank line spacing after headers
- Generic header text (no file/directory-specific information in headers)
- Code snippet formatting with triple backticks and language identifiers
- Directory name formatting with trailing slashes
- Remove duplicate headers and associated content

The reviewer system ensures consistent **structural formatting** while preserving the semantic
content and analytical depth generated by the original LLM prompts.

USAGE PATTERN:
--------------
LLM tools can programmatically select appropriate detail levels:
- Level 4-5: Quick file understanding and navigation
- Level 4-7: Architecture comprehension and design decisions  
- Level 4-10: Implementation understanding and usage patterns
- Level 4-11: Complete technical knowledge for maintenance and modification

This approach optimizes context window usage while providing comprehensive knowledge depth
when required for specific development tasks.
"""

import logging
from typing import Dict, Any, List
from pathlib import Path

from ...helpers.path_utils import get_portable_path

logger = logging.getLogger(__name__)


class EnhancedPrompts:
    """
    [Class intent]
    Container for specialized LLM prompts focusing on architectural analysis and design patterns.
    Provides structured prompts for different content types with emphasis on technical depth
    and implementation insights for comprehensive knowledge base generation.

    [Design principles]
    Architectural focus emphasizing design patterns and technical implementation strategies.
    Structured response format enabling clean programmatic content extraction and integration.
    Content-type specialization providing targeted analysis approaches for different technical contexts.
    Token efficiency through focused analysis reducing verbose generation while maintaining depth.
    Technical comprehensiveness ensuring coverage of critical architectural and implementation aspects.

    [Implementation details]
    Defines specialized prompts for file analysis with architectural emphasis and technical depth.
    Implements directory analysis prompts focusing on module organization and design relationships.
    Provides content-type specific prompts for different technical contexts and file types.
    Uses structured response format compatible with incremental markdown engine operations.
    """
    
    # Semantic Entity Usage specification (DRY principle - applies to all levels)
    SEMANTIC_ENTITY_USAGE_SPEC = """
**SEMANTIC ENTITY USAGE SPECIFICATION:**

**FUNDAMENTAL PRINCIPLE:**
When refering to semantic entities, **ALWAYS** prefer technical entity names when known. Use specific, unambiguous 
technical terminology rather than generic vague wording. This principle enhances semantic precision, improves 
project-wide search capability, and eliminates ambiguity.**ALWAYS surround semantic entity names with backquotes to 
allow clear identification**. 

**TECHNICAL ENTITY PREFERENCE HIERARCHY:**
1. **Exact Technical Names**: Use precise class names, function names, method names, API endpoints (with backquotes)
2. **Domain-Specific Terms**: Use established technical terminology from the relevant domain (with backquotes)
3. **Specific Identifiers**: Include actual module names, configuration keys, protocol names (with backquotes)
4. **Avoid Generic Terms**: Replace vague descriptions with concrete technical references or well-knwon jargon

**EXAMPLES OF PREFERRED USAGE:**
- ✅ **Good**: "`FileAnalysisCache` class provides timestamp-based staleness detection"
- ❌ **Avoid**: "Caching system provides performance optimization"
- ✅ **Good**: "REST API endpoints using `FastAPI` framework with `Pydantic` models"
- ❌ **Avoid**: "Web service interface with data validation"
- ✅ **Good**: "`HierarchicalIndexer` implements leaf-first processing strategy"
- ❌ **Avoid**: "Component handles directory processing workflow"

**LEVEL-SPECIFIC EMPHASIS:**
- **Level 4**: 🚨 **STRONGEST REQUIREMENT** - Technical entitiy names are critical for project-wide search optimization
- **Levels 5-11**: Technical entities strongly preferred with appropriate context for each level's focus

**SEMANTIC SEARCH OPTIMIZATION:**
- Include relevant technical terminology that developers would search for
- Use established patterns and naming conventions from the technology stack
- Reference specific APIs, libraries, frameworks, and tools by their exact names
- Provide semantic context that enables cross-project component discovery

**MAINTAINING FUNCTIONAL FOCUS:**
- Technical entity names enhance rather than replace functional descriptions
- Combine precise technical terms with clear explanations of capabilities and value
- Ensure technical precision serves the communication goal of each level

**LEVEL 4 SEMANTIC ENTITY EXTRACTION:**
- **MANDATORY**: Level 4 must actively identify and list specific semantic entities found in analyzed content
- **CONCRETE NAMES**: Use actual technical names, not generic categories
- **COMPREHENSIVE SCOPE**: Include entities from imports, references, configuration, domain concepts, and architectural patterns
- **VISUAL FORMATTING**: Surround all entities with backquotes for clear identification
"""

    # Level 8 External Dependencies formatting specification (DRY principle)
    LEVEL_8_FORMATTING_SPEC = """
**LEVEL 8 EXTERNAL DEPENDENCIES FORMATTING SPECIFICATION:**

**🚨 INTEGRATION SECTION REQUIREMENTS:**
**CONTEXT-SPECIFIC CONTENT**: Integration section must explain the **specific role** of this file/component within the broader system. Avoid generic descriptions that could apply to any file.

**Required Focus Areas:**
- **System Context**: How does this fit in the overall architecture/workflow?
- **Integration Significance**: Why are these integration points important?
- **Concrete Examples**: Use actual system names, protocols, endpoints, patterns from the analyzed content
- **Developer Actionability**: What should developers understand about these integrations?

**Avoid Generic Statements:**
❌ "Direct function import and async execution"
❌ "Loose coupling through utility wrapper functions"  
❌ "REST/GraphQL/gRPC/Event-driven/Direct-import"

**Prefer Specific Context:**
✅ "MCP resource endpoint validation for jesse://project/gitignore-files"
✅ "FastMCP resource testing pattern ensuring boundary marker compliance"
✅ "Critical validation for Jesse Framework MCP server resource protocol"

**For Code Files:**
```
**→ Inbound:** [what this file depends on]
- `identifier` - description of dependency and usage
- `path/to/file.py:function` - specific function dependency
- `external_library` (external library) - library usage pattern

**← Outbound:** [what depends on this file]
- `dependent/file.py:Class` - class that uses this file's exports
- `external_system` - system that consumes this file's output
- `generated/artifact.ext` - output consumed elsewhere

**⚡ System role and ecosystem integration:** [core vs peripheral positioning and integration significance]
- **System Role**: How this file/component fits within the broader system architecture and workflow
- **Ecosystem Position**: Whether this is central/core, peripheral/support, or auxiliary to system operation
- **Integration Pattern**: Who is using this file and how (humans, external processes, other codebase parts, and their usage patterns)
```

**For Non-Code Files:**
```
**→ References:** [what this content relies on]
- `external/doc.md` - referenced documentation
- `data/source.json` - required data input
- `https://external-api.com/spec` - external specification

**← Referenced By:** [what uses this content]
- `consumer/system.py` - system that processes this content
- `build/generated.html` - generated output from this content
- `workflow/process.yml` - workflow that depends on this content

**⚡ System role and ecosystem integration:** [core vs peripheral positioning and integration significance]
- **System Role**: How this content fits within the broader system architecture and workflow
- **Ecosystem Position**: Whether this is central/core, peripheral/support, or auxiliary to system operation
- **Integration Pattern**: Who is using this file and how (humans, external processes, other codebase parts, and their usage patterns)
```

**LOCATION IDENTIFIER FORMATTING RULES:**
- **Internal Files**: `relative/path/to/file.ext:symbol` (with file extension and optional symbol)
- **External Libraries**: `library_name` (external library) (with explicit external marker)
- **Configuration**: `config/file.ext:KEY_NAME` (with specific key when applicable)
- **APIs**: `domain.com/endpoint` or `https://full-url.com/path`
- **Generated Files**: `generated/output.ext` or `build/artifact.ext`
- **Directories**: `path/to/directory/` (with trailing slash)

**VISUAL SYMBOLS MEANINGS:**
- `→` indicates inbound dependencies (what this file/content depends on)
- `←` indicates outbound dependencies (what depends on this file/content)
- `⚡` indicates system role and ecosystem integration (core vs peripheral positioning and integration significance)

**MANDATORY REQUIREMENTS:**
- Each subsection (Inbound, Outbound, Integration) must be present even if empty
- All identifiers must include location information when available
- Descriptions must be concise but actionable (focus on "what" and "how")
- Integration section must specify protocol, interface, and coupling characteristics
- Use consistent formatting with backticks for all identifiers
- Follow the exact visual symbol format (→, ←, ⚡) for immediate recognition
"""
    
    def __init__(self):
        """
        [Class method intent]
        Initializes enhanced prompts with architecture-focused analysis templates.
        Sets up specialized prompts for different content types with structured response formats
        optimized for programmatic content extraction and technical depth.

        [Design principles]
        Comprehensive prompt initialization covering all major content analysis scenarios.
        Structured response format ensuring clean integration with template engine components.
        Technical focus providing prompts that emphasize architectural and implementation insights.

        [Implementation details]
        Defines core file analysis prompt with architectural emphasis and structured response format.
        Creates directory analysis prompt focusing on module organization and design relationships.
        Sets up content-type specific prompts for specialized technical contexts.
        """
        
        # Hierarchical semantic tree file analysis prompt
        self.file_analysis_prompt = f"""
Analyze this file and generate a hierarchical semantic tree using the specified structure.

**FILE INFORMATION:**
Path: {{file_path}}
Size: {{file_size}} bytes
Content Type: {{content_type}}

**FILE CONTENT:**
{{file_content}}

**CRITICAL REQUIREMENTS:**
🚨 **HIERARCHICAL STRUCTURE MANDATE**: You MUST structure your response using markdown headers levels 4-11 (####-###########) according to the semantic hierarchy specification below.

🚨 **NO REDUNDANCY RULE**: Each level (n-1) MUST contain NO overlapping information with level (n). Information must be unique to each level.

🚨 **PROGRESSIVE COMPLETENESS**: Each level must provide complete context at its depth without requiring higher detail levels.

**HIERARCHICAL SEMANTIC TREE STRUCTURE:**
🚨 **GENERIC HEADER REQUIREMENT**: Headers must contain ONLY generic section purposes. Do NOT include any specific information about the file or directory in the header text itself.

Use this EXACT structure with these EXACT header levels and do not generate any other headers, preambule, postambule or additional text:

#### Functional Intent & Features
*Functional intent (why this exists), features (what it provides), usage value (why consumers should use it), and key semantic entities enabling rapid codebase orientation and navigation*

##### Main Components  
*Primary components, classes, functions, or sections without implementation details*

###### Architecture & Design
*Design patterns, architectural decisions, and structural organization*

####### Implementation Approach
*Key algorithms, data structures, usage patterns, and technical implementation strategies*

######## External Dependencies & Integration Points
*External dependencies (inbound and outbound) and integration mechanisms*

######### Edge Cases & Error Handling
*Error conditions, edge cases, debugging approaches, and failure scenarios*

########## Internal Implementation Details
*Low-level implementation specifics, maintenance notes, and internal mechanisms*

########### Code Usage Examples
*Essential code snippets and usage patterns for this file's main features*
*Note: For non-code files, use this level for practical usage or integration examples*

**CONTENT-TYPE SPECIFIC GUIDELINES:**

**For Code Files:**
- Level 4: Functional intent (why this file exists), features (what capabilities it provides), usage value (why consumers should use it), key semantic entities (class names, function names, imported libraries, frameworks, APIs, configuration keys, protocols) enabling rapid codebase orientation and navigation, and one key technical aspect (using semantic entity names). **CRITICAL**: Every functional claim must be immediately substantiated with concrete evidence from the code (specific class names, method signatures, configuration values, imported modules, etc.)
- Level 5: What components/functions/classes it contains
- Level 6: How it's architecturally designed
- Level 7: Key implementation strategies, usage patterns, and algorithms  
- Level 8: External dependencies (inbound/outbound) and integration points with location-aware identifiers
- Level 9: Error handling and debugging guidance
- Level 10: Internal maintenance and implementation specifics
- Level 11: Essential code snippets developers need

**For Non-Code Files:**
- Structure based on logical information depth and contextual relevance
- Level 4: Functional intent (why this content exists), features (what information/value it provides), usage value (why consumers should reference/use it), key semantic entities (file formats, configuration keys, URLs, tool names, standards, protocols, domain concepts) enabling rapid codebase orientation and navigation, and one key technical aspect (using semantic entity names). **CRITICAL**: Every functional claim must be immediately substantiated with concrete evidence from the content (specific configuration keys, section headers, referenced tools, file paths, etc.)
- Level 5: Main content sections or information types
- Level 6: Organization and structure patterns
- Level 7: Key concepts, usage patterns, and information details
- Level 8: External dependencies (references/referenced by) and integration points with location-aware identifiers
- Level 9: Edge cases, limitations, and troubleshooting
- Level 10: Detailed specifications and technical minutiae
- Level 11: Practical usage and application examples

{self.SEMANTIC_ENTITY_USAGE_SPEC}

{self.LEVEL_8_FORMATTING_SPEC}

**FORMATTING REQUIREMENTS:**
- Write in present tense for intemporal knowledge representation
- **DIRECTORY FORMATTING**: When mentioning directory names, ALWAYS add a trailing slash (e.g., "src/" not "src", "docs/" not "docs")
- **CODE SNIPPET FORMATTING**: When including external file quotes or code snippets, ALWAYS wrap them in markdown code blocks using triple backticks (```). Include the language identifier when known (e.g., ```python, ```javascript, ```bash, ```yaml, etc.)
- **CODE SNIPPET INTENT**: Every code snippet must be prepended with a brief explanation of its intent and expected benefit, clarifying what the code accomplishes and why it's relevant
- **BLANK LINE REQUIREMENT**: Ensure there is always a blank line after each header level for proper markdown formatting
- Make content developer-focused and practical
- Ensure each level stands alone while building upon previous levels
- Use clear, professional technical writing
- **NEVER STATE THE OBVIOUS**: Avoid stating information or best practices known by any modern AI LLM. Focus on unique, valuable insights at each level
- **NO SUBJECTIVE JUDGMENTS**: Do not judge or propose enhancements. Focus on structured, detailed analysis without opinions or suggestions

**RESPONSE VALIDATION:**
Before submitting, verify:
- All 8 header levels (4-11) are present and properly formatted
- No information redundancy between levels
- Each level provides unique, complete context
- Content follows the hierarchical semantic specification
- Headers use exact markdown formatting (####, #####, etc.)

**🚨 MANDATORY TRUNCATION DETECTION:**
**CRITICAL**: Your response MUST end with exactly this line to detect truncation:
```
--END OF LLM OUTPUT--
```

**FAILURE TO INCLUDE THIS LINE WILL RESULT IN TRUNCATION DETECTION AND RETRY.**

Generate the hierarchical semantic tree analysis now.
"""

        # Hierarchical semantic tree directory analysis prompt
        self.directory_analysis_prompt = f"""
Analyze this directory and generate a hierarchical semantic tree using the specified structure.

**DIRECTORY INFORMATION:**
Path: {{directory_path}}/
Total Files: {{file_count}}
Total Subdirectories: {{subdirectory_count}}

**CHILD CONTENT SUMMARY:**
{{child_content_summary}}

**CRITICAL REQUIREMENTS:**
🚨 **HIERARCHICAL STRUCTURE MANDATE**: You MUST structure your response using markdown headers levels 4-11 (####-###########) according to the semantic hierarchy specification below.

🚨 **NO REDUNDANCY RULE**: Each level (n-1) MUST contain NO overlapping information with level (n). Information must be unique to each level.

🚨 **PROGRESSIVE COMPLETENESS**: Each level must provide complete context at its depth without requiring higher detail levels.

**HIERARCHICAL SEMANTIC TREE STRUCTURE:**
🚨 **GENERIC HEADER REQUIREMENT**: Headers must contain ONLY generic section purposes. Do NOT include any specific information about the file or directory in the header text itself.

Use this EXACT structure with these EXACT header levels:

#### Functional Intent & Features
*Functional intent (why this exists), features (what it provides), usage value (why developers should work with it), key semantic entities enabling rapid codebase orientation and navigation, and one key technical aspect (using semantic entity names)*

##### Directory Contents
*Primary subdirectories, file types, and main components without implementation details*

###### Organization & Structure  
*How the directory is organized, architectural patterns, and design decisions*

####### Implementation Patterns
*Common implementation approaches, usage patterns, coding patterns, and technical strategies used throughout*

######## External Dependencies & Integration Points
*External dependencies (inbound and outbound) and integration mechanisms*

######### Edge Cases & Dependencies
*Error conditions, edge cases, external dependencies, and troubleshooting guidance*

########## Internal Organization Details
*Low-level organization specifics, maintenance notes, and internal directory mechanisms*

########### Usage Examples
*Practical examples of how to work with this directory, common workflows, and integration patterns*

**DIRECTORY-SPECIFIC GUIDELINES:**

**For All Directory Types:**
- Level 4: Functional intent (why this directory exists), features (what capabilities it provides), usage value (why developers should work with it), key semantic entities (architectural patterns, technology stack indicators, framework structures, organizational patterns) enabling rapid codebase orientation and navigation, and one key technical aspect (using semantic entity names). **CRITICAL**: Every functional claim must be immediately substantiated with concrete evidence from the directory structure (specific subdirectory names, file types, configuration files, naming patterns, etc.)
- Level 5: What components, files, and subdirectories it contains
- Level 6: How it's organized and structured architecturally
- Level 7: Common implementation patterns and approaches used
- Level 8: External dependencies (inbound/outbound) and integration points with location-aware identifiers
- Level 9: Dependencies, edge cases, and troubleshooting
- Level 10: Internal organization details and maintenance specifics
- Level 11: Practical usage examples and workflow guidance

{self.SEMANTIC_ENTITY_USAGE_SPEC}

{self.LEVEL_8_FORMATTING_SPEC}

**FORMATTING REQUIREMENTS:**
- Write in present tense for intemporal knowledge representation
- **DIRECTORY FORMATTING**: When mentioning directory names, ALWAYS add a trailing slash (e.g., "src/" not "src", "models/" not "models")
- **CODE SNIPPET FORMATTING**: When including external file quotes or code snippets, ALWAYS wrap them in markdown code blocks using triple backticks (```). Include the language identifier when known (e.g., ```python, ```javascript, ```bash, ```yaml, etc.)
- **CODE SNIPPET INTENT**: Every code snippet must be prepended with a brief explanation of its intent and expected benefit, clarifying what the code accomplishes and why it's relevant
- **BLANK LINE REQUIREMENT**: Ensure there is always a blank line after each header level for proper markdown formatting
- Focus on developer navigation and practical understanding
- Ensure each level stands alone while building upon previous levels
- Use clear, professional technical writing
- Use guidance language ("You'll find...", "This contains...", "When working here...")
- **NEVER STATE THE OBVIOUS**: Avoid stated information known by any modern AI LLM. Focus on unique, valuable insights at each level
- **NO SUBJECTIVE JUDGMENTS**: Do not judge or propose enhancements. Focus on structured, detailed analysis without opinions or suggestions

**RESPONSE VALIDATION:**
Before submitting, verify:
- All 8 header levels (4-11) are present and properly formatted
- No information redundancy between levels
- Each level provides unique, complete context
- Content follows the hierarchical semantic specification
- Headers use exact markdown formatting (####, #####, etc.)
- Directory names include trailing slashes

**🚨 MANDATORY TRUNCATION DETECTION:**
**CRITICAL**: Your response MUST end with exactly this line to detect truncation:
```
--END OF LLM OUTPUT--
```

**FAILURE TO INCLUDE THIS LINE WILL RESULT IN TRUNCATION DETECTION AND RETRY.**

Generate the hierarchical semantic tree analysis now.
"""

        
        # Global summary prompt following hierarchical semantic tree structure
        self.global_summary_prompt = f"""
Analyze this complete directory content and generate a hierarchical semantic tree global summary.

**DIRECTORY**: {{directory_path}}/

**ASSEMBLED CONTENT**:
{{assembled_content}}

**CRITICAL REQUIREMENTS:**
🚨 **HIERARCHICAL STRUCTURE MANDATE**: You MUST structure your response using markdown headers levels 4-11 (####-###########) according to the semantic hierarchy specification below.

🚨 **NO REDUNDANCY RULE**: Each level (n-1) MUST contain NO overlapping information with level (n). Information must be unique to each level.

🚨 **PROGRESSIVE COMPLETENESS**: Each level must provide complete context at its depth without requiring higher detail levels.

**HIERARCHICAL SEMANTIC TREE STRUCTURE:**
🚨 **GENERIC HEADER REQUIREMENT**: Headers must contain ONLY generic section purposes. Do NOT include any specific information about the directory in the header text itself.

Use this EXACT structure with these EXACT header levels:

#### Functional Intent & Features
*Functional intent (why this exists), features (what it provides), usage value (why developers should work with it), and key semantic entities enabling rapid codebase orientation and navigation*

##### Main Components
*Primary subdirectories, file types, and main components without implementation details*

###### Architecture & Design
*Design patterns, architectural decisions, and structural organization*

####### Implementation Approach
*Key algorithms, data structures, usage patterns, and technical implementation strategies*

######## External Dependencies & Integration Points
*External dependencies (inbound and outbound) and integration mechanisms*

######### Edge Cases & Error Handling
*Error conditions, edge cases, debugging approaches, and failure scenarios*

########## Internal Implementation Details
*Low-level implementation specifics, maintenance notes, and internal mechanisms*

########### Usage Examples
*Essential usage patterns and workflow examples for working with this directory*

{self.SEMANTIC_ENTITY_USAGE_SPEC}

{self.LEVEL_8_FORMATTING_SPEC}

**FORMATTING REQUIREMENTS:**
- Present FACTUAL TECHNICAL INFORMATION only - no quality judgments, no enhancement proposals
- Identify specific design patterns, implementation strategies, and technical components
- Document integration points, dependencies, and system relationships
- Provide technical facts needed for code maintenance and understanding
- Write in present tense for intemporal knowledge representation
- **DIRECTORY FORMATTING**: When mentioning directory names, ALWAYS add a trailing slash (e.g., "src/" not "src", "tests/" not "tests")
- **CODE SNIPPET FORMATTING**: When including external file quotes or code snippets, ALWAYS wrap them in markdown code blocks using triple backticks (```). Include the language identifier when known (e.g., ```python, ```javascript, ```bash, ```yaml, etc.)
- **CODE SNIPPET INTENT**: Every code snippet must be prepended with a brief explanation of its intent and expected benefit, clarifying what the code accomplishes and why it's relevant
- **BLANK LINE REQUIREMENT**: Ensure there is always a blank line after each header level for proper markdown formatting
- Make content developer-focused and practical
- Ensure each level stands alone while building upon previous levels
- Use clear, professional technical writing
- **NEVER STATE THE OBVIOUS**: Avoid stating information known by any modern AI LLM. Focus on unique, valuable insights at each level
- **NO SUBJECTIVE JUDGMENTS**: Do not judge or propose enhancements. Focus on structured, detailed analysis without opinions or suggestions

**RESPONSE VALIDATION:**
Before submitting, verify:
- All 8 header levels (4-11) are present and properly formatted
- No information redundancy between levels
- Each level provides unique, complete context
- Content follows the hierarchical semantic specification
- Headers use exact markdown formatting (####, #####, etc.)

**🚨 MANDATORY TRUNCATION DETECTION:**
**CRITICAL**: Your response MUST end with exactly this line to detect truncation:
```
--END OF LLM OUTPUT--
```

**FAILURE TO INCLUDE THIS LINE WILL RESULT IN TRUNCATION DETECTION AND RETRY.**

Generate a hierarchical semantic tree global summary that synthesizes all the individual file analyses and subdirectory content into a cohesive understanding of this directory's purpose and implementation.
"""

        # File Analysis Reviewer Prompt
        self.file_analysis_reviewer_prompt = """
Review this file analysis output for structural and formatting compliance with hierarchical semantic tree requirements.

**GENERATED OUTPUT TO REVIEW:**
{generated_output}

**YOUR TASK:**
You are a structural compliance checker operating at the STRUCTURAL LEVEL ONLY. Review the provided output and either:
1. Return "COMPLIANT" if it perfectly meets all structural formatting requirements
2. Return the complete corrected version if any structural formatting issues are found

**REVIEWER SCOPE LIMITATIONS:**
- **STRUCTURAL COMPLIANCE ONLY**: You validate formatting structure, NOT semantic content relevance
- **NO SEMANTIC ASSESSMENT**: Do NOT assess whether content is semantically appropriate for each level
- **NO LEVEL COUNT ENFORCEMENT**: Do NOT require precise number of semantic levels (content may have fewer levels if appropriate)
- **NO INTENT MATCHING**: Do NOT check if header descriptions match original prompt intent
- **NO CONTENT QUALITY JUDGMENTS**: Do NOT evaluate content completeness or semantic accuracy

**STRUCTURAL FORMATTING REQUIREMENTS TO CHECK AND FIX:**

All requirements below are EQUALLY CRITICAL and must be validated with the same level of attention:

**HEADER STRUCTURE VALIDATION:**
- Headers must use correct markdown formatting (####, #####, ######, etc.)
- Headers must be GENERIC only (no specific file/directory information in header text)
- Each header level must be followed by a blank line
- No malformed headers or inconsistent markdown formatting

**CODE SNIPPET FORMATTING:**
- All code snippets MUST be wrapped in markdown code blocks with triple backticks (```)
- Language identifiers MUST be included when possible (```python, ```javascript, ```bash, etc.)
- Every code snippet MUST be preceded by a 2-sentence explanation of its intent and benefit
- **CRITICAL**: Any quotes from files or code snippets containing '#' characters MUST be properly enclosed in markdown code blocks to prevent confusion with structural markdown headers

**DIRECTORY FORMATTING:**
- All directory names MUST have trailing slashes (e.g., "src/" not "src")

**TEXT FORMATTING:**
- Content MUST be written in present tense
- Each header MUST be followed by a blank line
- Remove any subjective judgments or enhancement proposals
- Remove structural redundancy between levels (not semantic redundancy)

**OUTPUT COMPLETENESS VALIDATION:**
- The output MUST end with exactly this line:
```
--END OF LLM OUTPUT--
```
- If this line is missing, return exactly "TRUNCATED"

**FIXING INSTRUCTIONS:**
If you find structural formatting issues:
1. Fix markdown header formatting to be consistent and correct
2. Ensure headers contain only generic section purposes (no file-specific info)
3. Add missing blank lines after headers
4. Wrap all code in proper markdown blocks with language identifiers
5. Add 2-sentence intent explanations before code snippets
6. Add trailing slashes to directory names
7. Convert to present tense where needed
8. Remove structural formatting redundancy

**CRITICAL OUTPUT CONSTRAINTS:**
- **NO ADDITIONAL COMPLIANCE ISSUES**: You must NOT create any new compliance problems
- **NO EXPLANATIONS**: Do NOT add any explanation of discrepancies discovered or what was fixed
- **NO EXTRA FORMATTING**: Do NOT add any extra formatting elements, headers, or structural changes beyond corrections
- **STRICT OUTPUT**: Output ONLY the original input content but corrected to be compliant - nothing more, nothing less
- **NO COMMENTARY**: Do NOT add notes, comments, or explanations about the review process

**OUTPUT FORMAT:**
- If perfect: Return exactly "COMPLIANT"
- If fixes needed: Return the complete corrected version with ONLY the necessary structural formatting fixes applied - no explanations, no additional content, no extra formatting

Review the output now and provide your response.
"""

        # Directory Analysis Reviewer Prompt
        self.directory_analysis_reviewer_prompt = """
Review this directory analysis output for structural and formatting compliance with hierarchical semantic tree requirements.

**GENERATED OUTPUT TO REVIEW:**
{generated_output}

**YOUR TASK:**
You are a structural compliance checker operating at the STRUCTURAL LEVEL ONLY. Review the provided output and either:
1. Return "COMPLIANT" if it perfectly meets all structural formatting requirements
2. Return the complete corrected version if any structural formatting issues are found

**REVIEWER SCOPE LIMITATIONS:**
- **STRUCTURAL COMPLIANCE ONLY**: You validate formatting structure, NOT semantic content relevance
- **NO SEMANTIC ASSESSMENT**: Do NOT assess whether content is semantically appropriate for each level
- **NO LEVEL COUNT ENFORCEMENT**: Do NOT require precise number of semantic levels (content may have fewer levels if appropriate)
- **NO INTENT MATCHING**: Do NOT check if header descriptions match original prompt intent
- **NO CONTENT QUALITY JUDGMENTS**: Do NOT evaluate content completeness or semantic accuracy

**STRUCTURAL FORMATTING REQUIREMENTS TO CHECK AND FIX:**

All requirements below are EQUALLY CRITICAL and must be validated with the same level of attention:

**HEADER STRUCTURE VALIDATION:**
- Headers must use correct markdown formatting (####, #####, ######, etc.)
- Headers must be GENERIC only (no specific directory information in header text)
- Each header level must be followed by a blank line
- No malformed headers or inconsistent markdown formatting

**CODE SNIPPET FORMATTING:**
- All code snippets MUST be wrapped in markdown code blocks with triple backticks (```)
- Language identifiers MUST be included when possible (```python, ```javascript, ```bash, etc.)
- Every code snippet MUST be preceded by a 2-sentence explanation of its intent and benefit
- **CRITICAL**: Any quotes from files or code snippets containing '#' characters MUST be properly enclosed in markdown code blocks to prevent confusion with structural markdown headers

**DIRECTORY FORMATTING:**
- All directory names MUST have trailing slashes (e.g., "models/" not "models")

**TEXT FORMATTING:**
- Content MUST be written in present tense
- Each header MUST be followed by a blank line
- Remove any subjective judgments or enhancement proposals
- Remove structural redundancy between levels (not semantic redundancy)

**OUTPUT COMPLETENESS VALIDATION:**
- The output MUST end with exactly this line:
```
--END OF LLM OUTPUT--
```
- If this line is missing, return exactly "TRUNCATED"

**FIXING INSTRUCTIONS:**
If you find structural formatting issues:
1. Fix markdown header formatting to be consistent and correct
2. Ensure headers contain only generic section purposes (no directory-specific info)
3. Add missing blank lines after headers
4. Wrap all code in proper markdown blocks with language identifiers
5. Add 2-sentence intent explanations before code snippets
6. Add trailing slashes to all directory names
7. Convert to present tense where needed
8. Remove structural formatting redundancy

**CRITICAL OUTPUT CONSTRAINTS:**
- **NO ADDITIONAL COMPLIANCE ISSUES**: You must NOT create any new compliance problems
- **NO EXPLANATIONS**: Do NOT add any explanation of discrepancies discovered or what was fixed
- **NO EXTRA FORMATTING**: Do NOT add any extra formatting elements, headers, or structural changes beyond corrections
- **STRICT OUTPUT**: Output ONLY the original input content but corrected to be compliant - nothing more, nothing less
- **NO COMMENTARY**: Do NOT add notes, comments, or explanations about the review process

**OUTPUT FORMAT:**
- If perfect: Return exactly "COMPLIANT"
- If fixes needed: Return the complete corrected version with ONLY the necessary structural formatting fixes applied - no explanations, no additional content, no extra formatting

Review the output now and provide your response.
"""

        # Global Summary Reviewer Prompt
        self.global_summary_reviewer_prompt = """
Review this global summary output for structural and formatting compliance with hierarchical semantic tree requirements.

**GENERATED OUTPUT TO REVIEW:**
{generated_output}

**YOUR TASK:**
You are a structural compliance checker operating at the STRUCTURAL LEVEL ONLY. Review the provided output and either:
1. Return "COMPLIANT" if it perfectly meets all structural formatting requirements
2. Return the complete corrected version if any structural formatting issues are found

**REVIEWER SCOPE LIMITATIONS:**
- **STRUCTURAL COMPLIANCE ONLY**: You validate formatting structure, NOT semantic content relevance
- **NO SEMANTIC ASSESSMENT**: Do NOT assess whether content is semantically appropriate for each level
- **NO LEVEL COUNT ENFORCEMENT**: Do NOT require precise number of semantic levels (content may have fewer levels if appropriate)
- **NO INTENT MATCHING**: Do NOT check if header descriptions match original prompt intent
- **NO CONTENT QUALITY JUDGMENTS**: Do NOT evaluate content completeness or semantic accuracy

**STRUCTURAL FORMATTING REQUIREMENTS TO CHECK AND FIX:**

All requirements below are EQUALLY CRITICAL and must be validated with the same level of attention:

**HEADER STRUCTURE VALIDATION:**
- Headers must use correct markdown formatting (####, #####, ######, etc.)
- Headers must be GENERIC only (no specific directory information in header text)
- Each header level must be followed by a blank line
- No malformed headers or inconsistent markdown formatting

**CODE SNIPPET FORMATTING:**
- All code snippets MUST be wrapped in markdown code blocks with triple backticks (```)
- Language identifiers MUST be included when possible (```python, ```javascript, ```bash, etc.)
- Every code snippet MUST be preceded by a 2-sentence explanation of its intent and benefit
- **CRITICAL**: Any quotes from files or code snippets containing '#' characters MUST be properly enclosed in markdown code blocks to prevent confusion with structural markdown headers

**DIRECTORY FORMATTING:**
- All directory names MUST have trailing slashes (e.g., "tests/" not "tests")

**TEXT FORMATTING:**
- Content MUST be written in present tense
- Each header MUST be followed by a blank line
- Remove any subjective judgments or enhancement proposals
- Remove structural redundancy between levels (not semantic redundancy)
- Focus on factual technical information only

**OUTPUT COMPLETENESS VALIDATION:**
- The output MUST end with exactly this line:
```
--END OF LLM OUTPUT--
```
- If this line is missing, return exactly "TRUNCATED"

**FIXING INSTRUCTIONS:**
If you find structural formatting issues:
1. Fix markdown header formatting to be consistent and correct
2. Ensure headers contain only generic section purposes (no directory-specific info)
3. Add missing blank lines after headers
4. Wrap all code in proper markdown blocks with language identifiers
5. Add 2-sentence intent explanations before code snippets
6. Add trailing slashes to all directory names
7. Convert to present tense where needed
8. Remove structural formatting redundancy
9. Remove any subjective judgments or quality assessments

**CRITICAL OUTPUT CONSTRAINTS:**
- **NO ADDITIONAL COMPLIANCE ISSUES**: You must NOT create any new compliance problems
- **NO EXPLANATIONS**: Do NOT add any explanation of discrepancies discovered or what was fixed
- **NO EXTRA FORMATTING**: Do NOT add any extra formatting elements, headers, or structural changes beyond corrections
- **STRICT OUTPUT**: Output ONLY the original input content but corrected to be compliant - nothing more, nothing less
- **NO COMMENTARY**: Do NOT add notes, comments, or explanations about the review process

**OUTPUT FORMAT:**
- If perfect: Return exactly "COMPLIANT"
- If fixes needed: Return the complete corrected version with ONLY the necessary structural formatting fixes applied - no explanations, no additional content, no extra formatting

Review the output now and provide your response.
"""
        
        logger.info("EnhancedPrompts initialized with architecture-focused analysis templates and reviewer prompts")
    
    def get_file_analysis_prompt(
        self, 
        file_path: Path, 
        file_content: str, 
        file_size: int = 0
    ) -> str:
        """
        [Class method intent]
        Generates comprehensive file analysis prompt with architectural focus and portable path support.
        Provides consistent architectural analysis for all file types with emphasis on design patterns
        and technical implementation strategies using cross-platform compatible paths.

        [Design principles]
        Architectural emphasis ensuring focus on design patterns and technical implementation strategies.
        Consistent analysis approach providing uniform technical insights across all file types.
        Structured response format enabling clean programmatic content extraction and integration.
        Technical depth ensuring comprehensive coverage of architectural and implementation aspects.
        Portable path support ensuring cross-platform compatibility in generated knowledge.

        [Implementation details]
        Uses core file analysis prompt template with architectural focus and technical depth requirements.
        Converts file path to portable format for cross-platform compatibility in LLM prompts.
        Formats prompt with file metadata and content for comprehensive analysis context.
        Returns structured prompt ready for LLM processing with clear response format expectations.
        """
        try:
            # Convert file path to portable format for cross-platform compatibility
            try:
                portable_file_path = get_portable_path(file_path)
            except Exception as e:
                logger.warning(f"Failed to get portable path for {file_path}, using original: {e}")
                portable_file_path = str(file_path)
            
            # Build prompt with file information using portable path
            formatted_prompt = self.file_analysis_prompt.format(
                file_path=portable_file_path,
                file_size=file_size,
                content_type="general",
                file_content=file_content
            )
            
            logger.debug(f"Generated file analysis prompt for: {file_path}")
            return formatted_prompt
            
        except Exception as e:
            logger.error(f"File analysis prompt generation failed for {file_path}: {e}")
            raise RuntimeError(f"Prompt generation failed: {e}") from e
    
    def get_directory_analysis_prompt(
        self,
        directory_path: Path,
        file_count: int,
        subdirectory_count: int,
        child_content_summary: str
    ) -> str:
        """
        [Class method intent]
        Generates comprehensive directory analysis prompt focusing on module architecture and portable path support.
        Provides structured format for hierarchical analysis with emphasis on component relationships
        and architectural patterns within the directory structure using cross-platform compatible paths.

        [Design principles]
        Module architecture focus emphasizing component organization and design relationships.
        Hierarchical analysis supporting bottom-up architectural understanding and system insights.
        Structured response format enabling clean integration with directory knowledge generation.
        Architectural depth ensuring comprehensive coverage of module design and implementation patterns.
        Portable path support ensuring cross-platform compatibility in generated knowledge.

        [Implementation details]
        Uses directory analysis prompt template with architectural focus and component relationship emphasis.
        Converts directory path to portable format for cross-platform compatibility in LLM prompts.
        Incorporates child content summary for comprehensive hierarchical context and analysis.
        Formats prompt with directory metadata and child content for complete architectural analysis.
        Returns structured prompt ready for LLM processing with clear architectural analysis expectations.
        """
        try:
            # Convert directory path to portable format for cross-platform compatibility
            try:
                portable_directory_path = get_portable_path(directory_path)
            except Exception as e:
                logger.warning(f"Failed to get portable path for {directory_path}, using original: {e}")
                portable_directory_path = str(directory_path)
            
            # Build prompt with directory information using portable path
            formatted_prompt = self.directory_analysis_prompt.format(
                directory_path=portable_directory_path,
                file_count=file_count,
                subdirectory_count=subdirectory_count,
                child_content_summary=child_content_summary
            )
            
            logger.debug(f"Generated directory analysis prompt for: {directory_path}")
            return formatted_prompt
            
        except Exception as e:
            logger.error(f"Directory analysis prompt generation failed for {directory_path}: {e}")
            raise RuntimeError(f"Prompt generation failed: {e}") from e

    def get_file_analysis_reviewer_prompt(self, generated_output: str) -> str:
        """
        [Class method intent]
        Generates file analysis reviewer prompt for structural and formatting compliance checking.
        Provides comprehensive validation of generated file analysis output against hierarchical semantic
        tree requirements with automatic correction capabilities for formatting discrepancies.

        [Design principles]
        Quality assurance focus ensuring consistent structural compliance across all generated content.
        Automated correction approach providing immediate formatting fixes without manual intervention.
        Comprehensive validation covering all critical formatting requirements and structural mandates.
        Clear binary output enabling simple integration with content generation workflows.

        [Implementation details]
        Uses file analysis reviewer prompt template with comprehensive formatting validation rules.
        Formats prompt with generated output for complete structural and formatting review.
        Returns structured prompt ready for LLM processing with clear correction instructions.
        Supports both compliance verification and automatic correction in single operation.
        """
        try:
            formatted_prompt = self.file_analysis_reviewer_prompt.format(
                generated_output=generated_output
            )
            
            logger.debug("Generated file analysis reviewer prompt")
            return formatted_prompt
            
        except Exception as e:
            logger.error(f"File analysis reviewer prompt generation failed: {e}")
            raise RuntimeError(f"Reviewer prompt generation failed: {e}") from e

    def get_directory_analysis_reviewer_prompt(self, generated_output: str) -> str:
        """
        [Class method intent]
        Generates directory analysis reviewer prompt for structural and formatting compliance checking.
        Provides comprehensive validation of generated directory analysis output against hierarchical semantic
        tree requirements with automatic correction capabilities for formatting discrepancies.

        [Design principles]
        Quality assurance focus ensuring consistent structural compliance across all generated directory content.
        Automated correction approach providing immediate formatting fixes without manual intervention.
        Comprehensive validation covering all critical formatting requirements and structural mandates.
        Clear binary output enabling simple integration with directory knowledge generation workflows.

        [Implementation details]
        Uses directory analysis reviewer prompt template with comprehensive formatting validation rules.
        Formats prompt with generated output for complete structural and formatting review.
        Returns structured prompt ready for LLM processing with clear correction instructions.
        Supports both compliance verification and automatic correction in single operation.
        """
        try:
            formatted_prompt = self.directory_analysis_reviewer_prompt.format(
                generated_output=generated_output
            )
            
            logger.debug("Generated directory analysis reviewer prompt")
            return formatted_prompt
            
        except Exception as e:
            logger.error(f"Directory analysis reviewer prompt generation failed: {e}")
            raise RuntimeError(f"Reviewer prompt generation failed: {e}") from e

    def get_global_summary_prompt(
        self,
        directory_path: Path,
        assembled_content: str
    ) -> str:
        """
        [Class method intent]
        Generates comprehensive global summary prompt focusing on system-wide architectural synthesis and portable path support.
        Provides structured format for synthesizing individual file analyses and subdirectory content into cohesive
        understanding of complete directory architecture using cross-platform compatible paths.

        [Design principles]
        System-wide synthesis focus emphasizing complete architectural understanding and component integration.
        Hierarchical summary supporting comprehensive system insights from aggregated technical knowledge.
        Structured response format enabling clean integration with global knowledge generation workflows.
        Architectural comprehensiveness ensuring coverage of complete system design and implementation patterns.
        Portable path support ensuring cross-platform compatibility in generated summary knowledge.

        [Implementation details]
        Uses global summary prompt template with system-wide architectural synthesis and technical integration emphasis.
        Converts directory path to portable format for cross-platform compatibility in LLM prompts.
        Incorporates assembled content from individual analyses for comprehensive system-wide context.
        Formats prompt with directory metadata and aggregated content for complete architectural synthesis.
        Returns structured prompt ready for LLM processing with clear global summary generation expectations.
        """
        try:
            # Convert directory path to portable format for cross-platform compatibility
            try:
                portable_directory_path = get_portable_path(directory_path)
            except Exception as e:
                logger.warning(f"Failed to get portable path for {directory_path}, using original: {e}")
                portable_directory_path = str(directory_path)
            
            # Build prompt with directory information using portable path
            formatted_prompt = self.global_summary_prompt.format(
                directory_path=portable_directory_path,
                assembled_content=assembled_content
            )
            
            logger.debug(f"Generated global summary prompt for: {directory_path}")
            return formatted_prompt
            
        except Exception as e:
            logger.error(f"Global summary prompt generation failed for {directory_path}: {e}")
            raise RuntimeError(f"Prompt generation failed: {e}") from e

    def get_global_summary_reviewer_prompt(self, generated_output: str) -> str:
        """
        [Class method intent]
        Generates global summary reviewer prompt for structural and formatting compliance checking.
        Provides comprehensive validation of generated global summary output against hierarchical semantic
        tree requirements with automatic correction capabilities for formatting discrepancies.

        [Design principles]
        Quality assurance focus ensuring consistent structural compliance across all generated summary content.
        Automated correction approach providing immediate formatting fixes without manual intervention.
        Comprehensive validation covering all critical formatting requirements and structural mandates.
        Clear binary output enabling simple integration with global summary generation workflows.

        [Implementation details]
        Uses global summary reviewer prompt template with comprehensive formatting validation rules.
        Formats prompt with generated output for complete structural and formatting review.
        Returns structured prompt ready for LLM processing with clear correction instructions.
        Supports both compliance verification and automatic correction in single operation.
        """
        try:
            formatted_prompt = self.global_summary_reviewer_prompt.format(
                generated_output=generated_output
            )
            
            logger.debug("Generated global summary reviewer prompt")
            return formatted_prompt
            
        except Exception as e:
            logger.error(f"Global summary reviewer prompt generation failed: {e}")
            raise RuntimeError(f"Reviewer prompt generation failed: {e}") from e

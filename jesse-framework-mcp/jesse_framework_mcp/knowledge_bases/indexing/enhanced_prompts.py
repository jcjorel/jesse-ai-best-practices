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
# - All prompts must generate structured responses compatible with FileAnalysis and DirectorySummary dataclasses
# - Response format must be parseable and extractable for programmatic content insertion
# - Prompts must emphasize architectural and technical aspects over generic functionality descriptions
# - Content must be written in present tense for intemporal knowledge representation
# - Analysis depth must be comprehensive enough for technical decision-making and code understanding
###############################################################################
# [Dependencies]
# <codebase>: .markdown_template_engine - FileAnalysis and DirectorySummary structure definitions
# <system>: typing - Type hints for prompt template parameters and response structures
###############################################################################
# [GenAI tool change history]
# 2025-07-03T13:41:00Z : Added code quote and comment formatting specification to prevent markdown header confusion by CodeAssistant
# * Added HIERARCHY DESIGN PRINCIPLE 13 addressing special care for quotes and code snippets containing '#' characters
# * Specification requires all quotes and code snippets to be properly enclosed in markdown code blocks
# * Prevents confusion between code comments starting with '#' and hierarchical semantic tree markdown headers
# * Applies to both LLM prompt generation outputs and associated reviewer prompt validation processes
# 2025-07-03T13:24:00Z : Added missing get_global_summary_prompt method to complete EnhancedPrompts API by CodeAssistant
# * Added get_global_summary_prompt method following same pattern as other getter methods
# * Method includes comprehensive documentation with class method intent, design principles, and implementation details
# * Supports portable path conversion for cross-platform compatibility in generated global summary knowledge
# * Complete method implementation with proper error handling and logging for system-wide architectural synthesis
# 2025-07-03T13:20:00Z : Fixed level number inconsistencies across all prompts to align with specification by CodeAssistant
# * Corrected all "Level 3-10" references to "Level 4-11" in content-type guidelines sections
# * Updated response validation text from "8 header levels (3-10)" to "8 header levels (4-11)"
# * Fixed content-type guidelines level descriptions to match specification (Level 4: core purpose, Level 5: components, etc.)
# * Ensured complete alignment between prompt explanatory text and hierarchical semantic tree specification requirements
# 2025-07-03T13:08:00Z : Updated all three reviewer prompts with structural-only validation approach alignment by CodeAssistant
# * Applied REVIEWER SCOPE LIMITATIONS section to all three reviewer prompts (file, directory, global summary)
# * All reviewer prompts now clearly state they operate at STRUCTURAL LEVEL ONLY with explicit scope boundaries
# * Consistent structural validation approach across all reviewer prompts ensuring uniform behavior
# * Complete alignment with specification requirement that reviewers only validate formatting, not semantic content
# 2025-07-03T12:01:00Z : Added blank line requirement for proper markdown formatting to all prompts by CodeAssistant
# * Updated specification Rule 12 to require blank line after each header level for proper markdown formatting
# * Added BLANK LINE REQUIREMENT to all three prompts (file analysis, directory analysis, global summary)
# * Ensures consistent markdown formatting with proper spacing after all header levels
# * Aligned all prompts with enhanced specification for improved markdown readability and structure
# 2025-07-03T11:56:00Z : Fixed prompt header levels to match specification requirement 4-11 by CodeAssistant
# * Updated all three prompts to use correct hierarchical structure levels 4-11 (####-###########)
# * Corrected file analysis prompt from inconsistent 4-11 to proper 4-11 structure
# * Corrected directory analysis prompt from inconsistent 3-10 to proper 4-11 structure  
# * Corrected global summary prompt from inconsistent 3-10 to proper 4-11 structure
# * All prompts now consistently follow specification requirement for levels 4-11 hierarchical semantic tree
# 2025-07-03T11:43:00Z : Added code snippet intent documentation requirement to all prompts by CodeAssistant
#m * Updated specification to require every code snippet be prepended with brief explanation of intent and expected benefit
# * Added CODE SNIPPET INTENT requirement to all three prompts (file analysis, directory analysis, global summary)
# * Ensures all code examples include context about what they accomplish and why they're relevant to developers
# * Consistent code snippet documentation approach across the entire hierarchical semantic tree generation system
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
   - Level 4: Core purpose and existence rationale
   - Level 5: Main components and responsibilities  
   - Level 6: Architecture and design patterns
   - Level 7: Implementation approach, usage patterns and key algorithms
   - Level 8: Code snippets and usage examples (for code files)
   - Level 9: Advanced patterns and optimization strategies
   - Level 10: Edge cases, error handling, and debugging
   - Level 11: Internal implementation details and maintenance notes

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

8. **Never state the obvious!**: Avoid stating information and best practices known by any modern AI LLM in headers or content. Focus on
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
- Level 4-9: Implementation understanding and usage patterns
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
    Uses structured response format compatible with FileAnalysis and DirectorySummary dataclasses.
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
        self.file_analysis_prompt = """
Analyze this file and generate a hierarchical semantic tree using the specified structure.

**FILE INFORMATION:**
Path: {file_path}
Size: {file_size} bytes
Content Type: {content_type}

**FILE CONTENT:**
{file_content}

**CRITICAL REQUIREMENTS:**
🚨 **HIERARCHICAL STRUCTURE MANDATE**: You MUST structure your response using markdown headers levels 4-11 (####-###########) according to the semantic hierarchy specification below.

🚨 **NO REDUNDANCY RULE**: Each level (n-1) MUST contain NO overlapping information with level (n). Information must be unique to each level.

🚨 **PROGRESSIVE COMPLETENESS**: Each level must provide complete context at its depth without requiring higher detail levels.

**HIERARCHICAL SEMANTIC TREE STRUCTURE:**
🚨 **GENERIC HEADER REQUIREMENT**: Headers must contain ONLY generic section purposes. Do NOT include any specific information about the file or directory in the header text itself.

Use this EXACT structure with these EXACT header levels and do not generate any other headers, preambule, postambule or additional text:

#### File Purpose
*Core purpose and existence rationale - why this file exists in the system*

##### Main Components  
*Primary components, classes, functions, or sections without implementation details*

###### Architecture & Design
*Design patterns, architectural decisions, and structural organization*

####### Implementation Approach
*Key algorithms, data structures, usage patterns, and technical implementation strategies*

######## Code Usage Examples
*Essential code snippets and usage patterns for this file's main features*
*Note: For non-code files, use this level for practical usage or integration examples*

######### Advanced Patterns
*Optimization strategies, performance considerations, and advanced usage patterns*

########## Edge Cases & Error Handling
*Error conditions, edge cases, debugging approaches, and failure scenarios*

########### Internal Implementation Details
*Low-level implementation specifics, maintenance notes, and internal mechanisms*

**CONTENT-TYPE SPECIFIC GUIDELINES:**

**For Code Files:**
- Level 4: Why this file exists (business/technical purpose)
- Level 5: What components/functions/classes it contains
- Level 6: How it's architecturally designed
- Level 7: Key implementation strategies, usage patterns, and algorithms  
- Level 8: Essential code snippets developers need
- Level 9: Advanced usage and optimization patterns
- Level 10: Error handling and debugging guidance
- Level 11: Internal maintenance and implementation specifics

**For Non-Code Files:**
- Structure based on logical information depth and contextual relevance
- Level 4: Core purpose and why it exists
- Level 5: Main content sections or information types
- Level 6: Organization and structure patterns
- Level 7: Key concepts, usage patterns, and information details
- Level 8: Practical usage and application examples
- Level 9: Advanced topics and specialized information
- Level 10: Edge cases, limitations, and troubleshooting
- Level 11: Detailed specifications and technical minutiae

**FORMATTING REQUIREMENTS:**
- Write in present tense for intemporal knowledge representation
- **DIRECTORY FORMATTING**: When mentioning directory names, ALWAYS add a trailing slash (e.g., "src/" not "src", "docs/" not "docs")
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

Generate the hierarchical semantic tree analysis now.
"""

        # Hierarchical semantic tree directory analysis prompt
        self.directory_analysis_prompt = """
Analyze this directory and generate a hierarchical semantic tree using the specified structure.

**DIRECTORY INFORMATION:**
Path: {directory_path}/
Total Files: {file_count}
Total Subdirectories: {subdirectory_count}

**CHILD CONTENT SUMMARY:**
{child_content_summary}

**CRITICAL REQUIREMENTS:**
🚨 **HIERARCHICAL STRUCTURE MANDATE**: You MUST structure your response using markdown headers levels 4-11 (####-###########) according to the semantic hierarchy specification below.

🚨 **NO REDUNDANCY RULE**: Each level (n-1) MUST contain NO overlapping information with level (n). Information must be unique to each level.

🚨 **PROGRESSIVE COMPLETENESS**: Each level must provide complete context at its depth without requiring higher detail levels.

**HIERARCHICAL SEMANTIC TREE STRUCTURE:**
🚨 **GENERIC HEADER REQUIREMENT**: Headers must contain ONLY generic section purposes. Do NOT include any specific information about the file or directory in the header text itself.

Use this EXACT structure with these EXACT header levels:

#### Directory Purpose
*Core purpose and existence rationale - why this directory exists in the system*

##### Directory Contents
*Primary subdirectories, file types, and main components without implementation details*

###### Organization & Structure  
*How the directory is organized, architectural patterns, and design decisions*

####### Implementation Patterns
*Common implementation approaches, usage patterns, coding patterns, and technical strategies used throughout*

######## Usage Examples
*Practical examples of how to work with this directory, common workflows, and integration patterns*

######### Advanced Integration
*Complex integration patterns, optimization strategies, and advanced usage scenarios*

########## Edge Cases & Dependencies
*Error conditions, edge cases, external dependencies, and troubleshooting guidance*

########### Internal Organization Details
*Low-level organization specifics, maintenance notes, and internal directory mechanisms*

**DIRECTORY-SPECIFIC GUIDELINES:**

**For All Directory Types:**
- Level 4: Why this directory exists (functional/architectural purpose)
- Level 5: What components, files, and subdirectories it contains
- Level 6: How it's organized and structured architecturally
- Level 7: Common implementation patterns and approaches used
- Level 8: Practical usage examples and workflow guidance
- Level 9: Advanced integration patterns and optimization strategies
- Level 10: Dependencies, edge cases, and troubleshooting
- Level 11: Internal organization details and maintenance specifics

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

Generate the hierarchical semantic tree analysis now.
"""

        
        # Global summary prompt following hierarchical semantic tree structure
        self.global_summary_prompt = """
Analyze this complete directory content and generate a hierarchical semantic tree global summary.

**DIRECTORY**: {directory_path}/

**ASSEMBLED CONTENT**:
{assembled_content}

**CRITICAL REQUIREMENTS:**
🚨 **HIERARCHICAL STRUCTURE MANDATE**: You MUST structure your response using markdown headers levels 4-11 (####-###########) according to the semantic hierarchy specification below.

🚨 **NO REDUNDANCY RULE**: Each level (n-1) MUST contain NO overlapping information with level (n). Information must be unique to each level.

🚨 **PROGRESSIVE COMPLETENESS**: Each level must provide complete context at its depth without requiring higher detail levels.

**HIERARCHICAL SEMANTIC TREE STRUCTURE:**
🚨 **GENERIC HEADER REQUIREMENT**: Headers must contain ONLY generic section purposes. Do NOT include any specific information about the directory in the header text itself.

Use this EXACT structure with these EXACT header levels:

#### Directory Purpose
*Core purpose and existence rationale - why this directory exists in the system*

##### Main Components
*Primary subdirectories, file types, and main components without implementation details*

###### Architecture & Design
*Design patterns, architectural decisions, and structural organization*

####### Implementation Approach
*Key algorithms, data structures, usage patterns, and technical implementation strategies*

######## Usage Examples
*Essential usage patterns and workflow examples for working with this directory*

######### Advanced Patterns
*Optimization strategies, performance considerations, and advanced integration patterns*

########## Edge Cases & Error Handling
*Error conditions, edge cases, debugging approaches, and failure scenarios*

########### Internal Implementation Details
*Low-level implementation specifics, maintenance notes, and internal mechanisms*

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

**🚨 REVIEWER SCOPE LIMITATIONS:**
- **STRUCTURAL COMPLIANCE ONLY**: You validate formatting structure, NOT semantic content relevance
- **NO SEMANTIC ASSESSMENT**: Do NOT assess whether content is semantically appropriate for each level
- **NO LEVEL COUNT ENFORCEMENT**: Do NOT require precise number of semantic levels (content may have fewer levels if appropriate)
- **NO INTENT MATCHING**: Do NOT check if header descriptions match original prompt intent
- **NO CONTENT QUALITY JUDGMENTS**: Do NOT evaluate content completeness or semantic accuracy

**STRUCTURAL FORMATTING REQUIREMENTS TO CHECK AND FIX:**

🚨 **HEADER STRUCTURE VALIDATION:**
- Headers must use correct markdown formatting (####, #####, ######, etc.)
- Headers must be GENERIC only (no specific file/directory information in header text)
- Each header level must be followed by a blank line
- No malformed headers or inconsistent markdown formatting

🚨 **CODE SNIPPET FORMATTING:**
- All code snippets MUST be wrapped in markdown code blocks with triple backticks (```)
- Language identifiers MUST be included when possible (```python, ```javascript, ```bash, etc.)
- Every code snippet MUST be preceded by a 2-sentence explanation of its intent and benefit
- **CRITICAL**: Any quotes from files or code snippets containing '#' characters MUST be properly enclosed in markdown code blocks to prevent confusion with structural markdown headers

🚨 **DIRECTORY FORMATTING:**
- All directory names MUST have trailing slashes (e.g., "src/" not "src")

🚨 **TEXT FORMATTING:**
- Content MUST be written in present tense
- Each header MUST be followed by a blank line
- Remove any subjective judgments or enhancement proposals
- Remove structural redundancy between levels (not semantic redundancy)

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
🚨 **NO ADDITIONAL COMPLIANCE ISSUES**: You must NOT create any new compliance problems
🚨 **NO EXPLANATIONS**: Do NOT add any explanation of discrepancies discovered or what was fixed
🚨 **NO EXTRA FORMATTING**: Do NOT add any extra formatting elements, headers, or structural changes beyond corrections
🚨 **STRICT OUTPUT**: Output ONLY the original input content but corrected to be compliant - nothing more, nothing less
🚨 **NO COMMENTARY**: Do NOT add notes, comments, or explanations about the review process

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

**🚨 REVIEWER SCOPE LIMITATIONS:**
- **STRUCTURAL COMPLIANCE ONLY**: You validate formatting structure, NOT semantic content relevance
- **NO SEMANTIC ASSESSMENT**: Do NOT assess whether content is semantically appropriate for each level
- **NO LEVEL COUNT ENFORCEMENT**: Do NOT require precise number of semantic levels (content may have fewer levels if appropriate)
- **NO INTENT MATCHING**: Do NOT check if header descriptions match original prompt intent
- **NO CONTENT QUALITY JUDGMENTS**: Do NOT evaluate content completeness or semantic accuracy

**STRUCTURAL FORMATTING REQUIREMENTS TO CHECK AND FIX:**

🚨 **HEADER STRUCTURE VALIDATION:**
- Headers must use correct markdown formatting (####, #####, ######, etc.)
- Headers must be GENERIC only (no specific directory information in header text)
- Each header level must be followed by a blank line
- No malformed headers or inconsistent markdown formatting

🚨 **CODE SNIPPET FORMATTING:**
- All code snippets MUST be wrapped in markdown code blocks with triple backticks (```)
- Language identifiers MUST be included when possible (```python, ```javascript, ```bash, etc.)
- Every code snippet MUST be preceded by a 2-sentence explanation of its intent and benefit
- **CRITICAL**: Any quotes from files or code snippets containing '#' characters MUST be properly enclosed in markdown code blocks to prevent confusion with structural markdown headers

🚨 **DIRECTORY FORMATTING:**
- All directory names MUST have trailing slashes (e.g., "models/" not "models")

🚨 **TEXT FORMATTING:**
- Content MUST be written in present tense
- Each header MUST be followed by a blank line
- Remove any subjective judgments or enhancement proposals
- Remove structural redundancy between levels (not semantic redundancy)

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
🚨 **NO ADDITIONAL COMPLIANCE ISSUES**: You must NOT create any new compliance problems
🚨 **NO EXPLANATIONS**: Do NOT add any explanation of discrepancies discovered or what was fixed
🚨 **NO EXTRA FORMATTING**: Do NOT add any extra formatting elements, headers, or structural changes beyond corrections
🚨 **STRICT OUTPUT**: Output ONLY the original input content but corrected to be compliant - nothing more, nothing less
🚨 **NO COMMENTARY**: Do NOT add notes, comments, or explanations about the review process

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

**🚨 REVIEWER SCOPE LIMITATIONS:**
- **STRUCTURAL COMPLIANCE ONLY**: You validate formatting structure, NOT semantic content relevance
- **NO SEMANTIC ASSESSMENT**: Do NOT assess whether content is semantically appropriate for each level
- **NO LEVEL COUNT ENFORCEMENT**: Do NOT require precise number of semantic levels (content may have fewer levels if appropriate)
- **NO INTENT MATCHING**: Do NOT check if header descriptions match original prompt intent
- **NO CONTENT QUALITY JUDGMENTS**: Do NOT evaluate content completeness or semantic accuracy

**STRUCTURAL FORMATTING REQUIREMENTS TO CHECK AND FIX:**

🚨 **HEADER STRUCTURE VALIDATION:**
- Headers must use correct markdown formatting (####, #####, ######, etc.)
- Headers must be GENERIC only (no specific directory information in header text)
- Each header level must be followed by a blank line
- No malformed headers or inconsistent markdown formatting

🚨 **CODE SNIPPET FORMATTING:**
- All code snippets MUST be wrapped in markdown code blocks with triple backticks (```)
- Language identifiers MUST be included when possible (```python, ```javascript, ```bash, etc.)
- Every code snippet MUST be preceded by a 2-sentence explanation of its intent and benefit
- **CRITICAL**: Any quotes from files or code snippets containing '#' characters MUST be properly enclosed in markdown code blocks to prevent confusion with structural markdown headers

🚨 **DIRECTORY FORMATTING:**
- All directory names MUST have trailing slashes (e.g., "tests/" not "tests")

🚨 **TEXT FORMATTING:**
- Content MUST be written in present tense
- Each header MUST be followed by a blank line
- Remove any subjective judgments or enhancement proposals
- Remove structural redundancy between levels (not semantic redundancy)
- Focus on factual technical information only

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
🚨 **NO ADDITIONAL COMPLIANCE ISSUES**: You must NOT create any new compliance problems
🚨 **NO EXPLANATIONS**: Do NOT add any explanation of discrepancies discovered or what was fixed
🚨 **NO EXTRA FORMATTING**: Do NOT add any extra formatting elements, headers, or structural changes beyond corrections
🚨 **STRICT OUTPUT**: Output ONLY the original input content but corrected to be compliant - nothing more, nothing less
🚨 **NO COMMENTARY**: Do NOT add notes, comments, or explanations about the review process

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

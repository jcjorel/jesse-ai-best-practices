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
# 2025-07-01T16:23:00Z : Initial enhanced prompts creation by CodeAssistant
# * Created architecture-focused prompts for file and directory analysis
# * Implemented structured response format for programmatic content extraction
# * Set up content-type specialization for different technical contexts
###############################################################################

"""
Enhanced LLM Prompts for Architectural Analysis.

This module provides specialized prompts focusing on architectural analysis,
design patterns, and technical implementation details for comprehensive
knowledge base generation with token-efficient structured responses.
"""

import logging
from typing import Dict, Any, List
from pathlib import Path

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
        
        # Simplified file analysis prompt for natural markdown response
        self.file_analysis_prompt = """
Analyze this source code file and provide practical insights for developers working with it.

**FILE INFORMATION:**
Path: {file_path}
Size: {file_size} bytes
Content Type: {content_type}

**FILE CONTENT:**
{file_content}

**INSTRUCTIONS:**
- Provide practical information that helps developers understand what they'll find in this file
- Focus on navigation guidance: what to expect, main components, organization patterns
- Explain connections to other parts of the system
- Include context needed for effective development work
- Write in present tense and be developer-focused
- Respond in clear, well-formatted markdown
- **DIRECTORY FORMATTING**: When mentioning directory names, ALWAYS add a trailing slash (e.g., "src/" not "src", "docs/" not "docs")

Generate a comprehensive analysis that helps developers quickly understand and work with this code.
"""

        # Directory analysis prompt with navigation focus (helping developers understand what they'll find)
        self.directory_analysis_prompt = """
Help developers understand what to expect when navigating and working within this directory. Provide practical guidance in the following structured format:

**CRITICAL REQUIREMENTS:**
- Focus on DEVELOPER NAVIGATION - what will developers find and need to know when working in this directory
- Present information that helps developers quickly understand what to expect in this directory and its subdirectories
- Provide practical context for navigating and working within this module effectively
- Write in present tense using guidance language ("You'll find...", "This contains..., "When working here...")
- Be concise and developer-focused for practical navigation
- **DIRECTORY FORMATTING**: When mentioning directory names, ALWAYS add a trailing slash (e.g., "src/" not "src", "models/" not "models")

**DIRECTORY INFORMATION:**
Path: {directory_path}/
Total Files: {file_count}
Total Subdirectories: {subdirectory_count}

**CHILD CONTENT SUMMARY:**
{child_content_summary}

**REQUIRED NAVIGATION FORMAT:**

[WHAT_THIS_DIRECTORY_CONTAINS]

Describe what developers will find when working in this directory:
- Primary purpose and what this directory accomplishes
- Types of functionality and code you'll encounter here
- Main responsibilities and capabilities contained within
- Role this directory plays in the overall system

[HOW_ITS_ORGANIZED]

Explain how the directory is structured for effective navigation:
- How files and subdirectories are grouped and organized
- Logical organization patterns developers can expect
- Entry points and main interfaces available
- Common workflows and usage patterns within this directory
- Conventions and naming patterns used throughout

[COMMON_PATTERNS]

Identify patterns developers will encounter across the directory:
- Repeated design approaches and coding patterns
- Shared conventions and common implementations
- Configuration and setup patterns used throughout
- Error handling and validation approaches you'll find
- Testing and development patterns consistent across files

[HOW_IT_CONNECTS]

Show how this directory fits into the larger system:
- Dependencies and what this directory relies on
- Other parts of the system that use this directory
- External connections (APIs, databases, services)
- Integration points developers should be aware of
- Data flow and communication patterns with other modules

**IMPORTANT:** Focus on practical information that helps developers navigate, understand, and work within this directory effectively.
"""

        # Content-type specific prompts for specialized analysis
        self.content_type_prompts = {
            "configuration": """
Focus additional analysis on:
- Configuration schema and parameter relationships
- Environment-specific behavior and deployment implications
- Security implications of configuration choices
- Performance tuning parameters and system impact
- Validation and error handling for configuration values
""",
            
            "api": """
Focus additional analysis on:
- API design patterns and RESTful principles
- Request/response schema and data validation
- Error handling and status code strategies
- Authentication and authorization implementation
- Rate limiting and performance considerations
- Versioning and backward compatibility strategies
""",
            
            "database": """
Focus additional analysis on:
- Data modeling and schema design decisions
- Query patterns and performance optimization
- Transaction handling and consistency strategies
- Migration strategies and schema evolution
- Connection pooling and resource management
- Indexing strategies and performance characteristics
""",
            
            "testing": """
Focus additional analysis on:
- Testing architecture and strategy patterns
- Test data management and fixture patterns
- Mocking and isolation strategies
- Test coverage and quality assurance approaches
- Performance testing and load testing patterns
- Integration testing and end-to-end testing strategies
""",
            
            "infrastructure": """
Focus additional analysis on:
- Deployment patterns and infrastructure as code
- Monitoring and observability implementation
- Logging strategies and structured logging
- Health checks and service discovery patterns
- Scaling strategies and resource management
- Security hardening and compliance implementation
"""
        }
        
        logger.info("EnhancedPrompts initialized with architecture-focused analysis templates")
    
    def get_file_analysis_prompt(
        self, 
        file_path: Path, 
        file_content: str, 
        file_size: int = 0,
        content_type: str = "general"
    ) -> str:
        """
        [Class method intent]
        Generates comprehensive file analysis prompt with architectural focus and structured response format.
        Combines core analysis requirements with content-type specific analysis for targeted
        technical insights and architectural understanding.

        [Design principles]
        Architectural emphasis ensuring focus on design patterns and technical implementation strategies.
        Content-type specialization providing targeted analysis approaches for different technical contexts.
        Structured response format enabling clean programmatic content extraction and integration.
        Technical depth ensuring comprehensive coverage of architectural and implementation aspects.

        [Implementation details]
        Uses core file analysis prompt template with architectural focus and technical depth requirements.
        Incorporates content-type specific analysis extensions for specialized technical contexts.
        Formats prompt with file metadata and content for comprehensive analysis context.
        Returns structured prompt ready for LLM processing with clear response format expectations.
        """
        try:
            # Build base prompt with file information
            formatted_prompt = self.file_analysis_prompt.format(
                file_path=str(file_path),
                file_size=file_size,
                content_type=content_type,
                file_content=file_content
            )
            
            # Add content-type specific analysis if available
            if content_type in self.content_type_prompts:
                content_specific = self.content_type_prompts[content_type]
                formatted_prompt += f"\n\n**CONTENT-TYPE SPECIFIC ANALYSIS:**\n{content_specific}"
            
            logger.debug(f"Generated file analysis prompt for: {file_path} (type: {content_type})")
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
        Generates comprehensive directory analysis prompt focusing on module architecture and design organization.
        Provides structured format for hierarchical analysis with emphasis on component relationships
        and architectural patterns within the directory structure.

        [Design principles]
        Module architecture focus emphasizing component organization and design relationships.
        Hierarchical analysis supporting bottom-up architectural understanding and system insights.
        Structured response format enabling clean integration with directory knowledge generation.
        Architectural depth ensuring comprehensive coverage of module design and implementation patterns.

        [Implementation details]
        Uses directory analysis prompt template with architectural focus and component relationship emphasis.
        Incorporates child content summary for comprehensive hierarchical context and analysis.
        Formats prompt with directory metadata and child content for complete architectural analysis.
        Returns structured prompt ready for LLM processing with clear architectural analysis expectations.
        """
        try:
            formatted_prompt = self.directory_analysis_prompt.format(
                directory_path=str(directory_path),
                file_count=file_count,
                subdirectory_count=subdirectory_count,
                child_content_summary=child_content_summary
            )
            
            logger.debug(f"Generated directory analysis prompt for: {directory_path}")
            return formatted_prompt
            
        except Exception as e:
            logger.error(f"Directory analysis prompt generation failed for {directory_path}: {e}")
            raise RuntimeError(f"Prompt generation failed: {e}") from e
    
    def detect_content_type(self, file_path: Path, file_content: str) -> str:
        """
        [Class method intent]
        Detects content type of file for specialized analysis approach selection.
        Analyzes file extension, content patterns, and structural characteristics
        to determine appropriate analysis context and prompt specialization.

        [Design principles]
        Content-type detection enabling specialized analysis approaches for different technical contexts.
        Pattern recognition supporting accurate content type classification and analysis optimization.
        Extensible detection logic supporting addition of new content types and analysis specializations.

        [Implementation details]
        Analyzes file extension and content patterns for content type classification.
        Uses keyword analysis and structural patterns for accurate content type detection.
        Returns content type identifier for specialized prompt selection and analysis context.
        """
        try:
            file_extension = file_path.suffix.lower()
            file_name = file_path.name.lower()
            content_lower = file_content.lower()
            
            # Configuration files
            if any(pattern in file_name for pattern in ['config', 'settings', '.env', '.conf']):
                return "configuration"
            
            # API-related files
            if any(pattern in content_lower for pattern in ['@app.route', 'fastapi', 'flask', 'api', 'endpoint']):
                return "api"
            
            # Database-related files
            if any(pattern in content_lower for pattern in ['sqlalchemy', 'database', 'session', 'query', 'model']):
                return "database"
            
            # Testing files
            if any(pattern in file_name for pattern in ['test_', '_test', 'spec_']) or 'test' in file_name:
                return "testing"
            
            # Infrastructure files
            if file_extension in ['.yml', '.yaml'] or any(pattern in file_name for pattern in ['docker', 'deploy', 'infra']):
                return "infrastructure"
            
            # Default to general analysis
            return "general"
            
        except Exception as e:
            logger.warning(f"Content type detection failed for {file_path}: {e}")
            return "general"
    
    def parse_structured_response(self, llm_response: str) -> Dict[str, str]:
        """
        [Class method intent]
        Parses structured LLM response into component sections for programmatic content extraction.
        Extracts analysis sections from formatted LLM response for integration with
        FileAnalysis and DirectorySummary dataclasses.

        [Design principles]
        Structured response parsing enabling clean integration with template engine components.
        Robust parsing logic handling variations in LLM response format and structure.
        Error handling ensuring graceful degradation when response parsing encounters issues.

        [Implementation details]
        Uses section delimiter parsing to extract individual analysis components from LLM response.
        Maps parsed sections to FileAnalysis and DirectorySummary dataclass field requirements.
        Handles parsing errors gracefully with fallback content and detailed error reporting.
        """
        try:
            sections = {}
            current_section = None
            current_content = []
            
            lines = llm_response.split('\n')
            
            for line in lines:
                stripped_line = line.strip()
                
                # Check for section headers in various formats:
                # [SECTION_NAME], **[SECTION_NAME]**, ## [SECTION_NAME], etc.
                section_match = None
                
                if stripped_line.startswith('**[') and stripped_line.endswith(']**'):
                    # Format: **[SECTION_NAME]**
                    section_match = stripped_line[3:-3]
                elif stripped_line.startswith('[') and stripped_line.endswith(']'):
                    # Format: [SECTION_NAME]
                    section_match = stripped_line[1:-1]
                elif stripped_line.startswith('## [') and stripped_line.endswith(']'):
                    # Format: ## [SECTION_NAME]
                    section_match = stripped_line[4:-1]
                elif stripped_line.startswith('### [') and stripped_line.endswith(']'):
                    # Format: ### [SECTION_NAME]
                    section_match = stripped_line[5:-1]
                
                if section_match:
                    # Save previous section
                    if current_section:
                        sections[current_section] = '\n'.join(current_content).strip()
                    
                    # Start new section
                    current_section = section_match.lower()
                    current_content = []
                    logger.debug(f"Found section: {current_section}")
                
                elif current_section:
                    current_content.append(line)
            
            # Save final section
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            
            logger.debug(f"Parsed {len(sections)} sections from LLM response: {list(sections.keys())}")
            return sections
            
        except Exception as e:
            logger.error(f"Structured response parsing failed: {e}")
            return {
                "what_you_ll_find": "Analysis parsing failed",
                "main_components": "Analysis parsing failed", 
                "how_its_organized": "Analysis parsing failed",
                "connections": "Analysis parsing failed",
                "context_you_need": "Analysis parsing failed",
                "implementation_notes": "Analysis parsing failed"
            }

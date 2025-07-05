<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/llm/strands_agent_driver/examples/README.md -->
<!-- Cached On: 2025-07-05T14:11:20.928576 -->
<!-- Source Modified: 2025-07-01T08:59:29.237995 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This documentation provides comprehensive guidance for standalone example applications demonstrating Claude 4 Sonnet driver capabilities within the Jesse Framework MCP Server ecosystem, enabling developers to understand and implement AWS Bedrock integration patterns with practical, executable demonstrations. The content serves as both educational material and operational reference for developers working with the Strands Agent Driver system, offering step-by-step setup instructions, configuration examples, and troubleshooting guidance. Key semantic entities include `basic_conversation.py`, `streaming_conversation.py`, and `caching_example.py` example files, `Claude4SonnetConfig` configuration class with factory methods `create_optimized_for_conversations()`, `create_optimized_for_analysis()`, and `create_optimized_for_performance()`, `StrandsClaude4Driver` main driver class, AWS environment variables `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_PROFILE`, and `AWS_REGION`, Amazon Bedrock service integration, `ConversationMemoryStrategy.SUMMARIZING` memory management, prompt caching system with TTL configuration, streaming response processing, token usage tracking, and comprehensive error handling patterns including `NoCredentialsError`, `AccessDenied`, and model availability issues. The system implements async-first architecture with context manager patterns for resource lifecycle management and detailed performance metrics collection.

##### Main Components

The documentation contains six primary content sections providing comprehensive coverage of the Claude 4 Sonnet driver example ecosystem. The Prerequisites section outlines AWS credential configuration, Amazon Bedrock access requirements, and dependency installation procedures. The Available Examples section details three standalone demonstration scripts including basic conversation management, streaming response processing, and prompt caching optimization with specific execution commands and feature descriptions. The Example Output section provides formatted console output samples showing actual execution results with performance metrics and statistics. The Configuration Examples section demonstrates four different configuration patterns optimized for conversations, analysis, performance, and custom use cases. The Troubleshooting section addresses common issues including credential problems, access denied errors, model availability, and SDK installation with specific solutions. The Integration section shows how to incorporate the driver into Jesse MCP Server applications with practical code examples.

###### Architecture & Design

The architecture implements a documentation-first design pattern with clear separation between setup requirements, practical examples, and integration guidance, following educational progression from basic concepts to advanced implementation patterns. The design emphasizes hands-on learning through executable examples with comprehensive output formatting and detailed explanations of each feature demonstration. Key design patterns include the progressive complexity pattern moving from basic conversation to advanced caching, factory method pattern documentation for configuration optimization, troubleshooting pattern with specific error scenarios and solutions, and integration pattern showing real-world usage within the Jesse MCP Server ecosystem. The system uses structured formatting with emoji indicators, code block highlighting, and consistent section organization to enhance readability and developer experience.

####### Implementation Approach

The implementation uses executable Python scripts as primary teaching tools with comprehensive setup instructions and dependency management through `uv` package manager. Example execution employs standardized command patterns with `uv run python examples/` prefix for consistent developer experience across different environments. Configuration demonstration uses factory method patterns with specific parameter examples showing temperature settings, memory strategies, caching options, and streaming configurations. Output formatting implements structured console display with emoji indicators, section dividers, performance metrics, and detailed statistics to enhance educational value. Error handling documentation provides specific error messages with corresponding solutions and debugging approaches. Integration examples show practical usage patterns within larger application contexts with async patterns and session management.

######## External Dependencies & Integration Points

**→ References:**
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_PROFILE` environment variables - AWS credential configuration for Bedrock service authentication
- `Amazon Bedrock` service - AWS managed AI service providing Claude 4 Sonnet model access and API integration
- `uv` package manager - Python dependency management and virtual environment handling for example execution
- `strands-agents` package - core SDK providing Claude 4 Sonnet driver implementation and configuration classes
- `basic_conversation.py`, `streaming_conversation.py`, `caching_example.py` - standalone example applications demonstrating specific driver features
- `test_strands_driver.py` - test suite for driver installation verification and functionality validation
- `requirements.txt` - Python dependency specification for alternative installation methods

**← Referenced By:**
- Developer onboarding workflows - consuming setup instructions and example execution patterns for learning driver integration
- Jesse MCP Server integration projects - using configuration examples and integration patterns for production implementation
- Documentation and training materials - referencing example outputs and troubleshooting guidance for educational content
- Testing and validation processes - using example applications for driver functionality verification and regression testing

**⚡ System role and ecosystem integration:**
- **System Role**: Educational documentation hub for Claude 4 Sonnet driver within Jesse Framework MCP Server ecosystem, providing comprehensive guidance for AWS Bedrock integration and practical implementation patterns
- **Ecosystem Position**: Peripheral educational component supporting developer adoption and integration of core driver functionality, bridging standalone examples with production MCP server usage
- **Integration Pattern**: Used by developers through direct documentation reference and example execution, consumed by integration projects for configuration guidance, and referenced by educational workflows for hands-on learning experiences

######### Edge Cases & Error Handling

The system addresses missing AWS credentials through detailed environment variable configuration with multiple authentication methods including direct key specification and AWS profile usage. Amazon Bedrock access issues are handled with specific guidance for model access requests and IAM permission configuration. Model availability problems are addressed through region-specific guidance and model ID verification procedures. SDK installation issues are resolved through multiple installation methods including `uv sync` and traditional `pip install` approaches. Debug mode activation provides detailed logging configuration for troubleshooting complex integration issues. Connection failures include specific error message patterns with corresponding diagnostic steps and resolution procedures. The documentation provides fallback testing approaches for environments without AWS access through local test suite execution.

########## Internal Implementation Details

The documentation uses structured markdown formatting with consistent emoji indicators for different content types including prerequisites (📋), configuration (🌡️), execution commands (🚀), and troubleshooting (❌). Code examples employ syntax highlighting with language-specific formatting for bash commands, Python code, and configuration snippets. Performance metrics display includes specific formatting patterns for token usage, response times, cache statistics, and cost optimization data. Error message formatting uses consistent patterns with error codes, descriptions, and solution steps. Configuration examples show explicit parameter values including temperature settings (0.7, 0.8), token limits (4096), retry counts (3), and cache TTL values (300s). Integration patterns demonstrate async context manager usage, session management, and response processing with specific method calls and parameter passing.

########### Code Usage Examples

AWS credential configuration demonstrates the essential setup pattern for Bedrock service access. This approach provides multiple authentication methods to accommodate different deployment environments and security requirements.

```bash
# Environment variable configuration for AWS Bedrock access
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=us-east-1

# Alternative profile-based configuration
export AWS_PROFILE=your_profile_name
```

Driver configuration and integration showcases the practical implementation pattern for Jesse MCP Server integration. This pattern demonstrates factory method usage, async context management, and session-based conversation handling for production applications.

```python
# Jesse MCP Server integration with Claude 4 Sonnet driver
from llm.claude4_driver import StrandsClaude4Driver, Claude4SonnetConfig

class JESSEMCPServer:
    def __init__(self):
        config = Claude4SonnetConfig.create_optimized_for_conversations()
        self.claude_driver = StrandsClaude4Driver(config)
    
    async def handle_user_message(self, message: str, session_id: str):
        response = await self.claude_driver.send_message(message, session_id)
        return response.content
```
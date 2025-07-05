<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/llm/strands_agent_driver/examples/basic_conversation.py -->
<!-- Cached On: 2025-07-05T14:13:53.002341 -->
<!-- Source Modified: 2025-07-03T12:12:01.023700 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements a basic conversation demonstration script for the Claude 4 Sonnet driver, showcasing fundamental conversation capabilities through sequential question-answer interactions with comprehensive statistics tracking and error handling for educational and testing purposes. The script enables developers to understand and validate basic conversation patterns with the Strands Agent Driver system using live AWS Bedrock integration, demonstrating conversation lifecycle management and response metadata collection. Key semantic entities include `basic_conversation_example()` function for primary conversation demonstration, `StrandsClaude4Driver` class for AWS Bedrock integration, `Claude4SonnetConfig` configuration class with factory method `create_optimized_for_conversations()`, `start_conversation()` method for session initialization, `send_message()` method for message processing, `get_conversation_stats()` method for statistics retrieval, conversation identifier `basic_example_conversation`, response attributes `content`, `tokens_used`, and `from_cache`, configuration properties `model_id`, `temperature`, `memory_strategy`, `enable_prompt_caching`, `enable_extended_thinking`, and `suppress_reasoning_output`, `BedrockConnectionError` and `StrandsDriverError` exception classes, AWS environment variables `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_PROFILE`, and `AWS_REGION`, and comprehensive logging setup with structured formatting. The system implements async-first architecture with context manager patterns for resource lifecycle management and detailed console output formatting for educational demonstration purposes.

##### Main Components

The file contains two primary async functions providing comprehensive basic conversation demonstration capabilities. The `basic_conversation_example()` function performs the main conversation demonstration with predefined question sequences, response metadata display, conversation statistics collection, and global driver statistics reporting. The `main()` function serves as the orchestration entry point with AWS credential validation, region detection, and error handling for the demonstration execution. The script includes structured logging configuration with timestamp formatting, path manipulation for module imports, and detailed console output with emoji-based visual indicators for different conversation phases. The conversation flow uses a predefined list of four questions covering introduction, AI benefits, prompt caching explanation, and conversation closure with systematic processing and metadata reporting for each interaction.

###### Architecture & Design

The architecture implements a demonstration-focused design pattern with clear separation between conversation execution and orchestration logic, following educational progression through structured question sequences and comprehensive output formatting. The design emphasizes conversation lifecycle management through proper session initialization, message processing, and statistics collection. Key design patterns include the demonstration pattern with sequential question processing, factory method pattern usage for optimized configuration, async context manager pattern for resource management, and educational pattern with detailed explanatory output and metadata display. The system uses conversation isolation through unique identifiers, comprehensive exception handling with specific error types, and structured console formatting with emoji indicators and section dividers for enhanced readability.

####### Implementation Approach

The implementation uses async context managers for proper resource lifecycle management with `StrandsClaude4Driver` instances and factory method configuration through `create_optimized_for_conversations()` for optimized settings. Conversation processing employs sequential question iteration with `asyncio.sleep(1)` delays between questions for demonstration pacing. Response handling includes comprehensive metadata extraction and display including token usage, cache status, and content presentation. The approach implements detailed statistics collection at both conversation and global levels with structured data presentation. Error handling uses specific exception types with user-friendly error messages and troubleshooting guidance. Console output employs structured formatting with emoji indicators, section dividers, and detailed explanatory text to enhance educational value.

######## External Dependencies & Integration Points

**→ Inbound:**
- `asyncio` (external library) - async event loop management for demonstration execution and sleep delays between questions
- `sys` (external library) - Python path manipulation for module imports and exit handling with status codes
- `os` (external library) - environment variable access for AWS credentials and region configuration
- `logging` (external library) - structured logging setup with timestamp formatting and level configuration
- `pathlib.Path` (external library) - cross-platform path operations for module import path construction
- `strands_agent_driver:StrandsClaude4Driver` - main driver class for AWS Bedrock Claude 4 integration and conversation management
- `strands_agent_driver:Claude4SonnetConfig` - configuration class with factory methods for optimized conversation settings
- `strands_agent_driver:StrandsDriverError` - driver-specific exception handling for operational errors
- `strands_agent_driver:BedrockConnectionError` - AWS Bedrock connection error handling for authentication issues

**← Outbound:**
- Developer education workflows - consuming basic conversation demonstration output for understanding driver usage patterns
- Testing and validation processes - using conversation results to verify basic driver functionality and response handling
- Documentation and training materials - referencing conversation patterns and configuration examples for educational content
- AWS Bedrock service integration - generating actual API calls for live conversation demonstration when credentials are available

**⚡ System role and ecosystem integration:**
- **System Role**: Educational demonstration component for Strands Agent Driver basic conversation capabilities, providing foundational examples of conversation lifecycle management and response processing for developers learning the system
- **Ecosystem Position**: Peripheral educational component supporting developer onboarding and basic functionality validation, demonstrating core driver conversation features without being part of production workflows
- **Integration Pattern**: Used by developers through direct script execution for learning basic conversation patterns, consumed by educational processes for driver capability demonstration, and integrated with AWS Bedrock services for live conversation testing when proper credentials are configured

######### Edge Cases & Error Handling

The system handles missing AWS credentials gracefully by detecting environment variables and providing informative warnings with setup guidance without failing the demonstration. AWS Bedrock connection errors are caught with specific `BedrockConnectionError` handling and detailed troubleshooting steps including credential validation, Bedrock access verification, and model access confirmation. Driver operational errors are managed through `StrandsDriverError` exception handling with descriptive error messages. Keyboard interrupts are handled with clean exit messages and proper signal handling using `sys.exit(1)`. The script manages conversation initialization failures and message sending errors with comprehensive exception handling. Statistics retrieval handles missing or unavailable data gracefully with conditional display logic and error reporting.

########## Internal Implementation Details

The demonstration uses a hardcoded list of four questions including introduction, AI benefits inquiry, prompt caching explanation, and conversation closure for consistent educational flow. Configuration display shows specific properties including `model_id`, `temperature`, `memory_strategy.value`, `enable_prompt_caching`, `enable_extended_thinking`, and `suppress_reasoning_output` for comprehensive configuration transparency. Conversation ID is explicitly set to `basic_example_conversation` for clear session identification. Response processing includes content display with section dividers using `-` characters and metadata reporting including token usage and cache status. Statistics collection accesses both conversation-specific and global driver statistics with structured data presentation. Console output uses structured formatting with specific emoji indicators and detailed explanatory text for enhanced educational value.

########### Code Usage Examples

Basic conversation setup demonstrates the essential pattern for Claude 4 Sonnet driver initialization and configuration. This approach shows factory method usage for optimized conversation settings and proper async context management for resource lifecycle.

```python
# Initialize Claude 4 Sonnet driver with optimized conversation configuration
config = Claude4SonnetConfig.create_optimized_for_conversations()
async with StrandsClaude4Driver(config) as driver:
    conversation_id = "basic_example_conversation"
    await driver.start_conversation(conversation_id, {"example": "basic"})
```

Sequential conversation processing showcases the pattern for structured question-answer interactions with comprehensive metadata collection. This pattern demonstrates proper message sending, response handling, and statistics tracking for educational conversation flows.

```python
# Process sequential questions with response metadata and statistics tracking
questions = [
    "Hello! Can you introduce yourself?",
    "What are the key benefits of using AI in software development?",
    "Can you explain what prompt caching is and why it's useful?",
    "Thank you for the conversation!"
]

for i, question in enumerate(questions, 1):
    print(f"👤 Question {i}: {question}")
    response = await driver.send_message(question, conversation_id)
    print(response.content)
    print(f"📊 Tokens used: {response.tokens_used}")
    print(f"💾 From cache: {response.from_cache}")
    
    if i < len(questions):
        await asyncio.sleep(1)
```
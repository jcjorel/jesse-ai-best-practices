<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/llm/strands_agent_driver/driver.py -->
<!-- Cached On: 2025-07-05T14:22:02.493445 -->
<!-- Source Modified: 2025-07-04T17:47:39.173494 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements the main driver class for Claude 4 Sonnet integration using the Strands Agent SDK, providing a pure asyncio interface with streaming conversation capabilities, prompt caching, and conversation management designed for complete independence from Jesse MCP Server while offering clean integration interfaces. The driver enables developers to interact with Claude 4 Sonnet through AWS Bedrock with advanced features including real-time streaming, intelligent caching, multiple memory management strategies, and automatic retry logic with exponential backoff. Key semantic entities include `StrandsClaude4Driver` main driver class with async context manager support, `StreamingResponse` class for real-time response chunks with `content`, `is_complete`, and `metadata` attributes, `ConversationResponse` class for complete responses with `content`, `conversation_id`, `tokens_used`, `from_cache`, and `metadata` attributes, core methods `initialize()`, `send_message()`, `stream_conversation()`, `start_conversation()`, `get_conversation_stats()`, `clear_conversation()`, and `clear_all_conversations()`, internal methods `_build_conversation_prompt()`, `_send_with_retry()`, and `_stream_with_retry()`, `ConversationManager` integration for session and cache management, exception classes `StrandsDriverError`, `ConversationError`, `ModelConfigurationError`, `BedrockConnectionError`, `StreamingError`, and `TokenLimitError`, Strands SDK components `Agent`, `BedrockModel`, and `AgentResult`, convenience functions `create_driver()` and `conversation_session()` context manager, streaming event types including `data`, `reasoning`, `tool_use`, and `complete`, and comprehensive error handling with retry logic and graceful degradation for missing dependencies. The system implements async-first architecture with context manager patterns for resource lifecycle management and real streaming capabilities through the Strands Agent SDK.

##### Main Components

The file contains three primary classes and two convenience functions providing comprehensive Claude 4 Sonnet driver functionality. The `StrandsClaude4Driver` class serves as the main driver with initialization, conversation management, streaming capabilities, and resource cleanup through async context manager support. The `StreamingResponse` class represents individual streaming chunks with content, completion status, metadata, and timestamp information for real-time response processing. The `ConversationResponse` class encapsulates complete conversation responses with content, conversation tracking, token usage, cache status, metadata, and timestamp information. The `create_driver()` function provides a convenience factory for driver initialization with automatic setup. The `conversation_session()` async context manager enables session-scoped driver usage with automatic conversation initialization and cleanup. The module includes comprehensive error handling, Strands SDK integration with availability checking, logging infrastructure, and retry logic with exponential backoff for robust operation.

###### Architecture & Design

The architecture implements an async-first design pattern with comprehensive context manager support for resource lifecycle management, following clean separation between driver logic, conversation management, and streaming response handling. The design emphasizes independence from Jesse MCP Server while providing clean integration interfaces through well-defined APIs and response objects. Key design patterns include the async context manager pattern for automatic resource management, factory pattern for driver creation and configuration presets, adapter pattern for Strands SDK integration with graceful degradation, streaming iterator pattern for real-time response delivery, retry pattern with exponential backoff for reliability, and composition pattern with ConversationManager for session and cache management. The system uses dependency injection for configuration management, lazy initialization for Strands components, and comprehensive error handling with specific exception types for different failure scenarios.

####### Implementation Approach

The implementation uses async context managers with `__aenter__` and `__aexit__` methods for proper resource lifecycle management and automatic cleanup. Strands SDK integration employs conditional imports with availability checking and mock class definitions for type safety when the SDK is unavailable. Streaming implementation leverages real Strands Agent SDK streaming through `stream_async()` method with event processing for different stream types including data, reasoning, and tool usage events. The approach implements retry logic with exponential backoff using configurable delay and maximum retry attempts for both regular and streaming operations. Conversation management uses prompt building with role-based message formatting and context accumulation for multi-turn conversations. Error handling employs specific exception types with detailed error context and graceful degradation for missing dependencies or configuration issues.

######## External Dependencies & Integration Points

**→ Inbound:**
- `asyncio` (external library) - async event loop management for driver operations, streaming processing, and context manager lifecycle
- `logging` (external library) - structured logging for driver operations, error tracking, and debugging information
- `typing` (external library) - comprehensive type annotations including Dict, List, Optional, Any, AsyncIterator, Union for type safety
- `contextlib` (external library) - asynccontextmanager decorator for convenience context manager creation
- `time` (external library) - timestamp generation for response objects and performance tracking
- `strands:Agent` (external library) - Strands Agent SDK main class for Claude 4 Sonnet interaction and streaming capabilities
- `strands.models:BedrockModel` (external library) - Bedrock model wrapper for AWS integration and configuration management
- `strands.types:AgentResult` (external library) - response type for Strands Agent operations with optional availability
- `.models:Claude4SonnetConfig` - configuration class providing model parameters and AWS settings
- `.models:ConversationContext` - context management class for session tracking and metadata
- `.conversation:ConversationManager` - conversation and cache management component for session handling
- `.exceptions` module - comprehensive exception classes for error handling and debugging

**← Outbound:**
- Jesse Framework MCP Server integration - consuming driver through async context manager for Claude 4 Sonnet capabilities
- Example demonstration scripts - using driver for educational examples and feature validation
- Testing frameworks - consuming driver API for functionality verification and regression testing
- Application integration layers - using convenience functions and context managers for simplified integration
- Logging and monitoring systems - consuming log output for operational visibility and debugging

**⚡ System role and ecosystem integration:**
- **System Role**: Core driver implementation for Claude 4 Sonnet integration within Jesse Framework ecosystem, providing complete async interface for AWS Bedrock interaction with streaming, caching, and conversation management capabilities
- **Ecosystem Position**: Central driver component serving as the primary interface for Claude 4 Sonnet functionality, designed for independence from Jesse MCP Server while enabling clean integration through well-defined APIs
- **Integration Pattern**: Used by applications through async context manager pattern, consumed by Jesse MCP Server through direct instantiation and method calls, and integrated with Strands Agent SDK through adapter pattern with graceful degradation for missing dependencies

######### Edge Cases & Error Handling

The system handles missing Strands Agent SDK through conditional imports with `STRANDS_AVAILABLE` flag and mock class definitions for type checking when the SDK is unavailable. Driver initialization failures are managed through `BedrockConnectionError` with region context and detailed error messages for AWS Bedrock connection issues. Conversation management errors use `ConversationError` for session-specific issues with conversation ID context for debugging. Streaming failures employ `StreamingError` with retry logic and exponential backoff for transient network issues. Token limit scenarios are handled through `TokenLimitError` with current and maximum token information for resource management. Configuration validation raises `ModelConfigurationError` for invalid parameters with model ID context. The system provides comprehensive retry logic with configurable maximum attempts and exponential backoff for both regular and streaming operations, graceful degradation for missing conversations with automatic session creation, and detailed logging for all error conditions with appropriate log levels.

########## Internal Implementation Details

The driver uses lazy initialization with `_is_initialized` flag and async lock for thread-safe initialization of Strands components. Strands SDK integration employs `BedrockModel` initialization with configuration parameters from `to_strands_model_kwargs()` method and `Agent` initialization with empty tools list for non-MCP usage. Streaming implementation processes different event types including data events for text content, reasoning events for Claude 4 thinking output with suppression control, and tool usage events for MCP integration capabilities. Retry logic implements exponential backoff with configurable delay starting at `retry_delay_seconds` and doubling on each retry when `exponential_backoff` is enabled. Conversation prompt building uses role-based formatting with "Human:", "Assistant:", and "System:" prefixes for proper Claude 4 interaction patterns. Response processing handles different result types from Strands Agent including string responses, objects with content attributes, and generic object conversion to string. The system maintains conversation state through ConversationManager integration with automatic message addition and cache management for performance optimization.

########### Code Usage Examples

Basic driver usage demonstrates the async context manager pattern for automatic resource management and conversation handling. This approach provides essential driver lifecycle management with proper initialization and cleanup for reliable Claude 4 Sonnet interaction.

```python
# Use async context manager for automatic driver lifecycle management
from strands_agent_driver import StrandsClaude4Driver, Claude4SonnetConfig

async def basic_conversation():
    config = Claude4SonnetConfig.create_optimized_for_conversations()
    
    async with StrandsClaude4Driver(config) as driver:
        # Start conversation and send message
        await driver.start_conversation("my_chat")
        response = await driver.send_message("Hello, Claude!", "my_chat")
        
        print(f"Response: {response.content}")
        print(f"From cache: {response.from_cache}")
        print(f"Tokens used: {response.tokens_used}")
```

Advanced streaming usage showcases the real-time response processing pattern with comprehensive event handling and metadata inspection. This pattern demonstrates how to leverage streaming capabilities for immediate user feedback and different event type processing.

```python
# Process streaming responses with real-time event handling and metadata inspection
async def streaming_conversation():
    config = Claude4SonnetConfig(streaming=True, suppress_reasoning_output=False)
    
    async with StrandsClaude4Driver(config) as driver:
        await driver.start_conversation("streaming_chat")
        
        async for chunk in driver.stream_conversation("Explain quantum computing", "streaming_chat"):
            if chunk.metadata.get("stream_event") == "data":
                print(chunk.content, end="", flush=True)
            elif chunk.metadata.get("stream_event") == "reasoning":
                print(f"\n[Thinking: {chunk.content}]")
            elif chunk.is_complete:
                print("\n--- Response complete ---")
                break
```
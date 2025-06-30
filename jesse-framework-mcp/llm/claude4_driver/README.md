# Strands Claude 4 Sonnet Driver

Pure asyncio implementation for Amazon Bedrock Claude 4 Sonnet integration using the Strands Agent SDK, designed for JESSE MCP Server usage.

## Features

- **Pure Asyncio Interface**: Complete async/await support for modern Python applications
- **Streaming Conversations**: Real-time response streaming capabilities
- **Prompt Caching**: Intelligent caching system for performance optimization
- **Memory Management**: Multiple conversation memory strategies (summarizing, sliding window, null)
- **Claude 4 Sonnet Optimization**: Leverages extended thinking mode and 200K token context
- **Retry Logic**: Automatic retry with exponential backoff for reliability
- **Complete Independence**: No dependencies on JESSE MCP Server components

## Installation

The driver requires the Strands Agent SDK and AWS Bedrock access:

```bash
pip install strands-agents boto3
```

## Quick Start

### Basic Usage

```python
import asyncio
from llm.claude4_driver import StrandsClaude4Driver, Claude4SonnetConfig

async def basic_conversation():
    # Create configuration
    config = Claude4SonnetConfig.create_optimized_for_conversations()
    
    # Use context manager for automatic cleanup
    async with StrandsClaude4Driver(config) as driver:
        # Start a conversation
        conversation_id = "my_conversation"
        await driver.start_conversation(conversation_id)
        
        # Send a message
        response = await driver.send_message(
            "Hello! Can you explain quantum computing?",
            conversation_id
        )
        
        print(f"Claude: {response.content}")
        print(f"From cache: {response.from_cache}")
        print(f"Tokens used: {response.tokens_used}")

# Run the example
asyncio.run(basic_conversation())
```

### Streaming Conversations

```python
async def streaming_conversation():
    config = Claude4SonnetConfig()
    
    async with StrandsClaude4Driver(config) as driver:
        conversation_id = "streaming_chat"
        await driver.start_conversation(conversation_id)
        
        # Stream response in real-time
        async for chunk in driver.stream_conversation(
            "Write a story about space exploration",
            conversation_id
        ):
            print(chunk.content, end="", flush=True)
            
            if chunk.is_complete:
                print("\n--- Response complete ---")
                break

asyncio.run(streaming_conversation())
```

## Configuration Options

### Pre-configured Setups

```python
from llm.claude4_driver import Claude4SonnetConfig

# Optimized for long conversations
conversation_config = Claude4SonnetConfig.create_optimized_for_conversations()

# Optimized for analytical tasks
analysis_config = Claude4SonnetConfig.create_optimized_for_analysis()

# Optimized for fast responses
performance_config = Claude4SonnetConfig.create_optimized_for_performance()
```

### Custom Configuration

```python
from llm.claude4_driver import Claude4SonnetConfig, ConversationMemoryStrategy

config = Claude4SonnetConfig(
    # Model parameters
    model_id="claude-sonnet-4-20250514",
    temperature=0.8,
    max_tokens=4096,
    
    # AWS settings
    aws_region="us-east-1",
    aws_profile="default",
    
    # Memory management
    memory_strategy=ConversationMemoryStrategy.SUMMARIZING,
    max_context_tokens=180000,
    conversation_summary_threshold=150000,
    
    # Caching
    enable_prompt_caching=True,
    cache_ttl_seconds=3600,
    
    # Claude 4 features
    enable_extended_thinking=True,
    thinking_timeout_seconds=480,
    
    # Retry configuration
    max_retries=3,
    exponential_backoff=True
)
```

## Memory Management Strategies

### Summarizing Strategy (Recommended)

Automatically summarizes older messages when approaching context limits:

```python
config = Claude4SonnetConfig(
    memory_strategy=ConversationMemoryStrategy.SUMMARIZING,
    conversation_summary_threshold=150000
)
```

### Sliding Window Strategy

Keeps only the most recent messages:

```python
config = Claude4SonnetConfig(
    memory_strategy=ConversationMemoryStrategy.SLIDING_WINDOW
)
```

### Null Strategy

No memory persistence (each message is independent):

```python
config = Claude4SonnetConfig(
    memory_strategy=ConversationMemoryStrategy.NULL
)
```

## Advanced Features

### Conversation Management

```python
async def conversation_management():
    async with StrandsClaude4Driver() as driver:
        # Start multiple conversations
        await driver.start_conversation("work_chat", {"project": "AI"})
        await driver.start_conversation("personal_chat", {"type": "casual"})
        
        # Get conversation statistics
        work_stats = await driver.get_conversation_stats("work_chat")
        global_stats = await driver.get_conversation_stats()
        
        print(f"Work chat: {work_stats['message_count']} messages")
        print(f"Total conversations: {global_stats['total_conversations']}")
        
        # Clear specific conversation
        await driver.clear_conversation("work_chat")
        
        # Clear all conversations
        await driver.clear_all_conversations()
```

### Cache Management

```python
async def cache_example():
    config = Claude4SonnetConfig(
        enable_prompt_caching=True,
        cache_ttl_seconds=1800,  # 30 minutes
        max_cache_entries=50
    )
    
    async with StrandsClaude4Driver(config) as driver:
        conversation_id = "cached_chat"
        await driver.start_conversation(conversation_id)
        
        # First call - goes to Claude 4
        response1 = await driver.send_message("What is Python?", conversation_id)
        print(f"First call from cache: {response1.from_cache}")
        
        # Second call - retrieved from cache
        response2 = await driver.send_message("What is Python?", conversation_id)
        print(f"Second call from cache: {response2.from_cache}")
```

### Error Handling

```python
from llm.claude4_driver import (
    StrandsDriverError,
    BedrockConnectionError,
    ConversationError
)

async def error_handling_example():
    try:
        config = Claude4SonnetConfig(aws_region="invalid-region")
        async with StrandsClaude4Driver(config) as driver:
            await driver.send_message("Hello", "test_chat")
            
    except BedrockConnectionError as e:
        print(f"AWS connection failed: {e}")
    except ConversationError as e:
        print(f"Conversation error: {e}")
    except StrandsDriverError as e:
        print(f"Driver error: {e}")
```

## AWS Configuration

### Environment Variables

```bash
export AWS_REGION=us-east-1
export AWS_PROFILE=default
# OR
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
```

### Programmatic Configuration

```python
config = Claude4SonnetConfig(
    aws_region="us-west-2",
    aws_profile="bedrock-user"
)
```

## Testing

Run the included test suite to verify functionality:

```bash
cd jesse-framework-mcp
python test_strands_driver.py
```

The test suite includes:
- Configuration validation
- Driver initialization
- Conversation management
- Caching system
- Error handling

## Performance Optimization

### For Long Conversations

```python
config = Claude4SonnetConfig.create_optimized_for_conversations(
    enable_prompt_caching=True,
    memory_strategy=ConversationMemoryStrategy.SUMMARIZING,
    max_context_tokens=180000
)
```

### For Fast Responses

```python
config = Claude4SonnetConfig.create_optimized_for_performance(
    enable_extended_thinking=False,
    max_tokens=2048,
    memory_strategy=ConversationMemoryStrategy.NULL
)
```

### For Complex Analysis

```python
config = Claude4SonnetConfig.create_optimized_for_analysis(
    enable_extended_thinking=True,
    thinking_timeout_seconds=600,  # 10 minutes
    temperature=0.3
)
```

## Integration with JESSE MCP Server

While this driver is completely independent, it's designed for easy integration with the JESSE MCP Server:

```python
# In your MCP server code
from llm.claude4_driver import StrandsClaude4Driver, Claude4SonnetConfig

class JESSEMCPServer:
    def __init__(self):
        self.claude_driver = None
    
    async def initialize(self):
        config = Claude4SonnetConfig.create_optimized_for_conversations()
        self.claude_driver = StrandsClaude4Driver(config)
        await self.claude_driver.initialize()
    
    async def handle_user_message(self, message: str, session_id: str):
        response = await self.claude_driver.send_message(message, session_id)
        return response.content
```

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure `strands-agents` is installed
2. **AWS Credentials**: Verify AWS credentials and region configuration
3. **Model Access**: Ensure Bedrock access to Claude 4 Sonnet model
4. **Token Limits**: Monitor conversation token usage and adjust limits

### Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Your driver code here...
```

## Requirements

- Python 3.10+
- strands-agents (Strands Agent SDK)
- boto3 (AWS SDK)
- AWS Bedrock access with Claude 4 Sonnet model enabled

## License

This driver is part of the JESSE Framework and follows the same license terms.

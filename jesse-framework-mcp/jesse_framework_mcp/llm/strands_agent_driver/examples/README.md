# Claude 4 Sonnet Driver Examples

This directory contains standalone example applications that demonstrate the capabilities of the Claude 4 Sonnet driver for the JESSE MCP Server.

## Prerequisites

Before running these examples, make sure you have:

1. **AWS Credentials Configured**
   ```bash
   # Option 1: Environment variables
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_REGION=us-east-1
   
   # Option 2: AWS Profile
   export AWS_PROFILE=your_profile_name
   ```

2. **Amazon Bedrock Access**
   - Enable Amazon Bedrock in your AWS account
   - Request access to Claude 4 Sonnet model
   - Ensure your IAM role has Bedrock permissions

3. **Dependencies Installed**
   ```bash
   cd jesse-framework-mcp
   uv sync  # or pip install -r requirements.txt
   ```

## Available Examples

### 1. Basic Conversation (`basic_conversation.py`)

Demonstrates a simple conversation with Claude 4 Sonnet:
- Multiple questions and answers
- Conversation statistics
- Error handling
- Driver lifecycle management

**Run:**
```bash
cd jesse-framework-mcp
uv run python examples/basic_conversation.py
```

**Features demonstrated:**
- ✅ Driver initialization and cleanup
- ✅ Conversation management
- ✅ Response metadata (tokens, caching status)
- ✅ Statistics tracking
- ✅ Error handling

### 2. Streaming Conversation (`streaming_conversation.py`)

Shows real-time streaming responses from Claude 4 Sonnet:
- Streaming vs non-streaming comparison
- Real-time response chunks
- Performance metrics
- User experience improvements

**Run:**
```bash
cd jesse-framework-mcp
uv run python examples/streaming_conversation.py
```

**Features demonstrated:**
- ✅ Real-time streaming responses
- ✅ Chunk-by-chunk processing
- ✅ Performance comparison
- ✅ Streaming statistics
- ✅ User experience optimization

### 3. Prompt Caching (`caching_example.py`)

Demonstrates prompt caching for performance optimization:
- Cache hits vs cache misses
- Performance improvements
- Cache management
- Cost optimization

**Run:**
```bash
cd jesse-framework-mcp
uv run python examples/caching_example.py
```

**Features demonstrated:**
- ✅ Prompt caching system
- ✅ Performance optimization
- ✅ Cache statistics
- ✅ Cache expiration and eviction
- ✅ Cost savings analysis

## Example Output

### Basic Conversation
```
🚀 Basic Conversation Example with Claude 4 Sonnet
============================================================
📋 Configuration: Claude4SonnetModel.CLAUDE_4_SONNET
🌡️  Temperature: 0.8
🧠 Memory Strategy: summarizing
💾 Prompt Caching: True
🎯 Extended Thinking: True

🗣️  Starting conversation...

👤 Question 1: Hello! Can you introduce yourself?
🤖 Claude 4 Sonnet:
----------------------------------------
Hello! I'm Claude, an AI assistant created by Anthropic...
----------------------------------------
📊 Tokens used: 156
💾 From cache: False
```

### Streaming Conversation
```
🚀 Streaming Conversation Example with Claude 4 Sonnet
============================================================
📋 Configuration: Claude4SonnetModel.CLAUDE_4_SONNET
🌊 Streaming: True
📦 Chunk size: 64

👤 Question 1: Please write a detailed explanation...
🤖 Claude 4 Sonnet (streaming):
------------------------------------------------------------
Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions without being explicitly programmed for every scenario...
------------------------------------------------------------
📊 Streaming stats:
   Chunks received: 47
   Total time: 8.23s
   Response length: 2,847 chars
   Avg chunk size: 60 chars
```

### Caching Example
```
🚀 Prompt Caching Example with Claude 4 Sonnet
============================================================
📋 Configuration:
   Model: Claude4SonnetModel.CLAUDE_4_SONNET
   💾 Caching enabled: True
   ⏰ Cache TTL: 300s
   📦 Max cache entries: 10

🔄 Testing Cache Performance
========================================
1️⃣  First call (should go to API):
   ⏱️  Response time: 3.45s
   💾 From cache: False
   📏 Response length: 1,234 chars

2️⃣  Second call (should come from cache):
   ⏱️  Response time: 0.02s
   💾 From cache: True
   📏 Response length: 1,234 chars

📊 Performance Improvement:
   ⚡ Speed increase: 172.5x faster
   💰 Cost savings: 100% (no API call)
   🎯 Response identical: True
```

## Configuration Examples

### Optimized for Conversations
```python
config = Claude4SonnetConfig.create_optimized_for_conversations()
# Features: Summarizing memory, caching, extended thinking
```

### Optimized for Analysis
```python
config = Claude4SonnetConfig.create_optimized_for_analysis()
# Features: Low temperature, extended thinking, detailed responses
```

### Optimized for Performance
```python
config = Claude4SonnetConfig.create_optimized_for_performance()
# Features: Fast responses, no memory overhead, no extended thinking
```

### Custom Configuration
```python
config = Claude4SonnetConfig(
    model_id="claude-sonnet-4-20250514",
    temperature=0.7,
    max_tokens=4096,
    enable_prompt_caching=True,
    enable_extended_thinking=True,
    memory_strategy=ConversationMemoryStrategy.SUMMARIZING,
    streaming=True,
    max_retries=3
)
```

## Troubleshooting

### Common Issues

1. **AWS Credentials Not Found**
   ```
   ❌ AWS Bedrock connection failed: NoCredentialsError
   ```
   **Solution:** Set AWS credentials using environment variables or AWS profile

2. **Bedrock Access Denied**
   ```
   ❌ AWS Bedrock connection failed: AccessDenied
   ```
   **Solution:** Request access to Claude 4 Sonnet model in AWS Bedrock console

3. **Model Not Available**
   ```
   ❌ Model not found: claude-sonnet-4-20250514
   ```
   **Solution:** Check model availability in your AWS region

4. **Strands SDK Not Installed**
   ```
   ❌ Strands Agent SDK not available
   ```
   **Solution:** Install with `pip install strands-agents`

### Debug Mode

Enable debug logging to see detailed information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Without AWS

Run the driver test suite to verify installation:

```bash
cd jesse-framework-mcp
uv run python test_strands_driver.py
```

## Integration with JESSE MCP Server

These examples demonstrate standalone usage. For integration with the JESSE MCP Server:

```python
# In your MCP server code
from llm.claude4_driver import StrandsClaude4Driver, Claude4SonnetConfig

class JESSEMCPServer:
    def __init__(self):
        config = Claude4SonnetConfig.create_optimized_for_conversations()
        self.claude_driver = StrandsClaude4Driver(config)
    
    async def handle_user_message(self, message: str, session_id: str):
        response = await self.claude_driver.send_message(message, session_id)
        return response.content
```

## Performance Tips

1. **Enable Caching** for repeated queries
2. **Use Streaming** for better user experience
3. **Choose Appropriate Memory Strategy** based on use case
4. **Monitor Token Usage** to optimize costs
5. **Configure Retries** for production reliability

## Support

For issues with the driver or examples:
1. Check the logs for detailed error messages
2. Verify AWS credentials and permissions
3. Ensure Bedrock model access is enabled
4. Review the comprehensive README in the parent directory

<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/llm/strands_agent_driver/conversation.py -->
<!-- Cached On: 2025-07-05T14:23:20.420341 -->
<!-- Source Modified: 2025-07-04T17:45:56.408845 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements comprehensive conversation management capabilities with intelligent caching and memory management strategies for Claude 4 Sonnet interactions, providing conversation persistence, context tracking, prompt caching for performance optimization, and multiple memory management approaches including summarizing, sliding window, and null strategies. The module enables developers to maintain conversation state across interactions while optimizing performance through intelligent caching and managing token limits through configurable memory strategies. Key semantic entities include `ConversationManager` class for session and cache management, `PromptCache` class for in-memory response caching with TTL and LRU eviction, core methods `start_conversation()`, `add_message()`, `get_conversation_messages()`, `get_conversation_context()`, `check_cached_response()`, `cache_response()`, `clear_conversation()`, and `clear_all_conversations()`, memory management methods `_manage_conversation_memory()`, `_summarize_conversation()`, and `_apply_sliding_window()`, cache management methods `get()`, `set()`, `clear()`, and `stats()`, utility methods `_generate_key()`, `_is_expired()`, `_evict_expired()`, `_evict_lru()`, `_estimate_tokens()`, `_create_summary_text()`, and `_generate_config_hash()`, `ConversationMemoryStrategy` enum integration with `SUMMARIZING`, `SLIDING_WINDOW`, and `NULL` options, exception classes `ConversationError`, `CacheError`, and `TokenLimitError`, configuration integration through `Claude4SonnetConfig` and `ConversationContext` dataclasses, and comprehensive statistics tracking with cache hit rates, token usage, and conversation metrics. The system implements async-first architecture with in-memory storage, SHA-256 hashing for cache keys, and intelligent memory management based on token limits and conversation length.

##### Main Components

The file contains two primary classes providing comprehensive conversation and caching management capabilities. The `PromptCache` class implements an in-memory cache with TTL expiration and LRU eviction policies, including methods for key generation, expiration checking, cache eviction, response storage and retrieval, statistics tracking, and cache clearing. The `ConversationManager` class serves as the main orchestrator for conversation lifecycle management, integrating conversation persistence, message tracking, memory management strategies, cache integration, and statistics collection. The module includes comprehensive utility methods for token estimation, conversation summarization, sliding window memory management, configuration hashing, and error handling. Both classes implement async interfaces for non-blocking operation and include detailed logging for operational visibility and debugging support.

###### Architecture & Design

The architecture implements a layered design pattern with clear separation between caching logic and conversation management, following composition over inheritance principles with the ConversationManager integrating PromptCache functionality. The design emphasizes performance optimization through intelligent caching with configurable TTL and size limits, memory management through multiple strategies based on conversation length and token usage, and scalability through in-memory storage with efficient eviction policies. Key design patterns include the strategy pattern for memory management with pluggable algorithms, cache-aside pattern for prompt response caching, factory pattern for conversation context creation, observer pattern for conversation state updates, and template method pattern for memory management workflows. The system uses dependency injection for configuration management, composition for cache integration, and async patterns for non-blocking operations with comprehensive error handling and logging throughout.

####### Implementation Approach

The implementation uses SHA-256 hashing for cache key generation combining prompt content, conversation ID, and configuration hash for unique identification. Cache management employs TTL-based expiration with periodic cleanup and LRU eviction when cache size limits are exceeded. Memory management implements three distinct strategies: summarizing older messages when token thresholds are reached, sliding window approach keeping recent messages within token limits, and null strategy for stateless interactions. The approach implements token estimation using character-to-token ratio approximation for performance optimization. Conversation persistence uses in-memory dictionaries with conversation ID keys for fast access and message arrays for chronological ordering. Configuration hashing ensures cache invalidation when model parameters change, preventing stale responses with different settings.

######## External Dependencies & Integration Points

**→ Inbound:**
- `asyncio` (external library) - async event loop management for non-blocking conversation and cache operations
- `hashlib` (external library) - SHA-256 hashing for cache key generation and configuration fingerprinting
- `json` (external library) - configuration serialization for hash generation and data structure handling
- `time` (external library) - timestamp generation for cache TTL management and access time tracking
- `datetime` (external library) - ISO format timestamp generation for conversation tracking and message timestamping
- `typing` (external library) - comprehensive type annotations including Dict, List, Optional, Any, AsyncIterator, Tuple for type safety
- `dataclasses` (external library) - asdict function for configuration serialization and data structure conversion
- `logging` (external library) - structured logging for conversation operations, cache management, and error tracking
- `.models:Claude4SonnetConfig` - configuration class providing memory strategy settings, cache parameters, and token limits
- `.models:ConversationContext` - context dataclass for conversation metadata, token tracking, and session information
- `.models:ConversationMemoryStrategy` - enum defining memory management strategies for conversation handling
- `.exceptions:ConversationError` - conversation-specific exception for session management errors
- `.exceptions:CacheError` - cache-specific exception for storage and retrieval errors
- `.exceptions:TokenLimitError` - token limit exception for memory management constraint violations

**← Outbound:**
- Strands Claude 4 Driver components - consuming ConversationManager for session management and response caching
- Driver streaming operations - using conversation context and message history for multi-turn conversations
- Performance optimization systems - using cache statistics and hit rates for monitoring and tuning
- Memory management workflows - consuming conversation summaries and token usage data for optimization decisions
- Logging and monitoring systems - consuming conversation statistics and cache performance metrics for operational visibility

**⚡ System role and ecosystem integration:**
- **System Role**: Core conversation and cache management infrastructure for Claude 4 Sonnet driver, providing session persistence, intelligent caching, and memory management capabilities essential for multi-turn conversation support
- **Ecosystem Position**: Central support component serving the main driver with conversation state management, performance optimization through caching, and memory constraint handling for token limit compliance
- **Integration Pattern**: Used by StrandsClaude4Driver through direct instantiation and method calls, consumed by streaming operations for conversation context, and integrated with configuration management for cache behavior and memory strategy selection

######### Edge Cases & Error Handling

The system handles missing conversations through `ConversationError` exceptions with conversation ID context for debugging and automatic conversation creation in driver methods. Cache operation failures are managed through try-catch blocks with warning-level logging to prevent cache errors from disrupting conversation flow. Token limit violations trigger memory management strategies including conversation summarization and sliding window application to maintain context within limits. Cache eviction handles full cache scenarios through LRU policy implementation and expired entry cleanup to maintain performance. Configuration changes invalidate cached responses through configuration hash comparison preventing stale responses with different model parameters. Memory management edge cases include conversations with insufficient messages for summarization and token estimation accuracy limitations with fallback to conservative estimates. The system provides comprehensive logging for all error conditions with appropriate log levels and detailed context information for debugging and operational monitoring.

########## Internal Implementation Details

The cache implementation uses SHA-256 hash truncation to 16 characters for cache keys balancing uniqueness with storage efficiency. Token estimation employs a 4:1 character-to-token ratio approximation based on English text patterns for performance optimization. Memory management thresholds use configurable values including `conversation_summary_threshold` for summarization triggers and `max_context_tokens` for sliding window limits. Conversation summarization keeps the last 3 messages while summarizing older content into system messages with summary markers. Cache statistics track total entries, expired entries, active entries, maximum capacity, and TTL settings for operational monitoring. Configuration hashing includes model ID, temperature, max tokens, top_p, and top_k parameters to ensure cache invalidation when model behavior changes. The system maintains separate dictionaries for conversation contexts and message arrays enabling efficient access patterns and memory management operations.

########### Code Usage Examples

Basic conversation management demonstrates the essential pattern for session lifecycle and message tracking. This approach provides fundamental conversation persistence with automatic context updates and token tracking for memory management decisions.

```python
# Initialize conversation manager with configuration and start conversation session
from strands_agent_driver.conversation import ConversationManager
from strands_agent_driver.models import Claude4SonnetConfig

config = Claude4SonnetConfig.create_optimized_for_conversations()
manager = ConversationManager(config)

# Start conversation and add messages with automatic token tracking
context = await manager.start_conversation("chat_session_1", {"user": "developer"})
await manager.add_message("chat_session_1", "user", "Hello, Claude!")
await manager.add_message("chat_session_1", "assistant", "Hello! How can I help you today?")

# Retrieve conversation history and context for processing
messages = await manager.get_conversation_messages("chat_session_1")
context = await manager.get_conversation_context("chat_session_1")
```

Advanced caching and memory management showcases the optimization patterns for performance and resource management. This pattern demonstrates how to leverage caching for response optimization and memory strategies for token limit compliance.

```python
# Demonstrate caching and memory management with performance optimization
# Check cache before processing and store responses for future use
cached_response = await manager.check_cached_response("What is Python?", "chat_session_1")
if not cached_response:
    # Process new response and cache for future requests
    response = "Python is a high-level programming language..."
    await manager.cache_response("What is Python?", "chat_session_1", response)

# Monitor conversation statistics and cache performance
stats = manager.get_stats()
print(f"Total conversations: {stats['total_conversations']}")
print(f"Cache hit rate: {stats['cache_stats']['active_entries']}/{stats['cache_stats']['total_entries']}")

# Clear conversations when memory limits are reached
if context.is_near_limit(config):
    await manager.clear_conversation("chat_session_1")
```
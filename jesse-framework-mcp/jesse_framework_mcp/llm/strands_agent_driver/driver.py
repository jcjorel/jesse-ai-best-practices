"""
Strands Claude 4 Sonnet Driver

Main driver class for Claude 4 Sonnet integration using the Strands Agent SDK.
Provides pure asyncio interface with streaming conversation capabilities,
prompt caching, and conversation management.

This driver is designed to be completely independent from JESSE MCP Server
while providing a clean interface for integration.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, AsyncIterator, Union
from contextlib import asynccontextmanager
import time

from .models import Claude4SonnetConfig, ConversationContext
from .conversation import ConversationManager
from .exceptions import (
    StrandsDriverError,
    ConversationError,
    ModelConfigurationError,
    BedrockConnectionError,
    StreamingError,
    TokenLimitError
)

logger = logging.getLogger(__name__)

try:
    from strands import Agent
    from strands.models import BedrockModel
    STRANDS_AVAILABLE = True
    # AgentResult might not be available in some versions
    try:
        from strands.types import AgentResult
    except ImportError:
        AgentResult = None
except ImportError as e:
    logger.warning(f"Strands Agent SDK not available: {e}")
    STRANDS_AVAILABLE = False
    # Define mock classes for type checking
    Agent = None
    BedrockModel = None
    AgentResult = None


class StreamingResponse:
    """Represents a streaming response from Claude 4 Sonnet."""
    
    def __init__(self, content: str, is_complete: bool = False, metadata: Optional[Dict[str, Any]] = None):
        self.content = content
        self.is_complete = is_complete
        self.metadata = metadata or {}
        self.timestamp = time.time()


class ConversationResponse:
    """Represents a complete conversation response."""
    
    def __init__(self, content: str, conversation_id: str, tokens_used: Optional[int] = None, 
                 from_cache: bool = False, metadata: Optional[Dict[str, Any]] = None):
        self.content = content
        self.conversation_id = conversation_id
        self.tokens_used = tokens_used
        self.from_cache = from_cache
        self.metadata = metadata or {}
        self.timestamp = time.time()


class StrandsClaude4Driver:
    """
    Pure asyncio driver for Claude 4 Sonnet using Strands Agent SDK.
    
    Features:
    - Streaming conversation support
    - Prompt caching for performance
    - Multiple memory management strategies
    - Automatic retry with exponential backoff
    - Complete independence from JESSE MCP Server
    """
    
    def __init__(self, config: Optional[Claude4SonnetConfig] = None):
        if not STRANDS_AVAILABLE:
            raise ModelConfigurationError(
                "Strands Agent SDK is not available. Please install strands-agents package.",
                error_code="STRANDS_NOT_AVAILABLE"
            )
        
        self.config = config or Claude4SonnetConfig()
        self.conversation_manager = ConversationManager(self.config)
        self._agent: Optional[Agent] = None
        self._bedrock_model: Optional[BedrockModel] = None
        self._is_initialized = False
        self._lock = asyncio.Lock()
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.cleanup()
    
    async def initialize(self) -> None:
        """Initialize the driver and underlying Strands components."""
        if self._is_initialized:
            return
        
        async with self._lock:
            if self._is_initialized:
                return
            
            try:
                # Initialize Bedrock model with Claude 4 Sonnet
                model_kwargs = self.config.to_strands_model_kwargs()
                self._bedrock_model = BedrockModel(**model_kwargs)
                
                # Initialize Strands Agent with the model
                # Note: We don't use tools since we're not using MCP features
                self._agent = Agent(
                    model=self._bedrock_model,
                    tools=[]  # Empty tools list - no MCP integration
                )
                
                self._is_initialized = True
                logger.info(f"Initialized Strands Claude 4 Driver with model: {self.config.model_id}")
                
            except Exception as e:
                logger.error(f"Failed to initialize Strands Claude 4 Driver: {e}")
                raise BedrockConnectionError(
                    f"Failed to initialize Claude 4 Sonnet connection: {str(e)}",
                    region=self.config.aws_region
                ) from e
    
    async def cleanup(self) -> None:
        """Clean up resources."""
        async with self._lock:
            if self._agent:
                # Strands Agent doesn't require explicit cleanup
                self._agent = None
            if self._bedrock_model:
                self._bedrock_model = None
            self._is_initialized = False
            logger.info("Cleaned up Strands Claude 4 Driver")
    
    async def start_conversation(self, conversation_id: str, 
                               metadata: Optional[Dict[str, Any]] = None) -> ConversationContext:
        """Start a new conversation or resume an existing one."""
        if not self._is_initialized:
            await self.initialize()
        
        return await self.conversation_manager.start_conversation(conversation_id, metadata)
    
    async def send_message(self, message: str, conversation_id: str, 
                          use_cache: bool = True) -> ConversationResponse:
        """Send a message and get a complete response."""
        if not self._is_initialized:
            await self.initialize()
        
        # Check cache first if enabled
        cached_response = None
        if use_cache and self.config.enable_prompt_caching:
            cached_response = await self.conversation_manager.check_cached_response(message)
            if cached_response:
                logger.info(f"Retrieved cached response for conversation: {conversation_id}")
                return ConversationResponse(
                    content=cached_response,
                    conversation_id=conversation_id,
                    from_cache=True
                )
        
        # Get conversation context and messages
        try:
            context = await self.conversation_manager.get_conversation_context(conversation_id)
            messages = await self.conversation_manager.get_conversation_messages(conversation_id)
        except ConversationError:
            # Start new conversation if not found
            context = await self.start_conversation(conversation_id)
            messages = []
        
        # Add user message to conversation
        await self.conversation_manager.add_message(conversation_id, "user", message)
        
        # Prepare conversation prompt
        conversation_prompt = self._build_conversation_prompt(messages, message)
        
        # Send to Claude 4 Sonnet with retry logic
        response_content = await self._send_with_retry(conversation_prompt)
        
        # Add assistant response to conversation
        await self.conversation_manager.add_message(conversation_id, "assistant", response_content)
        
        # Cache the response if caching is enabled
        if use_cache and self.config.enable_prompt_caching and not cached_response:
            await self.conversation_manager.cache_response(message, response_content)
        
        return ConversationResponse(
            content=response_content,
            conversation_id=conversation_id,
            tokens_used=self.conversation_manager._estimate_tokens(response_content),
            from_cache=False
        )
    
    async def stream_conversation(self, message: str, conversation_id: str,
                                use_cache: bool = True) -> AsyncIterator[StreamingResponse]:
        """Stream a conversation response in real-time."""
        if not self._is_initialized:
            await self.initialize()
        
        # Check cache first if enabled
        if use_cache and self.config.enable_prompt_caching:
            cached_response = await self.conversation_manager.check_cached_response(message)
            if cached_response:
                logger.info(f"Streaming cached response for conversation: {conversation_id}")
                # Return cached response as single chunk
                yield StreamingResponse(
                    content=cached_response,
                    is_complete=True,
                    metadata={"from_cache": True}
                )
                return
        
        # Get conversation context and messages
        try:
            context = await self.conversation_manager.get_conversation_context(conversation_id)
            messages = await self.conversation_manager.get_conversation_messages(conversation_id)
        except ConversationError:
            # Start new conversation if not found
            context = await self.start_conversation(conversation_id)
            messages = []
        
        # Add user message to conversation
        await self.conversation_manager.add_message(conversation_id, "user", message)
        
        # Prepare conversation prompt
        conversation_prompt = self._build_conversation_prompt(messages, message)
        
        # Stream response from Claude 4 Sonnet
        full_response = ""
        async for chunk in self._stream_with_retry(conversation_prompt):
            full_response += chunk.content
            yield chunk
        
        # Add complete assistant response to conversation
        await self.conversation_manager.add_message(conversation_id, "assistant", full_response)
        
        # Cache the response if caching is enabled
        if use_cache and self.config.enable_prompt_caching:
            await self.conversation_manager.cache_response(message, full_response)
    
    def _build_conversation_prompt(self, messages: List[Dict[str, Any]], new_message: str) -> str:
        """Build a prompt from conversation history."""
        if not messages:
            return new_message
        
        # Build conversation context
        prompt_parts = []
        
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"Human: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        # Add new message
        prompt_parts.append(f"Human: {new_message}")
        prompt_parts.append("Assistant:")  # Prompt for response
        
        return "\n\n".join(prompt_parts)
    
    async def _send_with_retry(self, prompt: str) -> str:
        """Send prompt with retry logic."""
        last_exception = None
        delay = self.config.retry_delay_seconds
        
        for attempt in range(self.config.max_retries + 1):
            try:
                if not self._agent:
                    raise StrandsDriverError("Agent not initialized")
                
                # Use Strands Agent to send prompt
                result = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: self._agent(prompt)
                )
                
                if isinstance(result, str):
                    return result
                elif hasattr(result, 'content'):
                    return str(result.content)
                else:
                    return str(result)
                
            except Exception as e:
                last_exception = e
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                
                if attempt < self.config.max_retries:
                    await asyncio.sleep(delay)
                    if self.config.exponential_backoff:
                        delay *= 2
                else:
                    break
        
        # All retries failed
        raise StrandsDriverError(
            f"Failed to send message after {self.config.max_retries + 1} attempts: {last_exception}",
            error_code="MAX_RETRIES_EXCEEDED"
        ) from last_exception
    
    async def _stream_with_retry(self, prompt: str) -> AsyncIterator[StreamingResponse]:
        """Stream response with retry logic using real Strands SDK streaming."""
        if not self.config.streaming:
            # If streaming is disabled, fall back to regular send
            response = await self._send_with_retry(prompt)
            # Yield complete response as single chunk
            yield StreamingResponse(content=response, is_complete=True)
            return
        
        last_exception = None
        delay = self.config.retry_delay_seconds
        
        for attempt in range(self.config.max_retries + 1):
            try:
                if not self._agent:
                    raise StrandsDriverError("Agent not initialized")
                
                # Use real streaming from Strands Agent SDK
                accumulated_text = ""
                async for event in self._agent.stream_async(prompt):
                    # Process different types of stream events
                    if "data" in event:
                        # Real-time text data from the model
                        chunk_text = event["data"]
                        accumulated_text += chunk_text
                        yield StreamingResponse(
                            content=chunk_text,
                            is_complete=False,
                            metadata={"stream_event": "data", "total_length": len(accumulated_text)}
                        )
                    
                    elif "reasoning" in event and event.get("reasoning"):
                        # Claude 4's thinking/reasoning content
                        if "reasoningText" in event and not self.config.suppress_reasoning_output:
                            reasoning_text = event["reasoningText"]
                            yield StreamingResponse(
                                content=reasoning_text,
                                is_complete=False,
                                metadata={"stream_event": "reasoning", "type": "thinking"}
                            )
                    
                    elif "current_tool_use" in event:
                        # Tool usage events
                        tool_info = event["current_tool_use"]
                        yield StreamingResponse(
                            content="",
                            is_complete=False,
                            metadata={"stream_event": "tool_use", "tool_info": tool_info}
                        )
                
                # Send final completion event
                yield StreamingResponse(
                    content="",
                    is_complete=True,
                    metadata={"stream_event": "complete", "total_text": accumulated_text}
                )
                
                return  # Success, exit retry loop
                
            except Exception as e:
                last_exception = e
                logger.warning(f"Streaming attempt {attempt + 1} failed: {e}")
                
                if attempt < self.config.max_retries:
                    await asyncio.sleep(delay)
                    if self.config.exponential_backoff:
                        delay *= 2
                else:
                    break
        
        # All retries failed
        raise StreamingError(
            f"Failed to stream response after {self.config.max_retries + 1} attempts: {last_exception}",
            error_code="STREAMING_MAX_RETRIES_EXCEEDED"
        ) from last_exception
    
    
    async def get_conversation_stats(self, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """Get statistics for a conversation or all conversations."""
        if conversation_id:
            try:
                context = await self.conversation_manager.get_conversation_context(conversation_id)
                return {
                    "conversation_id": conversation_id,
                    "message_count": context.message_count,
                    "total_tokens": context.total_tokens,
                    "created_at": context.created_at,
                    "last_activity": context.last_activity,
                    "summary": context.summary
                }
            except ConversationError:
                raise ConversationError(f"Conversation not found: {conversation_id}")
        else:
            return self.conversation_manager.get_stats()
    
    async def clear_conversation(self, conversation_id: str) -> None:
        """Clear a specific conversation."""
        await self.conversation_manager.clear_conversation(conversation_id)
    
    async def clear_all_conversations(self) -> None:
        """Clear all conversations and cache."""
        await self.conversation_manager.clear_all_conversations()
    
    @property
    def is_initialized(self) -> bool:
        """Check if the driver is initialized."""
        return self._is_initialized
    
    @property
    def model_config(self) -> Claude4SonnetConfig:
        """Get the current model configuration."""
        return self.config


# Convenience factory functions
async def create_driver(config: Optional[Claude4SonnetConfig] = None) -> StrandsClaude4Driver:
    """Create and initialize a Strands Claude 4 Driver."""
    driver = StrandsClaude4Driver(config)
    await driver.initialize()
    return driver


@asynccontextmanager
async def conversation_session(conversation_id: str, 
                             config: Optional[Claude4SonnetConfig] = None):
    """Context manager for a conversation session."""
    async with StrandsClaude4Driver(config) as driver:
        await driver.start_conversation(conversation_id)
        yield driver

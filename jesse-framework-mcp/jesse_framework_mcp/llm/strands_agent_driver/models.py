"""
Claude 4 Sonnet Model Configuration

This module provides configuration classes and utilities for Claude 4 Sonnet
integration with Amazon Bedrock through the Strands Agent SDK.
"""

import os
from typing import Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum

from .exceptions import ModelConfigurationError


class Claude4SonnetModel(str, Enum):
    """Claude 4 Sonnet model identifiers for Amazon Bedrock."""
    
    # Claude 4 Sonnet inference profile - official ID for AWS Bedrock
    CLAUDE_4_SONNET = "us.anthropic.claude-sonnet-4-20250514-v1:0"  # Official Claude 4 Sonnet inference profile
    # Alternative regions can be added here if needed (e.g. eu.anthropic.claude-sonnet-4...)


class ConversationMemoryStrategy(str, Enum):
    """Memory management strategies for conversations."""
    
    SUMMARIZING = "summarizing"  # Summarize old messages when context limit approached
    SLIDING_WINDOW = "sliding_window"  # Keep recent N messages
    NULL = "null"  # No memory persistence


@dataclass
class Claude4SonnetConfig:
    """Configuration for Claude 4 Sonnet model integration."""
    
    # Model Configuration
    model_id: str = Claude4SonnetModel.CLAUDE_4_SONNET
    temperature: float = 0.7
    max_tokens: int = 200000  # Conservative limit for 200K token context
    top_p: float = 0.9
    top_k: int = 250
    
    # Streaming Configuration
    streaming: bool = True
    
    # AWS Configuration
    aws_region: Optional[str] = None
    aws_profile: Optional[str] = None
    
    # Conversation Management
    memory_strategy: ConversationMemoryStrategy = ConversationMemoryStrategy.SUMMARIZING
    max_context_tokens: int = 180000  # Conservative limit for 200K token context
    conversation_summary_threshold: int = 150000  # When to start summarizing
    
    # Caching Configuration
    enable_prompt_caching: bool = True
    cache_ttl_seconds: int = 3600  # 1 hour default
    max_cache_entries: int = 100
    
    # Retry Configuration
    max_retries: int = 3
    retry_delay_seconds: float = 1.0
    exponential_backoff: bool = True
    
    # Advanced Claude 4 Features
    enable_extended_thinking: bool = True  # Enable Claude 4's extended thinking mode
    thinking_timeout_seconds: int = 480  # 8 minutes max for extended thinking
    enable_tool_use: bool = False  # Disable by default since we're not using MCP
    suppress_reasoning_output: bool = True  # Suppress Claude 4's reasoning/thinking output from console
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        self._validate_config()
        self._set_aws_defaults()
    
    def _validate_config(self):
        """Validate configuration parameters."""
        if not (0.0 <= self.temperature <= 1.0):
            raise ModelConfigurationError(
                f"Temperature must be between 0.0 and 1.0, got {self.temperature}",
                model_id=self.model_id
            )
        
        if not (0.0 <= self.top_p <= 1.0):
            raise ModelConfigurationError(
                f"Top-p must be between 0.0 and 1.0, got {self.top_p}",
                model_id=self.model_id
            )
        
        if self.max_tokens <= 0:
            raise ModelConfigurationError(
                f"Max tokens must be positive, got {self.max_tokens}",
                model_id=self.model_id
            )
        
        if self.max_context_tokens > 200000:
            raise ModelConfigurationError(
                f"Max context tokens cannot exceed 200K for Claude 4, got {self.max_context_tokens}",
                model_id=self.model_id
            )
        
        if self.conversation_summary_threshold >= self.max_context_tokens:
            raise ModelConfigurationError(
                f"Summary threshold ({self.conversation_summary_threshold}) must be less than max context ({self.max_context_tokens})",
                model_id=self.model_id
            )
    
    def _set_aws_defaults(self):
        """Set AWS defaults from environment if not specified."""
        if self.aws_region is None:
            self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        
        if self.aws_profile is None:
            self.aws_profile = os.getenv("AWS_PROFILE")
    
    def to_bedrock_params(self) -> Dict[str, Any]:
        """Convert configuration to Bedrock model parameters."""
        return {
            "modelId": self.model_id,
            "inferenceConfig": {
                "temperature": self.temperature,
                "maxTokens": self.max_tokens,
                "topP": self.top_p,
                "topK": self.top_k
            }
        }
    
    def to_strands_model_kwargs(self) -> Dict[str, Any]:
        """Convert configuration to Strands BedrockModel kwargs."""
        kwargs = {
            "model_id": self.model_id,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "streaming": self.streaming,
            "region": self.aws_region
        }
        
        if self.aws_profile:
            kwargs["profile"] = self.aws_profile
        
        return kwargs
    
    @classmethod
    def create_optimized_for_conversations(cls, **overrides) -> "Claude4SonnetConfig":
        """Create configuration optimized for long conversations."""
        defaults = {
            "temperature": 0.8,  # Slightly more creative for conversations
            "memory_strategy": ConversationMemoryStrategy.SUMMARIZING,
            "enable_prompt_caching": True,
            "enable_extended_thinking": True,
            "max_context_tokens": 180000  # Leave room for response
        }
        defaults.update(overrides)
        return cls(**defaults)
    
    @classmethod
    def create_optimized_for_analysis(cls, **overrides) -> "Claude4SonnetConfig":
        """Create configuration optimized for analytical tasks."""
        defaults = {
            "temperature": 0.3,  # More deterministic for analysis
            "enable_extended_thinking": True,
            "thinking_timeout_seconds": 600,  # 10 minutes for complex analysis
            "max_tokens": 8192,  # Longer responses for detailed analysis
            "memory_strategy": ConversationMemoryStrategy.SLIDING_WINDOW,
            "suppress_reasoning_output": False  # Show reasoning for analysis tasks
        }
        defaults.update(overrides)
        return cls(**defaults)
    
    @classmethod
    def create_optimized_for_performance(cls, **overrides) -> "Claude4SonnetConfig":
        """Create configuration optimized for fast responses."""
        defaults = {
            "temperature": 0.5,
            "enable_extended_thinking": False,  # Disable for speed
            "max_tokens": 2048,
            "enable_prompt_caching": True,
            "memory_strategy": ConversationMemoryStrategy.NULL  # No memory overhead
        }
        defaults.update(overrides)
        return cls(**defaults)


@dataclass
class ConversationContext:
    """Context information for a conversation session."""
    
    conversation_id: str
    total_tokens: int = 0
    message_count: int = 0
    created_at: Optional[str] = None
    last_activity: Optional[str] = None
    summary: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def should_summarize(self, config: Claude4SonnetConfig) -> bool:
        """Check if conversation should be summarized based on token count."""
        return (
            config.memory_strategy == ConversationMemoryStrategy.SUMMARIZING and
            self.total_tokens >= config.conversation_summary_threshold
        )
    
    def is_near_limit(self, config: Claude4SonnetConfig, buffer_tokens: int = 10000) -> bool:
        """Check if conversation is near token limit."""
        return self.total_tokens >= (config.max_context_tokens - buffer_tokens)

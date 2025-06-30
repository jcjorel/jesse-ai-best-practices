"""
Strands Claude 4 Sonnet Driver Package

Pure asyncio implementation for Amazon Bedrock Claude 4 Sonnet integration
using the Strands Agent SDK, designed for JESSE MCP Server usage.

This package provides a complete conversation driver that:
- Uses Strands Agent SDK for Claude 4 Sonnet on Amazon Bedrock
- Implements prompt caching for performance optimization
- Provides streaming conversation support
- Maintains complete independence from JESSE MCP Server
- Offers pure asyncio interface for integration
"""

from .driver import StrandsClaude4Driver
from .conversation import ConversationManager
from .models import Claude4SonnetConfig, ConversationMemoryStrategy
from .exceptions import (
    StrandsDriverError,
    ConversationError,
    ModelConfigurationError,
    CacheError,
    BedrockConnectionError,
    StreamingError,
    TokenLimitError
)

__version__ = "0.1.0"
__author__ = "JESSE Framework"

__all__ = [
    "StrandsClaude4Driver",
    "ConversationManager", 
    "Claude4SonnetConfig",
    "ConversationMemoryStrategy",
    "StrandsDriverError",
    "ConversationError",
    "ModelConfigurationError",
    "CacheError",
    "BedrockConnectionError",
    "StreamingError",
    "TokenLimitError"
]

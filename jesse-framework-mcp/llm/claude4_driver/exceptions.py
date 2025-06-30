"""
Custom exceptions for Strands Claude 4 Sonnet Driver

This module defines specific exceptions for different error scenarios
in the Strands Agent SDK integration with Claude 4 Sonnet.
"""

from typing import Optional, Any


class StrandsDriverError(Exception):
    """Base exception for all Strands driver-related errors."""
    
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[dict] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}


class ConversationError(StrandsDriverError):
    """Exception raised for conversation management errors."""
    
    def __init__(self, message: str, conversation_id: Optional[str] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.conversation_id = conversation_id


class ModelConfigurationError(StrandsDriverError):
    """Exception raised for model configuration and initialization errors."""
    
    def __init__(self, message: str, model_id: Optional[str] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.model_id = model_id


class CacheError(StrandsDriverError):
    """Exception raised for caching-related errors."""
    
    def __init__(self, message: str, cache_key: Optional[str] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.cache_key = cache_key


class BedrockConnectionError(StrandsDriverError):
    """Exception raised for Amazon Bedrock connection issues."""
    
    def __init__(self, message: str, region: Optional[str] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.region = region


class StreamingError(StrandsDriverError):
    """Exception raised for streaming response errors."""
    
    def __init__(self, message: str, stream_position: Optional[int] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.stream_position = stream_position


class TokenLimitError(StrandsDriverError):
    """Exception raised when token limits are exceeded."""
    
    def __init__(self, message: str, current_tokens: Optional[int] = None, max_tokens: Optional[int] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.current_tokens = current_tokens
        self.max_tokens = max_tokens

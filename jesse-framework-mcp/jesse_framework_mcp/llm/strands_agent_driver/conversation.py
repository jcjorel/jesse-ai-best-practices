"""
Conversation Management with Caching

This module provides conversation management capabilities including:
- Conversation persistence and context tracking
- Prompt caching for performance optimization
- Memory management strategies (summarizing, sliding window, null)
- Token counting and context limit management
"""

import asyncio
import hashlib
import json
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, AsyncIterator, Tuple
from dataclasses import asdict
import logging

from .models import Claude4SonnetConfig, ConversationContext, ConversationMemoryStrategy
from .exceptions import ConversationError, CacheError, TokenLimitError

logger = logging.getLogger(__name__)


class PromptCache:
    """Simple in-memory cache for prompts and responses."""
    
    def __init__(self, max_entries: int = 100, ttl_seconds: int = 3600):
        self.max_entries = max_entries
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._access_times: Dict[str, float] = {}
    
    def _generate_key(self, prompt: str, conversation_id: str, config_hash: str) -> str:
        """Generate cache key from prompt, conversation_id, and configuration."""
        combined = f"{prompt}:{conversation_id}:{config_hash}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def _is_expired(self, key: str) -> bool:
        """Check if cache entry is expired."""
        if key not in self._access_times:
            return True
        return time.time() - self._access_times[key] > self.ttl_seconds
    
    def _evict_expired(self):
        """Remove expired entries from cache."""
        current_time = time.time()
        expired_keys = [
            key for key, access_time in self._access_times.items()
            if current_time - access_time > self.ttl_seconds
        ]
        for key in expired_keys:
            self._cache.pop(key, None)
            self._access_times.pop(key, None)
    
    def _evict_lru(self):
        """Evict least recently used entries if cache is full."""
        if len(self._cache) <= self.max_entries:
            return
        
        # Sort by access time and remove oldest entries
        sorted_keys = sorted(self._access_times.items(), key=lambda x: x[1])
        keys_to_remove = [key for key, _ in sorted_keys[:len(self._cache) - self.max_entries + 1]]
        
        for key in keys_to_remove:
            self._cache.pop(key, None)
            self._access_times.pop(key, None)
    
    async def get(self, prompt: str, conversation_id: str, config_hash: str) -> Optional[str]:
        """Get cached response for prompt."""
        key = self._generate_key(prompt, conversation_id, config_hash)
        
        if key not in self._cache or self._is_expired(key):
            return None
        
        self._access_times[key] = time.time()
        return self._cache[key].get("response")
    
    async def set(self, prompt: str, conversation_id: str, config_hash: str, response: str):
        """Cache response for prompt."""
        self._evict_expired()
        self._evict_lru()
        
        key = self._generate_key(prompt, conversation_id, config_hash)
        current_time = time.time()
        
        self._cache[key] = {
            "response": response,
            "created_at": current_time
        }
        self._access_times[key] = current_time
    
    def clear(self):
        """Clear all cache entries."""
        self._cache.clear()
        self._access_times.clear()
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        current_time = time.time()
        expired_count = sum(
            1 for access_time in self._access_times.values()
            if current_time - access_time > self.ttl_seconds
        )
        
        return {
            "total_entries": len(self._cache),
            "expired_entries": expired_count,
            "active_entries": len(self._cache) - expired_count,
            "max_entries": self.max_entries,
            "ttl_seconds": self.ttl_seconds
        }


class ConversationManager:
    """Manages conversation contexts, memory, and caching."""
    
    def __init__(self, config: Claude4SonnetConfig):
        self.config = config
        self.conversations: Dict[str, ConversationContext] = {}
        self.conversation_messages: Dict[str, List[Dict[str, Any]]] = {}
        
        # Initialize caching if enabled
        self.cache: Optional[PromptCache] = None
        if config.enable_prompt_caching:
            self.cache = PromptCache(
                max_entries=config.max_cache_entries,
                ttl_seconds=config.cache_ttl_seconds
            )
        
        # Generate configuration hash for cache keys
        self.config_hash = self._generate_config_hash()
    
    def _generate_config_hash(self) -> str:
        """Generate hash of configuration for cache key differentiation."""
        config_dict = {
            "model_id": self.config.model_id,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "top_p": self.config.top_p,
            "top_k": self.config.top_k
        }
        config_str = json.dumps(config_dict, sort_keys=True)
        return hashlib.sha256(config_str.encode()).hexdigest()[:8]
    
    async def start_conversation(self, conversation_id: str, metadata: Optional[Dict[str, Any]] = None) -> ConversationContext:
        """Start a new conversation or resume existing one."""
        if conversation_id in self.conversations:
            logger.info(f"Resuming conversation: {conversation_id}")
            return self.conversations[conversation_id]
        
        current_time = datetime.now(timezone.utc).isoformat()
        context = ConversationContext(
            conversation_id=conversation_id,
            created_at=current_time,
            last_activity=current_time,
            metadata=metadata or {}
        )
        
        self.conversations[conversation_id] = context
        self.conversation_messages[conversation_id] = []
        
        logger.info(f"Started new conversation: {conversation_id}")
        return context
    
    async def add_message(self, conversation_id: str, role: str, content: str, tokens: Optional[int] = None) -> None:
        """Add a message to the conversation."""
        if conversation_id not in self.conversations:
            raise ConversationError(f"Conversation not found: {conversation_id}", conversation_id=conversation_id)
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tokens": tokens or self._estimate_tokens(content)
        }
        
        self.conversation_messages[conversation_id].append(message)
        
        # Update conversation context
        context = self.conversations[conversation_id]
        context.message_count += 1
        context.total_tokens += message["tokens"]
        context.last_activity = message["timestamp"]
        
        # Check if we need to manage memory
        await self._manage_conversation_memory(conversation_id)
    
    def _estimate_tokens(self, text: str) -> int:
        """Rough estimation of token count for text."""
        # Simple estimation: ~4 characters per token for English text
        return max(1, len(text) // 4)
    
    async def _manage_conversation_memory(self, conversation_id: str) -> None:
        """Manage conversation memory based on strategy."""
        context = self.conversations[conversation_id]
        messages = self.conversation_messages[conversation_id]
        
        if self.config.memory_strategy == ConversationMemoryStrategy.NULL:
            return
        
        if context.should_summarize(self.config):
            await self._summarize_conversation(conversation_id)
        elif self.config.memory_strategy == ConversationMemoryStrategy.SLIDING_WINDOW:
            await self._apply_sliding_window(conversation_id)
    
    async def _summarize_conversation(self, conversation_id: str) -> None:
        """Summarize older messages in the conversation."""
        messages = self.conversation_messages[conversation_id]
        context = self.conversations[conversation_id]
        
        if len(messages) < 4:  # Need at least a few messages to summarize
            return
        
        # Keep the most recent messages and summarize the rest
        recent_count = 3  # Keep last 3 messages
        messages_to_summarize = messages[:-recent_count]
        recent_messages = messages[-recent_count:]
        
        if not messages_to_summarize:
            return
        
        # Create summary of older messages
        summary_text = self._create_summary_text(messages_to_summarize)
        
        # Create summary message
        summary_message = {
            "role": "system",
            "content": f"[CONVERSATION SUMMARY]: {summary_text}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tokens": self._estimate_tokens(summary_text),
            "is_summary": True
        }
        
        # Replace old messages with summary + recent messages
        self.conversation_messages[conversation_id] = [summary_message] + recent_messages
        
        # Update context
        context.summary = summary_text
        context.total_tokens = sum(msg["tokens"] for msg in self.conversation_messages[conversation_id])
        
        logger.info(f"Summarized conversation {conversation_id}: {len(messages_to_summarize)} messages -> summary")
    
    def _create_summary_text(self, messages: List[Dict[str, Any]]) -> str:
        """Create a summary of messages."""
        if not messages:
            return "No previous messages."
        
        # Extract key information from messages
        user_messages = [msg for msg in messages if msg["role"] == "user"]
        assistant_messages = [msg for msg in messages if msg["role"] == "assistant"]
        
        summary_parts = []
        
        if user_messages:
            user_topics = []
            for msg in user_messages[-3:]:  # Last 3 user messages for context
                content = msg["content"][:100]  # First 100 chars
                user_topics.append(content)
            summary_parts.append(f"User discussed: {'; '.join(user_topics)}")
        
        if assistant_messages:
            summary_parts.append(f"Assistant provided {len(assistant_messages)} responses covering the discussed topics")
        
        return ". ".join(summary_parts) + "."
    
    async def _apply_sliding_window(self, conversation_id: str) -> None:
        """Apply sliding window memory management."""
        messages = self.conversation_messages[conversation_id]
        context = self.conversations[conversation_id]
        
        if context.is_near_limit(self.config):
            # Keep only the most recent messages that fit in context
            target_tokens = self.config.max_context_tokens // 2  # Keep half the context
            
            recent_messages = []
            token_count = 0
            
            for message in reversed(messages):
                if token_count + message["tokens"] <= target_tokens:
                    recent_messages.insert(0, message)
                    token_count += message["tokens"]
                else:
                    break
            
            if len(recent_messages) < len(messages):
                self.conversation_messages[conversation_id] = recent_messages
                context.total_tokens = token_count
                logger.info(f"Applied sliding window to conversation {conversation_id}: {len(messages)} -> {len(recent_messages)} messages")
    
    async def get_conversation_messages(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Get all messages for a conversation."""
        if conversation_id not in self.conversations:
            raise ConversationError(f"Conversation not found: {conversation_id}", conversation_id=conversation_id)
        
        return self.conversation_messages[conversation_id].copy()
    
    async def get_conversation_context(self, conversation_id: str) -> ConversationContext:
        """Get conversation context."""
        if conversation_id not in self.conversations:
            raise ConversationError(f"Conversation not found: {conversation_id}", conversation_id=conversation_id)
        
        return self.conversations[conversation_id]
    
    async def check_cached_response(self, prompt: str, conversation_id: str) -> Optional[str]:
        """Check if there's a cached response for the prompt."""
        if not self.cache:
            return None
        
        try:
            return await self.cache.get(prompt, conversation_id, self.config_hash)
        except Exception as e:
            logger.warning(f"Cache retrieval error: {e}")
            return None
    
    async def cache_response(self, prompt: str, conversation_id: str, response: str) -> None:
        """Cache a response for the prompt."""
        if not self.cache:
            return
        
        try:
            await self.cache.set(prompt, conversation_id, self.config_hash, response)
        except Exception as e:
            logger.warning(f"Cache storage error: {e}")
    
    async def clear_conversation(self, conversation_id: str) -> None:
        """Clear a specific conversation."""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
        if conversation_id in self.conversation_messages:
            del self.conversation_messages[conversation_id]
        
        logger.info(f"Cleared conversation: {conversation_id}")
    
    async def clear_all_conversations(self) -> None:
        """Clear all conversations."""
        self.conversations.clear()
        self.conversation_messages.clear()
        if self.cache:
            self.cache.clear()
        
        logger.info("Cleared all conversations and cache")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get conversation manager statistics."""
        total_tokens = sum(ctx.total_tokens for ctx in self.conversations.values())
        total_messages = sum(ctx.message_count for ctx in self.conversations.values())
        
        stats = {
            "total_conversations": len(self.conversations),
            "total_messages": total_messages,
            "total_tokens": total_tokens,
            "memory_strategy": self.config.memory_strategy.value,
            "cache_enabled": self.cache is not None
        }
        
        if self.cache:
            stats["cache_stats"] = self.cache.stats()
        
        return stats

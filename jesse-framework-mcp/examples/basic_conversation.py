#!/usr/bin/env python3
"""
Basic Conversation Example with Claude 4 Sonnet Driver

This example demonstrates how to have a simple conversation with Claude 4 Sonnet
using the Strands Agent SDK through our driver.

Requirements:
- AWS credentials configured (AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY or AWS_PROFILE)
- Amazon Bedrock access with Claude 4 Sonnet model enabled
- strands-agents package installed
"""

import asyncio
import sys
import os
import logging
from pathlib import Path

# Add the llm directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "llm"))

from claude4_driver import (
    StrandsClaude4Driver, 
    Claude4SonnetConfig,
    StrandsDriverError,
    BedrockConnectionError
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def basic_conversation_example():
    """Demonstrate a basic conversation with Claude 4 Sonnet."""
    print("🚀 Basic Conversation Example with Claude 4 Sonnet")
    print("=" * 60)
    
    # Create configuration optimized for conversations
    config = Claude4SonnetConfig.create_optimized_for_conversations()
    print(f"📋 Configuration: {config.model_id}")
    print(f"🌡️  Temperature: {config.temperature}")
    print(f"🧠 Memory Strategy: {config.memory_strategy.value}")
    print(f"💾 Prompt Caching: {config.enable_prompt_caching}")
    print(f"🎯 Extended Thinking: {config.enable_extended_thinking}")
    print()
    
    try:
        async with StrandsClaude4Driver(config) as driver:
            conversation_id = "basic_example_conversation"
            
            # Start the conversation
            print("🗣️  Starting conversation...")
            await driver.start_conversation(conversation_id, {"example": "basic"})
            
            # List of questions to ask
            questions = [
                "Hello! Can you introduce yourself?",
                "What are the key benefits of using AI in software development?",
                "Can you explain what prompt caching is and why it's useful?",
                "Thank you for the conversation!"
            ]
            
            for i, question in enumerate(questions, 1):
                print(f"\n👤 Question {i}: {question}")
                print("🤖 Claude 4 Sonnet:")
                print("-" * 40)
                
                # Send message and get response
                response = await driver.send_message(question, conversation_id)
                
                print(response.content)
                print("-" * 40)
                
                # Show response metadata
                print(f"📊 Tokens used: {response.tokens_used}")
                print(f"💾 From cache: {response.from_cache}")
                
                # Small delay between questions
                if i < len(questions):
                    await asyncio.sleep(1)
            
            # Show conversation statistics
            stats = await driver.get_conversation_stats(conversation_id)
            print(f"\n📈 Conversation Statistics:")
            print(f"   Messages: {stats['message_count']}")
            print(f"   Total tokens: {stats['total_tokens']}")
            print(f"   Started: {stats['created_at']}")
            
            # Show global driver statistics
            global_stats = await driver.get_conversation_stats()
            print(f"\n🌍 Global Statistics:")
            print(f"   Total conversations: {global_stats['total_conversations']}")
            print(f"   Cache enabled: {global_stats['cache_enabled']}")
            if global_stats['cache_enabled']:
                cache_stats = global_stats['cache_stats']
                print(f"   Cache entries: {cache_stats['active_entries']}/{cache_stats['max_entries']}")
    
    except BedrockConnectionError as e:
        print(f"❌ AWS Bedrock connection failed: {e}")
        print("💡 Make sure you have:")
        print("   - Valid AWS credentials configured")
        print("   - Amazon Bedrock access enabled")
        print("   - Claude 4 Sonnet model access enabled")
        return False
        
    except StrandsDriverError as e:
        print(f"❌ Driver error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    print("\n✅ Basic conversation example completed successfully!")
    return True


async def main():
    """Main entry point."""
    print("Claude 4 Sonnet Driver - Basic Conversation Example")
    print("=" * 60)
    
    # Check AWS credentials
    if not (os.getenv("AWS_ACCESS_KEY_ID") or os.getenv("AWS_PROFILE")):
        print("⚠️  Warning: No AWS credentials detected")
        print("   Set AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY or AWS_PROFILE")
        print("   This example requires AWS Bedrock access")
        print()
    
    # Check region
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    print(f"🌍 AWS Region: {aws_region}")
    print()
    
    try:
        success = await basic_conversation_example()
        if success:
            print("\n🎉 Example completed successfully!")
        else:
            print("\n❌ Example failed. Check the error messages above.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Example interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Example failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

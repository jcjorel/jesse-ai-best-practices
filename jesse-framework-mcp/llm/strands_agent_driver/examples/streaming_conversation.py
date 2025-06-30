#!/usr/bin/env python3
"""
Streaming Conversation Example with Claude 4 Sonnet Driver

This example demonstrates real-time streaming conversation with Claude 4 Sonnet,
showing how responses are delivered in chunks as they're generated.

Requirements:
- AWS credentials configured (AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY or AWS_PROFILE)
- Amazon Bedrock access with Claude 4 Sonnet model enabled
- strands-agents package installed
"""

import asyncio
import sys
import os
import time
from pathlib import Path

# Add the llm directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from strands_agent_driver import (
    StrandsClaude4Driver, 
    Claude4SonnetConfig,
    StrandsDriverError,
    BedrockConnectionError
)


async def streaming_conversation_example():
    """Demonstrate streaming conversation with Claude 4 Sonnet."""
    print("🚀 Streaming Conversation Example with Claude 4 Sonnet")
    print("=" * 60)
    
    # Create configuration with streaming enabled
    config = Claude4SonnetConfig.create_optimized_for_conversations(
        streaming=True
    )
    
    print(f"📋 Configuration: {config.model_id}")
    print(f"🌊 Streaming: {config.streaming}")
    print(f"🧠 Extended Thinking: {config.enable_extended_thinking}")
    print(f"💾 Prompt Caching: {config.enable_prompt_caching}")
    print()
    
    try:
        async with StrandsClaude4Driver(config) as driver:
            conversation_id = "streaming_example_conversation"
            
            # Start the conversation
            print("🗣️  Starting streaming conversation...")
            await driver.start_conversation(conversation_id, {"example": "streaming"})
            
            # Questions that will generate longer responses
            questions = [
                "Please write a detailed explanation of how machine learning works, including the main types of algorithms.",
                "Can you tell me a short story about a robot learning to understand human emotions?",
                "What are the key considerations when designing a scalable web application architecture?"
            ]
            
            for i, question in enumerate(questions, 1):
                print(f"\n👤 Question {i}: {question}")
                print("🤖 Claude 4 Sonnet (streaming):")
                print("-" * 60)
                
                # Stream the response
                start_time = time.time()
                full_response = ""
                chunk_count = 0
                
                async for chunk in driver.stream_conversation(question, conversation_id):
                    # Print chunk content in real-time
                    print(chunk.content, end="", flush=True)
                    full_response += chunk.content
                    chunk_count += 1
                    
                    if chunk.is_complete:
                        break
                
                end_time = time.time()
                print("\n" + "-" * 60)
                
                # Show streaming statistics
                print(f"📊 Streaming stats:")
                print(f"   Chunks received: {chunk_count}")
                print(f"   Total time: {end_time - start_time:.2f}s")
                print(f"   Response length: {len(full_response)} chars")
                print(f"   Avg chunk size: {len(full_response) // chunk_count if chunk_count > 0 else 0} chars")
                
                # Pause between questions
                if i < len(questions):
                    print("\n⏸️  Pausing for 2 seconds...")
                    await asyncio.sleep(2)
            
            # Show final conversation statistics
            stats = await driver.get_conversation_stats(conversation_id)
            print(f"\n📈 Final Conversation Statistics:")
            print(f"   Messages: {stats['message_count']}")
            print(f"   Total tokens: {stats['total_tokens']}")
    
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
    
    print("\n✅ Streaming conversation example completed successfully!")
    return True


async def compare_streaming_vs_normal():
    """Compare streaming vs normal response times."""
    print("\n🔄 Comparing Streaming vs Normal Response")
    print("=" * 50)
    
    question = "Explain the concept of asynchronous programming in Python with examples."
    
    # Test normal response
    config_normal = Claude4SonnetConfig.create_optimized_for_conversations(streaming=False)
    
    print("📝 Testing normal response...")
    start_time = time.time()
    
    try:
        async with StrandsClaude4Driver(config_normal) as driver:
            await driver.start_conversation("normal_test")
            response = await driver.send_message(question, "normal_test")
            
        normal_time = time.time() - start_time
        print(f"⏱️  Normal response time: {normal_time:.2f}s")
        print(f"📏 Response length: {len(response.content)} chars")
        
    except Exception as e:
        print(f"❌ Normal response failed: {e}")
        return False
    
    # Test streaming response
    config_streaming = Claude4SonnetConfig.create_optimized_for_conversations(streaming=True)
    
    print("\n🌊 Testing streaming response...")
    start_time = time.time()
    first_chunk_time = None
    
    try:
        async with StrandsClaude4Driver(config_streaming) as driver:
            await driver.start_conversation("streaming_test")
            
            full_response = ""
            async for chunk in driver.stream_conversation(question, "streaming_test"):
                if first_chunk_time is None:
                    first_chunk_time = time.time() - start_time
                full_response += chunk.content
                if chunk.is_complete:
                    break
            
        streaming_time = time.time() - start_time
        print(f"⏱️  Streaming total time: {streaming_time:.2f}s")
        print(f"⚡ Time to first chunk: {first_chunk_time:.2f}s")
        print(f"📏 Response length: {len(full_response)} chars")
        
        # Show comparison
        print(f"\n📊 Comparison:")
        print(f"   Time to first content: {first_chunk_time:.2f}s vs {normal_time:.2f}s")
        print(f"   User perceives response: {first_chunk_time/normal_time*100:.1f}% faster")
        
    except Exception as e:
        print(f"❌ Streaming response failed: {e}")
        return False
    
    return True


async def main():
    """Main entry point."""
    print("Claude 4 Sonnet Driver - Streaming Conversation Example")
    print("=" * 70)
    
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
        # Run streaming example
        success = await streaming_conversation_example()
        if not success:
            print("\n❌ Streaming example failed. Check the error messages above.")
            sys.exit(1)
        
        # Run comparison
        success = await compare_streaming_vs_normal()
        if not success:
            print("\n❌ Comparison failed. Check the error messages above.")
            sys.exit(1)
            
        print("\n🎉 All streaming examples completed successfully!")
        
    except KeyboardInterrupt:
        print("\n🛑 Example interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Example failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

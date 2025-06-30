#!/usr/bin/env python3
"""
Prompt Caching Example with Claude 4 Sonnet Driver

This example demonstrates how prompt caching works to improve performance
by avoiding repeated API calls for similar questions.

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


async def caching_demonstration():
    """Demonstrate prompt caching capabilities."""
    print("🚀 Prompt Caching Example with Claude 4 Sonnet")
    print("=" * 60)
    
    # Create configuration with caching enabled
    config = Claude4SonnetConfig(
        enable_prompt_caching=True,
        cache_ttl_seconds=300,  # 5 minutes
        max_cache_entries=10,
        temperature=0.7
    )
    
    print(f"📋 Configuration:")
    print(f"   Model: {config.model_id}")
    print(f"   💾 Caching enabled: {config.enable_prompt_caching}")
    print(f"   ⏰ Cache TTL: {config.cache_ttl_seconds}s")
    print(f"   📦 Max cache entries: {config.max_cache_entries}")
    print()
    
    try:
        async with StrandsClaude4Driver(config) as driver:
            conversation_id = "caching_example_conversation"
            await driver.start_conversation(conversation_id, {"example": "caching"})
            
            # Test question that we'll ask multiple times
            test_question = "What are the main principles of object-oriented programming?"
            
            print("🔄 Testing Cache Performance")
            print("=" * 40)
            
            # First call - should go to Claude 4 Sonnet
            print("1️⃣  First call (should go to API):")
            start_time = time.time()
            response1 = await driver.send_message(test_question, conversation_id)
            first_call_time = time.time() - start_time
            
            print(f"   ⏱️  Response time: {first_call_time:.2f}s")
            print(f"   💾 From cache: {response1.from_cache}")
            print(f"   📏 Response length: {len(response1.content)} chars")
            print(f"   🔤 First 100 chars: {response1.content[:100]}...")
            
            # Second call - should come from cache
            print("\n2️⃣  Second call (should come from cache):")
            start_time = time.time()
            response2 = await driver.send_message(test_question, conversation_id)
            second_call_time = time.time() - start_time
            
            print(f"   ⏱️  Response time: {second_call_time:.2f}s")
            print(f"   💾 From cache: {response2.from_cache}")
            print(f"   📏 Response length: {len(response2.content)} chars")
            print(f"   🔤 First 100 chars: {response2.content[:100]}...")
            
            # Show performance improvement
            if response2.from_cache:
                speedup = first_call_time / second_call_time if second_call_time > 0 else float('inf')
                print(f"\n📊 Performance Improvement:")
                print(f"   ⚡ Speed increase: {speedup:.1f}x faster")
                print(f"   💰 Cost savings: 100% (no API call)")
                print(f"   🎯 Response identical: {response1.content == response2.content}")
            
            # Test with slight variations
            print(f"\n🔄 Testing Cache Sensitivity")
            print("=" * 40)
            
            similar_questions = [
                "What are the main principles of object-oriented programming?",  # Identical
                "what are the main principles of object-oriented programming?",  # Different case
                "What are the main principles of OOP?",  # Abbreviated
                "Explain the main principles of object-oriented programming.",  # Different wording
            ]
            
            for i, question in enumerate(similar_questions, 1):
                print(f"\n{i}️⃣  Question: {question}")
                start_time = time.time()
                response = await driver.send_message(question, conversation_id)
                response_time = time.time() - start_time
                
                print(f"   ⏱️  Time: {response_time:.2f}s")
                print(f"   💾 From cache: {response.from_cache}")
                print(f"   🎯 Cache hit rate depends on exact question match")
            
            # Show cache statistics
            stats = await driver.get_conversation_stats()
            if stats.get('cache_enabled'):
                cache_stats = stats['cache_stats']
                print(f"\n📈 Cache Statistics:")
                print(f"   Total entries: {cache_stats['total_entries']}")
                print(f"   Active entries: {cache_stats['active_entries']}")
                print(f"   Max entries: {cache_stats['max_entries']}")
                print(f"   TTL: {cache_stats['ttl_seconds']}s")
                
            # Demonstrate cache expiration
            print(f"\n⏰ Testing Cache Expiration")
            print("=" * 40)
            print("Cache expires after 5 minutes in this example.")
            print("For demonstration, we'll clear the cache manually.")
            
            # Clear conversation to reset cache for this conversation
            await driver.clear_conversation(conversation_id)
            
            # Start fresh conversation
            await driver.start_conversation(conversation_id)
            
            print("🗑️  Cache cleared. Next call will go to API again.")
            start_time = time.time()
            response3 = await driver.send_message(test_question, conversation_id)
            third_call_time = time.time() - start_time
            
            print(f"   ⏱️  Response time: {third_call_time:.2f}s")
            print(f"   💾 From cache: {response3.from_cache}")
            print(f"   📊 Similar to first call time: {abs(first_call_time - third_call_time) < 1.0}")
    
    except BedrockConnectionError as e:
        print(f"❌ AWS Bedrock connection failed: {e}")
        return False
        
    except StrandsDriverError as e:
        print(f"❌ Driver error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    print("\n✅ Caching example completed successfully!")
    return True


async def cache_efficiency_test():
    """Test cache efficiency with multiple similar questions."""
    print("\n🧪 Cache Efficiency Test")
    print("=" * 40)
    
    # Configuration with smaller cache for testing
    config = Claude4SonnetConfig(
        enable_prompt_caching=True,
        cache_ttl_seconds=60,
        max_cache_entries=3,  # Small cache for testing eviction
        temperature=0.7
    )
    
    try:
        async with StrandsClaude4Driver(config) as driver:
            conversation_id = "cache_efficiency_test"
            await driver.start_conversation(conversation_id)
            
            # Questions that should be cached
            questions = [
                "What is Python?",
                "What is JavaScript?", 
                "What is Java?",
                "What is C++?",
                "What is Python?",  # Repeat - should hit cache
                "What is Go?",      # Should evict oldest entry
                "What is JavaScript?", # May or may not hit cache
            ]
            
            cache_hits = 0
            api_calls = 0
            
            for i, question in enumerate(questions, 1):
                print(f"\n{i}️⃣  Asking: {question}")
                
                start_time = time.time()
                response = await driver.send_message(question, conversation_id)
                response_time = time.time() - start_time
                
                if response.from_cache:
                    cache_hits += 1
                    print(f"   💾 Cache hit! ({response_time:.3f}s)")
                else:
                    api_calls += 1
                    print(f"   🌐 API call ({response_time:.3f}s)")
            
            print(f"\n📊 Cache Efficiency Results:")
            print(f"   Cache hits: {cache_hits}")
            print(f"   API calls: {api_calls}")
            print(f"   Cache hit rate: {cache_hits/(cache_hits + api_calls)*100:.1f}%")
            
            # Show final cache stats
            stats = await driver.get_conversation_stats()
            if stats.get('cache_enabled'):
                cache_stats = stats['cache_stats']
                print(f"   Final cache entries: {cache_stats['active_entries']}/{cache_stats['max_entries']}")
    
    except Exception as e:
        print(f"❌ Cache efficiency test failed: {e}")
        return False
    
    return True


async def main():
    """Main entry point."""
    print("Claude 4 Sonnet Driver - Prompt Caching Example")
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
        # Run caching demonstration
        success = await caching_demonstration()
        if not success:
            print("\n❌ Caching demonstration failed.")
            sys.exit(1)
        
        # Run efficiency test
        success = await cache_efficiency_test()
        if not success:
            print("\n❌ Cache efficiency test failed.")
            sys.exit(1)
            
        print("\n🎉 All caching examples completed successfully!")
        print("\n💡 Key Takeaways:")
        print("   - Prompt caching can significantly improve response times")
        print("   - Cache hits are much faster than API calls")
        print("   - Exact question matching is required for cache hits")
        print("   - Cache has TTL and size limits to manage memory")
        
    except KeyboardInterrupt:
        print("\n🛑 Example interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Example failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

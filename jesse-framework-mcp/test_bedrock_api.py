#!/usr/bin/env python3
"""
End-to-end test for Bedrock LLM driver with actual API calls.
This test requires AWS credentials and makes real Bedrock API calls.
"""

import asyncio
import sys
import traceback

async def test_real_bedrock_call():
    """Test actual Bedrock API call with the usage example."""
    print("=== Testing Real Bedrock API Call ===")
    
    try:
        from llm.bedrock.driver import BedrockDriver
        from llm.bedrock.config import BedrockConfig
        
        # Create driver with Claude 4 Sonnet
        config = BedrockConfig(enable_debug_logging=True)
        async with BedrockDriver(config) as driver:
            print("✅ Driver created and context entered")
            
            # Test the exact example from the completion
            response = await driver.chat("What is the capital of France?")
            print(f"✅ Response received: {response.message.content[:100]}...")
            print(f"✅ Model used: {response.model_id}")
            print(f"✅ Response time: {response.response_time_ms:.2f}ms")
            
            if response.usage:
                print(f"✅ Token usage: {response.usage}")
            
            return True
            
    except Exception as e:
        print(f"❌ Real API call failed: {e}")
        traceback.print_exc()
        return False

async def test_streaming_call():
    """Test streaming response functionality."""
    print("\n=== Testing Streaming Response ===")
    
    try:
        from llm.bedrock.driver import BedrockDriver
        from llm.bedrock.config import BedrockConfig
        
        config = BedrockConfig()
        async with BedrockDriver(config) as driver:
            print("User: Write a haiku about coding")
            print("Assistant: ", end="", flush=True)
            
            response_text = ""
            async for chunk in driver.chat_stream("Write a haiku about coding"):
                if chunk.chunk_type == "content_delta" and chunk.content:
                    print(chunk.content, end="", flush=True)
                    response_text += chunk.content
            
            print(f"\n✅ Complete streaming response received ({len(response_text)} chars)")
            return True
            
    except Exception as e:
        print(f"❌ Streaming test failed: {e}")
        traceback.print_exc()
        return False

async def test_conversation_continuity():
    """Test multi-turn conversation."""
    print("\n=== Testing Conversation Continuity ===")
    
    try:
        from llm.bedrock.driver import BedrockDriver
        from llm.bedrock.config import BedrockConfig
        
        config = BedrockConfig()
        async with BedrockDriver(config) as driver:
            # Start a conversation
            session_id = await driver.start_conversation(
                system_prompt="You are a helpful math tutor."
            )
            print(f"✅ Started conversation: {session_id}")
            
            # First message
            response1 = await driver.chat(
                "What is 2 + 2?", 
                session_id=session_id
            )
            print(f"Q1: What is 2 + 2?")
            print(f"A1: {response1.message.content[:50]}...")
            
            # Follow-up message
            response2 = await driver.chat(
                "Now multiply that result by 3", 
                session_id=session_id
            )
            print(f"Q2: Now multiply that result by 3")
            print(f"A2: {response2.message.content[:50]}...")
            
            # Get conversation history
            history = await driver.get_conversation_history(session_id)
            print(f"✅ Conversation history has {len(history)} messages")
            
            return True
            
    except Exception as e:
        print(f"❌ Conversation test failed: {e}")
        traceback.print_exc()
        return False

async def test_health_check():
    """Test health check functionality."""
    print("\n=== Testing Health Check ===")
    
    try:
        from llm.bedrock.driver import BedrockDriver
        from llm.bedrock.config import BedrockConfig
        
        config = BedrockConfig()
        async with BedrockDriver(config) as driver:
            health = await driver.health_check()
            print(f"✅ Health status: {health['status']}")
            print(f"✅ Client region: {health['client']['region']}")
            print(f"✅ Available models: {health['client']['available_models_count']}")
            
            # Get performance stats
            stats = await driver.get_performance_stats()
            print(f"✅ Performance stats: {stats}")
            
            return health['status'] == 'healthy'
            
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        traceback.print_exc()
        return False

async def main():
    """Run all end-to-end tests."""
    print("Bedrock LLM Driver End-to-End API Test")
    print("=" * 60)
    print("⚠️  This test makes real AWS Bedrock API calls and will incur charges!")
    print("⚠️  Ensure you have valid AWS credentials configured.")
    print("=" * 60)
    
    tests = [
        ("Real Bedrock API Call", test_real_bedrock_call),
        ("Streaming Response", test_streaming_call),
        ("Conversation Continuity", test_conversation_continuity),
        ("Health Check", test_health_check)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            print(f"\n🧪 Running {test_name}...")
            result = await test_func()
            if result:
                passed_tests += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print(f"\n{'='*60}")
    print(f"API Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All API tests passed! Bedrock driver is fully functional.")
        return True
    else:
        print("⚠️  Some API tests failed. Check AWS credentials and Bedrock access.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

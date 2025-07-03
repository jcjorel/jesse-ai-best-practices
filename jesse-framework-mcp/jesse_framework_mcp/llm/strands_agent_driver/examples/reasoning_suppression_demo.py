#!/usr/bin/env python3
"""
Reasoning Suppression Demonstration

This example demonstrates the new reasoning suppression feature in the Claude 4 Sonnet driver.
It shows the difference between having reasoning output suppressed vs. enabled.

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
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from jesse_framework_mcp.llm.strands_agent_driver import (
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


async def demonstrate_reasoning_suppression():
    """Demonstrate reasoning suppression feature."""
    print("🧠 Claude 4 Sonnet Reasoning Suppression Demonstration")
    print("=" * 60)
    
    # Test question that would typically trigger Claude's thinking process
    test_question = "What are the pros and cons of using microservices architecture versus monolithic architecture? Please think through this carefully."
    
    print("📝 Test Question:")
    print(f"   {test_question}")
    print()
    
    # Configuration 1: Suppress reasoning (default for conversations)
    print("🤫 Testing with Reasoning SUPPRESSED (Default for Conversations)")
    print("-" * 60)
    config_suppressed = Claude4SonnetConfig.create_optimized_for_conversations()
    print(f"Configuration: suppress_reasoning_output = {config_suppressed.suppress_reasoning_output}")
    
    try:
        async with StrandsClaude4Driver(config_suppressed) as driver:
            conversation_id = "reasoning_demo_suppressed"
            
            print("🗣️  Starting conversation with reasoning suppressed...")
            await driver.start_conversation(conversation_id)
            
            print("🤖 Claude 4 Response (Reasoning Suppressed):")
            print("-" * 40)
            
            # Stream the response to see what gets output
            response_chunks = []
            async for chunk in driver.stream_conversation(test_question, conversation_id):
                if chunk.content:
                    response_chunks.append(chunk.content)
                    print(chunk.content, end="", flush=True)
                
                # Check metadata for reasoning events
                if chunk.metadata.get("stream_event") == "reasoning":
                    print(f"\n[REASONING DETECTED BUT SUPPRESSED: {chunk.metadata.get('type', 'unknown')}]")
            
            print("\n" + "-" * 40)
            print(f"✅ Complete response received ({len(''.join(response_chunks))} characters)")
            
    except Exception as e:
        print(f"❌ Error with suppressed reasoning: {e}")
        return False
    
    print("\n" + "=" * 60)
    
    # Configuration 2: Show reasoning (default for analysis)
    print("🔍 Testing with Reasoning ENABLED (Default for Analysis)")
    print("-" * 60)
    config_enabled = Claude4SonnetConfig.create_optimized_for_analysis()
    print(f"Configuration: suppress_reasoning_output = {config_enabled.suppress_reasoning_output}")
    
    try:
        async with StrandsClaude4Driver(config_enabled) as driver:
            conversation_id = "reasoning_demo_enabled"
            
            print("🗣️  Starting conversation with reasoning enabled...")
            await driver.start_conversation(conversation_id)
            
            print("🤖 Claude 4 Response (Reasoning Enabled):")
            print("-" * 40)
            
            # Stream the response to see reasoning output
            response_chunks = []
            reasoning_chunks = []
            async for chunk in driver.stream_conversation(test_question, conversation_id):
                if chunk.content:
                    if chunk.metadata.get("stream_event") == "reasoning":
                        # This is reasoning content
                        reasoning_chunks.append(chunk.content)
                        print(f"[THINKING: {chunk.content}]", flush=True)
                    else:
                        # This is the actual response
                        response_chunks.append(chunk.content)
                        print(chunk.content, end="", flush=True)
            
            print("\n" + "-" * 40)
            print(f"✅ Complete response received:")
            print(f"   - Response: {len(''.join(response_chunks))} characters")
            print(f"   - Reasoning: {len(''.join(reasoning_chunks))} characters")
            
    except Exception as e:
        print(f"❌ Error with enabled reasoning: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print("- With reasoning SUPPRESSED: Only the final answer is shown (cleaner console output)")
    print("- With reasoning ENABLED: Both thinking process and final answer are shown (useful for analysis)")
    print("- Default behavior: Conversations suppress reasoning, Analysis enables reasoning")
    print("- You can override this setting in any configuration as needed")
    
    return True


async def demonstrate_manual_configuration():
    """Show how to manually configure reasoning suppression."""
    print("\n🔧 Manual Configuration Examples")
    print("=" * 60)
    
    # Example 1: Explicitly suppress reasoning
    config1 = Claude4SonnetConfig(
        suppress_reasoning_output=True,
        temperature=0.7
    )
    print(f"Example 1 - Explicit suppression: suppress_reasoning_output = {config1.suppress_reasoning_output}")
    
    # Example 2: Explicitly enable reasoning
    config2 = Claude4SonnetConfig(
        suppress_reasoning_output=False,
        temperature=0.3,
        enable_extended_thinking=True
    )
    print(f"Example 2 - Explicit enabling: suppress_reasoning_output = {config2.suppress_reasoning_output}")
    
    # Example 3: Override factory defaults
    config3 = Claude4SonnetConfig.create_optimized_for_conversations(
        suppress_reasoning_output=False  # Override default
    )
    print(f"Example 3 - Override conversation default: suppress_reasoning_output = {config3.suppress_reasoning_output}")
    
    config4 = Claude4SonnetConfig.create_optimized_for_analysis(
        suppress_reasoning_output=True  # Override default
    )
    print(f"Example 4 - Override analysis default: suppress_reasoning_output = {config4.suppress_reasoning_output}")


async def main():
    """Main entry point."""
    print("Claude 4 Sonnet Driver - Reasoning Suppression Demo")
    print("=" * 60)
    
    # Check AWS credentials
    if not (os.getenv("AWS_ACCESS_KEY_ID") or os.getenv("AWS_PROFILE")):
        print("⚠️  Warning: No AWS credentials detected")
        print("   Set AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY or AWS_PROFILE")
        print("   This demo requires AWS Bedrock access")
        print()
    
    # Check region
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    print(f"🌍 AWS Region: {aws_region}")
    print()
    
    try:
        # Demonstrate manual configuration first
        await demonstrate_manual_configuration()
        
        # Then demonstrate actual reasoning suppression
        # Note: This requires actual AWS Bedrock access to see reasoning output
        print("\n" + "=" * 60)
        print("🚀 Live Demonstration")
        print("=" * 60)
        print("Note: The following demonstration requires valid AWS Bedrock access")
        print("      If you don't have access, you'll see connection errors but")
        print("      the configuration examples above show how the feature works.")
        print()
        
        success = await demonstrate_reasoning_suppression()
        if success:
            print("\n🎉 Reasoning suppression demonstration completed successfully!")
        else:
            print("\n❌ Demonstration failed. This is expected without proper AWS Bedrock access.")
            print("   The configuration examples above show how the feature works.")
            
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("This is expected without proper AWS Bedrock access.")
        print("The configuration examples show how the feature works.")


if __name__ == "__main__":
    asyncio.run(main())

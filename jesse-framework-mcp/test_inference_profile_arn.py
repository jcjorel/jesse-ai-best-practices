#!/usr/bin/env python3
"""
Test to find and use the correct ARN for Claude 4 Sonnet inference profile.
"""

import asyncio
import sys
import json
import traceback

async def dump_inference_profile_arns():
    """Dump full inference profile details to find ARNs."""
    print("=== FINDING CLAUDE 4 SONNET INFERENCE PROFILE ARN ===")
    print("This test will extract the proper ARN for Claude 4 Sonnet inference profile")
    print("=" * 80)
    
    try:
        from llm.bedrock.async_client import AsyncBedrockClient
        from llm.bedrock.config import BedrockConfig
        
        # Create client with debug logging
        config = BedrockConfig(enable_debug_logging=True)
        client = AsyncBedrockClient(config)
        
        print(f"✅ Client created for region: {config.region}")
        
        # List all inference profiles
        print("\n🔍 Listing inference profiles to find Claude 4 Sonnet...")
        profiles = await client.list_inference_profiles()
        
        claude4_profile = None
        for profile in profiles:
            profile_id = profile.get('inferenceProfileId', '')
            if 'claude-sonnet-4' in profile_id:
                claude4_profile = profile
                break
        
        if not claude4_profile:
            print("❌ Claude 4 Sonnet profile not found!")
            return None
        
        profile_id = claude4_profile.get('inferenceProfileId', '')
        print(f"✅ Found Claude 4 Sonnet profile: {profile_id}")
        
        # Get full profile details
        print(f"\n🔍 Getting full details for profile: {profile_id}")
        profile_details = await client.get_inference_profile(profile_id)
        
        print(f"\n📋 FULL PROFILE RESPONSE:")
        print(json.dumps(profile_details, indent=2, default=str))
        
        # Extract ARN if available
        arn_fields = ['inferenceProfileArn', 'arn', 'inferenceProfileId']
        profile_arn = None
        
        for field in arn_fields:
            if field in profile_details:
                value = profile_details[field]
                if value and ('arn:aws:bedrock' in value or field == 'inferenceProfileId'):
                    profile_arn = value
                    print(f"\n✅ Found ARN/ID in field '{field}': {profile_arn}")
                    break
        
        if not profile_arn:
            print("⚠️  No ARN found, trying to construct from available data...")
            # Try to construct ARN from available information
            region = config.region
            profile_id = profile_details.get('inferenceProfileId', '')
            
            # We need account ID - let's try to get it from the response metadata
            if 'ResponseMetadata' in profile_details:
                print(f"Response metadata: {profile_details['ResponseMetadata']}")
            
            # For now, let's try the profile ID directly
            profile_arn = profile_id
        
        return profile_arn
        
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        return None

async def test_claude4_with_arn(profile_arn: str):
    """Test Claude 4 Sonnet using the proper ARN."""
    print(f"\n" + "="*80)
    print("TESTING CLAUDE 4 SONNET WITH ARN")
    print("="*80)
    
    try:
        from llm.bedrock.driver import BedrockDriver
        from llm.bedrock.config import BedrockConfig
        
        print(f"🧪 Testing with ARN: {profile_arn}")
        
        # Create config with the ARN
        config = BedrockConfig(
            model_id=profile_arn,
            enable_debug_logging=True,
            enforce_claude4_only=False  # Disable for now to test
        )
        
        print(f"✅ Config created with ARN: {config.model_id}")
        
        async with BedrockDriver(config) as driver:
            print("✅ Driver created successfully")
            
            # Test simple chat
            print("🧪 Testing simple chat...")
            response = await driver.chat("What is 2+2? Answer briefly.")
            
            print(f"✅ SUCCESS! Claude 4 Sonnet response: {response.message.content[:100]}...")
            print(f"✅ Model used: {response.model_id}")
            print(f"✅ Response time: {response.response_time_ms:.2f}ms")
            
            if response.usage:
                print(f"✅ Token usage: {response.usage}")
            
            return True
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        if "You don't have access" in str(e):
            print("📋 This suggests the ARN format may still be incorrect")
            print("   or the account doesn't have access to Claude 4 Sonnet")
        return False

async def main():
    """Find and test Claude 4 Sonnet ARN."""
    print("Claude 4 Sonnet ARN Discovery and Testing")
    print("=" * 80)
    
    # Step 1: Find the ARN
    profile_arn = await dump_inference_profile_arns()
    
    if not profile_arn:
        print("❌ Could not find Claude 4 Sonnet ARN")
        return False
    
    # Step 2: Test with the ARN
    success = await test_claude4_with_arn(profile_arn)
    
    print(f"\n" + "="*80)
    print("FINAL RESULT")
    print("="*80)
    
    if success:
        print(f"✅ SUCCESS! Claude 4 Sonnet is working with ARN: {profile_arn}")
        print(f"\n📋 RECOMMENDATIONS:")
        print(f"   • Update model configuration to use ARN: {profile_arn}")
        print(f"   • Claude 4 Sonnet is now ready for production use")
        print(f"   • All tests should pass with this ARN")
    else:
        print(f"❌ FAILED: Claude 4 Sonnet not accessible with ARN: {profile_arn}")
        print(f"\n📋 NEXT STEPS:")
        print(f"   • Check AWS account access to Claude 4 Sonnet")
        print(f"   • Verify ARN format is correct")
        print(f"   • Consider using Claude 3.5 Sonnet as alternative")
    
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

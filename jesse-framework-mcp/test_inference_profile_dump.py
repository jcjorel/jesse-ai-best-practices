#!/usr/bin/env python3
"""
Comprehensive test to dump all available Bedrock inference profiles with full details.
This will help identify the correct Claude 4 Sonnet inference profile.
"""

import asyncio
import sys
import json
import traceback

async def dump_all_inference_profiles():
    """Dump all available inference profiles with comprehensive details."""
    print("=== COMPREHENSIVE BEDROCK INFERENCE PROFILE DUMP ===")
    print("This test will show ALL available inference profiles with complete details")
    print("=" * 80)
    
    try:
        from llm.bedrock.async_client import AsyncBedrockClient
        from llm.bedrock.config import BedrockConfig
        
        # Create client with debug logging
        config = BedrockConfig(enable_debug_logging=True)
        client = AsyncBedrockClient(config)
        
        print(f"✅ Client created for region: {config.region}")
        print(f"✅ Current AWS Identity: {config.aws_profile}")
        
        # List all inference profiles
        print("\n" + "="*80)
        print("LISTING ALL INFERENCE PROFILES")
        print("="*80)
        
        profiles = await client.list_inference_profiles()
        print(f"✅ Found {len(profiles)} total inference profiles")
        
        # Group profiles by provider
        anthropic_profiles = []
        amazon_profiles = []
        meta_profiles = []
        other_profiles = []
        
        for profile in profiles:
            profile_id = profile.get('inferenceProfileId', 'Unknown')
            if 'anthropic' in profile_id.lower():
                anthropic_profiles.append(profile)
            elif 'amazon' in profile_id.lower():
                amazon_profiles.append(profile)
            elif 'meta' in profile_id.lower():
                meta_profiles.append(profile)
            else:
                other_profiles.append(profile)
        
        # Display Anthropic profiles (our primary interest)
        print(f"\n🎯 ANTHROPIC PROFILES ({len(anthropic_profiles)} found):")
        print("-" * 60)
        
        claude4_profiles = []
        claude35_profiles = []
        claude3_profiles = []
        
        for i, profile in enumerate(anthropic_profiles):
            profile_id = profile.get('inferenceProfileId', 'Unknown')
            description = profile.get('description', 'No description')
            status = profile.get('status', 'Unknown')
            profile_name = profile.get('inferenceProfileName', 'No name')
            
            print(f"\n[{i+1}] Profile ID: {profile_id}")
            print(f"    Name: {profile_name}")
            print(f"    Description: {description}")
            print(f"    Status: {status}")
            
            # Check for model information
            if 'models' in profile:
                models = profile['models']
                print(f"    Models: {len(models)} available")
                for j, model in enumerate(models):
                    model_id = model.get('modelId', 'Unknown')
                    print(f"       [{j+1}] {model_id}")
                    
                    # Categorize by Claude version
                    if 'claude-sonnet-4' in model_id:
                        claude4_profiles.append({'profile': profile, 'model': model})
                    elif 'claude-3-5-sonnet' in model_id or 'claude-3.5-sonnet' in model_id:
                        claude35_profiles.append({'profile': profile, 'model': model})
                    elif 'claude-3' in model_id:
                        claude3_profiles.append({'profile': profile, 'model': model})
            else:
                print("    Models: Not specified in profile summary")
            
            # Show additional details if available
            if 'type' in profile:
                print(f"    Type: {profile['type']}")
            if 'createdAt' in profile:
                print(f"    Created: {profile['createdAt']}")
            if 'updatedAt' in profile:
                print(f"    Updated: {profile['updatedAt']}")
        
        # Summary of Claude models found
        print(f"\n📊 CLAUDE MODEL SUMMARY:")
        print(f"   • Claude 4 Sonnet profiles: {len(claude4_profiles)}")
        print(f"   • Claude 3.5 Sonnet profiles: {len(claude35_profiles)}")
        print(f"   • Claude 3 (other) profiles: {len(claude3_profiles)}")
        
        # Show Claude 4 Sonnet details if found
        if claude4_profiles:
            print(f"\n🎉 CLAUDE 4 SONNET PROFILES FOUND:")
            print("-" * 50)
            for i, item in enumerate(claude4_profiles):
                profile = item['profile']
                model = item['model']
                print(f"[{i+1}] Profile: {profile.get('inferenceProfileId')}")
                print(f"    Model: {model.get('modelId')}")
                print(f"    Description: {profile.get('description', 'N/A')}")
        else:
            print(f"\n❌ NO CLAUDE 4 SONNET PROFILES FOUND")
            print("   Claude 4 Sonnet may require:")
            print("   • Provisioned throughput setup")
            print("   • Custom inference profile creation")
            print("   • Different region or account access")
        
        # Show best alternatives if Claude 4 not available
        if claude35_profiles:
            print(f"\n💡 CLAUDE 3.5 SONNET ALTERNATIVES:")
            print("-" * 50)
            for i, item in enumerate(claude35_profiles):
                profile = item['profile']
                model = item['model']
                print(f"[{i+1}] Profile: {profile.get('inferenceProfileId')}")
                print(f"    Model: {model.get('modelId')}")
                print(f"    Status: RECOMMENDED ALTERNATIVE")
        
        # Display other providers briefly
        print(f"\n📋 OTHER PROVIDERS SUMMARY:")
        print(f"   • Amazon Nova profiles: {len(amazon_profiles)}")
        print(f"   • Meta Llama profiles: {len(meta_profiles)}")
        print(f"   • Other profiles: {len(other_profiles)}")
        
        # Test specific profile details
        print(f"\n🔍 DETAILED PROFILE INSPECTION:")
        print("-" * 50)
        
        # Try to get details for first few Anthropic profiles
        for i, profile in enumerate(anthropic_profiles[:3]):
            profile_id = profile.get('inferenceProfileId')
            print(f"\n[Profile {i+1}] Getting details for: {profile_id}")
            
            try:
                details = await client.get_inference_profile(profile_id)
                print(f"✅ Profile details retrieved successfully")
                
                # Show key details
                if 'inferenceProfileName' in details:
                    print(f"   Name: {details['inferenceProfileName']}")
                if 'description' in details:
                    print(f"   Description: {details['description']}")
                if 'status' in details:
                    print(f"   Status: {details['status']}")
                if 'type' in details:
                    print(f"   Type: {details['type']}")
                
                # Show models with full details
                if 'models' in details:
                    models = details['models']
                    print(f"   Models ({len(models)}):")
                    for model in models:
                        model_id = model.get('modelId', 'Unknown')
                        model_name = model.get('modelName', 'Unknown')
                        print(f"      • {model_id}")
                        if model_name != 'Unknown':
                            print(f"        Name: {model_name}")
                
            except Exception as e:
                print(f"⚠️  Could not get details: {e}")
        
        # Recommendations
        print(f"\n🎯 RECOMMENDATIONS:")
        print("-" * 30)
        
        if claude4_profiles:
            recommended_profile = claude4_profiles[0]['profile']
            recommended_model = claude4_profiles[0]['model']
            print(f"✅ USE CLAUDE 4 SONNET:")
            print(f"   Profile ID: {recommended_profile.get('inferenceProfileId')}")
            print(f"   Model ID: {recommended_model.get('modelId')}")
        elif claude35_profiles:
            recommended_profile = claude35_profiles[0]['profile']
            recommended_model = claude35_profiles[0]['model']
            print(f"💡 USE CLAUDE 3.5 SONNET (BEST ALTERNATIVE):")
            print(f"   Profile ID: {recommended_profile.get('inferenceProfileId')}")
            print(f"   Model ID: {recommended_model.get('modelId')}")
        else:
            print(f"❌ NO CLAUDE SONNET PROFILES AVAILABLE")
            print(f"   Check AWS console for model access")
        
        return profiles
        
    except Exception as e:
        print(f"❌ Profile dump failed: {e}")
        traceback.print_exc()
        return []

async def test_recommended_profile():
    """Test using the recommended profile."""
    print(f"\n" + "="*80)
    print("TESTING RECOMMENDED PROFILE")
    print("="*80)
    
    try:
        from llm.bedrock.driver import BedrockDriver
        from llm.bedrock.config import BedrockConfig
        
        # First, let's try Claude 3.5 Sonnet since it's likely available
        claude35_profile = "us.anthropic.claude-3-5-sonnet-20240620-v1:0"
        
        print(f"🧪 Testing profile: {claude35_profile}")
        
        config = BedrockConfig(
            model_id=claude35_profile,
            enable_debug_logging=True,
            enforce_claude4_only=False  # Disable enforcement for testing
        )
        
        async with BedrockDriver(config) as driver:
            print("✅ Driver created successfully")
            
            # Test simple chat
            response = await driver.chat("What is 2+2? Respond briefly.")
            print(f"✅ Chat response: {response.message.content[:100]}...")
            print(f"✅ Model used: {response.model_id}")
            print(f"✅ Response time: {response.response_time_ms:.2f}ms")
            
            if response.usage:
                print(f"✅ Token usage: {response.usage}")
            
            return True
            
    except Exception as e:
        print(f"❌ Profile test failed: {e}")
        return False

async def main():
    """Run comprehensive inference profile analysis."""
    print("Bedrock Inference Profile Comprehensive Analysis")
    print("=" * 80)
    print("This test will dump ALL available inference profiles to help identify")
    print("the correct Claude 4 Sonnet profile (or best alternative).")
    print("=" * 80)
    
    # Step 1: Dump all profiles
    profiles = await dump_all_inference_profiles()
    
    if not profiles:
        print("❌ No profiles found or error occurred")
        return False
    
    # Step 2: Test recommended profile
    test_success = await test_recommended_profile()
    
    print(f"\n" + "="*80)
    print("FINAL ANALYSIS")
    print("="*80)
    print(f"• Total profiles found: {len(profiles)}")
    print(f"• Test with available profile: {'✅ SUCCESS' if test_success else '❌ FAILED'}")
    
    if test_success:
        print(f"\n🎉 READY FOR DEVELOPMENT!")
        print(f"   • Bedrock driver is functional")
        print(f"   • Inference profiles are working")
        print(f"   • Can proceed with implementation")
    else:
        print(f"\n⚠️  NEEDS ATTENTION:")
        print(f"   • Check AWS account access")
        print(f"   • Verify Bedrock model permissions")
        print(f"   • Consider different region")
    
    return test_success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

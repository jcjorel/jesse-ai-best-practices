#!/usr/bin/env python3
"""
Simple test script to verify Bedrock LLM driver imports and basic functionality.
This test doesn't require AWS credentials or pytest - just verifies the code structure.
"""

import sys
import traceback

def test_imports():
    """Test that all Bedrock driver modules can be imported."""
    print("=== Testing Bedrock Driver Imports ===")
    
    # Test individual module imports
    modules_to_test = [
        ('llm', 'Main LLM package'),
        ('llm.bedrock', 'Bedrock package'),
        ('llm.bedrock.config', 'Configuration module'),
        ('llm.bedrock.exceptions', 'Exception classes'),
        ('llm.bedrock.models', 'Model specifications'),
        ('llm.bedrock.conversation', 'Conversation management'),
        ('llm.bedrock.async_client', 'Async client'),
        ('llm.bedrock.driver', 'Main driver')
    ]
    
    failed_imports = []
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name} - {description}")
        except Exception as e:
            print(f"❌ {module_name} - {description}: {e}")
            failed_imports.append((module_name, str(e)))
    
    return len(failed_imports) == 0

def test_basic_instantiation():
    """Test basic class instantiation without AWS calls."""
    print("\n=== Testing Basic Class Instantiation ===")
    
    try:
        from llm.bedrock.config import BedrockConfig
        from llm.bedrock.conversation import ConversationManager
        from llm.bedrock.models import get_model_config, CLAUDE_4_SONNET
        
        # Test config creation
        config = BedrockConfig()
        print(f"✅ BedrockConfig created - Model: {config.model_id}, Region: {config.region}")
        
        # Test conversation manager
        conversation_mgr = ConversationManager()
        print(f"✅ ConversationManager created - Max sessions: {conversation_mgr.max_sessions}")
        
        # Test model config lookup
        model_config = get_model_config(CLAUDE_4_SONNET.model_id)
        if model_config:
            print(f"✅ Model config found - {model_config.model_id}, Supports streaming: {model_config.supports_streaming}")
        else:
            print("❌ Model config not found")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Basic instantiation failed: {e}")
        traceback.print_exc()
        return False

def test_driver_creation():
    """Test driver creation without making AWS calls."""
    print("\n=== Testing Driver Creation ===")
    
    try:
        from llm.bedrock.driver import BedrockDriver
        from llm.bedrock.config import BedrockConfig
        
        # Create config with debug mode
        config = BedrockConfig(enable_debug_logging=True)
        
        # Create driver (this should not make any AWS calls)
        driver = BedrockDriver(config)
        print(f"✅ BedrockDriver created successfully")
        print(f"   - Model ID: {driver._config.model_id}")
        print(f"   - Region: {driver._config.region}")
        print(f"   - Debug logging: {driver._config.enable_debug_logging}")
        
        return True
        
    except Exception as e:
        print(f"❌ Driver creation failed: {e}")
        traceback.print_exc()
        return False

def test_model_info():
    """Test model information and configuration."""
    print("\n=== Testing Model Information ===")
    
    try:
        from llm.bedrock.models import list_available_models, model_registry
        
        all_models = list_available_models()
        print(f"✅ Found {len(all_models)} total models")
        
        anthropic_models = model_registry.find_models_by_provider("anthropic")
        print(f"✅ Found {len(anthropic_models)} Anthropic models")
        
        if anthropic_models:
            claude_model = anthropic_models[0]
            print(f"   - Sample model: {claude_model.model_id}")
            print(f"   - Max tokens: {claude_model.max_tokens}")
            print(f"   - Supports streaming: {claude_model.supports_streaming}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model info test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("Bedrock LLM Driver Basic Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Basic Instantiation Test", test_basic_instantiation),
        ("Driver Creation Test", test_driver_creation),
        ("Model Information Test", test_model_info)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed_tests += 1
                print(f"\n✅ {test_name} PASSED")
            else:
                print(f"\n❌ {test_name} FAILED")
        except Exception as e:
            print(f"\n❌ {test_name} FAILED with exception: {e}")
            traceback.print_exc()
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Bedrock driver is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

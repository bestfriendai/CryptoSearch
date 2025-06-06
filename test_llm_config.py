#!/usr/bin/env python3
"""
Test script to verify LLM configuration is working correctly.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_environment_variables():
    """Test that environment variables are loaded correctly."""
    print("=== Testing Environment Variables ===")
    
    # Check OpenRouter API key
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    print(f"OPENROUTER_API_KEY: {'✓ Set' if openrouter_key else '✗ Not set'}")
    
    # Check model configurations
    basic_model = os.getenv("BASIC_MODEL__MODEL")
    basic_api_key = os.getenv("BASIC_MODEL__OPENAI_API_KEY")
    basic_base_url = os.getenv("BASIC_MODEL__BASE_URL")
    
    print(f"BASIC_MODEL__MODEL: {basic_model}")
    print(f"BASIC_MODEL__OPENAI_API_KEY: {'✓ Set' if basic_api_key else '✗ Not set'}")
    print(f"BASIC_MODEL__BASE_URL: {basic_base_url}")
    
    return all([openrouter_key, basic_model, basic_api_key, basic_base_url])

def test_config_loading():
    """Test that configuration loading works."""
    print("\n=== Testing Configuration Loading ===")
    
    try:
        from src.config.loader import load_yaml_config, clear_config_cache
        from src.llms.llm import _get_env_llm_conf, clear_llm_cache
        
        # Clear caches to ensure fresh load
        clear_config_cache()
        clear_llm_cache()
        
        # Test YAML config loading
        conf_path = str(project_root / "conf.yaml")
        config = load_yaml_config(conf_path)
        print(f"YAML config loaded: {'✓' if config else '✗'}")
        
        if config:
            basic_model_config = config.get("BASIC_MODEL", {})
            print(f"BASIC_MODEL config: {basic_model_config}")
        
        # Test environment variable loading
        env_conf = _get_env_llm_conf("basic")
        print(f"Environment config for basic model: {env_conf}")
        
        return True
        
    except Exception as e:
        print(f"✗ Configuration loading failed: {e}")
        return False

def test_llm_initialization():
    """Test that LLM can be initialized with the configuration."""
    print("\n=== Testing LLM Initialization ===")
    
    try:
        from src.llms.llm import get_llm_by_type, clear_llm_cache
        from src.config.loader import clear_config_cache
        
        # Clear caches to ensure fresh load
        clear_config_cache()
        clear_llm_cache()
        
        # Try to initialize basic LLM
        basic_llm = get_llm_by_type("basic")
        print(f"Basic LLM initialized: ✓")
        print(f"LLM model: {basic_llm.model_name}")
        print(f"LLM base URL: {basic_llm.openai_api_base}")
        
        return True
        
    except Exception as e:
        print(f"✗ LLM initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_llm_call():
    """Test a simple LLM call to verify authentication."""
    print("\n=== Testing Simple LLM Call ===")
    
    try:
        from src.llms.llm import get_llm_by_type
        
        basic_llm = get_llm_by_type("basic")
        
        # Make a simple test call
        response = basic_llm.invoke("Hello! Please respond with just 'OK' to confirm you're working.")
        print(f"LLM response: {response.content}")
        print("✓ LLM call successful")
        
        return True
        
    except Exception as e:
        print(f"✗ LLM call failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("Testing LLM Configuration\n")
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Configuration Loading", test_config_loading),
        ("LLM Initialization", test_llm_initialization),
        ("Simple LLM Call", test_simple_llm_call),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n=== Test Results ===")
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    print(f"\nOverall: {'✓ ALL TESTS PASSED' if all_passed else '✗ SOME TESTS FAILED'}")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

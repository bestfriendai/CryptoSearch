#!/usr/bin/env python3
"""
Debug script to check environment variables and configuration
"""
import os
import sys
from pathlib import Path

def check_environment_variables():
    """Check all relevant environment variables"""
    print("=== Environment Variables Debug ===")
    
    # Check OpenRouter API key
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    print(f"OPENROUTER_API_KEY: {'✓ Set' if openrouter_key else '✗ Not set'}")
    if openrouter_key:
        print(f"  Value: {openrouter_key[:10]}...{openrouter_key[-4:] if len(openrouter_key) > 14 else openrouter_key}")
    
    # Check model-specific environment variables
    model_vars = [
        "BASIC_MODEL__MODEL",
        "BASIC_MODEL__OPENAI_API_KEY", 
        "BASIC_MODEL__BASE_URL",
        "REASONING_MODEL__MODEL",
        "REASONING_MODEL__OPENAI_API_KEY",
        "REASONING_MODEL__BASE_URL"
    ]
    
    print("\n=== Model Configuration Variables ===")
    for var in model_vars:
        value = os.getenv(var)
        if "API_KEY" in var and value:
            print(f"{var}: ✓ Set ({value[:10]}...{value[-4:] if len(value) > 14 else value})")
        else:
            print(f"{var}: {'✓ ' + value if value else '✗ Not set'}")
    
    # Check all environment variables starting with relevant prefixes
    print("\n=== All Relevant Environment Variables ===")
    relevant_prefixes = ["OPENROUTER", "BASIC_MODEL", "REASONING_MODEL", "VISION_MODEL"]
    for key, value in sorted(os.environ.items()):
        if any(key.startswith(prefix) for prefix in relevant_prefixes):
            if "API_KEY" in key or "KEY" in key:
                print(f"{key}: {'✓ Set' if value else '✗ Not set'}")
            else:
                print(f"{key}: {value}")

def check_config_file():
    """Check if config file exists and what it contains"""
    print("\n=== Configuration File Check ===")
    
    config_path = Path(__file__).parent / "conf.yaml"
    print(f"Looking for config at: {config_path}")
    print(f"Config file exists: {config_path.exists()}")
    
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                content = f.read()
            print(f"Config file content:\n{content}")
        except Exception as e:
            print(f"Error reading config file: {e}")

def test_llm_config():
    """Test LLM configuration loading"""
    print("\n=== Testing LLM Configuration ===")
    
    try:
        # Add the src directory to Python path
        src_path = Path(__file__).parent / "src"
        sys.path.insert(0, str(src_path))
        
        from llms.llm import _get_env_llm_conf
        
        # Test basic model configuration
        basic_conf = _get_env_llm_conf("basic")
        print(f"Basic model env config: {basic_conf}")
        
        reasoning_conf = _get_env_llm_conf("reasoning")
        print(f"Reasoning model env config: {reasoning_conf}")
        
    except Exception as e:
        print(f"Error testing LLM config: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_environment_variables()
    check_config_file()
    test_llm_config()

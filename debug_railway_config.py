#!/usr/bin/env python3
"""
Debug script to check Railway configuration in detail.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def debug_environment_variables():
    """Debug environment variables in detail."""
    print("🔍 Debugging Environment Variables")
    print("=" * 50)
    
    # Check all environment variables that start with our prefixes
    relevant_vars = {}
    for key, value in os.environ.items():
        if any(key.startswith(prefix) for prefix in [
            "OPENROUTER_", "BASIC_MODEL__", "REASONING_MODEL__", "VISION_MODEL__"
        ]):
            relevant_vars[key] = value
    
    print("Found relevant environment variables:")
    for key, value in sorted(relevant_vars.items()):
        if "API_KEY" in key:
            print(f"  {key}: {value[:20]}..." if value else f"  {key}: NOT SET")
        else:
            print(f"  {key}: {value}")
    
    return relevant_vars

def debug_config_loading():
    """Debug the configuration loading process."""
    print("\n🔍 Debugging Configuration Loading")
    print("=" * 50)
    
    try:
        from src.config.loader import load_yaml_config, clear_config_cache
        from src.llms.llm import _get_env_llm_conf, clear_llm_cache
        
        # Clear caches
        print("Clearing caches...")
        clear_config_cache()
        clear_llm_cache()
        
        # Check YAML config
        conf_path = str(project_root / "conf.yaml")
        print(f"Loading YAML config from: {conf_path}")
        config = load_yaml_config(conf_path)
        
        if config:
            print("YAML config loaded successfully:")
            for model_type in ["BASIC_MODEL", "REASONING_MODEL", "VISION_MODEL"]:
                model_config = config.get(model_type, {})
                print(f"  {model_type}: {model_config}")
        else:
            print("No YAML config found or empty config")
        
        # Check environment variable loading for each model type
        for model_type in ["basic", "reasoning", "vision"]:
            print(f"\nEnvironment config for {model_type} model:")
            env_conf = _get_env_llm_conf(model_type)
            print(f"  Raw env config: {env_conf}")
            
            # Show what the merged config would look like
            yaml_conf = config.get(f"{model_type.upper()}_MODEL", {}) if config else {}
            merged_conf = {**yaml_conf, **env_conf}
            print(f"  Merged config: {merged_conf}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def debug_llm_initialization():
    """Debug LLM initialization process."""
    print("\n🔍 Debugging LLM Initialization")
    print("=" * 50)
    
    try:
        from src.llms.llm import get_llm_by_type, clear_llm_cache, _create_llm_use_conf
        from src.config.loader import load_yaml_config, clear_config_cache
        
        # Clear caches to ensure fresh initialization
        clear_config_cache()
        clear_llm_cache()
        
        # Load config
        conf_path = str(project_root / "conf.yaml")
        config = load_yaml_config(conf_path)
        
        # Try to create LLM manually to see exact parameters
        print("Attempting to create basic LLM...")
        try:
            llm = _create_llm_use_conf("basic", config)
            print(f"✅ LLM created successfully!")
            print(f"  Model: {llm.model_name}")
            print(f"  Base URL: {getattr(llm, 'openai_api_base', 'Not set')}")
            print(f"  API Key: {getattr(llm, 'openai_api_key', 'Not set')[:20]}..." if hasattr(llm, 'openai_api_key') else "  API Key: Not accessible")
            
            # Try to make a test call
            print("\nTesting LLM call...")
            response = llm.invoke("Hello! Please respond with 'Test successful' to confirm you're working.")
            print(f"✅ LLM call successful: {response.content}")
            return True
            
        except Exception as e:
            print(f"❌ LLM creation/call failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    except Exception as e:
        print(f"❌ LLM initialization debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def debug_chatopen_ai_params():
    """Debug ChatOpenAI parameter handling."""
    print("\n🔍 Debugging ChatOpenAI Parameters")
    print("=" * 50)
    
    try:
        from langchain_openai import ChatOpenAI
        
        # Get the actual parameters we're using
        api_key = "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"
        model = "meta-llama/llama-3.2-1b-instruct:free"
        base_url = "https://openrouter.ai/api/v1"
        
        print(f"Testing ChatOpenAI with:")
        print(f"  API Key: {api_key[:20]}...")
        print(f"  Model: {model}")
        print(f"  Base URL: {base_url}")
        
        # Test the exact configuration we should be using
        llm = ChatOpenAI(
            model=model,
            openai_api_key=api_key,
            base_url=base_url,
            default_headers={
                "HTTP-Referer": "https://avaxsearch.vercel.app",
                "X-Title": "CryptoSearch",
            }
        )
        
        print("✅ ChatOpenAI initialized successfully")
        
        # Test call
        response = llm.invoke("Hello! Please respond with 'Direct test successful'.")
        print(f"✅ Direct ChatOpenAI call successful: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Direct ChatOpenAI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all debug checks."""
    print("🐛 Railway Configuration Debug Script")
    print("=" * 50)
    
    # Run all debug functions
    debug_functions = [
        ("Environment Variables", debug_environment_variables),
        ("Configuration Loading", debug_config_loading),
        ("LLM Initialization", debug_llm_initialization),
        ("ChatOpenAI Parameters", debug_chatopen_ai_params),
    ]
    
    results = []
    for name, func in debug_functions:
        try:
            result = func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} debug failed: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("🔍 Debug Summary")
    print("=" * 50)
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{name}: {status}")
    
    all_passed = all(result for _, result in results if isinstance(result, bool))
    print(f"\nOverall: {'✅ ALL CHECKS PASSED' if all_passed else '❌ SOME CHECKS FAILED'}")
    
    if not all_passed:
        print("\n💡 Recommendations:")
        print("1. Verify OpenRouter API key is valid and active")
        print("2. Check Railway environment variables are set correctly")
        print("3. Ensure application cache is cleared after config changes")
        print("4. Try redeploying the Railway service")

if __name__ == "__main__":
    main()

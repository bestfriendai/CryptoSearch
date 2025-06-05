#!/usr/bin/env python3
"""
Test script to verify the configuration is working properly.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment_variables():
    """Test that all required environment variables are set."""
    required_vars = [
        "OPENROUTER_API_KEY",
        "TAVILY_API_KEY", 
        "BASIC_MODEL__MODEL",
        "BASIC_MODEL__API_KEY",
        "BASIC_MODEL__BASE_URL",
        "SEARCH_API",
        "FRONTEND_URL",
        "REASONING_MODEL__API_KEY",
        "REASONING_MODEL__BASE_URL", 
        "REASONING_MODEL__MODEL",
        "VISION_MODEL__API_KEY",
        "VISION_MODEL__BASE_URL",
        "VISION_MODEL__MODEL"
    ]
    
    print("🔍 Checking environment variables...")
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if "API_KEY" in var:
                masked_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
                print(f"✅ {var}: {masked_value}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: NOT SET")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n❌ Missing {len(missing_vars)} required environment variables!")
        return False
    else:
        print(f"\n✅ All {len(required_vars)} environment variables are set!")
        return True

def test_model_configuration():
    """Test that the model configuration can be loaded."""
    try:
        print("\n🔍 Testing model configuration...")
        
        # Import after loading environment variables
        from src.llms.llm import get_llm_by_type
        
        # Test basic model
        print("Testing BASIC_MODEL...")
        basic_llm = get_llm_by_type("basic")
        print(f"✅ Basic model loaded: {basic_llm.model_name}")
        
        # Test reasoning model  
        print("Testing REASONING_MODEL...")
        reasoning_llm = get_llm_by_type("reasoning")
        print(f"✅ Reasoning model loaded: {reasoning_llm.model_name}")
        
        # Test vision model
        print("Testing VISION_MODEL...")
        vision_llm = get_llm_by_type("vision")
        print(f"✅ Vision model loaded: {vision_llm.model_name}")
        
        print("\n✅ All models configured successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Model configuration failed: {str(e)}")
        return False

def test_search_configuration():
    """Test that search configuration is working."""
    try:
        print("\n🔍 Testing search configuration...")
        
        search_api = os.getenv("SEARCH_API")
        tavily_key = os.getenv("TAVILY_API_KEY")
        
        if search_api == "tavily" and tavily_key:
            print(f"✅ Search API: {search_api}")
            print(f"✅ Tavily API Key: {tavily_key[:8]}...{tavily_key[-4:]}")
            return True
        else:
            print(f"❌ Search configuration incomplete")
            return False
            
    except Exception as e:
        print(f"\n❌ Search configuration failed: {str(e)}")
        return False

def main():
    """Run all configuration tests."""
    print("🚀 DeerFlow Configuration Test\n")
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Model Configuration", test_model_configuration), 
        ("Search Configuration", test_search_configuration),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Testing: {test_name}")
        print('='*50)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("CONFIGURATION TEST SUMMARY")
    print('='*50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All configuration tests passed! Your setup is ready.")
        return 0
    else:
        print(f"\n⚠️  {len(results) - passed} test(s) failed. Please check your configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

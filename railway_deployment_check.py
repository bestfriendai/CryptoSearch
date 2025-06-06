#!/usr/bin/env python3
"""
Railway Deployment Configuration Check
This script verifies that Railway environment variables are correctly configured for OpenRouter.
"""

import os
import sys
import requests
from typing import Dict, List, Tuple

def check_environment_variables() -> Tuple[bool, List[str]]:
    """Check if all required environment variables are set."""
    required_vars = [
        "OPENROUTER_API_KEY",
        "BASIC_MODEL__MODEL",
        "BASIC_MODEL__OPENAI_API_KEY", 
        "BASIC_MODEL__BASE_URL",
        "REASONING_MODEL__MODEL",
        "REASONING_MODEL__OPENAI_API_KEY",
        "REASONING_MODEL__BASE_URL",
        "VISION_MODEL__MODEL",
        "VISION_MODEL__OPENAI_API_KEY",
        "VISION_MODEL__BASE_URL",
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    return len(missing_vars) == 0, missing_vars

def check_api_key_format(api_key: str) -> bool:
    """Check if API key has correct OpenRouter format."""
    return api_key and api_key.startswith("sk-or-v1-") and len(api_key) > 20

def test_openrouter_connection(api_key: str, model: str) -> Tuple[bool, str]:
    """Test connection to OpenRouter API."""
    try:
        # Test models endpoint first
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://avaxsearch.vercel.app",
                "X-Title": "CryptoSearch",
            },
            timeout=10
        )
        
        if response.status_code != 200:
            return False, f"Models endpoint failed: {response.status_code} - {response.text}"
        
        # Test chat completion
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://avaxsearch.vercel.app",
                "X-Title": "CryptoSearch",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 5
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return True, "Connection successful"
        else:
            return False, f"Chat completion failed: {response.status_code} - {response.text}"
            
    except Exception as e:
        return False, f"Connection error: {str(e)}"

def main():
    """Main function to run all checks."""
    print("🚀 Railway Deployment Configuration Check")
    print("=" * 50)
    
    # Check environment variables
    print("\n1. Checking Environment Variables...")
    env_ok, missing_vars = check_environment_variables()
    
    if env_ok:
        print("✅ All required environment variables are set")
    else:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nTo fix this, run:")
        for var in missing_vars:
            if "API_KEY" in var:
                print(f"   railway variables --set \"{var}=your-openrouter-api-key\"")
            elif "MODEL" in var:
                print(f"   railway variables --set \"{var}=meta-llama/llama-3.2-1b-instruct:free\"")
            elif "BASE_URL" in var:
                print(f"   railway variables --set \"{var}=https://openrouter.ai/api/v1\"")
        return False
    
    # Check API key format
    print("\n2. Checking API Key Format...")
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if check_api_key_format(api_key):
        print("✅ API key format is correct")
    else:
        print("❌ API key format is incorrect")
        print("   Expected format: sk-or-v1-...")
        print("   Get a new key from: https://openrouter.ai/")
        return False
    
    # Check model configuration
    print("\n3. Checking Model Configuration...")
    model = os.getenv("BASIC_MODEL__MODEL")
    base_url = os.getenv("BASIC_MODEL__BASE_URL")
    
    if model and ":free" in model:
        print(f"✅ Using free model: {model}")
    else:
        print(f"⚠️  Model may not be free: {model}")
    
    if base_url == "https://openrouter.ai/api/v1":
        print("✅ Base URL is correct")
    else:
        print(f"❌ Incorrect base URL: {base_url}")
        return False
    
    # Test API connection
    print("\n4. Testing OpenRouter API Connection...")
    connection_ok, message = test_openrouter_connection(api_key, model)
    
    if connection_ok:
        print("✅ OpenRouter API connection successful")
    else:
        print(f"❌ OpenRouter API connection failed: {message}")
        print("\nTroubleshooting steps:")
        print("1. Verify API key at https://openrouter.ai/")
        print("2. Check if account has sufficient credits")
        print("3. Ensure model name is correct")
        return False
    
    print("\n🎉 All checks passed! Railway deployment should work correctly.")
    print("\nNext steps:")
    print("1. Deploy to Railway: railway deploy")
    print("2. Check logs: railway logs")
    print("3. Test the application at your Railway URL")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

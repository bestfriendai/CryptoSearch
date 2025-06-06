#!/usr/bin/env python3
"""
Test script to verify API key format and make a simple request.
"""

import os
import requests
from dotenv import load_dotenv
load_dotenv()

def test_api_key_format():
    """Test the API key format and make a simple request."""
    api_key = os.getenv("BASIC_MODEL__OPENAI_API_KEY")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    
    print("API Key Analysis:")
    print(f"BASIC_MODEL__OPENAI_API_KEY: {api_key[:20]}..." if api_key else "Not set")
    print(f"OPENROUTER_API_KEY: {openrouter_key[:20]}..." if openrouter_key else "Not set")
    print(f"Keys match: {api_key == openrouter_key}")
    
    if api_key:
        print(f"API Key length: {len(api_key)}")
        print(f"API Key starts with 'sk-or-': {api_key.startswith('sk-or-')}")
    
    # Test with a simple request to OpenRouter
    print(f"\nTesting API key with OpenRouter models endpoint...")
    
    try:
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://avaxsearch.vercel.app",
                "X-Title": "CryptoSearch",
            }
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✓ API key is valid!")
            models = response.json()
            print(f"Found {len(models.get('data', []))} models")
        else:
            print(f"✗ API key validation failed")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"✗ Request failed: {e}")

def test_chat_completion():
    """Test a simple chat completion."""
    api_key = os.getenv("BASIC_MODEL__OPENAI_API_KEY")
    model = os.getenv("BASIC_MODEL__MODEL")
    
    print(f"\nTesting chat completion with model: {model}")
    
    try:
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
                "messages": [
                    {
                        "role": "user",
                        "content": "Say 'OK' to confirm you're working."
                    }
                ],
                "max_tokens": 10
            }
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"✓ Chat completion successful!")
            print(f"Response: {content}")
            return True
        else:
            print(f"✗ Chat completion failed")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Chat completion request failed: {e}")
        return False

if __name__ == "__main__":
    test_api_key_format()
    test_chat_completion()

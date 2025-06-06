#!/usr/bin/env python3
"""
Test different authentication formats for OpenRouter.
"""

import os
import requests
from dotenv import load_dotenv
load_dotenv()

def test_auth_format(auth_header, description):
    """Test a specific authentication format."""
    print(f"\nTesting {description}")
    print(f"Auth header: {auth_header}")
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": auth_header,
                "Content-Type": "application/json",
                "HTTP-Referer": "https://avaxsearch.vercel.app",
                "X-Title": "CryptoSearch",
            },
            json={
                "model": "meta-llama/llama-3.2-1b-instruct:free",
                "messages": [
                    {
                        "role": "user",
                        "content": "Say 'OK'"
                    }
                ],
                "max_tokens": 5
            }
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"✓ Success! Response: {content}")
            return True
        else:
            print(f"✗ Failed. Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Request failed: {e}")
        return False

def test_without_optional_headers():
    """Test without optional headers."""
    api_key = os.getenv("BASIC_MODEL__OPENAI_API_KEY")
    
    print(f"\nTesting without optional headers")
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "meta-llama/llama-3.2-1b-instruct:free",
                "messages": [
                    {
                        "role": "user",
                        "content": "Say 'OK'"
                    }
                ],
                "max_tokens": 5
            }
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"✓ Success! Response: {content}")
            return True
        else:
            print(f"✗ Failed. Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Request failed: {e}")
        return False

def check_api_key_validity():
    """Check if the API key is valid by testing the credits endpoint."""
    api_key = os.getenv("BASIC_MODEL__OPENAI_API_KEY")
    
    print(f"\nChecking API key validity with credits endpoint...")
    
    try:
        response = requests.get(
            "https://openrouter.ai/api/v1/auth/key",
            headers={
                "Authorization": f"Bearer {api_key}",
            }
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✓ API key is valid!")
            print(f"Key info: {result}")
            return True
        else:
            print(f"✗ API key validation failed")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Request failed: {e}")
        return False

def main():
    api_key = os.getenv("BASIC_MODEL__OPENAI_API_KEY")
    
    print(f"Testing different authentication formats...")
    print(f"API Key: {api_key[:20]}..." if api_key else "Not set")
    
    # Check API key validity first
    check_api_key_validity()
    
    # Test different auth formats
    auth_formats = [
        (f"Bearer {api_key}", "Standard Bearer token"),
        (f"sk-or-v1 {api_key[9:]}", "Custom sk-or-v1 format"),  # Remove sk-or-v1- prefix
        (api_key, "Raw API key"),
    ]
    
    success_count = 0
    for auth_header, description in auth_formats:
        if test_auth_format(auth_header, description):
            success_count += 1
    
    # Test without optional headers
    if test_without_optional_headers():
        success_count += 1
    
    print(f"\nResults: {success_count} authentication methods worked")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Final test of the OpenRouter API key to verify it's working.
"""

import requests

def test_openrouter_api():
    """Test the OpenRouter API with the provided key."""
    api_key = "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"
    model = "meta-llama/llama-3.2-1b-instruct:free"
    
    print("🧪 Testing OpenRouter API...")
    print(f"API Key: {api_key[:20]}...")
    print(f"Model: {model}")
    
    try:
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
                "messages": [
                    {
                        "role": "user",
                        "content": "Hello! Please respond with 'API test successful' to confirm you're working."
                    }
                ],
                "max_tokens": 20
            },
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"✅ SUCCESS! Response: {content}")
            return True
        else:
            print(f"❌ FAILED! Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_openrouter_api()
    if success:
        print("\n🎉 The OpenRouter API key is working correctly!")
        print("Your Railway deployment should now work without 401 errors.")
    else:
        print("\n💥 The API key is still not working.")
        print("Please check your OpenRouter account and generate a new key if needed.")

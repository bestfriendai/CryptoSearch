#!/usr/bin/env python3
"""
Test script to verify OpenRouter API directly using OpenAI SDK.
"""

import os
from dotenv import load_dotenv
load_dotenv()

def test_openrouter_direct():
    """Test OpenRouter API using the exact approach from their documentation."""
    from openai import OpenAI
    
    api_key = os.getenv("BASIC_MODEL__OPENAI_API_KEY")
    model = os.getenv("BASIC_MODEL__MODEL")
    
    print(f"Testing OpenRouter direct connection:")
    print(f"  API Key: {api_key[:20]}..." if api_key else "  API Key: None")
    print(f"  Model: {model}")
    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://avaxsearch.vercel.app",  # Your site URL
                "X-Title": "CryptoSearch",  # Your site name
            },
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": "Say 'OK' to confirm you're working."
                }
            ]
        )
        
        print(f"✓ OpenRouter API call successful!")
        print(f"Response: {completion.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"✗ OpenRouter API call failed: {e}")
        return False

def test_langchain_with_headers():
    """Test LangChain ChatOpenAI with extra headers."""
    from langchain_openai import ChatOpenAI
    
    api_key = os.getenv("BASIC_MODEL__OPENAI_API_KEY")
    model = os.getenv("BASIC_MODEL__MODEL")
    
    print(f"\nTesting LangChain with extra headers:")
    
    try:
        llm = ChatOpenAI(
            model=model,
            openai_api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "https://avaxsearch.vercel.app",
                "X-Title": "CryptoSearch",
            }
        )
        
        response = llm.invoke("Say 'OK' to confirm you're working.")
        print(f"✓ LangChain with headers successful!")
        print(f"Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"✗ LangChain with headers failed: {e}")
        return False

if __name__ == "__main__":
    success1 = test_openrouter_direct()
    success2 = test_langchain_with_headers()
    
    if success1 or success2:
        print(f"\n✓ At least one method worked!")
    else:
        print(f"\n✗ Both methods failed!")

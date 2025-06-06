#!/usr/bin/env python3
"""
Test script to try different models and request formats.
"""

import os
import requests
from dotenv import load_dotenv
load_dotenv()

def test_model(model_name, description):
    """Test a specific model."""
    api_key = os.getenv("BASIC_MODEL__OPENAI_API_KEY")
    
    print(f"\nTesting {description}: {model_name}")
    
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
                "model": model_name,
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

def get_available_free_models():
    """Get list of available free models."""
    api_key = os.getenv("BASIC_MODEL__OPENAI_API_KEY")
    
    try:
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://avaxsearch.vercel.app",
                "X-Title": "CryptoSearch",
            }
        )
        
        if response.status_code == 200:
            models = response.json()
            free_models = []
            for model in models.get('data', []):
                pricing = model.get('pricing', {})
                if (pricing.get('prompt') == '0' or 
                    model.get('id', '').endswith(':free')):
                    free_models.append(model.get('id'))
            
            print(f"Found {len(free_models)} free models:")
            for model in free_models[:10]:  # Show first 10
                print(f"  - {model}")
            
            return free_models
        else:
            print(f"Failed to get models: {response.text}")
            return []
            
    except Exception as e:
        print(f"Failed to get models: {e}")
        return []

def main():
    print("Testing different models and formats...")
    
    # Get available free models
    free_models = get_available_free_models()
    
    # Test models
    models_to_test = [
        ("meta-llama/llama-3.2-1b-instruct:free", "Original model"),
        ("meta-llama/llama-3.2-3b-instruct:free", "Larger Llama model"),
        ("microsoft/phi-3-mini-128k-instruct:free", "Phi-3 model"),
        ("google/gemma-2-9b-it:free", "Gemma model"),
    ]
    
    # Only test models that are actually available
    available_models = [(model, desc) for model, desc in models_to_test if model in free_models]
    
    if not available_models:
        print("No test models found in available free models. Testing original anyway...")
        available_models = models_to_test[:1]
    
    success_count = 0
    for model, description in available_models:
        if test_model(model, description):
            success_count += 1
    
    print(f"\nResults: {success_count}/{len(available_models)} models worked")

if __name__ == "__main__":
    main()

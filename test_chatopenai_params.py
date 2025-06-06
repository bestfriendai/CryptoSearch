#!/usr/bin/env python3
"""
Test script to verify ChatOpenAI parameter names.
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

def test_chatopenai_params():
    """Test different parameter combinations for ChatOpenAI."""
    from langchain_openai import ChatOpenAI
    
    api_key = os.getenv("BASIC_MODEL__OPENAI_API_KEY")
    base_url = os.getenv("BASIC_MODEL__BASE_URL")
    model = os.getenv("BASIC_MODEL__MODEL")
    
    print(f"Testing with:")
    print(f"  API Key: {api_key[:20]}..." if api_key else "  API Key: None")
    print(f"  Base URL: {base_url}")
    print(f"  Model: {model}")
    
    # Test different parameter combinations
    test_configs = [
        {
            "name": "openai_api_key + base_url",
            "params": {
                "model": model,
                "openai_api_key": api_key,
                "base_url": base_url
            }
        },
        {
            "name": "openai_api_key + openai_api_base",
            "params": {
                "model": model,
                "openai_api_key": api_key,
                "openai_api_base": base_url
            }
        },
        {
            "name": "api_key + base_url",
            "params": {
                "model": model,
                "api_key": api_key,
                "base_url": base_url
            }
        }
    ]
    
    for config in test_configs:
        print(f"\n=== Testing {config['name']} ===")
        try:
            llm = ChatOpenAI(**config['params'])
            print(f"✓ ChatOpenAI initialized successfully")
            print(f"  Model: {llm.model_name}")
            print(f"  Base URL: {getattr(llm, 'openai_api_base', 'Not set')}")
            
            # Try a simple call
            try:
                response = llm.invoke("Say 'OK'")
                print(f"✓ API call successful: {response.content}")
                return True
            except Exception as e:
                print(f"✗ API call failed: {e}")
                
        except Exception as e:
            print(f"✗ ChatOpenAI initialization failed: {e}")
    
    return False

if __name__ == "__main__":
    test_chatopenai_params()

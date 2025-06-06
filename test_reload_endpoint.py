#!/usr/bin/env python3
"""
Test script to trigger the LLM configuration reload endpoint.
"""

import requests
import time

def test_reload_endpoint():
    """Test the reload endpoint on Railway."""
    railway_url = "https://dddd-production.up.railway.app"
    
    print("🔄 Testing LLM Configuration Reload Endpoint")
    print("=" * 50)
    print(f"Railway URL: {railway_url}")
    
    try:
        # First, check if the application is running
        print("\n1. Checking application health...")
        health_response = requests.get(f"{railway_url}/health", timeout=10)
        if health_response.status_code == 200:
            print("✅ Application is running")
        else:
            print(f"❌ Application health check failed: {health_response.status_code}")
            return False
        
        # Trigger the reload endpoint
        print("\n2. Triggering LLM configuration reload...")
        reload_response = requests.post(f"{railway_url}/api/admin/reload-llm", timeout=30)
        
        print(f"Status Code: {reload_response.status_code}")
        
        if reload_response.status_code == 200:
            result = reload_response.json()
            print(f"✅ Reload successful!")
            print(f"Response: {result}")
            
            # Wait a moment for the reload to complete
            print("\n3. Waiting for reload to complete...")
            time.sleep(3)
            
            # Test if the application is still responsive
            print("\n4. Testing application responsiveness...")
            health_response = requests.get(f"{railway_url}/health", timeout=10)
            if health_response.status_code == 200:
                print("✅ Application is still responsive after reload")
                return True
            else:
                print(f"❌ Application became unresponsive after reload")
                return False
        else:
            print(f"❌ Reload failed")
            print(f"Response: {reload_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing reload endpoint: {e}")
        return False

def test_chat_endpoint():
    """Test the chat endpoint to see if authentication works."""
    railway_url = "https://dddd-production.up.railway.app"
    
    print("\n🧪 Testing Chat Endpoint Authentication")
    print("=" * 50)
    
    try:
        # Test the chat endpoint with a simple message
        chat_data = {
            "messages": [{"role": "user", "content": "Hello! Please respond with 'Authentication test successful' to confirm you're working."}],
            "thread_id": "test-thread",
            "resources": [],
            "max_plan_iterations": 1,
            "max_step_num": 1,
            "max_search_results": 1,
            "auto_accepted_plan": True,
            "interrupt_feedback": "",
            "enable_background_investigation": False
        }
        
        print("Sending test message to chat endpoint...")
        response = requests.post(
            f"{railway_url}/api/chat/stream",
            json=chat_data,
            timeout=60,
            stream=True
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Chat endpoint responded successfully!")
            
            # Read the first few chunks of the streaming response
            chunk_count = 0
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    chunk_text = chunk.decode('utf-8', errors='ignore')
                    print(f"Chunk {chunk_count}: {chunk_text[:200]}...")
                    chunk_count += 1
                    if chunk_count >= 3:  # Only read first few chunks
                        break
            
            return True
        else:
            print(f"❌ Chat endpoint failed")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing chat endpoint: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Railway LLM Configuration Test")
    print("=" * 50)
    
    # Test reload endpoint
    reload_success = test_reload_endpoint()
    
    # Test chat endpoint
    chat_success = test_chat_endpoint()
    
    print("\n" + "=" * 50)
    print("🔍 Test Results")
    print("=" * 50)
    print(f"Reload Endpoint: {'✅ PASSED' if reload_success else '❌ FAILED'}")
    print(f"Chat Endpoint: {'✅ PASSED' if chat_success else '❌ FAILED'}")
    
    overall_success = reload_success and chat_success
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")
    
    if overall_success:
        print("\n🎉 The Railway deployment is working correctly!")
        print("The LLM configuration has been successfully reloaded.")
    else:
        print("\n💥 There are still issues with the deployment.")
        print("Check the Railway logs for more details.")

if __name__ == "__main__":
    main()

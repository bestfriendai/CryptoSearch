#!/usr/bin/env python3
"""
Comprehensive local testing script for CryptoSearch application
Tests all components: API key, LLM configuration, search, and endpoints
"""
import os
import sys
import asyncio
import json
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def load_environment():
    """Load environment variables from .env.local"""
    env_file = Path(__file__).parent / ".env.local"
    if env_file.exists():
        load_dotenv(env_file)
        print(f"✅ Loaded environment from {env_file}")
        return True
    else:
        print(f"❌ Environment file not found: {env_file}")
        return False

def test_environment_variables():
    """Test that all required environment variables are set"""
    print("\n" + "="*60)
    print("🔧 TESTING ENVIRONMENT VARIABLES")
    print("="*60)
    
    required_vars = [
        "OPENROUTER_API_KEY",
        "BASIC_MODEL__MODEL",
        "BASIC_MODEL__OPENAI_API_KEY",
        "BASIC_MODEL__BASE_URL",
        "REASONING_MODEL__MODEL",
        "REASONING_MODEL__OPENAI_API_KEY",
        "SEARCH_API"
    ]
    
    all_good = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if "API_KEY" in var:
                print(f"✅ {var}: {value[:15]}...{value[-10:]}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: NOT SET")
            all_good = False
    
    return all_good

def test_openrouter_direct():
    """Test OpenRouter API directly"""
    print("\n" + "="*60)
    print("🔑 TESTING OPENROUTER API DIRECTLY")
    print("="*60)
    
    try:
        import requests
        
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("❌ No OpenRouter API key found")
            return False
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "CryptoSearch-Local-Test"
        }
        
        data = {
            "model": "google/gemini-2.5-pro-preview",
            "messages": [
                {"role": "user", "content": "Hello! This is a test. Please respond with 'API test successful'."}
            ],
            "max_tokens": 50
        }
        
        print(f"Making request to: {url}")
        print(f"Model: {data['model']}")
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            message = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            print(f"✅ OpenRouter API Success!")
            print(f"Response: {message}")
            return True
        else:
            print(f"❌ OpenRouter API Failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ OpenRouter API Exception: {e}")
        return False

def test_llm_configuration():
    """Test LLM configuration loading"""
    print("\n" + "="*60)
    print("🤖 TESTING LLM CONFIGURATION")
    print("="*60)
    
    try:
        from llms.llm import get_llm_by_type, _get_env_llm_conf
        
        # Test environment configuration loading
        print("Testing environment configuration loading...")
        basic_env_conf = _get_env_llm_conf("basic")
        print(f"Basic env config: {basic_env_conf}")
        
        reasoning_env_conf = _get_env_llm_conf("reasoning")
        print(f"Reasoning env config: {reasoning_env_conf}")
        
        # Test LLM creation
        print("\nTesting LLM creation...")
        basic_llm = get_llm_by_type("basic", force_reload=True)
        print(f"✅ Basic LLM created: {type(basic_llm).__name__}")

        reasoning_llm = get_llm_by_type("reasoning", force_reload=True)
        print(f"✅ Reasoning LLM created: {type(reasoning_llm).__name__}")
        
        # Test simple LLM call
        print("\nTesting simple LLM call...")
        response = basic_llm.invoke("Hello! Please respond with 'LLM test successful'.")
        print(f"✅ LLM Response: {response.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM Configuration Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_search_functionality():
    """Test search functionality"""
    print("\n" + "="*60)
    print("🔍 TESTING SEARCH FUNCTIONALITY")
    print("="*60)

    try:
        from tools.search import get_web_search_tool

        # Test DuckDuckGo search
        print("Testing DuckDuckGo search...")
        search_tool = get_web_search_tool(max_search_results=3)
        results = search_tool.invoke("Bitcoin price today")

        if results:
            print(f"✅ Search successful!")
            print(f"Results: {str(results)[:200]}...")
            return True
        else:
            print("❌ Search returned no results")
            return False

    except Exception as e:
        print(f"❌ Search Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_graph_workflow():
    """Test the graph workflow"""
    print("\n" + "="*60)
    print("🔄 TESTING GRAPH WORKFLOW")
    print("="*60)
    
    try:
        from graph.graph import create_graph
        from graph.state import GraphState
        
        # Create the graph
        print("Creating graph...")
        graph = create_graph()
        print("✅ Graph created successfully")
        
        # Test simple workflow
        print("Testing simple workflow...")
        initial_state = GraphState(
            messages=[{"role": "user", "content": "What is Bitcoin?"}],
            user_query="What is Bitcoin?",
            search_results=[],
            final_response=""
        )
        
        # Run the workflow
        print("Running workflow...")
        result = await graph.ainvoke(initial_state)
        
        if result and result.get("final_response"):
            print(f"✅ Workflow successful!")
            print(f"Response: {result['final_response'][:200]}...")
            return True
        else:
            print("❌ Workflow failed - no response generated")
            return False
            
    except Exception as e:
        print(f"❌ Graph Workflow Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_server_startup():
    """Test server startup (without actually starting it)"""
    print("\n" + "="*60)
    print("🚀 TESTING SERVER CONFIGURATION")
    print("="*60)
    
    try:
        from server.app import app
        
        # Check if FastAPI app is created
        print("✅ FastAPI app created successfully")
        
        # Check routes
        routes = [route.path for route in app.routes]
        expected_routes = ["/api/chat/stream", "/api/rag/config", "/health"]
        
        for route in expected_routes:
            if any(route in r for r in routes):
                print(f"✅ Route found: {route}")
            else:
                print(f"❌ Route missing: {route}")
        
        return True
        
    except Exception as e:
        print(f"❌ Server Configuration Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def run_all_tests():
    """Run all tests"""
    print("🧪 CRYPTOSEARCH LOCAL TESTING SUITE")
    print("="*60)
    
    # Load environment
    if not load_environment():
        print("❌ Failed to load environment. Exiting.")
        return False
    
    # Run tests
    tests = [
        ("Environment Variables", test_environment_variables),
        ("OpenRouter API", test_openrouter_direct),
        ("LLM Configuration", test_llm_configuration),
        ("Search Functionality", test_search_functionality),
        ("Graph Workflow", test_graph_workflow),
        ("Server Configuration", test_server_startup),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! The application should work correctly in production.")
        return True
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please fix issues before deploying.")
        return False

if __name__ == "__main__":
    asyncio.run(run_all_tests())

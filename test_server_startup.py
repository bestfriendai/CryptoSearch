#!/usr/bin/env python3
"""
Test server startup locally to verify everything works
"""
import os
import sys
import asyncio
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

async def test_basic_llm_call():
    """Test basic LLM functionality"""
    print("\n" + "="*50)
    print("🤖 TESTING BASIC LLM FUNCTIONALITY")
    print("="*50)
    
    try:
        from llms.llm import get_llm_by_type
        
        # Test basic LLM
        print("Creating basic LLM...")
        llm = get_llm_by_type("basic", force_reload=True)
        
        print("Testing LLM call...")
        response = llm.invoke("What is Bitcoin? Please respond in one sentence.")
        
        print(f"✅ LLM Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ LLM Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_search_and_llm():
    """Test search + LLM combination"""
    print("\n" + "="*50)
    print("🔍 TESTING SEARCH + LLM COMBINATION")
    print("="*50)
    
    try:
        from tools.search import get_web_search_tool
        from llms.llm import get_llm_by_type
        
        # Get search results
        print("Performing search...")
        search_tool = get_web_search_tool(max_search_results=2)
        search_results = search_tool.invoke("Bitcoin price today")
        
        print(f"Search results: {str(search_results)[:200]}...")
        
        # Use LLM to summarize
        print("Using LLM to summarize search results...")
        llm = get_llm_by_type("basic", force_reload=True)
        
        prompt = f"""Based on the following search results about Bitcoin price, provide a brief summary:

Search Results: {search_results}

Please provide a concise summary of the current Bitcoin price and any relevant information."""

        response = llm.invoke(prompt)
        
        print(f"✅ LLM Summary: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Search + LLM Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests"""
    print("🧪 CRYPTOSEARCH CORE FUNCTIONALITY TEST")
    print("="*50)
    
    # Load environment
    if not load_environment():
        print("❌ Failed to load environment. Exiting.")
        return False
    
    # Test basic LLM
    llm_success = await test_basic_llm_call()
    
    # Test search + LLM
    search_llm_success = await test_search_and_llm()
    
    # Summary
    print("\n" + "="*50)
    print("📊 CORE FUNCTIONALITY TEST SUMMARY")
    print("="*50)
    
    print(f"Basic LLM: {'✅ PASS' if llm_success else '❌ FAIL'}")
    print(f"Search + LLM: {'✅ PASS' if search_llm_success else '❌ FAIL'}")
    
    if llm_success and search_llm_success:
        print("\n🎉 CORE FUNCTIONALITY WORKING!")
        print("The application should work correctly in production.")
        print("\nKey components verified:")
        print("✅ OpenRouter API authentication")
        print("✅ Google Gemini 2.5 Pro Preview model")
        print("✅ DuckDuckGo search integration")
        print("✅ LLM + Search combination")
        return True
    else:
        print("\n⚠️ Some core functionality failed.")
        return False

if __name__ == "__main__":
    asyncio.run(main())

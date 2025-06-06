#!/usr/bin/env python3
"""
Script to set up Railway environment variables for DeerFlow
Run this script to configure the necessary environment variables in Railway
"""

import subprocess
import sys

def set_railway_env_var(key, value):
    """Set an environment variable in Railway"""
    try:
        cmd = ["npx", "@railway/cli", "variables", "set", f"{key}={value}"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Set {key}")
            return True
        else:
            print(f"✗ Failed to set {key}: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error setting {key}: {e}")
        return False

def setup_openrouter_config():
    """Set up OpenRouter configuration for Railway"""
    print("=== Setting up OpenRouter Configuration for Railway ===")
    
    # You need to replace this with your actual OpenRouter API key
    openrouter_api_key = input("Enter your OpenRouter API key: ").strip()
    
    if not openrouter_api_key:
        print("❌ OpenRouter API key is required!")
        return False
    
    # Environment variables to set
    env_vars = {
        # OpenRouter API Key
        "OPENROUTER_API_KEY": openrouter_api_key,
        
        # Basic Model Configuration (using free OpenRouter model)
        "BASIC_MODEL__MODEL": "meta-llama/llama-3.2-1b-instruct:free",
        "BASIC_MODEL__OPENAI_API_KEY": openrouter_api_key,
        "BASIC_MODEL__BASE_URL": "https://openrouter.ai/api/v1",
        
        # Reasoning Model Configuration (using free OpenRouter model)
        "REASONING_MODEL__MODEL": "meta-llama/llama-3.2-1b-instruct:free", 
        "REASONING_MODEL__OPENAI_API_KEY": openrouter_api_key,
        "REASONING_MODEL__BASE_URL": "https://openrouter.ai/api/v1",
        
        # Vision Model Configuration (using free OpenRouter model)
        "VISION_MODEL__MODEL": "meta-llama/llama-3.2-1b-instruct:free",
        "VISION_MODEL__OPENAI_API_KEY": openrouter_api_key,
        "VISION_MODEL__BASE_URL": "https://openrouter.ai/api/v1",
        
        # Search API Configuration (optional)
        "SEARCH_API": "duckduckgo",  # Using free search API
        
        # Application Settings
        "PORT": "8080",
        "PYTHONPATH": "/app",
        "PYTHONUNBUFFERED": "1"
    }
    
    print(f"\nSetting {len(env_vars)} environment variables...")
    
    success_count = 0
    for key, value in env_vars.items():
        if set_railway_env_var(key, value):
            success_count += 1
    
    print(f"\n✅ Successfully set {success_count}/{len(env_vars)} environment variables")
    
    if success_count == len(env_vars):
        print("\n🎉 Railway environment configuration complete!")
        print("You can now deploy your application with: npx @railway/cli up")
        return True
    else:
        print("\n⚠️  Some environment variables failed to set. Please check the errors above.")
        return False

def check_railway_cli():
    """Check if Railway CLI is available"""
    try:
        result = subprocess.run(["npx", "@railway/cli", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Railway CLI is available: {result.stdout.strip()}")
            return True
        else:
            print("✗ Railway CLI not found")
            return False
    except Exception as e:
        print(f"✗ Error checking Railway CLI: {e}")
        return False

def main():
    print("🚂 Railway Environment Setup for DeerFlow")
    print("=" * 50)
    
    # Check Railway CLI
    if not check_railway_cli():
        print("\n❌ Please install Railway CLI first:")
        print("npm install -g @railway/cli")
        sys.exit(1)
    
    # Check if logged in to Railway
    try:
        result = subprocess.run(["npx", "@railway/cli", "whoami"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("\n❌ Please login to Railway first:")
            print("npx @railway/cli login")
            sys.exit(1)
        else:
            print(f"✓ Logged in to Railway as: {result.stdout.strip()}")
    except Exception as e:
        print(f"✗ Error checking Railway login: {e}")
        sys.exit(1)
    
    # Set up configuration
    if setup_openrouter_config():
        print("\n🎉 Setup complete! Your Railway environment is now configured.")
    else:
        print("\n❌ Setup failed. Please check the errors and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()

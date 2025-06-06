#!/usr/bin/env python3
"""
Railway Setup Script for OpenRouter Configuration
This script helps set up Railway environment variables for OpenRouter integration.
"""

import subprocess
import sys
from typing import Optional

def run_command(command: str) -> tuple[bool, str]:
    """Run a shell command and return success status and output."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)

def check_railway_cli() -> bool:
    """Check if Railway CLI is installed and user is logged in."""
    print("Checking Railway CLI...")
    
    # Check if Railway CLI is installed
    success, output = run_command("npx @railway/cli --version")
    if not success:
        print("❌ Railway CLI not found. Installing...")
        success, output = run_command("npm install -g @railway/cli")
        if not success:
            print(f"Failed to install Railway CLI: {output}")
            return False
    
    print("✅ Railway CLI is available")
    
    # Check if user is logged in
    success, output = run_command("npx @railway/cli whoami")
    if not success:
        print("❌ Not logged in to Railway")
        print("Please run: npx @railway/cli login")
        return False
    
    print(f"✅ Logged in to Railway: {output.strip()}")
    return True

def get_user_input(prompt: str, default: Optional[str] = None) -> str:
    """Get user input with optional default value."""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        while True:
            user_input = input(f"{prompt}: ").strip()
            if user_input:
                return user_input
            print("This field is required.")

def setup_openrouter_config():
    """Set up OpenRouter configuration for Railway."""
    print("\n🔧 Setting up OpenRouter Configuration")
    print("=" * 50)
    
    # Get API key
    print("\n1. Get your OpenRouter API key from: https://openrouter.ai/")
    api_key = get_user_input("Enter your OpenRouter API key")
    
    if not api_key.startswith("sk-or-v1-"):
        print("⚠️  Warning: API key doesn't look like an OpenRouter key")
        confirm = input("Continue anyway? (y/N): ").lower()
        if confirm != 'y':
            return False
    
    # Choose model
    print("\n2. Choose a model:")
    print("   1. meta-llama/llama-3.2-1b-instruct:free (Recommended - Fast)")
    print("   2. microsoft/phi-3-mini-128k-instruct:free (Good for longer contexts)")
    print("   3. google/gemma-2-9b-it:free (Balanced performance)")
    print("   4. Custom model")
    
    choice = get_user_input("Enter choice (1-4)", "1")
    
    model_map = {
        "1": "meta-llama/llama-3.2-1b-instruct:free",
        "2": "microsoft/phi-3-mini-128k-instruct:free", 
        "3": "google/gemma-2-9b-it:free",
    }
    
    if choice in model_map:
        model = model_map[choice]
    elif choice == "4":
        model = get_user_input("Enter custom model name")
    else:
        print("Invalid choice, using default")
        model = model_map["1"]
    
    print(f"\nSelected model: {model}")
    
    # Set environment variables
    print("\n3. Setting Railway environment variables...")
    
    variables = [
        ("OPENROUTER_API_KEY", api_key),
        ("BASIC_MODEL__MODEL", model),
        ("BASIC_MODEL__OPENAI_API_KEY", api_key),
        ("BASIC_MODEL__BASE_URL", "https://openrouter.ai/api/v1"),
        ("REASONING_MODEL__MODEL", model),
        ("REASONING_MODEL__OPENAI_API_KEY", api_key),
        ("REASONING_MODEL__BASE_URL", "https://openrouter.ai/api/v1"),
        ("VISION_MODEL__MODEL", model),
        ("VISION_MODEL__OPENAI_API_KEY", api_key),
        ("VISION_MODEL__BASE_URL", "https://openrouter.ai/api/v1"),
        ("SEARCH_API", "tavily"),
        ("TAVILY_API_KEY", "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"),
        ("FRONTEND_URL", "https://avaxsearch.vercel.app"),
    ]
    
    failed_vars = []
    for var_name, var_value in variables:
        print(f"Setting {var_name}...")
        success, output = run_command(f'npx @railway/cli variables --set "{var_name}={var_value}"')
        if not success:
            print(f"❌ Failed to set {var_name}: {output}")
            failed_vars.append(var_name)
        else:
            print(f"✅ Set {var_name}")
    
    if failed_vars:
        print(f"\n❌ Failed to set {len(failed_vars)} variables:")
        for var in failed_vars:
            print(f"   - {var}")
        return False
    
    print("\n✅ All environment variables set successfully!")
    return True

def deploy_to_railway():
    """Deploy the application to Railway."""
    print("\n🚀 Deploying to Railway...")
    
    deploy_choice = input("Deploy now? (Y/n): ").lower()
    if deploy_choice in ['', 'y', 'yes']:
        print("Starting deployment...")
        success, output = run_command("npx @railway/cli redeploy")
        if success:
            print("✅ Deployment started successfully!")
            print("Check deployment status with: npx @railway/cli logs")
        else:
            print(f"❌ Deployment failed: {output}")
            return False
    else:
        print("Skipping deployment. You can deploy later with: npx @railway/cli redeploy")
    
    return True

def main():
    """Main setup function."""
    print("🚂 Railway OpenRouter Setup Script")
    print("=" * 50)
    print("This script will help you configure Railway for OpenRouter integration.")
    
    # Check Railway CLI
    if not check_railway_cli():
        return False
    
    # Setup OpenRouter configuration
    if not setup_openrouter_config():
        return False
    
    # Deploy to Railway
    if not deploy_to_railway():
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Check deployment logs: npx @railway/cli logs")
    print("2. Test your application at the Railway URL")
    print("3. Monitor for any authentication errors")
    print("4. Run python railway_deployment_check.py to verify configuration")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
SwarmMind Installation and Setup Guide
=====================================

This script helps verify and set up SwarmMind on your system.
"""

import sys
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ required. Current: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True


def check_dependencies():
    """Check if required packages are installed."""
    required = [
        'openai',
        'anthropic',
        'google.generativeai',
        'dotenv',
        'pydantic',
        'yaml',
        'httpx',
        'diskcache',
        'tenacity',
        'pythonjsonlogger'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("\nRun: pip install -r requirements.txt")
        return False
    
    return True


def check_env_file():
    """Check if .env file exists and has content."""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("❌ .env file not found")
        print("\nRun: cp .env.example .env")
        return False
    
    with open(env_file) as f:
        content = f.read()
    
    if 'your_' in content and 'your_key' in content:
        print("⚠️  .env file exists but contains placeholder values")
        print("   Please update with real API keys")
        return False
    
    print("✅ .env file configured")
    return True


def check_config_file():
    """Check if agents.yaml exists."""
    config_file = Path('config/agents.yaml')
    
    if not config_file.exists():
        print("❌ config/agents.yaml not found")
        return False
    
    print("✅ config/agents.yaml exists")
    return True


def check_directories():
    """Ensure required directories exist."""
    dirs = ['logs', 'generated_output', '.cache']
    
    for d in dirs:
        Path(d).mkdir(exist_ok=True)
    
    print("✅ Directory structure ready")
    return True


def main():
    """Run all checks."""
    print("\n" + "="*50)
    print("🧠 SwarmMind Setup Verification")
    print("="*50 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment File", check_env_file),
        ("Configuration", check_config_file),
        ("Directories", check_directories),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 {name}:")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append(False)
    
    print("\n" + "="*50)
    if all(results):
        print("✅ All checks passed! Ready to run:")
        print("   python src/main.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)
    
    print("="*50 + "\n")


if __name__ == "__main__":
    main()

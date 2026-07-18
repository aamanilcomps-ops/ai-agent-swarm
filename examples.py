#!/usr/bin/env python3
"""
SwarmMind Quick Start Examples
==============================
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import get_settings
from src.agents import AIAgent
from src.cache import CacheManager
from src.rate_limiter import RateLimiter
from src.tasks import run_autonomous_workflow


def example_single_agent():
    """Example: Use a single agent directly."""
    print("\n" + "="*60)
    print("Example 1: Single Agent")
    print("="*60 + "\n")
    
    settings = get_settings()
    
    agent = AIAgent(
        name="TechWriter",
        role="Technical Documentation Writer",
        goal="Write clear, concise technical documentation",
        provider="ollama",
        model="llama2"
    )
    
    response = agent.execute("Write a brief Python function to calculate factorial")
    print(f"Response:\n{response}\n")


def example_with_caching():
    """Example: Use caching to avoid duplicate API calls."""
    print("\n" + "="*60)
    print("Example 2: Response Caching")
    print("="*60 + "\n")
    
    settings = get_settings()
    cache = CacheManager(cache_dir='.cache', ttl_hours=24)
    
    agent = AIAgent(
        name="CodeGen",
        role="Python Code Generator",
        goal="Generate efficient, well-documented Python code",
        provider="ollama",
        model="llama2",
        cache_manager=cache
    )
    
    # First call - hits API
    print("First call (hits API):")
    response1 = agent.execute("Generate a hello world function")
    print(f"Response length: {len(response1)} chars\n")
    
    # Second call - served from cache
    print("Second call (from cache):")
    response2 = agent.execute("Generate a hello world function")
    print(f"Response length: {len(response2)} chars")
    print(f"Same response: {response1 == response2}\n")


def example_with_rate_limiting():
    """Example: Use rate limiting."""
    print("\n" + "="*60)
    print("Example 3: Rate Limiting")
    print("="*60 + "\n")
    
    settings = get_settings()
    rate_limiter = RateLimiter(requests_per_minute=60)
    
    agent = AIAgent(
        name="Analyzer",
        role="Code Analyzer",
        goal="Analyze and optimize code",
        provider="ollama",
        model="llama2",
        rate_limiter=rate_limiter
    )
    
    print("Rate limiter active. Making requests with throttling...")
    for i in range(3):
        print(f"Request {i+1}...")
        response = agent.execute(f"Analyze this simple request: {i}")
        print(f"  -> Response: {response[:50]}...\n")


def example_multi_agent_workflow():
    """Example: Full multi-agent workflow."""
    print("\n" + "="*60)
    print("Example 4: Multi-Agent Workflow")
    print("="*60 + "\n")
    
    settings = get_settings()
    cache = CacheManager() if settings.cache_enabled else None
    rate_limiter = RateLimiter() if settings.rate_limit_enabled else None
    
    # Initialize agents
    agents = {
        'manager_agent': AIAgent(
            name="Manager",
            role="Task Manager",
            goal="Break down tasks",
            provider="ollama",
            model="llama2",
            cache_manager=cache,
            rate_limiter=rate_limiter
        ),
        'research_agent': AIAgent(
            name="Researcher",
            role="Research Specialist",
            goal="Research topics",
            provider="ollama",
            model="llama2",
            cache_manager=cache,
            rate_limiter=rate_limiter
        ),
        'writer_agent': AIAgent(
            name="Writer",
            role="Documentation Writer",
            goal="Write documentation",
            provider="ollama",
            model="llama2",
            cache_manager=cache,
            rate_limiter=rate_limiter
        )
    }
    
    # Run workflow
    user_request = "Create a Python function that validates email addresses"
    print(f"User Request: {user_request}\n")
    
    try:
        result = run_autonomous_workflow(agents, user_request)
        print(f"\nFinal Output:\n{result}\n")
    except Exception as e:
        print(f"Error: {e}\n")


def example_custom_config():
    """Example: Use custom configuration."""
    print("\n" + "="*60)
    print("Example 5: Custom Configuration")
    print("="*60 + "\n")
    
    settings = get_settings()
    
    print(f"Current Configuration:")
    print(f"  Cache Enabled: {settings.cache_enabled}")
    print(f"  Cache TTL: {settings.cache_ttl_hours} hours")
    print(f"  Rate Limit: {settings.rate_limit_requests_per_minute} req/min")
    print(f"  Log Level: {settings.log_level}")
    print(f"  Timeout: {settings.timeout_seconds}s\n")
    
    print("To customize, edit your .env file with:")
    print("  CACHE_ENABLED=false")
    print("  CACHE_TTL_HOURS=48")
    print("  RATE_LIMIT_REQUESTS_PER_MINUTE=30")
    print("  LOG_LEVEL=DEBUG")
    print("  TIMEOUT_SECONDS=600\n")


def main():
    """Run examples."""
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + "  SwarmMind Quick Start Examples".center(58) + "█")
    print("█" + " "*58 + "█")
    print("█"*60)
    
    examples = [
        ("Single Agent", example_single_agent),
        ("Response Caching", example_with_caching),
        ("Rate Limiting", example_with_rate_limiting),
        ("Multi-Agent Workflow", example_multi_agent_workflow),
        ("Custom Configuration", example_custom_config),
    ]
    
    print("\nAvailable Examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\nSelect example (1-5) or 'all' for all examples:")
    choice = input("> ").strip().lower()
    
    if choice == 'all':
        for _, func in examples:
            try:
                func()
            except Exception as e:
                print(f"Error running example: {e}")
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        try:
            examples[int(choice)-1][1]()
        except Exception as e:
            print(f"Error running example: {e}")
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()

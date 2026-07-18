import os
import sys
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import get_settings
from src.logger import setup_logger
from src.agents import AIAgent
from src.tasks import run_autonomous_workflow
from src.executor import CodeExecutor
from src.cache import CacheManager
from src.rate_limiter import RateLimiter

logger = setup_logger(__name__)


def load_configuration() -> dict:
    """Load and validate configuration."""
    try:
        config_path = Path(__file__).parent.parent / 'config' / 'agents.yaml'
        
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        
        logger.info(f"Configuration loaded from {config_path}")
        return config
    
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        raise


def initialize_agents(config: dict, settings) -> dict:
    """Initialize AI agents with proper configuration."""
    agents = {}
    
    try:
        # Initialize cache and rate limiter
        cache_manager = CacheManager(
            cache_dir=settings.cache_dir,
            ttl_hours=settings.cache_ttl_hours
        ) if settings.cache_enabled else None
        
        rate_limiter = RateLimiter(
            requests_per_minute=settings.rate_limit_requests_per_minute
        ) if settings.rate_limit_enabled else None
        
        # Initialize each agent
        for agent_key, agent_config in config.items():
            provider = agent_config.get('provider', 'ollama').lower()
            model = agent_config.get('model', settings.ollama_model)
            
            # Prepare provider-specific kwargs
            provider_kwargs = {
                'cache_manager': cache_manager,
                'rate_limiter': rate_limiter,
                'enable_cache': settings.cache_enabled,
                'enable_rate_limit': settings.rate_limit_enabled
            }
            
            # Add API keys based on provider
            if provider == 'openai':
                if not settings.openai_api_key or settings.openai_api_key == 'your_openai_key_here':
                    logger.warning(f"OpenAI API key not configured for {agent_key}")
                else:
                    provider_kwargs['api_key'] = settings.openai_api_key
            
            elif provider == 'anthropic':
                if not settings.anthropic_api_key or settings.anthropic_api_key == 'your_anthropic_key_here':
                    logger.warning(f"Anthropic API key not configured for {agent_key}")
                else:
                    provider_kwargs['api_key'] = settings.anthropic_api_key
            
            elif provider in ['gemini', 'google']:
                if not settings.gemini_api_key or settings.gemini_api_key == 'your_gemini_key_here':
                    logger.warning(f"Gemini API key not configured for {agent_key}")
                else:
                    provider_kwargs['api_key'] = settings.gemini_api_key
            
            elif provider == 'ollama':
                provider_kwargs['host'] = settings.ollama_host
            
            # Create agent
            agents[agent_key] = AIAgent(
                name=agent_config['name'],
                role=agent_config['role'],
                goal=agent_config['goal'],
                provider=provider,
                model=model,
                **provider_kwargs
            )
            
            logger.info(f"Agent '{agent_key}' initialized: {agent_config['name']}")
        
        return agents
    
    except Exception as e:
        logger.error(f"Failed to initialize agents: {e}")
        raise


def main():
    """Main application entry point."""
    try:
        # Load environment
        load_dotenv()
        logger.info("🚀 SwarmMind Starting Up")
        
        # Load settings
        settings = get_settings()
        logger.info(f"Settings loaded. Log level: {settings.log_level}, Format: {settings.log_format}")
        
        # Validate API keys
        try:
            available_keys = settings.validate_api_keys()
            logger.info(f"Available API providers: {list(available_keys.keys())}")
        except ValueError as e:
            logger.warning(f"API key validation: {e}")
        
        # Load agent configuration
        config = load_configuration()
        
        # Initialize agents
        agents = initialize_agents(config, settings)
        
        # Initialize code executor
        executor = CodeExecutor(
            output_dir='generated_output',
            timeout_seconds=settings.timeout_seconds,
            enable_execution=settings.enable_code_execution
        )
        
        # Display startup banner
        print("\n" + "="*60)
        print("🧠 SWARMMIND: AUTONOMOUS MULTI-AGENT AI SYSTEM")
        print("="*60)
        print(f"✅ Agents initialized: {', '.join(agents.keys())}")
        print(f"📦 Cache: {'ENABLED' if settings.cache_enabled else 'DISABLED'}")
        print(f"⏱️  Rate limiting: {'ENABLED' if settings.rate_limit_enabled else 'DISABLED'}")
        print(f"⚙️  Code execution: {'ENABLED' if settings.enable_code_execution else 'DISABLED'}")
        print("="*60 + "\n")
        
        # Main loop
        while True:
            try:
                user_prompt = input("Enter what you want the AI swarm to build/analyze (or 'quit' to exit):\n> ").strip()
                
                if not user_prompt:
                    print("❌ Please enter a prompt.\n")
                    continue
                
                if user_prompt.lower() in ['quit', 'exit', 'q']:
                    logger.info("User initiated shutdown")
                    print("\n👋 Goodbye!\n")
                    break
                
                # Special commands
                if user_prompt.lower() == 'status':
                    print("\n📊 System Status:")
                    for agent_key, agent in agents.items():
                        print(f"  {agent_key}: {agent.get_status()}")
                    print()
                    continue
                
                if user_prompt.lower() == 'cache_clear':
                    if settings.cache_enabled:
                        # Access cache manager through first agent
                        first_agent = next(iter(agents.values()))
                        if first_agent.cache_manager:
                            first_agent.cache_manager.clear()
                            print("✅ Cache cleared\n")
                    continue
                
                # Run workflow
                logger.info(f"User request: {user_prompt}")
                result_code = run_autonomous_workflow(agents, user_prompt)
                
                # Execute generated code
                success = executor.execute(result_code)
                
                if not success:
                    logger.warning("Code execution failed or disabled")
                    print("Generated code saved but execution failed. Check output in 'generated_output/'")
                
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received")
                print("\n\n❌ Interrupted by user\n")
                break
            except Exception as e:
                logger.error(f"Workflow error: {e}")
                print(f"\n💥 Error: {e}\n")
    
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        print(f"\n💥 Fatal error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()

import json
import httpx
from typing import Optional
from src.logger import setup_logger
from src.cache import CacheManager
from src.rate_limiter import RateLimiter, retry_with_backoff
from src.llm_providers import get_provider

logger = setup_logger(__name__)


class AIAgent:
    """Enhanced AI Agent with caching, rate limiting, and multi-provider support."""
    
    def __init__(
        self,
        name: str,
        role: str,
        goal: str,
        provider: str,
        model: str,
        cache_manager: Optional[CacheManager] = None,
        rate_limiter: Optional[RateLimiter] = None,
        enable_cache: bool = True,
        enable_rate_limit: bool = True,
        **kwargs
    ):
        """
        Initialize AIAgent.
        
        Args:
            name: Agent name
            role: Agent role description
            goal: Agent goal/objective
            provider: LLM provider name (openai, anthropic, gemini, ollama)
            model: Model name for the provider
            cache_manager: Optional CacheManager instance
            rate_limiter: Optional RateLimiter instance
            enable_cache: Whether to enable response caching
            enable_rate_limit: Whether to enable rate limiting
            **kwargs: Additional arguments for provider
        """
        self.name = name
        self.role = role
        self.goal = goal
        self.provider_name = provider
        self.model = model
        
        self.enable_cache = enable_cache
        self.enable_rate_limit = enable_rate_limit
        self.cache_manager = cache_manager
        self.rate_limiter = rate_limiter
        
        # Build system prompt
        self.system_prompt = (
            f"You are {self.name}, the {self.role}. Goal: {self.goal}. "
            f"Respond with ONLY raw, executable Python code. No markdown formatting ticks."
        )
        
        # Initialize LLM provider
        provider_kwargs = {
            'model': model,
            **kwargs
        }
        
        # Add API key if available
        if provider.lower() == 'openai' and kwargs.get('api_key'):
            provider_kwargs['api_key'] = kwargs['api_key']
        elif provider.lower() == 'anthropic' and kwargs.get('api_key'):
            provider_kwargs['api_key'] = kwargs['api_key']
        elif provider.lower() in ['gemini', 'google'] and kwargs.get('api_key'):
            provider_kwargs['api_key'] = kwargs['api_key']
        elif provider.lower() == 'ollama':
            provider_kwargs['host'] = kwargs.get('host', 'http://localhost:11434')
        
        self.llm_provider = get_provider(provider, **provider_kwargs)
        
        if not self.llm_provider:
            logger.error(f"Failed to initialize provider {provider}")
            raise ValueError(f"Invalid or unavailable provider: {provider}")
        
        logger.info(f"Agent {self.name} initialized with provider {provider}")
    
    def execute(self, task_prompt: str, context: str = "") -> str:
        """
        Execute agent task with caching and rate limiting.
        
        Args:
            task_prompt: Task description
            context: Additional context information
        
        Returns:
            Agent response
        
        Raises:
            Exception: If execution fails after retries
        """
        logger.info(f"[Agent] {self.name} starting execution")
        
        full_prompt = f"Context: {context}\n\nTask: {task_prompt}" if context else task_prompt
        
        # Check cache first
        if self.enable_cache and self.cache_manager:
            cached_response = self.cache_manager.get(
                self.name,
                task_prompt,
                context
            )
            if cached_response:
                logger.info(f"[Agent] {self.name} retrieved cached response")
                return cached_response
        
        # Apply rate limiting
        if self.enable_rate_limit and self.rate_limiter:
            self.rate_limiter.wait_if_needed(self.provider_name)
        
        # Call LLM provider
        try:
            logger.info(f"[Agent] {self.name} calling {self.provider_name} provider")
            response = self._call_llm(full_prompt)
            
            # Cache successful response
            if self.enable_cache and self.cache_manager:
                self.cache_manager.set(
                    self.name,
                    task_prompt,
                    response,
                    context
                )
            
            logger.info(f"[Agent] {self.name} execution completed successfully")
            return response
        
        except Exception as e:
            logger.error(f"[Agent] {self.name} execution failed: {e}")
            raise
    
    @retry_with_backoff(max_attempts=3, initial_delay=1, max_delay=10)
    def _call_llm(self, prompt: str) -> str:
        """
        Internal method to call LLM with retry logic.
        
        Args:
            prompt: Full prompt including context and task
        
        Returns:
            LLM response
        """
        return self.llm_provider.call(
            system_prompt=self.system_prompt,
            user_prompt=prompt
        )
    
    def get_status(self) -> dict:
        """Get agent status information."""
        return {
            'name': self.name,
            'role': self.role,
            'goal': self.goal,
            'provider': self.provider_name,
            'model': self.model,
            'cache_enabled': self.enable_cache,
            'rate_limit_enabled': self.enable_rate_limit
        }

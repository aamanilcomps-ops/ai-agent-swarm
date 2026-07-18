import hashlib
import json
import os
from typing import Any, Optional
from datetime import datetime, timedelta
import diskcache as dc
from src.logger import setup_logger

logger = setup_logger(__name__)


class CacheManager:
    """Manage agent response caching with TTL and serialization."""
    
    def __init__(self, cache_dir: str = '.cache', ttl_hours: int = 24):
        """
        Initialize cache manager.
        
        Args:
            cache_dir: Directory to store cache
            ttl_hours: Time-to-live for cache entries in hours
        """
        self.cache_dir = cache_dir
        self.ttl_seconds = ttl_hours * 3600
        self.cache = dc.Cache(cache_dir)
        logger.info(f'Cache initialized at {cache_dir} with TTL {ttl_hours}h')
    
    @staticmethod
    def _generate_key(agent_name: str, task_prompt: str, context: str = '') -> str:
        """Generate cache key from agent and task parameters."""
        combined = f'{agent_name}:{task_prompt}:{context}'
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def get(self, agent_name: str, task_prompt: str, context: str = '') -> Optional[str]:
        """
        Retrieve cached response if available and not expired.
        
        Args:
            agent_name: Name of the agent
            task_prompt: Task prompt string
            context: Additional context (optional)
        
        Returns:
            Cached response or None if not found/expired
        """
        key = self._generate_key(agent_name, task_prompt, context)
        
        try:
            cached_data = self.cache.get(key)
            if cached_data:
                timestamp, response = cached_data
                elapsed = datetime.now() - timestamp
                
                if elapsed.total_seconds() < self.ttl_seconds:
                    logger.debug(f'Cache HIT for {agent_name}')
                    return response
                else:
                    logger.debug(f'Cache EXPIRED for {agent_name}')
                    del self.cache[key]
        except Exception as e:
            logger.warning(f'Cache retrieval error: {e}')
        
        return None
    
    def set(self, agent_name: str, task_prompt: str, response: str, context: str = '') -> bool:
        """
        Store response in cache.
        
        Args:
            agent_name: Name of the agent
            task_prompt: Task prompt string
            response: Response to cache
            context: Additional context (optional)
        
        Returns:
            True if cached successfully, False otherwise
        """
        key = self._generate_key(agent_name, task_prompt, context)
        
        try:
            self.cache[key] = (datetime.now(), response)
            logger.debug(f'Cached response for {agent_name}')
            return True
        except Exception as e:
            logger.error(f'Cache storage error: {e}')
            return False
    
    def clear(self) -> None:
        """Clear all cache entries."""
        try:
            self.cache.clear()
            logger.info('Cache cleared')
        except Exception as e:
            logger.error(f'Cache clear error: {e}')
    
    def get_stats(self) -> dict:
        """Get cache statistics."""
        try:
            return {
                'cache_dir': self.cache_dir,
                'cache_size': len(self.cache),
                'ttl_hours': self.ttl_seconds / 3600
            }
        except Exception as e:
            logger.error(f'Cache stats error: {e}')
            return {}
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.cache.close()

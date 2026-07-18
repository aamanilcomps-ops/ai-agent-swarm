import time
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Callable, Any, TypeVar
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from src.logger import setup_logger

logger = setup_logger(__name__)

F = TypeVar('F', bound=Callable[..., Any])


class RateLimiter:
    """Rate limiter with per-provider tracking and token bucket algorithm."""
    
    def __init__(self, requests_per_minute: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_minute: Maximum requests per minute
        """
        self.requests_per_minute = requests_per_minute
        self.request_times = defaultdict(list)
        self.min_interval = 60.0 / requests_per_minute
    
    def is_allowed(self, provider: str) -> bool:
        """
        Check if request is allowed for provider.
        
        Args:
            provider: API provider name
        
        Returns:
            True if request allowed, False if rate limited
        """
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        
        # Clean up old timestamps
        self.request_times[provider] = [
            ts for ts in self.request_times[provider]
            if ts > minute_ago
        ]
        
        if len(self.request_times[provider]) >= self.requests_per_minute:
            logger.warning(f'Rate limit exceeded for {provider}')
            return False
        
        self.request_times[provider].append(now)
        return True
    
    def wait_if_needed(self, provider: str) -> None:
        """Wait if necessary to maintain rate limit."""
        if not self.is_allowed(provider):
            wait_time = self.min_interval
            logger.info(f'Rate limited. Waiting {wait_time:.2f}s')
            time.sleep(wait_time)


def retry_with_backoff(
    max_attempts: int = 3,
    initial_delay: int = 1,
    max_delay: int = 60
) -> Callable[[F], F]:
    """
    Decorator for retry logic with exponential backoff.
    
    Args:
        max_attempts: Maximum number of attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
    
    Returns:
        Decorated function with retry logic
    """
    def decorator(func: F) -> F:
        @retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(
                multiplier=initial_delay,
                min=initial_delay,
                max=max_delay
            ),
            retry=retry_if_exception_type((
                ConnectionError,
                TimeoutError,
                Exception
            )),
            reraise=True
        )
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    
    return decorator

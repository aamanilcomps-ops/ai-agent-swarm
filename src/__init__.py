"""SwarmMind - Autonomous Multi-Agent AI System

A comprehensive AI orchestration framework with multi-provider LLM support,
intelligent caching, rate limiting, and safe code execution.
"""

__version__ = "2.0.0"
__author__ = "SwarmMind Team"
__license__ = "MIT"

from src.config import get_settings
from src.logger import setup_logger
from src.agents import AIAgent
from src.cache import CacheManager
from src.rate_limiter import RateLimiter
from src.executor import CodeExecutor
from src.tasks import run_autonomous_workflow

__all__ = [
    'get_settings',
    'setup_logger',
    'AIAgent',
    'CacheManager',
    'RateLimiter',
    'CodeExecutor',
    'run_autonomous_workflow'
]

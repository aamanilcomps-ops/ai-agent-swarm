import os
from pydantic_settings import BaseSettings
from pydantic import validator
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Centralized configuration management with validation."""
    
    # API Keys
    openai_api_key: Optional[str] = os.getenv('OPENAI_API_KEY')
    anthropic_api_key: Optional[str] = os.getenv('ANTHROPIC_API_KEY')
    gemini_api_key: Optional[str] = os.getenv('GEMINI_API_KEY')
    
    # Ollama Configuration
    ollama_host: str = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    ollama_model: str = os.getenv('OLLAMA_MODEL', 'llama2')
    
    # Cache Configuration
    cache_enabled: bool = os.getenv('CACHE_ENABLED', 'true').lower() == 'true'
    cache_ttl_hours: int = int(os.getenv('CACHE_TTL_HOURS', '24'))
    cache_dir: str = os.getenv('CACHE_DIR', '.cache')
    
    # Rate Limiting
    rate_limit_enabled: bool = os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'true'
    rate_limit_requests_per_minute: int = int(os.getenv('RATE_LIMIT_REQUESTS_PER_MINUTE', '60'))
    rate_limit_retry_attempts: int = int(os.getenv('RATE_LIMIT_RETRY_ATTEMPTS', '3'))
    rate_limit_retry_delay_seconds: int = int(os.getenv('RATE_LIMIT_RETRY_DELAY_SECONDS', '2'))
    
    # Logging
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    log_format: str = os.getenv('LOG_FORMAT', 'json')
    log_dir: str = os.getenv('LOG_DIR', 'logs')
    
    # Execution
    enable_code_execution: bool = os.getenv('ENABLE_CODE_EXECUTION', 'true').lower() == 'true'
    timeout_seconds: int = int(os.getenv('TIMEOUT_SECONDS', '300'))
    max_retries: int = int(os.getenv('MAX_RETRIES', '3'))
    
    @validator('cache_ttl_hours', 'timeout_seconds', 'max_retries', 
               'rate_limit_requests_per_minute', 'rate_limit_retry_attempts')
    def positive_integers(cls, v):
        if v <= 0:
            raise ValueError('Must be positive')
        return v
    
    @validator('log_level')
    def valid_log_level(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'Must be one of {valid_levels}')
        return v.upper()
    
    @validator('log_format')
    def valid_log_format(cls, v):
        if v.lower() not in ['json', 'text']:
            raise ValueError('Must be json or text')
        return v.lower()
    
    def validate_api_keys(self) -> dict:
        """Validate that at least one API key is configured."""
        available_keys = {}
        if self.openai_api_key and self.openai_api_key != 'your_openai_key_here':
            available_keys['openai'] = True
        if self.anthropic_api_key and self.anthropic_api_key != 'your_anthropic_key_here':
            available_keys['anthropic'] = True
        if self.gemini_api_key and self.gemini_api_key != 'your_gemini_key_here':
            available_keys['gemini'] = True
        
        if not available_keys:
            raise ValueError('No valid API keys configured. Please set OPENAI_API_KEY, ANTHROPIC_API_KEY, or GEMINI_API_KEY in .env')
        
        return available_keys
    
    class Config:
        env_file = '.env'
        case_sensitive = False


def get_settings() -> Settings:
    """Get or create settings instance."""
    return Settings()

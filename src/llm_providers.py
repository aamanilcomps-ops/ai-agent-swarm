import json
import httpx
import time
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
from src.logger import setup_logger
from src.rate_limiter import retry_with_backoff

logger = setup_logger(__name__)


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def call(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Call the LLM provider."""
        pass
    
    @abstractmethod
    def validate_api_key(self) -> bool:
        """Validate if API key is configured."""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI API provider with GPT models."""
    
    def __init__(self, api_key: str, model: str = "gpt-4o", timeout: float = 60.0):
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.endpoint = "https://api.openai.com/v1/chat/completions"
    
    def validate_api_key(self) -> bool:
        return bool(self.api_key and self.api_key != 'your_openai_key_here')
    
    @retry_with_backoff(max_attempts=3)
    def call(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Call OpenAI API."""
        try:
            with httpx.Client() as client:
                response = client.post(
                    self.endpoint,
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        "temperature": kwargs.get("temperature", 0.7),
                        "max_tokens": kwargs.get("max_tokens", 2000)
                    },
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data['choices'][0]['message']['content']
                else:
                    logger.error(f"OpenAI error: {response.status_code} - {response.text}")
                    raise Exception(f"OpenAI API error: {response.status_code}")
        except Exception as e:
            logger.error(f"OpenAI call failed: {e}")
            raise


class AnthropicProvider(LLMProvider):
    """Anthropic Claude API provider."""
    
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet", timeout: float = 60.0):
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.endpoint = "https://api.anthropic.com/v1/messages"
    
    def validate_api_key(self) -> bool:
        return bool(self.api_key and self.api_key != 'your_anthropic_key_here')
    
    @retry_with_backoff(max_attempts=3)
    def call(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Call Anthropic API."""
        try:
            with httpx.Client() as client:
                response = client.post(
                    self.endpoint,
                    json={
                        "model": self.model,
                        "max_tokens": kwargs.get("max_tokens", 2000),
                        "system": system_prompt,
                        "messages": [
                            {"role": "user", "content": user_prompt}
                        ]
                    },
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01"
                    },
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data['content'][0]['text']
                else:
                    logger.error(f"Anthropic error: {response.status_code} - {response.text}")
                    raise Exception(f"Anthropic API error: {response.status_code}")
        except Exception as e:
            logger.error(f"Anthropic call failed: {e}")
            raise


class GoogleGenAIProvider(LLMProvider):
    """Google Generative AI provider (Gemini)."""
    
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash", timeout: float = 60.0):
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    
    def validate_api_key(self) -> bool:
        return bool(self.api_key and self.api_key != 'your_gemini_key_here')
    
    @retry_with_backoff(max_attempts=3)
    def call(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Call Google Generative AI API."""
        try:
            with httpx.Client() as client:
                response = client.post(
                    f"{self.endpoint}?key={self.api_key}",
                    json={
                        "system_instruction": {"parts": [{"text": system_prompt}]},
                        "contents": [
                            {"parts": [{"text": user_prompt}]}
                        ],
                        "generation_config": {
                            "temperature": kwargs.get("temperature", 0.7),
                            "max_output_tokens": kwargs.get("max_tokens", 2000)
                        }
                    },
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data['candidates'][0]['content']['parts'][0]['text']
                else:
                    logger.error(f"Google API error: {response.status_code} - {response.text}")
                    raise Exception(f"Google API error: {response.status_code}")
        except Exception as e:
            logger.error(f"Google API call failed: {e}")
            raise


class OllamaProvider(LLMProvider):
    """Local Ollama inference provider for offline usage."""
    
    def __init__(self, host: str = "http://localhost:11434", model: str = "llama2"):
        self.host = host
        self.model = model
        self.endpoint = f"{host}/api/chat"
    
    def validate_api_key(self) -> bool:
        """Ollama doesn't require API keys."""
        return True
    
    @retry_with_backoff(max_attempts=3)
    def call(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Call local Ollama instance."""
        try:
            with httpx.Client() as client:
                response = client.post(
                    self.endpoint,
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        "stream": False
                    },
                    timeout=kwargs.get("timeout", 300)
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data['message']['content']
                else:
                    logger.error(f"Ollama error: {response.status_code}")
                    raise Exception(f"Ollama error: {response.status_code}")
        except Exception as e:
            logger.error(f"Ollama call failed: {e}")
            raise


def get_provider(provider_name: str, **kwargs) -> Optional[LLMProvider]:
    """
    Factory function to get appropriate LLM provider.
    
    Args:
        provider_name: Name of the provider (openai, anthropic, gemini, ollama)
        **kwargs: Additional arguments for provider initialization
    
    Returns:
        Configured provider instance or None if invalid
    """
    providers = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "gemini": GoogleGenAIProvider,
        "google": GoogleGenAIProvider,
        "ollama": OllamaProvider
    }
    
    provider_class = providers.get(provider_name.lower())
    if not provider_class:
        logger.error(f"Unknown provider: {provider_name}")
        return None
    
    try:
        return provider_class(**kwargs)
    except Exception as e:
        logger.error(f"Failed to initialize {provider_name} provider: {e}")
        return None

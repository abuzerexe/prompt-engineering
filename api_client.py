"""
API client wrapper for LLM providers (Gemini and OpenAI)
"""
import logging
from openai import OpenAI
from google import genai

from config import (
    GEMINI_API_KEY, OPEN_ROUTER_API_KEY, OPEN_ROUTER_BASE_URL,
    DEFAULT_GEMINI_MODEL, DEFAULT_OPENAI_MODEL, MAX_TOKENS
)
from models import APIResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMAPIClient:
    """
    Unified client for interacting with different LLM APIs
    """
    
    def __init__(self):
        """Initialize API clients"""
        self.gemini_client = None
        self.openai_client = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize API clients with error handling"""
        # Initialize Gemini client
        try:
            if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_key":
                genai.configure(api_key=GEMINI_API_KEY)
                self.gemini_client = genai
                logger.info("Gemini client initialized successfully")
            else:
                logger.warning("Gemini API key not configured")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
        
        # Initialize OpenAI client (via OpenRouter)
        try:
            if OPEN_ROUTER_API_KEY and OPEN_ROUTER_API_KEY != "your_openrouter_key":
                self.openai_client = OpenAI(
                    base_url=OPEN_ROUTER_BASE_URL,
                    api_key=OPEN_ROUTER_API_KEY
                )
                logger.info("OpenAI client initialized successfully")
            else:
                logger.warning("OpenRouter API key not configured")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
    
    def call_gemini(self, prompt: str, model: str = DEFAULT_GEMINI_MODEL) -> APIResponse:
        """
        Make API call to Gemini
        
        Args:
            prompt: The prompt to send
            model: Model to use (default: gemini-2.5-flash)
            
        Returns:
            APIResponse object with response data
        """
        if not self.gemini_client:
            return APIResponse(
                response="",
                model="Gemini",
                token_usage={},
                success=False,
                error_message="Gemini client not initialized"
            )
        
        try:
            response = self.gemini_client.models.generate_content(
                model=model,
                contents=prompt
            )
            
            # Extract token usage information
            usage = response.usage_metadata
            token_usage = {
                "prompt_tokens": usage.prompt_token_count,
                "completion_tokens": usage.candidates_token_count,
                "total_tokens": usage.total_token_count
            }
            
            return APIResponse(
                response=response.text,
                model="Gemini",
                token_usage=token_usage,
                success=True
            )
            
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            return APIResponse(
                response="",
                model="Gemini",
                token_usage={},
                success=False,
                error_message=str(e)
            )
    
    def call_openai(self, prompt: str, model: str = DEFAULT_OPENAI_MODEL) -> APIResponse:
        """
        Make API call to OpenAI (via OpenRouter)
        
        Args:
            prompt: The prompt to send
            model: Model to use (default: openai/gpt-4o)
            
        Returns:
            APIResponse object with response data
        """
        if not self.openai_client:
            return APIResponse(
                response="",
                model="OpenAI",
                token_usage={},
                success=False,
                error_message="OpenAI client not initialized"
            )
        
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=MAX_TOKENS
            )
            
            # Extract response and token usage
            content = response.choices[0].message.content
            token_usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
            
            return APIResponse(
                response=content,
                model="OpenAI",
                token_usage=token_usage,
                success=True
            )
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            return APIResponse(
                response="",
                model="OpenAI",
                token_usage={},
                success=False,
                error_message=str(e)
            )
    
    def call_api(self, prompt: str, provider: str = "gemini") -> APIResponse:
        """
        Make API call to specified provider
        
        Args:
            prompt: The prompt to send
            provider: API provider ('gemini' or 'openai')
            
        Returns:
            APIResponse object with response data
        """
        provider = provider.lower()
        
        if provider == "gemini":
            return self.call_gemini(prompt)
        elif provider == "openai":
            return self.call_openai(prompt)
        else:
            return APIResponse(
                response="",
                model="Unknown",
                token_usage={},
                success=False,
                error_message=f"Unsupported provider: {provider}"
            )
    
    def test_connection(self, provider: str = "gemini") -> bool:
        """
        Test API connection
        
        Args:
            provider: API provider to test
            
        Returns:
            True if connection successful, False otherwise
        """
        test_prompt = "Say 'Hello' if you can receive this message."
        response = self.call_api(test_prompt, provider)
        return response.success and "hello" in response.response.lower()
    
    def get_available_providers(self) -> list:
        """
        Get list of available API providers
        
        Returns:
            List of available provider names
        """
        providers = []
        if self.gemini_client:
            providers.append("gemini")
        if self.openai_client:
            providers.append("openai")
        return providers
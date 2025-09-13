
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

class LLMClient:
    """
    Unified client for interacting with different LLM APIs
    """
    
    def __init__(self, provider: str = "gemini"):
        """
        Initialize API client
        
        Args:
            provider: API provider to use ("gemini" or "openai")
        """
        self.provider = provider.lower()
        self.gemini_client = None
        self.openai_client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate API client"""
        if self.provider == "gemini":
            self._initialize_gemini()
        elif self.provider == "openai":
            self._initialize_openai()
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _initialize_gemini(self):
        """Initialize Gemini client"""
        try:
            if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_key":
                raise ValueError("Gemini API key not configured")
            
            genai.configure(api_key=GEMINI_API_KEY)
            self.gemini_client = genai
            logger.info("Gemini client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            raise
    
    def _initialize_openai(self):
        """Initialize OpenAI client via OpenRouter"""
        try:
            if not OPEN_ROUTER_API_KEY or OPEN_ROUTER_API_KEY == "your_openrouter_key":
                raise ValueError("OpenRouter API key not configured")
            
            self.openai_client = OpenAI(
                base_url=OPEN_ROUTER_BASE_URL,
                api_key=OPEN_ROUTER_API_KEY
            )
            logger.info("OpenAI client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise
    
    def generate_response(self, prompt: str, temperature: float = 0.7, 
                         max_tokens: int = MAX_TOKENS) -> APIResponse:
        """
        Generate response using the configured provider
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            APIResponse with generated content and metadata
        """
        if self.provider == "gemini":
            return self._call_gemini(prompt, temperature, max_tokens)
        elif self.provider == "openai":
            return self._call_openai(prompt, temperature, max_tokens)
        else:
            return APIResponse(
                content="",
                model="Unknown",
                temperature=temperature,
                success=False,
                error_message=f"Unsupported provider: {self.provider}"
            )
    
    def _call_gemini(self, prompt: str, temperature: float, max_tokens: int) -> APIResponse:
        """Make API call to Gemini"""
        try:
            model = genai.GenerativeModel(DEFAULT_GEMINI_MODEL)
            
            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )
            
            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            # Extract token usage information
            usage = response.usage_metadata
            tokens_used = usage.total_token_count if usage else 0
            
            return APIResponse(
                content=response.text,
                model="Gemini",
                temperature=temperature,
                tokens_used=tokens_used,
                success=True
            )
            
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            return APIResponse(
                content="",
                model="Gemini",
                temperature=temperature,
                success=False,
                error_message=str(e)
            )
    
    def _call_openai(self, prompt: str, temperature: float, max_tokens: int) -> APIResponse:
        """Make API call to OpenAI via OpenRouter"""
        try:
            response = self.openai_client.chat.completions.create(
                model=DEFAULT_OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Extract response content and token usage
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            return APIResponse(
                content=content,
                model="OpenAI",
                temperature=temperature,
                tokens_used=tokens_used,
                success=True
            )
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            return APIResponse(
                content="",
                model="OpenAI", 
                temperature=temperature,
                success=False,
                error_message=str(e)
            )
    
    def test_connection(self) -> bool:
        """
        Test API connection with a simple prompt
        
        Returns:
            True if connection successful, False otherwise
        """
        test_prompt = "Say 'Connection successful' if you can read this."
        response = self.generate_response(test_prompt, temperature=0.1)
        
        return (response.success and 
                "connection successful" in response.content.lower())
    
    def get_provider_info(self) -> dict:
        """
        Get information about the current provider
        
        Returns:
            Dictionary with provider information
        """
        return {
            "provider": self.provider,
            "model": DEFAULT_GEMINI_MODEL if self.provider == "gemini" else DEFAULT_OPENAI_MODEL,
            "initialized": (self.gemini_client is not None if self.provider == "gemini" 
                          else self.openai_client is not None)
        }

class APIClientManager:
    """Manager class for handling multiple API clients"""
    
    def __init__(self):
        """Initialize manager"""
        self.clients = {}
        self._initialize_available_clients()
    
    def _initialize_available_clients(self):
        """Initialize all available API clients"""
        providers = ["gemini", "openai"]
        
        for provider in providers:
            try:
                client = LLMClient(provider)
                if client.test_connection():
                    self.clients[provider] = client
                    logger.info(f"{provider} client initialized and tested successfully")
                else:
                    logger.warning(f"{provider} client initialized but connection test failed")
            except Exception as e:
                logger.warning(f"Could not initialize {provider} client: {e}")
    
    def get_client(self, provider: str = None) -> LLMClient:
        """
        Get API client for specified provider
        
        Args:
            provider: Preferred provider, or None for first available
            
        Returns:
            LLMClient instance
            
        Raises:
            ValueError: If no clients available or provider not found
        """
        if not self.clients:
            raise ValueError("No API clients available. Check your API keys.")
        
        if provider:
            if provider in self.clients:
                return self.clients[provider]
            else:
                raise ValueError(f"Provider '{provider}' not available. Available: {list(self.clients.keys())}")
        
        # Return first available client
        return next(iter(self.clients.values()))
    
    def get_available_providers(self) -> list:
        """Get list of available providers"""
        return list(self.clients.keys())
    
    def test_all_connections(self) -> dict:
        """Test all client connections"""
        results = {}
        for provider, client in self.clients.items():
            results[provider] = client.test_connection()
        return results
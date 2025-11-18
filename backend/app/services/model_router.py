"""
Model Router Service
Routes requests to different AI model providers (OpenAI, Anthropic, Gemini, etc.)
"""
import logging
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class ModelProvider(ABC):
    """Abstract base class for model providers"""

    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from the model"""
        pass

    @abstractmethod
    async def generate_structured(self, prompt: str, schema: Dict, **kwargs) -> Dict:
        """Generate structured response"""
        pass


class OpenAIProvider(ModelProvider):
    """OpenAI model provider"""

    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview"):
        self.api_key = api_key
        self.model = model
        try:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key=api_key)
        except ImportError:
            logger.error("OpenAI library not installed")
            self.client = None

    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using OpenAI"""
        if not self.client:
            raise ValueError("OpenAI client not initialized")

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2000)
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI generation error: {str(e)}")
            raise

    async def generate_structured(self, prompt: str, schema: Dict, **kwargs) -> Dict:
        """Generate structured response using function calling"""
        if not self.client:
            raise ValueError("OpenAI client not initialized")

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                functions=[{
                    "name": "structured_output",
                    "parameters": schema
                }],
                function_call={"name": "structured_output"},
                temperature=kwargs.get("temperature", 0.7)
            )
            import json
            return json.loads(response.choices[0].message.function_call.arguments)
        except Exception as e:
            logger.error(f"OpenAI structured generation error: {str(e)}")
            raise


class AnthropicProvider(ModelProvider):
    """Anthropic Claude model provider"""

    def __init__(self, api_key: str, model: str = "claude-3-opus-20240229"):
        self.api_key = api_key
        self.model = model
        try:
            from anthropic import AsyncAnthropic
            self.client = AsyncAnthropic(api_key=api_key)
        except ImportError:
            logger.error("Anthropic library not installed")
            self.client = None

    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using Anthropic"""
        if not self.client:
            raise ValueError("Anthropic client not initialized")

        try:
            message = await self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.get("max_tokens", 2000),
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7)
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Anthropic generation error: {str(e)}")
            raise

    async def generate_structured(self, prompt: str, schema: Dict, **kwargs) -> Dict:
        """Generate structured response"""
        # Anthropic doesn't have native function calling, so we use prompt engineering
        structured_prompt = f"{prompt}\n\nPlease respond with valid JSON matching this schema:\n{schema}"
        response = await self.generate(structured_prompt, **kwargs)

        import json
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            import re
            json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            raise


class GeminiProvider(ModelProvider):
    """Google Gemini model provider"""

    def __init__(self, api_key: str, model: str = "gemini-pro"):
        self.api_key = api_key
        self.model = model
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.client = genai.GenerativeModel(model)
        except ImportError:
            logger.error("Google GenerativeAI library not installed")
            self.client = None

    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using Gemini"""
        if not self.client:
            raise ValueError("Gemini client not initialized")

        try:
            response = await self.client.generate_content_async(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini generation error: {str(e)}")
            raise

    async def generate_structured(self, prompt: str, schema: Dict, **kwargs) -> Dict:
        """Generate structured response"""
        structured_prompt = f"{prompt}\n\nRespond with valid JSON:\n{schema}"
        response = await self.generate(structured_prompt, **kwargs)

        import json
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            import re
            json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            raise


class ModelRouter:
    """Routes requests to appropriate AI model providers"""

    def __init__(self):
        self.providers: Dict[str, ModelProvider] = {}
        logger.info("ModelRouter initialized")

    def register_provider(self, name: str, provider: ModelProvider):
        """Register a model provider"""
        self.providers[name] = provider
        logger.info(f"Registered provider: {name}")

    def configure_openai(self, api_key: str, model: str = "gpt-4-turbo-preview"):
        """Configure OpenAI provider"""
        self.register_provider("openai", OpenAIProvider(api_key, model))

    def configure_anthropic(self, api_key: str, model: str = "claude-3-opus-20240229"):
        """Configure Anthropic provider"""
        self.register_provider("anthropic", AnthropicProvider(api_key, model))

    def configure_gemini(self, api_key: str, model: str = "gemini-pro"):
        """Configure Gemini provider"""
        self.register_provider("gemini", GeminiProvider(api_key, model))

    async def generate(
        self,
        prompt: str,
        provider: str = "openai",
        **kwargs
    ) -> str:
        """
        Generate response using specified provider

        Args:
            prompt: The prompt to send to the model
            provider: Provider name (openai, anthropic, gemini)
            **kwargs: Additional generation parameters

        Returns:
            Generated text response
        """
        if provider not in self.providers:
            raise ValueError(f"Provider '{provider}' not configured")

        logger.info(f"Generating with {provider}: {prompt[:50]}...")
        return await self.providers[provider].generate(prompt, **kwargs)

    async def generate_structured(
        self,
        prompt: str,
        schema: Dict,
        provider: str = "openai",
        **kwargs
    ) -> Dict:
        """
        Generate structured response using specified provider

        Args:
            prompt: The prompt to send to the model
            schema: JSON schema for structured output
            provider: Provider name
            **kwargs: Additional generation parameters

        Returns:
            Structured dictionary response
        """
        if provider not in self.providers:
            raise ValueError(f"Provider '{provider}' not configured")

        logger.info(f"Generating structured output with {provider}")
        return await self.providers[provider].generate_structured(prompt, schema, **kwargs)

    async def generate_multi_model(
        self,
        prompt: str,
        providers: List[str],
        **kwargs
    ) -> Dict[str, str]:
        """
        Generate responses from multiple models for comparison

        Args:
            prompt: The prompt to send to models
            providers: List of provider names
            **kwargs: Additional generation parameters

        Returns:
            Dictionary mapping provider names to responses
        """
        results = {}

        for provider in providers:
            if provider in self.providers:
                try:
                    results[provider] = await self.generate(prompt, provider, **kwargs)
                except Exception as e:
                    logger.error(f"Error generating with {provider}: {str(e)}")
                    results[provider] = f"Error: {str(e)}"

        return results


# Global model router instance
model_router = ModelRouter()

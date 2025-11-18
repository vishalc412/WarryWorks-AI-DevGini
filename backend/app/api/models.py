"""
AI Models API endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import logging

from app.services.model_router import model_router

logger = logging.getLogger(__name__)
router = APIRouter()


class ModelConfig(BaseModel):
    """Model configuration"""
    provider: str
    api_key: str
    model_name: str = None


class TestPromptRequest(BaseModel):
    """Test prompt request"""
    provider: str
    prompt: str


@router.post("/configure")
async def configure_model(config: ModelConfig):
    """
    Configure an AI model provider

    Args:
        config: Model configuration

    Returns:
        Success message
    """
    logger.info(f"Configuring model provider: {config.provider}")

    try:
        if config.provider.lower() == "openai":
            model_router.configure_openai(
                api_key=config.api_key,
                model=config.model_name or "gpt-4-turbo-preview"
            )
        elif config.provider.lower() == "anthropic":
            model_router.configure_anthropic(
                api_key=config.api_key,
                model=config.model_name or "claude-3-opus-20240229"
            )
        elif config.provider.lower() == "gemini":
            model_router.configure_gemini(
                api_key=config.api_key,
                model=config.model_name or "gemini-pro"
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported provider: {config.provider}"
            )

        return {
            "status": "success",
            "message": f"Provider {config.provider} configured successfully"
        }

    except Exception as e:
        logger.error(f"Error configuring model: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test")
async def test_model(request: TestPromptRequest):
    """
    Test a model provider with a prompt

    Args:
        request: Test request

    Returns:
        Model response
    """
    logger.info(f"Testing model provider: {request.provider}")

    try:
        response = await model_router.generate(
            prompt=request.prompt,
            provider=request.provider
        )

        return {
            "status": "success",
            "provider": request.provider,
            "response": response
        }

    except Exception as e:
        logger.error(f"Error testing model: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/providers")
async def list_providers():
    """List all available model providers"""
    return {
        "providers": [
            {
                "name": "openai",
                "models": [
                    "gpt-4-turbo-preview",
                    "gpt-4",
                    "gpt-3.5-turbo"
                ],
                "configured": "openai" in model_router.providers
            },
            {
                "name": "anthropic",
                "models": [
                    "claude-3-opus-20240229",
                    "claude-3-sonnet-20240229",
                    "claude-3-haiku-20240307"
                ],
                "configured": "anthropic" in model_router.providers
            },
            {
                "name": "gemini",
                "models": [
                    "gemini-pro",
                    "gemini-pro-vision"
                ],
                "configured": "gemini" in model_router.providers
            }
        ]
    }


@router.get("/status")
async def get_models_status():
    """Get status of configured models"""
    return {
        "configured_providers": list(model_router.providers.keys()),
        "total_providers": len(model_router.providers)
    }

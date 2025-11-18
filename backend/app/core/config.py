"""
Configuration settings for Lovable-AI Builder Platform
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "Lovable-AI Builder Platform"
    DEBUG: bool = True
    VERSION: str = "1.0.0"

    # API
    API_V1_PREFIX: str = "/api/v1"

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000"
    ]

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/lovable_ai"
    DB_ECHO: bool = False

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # AWS S3 (for artifact storage)
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = "lovable-ai-artifacts"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # AI Model Configuration
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    DEFAULT_MODEL_PROVIDER: str = "openai"
    DEFAULT_MODEL_NAME: str = "gpt-4-turbo-preview"

    # Generation Settings
    MAX_GENERATION_TIME: int = 300  # 5 minutes
    MAX_INTERVIEW_QUESTIONS: int = 25
    MIN_INTERVIEW_QUESTIONS: int = 10

    # Code Generation Templates
    TEMPLATE_DIR: str = "app/templates"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

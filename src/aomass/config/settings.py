"""Configuration management for AOMaaS."""
import os
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field


from pydantic import BaseModel
class Settings(BaseModel):
    """Application settings."""
    
    # Application
    app_name: str = Field(default="AOMaaS", env="APP_NAME")
    app_version: str = Field(default="0.1.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Database
    database_url: str = Field(
        default="postgresql://aomass:aomass@localhost:5432/aomass",
        env="DATABASE_URL"
    )
    
    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    
    # Qdrant
    qdrant_url: str = Field(default="http://localhost:6333", env="QDRANT_URL")
    
    # MinIO
    minio_endpoint: str = Field(default="localhost:9000", env="MINIO_ENDPOINT")
    minio_access_key: str = Field(default="aomass", env="MINIO_ACCESS_KEY")
    minio_secret_key: str = Field(default="aomass123", env="MINIO_SECRET_KEY")
    minio_secure: bool = Field(default=False, env="MINIO_SECURE")
    
    # GitHub
    github_token: Optional[str] = Field(default=None, env="GITHUB_TOKEN")
    github_app_id: Optional[str] = Field(default=None, env="GITHUB_APP_ID")
    github_private_key_path: Optional[str] = Field(
        default=None, env="GITHUB_PRIVATE_KEY_PATH"
    )
    
    # AI Services
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    
    # Security
    secret_key: str = Field(default="dev-secret-key", env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Worker
    celery_broker_url: str = Field(default="redis://localhost:6379/0", env="CELERY_BROKER_URL")
    celery_result_backend: str = Field(default="redis://localhost:6379/0", env="CELERY_RESULT_BACKEND")
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()

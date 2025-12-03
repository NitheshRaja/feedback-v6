"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union
import os
import json


class Settings(BaseSettings):
    """Application settings"""
    
    # Project
    PROJECT_NAME: str = "L1 Feedback Sentiment Analysis"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "sqlite:///./feedback.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS - accepts JSON array, comma-separated string, or "*"
    CORS_ORIGINS: Union[List[str], str] = "http://localhost:3000,http://localhost:5173,http://localhost:8080"
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "./uploads"
    
    # ML Model
    SENTIMENT_MODEL: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    DEVICE: str = "cpu"  # or "cuda" for GPU
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS_ORIGINS from various formats"""
        if not v:
            return ["*"]
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            v = v.strip()
            # Handle "*" directly
            if v == "*":
                return ["*"]
            # Try JSON parsing first
            if v.startswith('['):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            # Fall back to comma-separated
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        return ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Project
    PROJECT_NAME: str = "L1 Feedback Sentiment Analysis"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "1.0.0"
    
    # Database
    # Default to SQLite for development (no PostgreSQL required)
    # To use PostgreSQL, set DATABASE_URL environment variable
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./feedback.db"  # SQLite - works without database server
    )
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Security
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://localhost:5173,http://localhost:8080"
    ).split(",") if isinstance(os.getenv("CORS_ORIGINS", ""), str) else [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
    ]
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "./uploads"
    
    # ML Model
    SENTIMENT_MODEL: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    DEVICE: str = "cpu"  # or "cuda" for GPU
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


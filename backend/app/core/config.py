"""
Core configuration for UtopiaHire API
Handles environment variables and application settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "UtopiaHire API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-Powered Career Platform for MENA & Sub-Saharan Africa"
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "your-secret-key-change-in-production-use-openssl-rand-hex-32"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # Database Settings (PostgreSQL)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://utopia_user:utopia_secure_2025@localhost/utopiahire"
    )
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 10
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10 MB
    UPLOAD_DIR: str = "/tmp/utopiahire_uploads"
    
    # Define allowed extensions as property to avoid env parsing issues
    @property
    def allowed_extensions(self):
        return [".pdf", ".docx", ".doc"]
    
    # External API Keys (from existing .env)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    SERPAPI_KEY: Optional[str] = os.getenv("SERPAPI_API_KEY")
    JSEARCH_API_KEY: Optional[str] = os.getenv("JSEARCH_API_KEY")
    GITHUB_TOKEN: Optional[str] = os.getenv("GITHUB_TOKEN")
    STACKOVERFLOW_KEY: Optional[str] = os.getenv("STACKOVERFLOW_KEY")
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_AUTH: str = "5/minute"
    RATE_LIMIT_RESUME: str = "10/hour"
    RATE_LIMIT_JOBS: str = "5/hour"
    RATE_LIMIT_INTERVIEW: str = "20/hour"
    RATE_LIMIT_FOOTPRINT: str = "10/hour"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore"  # Ignore extra fields from .env
    )


# Global settings instance
settings = Settings()

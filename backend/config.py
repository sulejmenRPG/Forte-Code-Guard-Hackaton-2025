"""
Configuration management using Pydantic Settings
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # GitLab Configuration
    GITLAB_URL: str = "https://gitlab.com"
    GITLAB_TOKEN: str = "test_token"  # Required in production
    
    # LLM Provider Configuration
    LLM_PROVIDER: str = "gemini"  # openai, gemini, claude
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Webhook Configuration
    WEBHOOK_SECRET: str = "default_secret"  # Required in production
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./code_review.db"  # Fallback to SQLite
    
    # Application Settings
    APP_HOST: str = "0.0.0.0"
    PORT: int = 8000  # Railway will override this
    DEBUG: bool = False
    
    # Analysis Settings
    MAX_CODE_LENGTH: int = 50000
    ANALYSIS_TIMEOUT: int = 300  # seconds
    
    # Review Settings
    MIN_SCORE_FOR_APPROVAL: float = 7.0
    AUTO_LABEL_MR: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()

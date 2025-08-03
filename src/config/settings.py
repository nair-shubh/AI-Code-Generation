"""
Configuration settings for the Intelligent Code Automation Engine
"""

import os
from typing import Optional

class Settings:
    """Application settings"""
    
    # API Keys (from environment variables)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    E2B_API_KEY: Optional[str] = os.getenv("E2B_API_KEY")
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Application settings
    APP_NAME: str = "Intelligent Code Automation Engine"
    APP_VERSION: str = "2.0.0"
    APP_DESCRIPTION: str = "Advanced AI-powered code generation with E2B cloud execution"
    
    # Session settings
    SESSION_TIMEOUT: int = int(os.getenv("SESSION_TIMEOUT", "3600"))  # 1 hour
    
    # GitHub settings
    GITHUB_API_BASE_URL: str = "https://api.github.com"
    
    # E2B settings
    E2B_SESSION_TIMEOUT: int = int(os.getenv("E2B_SESSION_TIMEOUT", "300"))  # 5 minutes
    
    # OpenAI settings
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "4000"))
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

# Global settings instance
settings = Settings() 
"""Configuration settings for the Contax Brain.tech portal."""
from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # OpenAI Configuration
    openai_api_key: str = ""
    
    # Application Configuration
    app_name: str = "Contax Brain.tech"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    model_config = ConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()

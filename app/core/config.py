from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path

# Get the project root directory (two levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    # Database settings
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str 
    
    # Application settings
    DEBUG: bool = False
    SECRET_KEY: Optional[str] = None

    model_config = {
        "env_file": PROJECT_ROOT / ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True
    }


settings = Settings()
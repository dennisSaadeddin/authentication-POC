import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

# Load .env file explicitly
load_dotenv()

class Settings(BaseSettings):
    # JWT Settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database Settings
    DATABASE_URL: str = "sqlite+aiosqlite:///./auth.db"

    # Optional server settings
    HOST: Optional[str] = "0.0.0.0"
    PORT: Optional[int] = 8000
    DEBUG: Optional[bool] = True

    # This allows extra environment variables to be read
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra='allow'
    )

    @classmethod
    def validate_settings(cls):
        # Explicit validation and logging
        settings = cls()
        print("Configuration Loaded:")
        for field, value in settings.model_dump().items():
            print(f"{field}: {value}")
        return settings

def get_settings():
    try:
        return Settings.validate_settings()
    except Exception as e:
        print(f"Configuration Error: {e}")
        raise 
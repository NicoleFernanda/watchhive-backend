"""
Settings module for the application. Normally, these settings would be loaded from environment
variables or a .env file.
"""

from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

    DATABASE_URL: str = None
    ALLOWED_ORIGINS: str = ""

settings = Settings()

"""
Settings module for the application. Normally, these settings would be loaded from environment
variables or a .env file.
"""

from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    DATABASE_URL: str = None
    ALLOWED_ORIGINS: str = ""

    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> List[str]:
        """
        Parses the ALLOWED_ORIGINS string into a list of origins.
        If the string is empty, returns an empty list.
        """
        return v.split(",") if v else []

    class Config:
        """
        Configurations for the settings class.
        """
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()

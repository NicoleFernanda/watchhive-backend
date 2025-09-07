"""
Settings module for the application. Normally, these settings would be loaded from environment
variables or a .env file.
"""


from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    DATABASE_URL: str
    ALLOWED_ORIGINS: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str

    def get_allowed_origins(self) -> List[str]:
        """
        Transforma a string vinda do .env em lista de URLs.
        """
        if not self.ALLOWED_ORIGINS:
            return []
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


settings = Settings()

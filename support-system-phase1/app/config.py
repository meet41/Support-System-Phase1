from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application configuration from .env"""
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "support_system_db"
    SECRET_KEY: str = "your-secret-key-change-in-production-must-be-32-chars-minimum"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10
    COOKIE_NAME: str = "access_token"
    COOKIE_DOMAIN: Optional[str] = None
    COOKIE_PATH: str = "/"
    COOKIE_SECURE: bool = False
    COOKIE_HTTPONLY: bool = True
    COOKIE_SAMESITE: str = "lax"
    SESSION_SECRET_KEY: str = "session-secret-key-very-secret"
    SESSION_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

settings = Settings()
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application configuration from .env"""
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "support_system_db"
    # Legacy shared secret – kept for backward compatibility only.
    # Set ACCESS_TOKEN_SECRET and REFRESH_TOKEN_SECRET in your .env for
    # proper defence-in-depth (Issue #4).  Never deploy with the placeholder
    # values below in production (Issue #7).
    SECRET_KEY: str = "your-secret-key-change-in-production-must-be-32-chars-minimum"
    # Separate signing secrets for each token type (Issue #4, #7).
    # Override both via environment variables / .env in every environment.
    ACCESS_TOKEN_SECRET: str = "access-token-secret-change-in-production-must-be-32-chars"
    REFRESH_TOKEN_SECRET: str = "refresh-token-secret-change-in-production-must-be-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10
    COOKIE_NAME: str = "access_token"
    REFRESH_COOKIE_NAME: str = "refresh_token"
    COOKIE_DOMAIN: Optional[str] = None
    COOKIE_PATH: str = "/"
    # Set COOKIE_SECURE=True in production (HTTPS only) – Issue #8.
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
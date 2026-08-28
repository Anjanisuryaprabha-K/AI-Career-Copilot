"""
Centralized application configuration.

Uses pydantic-settings BaseSettings for automatic environment variable loading
with validation. Fallback is the plain class pattern if pydantic-settings is
not installed (e.g. during bare local development without the full requirements).

All settings are accessible via: `from app.config import settings`
"""
from typing import Optional

try:
    from pydantic_settings import BaseSettings

    class Settings(BaseSettings):
        # MongoDB
        MONGODB_URL: str = "mongodb://localhost:27017"
        MONGODB_DATABASE: str = "placement_db"
        USE_IN_MEMORY_DB: bool = False

        # JWT / Auth
        JWT_SECRET: str = "career-mentor-super-secret-jwt-key-2026-placement-platform"
        JWT_ALGORITHM: str = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

        # External APIs
        GOOGLE_API_KEY: Optional[str] = ""
        GOOGLE_CSE_ID: Optional[str] = ""
        AI_PROVIDER: str = "google_openai_native"
        AI_API_KEY: Optional[str] = ""

        # Speech / TTS
        SPEECH_TO_TEXT_PROVIDER: str = "whisper_browser_fallback"
        SPEECH_TO_TEXT_API_KEY: Optional[str] = ""
        TEXT_TO_SPEECH_PROVIDER: str = "native_web_speech"
        TEXT_TO_SPEECH_API_KEY: Optional[str] = ""

        # CORS
        FRONTEND_URL: str = "http://localhost:3000"

        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"
            case_sensitive = True
            extra = "ignore"

except ImportError:
    # Fallback: plain class with os.getenv (same behavior as original)
    import os

    class Settings:  # type: ignore[no-redef]
        MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        MONGODB_DATABASE: str = os.getenv("MONGODB_DATABASE", "placement_db")
        USE_IN_MEMORY_DB: bool = os.getenv("USE_IN_MEMORY_DB", "false").lower() in ("true", "1", "yes")
        JWT_SECRET: str = os.getenv("JWT_SECRET", "career-mentor-super-secret-jwt-key-2026-placement-platform")
        JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
        ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
        GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY", "")
        GOOGLE_CSE_ID: Optional[str] = os.getenv("GOOGLE_CSE_ID", "")
        FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
        AI_PROVIDER: str = os.getenv("AI_PROVIDER", "google_openai_native")
        AI_API_KEY: Optional[str] = os.getenv("AI_API_KEY", "")
        SPEECH_TO_TEXT_PROVIDER: str = os.getenv("SPEECH_TO_TEXT_PROVIDER", "whisper_browser_fallback")
        SPEECH_TO_TEXT_API_KEY: Optional[str] = os.getenv("SPEECH_TO_TEXT_API_KEY", "")
        TEXT_TO_SPEECH_PROVIDER: str = os.getenv("TEXT_TO_SPEECH_PROVIDER", "native_web_speech")
        TEXT_TO_SPEECH_API_KEY: Optional[str] = os.getenv("TEXT_TO_SPEECH_API_KEY", "")


settings = Settings()

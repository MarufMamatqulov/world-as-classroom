import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "World as a Classroom"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./world_classroom.db")
    
    # JWT Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "world-as-a-classroom-super-secret-key-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Gemini AI
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Security & Wordbox Integration
    ALLOWED_ORIGINS_RAW: str = os.getenv(
        "ALLOWED_ORIGINS",
        "https://wordbox.uz,https://www.wordbox.uz,http://wordbox.uz,http://www.wordbox.uz,https://ai.wordbox.uz,https://aimarafon.uz,https://api.aimarafon.uz,http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173"
    )
    WORDBOX_API_SECRET: str = os.getenv("WORDBOX_API_SECRET", "wordbox-classroom-secure-2026")

    @property
    def CORS_ORIGINS(self) -> List[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS_RAW.split(",") if o.strip()]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

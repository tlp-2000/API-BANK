
from pydantic_settings import BaseSettings
class Settings(BaseSettings): # type: ignore
    PROJECT_NAME: str = "Bank API"
    SECRET_KEY: str = "replace-with-a-secure-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 dia
    DATABASE_URL: str = "sqlite+aiosqlite:///./bank.db"

    class Config:
        env_file = ".env"

settings = Settings()
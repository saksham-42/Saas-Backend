from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: Optional[str] = None
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


settings = Settings()

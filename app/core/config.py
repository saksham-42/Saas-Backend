from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: Optional[str] = None
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRE_MINUTES: int

    model_config = ConfigDict(extra="ignore")

settings = Settings()   

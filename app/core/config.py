from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL : str
    TEST_DATABASE_URL : str
    SECRET_KEY : str
    ALGORITHM : str
    EXPIRE_MINUTES : int

    class Config:
        env_file = ".env"

settings = Settings()
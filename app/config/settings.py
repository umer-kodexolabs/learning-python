from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    database_client: str
    database_name: str

    class Config:
        env_file = ".env"


# Instantiate settings
settings = Settings()

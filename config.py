import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    root_directory: str = os.path.dirname(os.path.abspath(__file__))

settings = Settings()
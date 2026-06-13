from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_key: str
    app_name: str
    
    class Config:
        env_file = ".env"   
        env_file_encoding = "utf-8"

settings = Settings()
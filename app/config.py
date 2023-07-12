from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    
    CLIENT_ORIGIN: str

    class Config:
        env_file = '/.env-docker'



settings = Settings()

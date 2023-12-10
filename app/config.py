from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str

    CLIENT_ORIGIN: str

    MAILSAC_KEY: str
    MAILSAC_BASE_URL: str
    MYOSOTIS_PRIVATE_DOMAIN: str

    class Config:
        env_file = "docker/development/env/.env-docker"


settings = Settings()

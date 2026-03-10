from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/shortener"
    REDIS_URL: str = "redis://redis:6379"

    JWT_SECRET: str = "SECRET"

settings = Settings()

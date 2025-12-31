from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    QUEUE_BACKEND: str = "in_memory"
    SQS_QUEUE_URL: str | None = None

    class Config:
        env_file = ".env"
        extra = "forbid" 


settings = Settings()
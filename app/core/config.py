from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str

    aws_region: str
    sqs_queue_url: str
    max_job_retries: int = 3

    class Config:
        env_file = ".env"


settings = Settings()

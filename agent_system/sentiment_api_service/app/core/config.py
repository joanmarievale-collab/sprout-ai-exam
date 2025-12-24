from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_name: str = "Sentiment Analysis API"
    debug: bool = False
    api_prefix: str = "/sentiment"
    version: str = "1.0.0"
    description: str = "RoBERTa-based Sentiment Analysis Service"

    # Model
    model_name: str = "cardiffnlp/twitter-roberta-base-sentiment"
    device: str = "auto"  # auto | cpu | cuda
    max_tokens: int = 512

    # Label mapping
    label_negative: str = "negative"
    label_neutral: str = "neutral"
    label_positive: str = "positive"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

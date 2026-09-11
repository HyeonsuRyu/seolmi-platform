from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "dev"
    openai_api_key: str = ""

    # 폴더 구조상 자리만 잡아둔 값 — DB/인증 도메인 구현 전까지는 사용되지 않는다.
    database_url: str = "sqlite:///./chowon.db"
    jwt_secret: str = "change-me"


@lru_cache
def get_settings() -> Settings:
    return Settings()

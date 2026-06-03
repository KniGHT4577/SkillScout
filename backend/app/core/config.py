from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, BeforeValidator, validator
from typing import Annotated, Any

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, (list, str)):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    # Fallback to sqlite if no DATABASE_URL is provided in env
    DATABASE_URL: str = "sqlite+aiosqlite:///./skillscout.db"
    SECRET_KEY: str = "supersecretkeythatyoushouldchangeinproduction"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440 # 24 hours
    TAVILY_API_KEY: str | None = None
    OPENROUTER_API_KEY: str | None = None
    CRON_SECRET_TOKEN: str

    BACKEND_CORS_ORIGINS: Annotated[list[AnyHttpUrl] | str, BeforeValidator(parse_cors)] | list[str] = ["http://localhost:5173", "http://localhost:3000", "http://localhost:8000"]

    class Config:
        env_file = ".env"

settings = Settings()

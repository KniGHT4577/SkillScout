from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Fallback to sqlite if no DATABASE_URL is provided in env
    DATABASE_URL: str = "sqlite+aiosqlite:///./skillscout.db"
    SECRET_KEY: str = "supersecretkeythatyoushouldchangeinproduction"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440 # 24 hours
    TAVILY_API_KEY: str | None = None
    OPENROUTER_API_KEY: str | None = None
    CRON_SECRET_TOKEN: str

    class Config:
        env_file = ".env"

settings = Settings()

import os
from unittest.mock import patch
from app.core.config import Settings

def test_cors_origins_secure_by_default():
    with patch.dict(os.environ, {"SECRET_KEY": "test", "CRON_SECRET_TOKEN": "test"}):
        settings = Settings()
        assert settings.BACKEND_CORS_ORIGINS == []

def test_cors_origins_parsing():
    with patch.dict(os.environ, {
        "SECRET_KEY": "test",
        "CRON_SECRET_TOKEN": "test",
        "BACKEND_CORS_ORIGINS": "https://example.com,http://localhost:5173"
    }):
        settings = Settings()
        origins = [str(origin).rstrip("/") for origin in settings.BACKEND_CORS_ORIGINS]
        assert "https://example.com" in origins
        assert "http://localhost:5173" in origins

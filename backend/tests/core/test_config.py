import pytest
from pydantic import ValidationError
import os
import importlib
import sys

def test_settings_require_secrets(monkeypatch):
    # Temporarily remove any existing environment variables so they aren't loaded
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("CRON_SECRET_TOKEN", raising=False)

    # In case app.core.config was already imported in another test,
    # we need to remove it to force a re-evaluation
    if "app.core.config" in sys.modules:
        del sys.modules["app.core.config"]

    with pytest.raises(ValidationError) as exc_info:
        import app.core.config

    errors = exc_info.value.errors()
    missing_fields = {error["loc"][0] for error in errors if error["type"] == "missing"}

    assert "SECRET_KEY" in missing_fields
    assert "CRON_SECRET_TOKEN" in missing_fields

    # Restore module state by putting standard values back and reloading
    monkeypatch.setenv("SECRET_KEY", "test_secret_key")
    monkeypatch.setenv("CRON_SECRET_TOKEN", "test_cron_secret")

    # Needs to be reloaded so other tests don't fail when importing config
    if "app.core.config" in sys.modules:
        del sys.modules["app.core.config"]
    import app.core.config

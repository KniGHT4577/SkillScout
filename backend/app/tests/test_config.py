import unittest
import os
import sys

# Import ValidationError from pydantic, not pydantic_core, usually more reliable
from pydantic import ValidationError

class TestConfig(unittest.TestCase):
    def test_settings_missing_keys(self):
        original_secret = os.environ.get("SECRET_KEY")
        original_cron = os.environ.get("CRON_SECRET_TOKEN")

        if "SECRET_KEY" in os.environ:
            del os.environ["SECRET_KEY"]
        if "CRON_SECRET_TOKEN" in os.environ:
            del os.environ["CRON_SECRET_TOKEN"]

        try:
            # We import Settings specifically so we don't trigger the instantiated settings object
            # if we can avoid it. Oh, config.py instantiates it at the bottom.
            from app.core.config import Settings
            with self.assertRaises(ValidationError):
                Settings()
        except ValidationError:
            # If the module import itself throws ValidationError because of settings = Settings() at the end,
            # that's also valid for this test
            pass
        finally:
            if original_secret is not None:
                os.environ["SECRET_KEY"] = original_secret
            if original_cron is not None:
                os.environ["CRON_SECRET_TOKEN"] = original_cron

    def test_settings_with_keys(self):
        original_secret = os.environ.get("SECRET_KEY")
        original_cron = os.environ.get("CRON_SECRET_TOKEN")

        os.environ["SECRET_KEY"] = "testsecret"
        os.environ["CRON_SECRET_TOKEN"] = "testcron"

        try:
            from app.core.config import Settings
            settings = Settings()
            self.assertEqual(settings.SECRET_KEY, "testsecret")
            self.assertEqual(settings.CRON_SECRET_TOKEN, "testcron")
        finally:
            if original_secret is not None:
                os.environ["SECRET_KEY"] = original_secret
            else:
                del os.environ["SECRET_KEY"]

            if original_cron is not None:
                os.environ["CRON_SECRET_TOKEN"] = original_cron
            else:
                del os.environ["CRON_SECRET_TOKEN"]

if __name__ == "__main__":
    unittest.main()

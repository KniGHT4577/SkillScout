import pytest
from app.services.scraper import is_safe_url, scrape_url
import socket

@pytest.mark.asyncio
async def test_is_safe_url_safe():
    # Test valid, public URL
    # Using a reliable domain that should always resolve correctly
    assert await is_safe_url("https://www.google.com") == True
    assert await is_safe_url("http://example.com") == True

@pytest.mark.asyncio
async def test_is_safe_url_unsafe_local():
    assert await is_safe_url("http://localhost") == False
    assert await is_safe_url("http://127.0.0.1") == False
    assert await is_safe_url("http://127.0.0.1:8000/api") == False

@pytest.mark.asyncio
async def test_is_safe_url_unsafe_private():
    assert await is_safe_url("http://10.0.0.1") == False
    assert await is_safe_url("http://192.168.1.1") == False
    assert await is_safe_url("http://172.16.0.1") == False

@pytest.mark.asyncio
async def test_is_safe_url_unsafe_cloud():
    # AWS metadata endpoint
    assert await is_safe_url("http://169.254.169.254/latest/meta-data/") == False

@pytest.mark.asyncio
async def test_is_safe_url_unsafe_scheme():
    assert await is_safe_url("file:///etc/passwd") == False
    assert await is_safe_url("ftp://example.com") == False

@pytest.mark.asyncio
async def test_scrape_url_blocked_ssrf(mocker):
    # Test that scrape_url actually uses is_safe_url and returns "" when blocked
    # We mock is_safe_url to avoid actual network calls in this test
    mocker.patch("app.services.scraper.is_safe_url", return_value=False)

    result = await scrape_url("http://localhost:8000/sensitive")
    assert result == ""

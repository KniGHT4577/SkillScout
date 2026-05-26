import pytest
import logging
from unittest.mock import AsyncMock
from app.services.scraper import scrape_url

@pytest.mark.asyncio
async def test_scrape_url_exception(mocker, caplog):
    # Mock async_playwright context manager and its launch method
    # Since async_playwright() is an async context manager, we need a mock that handles __aenter__ and __aexit__

    # We want to patch the actual async_playwright function in app.services.scraper
    mock_async_playwright = mocker.patch("app.services.scraper.async_playwright")

    # Set up the mock context manager
    mock_context_manager = AsyncMock()
    # The __aenter__ method returns the playwright object (p in our code)
    mock_p = AsyncMock()
    # Setup chromium to raise an exception when launched
    mock_p.chromium.launch.side_effect = Exception("Mocked Playwright Error")
    mock_context_manager.__aenter__.return_value = mock_p

    mock_async_playwright.return_value = mock_context_manager

    url = "http://example.com"

    with caplog.at_level(logging.ERROR):
        result = await scrape_url(url)

    # Verify the result is an empty string
    assert result == ""

    # Verify that the exception was caught and logged
    assert f"Error scraping {url}: Mocked Playwright Error" in caplog.text

@pytest.mark.asyncio
async def test_scrape_url_success(mocker):
    # Setup the mock async_playwright
    mock_async_playwright = mocker.patch("app.services.scraper.async_playwright")

    mock_context_manager = AsyncMock()
    mock_p = AsyncMock()

    mock_browser = AsyncMock()
    mock_page = AsyncMock()

    mock_p.chromium.launch.return_value = mock_browser
    mock_browser.new_page.return_value = mock_page

    # Set up some dummy HTML to return
    dummy_html = """
    <html>
        <body>
            <script>alert('test')</script>
            <style>.hidden { display: none; }</style>
            <nav>Menu</nav>
            <main>
                <h1>Test Page</h1>
                <p>This is a test paragraph.</p>
            </main>
            <footer>Copyright 2023</footer>
        </body>
    </html>
    """
    mock_page.content.return_value = dummy_html

    mock_context_manager.__aenter__.return_value = mock_p
    mock_async_playwright.return_value = mock_context_manager

    url = "http://example.com"

    result = await scrape_url(url)

    # Verify the script, style, nav, and footer were removed
    # and only the text content remains
    assert "alert" not in result
    assert "hidden" not in result
    assert "Menu" not in result
    assert "Copyright" not in result
    assert "Test Page This is a test paragraph." in result

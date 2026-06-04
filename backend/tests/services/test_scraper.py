import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.scraper import scrape_url

@pytest.mark.asyncio
async def test_scrape_url_success():
    # Arrange
    mock_html = """
    <html>
        <body>
            <nav>Navigation</nav>
            <h1>Main Title</h1>
            <p>Some useful content.</p>
            <script>alert('test')</script>
            <style>body { color: red; }</style>
            <footer>Footer Info</footer>
        </body>
    </html>
    """

    mock_page = AsyncMock()
    mock_page.goto.return_value = None
    mock_page.content.return_value = mock_html

    mock_browser = AsyncMock()
    mock_browser.new_page.return_value = mock_page
    mock_browser.close.return_value = None

    mock_chromium = AsyncMock()
    mock_chromium.launch.return_value = mock_browser

    mock_p = MagicMock()
    mock_p.chromium = mock_chromium

    mock_async_playwright_cm = AsyncMock()
    mock_async_playwright_cm.__aenter__.return_value = mock_p
    mock_async_playwright_cm.__aexit__.return_value = None

    with patch("app.services.scraper.async_playwright", return_value=mock_async_playwright_cm) as mock_playwright:
        # Act
        result = await scrape_url("http://example.com")

        # Assert
        assert result == "Main Title Some useful content."
        mock_playwright.assert_called_once()
        mock_chromium.launch.assert_called_once_with(headless=True)
        mock_browser.new_page.assert_called_once()
        mock_page.goto.assert_called_once_with("http://example.com", wait_until="networkidle", timeout=15000)
        mock_page.content.assert_called_once()
        mock_browser.close.assert_called_once()

@pytest.mark.asyncio
async def test_scrape_url_exception():
    # Arrange
    mock_async_playwright_cm = AsyncMock()
    mock_async_playwright_cm.__aenter__.side_effect = Exception("Browser failed to launch")
    mock_async_playwright_cm.__aexit__.return_value = None

    with patch("app.services.scraper.async_playwright", return_value=mock_async_playwright_cm):
        with patch("app.services.scraper.logger") as mock_logger:
            # Act
            result = await scrape_url("http://example.com")

            # Assert
            assert result == ""
            mock_logger.error.assert_called_once()
            assert "Error scraping http://example.com: Browser failed to launch" in mock_logger.error.call_args[0][0]

@pytest.mark.asyncio
async def test_scrape_url_truncation():
    # Arrange
    long_text = "A" * 15000
    mock_html = f"<html><body><p>{long_text}</p></body></html>"

    mock_page = AsyncMock()
    mock_page.goto.return_value = None
    mock_page.content.return_value = mock_html

    mock_browser = AsyncMock()
    mock_browser.new_page.return_value = mock_page
    mock_browser.close.return_value = None

    mock_chromium = AsyncMock()
    mock_chromium.launch.return_value = mock_browser

    mock_p = MagicMock()
    mock_p.chromium = mock_chromium

    mock_async_playwright_cm = AsyncMock()
    mock_async_playwright_cm.__aenter__.return_value = mock_p
    mock_async_playwright_cm.__aexit__.return_value = None

    with patch("app.services.scraper.async_playwright", return_value=mock_async_playwright_cm):
        # Act
        result = await scrape_url("http://example.com")

        # Assert
        assert len(result) == 10000
        assert result == "A" * 10000

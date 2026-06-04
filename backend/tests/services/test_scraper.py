import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.scraper import scrape_url

@pytest.fixture
def mock_playwright():
    with patch('app.services.scraper.async_playwright') as mock:
        yield mock

@pytest.mark.asyncio
async def test_scrape_url_happy_path(mock_playwright):
    # Setup mock structure
    mock_p = AsyncMock()
    mock_browser = AsyncMock()
    mock_page = AsyncMock()

    mock_playwright.return_value.__aenter__.return_value = mock_p
    mock_p.chromium.launch.return_value = mock_browser
    mock_browser.new_page.return_value = mock_page

    # Mock HTML content with elements that should be removed
    mock_html = """
    <html>
        <head>
            <script>console.log("ignore me")</script>
            <style>.hidden { display: none; }</style>
        </head>
        <body>
            <nav>Menu</nav>
            <main>
                <h1>Test Page</h1>
                <p>This is a <b>test</b>.</p>
            </main>
            <footer>Copyright</footer>
        </body>
    </html>
    """
    mock_page.content.return_value = mock_html

    url = "http://example.com"
    result = await scrape_url(url)

    # Assertions on API calls
    mock_p.chromium.launch.assert_called_once_with(headless=True)
    mock_browser.new_page.assert_called_once()
    mock_page.goto.assert_called_once_with(url, wait_until="networkidle", timeout=15000)
    mock_page.content.assert_called_once()
    mock_browser.close.assert_called_once()

    # Assertions on result
    # bs4 get_text with separator=' ' outputs "This is a test ." for <p>This is a <b>test</b>.</p>
    assert "ignore me" not in result
    assert ".hidden" not in result
    assert "Menu" not in result
    assert "Copyright" not in result
    assert "Test Page" in result
    assert "This is a test" in result

@pytest.mark.asyncio
async def test_scrape_url_truncation(mock_playwright):
    # Setup mock structure
    mock_p = AsyncMock()
    mock_browser = AsyncMock()
    mock_page = AsyncMock()

    mock_playwright.return_value.__aenter__.return_value = mock_p
    mock_p.chromium.launch.return_value = mock_browser
    mock_browser.new_page.return_value = mock_page

    # Create large HTML
    large_text = "A" * 15000
    mock_html = f"<html><body>{large_text}</body></html>"
    mock_page.content.return_value = mock_html

    result = await scrape_url("http://example.com")

    # Should truncate at 10000 chars
    assert len(result) == 10000

@pytest.mark.asyncio
async def test_scrape_url_exception(mock_playwright, caplog):
    # Setup mock structure to raise exception
    mock_p = AsyncMock()
    mock_playwright.return_value.__aenter__.return_value = mock_p

    # Raise exception when launching browser
    mock_p.chromium.launch.side_effect = Exception("Playwright failed")

    url = "http://example.com"
    result = await scrape_url(url)

    # Should return empty string on error
    assert result == ""

    # Should log the error
    assert f"Error scraping {url}: Playwright failed" in caplog.text

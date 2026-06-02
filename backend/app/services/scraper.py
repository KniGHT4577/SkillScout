from playwright.async_api import async_playwright, Browser, Playwright
from bs4 import BeautifulSoup
import logging
import asyncio

logger = logging.getLogger(__name__)

_playwright: Playwright | None = None
_browser: Browser | None = None
_lock = asyncio.Lock()

async def get_browser() -> Browser:
    global _playwright, _browser
    if _browser is None:
        async with _lock:
            if _browser is None:
                _playwright = await async_playwright().start()
                _browser = await _playwright.chromium.launch(headless=True)
    return _browser

async def close_browser():
    global _playwright, _browser
    async with _lock:
        if _browser:
            await _browser.close()
            _browser = None
        if _playwright:
            await _playwright.stop()
            _playwright = None

async def scrape_url(url: str) -> str:
    """Scrapes the visible text from a URL using Playwright."""
    try:
        browser = await get_browser()
        page = await browser.new_page()

        try:
            # Wait for content to load, timeout after 15 seconds
            await page.goto(url, wait_until="networkidle", timeout=15000)
            
            # Get HTML
            html = await page.content()
            
            # Use BeautifulSoup to extract text cleanly
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove scripts and styles
            for script in soup(["script", "style", "nav", "footer"]):
                script.extract()
                
            text = soup.get_text(separator=' ', strip=True)
            
            # Truncate to reasonable length for AI processing
            return text[:10000] 
        finally:
            await page.close()

    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
        return ""

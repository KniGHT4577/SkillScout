from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

async def scrape_url(url: str) -> str:
    """Scrapes the visible text from a URL using Playwright."""
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Wait for content to load, timeout after 15 seconds
            await page.goto(url, wait_until="networkidle", timeout=15000)
            
            # Get HTML
            html = await page.content()
            await browser.close()
            
            # Use BeautifulSoup to extract text cleanly
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove scripts and styles
            for script in soup(["script", "style", "nav", "footer"]):
                script.extract()
                
            text = soup.get_text(separator=' ', strip=True)
            
            # Truncate to reasonable length for AI processing
            return text[:10000] 
    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
        return ""

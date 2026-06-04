from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import logging
import asyncio
import socket
import ipaddress
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

async def is_safe_url(url: str) -> bool:
    """Validates the scheme, hostname, and resolves IPs against private address blocks to mitigate SSRF."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False

        hostname = parsed.hostname
        if not hostname:
            return False

        loop = asyncio.get_running_loop()
        try:
            addr_info = await loop.getaddrinfo(hostname, None)
        except socket.gaierror:
            return False

        for info in addr_info:
            ip_str = info[4][0]
            ip = ipaddress.ip_address(ip_str)
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved:
                return False

        return True
    except Exception as e:
        logger.warning(f"URL validation error for {url}: {e}")
        return False

async def scrape_url(url: str) -> str:
    """Scrapes the visible text from a URL using Playwright."""
    try:
        if not await is_safe_url(url):
            logger.error(f"SSRF attempt blocked for url: {url}")
            return ""

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Wait for content to load, timeout after 15 seconds
            await page.goto(url, wait_until="networkidle", timeout=15000)
            
            # Get HTML
            html = await page.content()
            await browser.close()
            
            # Use BeautifulSoup to extract text cleanly
            # Using asyncio.to_thread to prevent blocking the event loop during CPU-bound parsing
            def parse_html():
                soup = BeautifulSoup(html, 'html.parser')
                # Remove scripts and styles
                for script in soup(["script", "style", "nav", "footer"]):
                    script.extract()
                return soup.get_text(separator=' ', strip=True)
            
            text = await asyncio.to_thread(parse_html)
            
            # Truncate to reasonable length for AI processing
            return text[:10000] 
    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
        return ""

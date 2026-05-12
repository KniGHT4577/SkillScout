import httpx
import logging
import asyncio
from app.core.config import settings
from app.services.scraper import scrape_url
from app.services.ai import generate_ai_metadata
from app.db.session import AsyncSessionLocal
from app.models.opportunity import Opportunity, DifficultyLevel
from sqlalchemy import select

logger = logging.getLogger(__name__)

async def discover_opportunities(query: str = "free tech certifications courses bootcamps"):
    """Uses Tavily to search for new opportunities."""
    urls = []
    
    if not settings.TAVILY_API_KEY:
        logger.warning("TAVILY_API_KEY not set, using mock URLs for discovery")
        urls = [
            "https://www.coursera.org/learn/machine-learning",
            "https://cs50.harvard.edu/x/2024/",
            "https://www.freecodecamp.org/"
        ]
    else:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": settings.TAVILY_API_KEY,
                        "query": query,
                        "search_depth": "advanced",
                        "include_answer": False,
                        "include_raw_content": False,
                        "max_results": 10
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                urls = [result["url"] for result in data.get("results", [])]
        except Exception as e:
            logger.error(f"Error calling Tavily: {e}")
            urls = []

    # Process URLs
    if urls:
        await asyncio.gather(*(process_url(url) for url in urls))

async def process_url(url: str):
    """Scrape, analyze, and save a URL to the DB."""
    async with AsyncSessionLocal() as db:
        # Check if already exists
        existing = await db.execute(select(Opportunity).where(Opportunity.url == url))
        if existing.scalars().first():
            logger.info(f"URL already exists in DB: {url}")
            return
            
        logger.info(f"Processing new URL: {url}")
        
        # Scrape
        text_content = await scrape_url(url)
        if not text_content:
            logger.warning(f"Could not extract text from {url}")
            return
            
        # Analyze
        metadata = await generate_ai_metadata(url, text_content)
        
        # Ensure enum values are correct
        diff_str = metadata.get("difficulty", "all_levels").lower()
        diff_enum = DifficultyLevel.all_levels
        try:
            diff_enum = DifficultyLevel(diff_str)
        except ValueError:
            pass

        # Save to DB
        new_opp = Opportunity(
            title=metadata.get("title", "Unknown Title"),
            provider=metadata.get("provider", "Unknown Provider"),
            url=url,
            description=text_content[:500] + "...", # Small snippet
            category=metadata.get("category", "Course"),
            is_free=metadata.get("is_free", True),
            original_price=metadata.get("original_price"),
            ai_summary=metadata.get("ai_summary"),
            skills_covered=metadata.get("skills_covered"),
            difficulty=diff_enum,
            estimated_duration=metadata.get("estimated_duration"),
            source="Pipeline"
        )
        
        db.add(new_opp)
        try:
            await db.commit()
            logger.info(f"Successfully saved {url} to DB")
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to save {url} to DB: {e}")

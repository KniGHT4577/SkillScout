import httpx
import json
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

async def generate_ai_metadata(url: str, text_content: str) -> dict:
    """Uses OpenRouter to generate metadata from scraped text."""
    if not settings.OPENROUTER_API_KEY:
        logger.warning("OPENROUTER_API_KEY not set, returning mock metadata")
        return get_mock_metadata()

    prompt = f"""
    Analyze the following extracted text from a learning opportunity page ({url}).
    Extract the following details and return ONLY a JSON object:
    - title: The name of the course/certification
    - provider: The organization offering it (e.g., Coursera, Microsoft, local bootcamp)
    - category: One of [Course, Certification, Bootcamp, Workshop]
    - is_free: boolean (true if it's completely free or has a significant free tier)
    - original_price: string (e.g., "$99" or null if free)
    - ai_summary: A concise 2-3 sentence summary of what this is and why it's valuable.
    - skills_covered: A comma-separated string of 3-5 key skills taught.
    - difficulty: One of [beginner, intermediate, advanced, all_levels]
    - estimated_duration: A short string (e.g., "4 weeks", "10 hours")

    Text content (truncated):
    {text_content[:4000]}
    """

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "google/gemini-pro",
                    "messages": [{"role": "user", "content": prompt}],
                    "response_format": {"type": "json_object"}
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            
            try:
                # Sometimes LLMs wrap json in code blocks
                if content.startswith("```json"):
                    content = content[7:-3]
                return json.loads(content)
            except json.JSONDecodeError:
                logger.error(f"Failed to parse OpenRouter JSON response: {content}")
                return get_mock_metadata()
                
    except Exception as e:
        logger.error(f"Error calling OpenRouter: {e}")
        return get_mock_metadata()

def get_mock_metadata() -> dict:
    return {
        "title": "Machine Learning Foundations",
        "provider": "Mock Provider Inc.",
        "category": "Course",
        "is_free": True,
        "original_price": None,
        "ai_summary": "This is a dynamically generated summary of the learning opportunity. It teaches the core concepts of machine learning in a concise manner.",
        "skills_covered": "Python, Scikit-Learn, Data Analysis",
        "difficulty": "beginner",
        "estimated_duration": "4 weeks"
    }

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from app.services.discovery import discover_opportunities

logger = logging.getLogger(__name__)

def start_scheduler():
    logger.info("Starting background scheduler...")
    scheduler = AsyncIOScheduler()
    
    # Run discovery pipeline every 4 hours
    scheduler.add_job(
        discover_opportunities,
        trigger=CronTrigger(hour="*/4"),
        id="discovery_pipeline",
        name="Discover new learning opportunities",
        replace_existing=True
    )
    
    scheduler.start()
    return scheduler

# Utility to trigger manually for initial seed
async def seed_data():
    logger.info("Running initial data seed...")
    await discover_opportunities()

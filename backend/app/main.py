from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import logging
import os

from app.api.endpoints import auth, users, opportunities, bookmarks
from app.services.scheduler import start_scheduler, seed_data

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = None
    
    # In Cloud Run, we should rely on Cloud Scheduler calling /trigger-discovery
    # rather than APScheduler, but we'll leave APScheduler running if we are local.
    is_cloud_run = os.environ.get("K_SERVICE") is not None
    
    if not is_cloud_run:
        logger.info("Running locally - Starting internal APScheduler")
        scheduler = start_scheduler()
    else:
        logger.info("Running on Cloud Run - Skipping internal APScheduler (Use Cloud Scheduler -> /api/opportunities/trigger-discovery instead)")
    
    # Run a background task to seed initial data so the app isn't empty on first run
    asyncio.create_task(seed_data())
    
    yield
    
    # Shutdown
    if scheduler:
        scheduler.shutdown()

app = FastAPI(title="SkillScout AI API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Update for production to actual domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(opportunities.router, prefix="/api/opportunities", tags=["opportunities"])
app.include_router(bookmarks.router, prefix="/api/bookmarks", tags=["bookmarks"])

@app.get("/")
async def root():
    return {"message": "Welcome to SkillScout AI API. Status: Healthy"}

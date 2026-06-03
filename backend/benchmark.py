import asyncio
import time
import os
import aiosqlite
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base
from app.models.opportunity import Opportunity, DifficultyLevel
from app.models.bookmark import Bookmark # Make sure models are loaded

DATABASE_URL = "sqlite+aiosqlite:///./test_benchmark.db"
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def setup_data():
    if os.path.exists("./test_benchmark.db"):
        os.remove("./test_benchmark.db")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        print("Inserting 50,000 records...")
        opportunities = []
        for i in range(50000):
            opportunities.append(Opportunity(
                title=f"Opportunity {i}",
                provider="Provider",
                url=f"http://example.com/{i}",
                description="Description",
                category="Course" if i % 2 == 0 else "Bootcamp",
                is_free=i % 3 == 0,
                difficulty=DifficultyLevel.beginner if i % 4 == 0 else DifficultyLevel.advanced
            ))
            if len(opportunities) >= 5000:
                session.add_all(opportunities)
                await session.commit()
                opportunities = []
        if opportunities:
            session.add_all(opportunities)
            await session.commit()
        print("Data inserted.")

async def run_benchmark():
    async with AsyncSessionLocal() as session:
        start = time.perf_counter()

        # We need to explicitly consume the results for the DB to actually do the filtering and return rows
        # Just calling execute might lazy-evaluate or not fetch all depending on the driver
        for _ in range(50):
            res = await session.execute(
                select(Opportunity).where(Opportunity.category == "Course")
            )
            res.fetchall()

            res = await session.execute(
                select(Opportunity).where(Opportunity.is_free == True)
            )
            res.fetchall()

            res = await session.execute(
                select(Opportunity).where(Opportunity.difficulty == DifficultyLevel.beginner)
            )
            res.fetchall()

            res = await session.execute(
                select(Opportunity)
                .where(Opportunity.category == "Course")
                .where(Opportunity.is_free == True)
                .where(Opportunity.difficulty == DifficultyLevel.beginner)
            )
            res.fetchall()

        end = time.perf_counter()
        print(f"Benchmark completed in {end - start:.4f} seconds")

async def main():
    await setup_data()
    await run_benchmark()
    await engine.dispose()
    if os.path.exists("./test_benchmark.db"):
        os.remove("./test_benchmark.db")

if __name__ == "__main__":
    asyncio.run(main())

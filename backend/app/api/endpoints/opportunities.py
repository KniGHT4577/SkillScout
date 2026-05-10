from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, desc
from typing import Any, List, Optional

from app.db.session import get_db
from app.models.opportunity import Opportunity, DifficultyLevel
from app.schemas.opportunity import Opportunity as OpportunitySchema, PaginatedOpportunities

router = APIRouter()

@router.get("/", response_model=PaginatedOpportunities)
async def get_opportunities(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    category: Optional[str] = None,
    difficulty: Optional[DifficultyLevel] = None,
    is_free: Optional[bool] = None,
) -> Any:
    skip = (page - 1) * size
    
    query = select(Opportunity)
    count_query = select(func.count()).select_from(Opportunity)
    
    if search:
        search_filter = or_(
            Opportunity.title.ilike(f"%{search}%"),
            Opportunity.description.ilike(f"%{search}%"),
            Opportunity.skills_covered.ilike(f"%{search}%")
        )
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)
        
    if category:
        query = query.where(Opportunity.category == category)
        count_query = count_query.where(Opportunity.category == category)
        
    if difficulty:
        query = query.where(Opportunity.difficulty == difficulty)
        count_query = count_query.where(Opportunity.difficulty == difficulty)
        
    if is_free is not None:
        query = query.where(Opportunity.is_free == is_free)
        count_query = count_query.where(Opportunity.is_free == is_free)
        
    # Order by newest
    query = query.order_by(desc(Opportunity.created_at))
        
    query = query.offset(skip).limit(size)
    
    result = await db.execute(query)
    items = result.scalars().all()
    
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size
    }

@router.get("/{id}", response_model=OpportunitySchema)
async def get_opportunity(id: int, db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(select(Opportunity).where(Opportunity.id == id))
    opportunity = result.scalars().first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opportunity

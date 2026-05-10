from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Any, List
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.user import User
from app.models.bookmark import Bookmark
from app.models.opportunity import Opportunity
from app.schemas.bookmark import Bookmark as BookmarkSchema, BookmarkCreate
from app.api.deps import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[BookmarkSchema])
async def get_bookmarks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    result = await db.execute(
        select(Bookmark)
        .where(Bookmark.user_id == current_user.id)
        .options(selectinload(Bookmark.opportunity))
    )
    return result.scalars().all()

@router.post("/", response_model=BookmarkSchema)
async def create_bookmark(
    bookmark_in: BookmarkCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    # Check if opportunity exists
    opt_result = await db.execute(select(Opportunity).where(Opportunity.id == bookmark_in.opportunity_id))
    if not opt_result.scalars().first():
        raise HTTPException(status_code=404, detail="Opportunity not found")
        
    # Check if already bookmarked
    existing = await db.execute(
        select(Bookmark).where(
            and_(Bookmark.user_id == current_user.id, Bookmark.opportunity_id == bookmark_in.opportunity_id)
        )
    )
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="Already bookmarked")

    bookmark = Bookmark(user_id=current_user.id, opportunity_id=bookmark_in.opportunity_id)
    db.add(bookmark)
    await db.commit()
    await db.refresh(bookmark)
    
    # Reload with opportunity relation
    result = await db.execute(
        select(Bookmark)
        .where(Bookmark.id == bookmark.id)
        .options(selectinload(Bookmark.opportunity))
    )
    return result.scalars().first()

@router.delete("/{opportunity_id}")
async def delete_bookmark(
    opportunity_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    result = await db.execute(
        select(Bookmark).where(
            and_(Bookmark.user_id == current_user.id, Bookmark.opportunity_id == opportunity_id)
        )
    )
    bookmark = result.scalars().first()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
        
    await db.delete(bookmark)
    await db.commit()
    return {"message": "Bookmark removed"}

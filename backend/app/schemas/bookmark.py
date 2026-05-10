from pydantic import BaseModel
from datetime import datetime
from app.schemas.opportunity import Opportunity

class BookmarkBase(BaseModel):
    opportunity_id: int

class BookmarkCreate(BookmarkBase):
    pass

class Bookmark(BookmarkBase):
    id: int
    user_id: int
    created_at: datetime
    opportunity: Opportunity

    class Config:
        from_attributes = True

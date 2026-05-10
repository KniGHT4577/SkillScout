from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime
from app.models.opportunity import DifficultyLevel

class OpportunityBase(BaseModel):
    title: str
    provider: str
    url: HttpUrl
    description: Optional[str] = None
    category: Optional[str] = None
    is_free: bool = True
    original_price: Optional[str] = None
    ai_summary: Optional[str] = None
    skills_covered: Optional[str] = None
    difficulty: DifficultyLevel = DifficultyLevel.all_levels
    estimated_duration: Optional[str] = None
    source: Optional[str] = None

class OpportunityCreate(OpportunityBase):
    pass

class Opportunity(OpportunityBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        
class PaginatedOpportunities(BaseModel):
    items: List[Opportunity]
    total: int
    page: int
    size: int

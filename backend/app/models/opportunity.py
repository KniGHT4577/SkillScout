from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Enum
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime
import enum

class DifficultyLevel(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"
    all_levels = "all_levels"

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    provider = Column(String, index=True, nullable=False) # e.g., Coursera, Udemy, Local Bootcamp
    url = Column(String, unique=True, nullable=False)
    description = Column(Text)
    category = Column(String, index=True) # e.g., Certification, Course, Bootcamp
    
    # Pricing info
    is_free = Column(Boolean, default=True, index=True)
    original_price = Column(String, nullable=True)
    
    # AI generated metadata
    ai_summary = Column(Text, nullable=True)
    skills_covered = Column(String, nullable=True) # Comma separated or JSON string
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.all_levels, index=True)
    estimated_duration = Column(String, nullable=True)
    
    source = Column(String) # Where did we find it (e.g., Tavily, direct scrape)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    bookmarks = relationship("Bookmark", back_populates="opportunity")

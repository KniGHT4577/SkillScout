from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta
from typing import Any

from app.db.session import get_db
from app.core.config import settings
from app.core.security.password import verify_password, get_password_hash
from app.core.security.jwt import create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, Token
from pydantic import BaseModel

router = APIRouter()

class SignupResponse(BaseModel):
    message: str

@router.post("/signup", response_model=SignupResponse)
async def signup(user_in: UserCreate, db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(select(User).where(User.email == user_in.email))
    user = result.scalars().first()

    success_response = {"message": "Signup process completed."}

    if user:
        # Prevent timing attacks by hashing a dummy password
        # This ensures the response time is roughly equal whether the user exists or not
        get_password_hash(user_in.password)
        return success_response
    
    hashed_password = get_password_hash(user_in.password)
    user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
    )
    db.add(user)
    await db.commit()

    return success_response

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

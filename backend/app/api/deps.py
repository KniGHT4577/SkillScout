from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security.jwt import decode_access_token
from app.schemas.user import TokenData
from app.models.user import User
from sqlalchemy import select
from cachetools import TTLCache

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# Cache to store user objects by email (max 1000 items, expires in 5 minutes)
user_cache = TTLCache(maxsize=1000, ttl=300)

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    # Check cache first using get() to avoid KeyError if TTL expires between check and access
    cached_user = user_cache.get(email)
    if cached_user:
        return cached_user

    token_data = TokenData(email=email)
    
    result = await db.execute(select(User).where(User.email == token_data.email))
    user = result.scalars().first()
    
    if user is None:
        raise credentials_exception

    # Store in cache
    user_cache[email] = user
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

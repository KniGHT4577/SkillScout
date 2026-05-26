import bcrypt
import asyncio

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return await asyncio.to_thread(
        bcrypt.checkpw,
        plain_password[:72].encode('utf-8'),
        hashed_password.encode('utf-8')
    )

async def get_password_hash(password: str) -> str:
    def _hashpw():
        return bcrypt.hashpw(password[:72].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    return await asyncio.to_thread(_hashpw)

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.models.user import User
from sqlalchemy import select

@pytest.mark.asyncio
async def test_signup_new_user(override_get_db, db_session):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/auth/signup",
            json={
                "email": "testnew@example.com",
                "password": "strongpassword123",
                "full_name": "Test New User"
            }
        )
    assert response.status_code == 200
    assert response.json() == {"message": "Signup process completed."}

    # Verify the user was created
    result = await db_session.execute(select(User).where(User.email == "testnew@example.com"))
    user = result.scalars().first()
    assert user is not None
    assert user.full_name == "Test New User"

@pytest.mark.asyncio
async def test_signup_existing_user(override_get_db):
    # First signup
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            "/api/auth/signup",
            json={
                "email": "testexisting@example.com",
                "password": "strongpassword123",
                "full_name": "Test Existing User"
            }
        )

        # Second signup with same email
        response = await ac.post(
            "/api/auth/signup",
            json={
                "email": "testexisting@example.com",
                "password": "differentpassword",
                "full_name": "Different Name"
            }
        )

    # Should not reveal the user exists via 400 error
    assert response.status_code == 200
    assert response.json() == {"message": "Signup process completed."}

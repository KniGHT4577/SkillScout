import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from jose import jwt
from app.core.security.jwt import create_access_token
from app.core.config import settings

@patch("app.core.security.jwt.datetime")
def test_create_access_token_default_expiration(mock_datetime):
    # Set a fixed mocked current time
    fixed_now = datetime(2023, 1, 1, 12, 0, 0)
    mock_datetime.utcnow.return_value = fixed_now

    data = {"sub": "user_123"}
    token = create_access_token(data=data)

    # Decode token, disabling expiration verification since the mocked time is in the past
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={"verify_exp": False})

    # Assert payload contains subject
    assert decoded.get("sub") == "user_123"

    # Verify expiration is correctly calculated
    expected_expire = fixed_now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # JWT standard expiration claims are integers (Unix timestamps)
    assert decoded.get("exp") == int(expected_expire.timestamp())

@patch("app.core.security.jwt.datetime")
def test_create_access_token_custom_expiration(mock_datetime):
    # Set a fixed mocked current time
    fixed_now = datetime(2023, 1, 1, 12, 0, 0)
    mock_datetime.utcnow.return_value = fixed_now

    data = {"sub": "user_123"}
    expires_delta = timedelta(hours=2)
    token = create_access_token(data=data, expires_delta=expires_delta)

    # Decode token with verify_exp=False
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={"verify_exp": False})

    # Assert payload contains subject
    assert decoded.get("sub") == "user_123"

    # Verify expiration is correctly calculated
    expected_expire = fixed_now + expires_delta
    # JWT standard expiration claims are integers (Unix timestamps)
    assert decoded.get("exp") == int(expected_expire.timestamp())

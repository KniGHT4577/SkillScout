import pytest
from datetime import timedelta
from app.core.security.jwt import create_access_token, decode_access_token
from app.core.config import settings

def test_decode_access_token_valid():
    # Arrange
    data = {"sub": "testuser@example.com"}
    token = create_access_token(data)

    # Act
    decoded_data = decode_access_token(token)

    # Assert
    assert decoded_data.get("sub") == data["sub"]
    assert "exp" in decoded_data

def test_decode_access_token_invalid():
    # Arrange
    invalid_token = "this.is.an.invalid.token"

    # Act
    decoded_data = decode_access_token(invalid_token)

    # Assert
    assert decoded_data == {}


def test_create_access_token_with_expires_delta():
    # Arrange
    data = {"sub": "testuser@example.com"}
    delta = timedelta(minutes=5)

    # Act
    token = create_access_token(data, expires_delta=delta)
    decoded_data = decode_access_token(token)

    # Assert
    assert decoded_data.get("sub") == data["sub"]
    assert "exp" in decoded_data

import pytest
from datetime import timedelta
from app.core.security.jwt import create_access_token, decode_access_token

def test_create_and_decode_access_token():
    data = {"sub": "user_id_123"}
    token = create_access_token(data=data)
    decoded = decode_access_token(token)
    assert decoded.get("sub") == "user_id_123"
    assert "exp" in decoded

def test_decode_access_token_malformed():
    token = "invalid.token.string"
    decoded = decode_access_token(token)
    assert decoded == {}

def test_decode_access_token_expired():
    data = {"sub": "user_id_123"}
    # create a token that expired 1 minute ago
    token = create_access_token(data=data, expires_delta=timedelta(minutes=-1))
    decoded = decode_access_token(token)
    assert decoded == {}

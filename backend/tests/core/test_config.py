import pytest
from app.core.config import parse_cors

def test_parse_cors_comma_separated_string():
    assert parse_cors("http://localhost, http://example.com") == ["http://localhost", "http://example.com"]
    assert parse_cors("http://localhost") == ["http://localhost"]
    assert parse_cors("a,b, c , d ") == ["a", "b", "c", "d"]

def test_parse_cors_list():
    assert parse_cors(["http://localhost", "http://example.com"]) == ["http://localhost", "http://example.com"]
    assert parse_cors([]) == []

def test_parse_cors_string_starting_with_bracket():
    # If a string starts with '[', it returns the string itself
    assert parse_cors('["http://localhost"]') == '["http://localhost"]'

def test_parse_cors_invalid_type():
    with pytest.raises(ValueError):
        parse_cors(123)

    with pytest.raises(ValueError):
        parse_cors({"origins": "http://localhost"})

    with pytest.raises(ValueError):
        parse_cors(None)

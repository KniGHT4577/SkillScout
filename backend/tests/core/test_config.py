import pytest
from app.core.config import parse_cors

def test_parse_cors_comma_separated_string():
    assert parse_cors("http://localhost, http://example.com") == ["http://localhost", "http://example.com"]
    assert parse_cors("http://localhost") == ["http://localhost"]
    assert parse_cors("http://localhost,http://example.com") == ["http://localhost", "http://example.com"]

def test_parse_cors_list():
    assert parse_cors(["http://localhost", "http://example.com"]) == ["http://localhost", "http://example.com"]
    assert parse_cors([]) == []

def test_parse_cors_string_starting_with_bracket():
    # If the string starts with "[", the code currently returns it as-is
    assert parse_cors('["http://localhost"]') == '["http://localhost"]'

def test_parse_cors_invalid_input():
    with pytest.raises(ValueError):
        parse_cors(123)

    with pytest.raises(ValueError):
        parse_cors({"key": "value"})

    with pytest.raises(ValueError):
        parse_cors(None)

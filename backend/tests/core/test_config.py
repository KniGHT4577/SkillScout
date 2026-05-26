import pytest
from app.core.config import parse_cors

def test_parse_cors_valid_string():
    assert parse_cors("http://localhost:3000, http://localhost:8000") == ["http://localhost:3000", "http://localhost:8000"]

def test_parse_cors_valid_string_no_spaces():
    assert parse_cors("http://localhost:3000,http://localhost:8000") == ["http://localhost:3000", "http://localhost:8000"]

def test_parse_cors_valid_list():
    assert parse_cors(["http://localhost:3000", "http://localhost:8000"]) == ["http://localhost:3000", "http://localhost:8000"]

def test_parse_cors_valid_string_starts_with_bracket():
    assert parse_cors('["http://localhost:3000"]') == '["http://localhost:3000"]'

def test_parse_cors_invalid_type_dict():
    with pytest.raises(ValueError) as excinfo:
        parse_cors({"http://localhost:3000": True})
    assert excinfo.value.args[0] == {"http://localhost:3000": True}

def test_parse_cors_invalid_type_int():
    with pytest.raises(ValueError) as excinfo:
        parse_cors(123)
    assert excinfo.value.args[0] == 123

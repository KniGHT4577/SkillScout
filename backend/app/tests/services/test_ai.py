import pytest
import httpx
from unittest.mock import AsyncMock
import json
from app.services.ai import generate_ai_metadata, get_mock_metadata
from app.core.config import settings

@pytest.mark.asyncio
async def test_generate_ai_metadata_openrouter_exception(mocker):
    # Ensure OPENROUTER_API_KEY is set so it doesn't return early
    mocker.patch.object(settings, "OPENROUTER_API_KEY", "test_key")

    mock_client = mocker.patch("app.services.ai.httpx.AsyncClient", autospec=True)
    mock_instance = mock_client.return_value
    mock_instance.__aenter__.return_value = mock_instance

    # Use httpx.RequestError properly with request parameter
    mock_request = mocker.Mock(spec=httpx.Request)
    mock_instance.post.side_effect = httpx.RequestError("Connection error", request=mock_request)

    result = await generate_ai_metadata("http://example.com", "Sample text content")

    # Verify it falls back to mock metadata on RequestError
    assert result == get_mock_metadata()
    mock_instance.post.assert_called_once()


@pytest.mark.asyncio
async def test_generate_ai_metadata_json_decode_error(mocker):
    # Ensure OPENROUTER_API_KEY is set
    mocker.patch.object(settings, "OPENROUTER_API_KEY", "test_key")

    mock_client = mocker.patch("app.services.ai.httpx.AsyncClient", autospec=True)
    mock_instance = mock_client.return_value
    mock_instance.__aenter__.return_value = mock_instance

    # Mock response with invalid JSON
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Invalid JSON content"}}]
    }
    mock_instance.post.return_value = mock_response

    result = await generate_ai_metadata("http://example.com", "Sample text content")

    # Verify it falls back to mock metadata on JSONDecodeError
    assert result == get_mock_metadata()
    mock_instance.post.assert_called_once()

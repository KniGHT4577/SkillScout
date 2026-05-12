from app.services.ai import get_mock_metadata

def test_get_mock_metadata():
    metadata = get_mock_metadata()

    # Assert it returns a dictionary
    assert isinstance(metadata, dict)

    # Assert all expected keys are present
    expected_keys = [
        "title",
        "provider",
        "category",
        "is_free",
        "original_price",
        "ai_summary",
        "skills_covered",
        "difficulty",
        "estimated_duration"
    ]
    for key in expected_keys:
        assert key in metadata

    # Additional specific value assertions based on the hardcoded implementation
    assert metadata["title"] == "Machine Learning Foundations"
    assert metadata["is_free"] is True
    assert metadata["original_price"] is None
    assert metadata["difficulty"] == "beginner"

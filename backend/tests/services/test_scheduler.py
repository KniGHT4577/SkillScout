import pytest
from unittest.mock import patch, MagicMock
from app.services.scheduler import start_scheduler

def test_start_scheduler_registers_jobs():
    with patch("app.services.scheduler.AsyncIOScheduler") as mock_scheduler_cls:
        # Arrange
        mock_scheduler = MagicMock()
        mock_scheduler_cls.return_value = mock_scheduler

        # Act
        scheduler = start_scheduler()

        # Assert
        assert scheduler == mock_scheduler
        mock_scheduler_cls.assert_called_once()
        mock_scheduler.add_job.assert_called_once()

        # Verify the specific job registration details
        call_args, call_kwargs = mock_scheduler.add_job.call_args
        from app.services.discovery import discover_opportunities
        assert call_args[0] == discover_opportunities
        assert call_kwargs['id'] == "discovery_pipeline"
        assert call_kwargs['name'] == "Discover new learning opportunities"
        assert call_kwargs['replace_existing'] is True

        # Verify it started
        mock_scheduler.start.assert_called_once()

@pytest.mark.asyncio
async def test_seed_data():
    with patch("app.services.scheduler.discover_opportunities") as mock_discover:
        # Arrange
        from app.services.scheduler import seed_data

        # Act
        await seed_data()

        # Assert
        mock_discover.assert_called_once()

"""Pytest configuration and fixtures."""

import os
import sys
from pathlib import Path

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load .env file BEFORE any other imports
from dotenv import load_dotenv

load_dotenv(dotenv_path=project_root / ".env")

# Set default log level for tests
os.environ.setdefault("LOG_LEVEL", "DEBUG")


@pytest.fixture
def api_token():
    """Get API token from environment for integration tests."""
    token = os.environ.get("ACEDATACLOUD_API_TOKEN", "")
    if not token:
        pytest.skip("ACEDATACLOUD_API_TOKEN not configured for integration tests")
    return token


@pytest.fixture
def mock_video_response():
    """Mock successful video generation response."""
    return {
        "success": True,
        "task_id": "test-task-123",
        "trace_id": "test-trace-456",
        "data": [
            {
                "id": "video-id-1",
                "video_url": "https://platform.cdn.acedata.cloud/veo/test-video.mp4",
                "created_at": "2025-01-21 00:00:00",
                "complete_at": "2025-01-21 00:02:00",
                "state": "succeeded",
            }
        ],
    }


@pytest.fixture
def mock_task_response():
    """Mock task query response."""
    return {
        "id": "task-123",
        "created_at": 1705788000.0,
        "request": {
            "action": "text2video",
            "model": "veo2",
            "prompt": "A test video",
        },
        "response": {
            "success": True,
            "task_id": "task-123",
            "data": [
                {
                    "id": "video-id-1",
                    "state": "succeeded",
                    "video_url": "https://platform.cdn.acedata.cloud/veo/test.mp4",
                }
            ],
        },
    }


@pytest.fixture
def mock_error_response():
    """Mock error response."""
    return {
        "success": False,
        "error": {
            "code": "invalid_request",
            "message": "Invalid parameters provided",
        },
    }

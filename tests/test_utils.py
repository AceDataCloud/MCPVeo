"""Unit tests for utility functions."""

import json

from core.utils import (
    format_task_result,
    format_video_result,
)


class TestFormatVideoResult:
    """Tests for format_video_result function."""

    def test_format_success(self, mock_video_response):
        """Test formatting successful video response."""
        result = format_video_result(mock_video_response)
        data = json.loads(result)
        assert data["success"] is True
        assert data["task_id"] == "test-task-123"
        assert data["trace_id"] == "test-trace-456"
        assert len(data["data"]) == 1
        assert data["data"][0]["id"] == "video-id-1"
        assert data["data"][0]["state"] == "succeeded"
        assert "video_url" in data["data"][0]

    def test_format_error(self, mock_error_response):
        """Test formatting error response."""
        result = format_video_result(mock_error_response)
        data = json.loads(result)
        assert data["success"] is False
        assert data["error"]["code"] == "invalid_request"

    def test_format_empty_data(self):
        """Test formatting response with no video data."""
        response = {"success": True, "task_id": "123", "data": []}
        result = format_video_result(response)
        data = json.loads(result)
        assert data["task_id"] == "123"
        assert data["data"] == []


class TestFormatTaskResult:
    """Tests for format_task_result function."""

    def test_format_success(self, mock_task_response):
        """Test formatting successful task response."""
        result = format_task_result(mock_task_response)
        data = json.loads(result)
        assert data["id"] == "task-123"
        assert data["request"]["action"] == "text2video"
        assert data["response"]["success"] is True
        assert data["response"]["data"][0]["id"] == "video-id-1"

    def test_format_error(self):
        """Test formatting error response."""
        error_response = {"error": {"code": "not_found", "message": "Task not found"}}
        result = format_task_result(error_response)
        data = json.loads(result)
        assert data["error"]["code"] == "not_found"

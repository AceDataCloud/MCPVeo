"""Unit tests for utility functions."""

from core.utils import (
    format_task_result,
    format_video_result,
)


class TestFormatVideoResult:
    """Tests for format_video_result function."""

    def test_format_success(self, mock_video_response):
        """Test formatting successful video response."""
        result = format_video_result(mock_video_response)
        assert "Task ID: test-task-123" in result
        assert "Trace ID: test-trace-456" in result
        assert "Video 1" in result
        assert "video-id-1" in result
        assert "succeeded" in result
        assert "https://platform.cdn.acedata.cloud/veo/test-video.mp4" in result

    def test_format_error(self, mock_error_response):
        """Test formatting error response."""
        result = format_video_result(mock_error_response)
        assert "Error: invalid_request" in result
        assert "Invalid parameters" in result

    def test_format_empty_data(self):
        """Test formatting response with no video data."""
        response = {"success": True, "task_id": "123", "data": []}
        result = format_video_result(response)
        assert "Task ID: 123" in result
        assert "Video" not in result


class TestFormatTaskResult:
    """Tests for format_task_result function."""

    def test_format_success(self, mock_task_response):
        """Test formatting successful task response."""
        result = format_task_result(mock_task_response)
        assert "Task ID: task-123" in result
        assert "Action: text2video" in result
        assert "Response: Success" in result
        assert "video-id-1" in result

    def test_format_error(self):
        """Test formatting error response."""
        error_response = {"error": {"code": "not_found", "message": "Task not found"}}
        result = format_task_result(error_response)
        assert "Error: not_found" in result

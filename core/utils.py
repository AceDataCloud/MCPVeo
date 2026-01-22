"""Utility functions for MCP Veo server."""

from typing import Any


def format_video_result(data: dict[str, Any]) -> str:
    """Format video generation result for display.

    Args:
        data: API response dictionary

    Returns:
        Formatted string representation of the result
    """
    if not data.get("success", False):
        error = data.get("error", {})
        return f"Error: {error.get('code', 'unknown')} - {error.get('message', 'Unknown error')}"

    lines = [
        f"Task ID: {data.get('task_id', 'N/A')}",
        f"Trace ID: {data.get('trace_id', 'N/A')}",
        "",
    ]

    videos = data.get("data", [])
    for i, video in enumerate(videos, 1):
        lines.extend(
            [
                f"--- Video {i} ---",
                f"ID: {video.get('id', 'N/A')}",
                f"State: {video.get('state', 'N/A')}",
                f"Created At: {video.get('created_at', 'N/A')}",
                f"Complete At: {video.get('complete_at') or 'N/A'}",
                f"Video URL: {video.get('video_url', 'N/A')}",
                "",
            ]
        )

    return "\n".join(lines)


def format_task_result(data: dict[str, Any]) -> str:
    """Format task query result for display.

    Args:
        data: API response dictionary

    Returns:
        Formatted string representation of the result
    """
    if "error" in data:
        error = data.get("error", {})
        return f"Error: {error.get('code', 'unknown')} - {error.get('message', 'Unknown error')}"

    request_info = data.get("request", {})
    response_info = data.get("response", {})

    lines = [
        f"Task ID: {data.get('id', 'N/A')}",
        f"Created At: {data.get('created_at', 'N/A')}",
        "",
        "Request:",
        f"  Action: {request_info.get('action', 'N/A')}",
        f"  Model: {request_info.get('model', 'N/A')}",
        f"  Prompt: {request_info.get('prompt', 'N/A')}",
        "",
    ]

    if response_info.get("success"):
        lines.append("Response: Success")
        lines.append("")

        for i, video in enumerate(response_info.get("data", []), 1):
            lines.extend(
                [
                    f"--- Video {i} ---",
                    f"ID: {video.get('id', 'N/A')}",
                    f"State: {video.get('state', 'N/A')}",
                    f"Video URL: {video.get('video_url', 'N/A')}",
                    "",
                ]
            )
    else:
        lines.append(f"Response: {response_info}")

    return "\n".join(lines)

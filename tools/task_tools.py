"""Task query tools for Veo API."""

import asyncio
from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import format_task_result


@mcp.tool()
async def veo_get_task(
    task_id: Annotated[
        str,
        Field(
            description="The task ID returned from a generation request. This is the 'task_id' field from any veo_text_to_video, veo_image_to_video, or veo_get_1080p tool response."
        ),
    ] = "",
    trace_id: Annotated[
        str,
        Field(description="Optional trace identifier of the task to retrieve."),
    ] = "",
) -> str:
    """Query the status and result of a video generation task.

    Use this to check if a generation is complete and retrieve the resulting
    video URLs and metadata.

    Use this when:
    - You want to check if a generation has completed
    - You need to retrieve video URLs from a previous generation
    - You want to get the full details of a generated video

    Task states:
    - 'processing': Generation is still in progress
    - 'succeeded': Generation finished successfully
    - 'failed': Generation failed (check error message)

    Returns:
        Task status and generated video information including URLs and state.
    """
    payload: dict = {"action": "retrieve"}
    if task_id:
        payload["id"] = task_id
    if trace_id:
        payload["trace_id"] = trace_id

    result = await client.query_task(**payload)
    # Throttle polling: sleep 5s for incomplete tasks so LLM clients
    # don't burn through poll attempts in seconds.
    response = result.get("response", {})
    is_complete = response.get("success") is True
    is_failed = response.get("success") is False or str(result.get("state", "")).lower() in {
        "failed",
        "error",
        "cancelled",
        "canceled",
    }
    if not is_complete and not is_failed:
        await asyncio.sleep(5)
    return format_task_result(result)


@mcp.tool()
async def veo_get_tasks_batch(
    task_ids: Annotated[
        list[str] | None,
        Field(
            description="Optional list of task IDs to query. Maximum recommended batch size is 50 tasks."
        ),
    ] = None,
    trace_ids: Annotated[
        list[str] | None,
        Field(description="Optional list of trace identifiers to query."),
    ] = None,
    offset: Annotated[
        int,
        Field(description="Number of matching tasks to skip for list retrieval."),
    ] = 0,
    limit: Annotated[
        int,
        Field(description="Maximum number of tasks to return."),
    ] = 12,
    type: Annotated[
        str,
        Field(description="Optional task type filter."),
    ] = "",
    created_at_min: Annotated[
        float | None,
        Field(description="Return tasks created after this Unix timestamp."),
    ] = None,
    created_at_max: Annotated[
        float | None,
        Field(description="Return tasks created before this Unix timestamp."),
    ] = None,
) -> str:
    """Query multiple video generation tasks at once.

    Efficiently check the status of multiple tasks in a single request.
    More efficient than calling veo_get_task multiple times.

    Use this when:
    - You have multiple pending generations to check
    - You want to get status of several videos at once
    - You're tracking a batch of generations

    Returns:
        Status and video information for all queried tasks.
    """
    payload: dict = {
        "action": "retrieve_batch",
        "offset": offset,
        "limit": limit,
    }
    if task_ids:
        payload["ids"] = task_ids
    if trace_ids:
        payload["trace_ids"] = trace_ids
    if type:
        payload["type"] = type
    if created_at_min is not None:
        payload["created_at_min"] = created_at_min
    if created_at_max is not None:
        payload["created_at_max"] = created_at_max

    result = await client.query_task(**payload)

    if "error" in result:
        error = result.get("error", {})
        return f"Error: {error.get('code', 'unknown')} - {error.get('message', 'Unknown error')}"

    lines = [f"Total Tasks: {result.get('count', 0)}", ""]

    for item in result.get("items", []):
        response_info = item.get("response", {})
        lines.extend(
            [
                f"=== Task: {item.get('id', 'N/A')} ===",
                f"Created At: {item.get('created_at', 'N/A')}",
                f"Success: {response_info.get('success', False)}",
            ]
        )

        for video in response_info.get("data", []):
            lines.append(f"  - {video.get('id', 'Unknown')}: {video.get('video_url', 'N/A')}")

        lines.append("")

    return "\n".join(lines)

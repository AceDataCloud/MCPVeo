"""Guards against re-introducing models/endpoints/params the API no longer accepts."""

import inspect
from typing import get_args

import pytest

from core.client import VeoClient
from core.types import DEFAULT_MODEL, AspectRatio, VeoModel
from tools import task_tools, video_tools

# Mirrors the `model` / `aspect_ratio` enums in the Veo OpenAPI spec.
SPEC_MODELS = {"veo3", "veo3-fast", "veo31", "veo31-fast", "veo31-fast-ingredients"}
SPEC_ASPECT_RATIOS = {"16:9", "9:16"}
SPEC_TASK_PARAMS = {
    "task_ids",
    "trace_ids",
    "offset",
    "limit",
    "type",
    "created_at_min",
    "created_at_max",
}


def test_models_match_spec():
    assert set(get_args(VeoModel)) == SPEC_MODELS


def test_retired_models_are_gone():
    # veo2/veo2-fast were retired upstream and now 400.
    assert "veo2" not in get_args(VeoModel)
    assert "veo2-fast" not in get_args(VeoModel)


def test_aspect_ratios_match_spec():
    assert set(get_args(AspectRatio)) == SPEC_ASPECT_RATIOS


def test_default_model_is_selectable():
    assert DEFAULT_MODEL in get_args(VeoModel)


def test_removed_video_endpoints_are_not_exposed():
    assert not hasattr(VeoClient, "upsample_video")
    assert not hasattr(VeoClient, "extend_video")
    assert not hasattr(VeoClient, "reshoot_video")
    assert not hasattr(VeoClient, "video_objects")


def test_removed_video_tools_are_not_registered():
    assert not hasattr(video_tools, "veo_upsample")
    assert not hasattr(video_tools, "veo_extend_video")
    assert not hasattr(video_tools, "veo_reshoot")
    assert not hasattr(video_tools, "veo_video_objects")


def test_task_tools_cover_spec_params():
    single_params = set(inspect.signature(task_tools.veo_get_task).parameters)
    batch_params = set(inspect.signature(task_tools.veo_get_tasks_batch).parameters)

    assert {"task_id", "trace_id"} <= single_params
    assert batch_params >= SPEC_TASK_PARAMS


@pytest.mark.asyncio
async def test_get_task_forwards_trace_id(monkeypatch):
    class FakeClient:
        def __init__(self):
            self.payload = None

        async def query_task(self, **kwargs):
            self.payload = kwargs
            return {"id": "task-1", "request": {}, "response": {"success": True, "data": []}}

    fake_client = FakeClient()
    monkeypatch.setattr(task_tools, "client", fake_client)

    await task_tools.veo_get_task(trace_id="00000000-0000-0000-0000-000000000000")

    assert fake_client.payload == {
        "action": "retrieve",
        "trace_id": "00000000-0000-0000-0000-000000000000",
    }


@pytest.mark.asyncio
async def test_get_tasks_batch_forwards_list_filters(monkeypatch):
    class FakeClient:
        def __init__(self):
            self.payload = None

        async def query_task(self, **kwargs):
            self.payload = kwargs
            return {"count": 0, "items": []}

    fake_client = FakeClient()
    monkeypatch.setattr(task_tools, "client", fake_client)

    await task_tools.veo_get_tasks_batch(
        trace_ids=["00000000-0000-0000-0000-000000000000"],
        offset=2,
        limit=5,
        type="video",
        created_at_min=1.0,
        created_at_max=2.0,
    )

    assert fake_client.payload == {
        "action": "retrieve_batch",
        "trace_ids": ["00000000-0000-0000-0000-000000000000"],
        "offset": 2,
        "limit": 5,
        "type": "video",
        "created_at_min": 1.0,
        "created_at_max": 2.0,
    }

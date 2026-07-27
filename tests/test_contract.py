"""Guards against re-introducing models/params the API no longer accepts."""

from typing import get_args

from core.types import DEFAULT_MODEL, AspectRatio, VeoModel

# Mirrors the `model` / `aspect_ratio` enums in the Veo OpenAPI spec.
SPEC_MODELS = {"veo3", "veo3-fast", "veo31", "veo31-fast", "veo31-fast-ingredients"}
SPEC_ASPECT_RATIOS = {"16:9", "9:16"}


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

"""Type definitions for Veo MCP server."""

from typing import Literal

# Veo model versions
VeoModel = Literal[
    "veo3",
    "veo3-fast",
    "veo31",
    "veo31-fast",
    "veo31-fast-ingredients",
]

# Aspect ratio options
AspectRatio = Literal["16:9", "9:16"]

# Default model
DEFAULT_MODEL: VeoModel = "veo31-fast"

# Video resolution options
VideoResolution = Literal["4k", "1080p", "gif"]

# Default aspect ratio
DEFAULT_ASPECT_RATIO: AspectRatio = "16:9"

# Upsample action options
VeoUpsampleAction = Literal["1080p", "4k", "gif"]

# Extend model options (only veo31 series)
VeoExtendModel = Literal["veo31-fast", "veo31"]

# Camera motion types for reshoot
VeoMotionType = Literal[
    "STATIONARY",
    "STATIONARY_UP",
    "STATIONARY_DOWN",
    "STATIONARY_LEFT",
    "STATIONARY_RIGHT",
    "STATIONARY_DOLLY_IN_ZOOM_OUT",
    "STATIONARY_DOLLY_OUT_ZOOM_IN",
    "UP",
    "DOWN",
    "LEFT_TO_RIGHT",
    "RIGHT_TO_LEFT",
    "FORWARD",
    "BACKWARD",
    "DOLLY_IN_ZOOM_OUT",
    "DOLLY_OUT_ZOOM_IN",
]

# Object action options
VeoObjectAction = Literal["insert", "remove"]

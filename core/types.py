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

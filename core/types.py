"""Type definitions for Veo MCP server."""

from typing import Literal

# Veo model versions
VeoModel = Literal[
    "veo2",
    "veo2-fast",
    "veo3",
    "veo3-fast",
    "veo31",
    "veo31-fast",
    "veo31-fast-ingredients",
]

# Aspect ratio options
AspectRatio = Literal["16:9", "3:4", "4:3", "1:1"]

# Default model
DEFAULT_MODEL: VeoModel = "veo2"

# Default aspect ratio
DEFAULT_ASPECT_RATIO: AspectRatio = "16:9"

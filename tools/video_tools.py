"""Video generation tools for Veo API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import DEFAULT_ASPECT_RATIO, DEFAULT_MODEL, AspectRatio, VeoModel
from core.utils import format_video_result


@mcp.tool()
async def veo_text_to_video(
    prompt: Annotated[
        str,
        Field(
            description="Description of the video to generate. Be descriptive about scene, subject, action, camera movement, lighting, and style. Examples: 'A white ceramic coffee mug on a glossy marble countertop, steam rising, soft morning light', 'Cinematic drone shot over a forest at sunset, golden hour lighting'"
        ),
    ],
    model: Annotated[
        VeoModel,
        Field(
            description="Veo model version. 'veo2' for quality mode, 'veo2-fast' for faster generation. 'veo3'/'veo31' offer improved quality. Models with '-fast' suffix are faster but slightly lower quality."
        ),
    ] = DEFAULT_MODEL,
    aspect_ratio: Annotated[
        AspectRatio,
        Field(
            description="Video aspect ratio. '16:9' for landscape/widescreen, '9:16' for portrait/vertical, '1:1' for square, '4:3' for standard, '3:4' for portrait standard."
        ),
    ] = DEFAULT_ASPECT_RATIO,
    translation: Annotated[
        bool,
        Field(
            description="If true, automatically translate the prompt to English for better generation quality. Useful for non-English prompts."
        ),
    ] = False,
    callback_url: Annotated[
        str,
        Field(
            description="Optional URL to receive a POST callback when generation completes. The callback will include the task_id and video results."
        ),
    ] = "",
) -> str:
    """Generate AI video from a text prompt using Veo.

    This creates a video from scratch based on your text description. Veo
    will interpret your prompt and generate a matching video clip.

    Use this when:
    - You want to create a video from a text description
    - You don't have a reference image to use
    - You want maximum creative freedom for Veo

    For video generation starting from an image, use veo_image_to_video instead.

    Returns:
        Task ID and generated video information including URLs and state.
    """
    payload: dict = {
        "action": "text2video",
        "prompt": prompt,
        "model": model,
        "aspect_ratio": aspect_ratio,
    }

    if translation:
        payload["translation"] = translation
    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.generate_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def veo_image_to_video(
    prompt: Annotated[
        str,
        Field(
            description="Description of the video motion and action. Describe what should happen to the subject in the image. Examples: 'The coffee steam rises gently', 'The person turns and smiles at the camera', 'Camera slowly zooms out revealing the landscape'"
        ),
    ],
    image_urls: Annotated[
        list[str],
        Field(
            description="List of image URLs to use as reference. For first-frame mode, provide 1 image. For first-last frame mode, provide 2-3 images. The first image is the starting frame, the last image is the ending frame. Maximum 3 images."
        ),
    ],
    model: Annotated[
        VeoModel,
        Field(
            description="Veo model version. Note: 'veo31-fast-ingredients' is for multi-image fusion mode only. Other models support 1 image (first frame) or 2-3 images (first/last frame)."
        ),
    ] = DEFAULT_MODEL,
    aspect_ratio: Annotated[
        AspectRatio,
        Field(
            description="Video aspect ratio. Should typically match your input image aspect ratio for best results."
        ),
    ] = DEFAULT_ASPECT_RATIO,
    translation: Annotated[
        bool,
        Field(
            description="If true, automatically translate the prompt to English for better generation quality."
        ),
    ] = False,
    callback_url: Annotated[
        str,
        Field(description="Optional URL to receive a POST callback when generation completes."),
    ] = "",
) -> str:
    """Generate AI video from one or more reference images using Veo.

    This creates a video using your image(s) as reference frames. The video
    will animate from/between your provided images according to the prompt.

    Image modes:
    - 1 image: First-frame mode - the video starts from your image
    - 2-3 images: First-last frame mode - video interpolates between images
    - veo31-fast-ingredients model: Multi-image fusion - blends elements from all images

    Use this when:
    - You have a specific image you want to animate
    - You want consistent visual style from a reference
    - You need to create a video transition between two images

    For video generation from text only, use veo_text_to_video instead.

    Returns:
        Task ID and generated video information including URLs and state.
    """
    payload: dict = {
        "action": "image2video",
        "prompt": prompt,
        "image_urls": image_urls,
        "model": model,
        "aspect_ratio": aspect_ratio,
    }

    if translation:
        payload["translation"] = translation
    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.generate_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def veo_get_1080p(
    video_id: Annotated[
        str,
        Field(
            description="The video ID from a previous generation result. This is the 'id' field from the video data, not the task_id."
        ),
    ],
) -> str:
    """Get the 1080p high-resolution version of a generated video.

    By default, Veo generates videos at a lower resolution for faster processing.
    Use this tool to get the full 1080p version of a completed video.

    Use this when:
    - You need a higher resolution version for production use
    - The initial video generation is complete and you want to upscale
    - You need a clearer, more detailed video output

    Note: The video must be in 'succeeded' state before requesting 1080p version.

    Returns:
        Task ID and the 1080p video information including the new video URL.
    """
    result = await client.get_1080p(video_id)
    return format_video_result(result)

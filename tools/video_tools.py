"""Video generation tools for Veo API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import (
    DEFAULT_ASPECT_RATIO,
    DEFAULT_MODEL,
    AspectRatio,
    VeoExtendModel,
    VeoModel,
    VeoMotionType,
    VeoObjectAction,
    VeoUpsampleAction,
    VideoResolution,
)
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
            description="Veo model version. 'veo31'/'veo31-fast' are the latest; 'veo3'/'veo3-fast' remain available. Models with '-fast' suffix are faster but slightly lower quality."
        ),
    ] = DEFAULT_MODEL,
    aspect_ratio: Annotated[
        AspectRatio,
        Field(
            description="Video aspect ratio: '16:9' for landscape/widescreen or '9:16' for portrait/vertical."
        ),
    ] = DEFAULT_ASPECT_RATIO,
    translation: Annotated[
        bool,
        Field(
            description="If true, automatically translate the prompt to English for better generation quality. Useful for non-English prompts."
        ),
    ] = False,
    resolution: Annotated[
        VideoResolution | None,
        Field(
            description="Video resolution. Options: '4k' for highest quality, '1080p' for standard HD, 'gif' for animated GIF format. If not specified, uses the model's default resolution."
        ),
    ] = None,
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
    if resolution:
        payload["resolution"] = resolution
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
    resolution: Annotated[
        VideoResolution | None,
        Field(
            description="Video resolution. Options: '4k' for highest quality, '1080p' for standard HD, 'gif' for animated GIF format."
        ),
    ] = None,
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
    action = "ingredients2video" if model == "veo31-fast-ingredients" else "image2video"
    payload: dict = {
        "action": action,
        "prompt": prompt,
        "image_urls": image_urls,
        "model": model,
        "aspect_ratio": aspect_ratio,
    }

    if translation:
        payload["translation"] = translation
    if resolution:
        payload["resolution"] = resolution
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
    model: Annotated[
        VeoModel,
        Field(
            description="The model used to generate the source video. Required by the API; pass the same model you used for the original generation."
        ),
    ] = DEFAULT_MODEL,
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
    result = await client.get_1080p(video_id, model)
    return format_video_result(result)


@mcp.tool()
async def veo_upsample(
    video_id: Annotated[
        str,
        Field(
            description="The video ID from a previous generation result. This is the 'id' field from the video data, not the task_id."
        ),
    ],
    action: Annotated[
        VeoUpsampleAction,
        Field(
            description="Upsample action. '1080p' upscales to 1080p resolution, '4k' upscales to 4K resolution, 'gif' converts to animated GIF."
        ),
    ] = "1080p",
    callback_url: Annotated[
        str,
        Field(description="Optional URL to receive a POST callback when upsampling completes."),
    ] = "",
) -> str:
    """Upsample a generated video to higher resolution.

    Use this to convert a video to a higher resolution (1080p, 4K) or to animated GIF.

    Use this when:
    - You need a higher resolution version for production use
    - You want to convert a video to GIF format
    - The initial video generation is complete and you want to upscale

    Note: The video must be in 'succeeded' state before upsampling.

    Returns:
        Task ID and the upsampled video information including the new video URL.
    """
    payload: dict = {
        "video_id": video_id,
        "action": action,
    }

    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.upsample_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def veo_extend_video(
    video_id: Annotated[
        str,
        Field(
            description="The video ID from a previous generation result. The source video must not itself be an extended video. Use the 'id' field from the video data."
        ),
    ],
    model: Annotated[
        VeoExtendModel,
        Field(
            description="The model used to extend the video. Only Veo 3.1 series is supported: 'veo31' for best quality, 'veo31-fast' for faster generation."
        ),
    ] = "veo31-fast",
    prompt: Annotated[
        str,
        Field(description="Optional prompt that guides the extended section of the video."),
    ] = "",
    callback_url: Annotated[
        str,
        Field(description="Optional URL to receive a POST callback when extension completes."),
    ] = "",
) -> str:
    """Extend a generated video by adding more content.

    Continues a previously generated video by appending a new section.
    Only Veo 3.1 series models (veo31, veo31-fast) are supported.

    Use this when:
    - You want to make a video longer
    - You need to add more content to an existing video
    - You want to guide what happens next in the video

    Returns:
        Task ID and extended video information including URLs and state.
    """
    payload: dict = {
        "video_id": video_id,
        "model": model,
    }

    if prompt:
        payload["prompt"] = prompt
    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.extend_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def veo_reshoot(
    video_id: Annotated[
        str,
        Field(
            description="The video ID from a previous generation result. Use the 'id' field from the video data."
        ),
    ],
    motion_type: Annotated[
        VeoMotionType,
        Field(
            description=(
                "Camera motion to apply when re-rendering the video. "
                "STATIONARY* keeps the camera fixed (with optional direction pan). "
                "UP/DOWN/LEFT_TO_RIGHT/RIGHT_TO_LEFT are directional camera movements. "
                "FORWARD/BACKWARD moves camera toward/away from subject. "
                "DOLLY_IN_ZOOM_OUT/DOLLY_OUT_ZOOM_IN are dolly-zoom effects."
            )
        ),
    ],
    callback_url: Annotated[
        str,
        Field(description="Optional URL to receive a POST callback when reshoot completes."),
    ] = "",
) -> str:
    """Re-render a video with a different camera motion.

    Re-renders an existing video clip with a new camera movement applied.
    Useful for changing the cinematography of a video without regenerating it from scratch.

    Use this when:
    - You want to change the camera movement in a video
    - You need a static shot vs a dynamic camera movement
    - You want to apply a dolly-zoom or tracking shot to existing video

    Returns:
        Task ID and re-rendered video information including URLs and state.
    """
    payload: dict = {
        "video_id": video_id,
        "motion_type": motion_type,
    }

    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.reshoot_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def veo_video_objects(
    video_id: Annotated[
        str,
        Field(
            description="The video ID from a previous generation result. Use the 'id' field from the video data."
        ),
    ],
    action: Annotated[
        VeoObjectAction,
        Field(
            description="'insert' adds a new object to the video. 'remove' deletes an object from a specific area."
        ),
    ],
    prompt: Annotated[
        str,
        Field(
            description="For 'insert': describes what object to add (strongly recommended). For 'remove': describes what to remove (optional). If omitted for insert, the API may reject the request."
        ),
    ] = "",
    image_mask: Annotated[
        str,
        Field(
            description="Optional mask image URL where white pixels indicate the region to operate on. Providing a mask improves precision for both insert and remove operations."
        ),
    ] = "",
    callback_url: Annotated[
        str,
        Field(description="Optional URL to receive a POST callback when the operation completes."),
    ] = "",
) -> str:
    """Insert or remove objects in a video.

    Modifies a generated video by adding or removing objects in specific regions.

    Use this when:
    - You want to add a new object to an existing video
    - You need to remove an unwanted object from a video
    - You want to precisely modify specific areas of a video

    Returns:
        Task ID and modified video information including URLs and state.
    """
    payload: dict = {
        "video_id": video_id,
        "action": action,
    }

    if prompt:
        payload["prompt"] = prompt
    if image_mask:
        payload["image_mask"] = image_mask
    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.video_objects(**payload)
    return format_video_result(result)

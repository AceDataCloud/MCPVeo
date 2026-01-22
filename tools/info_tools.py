"""Informational tools for Veo API."""

from core.server import mcp


@mcp.tool()
async def veo_list_models() -> str:
    """List all available Veo models and their capabilities.

    Shows all available model versions with their features, supported actions,
    and image input rules. Use this to understand which model to choose
    for your video generation.

    Model comparison:
    - veo2/veo2-fast: Standard models, 1 image (first frame)
    - veo3/veo3-fast: Improved quality, 1-3 images supported
    - veo31/veo31-fast: Latest models, 1-3 images supported
    - veo31-fast-ingredients: Multi-image fusion mode (image2video only)

    Returns:
        Table of all models with their capabilities and image rules.
    """
    return """Available Veo Models:

| Model                  | Text2Video | Image2Video | Image Input Rules           |
|------------------------|------------|-------------|------------------------------|
| veo2                   | ✅         | ✅          | 1 image (first frame)        |
| veo2-fast              | ✅         | ✅          | 1 image (first frame)        |
| veo3                   | ✅         | ✅          | 1-3 images (first/last)      |
| veo3-fast              | ✅         | ✅          | 1-3 images (first/last)      |
| veo31                  | ✅         | ✅          | 1-3 images (first/last)      |
| veo31-fast             | ✅         | ✅          | 1-3 images (first/last)      |
| veo31-fast-ingredients | ❌         | ✅          | 1-3 images (multi-fusion)    |

Image Input Modes:
- First Frame Mode (1 image): Video starts from your image
- First/Last Frame Mode (2-3 images): Video interpolates between images
- Multi-Fusion Mode (veo31-fast-ingredients only): Blends elements from all images

Recommendations:
- For quick generation: Use '-fast' suffix models
- For best quality: Use veo31 or veo3 (non-fast)
- For image fusion: Use veo31-fast-ingredients
- For text-only: Any model except veo31-fast-ingredients

Aspect Ratios:
- 16:9: Landscape/widescreen (default)
- 9:16: Portrait/vertical (social media stories)
- 4:3: Standard
- 3:4: Portrait standard
- 1:1: Square
"""


@mcp.tool()
async def veo_list_actions() -> str:
    """List all available Veo API actions and corresponding tools.

    Reference guide for what each action does and which tool to use.
    Helpful for understanding the full capabilities of the Veo MCP.

    Returns:
        Categorized list of all actions and their corresponding tools.
    """
    return """Available Veo Actions and Tools:

Video Generation:
- veo_text_to_video: Create video from a text prompt only
- veo_image_to_video: Create video from reference image(s) + prompt
- veo_get_1080p: Get high-resolution 1080p version of a video

Task Management:
- veo_get_task: Check status of a single video generation
- veo_get_tasks_batch: Check status of multiple generations at once

Information:
- veo_list_models: Show available models and their capabilities
- veo_list_actions: Show this action reference (you are here)
- veo_get_prompt_guide: Get tips for writing effective video prompts

Workflow Examples:
1. Quick video: veo_text_to_video → veo_get_task → (optional) veo_get_1080p
2. Image animation: veo_image_to_video → veo_get_task
3. Image transition: veo_image_to_video (with 2-3 images) → veo_get_task
4. Multi-image fusion: veo_image_to_video (model=veo31-fast-ingredients) → veo_get_task

API Response States:
- processing: Video is being generated
- succeeded: Generation complete, video URL available
- failed: Generation failed (check error message)

Tips:
- Generation typically takes 1-2 minutes
- Use callback_url for async notifications
- Request 1080p after initial generation succeeds
"""


@mcp.tool()
async def veo_get_prompt_guide() -> str:
    """Get guidance on writing effective prompts for Veo video generation.

    Shows how to structure prompts for best video generation results.
    Following these tips helps Veo understand your vision and generate
    more accurate and higher quality videos.

    Returns:
        Complete guide with prompt structure, examples, and tips.
    """
    return """Veo Prompt Writing Guide:

## Prompt Structure

A good video prompt should include:
1. **Subject**: What/who is in the video
2. **Action**: What is happening or moving
3. **Setting**: Where the scene takes place
4. **Camera**: Camera movement or angle
5. **Lighting**: Time of day, lighting style
6. **Style**: Visual style or mood

## Example Prompts by Category

**Product/Commercial:**
"A white ceramic coffee mug on a glossy marble countertop, steam rising gently, soft morning sunlight streaming through a window, shallow depth of field, commercial style"

**Nature/Landscape:**
"Cinematic drone shot slowly ascending over a misty forest at sunrise, golden rays filtering through the trees, 4K quality, documentary style"

**Portrait/People:**
"Close-up of a young woman with curly hair, she turns to look at the camera and smiles warmly, natural lighting, shallow depth of field, lifestyle photography"

**Abstract/Artistic:**
"Flowing liquid metal in slow motion, iridescent colors shifting and reflecting, black background, macro lens, surreal and mesmerizing"

**Action/Movement:**
"A red sports car drifting around a corner on a mountain road, dust and smoke trailing behind, tracking shot following the car, cinematic lighting"

## Camera Movement Keywords

- **Static**: Fixed camera, no movement
- **Pan**: Camera rotates left/right
- **Tilt**: Camera rotates up/down
- **Zoom**: Camera zooms in/out
- **Tracking/Following**: Camera moves with subject
- **Dolly**: Camera moves forward/backward
- **Crane/Aerial**: Camera moves up/down
- **Handheld**: Slightly shaky, documentary feel
- **Steadicam**: Smooth gliding movement

## Lighting Keywords

- **Golden hour**: Warm, soft sunset/sunrise light
- **Blue hour**: Cool, moody twilight
- **High key**: Bright, minimal shadows
- **Low key**: Dark, dramatic shadows
- **Backlit**: Light from behind subject
- **Rim lighting**: Outline of light around subject
- **Natural light**: Realistic outdoor lighting
- **Studio lighting**: Controlled, professional

## Style Keywords

- **Cinematic**: Film-like quality
- **Documentary**: Realistic, observational
- **Commercial**: Clean, professional
- **Artistic**: Creative, experimental
- **Vintage**: Retro, nostalgic look
- **Modern**: Contemporary, sleek
- **Dreamy**: Soft, ethereal

## Tips for Best Results

1. Be specific but not overly complex
2. Describe motion and change, not just static scenes
3. Include camera movement for dynamic videos
4. Specify lighting conditions
5. Use the translation option for non-English prompts
6. Match aspect ratio to your intended use (16:9 for landscape, 9:16 for vertical)
"""

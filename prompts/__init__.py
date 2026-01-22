"""Prompt templates for Veo MCP server.

MCP Prompts provide guidance to LLMs on when and how to use the available tools.
These are exposed via the MCP protocol and help LLMs make better decisions.
"""

from core.server import mcp


@mcp.prompt()
def veo_video_generation_guide() -> str:
    """Guide for choosing the right Veo tool for video generation."""
    return """# Veo Video Generation Guide

When the user wants to generate video, choose the appropriate tool based on their needs:

## Text to Video
**Tool:** `veo_text_to_video`
**Use when:**
- User gives a text description without images
- User wants to generate video from scratch
- User describes a scene, action, or concept

**Example:** "Create a video of a sunset over the ocean"
→ Call `veo_text_to_video` with prompt="Cinematic shot of a sunset over the ocean, golden hour lighting, waves gently rolling, peaceful atmosphere"

## Image to Video
**Tool:** `veo_image_to_video`
**Use when:**
- User provides one or more reference images
- User wants to animate a specific image
- User wants a video transition between images

**Image modes:**
- 1 image: First-frame mode (video starts from image)
- 2-3 images: First/last frame mode (video transitions between images)
- veo31-fast-ingredients: Multi-image fusion (blends elements)

**Example:** "Animate this product image"
→ Call `veo_image_to_video` with the image URL and a motion prompt

## Get High Resolution
**Tool:** `veo_get_1080p`
**Use when:**
- User wants a higher quality version
- Initial generation is complete
- User needs production-ready video

**Example:** "I need the 1080p version"
→ Call `veo_get_1080p` with the video_id from previous generation

## Checking Status
**Tool:** `veo_get_task`
**Use when:**
- Generation takes time and user wants to check progress
- User asks "is my video done?"
- Retrieving video URLs from a previous task

## Model Selection

**For quality:**
- veo31 or veo3 (non-fast versions)

**For speed:**
- veo2-fast, veo3-fast, veo31-fast

**For image fusion:**
- veo31-fast-ingredients (image2video only)

## Important Notes:
1. Video generation is async - always return the task_id
2. Generation typically takes 1-2 minutes
3. Use callback_url for async notifications
4. Match aspect ratio to intended use (16:9 landscape, 9:16 portrait)
"""


@mcp.prompt()
def veo_workflow_examples() -> str:
    """Common workflow examples for Veo video generation."""
    return """# Veo Workflow Examples

## Workflow 1: Text to Video Generation
1. User: "Create a video of a cat playing with yarn"
2. Call `veo_text_to_video(prompt="Close-up shot of an adorable cat playfully batting at a ball of red yarn, soft indoor lighting, shallow depth of field")`
3. Return task_id to user
4. User can check status with `veo_get_task(task_id)`
5. Once complete, optionally get 1080p with `veo_get_1080p(video_id)`

## Workflow 2: Image Animation
1. User provides an image URL
2. Ask what motion/action they want if not specified
3. Call `veo_image_to_video(prompt="The subject slowly turns to face the camera", image_urls=["user_image_url"])`
4. Return task_id

## Workflow 3: Image Transition Video
1. User provides 2-3 images
2. User wants a video that transitions between them
3. Call `veo_image_to_video(prompt="Smooth transition between scenes, camera movement", image_urls=["img1", "img2", "img3"], model="veo31")`
4. Return task_id

## Workflow 4: Multi-Image Fusion
1. User has multiple images they want to blend
2. Use the ingredients model for creative fusion
3. Call `veo_image_to_video(prompt="Blend the elements from each image into a cohesive scene", image_urls=[...], model="veo31-fast-ingredients")`
4. Return task_id

## Workflow 5: Production-Ready Video
1. Generate initial video with `veo_text_to_video`
2. Wait for completion with `veo_get_task`
3. Get high-res version with `veo_get_1080p(video_id)`

## Tips:
- Write detailed prompts including subject, action, camera, lighting
- Use translation=true for non-English prompts
- Choose aspect ratio based on platform (16:9 YouTube, 9:16 TikTok/Reels)
- For fast iterations, use '-fast' model variants
"""


@mcp.prompt()
def veo_style_suggestions() -> str:
    """Style and prompt writing suggestions for Veo."""
    return """# Veo Prompt Style Guide

## Effective Prompt Components

Good prompts include:
- **Subject:** The main focus of the video
- **Action:** What is happening, motion description
- **Camera:** Camera movement and angle
- **Lighting:** Time of day, light quality
- **Style:** Visual style, mood, quality

## Example Prompts by Use Case

**Product Commercial:**
"A sleek smartphone rotating slowly on a reflective surface, studio lighting with soft shadows, premium commercial style, 4K quality"

**Social Media Content:**
"POV walking through a vibrant night market in Tokyo, colorful neon signs reflecting on wet pavement, handheld camera movement, cinematic"

**Nature/Travel:**
"Aerial drone shot slowly descending over a pristine turquoise lagoon, tropical island in background, golden hour lighting, peaceful atmosphere"

**Portrait/Lifestyle:**
"Young woman sitting in a cozy cafe, turning to look out the window, soft natural light, shallow depth of field, lifestyle photography style"

**Abstract/Artistic:**
"Ink drops falling into water in slow motion, swirling colors of blue and gold, macro lens, black background, mesmerizing and fluid"

**Action/Sports:**
"Skateboarder performing a kickflip in slow motion, tracking shot following the board, sunset backlighting, urban environment"

## Camera Movement Terms

- Static: No camera movement
- Pan left/right: Camera rotates horizontally
- Tilt up/down: Camera rotates vertically
- Zoom in/out: Changes focal length
- Tracking shot: Camera follows subject
- Dolly in/out: Camera physically moves
- Crane shot: Elevated camera movement
- Handheld: Slight natural shake
- Steadicam: Smooth floating movement
- Aerial/Drone: From above

## Lighting Descriptions

- Golden hour: Warm sunset/sunrise light
- Blue hour: Cool twilight tones
- High key: Bright, minimal shadows
- Low key: Dark, dramatic contrast
- Backlit: Light from behind
- Rim light: Edge lighting around subject
- Natural: Realistic ambient light
- Studio: Controlled professional lighting
- Neon: Colorful artificial lighting

## Quality and Style Keywords

- Cinematic: Film-like quality
- 4K/8K: High resolution
- Slow motion: Slowed down footage
- Timelapse: Sped up footage
- Macro: Extreme close-up
- Wide angle: Expansive view
- Shallow depth of field: Blurred background
- Documentary: Realistic, observational
- Artistic: Creative, experimental
"""

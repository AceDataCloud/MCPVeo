# MCP Veo

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for AI video generation using [Veo](https://deepmind.google/technologies/veo/) through the [AceDataCloud API](https://platform.acedata.cloud).

Generate AI videos from text prompts or images directly from Claude, VS Code, or any MCP-compatible client.

## Features

- **Text to Video** - Create AI-generated videos from text descriptions
- **Image to Video** - Animate images or create transitions between images
- **Multi-Image Fusion** - Blend elements from multiple images
- **1080p Upscaling** - Get high-resolution versions of generated videos
- **Task Tracking** - Monitor generation progress and retrieve results
- **Multiple Models** - Choose between quality and speed with various Veo models

## Quick Start

### 1. Get API Token

Get your API token from [AceDataCloud Platform](https://platform.acedata.cloud):

1. Sign up or log in
2. Navigate to [Veo Videos API](https://platform.acedata.cloud/documents/63e01dc3-eb21-499e-8049-3025c460058f)
3. Click "Acquire" to get your token

### 2. Install

```bash
# Clone the repository
git clone https://github.com/AceDataCloud/MCPVeo.git
cd MCPVeo

# Install with pip
pip install -e .

# Or with uv (recommended)
uv pip install -e .
```

### 3. Configure

```bash
# Copy example environment file
cp .env.example .env

# Edit with your API token
echo "ACEDATACLOUD_API_TOKEN=your_token_here" > .env
```

### 4. Run

```bash
# Run the server
mcp-veo

# Or with Python directly
python main.py
```

## Claude Desktop Integration

Add to your Claude Desktop configuration:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "veo": {
      "command": "mcp-veo",
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

Or if using uv:

```json
{
  "mcpServers": {
    "veo": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/MCPVeo", "mcp-veo"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

## Available Tools

### Video Generation

| Tool | Description |
|------|-------------|
| `veo_text_to_video` | Generate video from a text prompt |
| `veo_image_to_video` | Generate video from reference image(s) |
| `veo_get_1080p` | Get high-resolution 1080p version |

### Tasks

| Tool | Description |
|------|-------------|
| `veo_get_task` | Query a single task status |
| `veo_get_tasks_batch` | Query multiple tasks at once |

### Information

| Tool | Description |
|------|-------------|
| `veo_list_models` | List available Veo models |
| `veo_list_actions` | List available API actions |
| `veo_get_prompt_guide` | Get video prompt writing guide |

## Usage Examples

### Generate Video from Text

```
User: Create a video of a sunset over the ocean

Claude: I'll generate a sunset video for you.
[Calls veo_text_to_video with prompt="Cinematic shot of a golden sunset over the ocean, waves gently rolling, warm colors reflecting on the water"]
```

### Animate an Image

```
User: Animate this product image to make it rotate slowly

Claude: I'll create a video from your image.
[Calls veo_image_to_video with image_urls=["product_image.jpg"], prompt="Product slowly rotates 360 degrees, studio lighting"]
```

### Create Image Transition

```
User: Create a video that transitions between these two landscape photos

Claude: I'll create a transition video between your images.
[Calls veo_image_to_video with image_urls=["img1.jpg", "img2.jpg"], prompt="Smooth cinematic transition between scenes"]
```

## Available Models

| Model | Text2Video | Image2Video | Image Input |
|-------|------------|-------------|-------------|
| `veo2` | ✅ | ✅ | 1 image (first frame) |
| `veo2-fast` | ✅ | ✅ | 1 image (first frame) |
| `veo3` | ✅ | ✅ | 1-3 images |
| `veo3-fast` | ✅ | ✅ | 1-3 images |
| `veo31` | ✅ | ✅ | 1-3 images |
| `veo31-fast` | ✅ | ✅ | 1-3 images |
| `veo31-fast-ingredients` | ❌ | ✅ | 1-3 images (fusion) |

**Aspect Ratios**:
- `16:9` - Landscape/widescreen (default)
- `9:16` - Portrait/vertical (social media)
- `4:3` - Standard
- `3:4` - Portrait standard
- `1:1` - Square

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ACEDATACLOUD_API_TOKEN` | API token from AceDataCloud | **Required** |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `VEO_DEFAULT_MODEL` | Default model for generation | `veo2` |
| `VEO_REQUEST_TIMEOUT` | Request timeout in seconds | `180` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Command Line Options

```bash
mcp-veo --help

Options:
  --version          Show version
  --transport        Transport mode: stdio (default) or http
  --port             Port for HTTP transport (default: 8000)
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/AceDataCloud/MCPVeo.git
cd MCPVeo

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows

# Install with dev dependencies
pip install -e ".[dev,test]"
```

### Run Tests

```bash
# Run unit tests
pytest

# Run with coverage
pytest --cov=core --cov=tools

# Run integration tests (requires API token)
pytest tests/test_integration.py -m integration
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type check
mypy core tools
```

### Build & Publish

```bash
# Install build dependencies
pip install -e ".[release]"

# Build package
python -m build

# Upload to PyPI
twine upload dist/*
```

## Project Structure

```
MCPVeo/
├── core/                   # Core modules
│   ├── __init__.py
│   ├── client.py          # HTTP client for Veo API
│   ├── config.py          # Configuration management
│   ├── exceptions.py      # Custom exceptions
│   ├── server.py          # MCP server initialization
│   ├── types.py           # Type definitions
│   └── utils.py           # Utility functions
├── tools/                  # MCP tool definitions
│   ├── __init__.py
│   ├── video_tools.py     # Video generation tools
│   ├── info_tools.py      # Information tools
│   └── task_tools.py      # Task query tools
├── prompts/                # MCP prompts
│   └── __init__.py
├── tests/                  # Test suite
│   ├── conftest.py
│   ├── test_client.py
│   ├── test_config.py
│   ├── test_integration.py
│   └── test_utils.py
├── .env.example           # Environment template
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── main.py                # Entry point
├── pyproject.toml         # Project configuration
└── README.md
```

## API Reference

This server wraps the [AceDataCloud Veo API](https://platform.acedata.cloud/documents/63e01dc3-eb21-499e-8049-3025c460058f):

- [Veo Videos API](https://platform.acedata.cloud/documents/63e01dc3-eb21-499e-8049-3025c460058f) - Video generation
- [Veo Tasks API](https://platform.acedata.cloud/documents/63e01dc3-eb21-499e-8049-3025c460058f) - Task queries

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [AceDataCloud Platform](https://platform.acedata.cloud)
- [Google Veo](https://deepmind.google/technologies/veo/)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

Made with love by [AceDataCloud](https://platform.acedata.cloud)

# VeoMCP

<!-- mcp-name: io.github.AceDataCloud/mcp-veo -->

[![PyPI version](https://img.shields.io/pypi/v/mcp-veo.svg)](https://pypi.org/project/mcp-veo/)
[![PyPI downloads](https://img.shields.io/pypi/dm/mcp-veo.svg)](https://pypi.org/project/mcp-veo/)
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

## Tool Reference

| Tool | Description |
|------|-------------|
| `veo_text_to_video` | Generate AI video from a text prompt using Veo. |
| `veo_image_to_video` | Generate AI video from one or more reference images using Veo. |
| `veo_get_1080p` | Get the 1080p high-resolution version of a generated video. |
| `veo_get_task` | Query the status and result of a video generation task. |
| `veo_get_tasks_batch` | Query multiple video generation tasks at once. |
| `veo_list_models` | List all available Veo models and their capabilities. |
| `veo_list_actions` | List all available Veo API actions and corresponding tools. |
| `veo_get_prompt_guide` | Get guidance on writing effective prompts for Veo video generation. |

## Quick Start

### 1. Get Your API Token

1. Sign up at [AceDataCloud Platform](https://platform.acedata.cloud)
2. Go to the [API documentation page](https://platform.acedata.cloud/documents/veo-videos)
3. Click **"Acquire"** to get your API token
4. Copy the token for use below

### 2. Use the Hosted Server (Recommended)

AceDataCloud hosts a managed MCP server — **no local installation required**.

**Endpoint:** `https://veo.mcp.acedata.cloud/mcp`

All requests require a Bearer token. Use the API token from Step 1.

#### Claude.ai

Connect directly on [Claude.ai](https://claude.ai) with OAuth — **no API token needed**:

1. Go to Claude.ai **Settings → Integrations → Add More**
2. Enter the server URL: `https://veo.mcp.acedata.cloud/mcp`
3. Complete the OAuth login flow
4. Start using the tools in your conversation

#### Claude Desktop

Add to your config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "veo": {
      "type": "streamable-http",
      "url": "https://veo.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### Cursor / Windsurf

Add to your MCP config (`.cursor/mcp.json` or `.windsurf/mcp.json`):

```json
{
  "mcpServers": {
    "veo": {
      "type": "streamable-http",
      "url": "https://veo.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### VS Code (Copilot)

Add to your VS Code MCP config (`.vscode/mcp.json`):

```json
{
  "servers": {
    "veo": {
      "type": "streamable-http",
      "url": "https://veo.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

Or install the [Ace Data Cloud MCP extension](https://marketplace.visualstudio.com/items?itemName=acedatacloud.acedatacloud-mcp) for VS Code, which registers the hosted MCP servers with one-click setup.

#### JetBrains IDEs

1. Go to **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**
2. Click **Add** → **HTTP**
3. Paste:

```json
{
  "mcpServers": {
    "veo": {
      "url": "https://veo.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```


#### Claude Code

Claude Code supports MCP servers natively:

```bash
claude mcp add veo --transport http https://veo.mcp.acedata.cloud/mcp \
  -h "Authorization: Bearer YOUR_API_TOKEN"
```

Or add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "veo": {
      "type": "streamable-http",
      "url": "https://veo.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### Cline

Add to Cline's MCP settings (`.cline/mcp_settings.json`):

```json
{
  "mcpServers": {
    "veo": {
      "type": "streamable-http",
      "url": "https://veo.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### Amazon Q Developer

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "veo": {
      "type": "streamable-http",
      "url": "https://veo.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### Roo Code

Add to Roo Code MCP settings:

```json
{
  "mcpServers": {
    "veo": {
      "type": "streamable-http",
      "url": "https://veo.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### Continue.dev

Add to `.continue/config.yaml`:

```yaml
mcpServers:
  - name: veo
    type: streamable-http
    url: https://veo.mcp.acedata.cloud/mcp
    headers:
      Authorization: "Bearer YOUR_API_TOKEN"
```

#### Zed

Add to Zed's settings (`~/.config/zed/settings.json`):

```json
{
  "language_models": {
    "mcp_servers": {
      "veo": {
        "url": "https://veo.mcp.acedata.cloud/mcp",
        "headers": {
          "Authorization": "Bearer YOUR_API_TOKEN"
        }
      }
    }
  }
}
```

#### cURL Test

```bash
# Health check (no auth required)
curl https://veo.mcp.acedata.cloud/health

# MCP initialize
curl -X POST https://veo.mcp.acedata.cloud/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```

### 3. Or Run Locally (Alternative)

If you prefer to run the server on your own machine:

```bash
# Install from PyPI
pip install mcp-veo
# or
uvx mcp-veo

# Set your API token
export ACEDATACLOUD_API_TOKEN="your_token_here"

# Run (stdio mode for Claude Desktop / local clients)
mcp-veo

# Run (HTTP mode for remote access)
mcp-veo --transport http --port 8000
```

#### Claude Desktop (Local)

```json
{
  "mcpServers": {
    "veo": {
      "command": "uvx",
      "args": ["mcp-veo"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

#### Docker (Self-Hosting)

```bash
docker pull ghcr.io/acedatacloud/mcp-veo:latest
docker run -p 8000:8000 ghcr.io/acedatacloud/mcp-veo:latest
```

Clients connect with their own Bearer token — the server extracts the token from each request's `Authorization` header.

## Available Tools

### Video Generation

| Tool                 | Description                            |
| -------------------- | -------------------------------------- |
| `veo_text_to_video`  | Generate video from a text prompt      |
| `veo_image_to_video` | Generate video from reference image(s) |
| `veo_get_1080p`      | Get high-resolution 1080p version      |

### Tasks

| Tool                  | Description                  |
| --------------------- | ---------------------------- |
| `veo_get_task`        | Query a single task status   |
| `veo_get_tasks_batch` | Query multiple tasks at once |

### Information

| Tool                   | Description                    |
| ---------------------- | ------------------------------ |
| `veo_list_models`      | List available Veo models      |
| `veo_list_actions`     | List available API actions     |
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

| Model                    | Text2Video | Image2Video | Image Input           |
| ------------------------ | ---------- | ----------- | --------------------- |
| `veo3`                   | ✅         | ✅          | 1-3 images            |
| `veo3-fast`              | ✅         | ✅          | 1-3 images            |
| `veo31`                  | ✅         | ✅          | 1-3 images            |
| `veo31-fast`             | ✅         | ✅          | 1-3 images            |
| `veo31-fast-ingredients` | ❌         | ✅          | 1-3 images (fusion)   |

**Aspect Ratios**:

- `16:9` - Landscape/widescreen (default)
- `9:16` - Portrait/vertical (social media)

## Configuration

### Environment Variables

| Variable                    | Description                  | Default                     |
| --------------------------- | ---------------------------- | --------------------------- |
| `ACEDATACLOUD_API_TOKEN`    | API token from AceDataCloud  | **Required**                |
| `ACEDATACLOUD_API_BASE_URL` | API base URL                 | `https://api.acedata.cloud` |
| `ACEDATACLOUD_OAUTH_CLIENT_ID`  | OAuth client ID (hosted mode) | —                           |
| `ACEDATACLOUD_PLATFORM_BASE_URL` | Platform base URL            | `https://platform.acedata.cloud` |
| `VEO_DEFAULT_MODEL`         | Default model for generation | `veo31-fast`                |
| `VEO_REQUEST_TIMEOUT`       | Request timeout in seconds   | `180`                       |
| `LOG_LEVEL`                 | Logging level                | `INFO`                      |

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
git clone https://github.com/AceDataCloud/VeoMCP.git
cd VeoMCP

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
VeoMCP/
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
├── deploy/                 # Deployment configs
│   └── production/
│       ├── deployment.yaml
│       ├── ingress.yaml
│       └── service.yaml
├── .env.example           # Environment template
├── .gitignore
├── Dockerfile             # Docker image for HTTP mode
├── docker-compose.yaml    # Docker Compose config
├── LICENSE
├── main.py                # Entry point
├── pyproject.toml         # Project configuration
└── README.md
```

## API Reference

This server wraps the [AceDataCloud Veo API](https://platform.acedata.cloud/documents/veo-videos):

- [Veo Videos API](https://platform.acedata.cloud/documents/veo-videos) - Video generation
- [Veo Tasks API](https://platform.acedata.cloud/documents/veo-videos) - Task queries

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## Documentation

<!-- canonical-documentation -->
[Documentation](https://platform.acedata.cloud/documents/veo-mcp)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [AceDataCloud Platform](https://platform.acedata.cloud)
- [Google Veo](https://deepmind.google/technologies/veo/)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

Made with love by [AceDataCloud](https://platform.acedata.cloud)

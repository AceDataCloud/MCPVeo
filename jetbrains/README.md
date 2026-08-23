# Veo MCP — JetBrains Plugin

AI Video Generation with [Google Veo](https://deepmind.google/technologies/veo) via [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) for JetBrains IDEs.

<!-- Plugin description -->
This plugin helps you set up the MCP Google Veo server with JetBrains AI Assistant.
Once configured, AI Assistant can generate videos from text and images
— all powered by [Ace Data Cloud](https://platform.acedata.cloud).

**14 AI Tools** — Generate videos from text and images.
<!-- Plugin description end -->

## Quick Start

1. Install this plugin from the [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/com.acedatacloud.mcp.veo)
2. Open **Settings → Tools → Veo MCP**
3. Enter your [Ace Data Cloud](https://platform.acedata.cloud) API token
4. Click **Copy Config** (STDIO or HTTP)
5. Paste into **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**

### STDIO Mode (Local)

Runs the MCP server locally. Requires [uv](https://github.com/astral-sh/uv) installed.

```json
{
  "mcpServers": {
    "veo": {
      "command": "uvx",
      "args": ["mcp-veo"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your-token"
      }
    }
  }
}
```

### HTTP Mode (Remote)

Connects to the hosted MCP server at `veo.mcp.acedata.cloud`. No local install needed.

```json
{
  "mcpServers": {
    "veo": {
      "url": "https://veo.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer your-token"
      }
    }
  }
}
```

## Links

- [Ace Data Cloud Platform](https://platform.acedata.cloud)
- [Documentation](https://platform.acedata.cloud/documents/veo-mcp)
- [PyPI Package](https://pypi.org/project/mcp-veo/)
- [Source Code](https://github.com/AceDataCloud/VeoMCP)

## License

MIT

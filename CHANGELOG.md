# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Removed

- `veo2` and `veo2-fast` models — retired upstream; both now return `400 model is not supported`
- Aspect ratios `4:3`, `3:4` and `1:1` — the API only accepts `16:9` and `9:16`

### Changed

- Default model is now `veo31-fast` (was `veo2`)

## [0.1.0] - 2025-06-01

### Added

- Initial release of MCP Veo Server
- Video generation tools:
  - `veo_generate_video` - Generate video from text prompts
  - `veo_generate_video_from_image` - Generate video using reference images
- Task tracking:
  - `veo_get_task` - Query single task status
  - `veo_get_tasks_batch` - Query multiple tasks
- Information tools:
  - `veo_list_models` - List available models
  - `veo_list_actions` - List available actions
- stdio and HTTP transport modes
- Comprehensive test suite
- Full documentation

[Unreleased]: https://github.com/AceDataCloud/VeoMCP/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/AceDataCloud/VeoMCP/releases/tag/v0.1.0

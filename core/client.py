"""HTTP client for Veo API."""

import json
from typing import Any

import httpx
from loguru import logger

from core.config import settings
from core.exceptions import VeoAPIError, VeoAuthError, VeoTimeoutError


class VeoClient:
    """Async HTTP client for AceDataCloud Veo API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        """Initialize the Veo API client.

        Args:
            api_token: API token for authentication. If not provided, uses settings.
            base_url: Base URL for the API. If not provided, uses settings.
        """
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

        logger.info(f"VeoClient initialized with base_url: {self.base_url}")
        logger.debug(f"API token configured: {'Yes' if self.api_token else 'No'}")
        logger.debug(f"Request timeout: {self.timeout}s")

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            logger.error("API token not configured!")
            raise VeoAuthError("API token not configured")

        return {
            "accept": "application/json",
            "authorization": f"Bearer {self.api_token}",
            "content-type": "application/json",
        }

    async def request(
        self,
        endpoint: str,
        payload: dict[str, Any],
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Make a POST request to the Veo API.

        Args:
            endpoint: API endpoint path (e.g., "/veo/videos")
            payload: Request body as dictionary
            timeout: Optional timeout override

        Returns:
            API response as dictionary

        Raises:
            VeoAuthError: If authentication fails
            VeoAPIError: If the API request fails
            VeoTimeoutError: If the request times out
        """
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout

        logger.info(f"🚀 POST {url}")
        logger.debug(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        logger.debug(f"Timeout: {request_timeout}s")

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self._get_headers(),
                    timeout=request_timeout,
                )

                logger.info(f"📥 Response status: {response.status_code}")

                if response.status_code == 401:
                    logger.error("❌ Authentication failed: Invalid API token")
                    raise VeoAuthError("Invalid API token")

                if response.status_code == 403:
                    logger.error("❌ Access denied: Check API permissions")
                    raise VeoAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()

                result = response.json()
                logger.success(f"✅ Request successful! Task ID: {result.get('task_id', 'N/A')}")

                # Log summary of response
                if result.get("success"):
                    data = result.get("data", [])
                    if isinstance(data, list):
                        logger.info(f"📊 Returned {len(data)} item(s)")
                        for i, item in enumerate(data, 1):
                            if "video_url" in item:
                                logger.info(
                                    f"   Video {i}: {item.get('id', 'Unknown')} - {item.get('state', 'unknown')}"
                                )
                else:
                    logger.warning(f"⚠️ API returned success=false: {result.get('error', {})}")

                return result  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                logger.error(f"⏰ Request timeout after {request_timeout}s: {e}")
                raise VeoTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except VeoAuthError:
                raise

            except httpx.HTTPStatusError as e:
                logger.error(f"❌ HTTP error {e.response.status_code}: {e.response.text}")
                raise VeoAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                logger.error(f"❌ Request error: {e}")
                raise VeoAPIError(message=str(e)) from e

    # Convenience methods for specific endpoints
    async def generate_video(self, **kwargs: Any) -> dict[str, Any]:
        """Generate video using the videos endpoint."""
        logger.info(f"🎬 Generating video with action: {kwargs.get('action', 'text2video')}")
        return await self.request("/veo/videos", kwargs)

    async def get_1080p(self, video_id: str) -> dict[str, Any]:
        """Get 1080p version of a video."""
        logger.info(f"📺 Getting 1080p video for: {video_id}")
        return await self.request("/veo/videos", {"action": "get1080p", "video_id": video_id})

    async def query_task(self, **kwargs: Any) -> dict[str, Any]:
        """Query task status using the tasks endpoint."""
        task_id = kwargs.get("id") or kwargs.get("ids", [])
        logger.info(f"🔍 Querying task(s): {task_id}")
        return await self.request("/veo/tasks", kwargs)


# Global client instance
client = VeoClient()

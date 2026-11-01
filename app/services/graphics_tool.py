# app/services/video_tool.py
import os
from dataclasses import dataclass


@dataclass
class VideoToolConfig:
    provider: str = os.getenv("VIDEO_PROVIDER", "kling")
    api_key: str | None = os.getenv("VIDEO_PROVIDER_API_KEY")
    api_url: str | None = os.getenv("VIDEO_PROVIDER_URL")
    default_resolution: str = os.getenv("VIDEO_RESOLUTION", "1080x1920")
    default_duration_seconds: int = int(os.getenv("VIDEO_DURATION_SECONDS", "30"))
    enabled: bool = bool(os.getenv("VIDEO_PROVIDER_API_KEY"))


class VideoToolAdapter:
    def __init__(self, config: VideoToolConfig | None = None):
        self.config = config or VideoToolConfig()

    def is_ready(self) -> bool:
        return self.config.enabled and bool(self.config.api_key) and bool(self.config.api_url)

    def create_request(self, prompt: str, product_name: str) -> dict:
        return {
            "provider": self.config.provider,
            "product_name": product_name,
            "prompt": prompt,
            "resolution": self.config.default_resolution,
            "duration_seconds": self.config.default_duration_seconds,
            "mode": "commercial_ad",
        }

    def submit(self, prompt: str, product_name: str) -> dict:
        payload = self.create_request(prompt, product_name)
        if not self.is_ready():
            return {
                "status": "not_configured",
                "provider": self.config.provider,
                "message": "Add VIDEO_PROVIDER_API_KEY and VIDEO_PROVIDER_URL to enable the live video tool.",
                "request": payload,
            }

        import httpx

        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

        try:
            response = httpx.post(self.config.api_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            return {
                "status": "queued",
                "provider": self.config.provider,
                "request": payload,
                "provider_response": response.json(),
            }
        except Exception as exc:
            return {
                "status": "error",
                "provider": self.config.provider,
                "message": str(exc),
                "request": payload,
            }

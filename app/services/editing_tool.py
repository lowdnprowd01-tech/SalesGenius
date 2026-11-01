# app/services/graphics_tool.py
import os
from dataclasses import dataclass


@dataclass
class GraphicsToolConfig:
    provider: str = os.getenv("GRAPHICS_PROVIDER", "midjourney")
    api_key: str | None = os.getenv("GRAPHICS_PROVIDER_API_KEY")
    api_url: str | None = os.getenv("GRAPHICS_PROVIDER_URL")
    aspect_ratio: str = os.getenv("GRAPHICS_ASPECT_RATIO", "9:16")
    enabled: bool = bool(os.getenv("GRAPHICS_PROVIDER_API_KEY"))


class GraphicsToolAdapter:
    def __init__(self, config: GraphicsToolConfig | None = None):
        self.config = config or GraphicsToolConfig()

    def is_ready(self) -> bool:
        return self.config.enabled and bool(self.config.api_key) and bool(self.config.api_url)

    def create_request(self, prompt: str, product_name: str) -> dict:
        return {
            "provider": self.config.provider,
            "product_name": product_name,
            "prompt": prompt,
            "aspect_ratio": self.config.aspect_ratio,
            "style": "premium cinematic ad design",
            "mode": "hero_visual",
        }

    def submit(self, prompt: str, product_name: str) -> dict:
        payload = self.create_request(prompt, product_name)
        if not self.is_ready():
            return {
                "status": "not_configured",
                "provider": self.config.provider,
                "message": "Add GRAPHICS_PROVIDER_API_KEY and GRAPHICS_PROVIDER_URL to enable the live graphics tool.",
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

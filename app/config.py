# app/config.py
from pydantic import BaseModel, Field
from typing import Optional


class AppSettings(BaseModel):
    app_name: str = "SalesGenius Creative Agent"
    environment: str = "development"
    dry_run: bool = True
    auto_publish: bool = False
    enable_kill_switch: bool = True

    video_provider: str = "kling"
    video_provider_api_key: Optional[str] = None
    video_provider_url: Optional[str] = None
    video_resolution: str = "1080x1920"
    video_duration_seconds: int = 30

    graphics_provider: str = "midjourney"
    graphics_provider_api_key: Optional[str] = None
    graphics_provider_url: Optional[str] = None
    graphics_aspect_ratio: str = "9:16"

    editing_provider: str = "premiere_pro"
    editing_enabled: bool = False

    class Config:
        arbitrary_types_allowed = True

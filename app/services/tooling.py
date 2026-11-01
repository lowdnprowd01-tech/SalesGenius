from dataclasses import dataclass


@dataclass
class MotionToolConfig:
    provider: str = "kling"
    model: str = "standard"
    default_resolution: str = "1080x1920"


@dataclass
class GraphicsToolConfig:
    provider: str = "midjourney"
    style: str = "premium cinematic ad design"
    default_aspect: str = "9:16"


class VideoGenerationService:
    def __init__(self, config: MotionToolConfig | None = None):
        self.config = config or MotionToolConfig()

    def generate_video_prompt(self, storyboard: list[dict], product_name: str) -> str:
        scenes = "; ".join(scene["visual"] for scene in storyboard)
        return (
            f"Create a {self.config.default_resolution} vertical advertisement for {product_name}. "
            f"High-end commercial feel. Smooth cinematic movement. Premium lighting. "
            f"Scenes: {scenes}. Conversion-focused, polished, realistic product use."
        )


class GraphicsService:
    def __init__(self, config: GraphicsToolConfig | None = None):
        self.config = config or GraphicsToolConfig()

    def generate_graphics_prompt(self, product_name: str, audience: str, tone: str) -> str:
        return (
            f"Premium product advertisement concept for {product_name}. Audience: {audience}. "
            f"Style: {tone}, luxury, modern, clean, conversion-focused. "
            f"9:16 composition, bold typography, polished product mockup, premium lighting, sharp edges, high contrast."
        )


class EditingService:
    def __init__(self):
        pass

    def get_editing_notes(self) -> list[str]:
        return [
            "Use a strong 2-second hook immediately",
            "Keep product reveal within the first 5 seconds",
            "Use bold subtitles and minimal text overlay",
            "Use fast but not chaotic pacing",
            "End with a clear and direct CTA",
        ]

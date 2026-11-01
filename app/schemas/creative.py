from pydantic import BaseModel, Field


class CreativeRequest(BaseModel):
    product_name: str = Field(..., description="Name of the product or offer")
    description: str = Field(..., description="Full product description")
    audience: str = Field(default="general consumers", description="Target audience")
    tone: str = Field(default="premium", description="Brand tone")
    platform: str = Field(default="instagram", description="Target platform")
    duration_seconds: int = Field(default=30, ge=10, le=45)
    cta: str = Field(default="Shop now", description="Call to action")


class Shot(BaseModel):
    scene_number: int
    visual: str
    motion: str
    caption: str
    duration_seconds: int


class VideoScript(BaseModel):
    hook: str
    problem: str
    solution: str
    proof: str
    cta: str


class CreativeResponse(BaseModel):
    product_name: str
    platform: str
    duration_seconds: int
    script: VideoScript
    storyboard: list[Shot]
    video_prompt: str
    graphics_prompt: str
    editing_notes: list[str]

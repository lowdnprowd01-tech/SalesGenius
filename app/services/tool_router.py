from app.services.video_tool import VideoToolConfig, VideoToolAdapter
from app.services.graphics_tool import GraphicsToolConfig, GraphicsToolAdapter
from app.services.editing_tool import EditingToolConfig, EditingToolAdapter


class CreativeToolRouter:
    def __init__(
        self,
        video_config: VideoToolConfig | None = None,
        graphics_config: GraphicsToolConfig | None = None,
        editing_config: EditingToolConfig | None = None,
    ):
        self.video = VideoToolAdapter(video_config)
        self.graphics = GraphicsToolAdapter(graphics_config)
        self.editing = EditingToolAdapter(editing_config)

    def prepare(self, request, script, storyboard):
        video_prompt = (
            f"Create a premium {request.duration_seconds}-second social ad for {request.product_name}. "
            f"Hook: {script.hook}. Problem: {script.problem}. Solution: {script.solution}. CTA: {script.cta}. "
            f"Scenes: {'; '.join(s.visual for s in storyboard)}"
        )

        graphics_prompt = (
            f"Premium ad stills for {request.product_name}. Audience: {request.audience}. "
            f"Tone: {request.tone}. Hero product visual with luxury modern branding. "
            f"Use bold typography and a clean 9:16 composition. CTA: {script.cta}."
        )

        return {
            "video_request": self.video.create_request(video_prompt, request.product_name),
            "graphics_request": self.graphics.create_request(graphics_prompt, request.product_name),
            "editing_project": self.editing.create_project(request.product_name, [s.model_dump() for s in storyboard]),
        }

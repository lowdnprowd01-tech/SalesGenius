from app.services.script_generator import ScriptGenerator
from app.services.storyboard_generator import StoryboardGenerator
from app.services.prompt_builder import PromptBuilder
from app.services.quality_gate import QualityGate


class CreativeAgent:
    def __init__(self):
        self.script_generator = ScriptGenerator()
        self.storyboard_generator = StoryboardGenerator()
        self.prompt_builder = PromptBuilder()
        self.quality_gate = QualityGate()

    def generate(self, request):
        script = self.script_generator.generate(request)
        storyboard = self.storyboard_generator.generate(request, script)
        video_prompt = self.prompt_builder.build_video_prompt(request, script, storyboard)
        graphics_prompt = self.prompt_builder.build_graphics_prompt(request, script)
        quality = self.quality_gate.evaluate(script, storyboard)

        return {
            \"product_name\": request.product_name,
            \"platform\": request.platform,
            \"duration_seconds\": request.duration_seconds,
            \"script\": script.model_dump(),
            \"storyboard\": [shot.model_dump() for shot in storyboard],
            \"video_prompt\": video_prompt,
            \"graphics_prompt\": graphics_prompt,
            \"editing_notes\": quality[\"notes\"],
            \"quality_pass\": quality[\"pass\"],
            \"quality_checks\": quality[\"checks\"],
        }

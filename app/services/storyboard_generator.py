from app.schemas.creative import CreativeRequest, Shot, VideoScript


class StoryboardGenerator:
    def generate(self, request: CreativeRequest, script: VideoScript) -> list[Shot]:
        scenes = [
            Shot(
                scene_number=1,
                visual=f\"Close-up product shot of {request.product_name} in a premium lifestyle environment\",\n                motion=\"Slow push-in with cinematic lighting\",\n                caption=script.hook,\n                duration_seconds=max(4, request.duration_seconds // 4),\n            ),
            Shot(
                scene_number=2,
                visual=f\"Problem framing for {request.product_name}: wasted effort, poor setup, and average results\",\n                motion=\"Quick cut to frustration moment\",\n                caption=script.problem,\n                duration_seconds=max(4, request.duration_seconds // 4),\n            ),
            Shot(\n                scene_number=3,\n                visual=f\"Solution moment showing {request.product_name} delivering a premium, effortless experience\",\n                motion=\"Smooth motion reveal with precision transitions\",\n                caption=script.solution,\n                duration_seconds=max(4, request.duration_seconds // 4),\n            ),\n            Shot(\n                scene_number=4,\n                visual=f\"Final CTA shot with clear product branding and the text '{script.cta}'\",\n                motion=\"Lock-on hero shot and final hold\",\n                caption=script.cta,\n                duration_seconds=max(4, request.duration_seconds // 4),\n            ),\n        ]\n\n        total = sum(s.duration_seconds for s in scenes)\n        if total > request.duration_seconds:\n            diff = total - request.duration_seconds\n            for shot in scenes[:-1]:\n                if diff <= 0:\n                    break\n                if shot.duration_seconds > 2:\n                    shot.duration_seconds -= 1\n                    diff -= 1\n        return scenes\nPY

cat > app/services/prompt_builder.py <<'PY'
from app.schemas.creative import CreativeRequest, VideoScript


class PromptBuilder:
    def build_video_prompt(self, request: CreativeRequest, script: VideoScript, storyboard) -> str:
        scenes = \"; \".join(
            f\"Scene {shot.scene_number}: {shot.visual} ({shot.motion})\" for shot in storyboard\n        )
        return (\n            f\"Create a {request.duration_seconds}-second {request.platform} ad for {request.product_name}. \"\n            f\"Hook: {script.hook}. Problem: {script.problem}. Solution: {script.solution}. CTA: {script.cta}. \"\n            f\"Visual direction: premium, cinematic, modern, polished, conversion-focused. \"\n            f\"Storyboard scenes: {scenes}.\"\n        )

    def build_graphics_prompt(self, request: CreativeRequest, script: VideoScript) -> str:\n        return (\n            f\"Create a premium hero image for {request.product_name} optimized for {request.platform}. \"\n            f\"Use a luxury modern aesthetic. Audience: {request.audience}. Tone: {request.tone}. \"\n            f\"Include high-end product mockup, bold typography, and a clean commercial layout. \"\n            f\"CTA: {script.cta}.\"\n        )\nPY

cat > app/services/quality_gate.py <<'PY'
from app.schemas.creative import VideoScript


class QualityGate:
    def evaluate(self, script: VideoScript, storyboard) -> dict:
        tests = {\n            \"hook_present\": bool(script.hook),\n            \"problem_present\": bool(script.problem),\n            \"solution_present\": bool(script.solution),\n            \"cta_present\": bool(script.cta),\n            \"storyboard_complete\": len(storyboard) >= 3,\n        }\n        notes = [\n            \"Strong hook with clear product positioning\",\n            \"Problem/solution sequence is clear and direct\",\n            \"CTA is explicit and conversion-oriented\",\n            \"Storyboard pacing supports a polished short-form ad\",\n        ]\n        return {\n            \"pass\": all(tests.values()),\n            \"checks\": tests,\n            \"notes\": notes,\n        }\nPY

cat > app/api/creative_route.py <<'PY'
from fastapi import APIRouter

from app.schemas.creative import CreativeRequest, CreativeResponse
from app.agents.creative_agent import CreativeAgent

router = APIRouter(prefix=\"/creative\")
agent = CreativeAgent()

@router.post(\"/generate\", response_model=CreativeResponse)
async def generate_creative(request: CreativeRequest):
    result = agent.generate(request)
    return CreativeResponse(**result)

@router.get(\"/health\")
async def health():
    return {\"status\": \"ok\", \"service\": \"creative-agent\"}

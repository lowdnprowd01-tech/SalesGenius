from app.schemas.creative import CreativeRequest, VideoScript


class ScriptGenerator:
    def generate(self, request: CreativeRequest) -> VideoScript:
        return VideoScript(
            hook=f\"Meet {request.product_name}, the {request.tone} solution made for {request.audience}.\",
            problem=\"Most people waste time and money trying products that look good but do not actually work in real life.\",
            solution=f\"{request.product_name} is designed to make everyday results feel simple, premium, and reliable without the guesswork.\",
            proof=f\"Built for {request.platform} campaigns and optimized for busy customers who want instant clarity and results.\",
            cta=request.cta,
        )

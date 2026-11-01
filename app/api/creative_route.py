from fastapi import APIRouter

from app.schemas.creative import CreativeRequest, CreativeResponse
from app.agents.creative_agent import CreativeAgent

router = APIRouter(prefix="/creative")
agent = CreativeAgent()

@router.post("/generate", response_model=CreativeResponse)
async def generate_creative(request: CreativeRequest):
    result = agent.generate(request)
    return CreativeResponse(**result)

@router.get("/health")
async def health():
    return {"status": "ok", "service": "creative-agent"}

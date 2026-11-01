from fastapi import FastAPI

from app.auth.oauth_routes import router as auth_router
from app.agents.orchestrator import orchestrator_router

app = FastAPI(title="ProductOps AI")

app.include_router(auth_router)
app.include_router(orchestrator_router)

@app.get("/health")
async def health():
    return {"status": "ok"}

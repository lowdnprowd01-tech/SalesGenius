from fastapi import FastAPI

from app.auth.oauth_routes import router as auth_router
from app.api.creative_route import router as creative_router

app = FastAPI(title="SalesGenius Creative Agent")

app.include_router(auth_router)
app.include_router(creative_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "SalesGenius Creative Agent"}

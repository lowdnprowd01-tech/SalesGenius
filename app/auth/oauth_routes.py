from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/auth")


@router.get("/connect/{provider}")
async def connect_provider(provider: str):
    if provider not in ["meta", "shopify", "etsy", "tiktok", "youtube"]:
        raise HTTPException(status_code=404, detail="Provider not supported")
    return {
        "provider": provider,
        "auth_url": f"http://localhost:8000/auth/callback/{provider}",
        "message": "Use the provider OAuth flow and store the resulting token securely.",
    }


@router.get("/callback/{provider}")
async def oauth_callback(provider: str, code: str = Query(...)):
    return {
        "provider": provider,
        "status": "connected",
        "code": code,
        "message": "In production, exchange this code for tokens and store them securely.",
    }

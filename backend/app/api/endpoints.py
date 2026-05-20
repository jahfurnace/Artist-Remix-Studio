from fastapi import APIRouter
from app.api import endpoints, audio, subscriptions

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

router.include_router(audio.router, prefix="/audio", tags=["audio"])
router.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])

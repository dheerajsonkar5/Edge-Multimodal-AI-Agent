from fastapi import APIRouter
from datetime import datetime

router = APIRouter(tags=["Health"])


@router.get("/")
def home():
    return {
        "project": "Edge Multimodal AI Agent",
        "status": "Running",
        "time": str(datetime.now())
    }


@router.get("/health")
def health():
    return {
        "status": "healthy",
        "server": "online"
    }
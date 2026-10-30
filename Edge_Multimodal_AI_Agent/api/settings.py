from fastapi import APIRouter

router = APIRouter(tags=["Settings"])

settings = {
    "camera_index": 0,
    "confidence_threshold": 0.60,
    "capture_interval": 5,
    "enable_face": True,
    "enable_eye": True,
    "enable_person": True,
}


@router.get("/settings")
def get_settings():
    return settings


@router.put("/settings")
def update_settings(data: dict):

    settings.update(data)

    return {
        "message": "Settings Updated",
        "settings": settings
    }
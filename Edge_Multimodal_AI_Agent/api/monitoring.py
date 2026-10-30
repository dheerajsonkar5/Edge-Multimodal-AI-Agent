from fastapi import APIRouter
from datetime import datetime

router = APIRouter(tags=["Monitoring"])


@router.get("/monitor")
def monitor():

    return {

        "timestamp": str(datetime.now()),

        "camera": "Active",

        "person_detected": False,

        "face_detected": False,

        "eyes_open": False,

        "alert": False

    }
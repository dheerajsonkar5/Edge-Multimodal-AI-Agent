from fastapi import APIRouter
import threading

from main import monitor_service

router = APIRouter(tags=["Agent"])


@router.get("/start_agent")
def start_agent():

    if monitor_service.running:

        return {
            "status": "Already Running"
        }

    threading.Thread(
        target=monitor_service.start,
        daemon=True
    ).start()

    return {
        "status": "Monitoring Started"
    }


@router.get("/stop_agent")
def stop_agent():

    monitor_service.stop()

    return {
        "status": "Monitoring Stopped"
    }


@router.get("/status")
def status():

    return monitor_service.status()
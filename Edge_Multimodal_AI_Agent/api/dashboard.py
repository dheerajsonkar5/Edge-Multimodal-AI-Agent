from fastapi import APIRouter
import os
import platform
import psutil
import datetime

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

# -----------------------------
# Dashboard Home
# -----------------------------
@router.get("/")
def dashboard():

    return {

        "project": "Edge Multimodal AI Agent",

        "version": "2.0",

        "status": "Running",

        "timestamp": datetime.datetime.now(),

        "modules": {

            "Vision": True,

            "LLM": True,

            "Camera": True,

            "Reports": True,

            "Database": True

        }

    }


# -----------------------------
# System Information
# -----------------------------
@router.get("/system")
def system_information():

    memory = psutil.virtual_memory()

    disk = psutil.disk_usage("/")

    cpu = psutil.cpu_percent(interval=1)

    return {

        "Operating System": platform.system(),

        "Release": platform.release(),

        "Processor": platform.processor(),

        "Python Version": platform.python_version(),

        "CPU Usage (%)": cpu,

        "RAM Total (GB)": round(memory.total / (1024**3),2),

        "RAM Used (%)": memory.percent,

        "Disk Total (GB)": round(disk.total/(1024**3),2),

        "Disk Used (%)": disk.percent

    }


# -----------------------------
# Monitoring Statistics
# -----------------------------
@router.get("/stats")
def statistics():

    reports = 0
    snapshots = 0
    logs = 0

    if os.path.exists("reports"):
        reports = len(os.listdir("reports"))

    if os.path.exists("snapshots"):
        snapshots = len(os.listdir("snapshots"))

    if os.path.exists("logs"):
        logs = len(os.listdir("logs"))

    return {

        "Reports": reports,

        "Snapshots": snapshots,

        "Logs": logs,

        "Faces Detected": 0,

        "Persons Detected": 0,

        "Objects Detected": 0,

        "Alerts": 0

    }


# -----------------------------
# Live Status
# -----------------------------
@router.get("/live")
def live_status():

    return {

        "Camera": "Ready",

        "Detection Engine": "Running",

        "Face Detection": True,

        "Eye Detection": True,

        "Person Detection": True,

        "Pose Detection": True,

        "Object Detection": True,

        "LLM": "Connected",

        "Ollama": "Available",

        "Workspace": "Monitoring"

    }


# -----------------------------
# Health Score
# -----------------------------
@router.get("/health")
def dashboard_health():

    cpu = psutil.cpu_percent()

    ram = psutil.virtual_memory().percent

    score = 100

    if cpu > 80:
        score -= 20

    if ram > 80:
        score -= 20

    return {

        "Health Score": score,

        "CPU": cpu,

        "RAM": ram,

        "Status": "Healthy" if score > 60 else "Warning"

    }
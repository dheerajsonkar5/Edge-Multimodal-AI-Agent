import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


class Settings:

    PROJECT_NAME = "Edge Multimodal AI Agent"

    VERSION = "1.0.0"

    DEBUG = os.getenv("DEBUG", "True") == "True"

    HOST = os.getenv("HOST", "127.0.0.1")

    PORT = int(os.getenv("PORT", 8000))

    CAMERA_INDEX = int(os.getenv("CAMERA_INDEX", 0))

    REPORT_PATH = BASE_DIR / "reports"

    SNAPSHOT_PATH = BASE_DIR / "snapshots"

    LOG_PATH = BASE_DIR / "logs"

    DATABASE = BASE_DIR / "database" / "workspace.db"

    OLLAMA_URL = os.getenv(
        "OLLAMA_URL",
        "http://localhost:11434"
    )

    OLLAMA_MODEL = os.getenv(
        "OLLAMA_MODEL",
        "llama3.2:latest"
    )

    #FACE_MODEL = BASE_DIR / "models" / "haarcascade_frontalface_default.xml"

    #EYE_MODEL = BASE_DIR / "models" / "haarcascade_eye.xml"

    FACE_SCALE = 1.1

    FACE_NEIGHBORS = 5

    EYE_SCALE = 1.1

    EYE_NEIGHBORS = 5


settings = Settings()
from fastapi import APIRouter
from pathlib import Path

router = APIRouter(tags=["Reports"])

REPORT_DIR = Path("reports")


@router.get("/reports")
def reports():

    REPORT_DIR.mkdir(exist_ok=True)

    files = []

    for file in REPORT_DIR.iterdir():

        if file.is_file():

            files.append(file.name)

    return {

        "total_reports": len(files),

        "reports": files

    }
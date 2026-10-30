from fastapi import APIRouter
from dashboard.charts import DashboardCharts
from dashboard.widgets import DashboardWidgets

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

charts = DashboardCharts()
widgets = DashboardWidgets()


@router.get("/")
def home():
    return {
        "dashboard": "Edge Multimodal AI Agent",
        "version": "2.0",
        "status": "running"
    }


@router.get("/stats")
def stats():

    return {
        "widgets": widgets.summary(),
        "charts": charts.summary()
    }


@router.get("/live")
def live():

    return {
        "people": widgets.people_count,
        "faces": widgets.face_count,
        "alerts": widgets.alerts,
        "camera_status": "Active"
    }


@router.get("/alerts")
def alerts():

    return {
        "total_alerts": widgets.alerts,
        "today": widgets.today_alerts()
    }
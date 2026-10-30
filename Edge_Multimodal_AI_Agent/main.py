"""
=========================================================
Edge Multimodal AI Agent - COMPLETE WORKING VERSION
Smart Workspace Security using Local Vision Language Models
Author : Dheeraj Sonkar
Python : 3.11
=========================================================
"""
import cv2
import threading
import time
import os
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, HTMLResponse, JSONResponse

# -----------------------------
# Core
# -----------------------------
from core.logger import get_logger
from core.config import settings

# -----------------------------
# Services
# -----------------------------
from services.camera_service import CameraService
from services.monitor_service import MonitorService
from services.alert_service import AlertService
from services.report_service import ReportService

# -----------------------------
# Database
# -----------------------------
from database.sqlite import Database

# -----------------------------
# Vision
# -----------------------------
from vision.frame_processor import FrameProcessor

# -----------------------------
# LLM
# -----------------------------
from llm.reasoning import WorkspaceReasoning

# =====================================================
# Logger
# =====================================================
logger = get_logger()

# =====================================================
# Global Objects
# =====================================================
camera_service = CameraService()
frame_processor = FrameProcessor()
alert_service = AlertService()
report_service = ReportService()
database = Database()
reasoning_engine = WorkspaceReasoning()

monitor_service = MonitorService(
    camera_service=camera_service,
    frame_processor=frame_processor,
    alert_service=alert_service,
    report_service=report_service,
    database=database,
    reasoning_engine=reasoning_engine,
)

# =====================================================
# Global State
# =====================================================
AGENT_RUNNING = False
monitor_thread = None
current_frame = None
current_events = []
frame_lock = threading.Lock()
latest_results = {}

# =====================================================
# FastAPI App
# =====================================================
app = FastAPI(
    title="Edge Multimodal AI Agent",
    description="AI Powered Smart Workspace Monitoring with Face, Eye, Fatigue Detection",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# ROOT API
# =====================================================
@app.get("/")
def home():
    return {
        "project": "Edge Multimodal AI Agent",
        "version": "1.0",
        "status": "Running",
        "docs": "/docs",
        "dashboard": "/dashboard/",
        "author": "Dheeraj Sonkar"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy" if camera_service.is_open() else "degraded",
        "camera": camera_service.is_open(),
        "agent": AGENT_RUNNING,
        "timestamp": datetime.now().isoformat()
    }

# =====================================================
# BACKGROUND MONITORING THREAD
# =====================================================
def monitoring_loop():
    global AGENT_RUNNING, current_frame, current_events, latest_results
    
    logger.info("Monitoring thread started.")
    
    while AGENT_RUNNING:
        try:
            frame = camera_service.read_frame()
            
            if frame is None:
                time.sleep(0.03)
                continue
            
            processed_frame, result = frame_processor.process_frame(frame)
            
            with frame_lock:
                current_frame = processed_frame if processed_frame is not None else frame
                if result:
                    current_events = result.get("events", [])
                    latest_results = result
            
            if result:
                try:
                    monitor_service.update(result)
                except:
                    pass
            
        except Exception as e:
            logger.error(f"Monitoring Error: {e}")
        
        time.sleep(0.03)
    
    logger.info("Monitoring thread stopped.")

# =====================================================
# VIDEO FEED
# =====================================================
@app.get("/video_feed")
async def video_feed():
    def generate():
        while True:
            with frame_lock:
                frame = current_frame
            
            if frame is not None:
                try:
                    _, buffer = cv2.imencode('.jpg', frame)
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + 
                           buffer.tobytes() + b'\r\n')
                except:
                    pass
            time.sleep(0.05)
    
    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace; boundary=frame")

# =====================================================
# AGENT APIs
# =====================================================
@app.get("/start_agent")
def start_agent():
    global AGENT_RUNNING, monitor_thread
    
    if AGENT_RUNNING:
        return {"success": True, "message": "Agent already running."}
    
    try:
        camera_service.open()
        logger.info("Camera opened successfully")
    except Exception as e:
        logger.error(f"Camera open failed: {e}")
        return {"success": False, "message": str(e)}
    
    AGENT_RUNNING = True
    monitor_thread = threading.Thread(target=monitoring_loop, daemon=True)
    monitor_thread.start()
    
    logger.info("AI Agent Started Successfully!")
    return {"success": True, "message": "Agent Started Successfully!"}

@app.get("/stop_agent")
def stop_agent():
    global AGENT_RUNNING
    
    if not AGENT_RUNNING:
        return {"success": True, "message": "Agent already stopped."}
    
    AGENT_RUNNING = False
    
    try:
        camera_service.release()
    except:
        pass
    
    logger.info("AI Agent Stopped.")
    return {"success": True, "message": "Agent Stopped Successfully!"}

@app.get("/status")
def status():
    with frame_lock:
        events_count = len(current_events)
        results = latest_results.copy()
    
    return {
        "success": True,
        "data": {
            "running": AGENT_RUNNING,
            "camera": camera_service.is_open(),
            "database": True,
            "reports": report_service.total_reports() if report_service else 0,
            "events": events_count,
            "latest_results": results,
            "timestamp": datetime.now().isoformat()
        }
    }

@app.get("/camera")
def camera_status():
    return {"camera_open": camera_service.is_open()}

@app.get("/ping")
def ping():
    return {"message": "Server Running", "timestamp": datetime.now().isoformat()}

# =====================================================
# SNAPSHOT
# =====================================================
@app.get("/snapshot")
def take_snapshot():
    try:
        with frame_lock:
            frame = current_frame
        
        if frame is None:
            frame = camera_service.read_frame()
        
        if frame is None:
            return {"success": False, "message": "No Camera Frame"}
        
        os.makedirs("snapshots", exist_ok=True)
        filename = f"snapshot_{int(time.time())}.jpg"
        path = os.path.join("snapshots", filename)
        cv2.imwrite(path, frame)
        
        logger.info(f"Snapshot saved: {path}")
        return {"success": True, "snapshot": path}
    except Exception as e:
        logger.error(f"Snapshot error: {e}")
        return {"success": False, "error": str(e)}

# =====================================================
# REPORT GENERATION
# =====================================================
@app.get("/generate_report")
def generate_report():
    try:
        with frame_lock:
            events = latest_results.get("events", []) if latest_results else []
            if not events:
                events = current_events.copy() if current_events else []
        
        logger.info(f"Generating report with {len(events)} events")
        
        report_path = report_service.generate(events=events, format="json")
        
        if report_path:
            logger.info(f"Report generated: {report_path}")
            return {
                "success": True, 
                "report": report_path,
                "events_count": len(events),
                "message": f"Report generated with {len(events)} events"
            }
        else:
            return {
                "success": False, 
                "error": "Report generation failed"
            }
    except Exception as e:
        logger.error(f"Report generation error: {e}")
        return {"success": False, "error": str(e)}

# =====================================================
# GET REPORTS LIST
# =====================================================
@app.get("/reports")
def get_reports():
    try:
        reports = report_service.list_reports() if report_service else []
        return {"success": True, "reports": reports, "count": len(reports)}
    except Exception as e:
        return {"success": False, "error": str(e)}

# =====================================================
# DASHBOARD - WOW UI
# =====================================================
@app.get("/dashboard/")
async def dashboard():
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Edge Multimodal AI Agent Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', 'Segoe UI', sans-serif;
            background: #0a0e17;
            color: #fff;
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        /* Animated Background */
        .bg-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            overflow: hidden;
        }
        .bg-animation .circle {
            position: absolute;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(102, 126, 234, 0.15), transparent 70%);
            animation: float 20s infinite ease-in-out;
        }
        .bg-animation .circle:nth-child(1) { width: 500px; height: 500px; top: -10%; left: -5%; animation-delay: 0s; }
        .bg-animation .circle:nth-child(2) { width: 400px; height: 400px; bottom: -10%; right: -5%; animation-delay: -7s; }
        .bg-animation .circle:nth-child(3) { width: 300px; height: 300px; top: 40%; right: 20%; animation-delay: -14s; }
        @keyframes float {
            0%, 100% { transform: translate(0, 0) scale(1); }
            33% { transform: translate(30px, -30px) scale(1.1); }
            66% { transform: translate(-20px, 20px) scale(0.9); }
        }
        
        .container {
            position: relative;
            z-index: 1;
            max-width: 1440px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* Glass Header */
        .header {
            background: rgba(26, 31, 46, 0.8);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.08);
            padding: 25px 35px;
            border-radius: 24px;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .header-left h1 {
            font-size: 1.8em;
            font-weight: 900;
            background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .header-left p {
            opacity: 0.6;
            font-weight: 300;
            -webkit-text-fill-color: #8899bb;
        }
        .header-badge {
            background: rgba(255,255,255,0.05);
            padding: 10px 25px;
            border-radius: 50px;
            border: 1px solid rgba(255,255,255,0.1);
            font-size: 0.8em;
            backdrop-filter: blur(10px);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .live-dot {
            display: inline-block;
            width: 10px;
            height: 10px;
            background: #f44336;
            border-radius: 50%;
            animation: pulse 1.5s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); box-shadow: 0 0 0 0 rgba(244,67,54,0.4); }
            50% { opacity: 0.5; transform: scale(0.8); box-shadow: 0 0 20px 5px rgba(244,67,54,0.2); }
        }
        
        /* Stats Grid */
        .grid {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }
        .card {
            background: rgba(26, 31, 46, 0.7);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255,255,255,0.06);
            padding: 20px;
            border-radius: 16px;
            text-align: center;
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            cursor: default;
            position: relative;
            overflow: hidden;
        }
        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(102,126,234,0.05), transparent);
            opacity: 0;
            transition: opacity 0.4s;
        }
        .card:hover::before { opacity: 1; }
        .card:hover {
            transform: translateY(-5px) scale(1.02);
            border-color: rgba(102,126,234,0.3);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }
        .card .value {
            font-size: 2.2em;
            font-weight: 800;
            transition: all 0.3s;
        }
        .card .label {
            color: #8899bb;
            margin-top: 5px;
            font-size: 0.75em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }
        .card .icon {
            font-size: 1.5em;
            margin-bottom: 5px;
            display: block;
        }
        .status-running { color: #4CAF50; }
        .status-stopped { color: #f44336; }
        .status-active { color: #4CAF50; }
        .status-inactive { color: #f44336; }
        
        /* Buttons */
        .flex {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin: 15px 0 20px;
            justify-content: center;
        }
        .btn {
            padding: 14px 32px;
            border: none;
            border-radius: 14px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.9em;
            font-family: 'Inter', sans-serif;
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            display: flex;
            align-items: center;
            gap: 10px;
            position: relative;
            overflow: hidden;
        }
        .btn::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255,255,255,0.2);
            transition: all 0.6s;
            transform: translate(-50%, -50%);
        }
        .btn:active::after {
            width: 300px;
            height: 300px;
        }
        .btn:hover {
            transform: translateY(-3px) scale(1.03);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .btn:active { transform: scale(0.95); }
        .btn-start { background: linear-gradient(135deg, #4CAF50, #2E7D32); color: white; }
        .btn-stop { background: linear-gradient(135deg, #f44336, #c62828); color: white; }
        .btn-snapshot { background: linear-gradient(135deg, #2196F3, #0D47A1); color: white; }
        .btn-report { background: linear-gradient(135deg, #FF9800, #E65100); color: white; }
        .btn-refresh { background: linear-gradient(135deg, #607D8B, #37474F); color: white; }
        
        /* Two Column */
        .two-col {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
        }
        .glass-card {
            background: rgba(26, 31, 46, 0.7);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 16px;
            overflow: hidden;
            transition: all 0.4s;
        }
        .glass-card:hover { border-color: rgba(102,126,234,0.2); }
        .glass-card .card-header {
            padding: 15px 20px;
            background: rgba(0,0,0,0.2);
            border-bottom: 1px solid rgba(255,255,255,0.05);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .glass-card .card-header h3 { font-weight: 600; font-size: 0.95em; }
        .glass-card .card-header span { opacity: 0.5; font-size: 0.8em; }
        .glass-card img { width: 100%; height: auto; display: block; }
        
        /* Events List */
        .events-list {
            max-height: 450px;
            overflow-y: auto;
            padding: 10px;
        }
        .events-list::-webkit-scrollbar { width: 4px; }
        .events-list::-webkit-scrollbar-track { background: rgba(255,255,255,0.03); border-radius: 10px; }
        .events-list::-webkit-scrollbar-thumb { background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 10px; }
        
        .event-item {
            padding: 12px 15px;
            margin-bottom: 8px;
            border-radius: 12px;
            background: rgba(255,255,255,0.03);
            border-left: 3px solid #667eea;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s;
        }
        .event-item:hover { background: rgba(255,255,255,0.06); }
        .event-item .time { font-size: 0.7em; opacity: 0.4; }
        
        .badge {
            padding: 4px 14px;
            border-radius: 50px;
            font-size: 0.65em;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .badge-high { background: #f44336; color: white; }
        .badge-medium { background: #FF9800; color: white; }
        .badge-low { background: #4CAF50; color: white; }
        .badge-info { background: #2196F3; color: white; }
        
        /* System Info */
        pre {
            background: rgba(0,0,0,0.4);
            padding: 15px;
            border-radius: 12px;
            overflow-x: auto;
            font-size: 0.7em;
            color: #8899bb;
            max-height: 200px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            border: 1px solid rgba(255,255,255,0.03);
            margin-top: 10px;
            line-height: 1.6;
        }
        
        /* Toast */
        .toast {
            position: fixed;
            top: 25px;
            right: 25px;
            padding: 16px 28px;
            border-radius: 14px;
            z-index: 9999;
            animation: slideIn 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            max-width: 420px;
            font-weight: 500;
            font-size: 0.9em;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            backdrop-filter: blur(20px);
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .toast-success { background: rgba(76, 175, 80, 0.9); color: white; border: 1px solid rgba(76,175,80,0.3); }
        .toast-error { background: rgba(244, 67, 54, 0.9); color: white; border: 1px solid rgba(244,67,54,0.3); }
        .toast-info { background: rgba(33, 150, 243, 0.9); color: white; border: 1px solid rgba(33,150,243,0.3); }
        @keyframes slideIn {
            from { transform: translateX(100%) scale(0.9); opacity: 0; }
            to { transform: translateX(0) scale(1); opacity: 1; }
        }
        
        .empty-state {
            color: #8899bb;
            padding: 30px;
            text-align: center;
            font-size: 0.9em;
        }
        .empty-state i { font-size: 2em; display: block; margin-bottom: 10px; opacity: 0.3; }
        
        /* Responsive */
        @media (max-width: 992px) {
            .two-col { grid-template-columns: 1fr; }
            .grid { grid-template-columns: repeat(3, 1fr); }
        }
        @media (max-width: 600px) {
            .grid { grid-template-columns: repeat(2, 1fr); }
            .header { flex-direction: column; text-align: center; gap: 15px; }
            .header-left h1 { font-size: 1.3em; }
            .btn { padding: 12px 20px; font-size: 0.8em; }
        }
    </style>
</head>
<body>
    <div class="bg-animation">
        <div class="circle"></div>
        <div class="circle"></div>
        <div class="circle"></div>
    </div>
    
    <div class="container">
        <div class="header">
            <div class="header-left">
                <h1><i class="fas fa-brain" style="-webkit-text-fill-color: #667eea;"></i> Edge AI Agent</h1>
                <p>Smart Workspace Monitoring · Face · Eye · Fatigue Detection</p>
            </div>
            <div class="header-badge">
                <span class="live-dot"></span>
                <span id="liveStatus">LIVE</span>
                <span style="opacity:0.4;margin:0 5px;">|</span>
                <span id="timeDisplay"></span>
            </div>
        </div>
        
        <div class="grid" id="stats">
            <div class="card">
                <span class="icon"><i class="fas fa-microchip"></i></span>
                <div class="value" id="status_val">⏹️</div>
                <div class="label">Agent Status</div>
            </div>
            <div class="card">
                <span class="icon"><i class="fas fa-video"></i></span>
                <div class="value" id="camera_val">📷</div>
                <div class="label">Camera</div>
            </div>
            <div class="card">
                <span class="icon"><i class="fas fa-user"></i></span>
                <div class="value" id="faces_val">0</div>
                <div class="label">Faces</div>
            </div>
            <div class="card">
                <span class="icon"><i class="fas fa-users"></i></span>
                <div class="value" id="persons_val">0</div>
                <div class="label">Persons</div>
            </div>
            <div class="card">
                <span class="icon"><i class="fas fa-bell"></i></span>
                <div class="value" id="events_val">0</div>
                <div class="label">Events</div>
            </div>
            <div class="card">
                <span class="icon"><i class="fas fa-bolt"></i></span>
                <div class="value" id="fatigue_val">0%</div>
                <div class="label">Fatigue</div>
            </div>
        </div>
        
        <div class="flex">
            <button class="btn btn-start" onclick="startAgent()"><i class="fas fa-play"></i> Start</button>
            <button class="btn btn-stop" onclick="stopAgent()"><i class="fas fa-stop"></i> Stop</button>
            <button class="btn btn-snapshot" onclick="takeSnapshot()"><i class="fas fa-camera"></i> Snapshot</button>
            <button class="btn btn-report" onclick="generateReport()"><i class="fas fa-file-alt"></i> Report</button>
            <button class="btn btn-refresh" onclick="refreshStatus()"><i class="fas fa-sync-alt"></i> Refresh</button>
        </div>
        
        <div class="two-col">
            <div class="glass-card">
                <div class="card-header">
                    <h3><i class="fas fa-eye" style="color:#667eea;"></i> Live Camera Feed</h3>
                    <span>Range: Up to 5m</span>
                </div>
                <img id="videoFeed" src="/video_feed" style="width:100%;" onerror="this.style.display='none'">
            </div>
            <div class="glass-card">
                <div class="card-header">
                    <h3><i class="fas fa-list-ul" style="color:#764ba2;"></i> Recent Events</h3>
                    <span id="eventCount">0</span>
                </div>
                <div class="events-list" id="events_list">
                    <div class="empty-state"><i class="fas fa-inbox"></i>No events yet</div>
                </div>
            </div>
        </div>
        
        <div class="glass-card" style="margin-top:20px;padding:20px;">
            <h3 style="margin-bottom:10px;"><i class="fas fa-code" style="color:#f093fb;"></i> System Info</h3>
            <pre id="system_info">Loading...</pre>
        </div>
    </div>
    
    <script>
        function updateTime() {
            var now = new Date();
            document.getElementById('timeDisplay').textContent = now.toLocaleTimeString();
        }
        setInterval(updateTime, 1000);
        updateTime();
        
        function showToast(message, type) {
            type = type || 'success';
            var toast = document.createElement('div');
            toast.className = 'toast toast-' + type;
            var icon = type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️';
            toast.innerHTML = '<span>' + icon + '</span> ' + message;
            document.body.appendChild(toast);
            setTimeout(function() { toast.remove(); }, 4000);
        }
        
        async function fetchAPI(url) {
            try {
                var resp = await fetch(url, { cache: 'no-store' });
                return await resp.json();
            } catch(e) {
                showToast('Error: ' + e.message, 'error');
                return { success: false };
            }
        }
        
        async function refreshStatus() {
            try {
                var resp = await fetch('/status', { cache: 'no-store' });
                var data = await resp.json();
                var d = data.data || {};
                var latest = d.latest_results || {};
                
                var statusEl = document.getElementById('status_val');
                statusEl.textContent = d.running ? 'Running' : 'Stopped';
                statusEl.style.color = d.running ? '#4CAF50' : '#f44336';
                
                var camEl = document.getElementById('camera_val');
                camEl.textContent = d.camera ? 'Active' : 'Inactive';
                camEl.style.color = d.camera ? '#4CAF50' : '#f44336';
                
                document.getElementById('events_val').textContent = d.events || 0;
                document.getElementById('faces_val').textContent = latest.faces || 0;
                document.getElementById('persons_val').textContent = latest.persons || 0;
                document.getElementById('fatigue_val').textContent = latest.fatigue_level ? Math.round(latest.fatigue_level) + '%' : '0%';
                document.getElementById('eventCount').textContent = (latest.events || []).length;
                
                var events = latest.events || [];
                var eventsDiv = document.getElementById('events_list');
                if (!events || events.length === 0) {
                    eventsDiv.innerHTML = '<div class="empty-state"><i class="fas fa-inbox"></i>No events yet</div>';
                } else {
                    var html = '';
                    for (var i = events.length - 1; i >= 0 && i >= events.length - 10; i--) {
                        var e = events[i];
                        var badgeClass = e.severity || 'info';
                        html += '<div class="event-item">' +
                            '<span><span style="color:#667eea;font-weight:600;">' + (e.type || 'event') + '</span> ' + (e.description || '') + '</span>' +
                            '<span class="badge badge-' + badgeClass + '">' + badgeClass + '</span>' +
                        '</div>';
                    }
                    eventsDiv.innerHTML = html;
                }
                
                document.getElementById('system_info').textContent = JSON.stringify({
                    running: d.running,
                    camera: d.camera,
                    events: d.events,
                    faces: latest.faces,
                    persons: latest.persons,
                    fatigue: latest.fatigue_level,
                    timestamp: new Date().toISOString()
                }, null, 2);
            } catch(e) {
                console.error('Refresh error:', e);
            }
        }
        
        async function startAgent() {
            showToast('Starting agent...', 'info');
            var result = await fetchAPI('/start_agent');
            if (result.success) {
                showToast(result.message, 'success');
            } else {
                showToast(result.message, 'error');
            }
            setTimeout(refreshStatus, 1000);
        }
        
        async function stopAgent() {
            showToast('Stopping agent...', 'info');
            var result = await fetchAPI('/stop_agent');
            if (result.success) {
                showToast(result.message, 'success');
            } else {
                showToast(result.message, 'error');
            }
            setTimeout(refreshStatus, 1000);
        }
        
        async function takeSnapshot() {
            showToast('Taking snapshot...', 'info');
            var result = await fetchAPI('/snapshot');
            if (result.success) {
                showToast('Snapshot: ' + result.snapshot, 'success');
            } else {
                showToast(result.message, 'error');
            }
            setTimeout(refreshStatus, 1000);
        }
        
        async function generateReport() {
            showToast('Generating report...', 'info');
            var result = await fetchAPI('/generate_report');
            if (result.success) {
                showToast('Report: ' + result.report, 'success');
            } else {
                showToast(result.error, 'error');
            }
            setTimeout(refreshStatus, 1000);
        }
        
        refreshStatus();
        setInterval(refreshStatus, 3000);
    </script>
</body>
</html>"""
    return HTMLResponse(html)

# =====================================================
# MAIN
# =====================================================
if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🚀 Edge Multimodal AI Agent - FINAL WORKING!")
    print("=" * 60)
    print(f"📁 Server: http://127.0.0.1:8000")
    print(f"📚 Swagger: http://127.0.0.1:8000/docs")
    print(f"📊 Dashboard: http://127.0.0.1:8000/dashboard/")
    print("=" * 60)
    print("✅ Features: Face Detection | Eye Tracking | Fatigue Detection")
    print("✅ Object Detection | Person Detection | Report Generation")
    print("=" * 60)
    print("Press CTRL+C to stop")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
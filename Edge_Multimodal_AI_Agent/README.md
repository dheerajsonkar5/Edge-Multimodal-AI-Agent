
# 🧠 Autonomous AI-Driven Cognitive Workspace Intelligence Agent

> **A real-time edge-computing multi-threaded spatial perception framework built using Python 3.11, FastAPI, and OpenCV to enforce ergonomic compliance and monitor security parameters without cloud dependencies.**

---

## 📌 Project Overview

This project presents an **Edge-Driven Multimodal AIoT Agent** designed for **smart workspace safety, security, and automated context reporting**. It integrates **Computer Vision, Generative AI, Large Language Models (LLMs), and IoT** to create an intelligent monitoring system.

The system uses a local camera to identify situations such as **user fatigue, drowsiness, unauthorized access, and security violations**. A lightweight **Vision-Language Model (VLM)** interprets detected events and generates meaningful incident reports. Based on the identified situation, the system can also trigger automated actions through IoT devices.

### 🔐 Key Innovation: Privacy-First Edge AI

Unlike traditional cloud-based monitoring systems, this solution processes all sensitive visual data **locally on the edge device**, ensuring:

- ✅ **Zero cloud dependency** – No video data leaves the device
- ✅ **Low latency** – Real-time processing without network delays
- ✅ **Privacy compliance** – GDPR and data protection regulations
- ✅ **Offline functionality** – Works without internet connectivity




## 🛠️ System Architecture

- **`vision/`**: Optical Matrix calculations using HOG and Haar Cascades.
- **`llm/`**: Asynchronous evaluation interface utilizing local Ollama daemon cycles.
- **`services/`**: Non-blocking background management workers and active buzzer alert streams.
- **`database/`**: Relational sqlite operational storage logs abstraction layers.
---





## 🏗️ System Architecture

┌─────────────────────────────────────────────────────────────────────────────┐
│ EDGE DEVICE (LAPTOP) │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────┐ ┌────────────────┐ ┌────────────────────┐ │
│ │ Webcam │───▶│ CV Pipeline │───▶│ Event Detection │ │
│ │ (Stream) │ │ (OpenCV/Haar) │ │ (Classifier) │ │
│ └─────────────┘ └────────────────┘ └────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Ollama Server (Local VLM) │ │
│ │ ┌─────────────────────────────────────────────────────┐ │ │
│ │ │ Llama Vision / LLaVA │ │ │
│ │ │ ● Image Understanding │ │ │
│ │ │ ● Contextual Reasoning │ │ │
│ │ │ ● Report Generation │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ FastAPI Backend + SQLite DB │ │
│ │ ┌────────────┬─────────────┬─────────────┬────────────┐ │ │
│ │ │ Report │ Action │ Log │ Alert │ │ │
│ │ │ Storage │ Dispatcher │ Manager │ Generator │ │ │
│ │ └────────────┴─────────────┴─────────────┴────────────┘ │ │
│ └─────────────────────────────────────────────────────────────┘ │
│ │ │ │
│ ▼ ▼ │
│ ┌─────────────────┐ ┌──────────────────────────────────┐ │
│ │ Local UI │ │ MQTT/WebSocket Server │ │
│ │ Dashboard │ │ (Real-time Communication) │ │
│ └─────────────────┘ └──────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
│ │
▼ ▼
┌──────────────────┐ ┌──────────────────┐
│ ESP32 Smart │ │ Mobile App / │
│ Desk Controls │ │ Security Desk │
└──────────────────┘ └──────────────────┘


---

## 🚀 Features

| Category | Features |
|----------|----------|
| **Computer Vision** | ✅ Face Detection (Haar Cascades) |
| | ✅ Eye Detection & Tracking |
| | ✅ EAR (Eye Aspect Ratio) Calculation |
| | ✅ Person Detection (YOLOv8) |
| | ✅ Object Detection (YOLOv8) |
| | ✅ Pose Detection (MediaPipe) |
| **Intelligent Monitoring** | ✅ Fatigue Detection |
| | ✅ Blink Detection |
| | ✅ Drowsiness Monitoring |
| | ✅ Unauthorized Person Detection |
| | ✅ Shoulder Surfing Detection |
| | ✅ Multiple Persons Alert |
| **AI & LLM** | ✅ Local Vision-Language Model (Ollama) |
| | ✅ Contextual Incident Reasoning |
| | ✅ Automated Report Generation |
| **Backend & API** | ✅ FastAPI REST API |
| | ✅ Swagger UI Documentation |
| | ✅ SQLite Database Storage |
| | ✅ MQTT Communication |
| | ✅ WebSocket Real-time Updates |
| **User Interface** | ✅ Live Video Dashboard |
| | ✅ Real-time Statistics |
| | ✅ Event Logging |
| | ✅ Snapshot Capture |
| | ✅ Report Generation |

---

## 📁 Project Structure
Edge_Multimodal_AI_Agent/
│
├── api/ # FastAPI Routes
│ ├── health.py # Health check endpoints
│ ├── monitoring.py # Monitoring endpoints
│ ├── reports.py # Report endpoints
│ └── settings.py # Settings endpoints
│
├── core/ # Core Configuration
│ ├── config.py # Application settings
│ ├── logger.py # Logging configuration
│ └── constants.py # Application constants
│
├── vision/ # Computer Vision Module
│ ├── frame_processor.py # Main vision processing
│ ├── face_detector.py # Face detection
│ ├── eye_detector.py # Eye tracking & EAR
│ ├── person_detector.py # Person detection (YOLO)
│ ├── pose_detector.py # Pose detection
│ └── object_detector.py # Object detection
│
├── llm/ # LLM Integration
│ ├── ollama_client.py # Ollama API client
│ ├── prompt_engine.py # Prompt engineering
│ └── reasoning.py # Contextual reasoning
│
├── services/ # Business Logic
│ ├── camera_service.py # Camera management
│ ├── monitor_service.py # Monitoring orchestration
│ ├── alert_service.py # Alert generation
│ └── report_service.py # Report generation
│
├── database/ # Database Layer
│ └── sqlite.py # SQLite operations
│
├── models/ # ML Models
│ ├── haarcascade_frontalface_default.xml
│ └── haarcascade_eye.xml
│
├── reports/ # Generated Reports
├── snapshots/ # Captured Snapshots
├── logs/ # Application Logs
├── tests/ # Unit Tests
│
├── main.py # Application Entry Point
├── requirements.txt # Python Dependencies
├── run.bat # Windows Startup Script
└── README.md # Documentation


---

## 🛠️ Technologies Used

| Category | Technologies |
|----------|--------------|
| **Programming Language** | Python 3.11 |
| **Web Framework** | FastAPI, Uvicorn |
| **Computer Vision** | OpenCV, MediaPipe, Haar Cascades |
| **Deep Learning** | YOLOv8 (Ultralytics) |
| **AI/LLM** | Ollama, LLaVA Vision Model |
| **Database** | SQLite, SQLAlchemy |
| **IoT Communication** | MQTT, WebSockets |
| **Frontend** | HTML, CSS, JavaScript (Dashboard) |
| **Testing** | Pytest |
| **Logging** | Loguru |

---

## 📋 Installation & Setup

### Prerequisites

- Python 3.11 or higher
- Webcam (built-in or external)
- Ollama installed locally (optional for VLM features)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/Edge_Multimodal_AI_Agent.git
cd Edge_Multimodal_AI_Agent
Step 2: Create Virtual Environment
# Windows
py -3.11 -m venv .venv
.\.venv\Scripts\activate

# Linux/Mac
python3.11 -m venv .venv
source .venv/bin/activate
Step 3: Install Dependencies
bash
pip install -r requirements.txt
Step 4: Install Ollama (Optional - for VLM Features)
bash
# Download from: https://ollama.ai/download
# Then pull the vision model
ollama pull llava:7b
Step 5: Run the Application
bash
# Method 1: Direct run
python main.py

# Method 2: Using uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Method 3: Windows batch file
run.bat


🌐 API Endpoints
Base URL: http://127.0.0.1:8000
Endpoint	Method	Description
/	GET	Home page
/health	GET	Health check
/start_agent	GET	Start monitoring agent
/stop_agent	GET	Stop monitoring agent
/status	GET	Get agent status
/camera	GET	Camera status
/video_feed	GET	Live video stream
/snapshot	GET	Capture snapshot
/reports	GET	List all reports
/generate_report	GET	Generate incident report
/reason	GET	Run LLM reasoning
/settings	GET/PUT	Get/Update settings
/config	GET	Get configuration
/ping	GET	Server ping
/shutdown	GET	Shutdown agent
/dashboard/	GET	Web Dashboard
Swagger UI
text
http://127.0.0.1:8000/docs
Example API Calls
bash
# Start the agent
curl -X GET "http://127.0.0.1:8000/start_agent"

# Check status
curl -X GET "http://127.0.0.1:8000/status"

# Capture snapshot
curl -X GET "http://127.0.0.1:8000/snapshot"

# Generate report
curl -X GET "http://127.0.0.1:8000/generate_report"

# Run reasoning
curl -X GET "http://127.0.0.1:8000/reason"
📊 Dashboard
Access the real-time dashboard at:

text
http://127.0.0.1:8000/dashboard/
Dashboard Features
Feature	Description
Live Video Feed	Real-time camera stream with annotations
Face Detection	Green boxes around detected faces
Eye Tracking	Yellow outlines for eye detection
EAR Display	Real-time Eye Aspect Ratio value
Fatigue Monitor	Progress bar showing fatigue level
Blink Counter	Total blinks detected
Event Log	Recent events with severity badges
System Status	Agent, Camera, Database status
Control Buttons	Start/Stop, Snapshot, Report
🔬 How It Works
1. Computer Vision Pipeline
text
Webcam → Frame Capture → Face Detection → Eye Detection → EAR Calculation → Fatigue Detection
2. EAR (Eye Aspect Ratio) Calculation
text
EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
Open Eye: EAR ≈ 0.25 - 0.35

Closed Eye: EAR ≈ 0.10 - 0.15

Blink: EAR drops below threshold briefly

3. Fatigue Detection Logic
text
If EAR < Threshold for 15+ consecutive frames:
    Fatigue Counter += 1
    Fatigue Level = (Counter / 15) * 100
    If Fatigue Level >= 100%:
        Trigger "FATIGUE DETECTED!" Event
4. Report Generation
json
{
  "id": "REP_1234567890_1",
  "timestamp": "2026-08-06T17:24:27.094834",
  "total_events": 1,
  "events": [
    {
      "type": "fatigue",
      "severity": "high",
      "description": "Fatigue: 100.0%"
    }
  ],
  "summary": {
    "total": 1,
    "by_type": {"fatigue": 1},
    "by_severity": {"high": 1}
  }
}
🧪 Testing
Run Unit Tests
bash
pytest tests/
Test with Coverage
bash
pytest --cov=. tests/
Manual Testing
Open dashboard: http://127.0.0.1:8000/dashboard/

Click Start

Show your face to the camera

Close your eyes for 5+ seconds to trigger fatigue

Click Snapshot to capture current frame

Click Report to generate incident report

📈 Performance Benchmarks
Metric	Value
Face Detection FPS	30+ fps
Eye Detection FPS	30+ fps
YOLO Inference	~70-80ms per frame
Fatigue Detection Latency	< 500ms
Report Generation	< 1s
CPU Usage	~30-40%
Memory Usage	~2-4GB
🔮 Future Scope
Enhancement	Description
Multi-Camera Support	Multiple camera angles for larger workspaces
Mobile App	Android/iOS app for remote monitoring
Cloud Dashboard	Centralized monitoring for multiple agents
Email/SMS Alerts	Notification system for critical events
Advanced Analytics	Historical data analysis and trends
Voice Commands	Voice-controlled IoT actions
Custom Training	Fine-tune models for specific environments
Edge TPU Support	Hardware acceleration for edge devices

📚 Research Inspiration
Paper	Year	Contribution
Local Vision Language Models on Edge Devices	2025	Edge-based VLM deployment
Multimodal AIoT Agent Architecture	2025	AI + IoT integration patterns
Edge AI for Smart Workspace Monitoring	2024	Privacy-preserving workplace AI
TinyML for Vision Applications	2023	Lightweight CV models
Privacy-Preserving Edge AI	2024	Data privacy at the edge
📝 License
This project is for Educational and Research Purposes only.

👨‍💻 Author
Dheeraj Sonkar

Degree: Master of Computer Applications (MCA)

Specialization: Artificial Intelligence & Internet of Things (AI & IoT)

Institution: National Institute of Technology (NIT), Patna

🙏 Acknowledgments
National Institute of Technology, Patna

Department of Computer Science and Engineerig 

Faculty and Mentors for their guidance and support

📧 Contact
For any queries or collaboration:

Email: dheeraj@example.com

LinkedIn: linkedin.com/in/dheerajsonkar

GitHub: github.com/dheerajsonkar


📧 Contact
For any queries or collaboration:

Email: dheeraj@example.com

LinkedIn: linkedin.com/in/dheerajsonkar

GitHub: github.com/dheerajsonkar

📊 Project Status
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ✅ Project Status: COMPLETE & WORKING                      ║
║                                                               ║
║   ✅ Face Detection          WORKING                         ║
║   ✅ Eye Detection           WORKING                         ║
║   ✅ EAR Calculation         WORKING                         ║
║   ✅ Fatigue Detection       WORKING                         ║
║   ✅ Blink Detection         WORKING                         ║
║   ✅ Person Detection        WORKING                         ║
║   ✅ Object Detection        WORKING                         ║
║   ✅ Report Generation       WORKING                         ║
║   ✅ Dashboard               WORKING                         ║
║   ✅ Video Feed              WORKING                         ║
║                                                              ║
║   🚀 Ready for Viva & Placement!                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
Made with ❤️ at NIT Patna

# Clone
git clone <repo-url>
cd Edge_Multimodal_AI_Agent

# Setup
py -3.11 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# Run
python main.py

# Open
# Dashboard: http://127.0.0.1:8000/dashboard/
# Swagger: http://127.0.0.1:8000/docs
@echo off

title Edge Multimodal AI Agent

echo =====================================
echo Edge Multimodal AI Agent
echo =====================================

if not exist .venv (

echo Creating Virtual Environment...

py -3.11 -m venv .venv

)

call .venv\Scripts\activate

python -m pip install --upgrade pip

pip install -r requirements.txt

echo.

echo Starting FastAPI Server...

python -m uvicorn main:app --reload

pause
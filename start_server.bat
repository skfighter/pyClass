@echo off
REM PyClass - Start Development Server
REM This script activates the virtual environment and starts the FastAPI server

echo Starting PyClass API Server...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause

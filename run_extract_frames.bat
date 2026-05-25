@echo off
setlocal

cd /d "%~dp0"

set "PYTHON=D:\sd.webui\ComfyUI\venv\Scripts\python.exe"
set "INPUT_VIDEO=video_inputs\input.mp4"
set "OUTPUT_DIR=video_frames"
set "FPS=1"

if not exist "%PYTHON%" (
    echo ERROR: Python not found: %PYTHON%
    pause
    exit /b 1
)

"%PYTHON%" -c "import cv2" >nul 2>nul
if errorlevel 1 (
    echo OpenCV not found. Installing opencv-python...
    "%PYTHON%" -m pip install opencv-python --no-cache-dir --timeout 1000 --retries 20 --progress-bar off
    if errorlevel 1 (
        echo ERROR: Failed to install opencv-python.
        pause
        exit /b 1
    )
)

if not exist "%INPUT_VIDEO%" (
    echo ERROR: Input video not found: %cd%\%INPUT_VIDEO%
    echo Put your video at video_inputs\input.mp4 or edit this BAT file.
    pause
    exit /b 1
)

"%PYTHON%" "%~dp0scripts\extract_frames.py" --input "%INPUT_VIDEO%" --output "%OUTPUT_DIR%" --fps "%FPS%"

pause

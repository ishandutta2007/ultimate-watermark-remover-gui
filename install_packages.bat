@echo off

REM Install Python packages
pip install -r requirements.txt

REM Check for ffmpeg
where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    echo ffmpeg could not be found. Please install ffmpeg to process videos.
    echo You can download it from https://ffmpeg.org/download.html
    exit /b 1
)

echo Installation complete.

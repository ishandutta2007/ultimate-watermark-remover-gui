@echo off
setlocal
cd /d "%~dp0"

set "VENV_DIR=.venv"
set "PYTHON_EXE=%VENV_DIR%\Scripts\python.exe"

echo.
echo =============================================
echo   Ultimate Watermark Remover Windows Build
echo =============================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo [X] Python was not found on PATH.
    echo     Install Python 3.11 or newer and try again.
    exit /b 1
)

if not exist "%PYTHON_EXE%" (
    echo [*] Creating virtual environment...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo [X] Failed to create the virtual environment.
        exit /b 1
    )
)

echo [*] Installing build dependencies...
"%PYTHON_EXE%" -m pip install --upgrade pip
if errorlevel 1 exit /b 1

"%PYTHON_EXE%" -m pip install --requirement requirements.txt pyinstaller
if errorlevel 1 (
    echo [X] Failed to install build dependencies.
    exit /b 1
)

echo [*] Building the application...
"%PYTHON_EXE%" -m PyInstaller --noconfirm --clean UltimateWatermarkRemover.spec
if errorlevel 1 (
    echo [X] Build failed.
    exit /b 1
)

echo.
echo [OK] Build complete:
echo     dist\UltimateWatermarkRemover\UltimateWatermarkRemover.exe
echo.
echo FFmpeg must be installed separately and available on PATH for video audio processing.
endlocal

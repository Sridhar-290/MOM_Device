@echo off
echo Starting MOM Device Simulation (Mock Mode)...

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not found! Please install Python from python.org
    pause
    exit /b
)

:: Install dependencies
echo Installing dependencies...
pip install -r server/requirements.txt

:: Start Server in a new window
echo Starting Flask Server...
start "MOM Server" cmd /k "python server/app.py"

:: Wait for server to start
timeout /t 5

:: Run Test Script
echo Running Test Script...
python server/test_growl.py

echo.
echo Simulation Complete!
pause

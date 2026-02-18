@echo off
REM Store Opening AI - Start Dashboard Script (Windows)
REM Activates virtual environment and starts the Streamlit dashboard
REM 
REM USAGE: start_dashboard.bat (NOT ./start_dashboard.bat)

echo ============================================================
echo Starting Store Opening AI Dashboard...
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Error: Virtual environment not found.
    echo Please run setup.bat first to set up the project.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if backend is running (simple check)
echo Checking if backend is running...
curl -s http://localhost:5000/health >nul 2>&1
if errorlevel 1 (
    echo Warning: Backend might not be running.
    echo Make sure to start the backend first:
    echo start_backend.bat (in another terminal)
    echo.
    echo Continuing anyway...
    echo.
)

REM Start dashboard
echo Starting dashboard (will open in browser^)...
echo Press Ctrl+C to stop
echo.
streamlit run frontend\dashboard.py

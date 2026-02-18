@echo off
REM Store Opening AI - Start Backend Script (Windows)
REM Activates virtual environment and starts the backend API

echo ============================================================
echo Starting Store Opening AI Backend...
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

REM Check if database exists
if not exist "store_opening.db" (
    echo Warning: Database not found. Initializing...
    python data\seed_beta_data.py
    echo.
)

REM Start backend
echo Starting backend on http://localhost:5000
echo Press Ctrl+C to stop
echo.
python main.py

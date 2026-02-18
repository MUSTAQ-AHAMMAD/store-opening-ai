@echo off
REM Store Opening AI - Quick Setup Script (Windows)
REM This script automates the initial setup process
REM 
REM USAGE: 
REM   Run this script from the project directory:
REM     setup.bat             (preferred)
REM   or
REM     .\setup.bat
REM   
REM   DO NOT use: ./setup.bat (Unix syntax - will not work on Windows)

echo ============================================================
echo Store Opening AI - Quick Setup Script (Windows)
echo ============================================================
echo.

REM Check Python installation
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%
echo OK Python version
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo OK Virtual environment created
) else (
    echo OK Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo OK Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel --quiet
echo OK pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt --quiet
echo OK Dependencies installed
echo.

REM Setup .env file
echo Setting up environment configuration...
if not exist ".env" (
    copy .env.example .env
    echo OK .env file created
) else (
    echo OK .env file already exists (not modified)
)

REM Ensure TEST_MODE is set to true
powershell -Command "(Get-Content .env) -replace 'TEST_MODE=false', 'TEST_MODE=true' | Set-Content .env"
echo OK TEST_MODE enabled
echo.

REM Initialize database
echo Initializing database with sample data...
python data\seed_beta_data.py
echo OK Database initialized
echo.

echo ============================================================
echo Setup Complete! Success!
echo ============================================================
echo.
echo You can now start the application:
echo.
echo   Terminal 1 - Backend API:
echo     venv\Scripts\activate
echo     python main.py
echo.
echo   Terminal 2 - Dashboard:
echo     venv\Scripts\activate
echo     streamlit run frontend\dashboard.py
echo.
echo Then open your browser to:
echo   - Backend: http://localhost:5000
echo   - Dashboard: http://localhost:8501
echo.
echo Login with:
echo   - Username: admin
echo   - Password: admin123
echo.
echo For more details, see LOCAL_TESTING_GUIDE.md
echo ============================================================
echo.
pause

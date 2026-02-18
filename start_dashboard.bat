@echo off
REM Store Opening AI - Start React Dashboard Script (Windows)
REM Starts the React.js frontend dashboard
REM 
REM USAGE: start_dashboard.bat (NOT ./start_dashboard.bat)

echo ============================================================
echo Starting Store Opening AI React Dashboard...
echo ============================================================
echo.

REM Check if react-frontend directory exists
if not exist "react-frontend" (
    echo Error: react-frontend directory not found.
    pause
    exit /b 1
)

REM Navigate to react-frontend directory
cd react-frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing React dependencies...
    call npm install
    echo.
)

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

REM Start React dashboard
echo Starting React dashboard...
echo Dashboard will open at http://localhost:3000
echo Press Ctrl+C to stop
echo.
call npm start

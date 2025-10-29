@echo off
echo ====================================
echo   Solana Mint Tracker Starting
echo ====================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js not found!
    echo.
    echo Please install Node.js first:
    echo 1. Go to https://nodejs.org
    echo 2. Download LTS version
    echo 3. Install it
    echo 4. Close and reopen PowerShell
    echo 5. Run this file again
    echo.
    pause
    exit /b 1
)

echo [OK] Node.js found!
echo.

REM Check if node_modules exists
if not exist "node_modules\" (
    echo Installing dependencies...
    echo.
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo [ERROR] npm install failed!
        pause
        exit /b 1
    )
    echo.
    echo [OK] Dependencies installed!
    echo.
)

echo Starting application...
echo.
echo Web interface: http://localhost:3000
echo.
echo Press CTRL+C to stop
echo ====================================
echo.

call npm start

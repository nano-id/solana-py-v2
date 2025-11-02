@echo off
echo ====================================
echo   Node.js Auto Installer
echo ====================================
echo.

echo Checking if Node.js is already installed...
where node >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Node.js is already installed!
    node --version
    npm --version
    echo.
    pause
    exit /b 0
)

echo [INFO] Node.js not found. Starting installation...
echo.

REM Open Node.js download page
echo Opening Node.js download page in your browser...
start https://nodejs.org/

echo.
echo ====================================
echo   Installation Instructions:
echo ====================================
echo.
echo 1. The download page should open in your browser
echo 2. Download the LTS version (recommended)
echo 3. Run the installer (.msi file)
echo 4. Click "Next" on all screens
echo 5. After installation, close this window
echo 6. Run start.bat again
echo.
echo ====================================
echo.
pause












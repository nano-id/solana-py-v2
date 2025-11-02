@echo off
chcp 65001 >nul
echo ========================================
echo   Solana-py-v2 - Hizli Baslat
echo ========================================
echo.
echo [1] Yerel sunucu baslat (http://localhost:8080)
echo [2] Git durum kontrolu
echo [3] GitHub'a push
echo [4] Render deployment bilgileri
echo.
set /p secim="Seciminiz (1-4): "

if "%secim%"=="1" (
    echo.
    echo Sunucu baslatiliyor...
    echo Tarayicida: http://localhost:8080
    echo.
    python -m uvicorn main:app --host 0.0.0.0 --port 8080
    pause
    exit
)

if "%secim%"=="2" (
    echo.
    echo Git Durumu:
    echo ----------------------------------------
    git status
    echo.
    pause
    exit
)

if "%secim%"=="3" (
    echo.
    echo GitHub'a push yapiliyor...
    echo.
    git push -u origin main
    echo.
    echo Push tamamlandi!
    echo.
    pause
    exit
)

if "%secim%"=="4" (
    echo.
    echo ========================================
    echo Render Deployment Bilgileri
    echo ========================================
    echo.
    echo Build Command:
    echo   pip install -r requirements.txt
    echo.
    echo Start Command:
    echo   uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
    echo.
    echo Port: 8080
    echo.
    echo Detaylar icin: DURUM_RAPORU.md
    echo.
    pause
    exit
)

echo Gecersiz secim!
pause


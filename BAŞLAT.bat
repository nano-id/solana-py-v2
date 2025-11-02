@echo off
echo ====================================
echo   Solana Mint Tracker Başlatılıyor
echo ====================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [HATA] Node.js bulunamadı!
    echo.
    echo Lutfen once Node.js kurulumu yapin:
    echo 1. https://nodejs.org adresine gidin
    echo 2. LTS surumunu indirin
    echo 3. Kurulumu tamamlayin
    echo 4. PowerShell'i kapatip yeniden acin
    echo 5. Bu dosyayi tekrar calistirin
    echo.
    pause
    exit /b 1
)

echo [OK] Node.js bulundu!
echo.

REM Check if node_modules exists
if not exist "node_modules\" (
    echo Node modulleri bulunamadi. Yukleniyor...
    echo.
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo [HATA] npm install basarisiz oldu!
        pause
        exit /b 1
    )
    echo.
    echo [OK] Node modulleri yuklendi!
    echo.
)

echo Uygulama baslatiliyor...
echo.
echo Web arayuzune erismek icin: http://localhost:3000
echo.
echo Kapatmak icin: CTRL+C
echo ====================================
echo.

call npm start












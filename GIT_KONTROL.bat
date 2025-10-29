@echo off
echo ========================================
echo Git ve GitHub Baglanti Kontrolu
echo ========================================
echo.

REM Git kurulu mu?
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Git kurulu DEGIL!
    echo     Lutfen suradan kurun: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
) else (
    echo [OK] Git kurulu
    git --version
)

echo.
echo ----------------------------------------
echo Git Repository Durumu:
echo ----------------------------------------

REM .git klasoru var mi?
if exist ".git" (
    echo [OK] Git repository mevcut
    echo.
    echo Branch:
    git branch --show-current 2>nul || echo "Henuz commit yok"
    echo.
    echo Remote Repository:
    git remote -v 2>nul || echo "Remote baglanti yok"
) else (
    echo [X] Git repository YOK!
    echo     'git init' komutuyla baslatilmali
)

echo.
echo ----------------------------------------
echo Dosya Durumu:
echo ----------------------------------------
git status --short 2>nul || echo "Git repository yok - 'git init' calistirin"

echo.
echo ========================================
echo Detayli rehber icin: GITHUB_BAGLAN.md
echo ========================================
pause


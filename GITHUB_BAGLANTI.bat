@echo off
chcp 65001 >nul
echo ========================================
echo   GitHub Baglanti Ayarlari
echo ========================================
echo.

set /p GITHUB_USER="GitHub kullanici adi [nano-id]: "
if "%GITHUB_USER%"=="" set GITHUB_USER=nano-id

set /p REPO_NAME="Repo adi [solana-py-v2]: "
if "%REPO_NAME%"=="" set REPO_NAME=solana-py-v2

echo.
echo ----------------------------------------
echo Ayarlar:
echo ----------------------------------------
echo GitHub Kullanici: %GITHUB_USER%
echo Repo Adi: %REPO_NAME%
echo Repo URL: https://github.com/%GITHUB_USER%/%REPO_NAME%
echo.
set /p CONFIRM="Dogru mu? (E/H): "
if /i not "%CONFIRM%"=="E" (
    echo Iptal edildi.
    pause
    exit /b
)

echo.
echo ----------------------------------------
echo Git Kontrolu...
echo ----------------------------------------

git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Git kurulu DEGIL!
    echo.
    echo Lutfen once Git kurun:
    echo https://git-scm.com/download/win
    echo.
    start https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [OK] Git kurulu
echo.

REM Git config kontrolu
git config user.name >nul 2>&1
if %errorlevel% neq 0 (
    echo Git kullanici adi ayarlanmamis.
    set /p GIT_NAME="Git kullanici adiniz (commit icin): "
    git config user.name "%GIT_NAME%"
)

git config user.email >nul 2>&1
if %errorlevel% neq 0 (
    set /p GIT_EMAIL="Git email adresiniz (commit icin): "
    git config user.email "%GIT_EMAIL%"
)

echo.
echo ----------------------------------------
echo Repository Ayarlari...
echo ----------------------------------------

REM .git klasoru var mi kontrol et
if not exist ".git" (
    echo [*] Git repository baslatiliyor...
    git init
    echo [OK] Git repository baslatildi
) else (
    echo [OK] Git repository zaten mevcut
)

echo.
echo ----------------------------------------
echo Dosyalar Ekleniyor...
echo ----------------------------------------
git add .
echo [OK] Dosyalar eklendi

echo.
echo ----------------------------------------
echo Commit Olusturuluyor...
echo ----------------------------------------
git commit -m "Initial commit: Render-optimized FastAPI backend" 2>nul
if %errorlevel% neq 0 (
    echo [*] Zaten commit yapilmis veya degisiklik yok
)

echo.
echo ----------------------------------------
echo GitHub Baglantisi...
echo ----------------------------------------

REM Mevcut remote var mi kontrol et
git remote get-url origin >nul 2>&1
if %errorlevel% equ 0 (
    echo [*] Remote 'origin' zaten mevcut
    set /p UPDATE_REMOTE="Guncellemek istiyor musunuz? (E/H): "
    if /i "%UPDATE_REMOTE%"=="E" (
        git remote remove origin
        git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git
        echo [OK] Remote guncellendi
    ) else (
        echo [*] Remote degistirilmedi
    )
) else (
    git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git
    echo [OK] Remote eklendi
)

echo.
echo ----------------------------------------
echo Branch Ayari...
echo ----------------------------------------
git branch -M main 2>nul
echo [OK] Branch 'main' olarak ayarlandi

echo.
echo ========================================
echo   Hazir! Push Icin Son Adim
echo ========================================
echo.
echo Su komutu calistir:
echo.
echo   git push -u origin main
echo.
echo Authentication icin:
echo - GitHub kullanici adi
echo - Personal Access Token (sifre yerine)
echo.
echo Token olusturmak icin:
echo https://github.com/settings/tokens
echo.
echo GitHub reposunu kontrol et:
start https://github.com/%GITHUB_USER%/%REPO_NAME%
echo.
pause


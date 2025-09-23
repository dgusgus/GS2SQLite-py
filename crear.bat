@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                🏗️  CREAR ESTRUCTURA DE BD                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

if not exist "venv" (
    echo ❌ Sistema no instalado. Ejecuta setup.bat primero
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
python main.py crear

echo.
pause
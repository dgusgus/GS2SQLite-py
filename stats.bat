@echo off
chcp 65001 >nul
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                  📊 ESTADÍSTICAS DE DATOS                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

if not exist "venv" (
    echo ❌ Sistema no instalado. Ejecuta setup.bat primero
    pause
    exit /b 1
)

if not exist "../database/operadores.db" (
    echo ❌ Base de datos no encontrada
    echo 💡 Ejecuta ejecutar.bat primero para crear la base de datos
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
python main.py stats

echo.
pause

REM ===================================================================

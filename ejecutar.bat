@echo off
chcp 65001 >nul
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                   🚀 CONVERSIÓN COMPLETA                      ║
echo ║          Google Sheets → Base de Datos SQLite                 ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Verificaciones previas
if not exist "venv" (
    echo ❌ Entorno virtual no encontrado
    echo 💡 Ejecuta setup.bat primero
    echo.
    pause
    exit /b 1
)

if not exist "generador-docs-31f4b831a196.json" (
    echo ❌ Credenciales no encontradas
    echo 💡 Coloca el archivo 'generador-docs-31f4b831a196.json' aquí
    echo.
    pause
    exit /b 1
)

echo 🔄 Activando entorno virtual...
call venv\Scripts\activate.bat

echo 🚀 Iniciando conversión completa...
echo.
python main.py todo

echo.
if errorlevel 0 (
    echo ╔════════════════════════════════════════════════════════════════╗
    echo ║                    ✅ CONVERSIÓN EXITOSA                       ║
    echo ╚════════════════════════════════════════════════════════════════╝
    echo.
    echo 📁 Base de datos guardada en: ../database/operadores.db
    echo 🎯 El archivo está listo para usar en los otros sistemas
) else (
    echo ╔════════════════════════════════════════════════════════════════╗
    echo ║                     ❌ ERROR EN CONVERSIÓN                     ║
    echo ╚════════════════════════════════════════════════════════════════╝
    echo.
    echo 💡 Revisa los mensajes de error arriba
)

echo.
echo Presiona cualquier tecla para salir...
pause >nul
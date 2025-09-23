REM importar.bat - Solo importar datos
@echo off
chcp 65001 >nul
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║               📥 IMPORTAR DATOS ACTUALIZADOS                   ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

if not exist "venv" (
    echo ❌ Sistema no instalado. Ejecuta setup.bat primero
    pause
    exit /b 1
)

if not exist "../database/operadores.db" (
    echo ❌ Base de datos no existe
    echo 💡 Ejecuta ejecutar.bat primero para crear la estructura
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
echo 🔄 Reimportando datos desde Google Sheets...
echo ⚠️  Esto actualizará los datos existentes sin duplicar
echo.
python main.py importar

echo.
echo ✅ Datos actualizados
echo 💡 Usa stats.bat para ver los cambios
echo.
pause

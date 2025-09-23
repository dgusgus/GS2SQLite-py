@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    🧹 LIMPIAR INSTALACIÓN                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo ⚠️  Esto eliminará:
echo    • El entorno virtual (venv/)
echo    • Archivos temporales de Python (__pycache__/)
echo    • La base de datos (../database/operadores.db)
echo.
set /p respuesta="¿Estás seguro? (s/N): "
if /i not "%respuesta%"=="s" (
    echo Cancelado por el usuario
    pause
    exit /b 0
)

echo.
echo 🧹 Limpiando...

if exist "venv" (
    rmdir /s /q "venv"
    echo    ✅ Entorno virtual eliminado
)

if exist "__pycache__" (
    rmdir /s /q "__pycache__"
    echo    ✅ Cache de Python eliminado
)

if exist "..\database\operadores.db" (
    del "..\database\operadores.db"
    echo    ✅ Base de datos eliminada
)

echo.
echo ✅ Limpieza completada
echo 💡 Ejecuta setup.bat para reinstalar
echo.
pause
# run.bat - Windows
@echo off
echo ========================================
echo   Sistema 1: Conversion de Datos
echo   Ejecucion completa
echo ========================================
echo.

if not exist venv (
    echo ❌ Entorno virtual no encontrado
    echo Ejecuta setup.bat primero
    pause
    exit /b 1
)

if not exist generador-docs-31f4b831a196.json (
    echo ❌ Archivo de credenciales no encontrado
    echo Copia generador-docs-31f4b831a196.json en esta carpeta
    pause
    exit /b 1
)

echo Activando entorno virtual...
call venv\Scripts\activate.bat

echo Ejecutando conversion completa...
python main.py --action all

echo.
if errorlevel 0 (
    echo ✅ Conversion completada exitosamente!
) else (
    echo ❌ Error en la conversion
)
echo.
echo Presiona cualquier tecla para salir...
pause

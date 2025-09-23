# setup.bat - Windows
@echo off
echo ========================================
echo   Sistema 1: Conversion de Datos
echo   Configuracion automatica
echo ========================================
echo.

echo [1/4] Verificando Python...
python --version
if errorlevel 1 (
    echo ❌ Python no encontrado. Instala Python 3.8+
    pause
    exit /b 1
)

echo [2/4] Creando entorno virtual...
python -m venv venv
if errorlevel 1 (
    echo ❌ Error creando entorno virtual
    pause
    exit /b 1
)

echo [3/4] Activando entorno virtual...
call venv\Scripts\activate.bat

echo [4/4] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)

echo.
echo ✅ Configuracion completada!
echo.
echo Para ejecutar el sistema:
echo   - Conversion completa: run.bat
echo   - Solo estadisticas: run-stats.bat
echo.
pause
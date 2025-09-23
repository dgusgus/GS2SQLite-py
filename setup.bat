@echo off
chcp 65001 >nul
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    SISTEMA 1 - INSTALACIÓN                    ║
echo ║                   Conversión de Datos                          ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo [1/5] 🔍 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    echo.
    echo 💡 SOLUCIÓN:
    echo    1. Instala Python desde: https://python.org/downloads/
    echo    2. Marca "Add Python to PATH" durante la instalación
    echo    3. Reinicia el CMD y ejecuta setup.bat otra vez
    echo.
    pause
    exit /b 1
)

python --version
echo    ✅ Python disponible

echo.
echo [2/5] 📁 Creando estructura de carpetas...
if not exist "../database" mkdir "../database"
echo    ✅ Carpeta database creada

echo.
echo [3/5] 🐍 Creando entorno virtual...
if exist "venv" (
    echo    ⚠️  Entorno virtual ya existe, recreando...
    rmdir /s /q "venv"
)

python -m venv venv
if errorlevel 1 (
    echo ❌ Error creando entorno virtual
    pause
    exit /b 1
)
echo    ✅ Entorno virtual creado

echo.
echo [4/5] 📦 Instalando dependencias...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Error instalando dependencias
    echo.
    echo 💡 Verifica tu conexión a internet e intenta de nuevo
    pause
    exit /b 1
)
echo    ✅ Dependencias instaladas

echo.
echo [5/5] 🔑 Verificando credenciales...
if exist "generador-docs-31f4b831a196.json" (
    echo    ✅ Archivo de credenciales encontrado
) else (
    echo    ⚠️  Archivo de credenciales NO encontrado
    echo.
    echo 💡 PENDIENTE:
    echo    Coloca 'generador-docs-31f4b831a196.json' en esta carpeta
)

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    ✅ INSTALACIÓN COMPLETA                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 🚀 CÓMO USAR:
echo    • Conversión completa:    ejecutar.bat
echo    • Solo estadísticas:      stats.bat
echo    • Solo importar datos:    importar.bat
echo    • Solo crear estructura:  crear.bat
echo.
pause
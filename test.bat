@echo off
chcp 65001 >nul
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    🧪 PRUEBAS DEL SISTEMA                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

if not exist "venv" (
    echo ❌ Sistema no instalado. Ejecuta setup.bat primero
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo 🔍 Probando conexión con Google Sheets...
python -c "
try:
    from config import *
    from sheets import SheetsManager
    sheets = SheetsManager()
    hojas = sheets.list_sheets()
    print(f'✅ Conexión exitosa. Hojas disponibles: {len(hojas)}')
    for hoja in hojas:
        print(f'   📄 {hoja}')
except Exception as e:
    print(f'❌ Error: {e}')
"

echo.
echo 🔍 Probando base de datos...
python -c "
try:
    from database import DatabaseManager
    db = DatabaseManager()
    db.create_schema()
    stats = db.get_stats()
    print('✅ Base de datos funcional')
    print(f'📊 Tablas creadas: {len(stats)}')
except Exception as e:
    print(f'❌ Error: {e}')
"

echo.
pause
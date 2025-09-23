# test_connection.py - Script para probar conexión
import os
import sys
from pathlib import Path

def test_credentials():
    """Prueba las credenciales de Google Sheets"""
    creds_path = "generador-docs-31f4b831a196.json"
    
    if not os.path.exists(creds_path):
        print("❌ Archivo de credenciales no encontrado")
        print(f"   Busca: {creds_path}")
        return False
    
    try:
        import json
        with open(creds_path, 'r') as f:
            creds = json.load(f)
        
        required_fields = ['type', 'project_id', 'private_key', 'client_email']
        missing = [field for field in required_fields if field not in creds]
        
        if missing:
            print(f"❌ Campos faltantes en credenciales: {missing}")
            return False
        
        print("✅ Archivo de credenciales válido")
        return True
        
    except json.JSONDecodeError:
        print("❌ Archivo de credenciales malformado (no es JSON válido)")
        return False
    except Exception as e:
        print(f"❌ Error leyendo credenciales: {e}")
        return False

def test_google_sheets_connection():
    """Prueba conexión con Google Sheets"""
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        
        SCOPES = [
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/drive.readonly'
        ]
        
        creds = Credentials.from_service_account_file(
            "generador-docs-31f4b831a196.json", scopes=SCOPES
        )
        client = gspread.authorize(creds)
        
        # Probar acceso al spreadsheet
        spreadsheet_id = "1ehySw2tVI1l8INo4fgE7kEGFd0Kb2miPs7vCqsFZC8I"
        spreadsheet = client.open_by_key(spreadsheet_id)
      
        print(f"✅ Conexión exitosa a: {spreadsheet.title}")
        
        # Listar hojas disponibles
        worksheets = [ws.title for ws in spreadsheet.worksheets()]
        print(f"📊 Hojas disponibles: {len(worksheets)}")
        for ws in worksheets:
            print(f"   - {ws}")
        
        return True
        
    except ImportError:
        print("❌ Librerías no instaladas. Ejecuta: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error conectando con Google Sheets: {e}")
        return False

def test_database_creation():
    """Prueba creación de base de datos"""
    try:
        import sqlite3
        from pathlib import Path
        
        # Crear directorio si no existe
        db_path = Path("../database/operadores.db")
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Probar conexión
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Crear tabla de prueba
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        """)
        
        # Insertar dato de prueba
        cursor.execute("INSERT INTO test_table (name) VALUES (?)", ("test",))
        
        # Verificar dato
        cursor.execute("SELECT COUNT(*) FROM test_table")
        count = cursor.fetchone()[0]
        
        # Limpiar
        cursor.execute("DROP TABLE test_table")
        conn.commit()
        conn.close()
        
        print(f"✅ Base de datos funcional en: {db_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error con base de datos: {e}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("🧪 PRUEBAS DEL SISTEMA 1: CONVERSIÓN DE DATOS")
    print("=" * 50)
    
    tests = [
        ("Archivo de credenciales", test_credentials),
        ("Conexión Google Sheets", test_google_sheets_connection),
        ("Base de datos SQLite", test_database_creation)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Probando: {test_name}")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE PRUEBAS")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.ljust(25)}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 Todas las pruebas pasaron! El sistema está listo.")
        print("\nPara ejecutar conversión completa:")
        print("  python main.py --action all")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
# debug_data.py - Script para diagnosticar problemas de inserción
import sqlite3
import json
from pathlib import Path
from main import GoogleSheetsManager, DatabaseManager, SPREADSHEET_ID, CREDENTIALS_PATH, DATABASE_PATH

def inspect_sheets_data():
    """Inspecciona los datos raw de Google Sheets"""
    print("🔍 DIAGNÓSTICO: Inspeccionando datos de Google Sheets")
    print("=" * 60)
    
    try:
        sheets_manager = GoogleSheetsManager(CREDENTIALS_PATH, SPREADSHEET_ID)
        
        # Inspeccionar cada hoja
        worksheets = sheets_manager.get_all_worksheet_names()
        
        for sheet_name in worksheets:
            print(f"\n📊 HOJA: '{sheet_name}'")
            print("-" * 40)
            
            data = sheets_manager.get_worksheet_data(sheet_name)
            
            if not data:
                print("❌ Sin datos o error al leer")
                continue
                
            # Mostrar estructura del primer registro
            if len(data) > 0:
                print(f"📈 Registros encontrados: {len(data)}")
                print("🔑 Campos disponibles:")
                first_record = data[0]
                for key, value in first_record.items():
                    value_preview = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
                    print(f"   {key}: '{value_preview}'")
                
                # Mostrar todos los registros si son pocos
                if len(data) <= 3:
                    print("\n📋 Todos los registros:")
                    for i, record in enumerate(data):
                        print(f"   Registro {i+1}: {record}")
            else:
                print("❌ No hay registros")
                
    except Exception as e:
        print(f"❌ Error: {e}")

def inspect_database():
    """Inspecciona el contenido de la base de datos"""
    print("\n🗄️ DIAGNÓSTICO: Inspeccionando base de datos")
    print("=" * 60)
    
    db_path = Path(DATABASE_PATH)
    if not db_path.exists():
        print("❌ Base de datos no existe")
        return
    
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            
            # Obtener todas las tablas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            print(f"📊 Tablas encontradas: {len(tables)}")
            
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                
                print(f"\n📋 TABLA: {table}")
                print(f"   Registros: {count}")
                
                if count > 0:
                    # Mostrar estructura de la tabla
                    cursor.execute(f"PRAGMA table_info({table})")
                    columns = cursor.fetchall()
                    print("   Columnas:")
                    for col in columns:
                        print(f"     - {col[1]} ({col[2]})")
                    
                    # Mostrar algunos registros
                    cursor.execute(f"SELECT * FROM {table} LIMIT 3")
                    records = cursor.fetchall()
                    print("   Primeros registros:")
                    for record in records:
                        print(f"     {record}")
                        
    except Exception as e:
        print(f"❌ Error: {e}")

def test_manual_insertion():
    """Prueba inserción manual para identificar el problema"""
    print("\n🧪 DIAGNÓSTICO: Prueba de inserción manual")
    print("=" * 60)
    
    try:
        db_manager = DatabaseManager(DATABASE_PATH)
        
        # Probar inserción directa
        test_data = {
            'nombre': 'Test Jefe',
            'telefono': '+591-123456',
            'email': 'test@email.com'
        }
        
        print("🔬 Insertando registro de prueba...")
        jefe_id = db_manager.insert_or_update_record('jefe', test_data, 'nombre')
        print(f"✅ Jefe insertado con ID: {jefe_id}")
        
        # Verificar inserción
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM jefe WHERE nombre = ?", (test_data['nombre'],))
            result = cursor.fetchone()
            print(f"🔍 Registro encontrado: {result}")
            
            # Limpiar
            cursor.execute("DELETE FROM jefe WHERE nombre = ?", (test_data['nombre'],))
            conn.commit()
            print("🧹 Registro de prueba eliminado")
        
    except Exception as e:
        print(f"❌ Error en inserción manual: {e}")
        import traceback
        traceback.print_exc()

def test_conversion_functions():
    """Prueba las funciones de conversión paso a paso"""
    print("\n🔧 DIAGNÓSTICO: Probando funciones de conversión")
    print("=" * 60)
    
    try:
        from main import DataConverter
        
        sheets_manager = GoogleSheetsManager(CREDENTIALS_PATH, SPREADSHEET_ID)
        db_manager = DatabaseManager(DATABASE_PATH)
        converter = DataConverter(db_manager, sheets_manager)
        
        # Probar función específica
        print("🔬 Probando conversión de jefes...")
        
        # Obtener datos raw
        data = sheets_manager.get_worksheet_data('jefes')
        print(f"📊 Datos obtenidos: {data}")
        
        if data:
            print("🔧 Procesando primer registro...")
            row = data[0]
            print(f"   Registro raw: {row}")
            
            # Verificar campos requeridos
            if row.get('nombre'):
                print(f"   ✅ Campo 'nombre' encontrado: '{row.get('nombre')}'")
                
                jefe_data = {
                    'nombre': row.get('nombre', '').strip(),
                    'telefono': row.get('telefono', '').strip(),
                    'email': row.get('email', '').strip()
                }
                print(f"   📋 Datos procesados: {jefe_data}")
                
                # Intentar inserción
                jefe_id = db_manager.insert_or_update_record('jefe', jefe_data, 'nombre')
                print(f"   ✅ Insertado con ID: {jefe_id}")
                
            else:
                print("   ❌ Campo 'nombre' no encontrado o vacío")
                print(f"   🔍 Campos disponibles: {list(row.keys())}")
        
    except Exception as e:
        print(f"❌ Error en función de conversión: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Ejecuta todos los diagnósticos"""
    print("🚨 DIAGNÓSTICO COMPLETO DEL SISTEMA 1")
    print("=" * 60)
    
    # 1. Inspeccionar datos de entrada
    inspect_sheets_data()
    
    # 2. Inspeccionar base de datos
    inspect_database()
    
    # 3. Probar inserción manual
    test_manual_insertion()
    
    # 4. Probar funciones de conversión
    test_conversion_functions()
    
    print("\n" + "=" * 60)
    print("🎯 DIAGNÓSTICO COMPLETADO")
    print("=" * 60)
    print("Revisa la salida arriba para identificar el problema.")

if __name__ == "__main__":
    main()
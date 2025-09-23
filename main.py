# main.py - Programa principal
import argparse
from datetime import datetime
from database import DatabaseManager
from sheets import SheetsManager
from converters import DataConverters 
from config import SPREADSHEET_ID, CREDENTIALS_FILE, DATABASE_PATH, SHEET_NAMES

def show_stats(db: DatabaseManager):
    """Muestra estadísticas detalladas"""
    print("\n" + "="*60)
    print("📊 ESTADÍSTICAS DE LA BASE DE DATOS")
    print("="*60)
    
    stats = db.get_stats()
    total = sum(stats.values())
    
    for table, count in stats.items():
        emoji = {
            'jefe': '👔', 'coordinador': '👥', 'grupo': '🏢',
            'departamento': '🏛️', 'provincia': '🌄', 'municipio': '🏘️',
            'asiento_electoral': '🗳️', 'recinto': '🏫', 'vehiculo': '🚗',
            'chofer': '🚛', 'operador': '👷'
        }.get(table, '📋')
        
        print(f"{emoji} {table.replace('_', ' ').title().ljust(20)}: {count:>6} registros")
    
    print("="*60)
    print(f"🎯 TOTAL: {total:>6} registros")
    print("="*60)

def main():
    print("🚀 SISTEMA 1: CONVERSIÓN DE DATOS")
    print("=" * 50)
    print(f"⏰ Ejecutado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    parser = argparse.ArgumentParser(description="Convierte datos de Google Sheets a SQLite")
    parser.add_argument('comando', nargs='?', default='todo',
                       choices=['crear', 'importar', 'stats', 'todo'],
                       help='Comando a ejecutar')
    
    args = parser.parse_args()
    
    try:
        # Inicializar base de datos
        db = DatabaseManager()
        
        if args.comando == 'crear':
            print("🏗️  Creando estructura de base de datos...")
            db.create_schema()
            print("✅ Estructura creada")
            
        elif args.comando == 'importar':
            print("📥 Importando datos desde Google Sheets...")
            sheets = SheetsManager()
            converters = DataConverters(db)
            
            # Orden de importación (importante por dependencias)
            import_order = [
                ('jefes', converters.convert_jefes),
                ('coordinadores', converters.convert_coordinadores),
                ('grupos', converters.convert_grupos),
                ('departamentos', converters.convert_departamentos),
                ('provincias', converters.convert_provincias),
                ('municipios', converters.convert_municipios),
                ('asientos', converters.convert_asientos),
                ('recintos', converters.convert_recintos),
                ('vehiculos', converters.convert_vehiculos),
                ('choferes', converters.convert_choferes),
                ('operadores', converters.convert_operadores)
            ]
            
            for data_type, converter_func in import_order:
                sheet_name = SHEET_NAMES[data_type]
                data = sheets.get_sheet_data(sheet_name)
                if data:
                    converter_func(data)
                    
            print("✅ Importación completada")
            
        elif args.comando == 'stats':
            show_stats(db)
            
        else:  # 'todo'
            print("🏗️  Creando estructura...")
            db.create_schema()
            
            print("\n📥 Importando datos...")
            sheets = SheetsManager()
            converters = DataConverters(db)
            
            # Orden de importación (importante por dependencias)
            import_order = [
                ('jefes', converters.convert_jefes),
                ('coordinadores', converters.convert_coordinadores),
                ('grupos', converters.convert_grupos),
                ('departamentos', converters.convert_departamentos),
                ('provincias', converters.convert_provincias),
                ('municipios', converters.convert_municipios),
                ('asientos', converters.convert_asientos),
                ('recintos', converters.convert_recintos),
                ('vehiculos', converters.convert_vehiculos),
                ('choferes', converters.convert_choferes),
                ('operadores', converters.convert_operadores)
            ]
            
            for data_type, converter_func in import_order:
                sheet_name = SHEET_NAMES[data_type]
                data = sheets.get_sheet_data(sheet_name)
                if data:
                    converter_func(data)
            
            print("\n📊 Mostrando estadísticas...")
            show_stats(db)
            
        print(f"\n🎉 Proceso completado exitosamente!")
        print(f"💾 Base de datos guardada en: {db.db_path}")
        
    except FileNotFoundError as e:
        print(f"❌ Archivo no encontrado: {e}")
        print("\n💡 SOLUCIÓN:")
        print("   1. Coloca 'generador-docs-31f4b831a196.json' en esta carpeta")
        print("   2. Verifica que tengas acceso al Google Sheet")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Si el problema persiste:")
        print("   1. Verifica tu conexión a internet")
        print("   2. Revisa que las credenciales sean válidas") 
        print("   3. Comprueba los permisos del Google Sheet")

if __name__ == "__main__":
    main()
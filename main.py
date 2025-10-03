# main.py - Programa principal
import argparse
from datetime import datetime
from database import DatabaseManager
from sheets import SheetsManager
from converters import DataConverters
from config import SHEET_NAMES


def show_stats(db: DatabaseManager):
    """Muestra estadísticas detalladas"""
    print("\n" + "=" * 60)
    print("📊 ESTADÍSTICAS DE LA BASE DE DATOS")
    print("=" * 60)

    stats = db.get_stats()
    total = sum(stats.values())

    for table, count in stats.items():
        emoji = {
            'jefe': '👔',
            'coordinador': '👥',
            'grupo': '🏢',
            'departamento': '🏛️',
            'provincia': '🌄',
            'municipio': '🏘️',
            'asiento_electoral': '🗳️',
            'recinto': '🏫',
            'operador': '👷',
            'notario': '📜',
            'acta': '📄',
            'cuenta': '🔑'
        }.get(table, '📋')

        print(f"{emoji} {table.replace('_', ' ').title().ljust(20)}: {count:>6} registros")

    print("=" * 60)
    print(f"🎯 TOTAL: {total:>6} registros")
    print("=" * 60)


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
                ('asientos_electorales', converters.convert_asientos_electorales),
                ('recintos', converters.convert_recintos),
                ('operadores', converters.convert_operadores),
                ('notarios', converters.convert_notarios),
                ('actas', converters.convert_actas),
                ('cuentas', converters.convert_cuentas),
            ]

            for data_type, converter_func in import_order:
                sheet_name = SHEET_NAMES[data_type]
                print(f"📖 Leyendo hoja: {sheet_name}...")
                data = sheets.get_sheet_data(sheet_name)
                if data:
                    print(f"   📊 Procesando {len(data)} registros...")
                    converter_func(data)
                else:
                    print(f"   ⚠️  No se encontraron datos en {sheet_name}")

            print("✅ Importación completada")

        elif args.comando == 'stats':
            show_stats(db)

        else:  # 'todo'
            print("🏗️  Creando estructura...")
            db.create_schema()

            print("\n📥 Importando datos...")
            sheets = SheetsManager()
            converters = DataConverters(db)

            import_order = [
                ('jefes', converters.convert_jefes),
                ('coordinadores', converters.convert_coordinadores),
                ('grupos', converters.convert_grupos),
                ('departamentos', converters.convert_departamentos),
                ('provincias', converters.convert_provincias),
                ('municipios', converters.convert_municipios),
                ('asientos_electorales', converters.convert_asientos_electorales),
                ('recintos', converters.convert_recintos),
                ('operadores', converters.convert_operadores),
                ('notarios', converters.convert_notarios),
                ('actas', converters.convert_actas),
                ('cuentas', converters.convert_cuentas),
            ]

            for data_type, converter_func in import_order:
                sheet_name = SHEET_NAMES[data_type]
                print(f"📖 Leyendo hoja: {sheet_name}...")
                data = sheets.get_sheet_data(sheet_name)
                if data:
                    print(f"   📊 Procesando {len(data)} registros...")
                    converter_func(data)
                else:
                    print(f"   ⚠️  No se encontraron datos en {sheet_name}")

            print("\n📊 Mostrando estadísticas...")
            show_stats(db)

        print(f"\n🎉 Proceso completado exitosamente!")
        print(f"💾 Base de datos guardada en: {db.db_path}")

    except FileNotFoundError as e:
        print(f"❌ Archivo no encontrado: {e}")
        print("\n💡 SOLUCIÓN:")
        print("   1. Coloca 'generador-docs-31f4b831a196.json' en esta carpeta")
        print("   2. Verifica que tengas acceso al Google Sheet")

    except KeyError as e:
        print(f"❌ Error de configuración: {e}")
        print("\n💡 SOLUCIÓN:")
        print("   1. Verifica que SHEET_NAMES en config.py coincida con los nombres reales de las hojas")
        print("   2. Revisa que todas las hojas necesarias existan en el Google Sheet")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        print("\n💡 Si el problema persiste:")
        print("   1. Verifica tu conexión a internet")
        print("   2. Revisa que las credenciales sean válidas")
        print("   3. Comprueba los permisos del Google Sheet")
        print("   4. Verifica que los nombres de columnas coincidan con COLUMN_MAPPING")


if __name__ == "__main__":
    main()
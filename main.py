# main.py - Orquestador principal (esquema simplificado)
import argparse
from datetime import datetime
from database import DatabaseManager
from sheets import SheetsManager
from converters import DataConverters
from config import SHEET_NAMES


def show_stats(db: DatabaseManager):
    print("\n" + "=" * 60)
    print("📊 ESTADÍSTICAS DE LA BASE DE DATOS")
    print("=" * 60)

    stats = db.get_stats()

    labels = {
        'jefe':                ('👔', 'Jefes'),
        'coordinador':         ('👥', 'Coordinadores'),
        'grupo':               ('🏢', 'Grupos'),
        'departamento':        ('🏛️ ', 'Departamentos'),
        'provincia':           ('🌄', 'Provincias'),
        'municipio':           ('🏘️ ', 'Municipios'),
        'asiento_electoral':   ('🗳️ ', 'Asientos Electorales'),
        'recinto':             ('🏫', 'Recintos'),
        'persona':             ('👷', 'Personas (total)'),
        'operadores':          ('  ↳ 🟢', 'Operadores'),
        'notarios':            ('  ↳ 📜', 'Notarios'),
        'cuentas':             ('  ↳ 🔑', 'Con cuenta de acceso'),
        'acta':                ('📄', 'Actas'),
    }

    total_base = sum(v for k, v in stats.items()
                     if k in ['jefe','coordinador','grupo','departamento',
                               'provincia','municipio','asiento_electoral',
                               'recinto','persona','acta'])

    for key, (emoji, label) in labels.items():
        count = stats.get(key, 0)
        print(f"{emoji} {label.ljust(25)}: {count:>6} registros")

    print("=" * 60)
    print(f"🎯 TOTAL (tablas principales): {total_base:>6} registros")
    print("=" * 60)


def run_import(db: DatabaseManager):
    """Ejecuta la importación completa desde Google Sheets"""
    sheets = SheetsManager()
    converters = DataConverters(db)

    # ── Geografía y organización (orden por dependencias) ────────────
    geo_org_order = [
        ('jefes',                converters.convert_jefes),
        ('coordinadores',        converters.convert_coordinadores),
        ('grupos',               converters.convert_grupos),
        ('departamentos',        converters.convert_departamentos),
        ('provincias',           converters.convert_provincias),
        ('municipios',           converters.convert_municipios),
        ('asientos_electorales', converters.convert_asientos_electorales),
        ('recintos',             converters.convert_recintos),
    ]

    for data_type, converter_func in geo_org_order:
        sheet_name = SHEET_NAMES[data_type]
        print(f"📖 Leyendo '{sheet_name}'...")
        data = sheets.get_sheet_data(sheet_name)
        if data:
            converter_func(data)
        else:
            print(f"   ⚠️  Sin datos en '{sheet_name}'")

    # ── Personas: operadores + notarios + cuentas juntos ─────────────
    print(f"📖 Leyendo personas (Operadores / Notarios / Cuentas)...")
    operadores_data = sheets.get_sheet_data(SHEET_NAMES['operadores'])
    notarios_data   = sheets.get_sheet_data(SHEET_NAMES['notarios'])
    cuentas_data    = sheets.get_sheet_data(SHEET_NAMES['cuentas'])
    converters.convert_personas(operadores_data, notarios_data, cuentas_data)

    # ── Actas ────────────────────────────────────────────────────────
    print(f"📖 Leyendo '{SHEET_NAMES['actas']}'...")
    actas_data = sheets.get_sheet_data(SHEET_NAMES['actas'])
    if actas_data:
        converters.convert_actas(actas_data)
    else:
        print(f"   ⚠️  Sin datos en '{SHEET_NAMES['actas']}'")


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
        db = DatabaseManager()

        if args.comando == 'crear':
            print("🏗️  Creando estructura...")
            db.create_schema()

        elif args.comando == 'importar':
            print("📥 Importando datos...")
            run_import(db)
            print("✅ Importación completada")

        elif args.comando == 'stats':
            show_stats(db)

        else:  # 'todo'
            print("🏗️  Creando estructura...")
            db.create_schema()
            print("\n📥 Importando datos...")
            run_import(db)
            print()
            show_stats(db)

        print(f"\n🎉 Proceso completado exitosamente!")
        print(f"💾 Base de datos: {db.db_path}")

    except FileNotFoundError as e:
        print(f"❌ Archivo no encontrado: {e}")
        print("   Coloca 'generador-docs-31f4b831a196.json' en esta carpeta")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
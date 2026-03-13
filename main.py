# ============================================
# main.py
# Cambios v2:
#   - run_import() llama al validador antes de importar
#   - eliminada lectura de hoja Cuentas y Grupos
#   - convert_personas() ya no recibe cuentas_data
# ============================================

import argparse
from datetime import datetime
from database import DatabaseManager
from sheets import SheetsManager
from converters import DataConverters
from validator import run_validation
from config import SHEET_NAMES


def show_stats(db: DatabaseManager):
    print("\n" + "=" * 60)
    print("📊 ESTADÍSTICAS DE LA BASE DE DATOS")
    print("=" * 60)

    stats = db.get_stats()

    labels = {
        'jefe':               ('👔', 'Jefes'),
        'coordinador':        ('👥', 'Coordinadores (con grupo)'),
        'departamento':       ('🏛️ ', 'Departamentos'),
        'provincia':          ('🌄', 'Provincias'),
        'municipio':          ('🏘️ ', 'Municipios'),
        'asiento_electoral':  ('🗳️ ', 'Asientos Electorales'),
        'recinto':            ('🏫', 'Recintos'),
        'persona':            ('👷', 'Personas (total)'),
        'operadores':         ('  ↳ 🟢', 'Operadores'),
        'notarios':           ('  ↳ 📜', 'Notarios'),
        'cuentas':            ('  ↳ 🔑', 'Con cuenta de acceso'),
        'acta':               ('📄', 'Actas'),
    }

    total_base = sum(
        v for k, v in stats.items()
        if k in [
            'jefe', 'coordinador', 'departamento', 'provincia',
            'municipio', 'asiento_electoral', 'recinto', 'persona', 'acta',
        ]
    )

    for key, (emoji, label) in labels.items():
        count = stats.get(key, 0)
        print(f"{emoji} {label.ljust(28)}: {count:>6} registros")

    print("=" * 60)
    print(f"🎯 TOTAL (tablas principales): {total_base:>6} registros")
    print("=" * 60)


def _leer_datos(sheets: SheetsManager) -> dict:
    """Lee todas las hojas necesarias y las devuelve en un dict."""
    datos = {}
    hojas = [
        'jefes', 'coordinadores', 'departamentos', 'provincias',
        'municipios', 'asientos_electorales', 'recintos',
        'operadores', 'notarios', 'actas',
    ]
    for key in hojas:
        sheet_name = SHEET_NAMES[key]
        print(f"  📖 Leyendo '{sheet_name}'...")
        datos[key] = sheets.get_sheet_data(sheet_name)
    return datos


def run_import(db: DatabaseManager, skip_validation: bool = False):
    sheets = SheetsManager()
    converters = DataConverters(db)

    print("\n📥 Leyendo datos de Google Sheets...")
    datos = _leer_datos(sheets)

    # ── VALIDACIÓN PREVIA ─────────────────────────────────────────────
    if not skip_validation:
        puede_continuar = run_validation(
            jefes_data=         datos['jefes'],
            coordinadores_data= datos['coordinadores'],
            operadores_data=    datos['operadores'],
            notarios_data=      datos['notarios'],
            actas_data=         datos['actas'],
        )
        if not puede_continuar:
            print("\n🚫 Importación cancelada. Corrige los errores en Google Sheets.")
            return False
    else:
        print("  ⚠️  Validación omitida (--skip-validation)")

    print("\n💾 Importando a base de datos...")

    # ── Organización y geografía (orden por dependencias) ─────────────
    orden = [
        ('jefes',                converters.convert_jefes),
        ('coordinadores',        converters.convert_coordinadores),
        ('departamentos',        converters.convert_departamentos),
        ('provincias',           converters.convert_provincias),
        ('municipios',           converters.convert_municipios),
        ('asientos_electorales', converters.convert_asientos_electorales),
        ('recintos',             converters.convert_recintos),
    ]
    for key, fn in orden:
        if datos[key]:
            fn(datos[key])
        else:
            print(f"   ⚠️  Sin datos en '{SHEET_NAMES[key]}'")

    # ── Personas (operadores + notarios) ──────────────────────────────
    converters.convert_personas(datos['operadores'], datos['notarios'])

    # ── Actas ─────────────────────────────────────────────────────────
    if datos['actas']:
        converters.convert_actas(datos['actas'])
    else:
        print(f"   ⚠️  Sin datos en '{SHEET_NAMES['actas']}'")

    print("\n✅ Importación completada")
    return True


def main():
    print("🚀 SISTEMA 1: CONVERSIÓN DE DATOS")
    print("=" * 50)
    print(f"⏰ Ejecutado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    parser = argparse.ArgumentParser(description="Convierte datos de Google Sheets a SQLite")
    parser.add_argument(
        'comando', nargs='?', default='todo',
        choices=['crear', 'importar', 'stats', 'todo', 'validar'],
        help='Comando a ejecutar'
    )
    parser.add_argument(
        '--skip-validation', action='store_true',
        help='Omitir validación previa (no recomendado)'
    )
    args = parser.parse_args()

    try:
        db = DatabaseManager()

        if args.comando == 'crear':
            print("🏗️  Creando estructura...")
            db.create_schema()

        elif args.comando == 'importar':
            run_import(db, skip_validation=args.skip_validation)

        elif args.comando == 'stats':
            show_stats(db)

        elif args.comando == 'validar':
            # Solo validar, sin importar
            sheets = SheetsManager()
            print("\n📖 Leyendo datos...")
            datos = _leer_datos(sheets)
            run_validation(
                jefes_data=         datos['jefes'],
                coordinadores_data= datos['coordinadores'],
                operadores_data=    datos['operadores'],
                notarios_data=      datos['notarios'],
                actas_data=         datos['actas'],
            )
            return

        else:  # 'todo'
            print("🏗️  Creando estructura...")
            db.create_schema()
            ok = run_import(db, skip_validation=args.skip_validation)
            if ok:
                print()
                show_stats(db)

        print(f"\n🎉 Proceso completado!")
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
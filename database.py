# ============================================
# database.py
# Cambios v2:
#   - tabla 'grupo' eliminada: coordinador tiene campo nombre_grupo
#   - persona.grupo_id → persona.coordinador_id (referencia directa)
#   - acta: solo codigo + persona_id (sin recinto_id)
# ============================================

import sqlite3
from pathlib import Path
from typing import Dict, Any, Optional, Union
from config import DATABASE_PATH


class DatabaseManager:
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Base de datos: {self.db_path}")

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def create_schema(self):
        tables_sql = {

            # ── ORGANIZACIÓN ──────────────────────────────────────────
            'jefe': """
                CREATE TABLE IF NOT EXISTS jefe (
                    id      INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre  TEXT NOT NULL UNIQUE,
                    cargo   TEXT,
                    celular TEXT
                )
            """,

            # nombre_grupo fusionado aquí; antes era tabla separada
            'coordinador': """
                CREATE TABLE IF NOT EXISTS coordinador (
                    id           INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre       TEXT NOT NULL,
                    ci           TEXT UNIQUE NOT NULL,
                    expedido     TEXT,
                    celular      TEXT,
                    correo       TEXT,
                    cargo        TEXT,
                    nombre_grupo TEXT,
                    jefe_id      INTEGER,
                    FOREIGN KEY (jefe_id) REFERENCES jefe(id)
                )
            """,
            # jefe_id es NULL-able: coordinador puede no tener jefe asignado aún

            # ── GEOGRAFÍA ─────────────────────────────────────────────
            'departamento': """
                CREATE TABLE IF NOT EXISTS departamento (
                    id     INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE
                )
            """,

            'provincia': """
                CREATE TABLE IF NOT EXISTS provincia (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre          TEXT NOT NULL,
                    departamento_id INTEGER NOT NULL,
                    es_urbano       BOOLEAN DEFAULT 0,
                    UNIQUE(departamento_id, nombre),
                    FOREIGN KEY (departamento_id) REFERENCES departamento(id)
                )
            """,

            'municipio': """
                CREATE TABLE IF NOT EXISTS municipio (
                    id           INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre       TEXT NOT NULL,
                    provincia_id INTEGER NOT NULL,
                    UNIQUE(provincia_id, nombre),
                    FOREIGN KEY (provincia_id) REFERENCES provincia(id)
                )
            """,

            'asiento_electoral': """
                CREATE TABLE IF NOT EXISTS asiento_electoral (
                    id           INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre       TEXT NOT NULL,
                    municipio_id INTEGER NOT NULL,
                    UNIQUE(municipio_id, nombre),
                    FOREIGN KEY (municipio_id) REFERENCES municipio(id)
                )
            """,

            'recinto': """
                CREATE TABLE IF NOT EXISTS recinto (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre     TEXT NOT NULL,
                    direccion  TEXT,
                    distrito   INTEGER DEFAULT 0,
                    asiento_id INTEGER NOT NULL,
                    UNIQUE(asiento_id, nombre),
                    FOREIGN KEY (asiento_id) REFERENCES asiento_electoral(id)
                )
            """,

            # ── PERSONAS ──────────────────────────────────────────────
            # coordinador_id reemplaza grupo_id (vínculo directo al coordinador)
            # user/password fusionados (antes eran hoja Cuentas)
            'persona': """
                CREATE TABLE IF NOT EXISTS persona (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo            TEXT NOT NULL CHECK(tipo IN ('operador', 'notario')),
                    nombre          TEXT NOT NULL,
                    ci              TEXT UNIQUE NOT NULL,
                    expedido        TEXT,
                    celular         TEXT,
                    correo          TEXT,
                    cargo           TEXT,
                    recinto_id      INTEGER NOT NULL,
                    coordinador_id  INTEGER,
                    user            TEXT UNIQUE,
                    password        TEXT,
                    FOREIGN KEY (recinto_id)     REFERENCES recinto(id),
                    FOREIGN KEY (coordinador_id) REFERENCES coordinador(id)
                )
            """,

            # ── ACTAS ─────────────────────────────────────────────────
            # Solo codigo + persona_id; recinto se hereda via persona.recinto_id
            'acta': """
                CREATE TABLE IF NOT EXISTS acta (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo     TEXT NOT NULL UNIQUE,
                    persona_id INTEGER NOT NULL,
                    FOREIGN KEY (persona_id) REFERENCES persona(id)
                )
            """,
        }

        # ── ÍNDICES ───────────────────────────────────────────────────
        indexes_sql = [
            "CREATE INDEX IF NOT EXISTS idx_persona_ci         ON persona(ci)",
            "CREATE INDEX IF NOT EXISTS idx_persona_tipo       ON persona(tipo)",
            "CREATE INDEX IF NOT EXISTS idx_persona_coordinador ON persona(coordinador_id)",
            "CREATE INDEX IF NOT EXISTS idx_acta_persona       ON acta(persona_id)",
            "CREATE INDEX IF NOT EXISTS idx_recinto_asiento    ON recinto(asiento_id)",
            "CREATE INDEX IF NOT EXISTS idx_coordinador_jefe   ON coordinador(jefe_id)",
        ]

        # ── VISTAS ────────────────────────────────────────────────────
        views_sql = {
            'v_operadores': """
                CREATE VIEW IF NOT EXISTS v_operadores AS
                SELECT
                    p.id,
                    p.nombre,
                    p.ci,
                    p.celular,
                    p.correo,
                    p.cargo,
                    p.user,
                    c.nombre_grupo  AS grupo,
                    c.nombre        AS coordinador,
                    c.ci            AS coordinador_ci,
                    j.nombre        AS jefe,
                    r.nombre        AS recinto,
                    r.direccion     AS recinto_direccion,
                    ae.nombre       AS asiento_electoral,
                    m.nombre        AS municipio,
                    pr.nombre       AS provincia,
                    d.nombre        AS departamento,
                    CASE WHEN pr.es_urbano = 1 THEN 'urbano' ELSE 'rural' END AS tipo_zona
                FROM persona p
                JOIN recinto r            ON p.recinto_id = r.id
                JOIN asiento_electoral ae ON r.asiento_id = ae.id
                JOIN municipio m          ON ae.municipio_id = m.id
                JOIN provincia pr         ON m.provincia_id = pr.id
                JOIN departamento d       ON pr.departamento_id = d.id
                LEFT JOIN coordinador c   ON p.coordinador_id = c.id
                LEFT JOIN jefe j          ON c.jefe_id = j.id
                WHERE p.tipo = 'operador'
            """,

            'v_notarios': """
                CREATE VIEW IF NOT EXISTS v_notarios AS
                SELECT
                    p.id,
                    p.nombre,
                    p.ci,
                    p.celular,
                    p.correo,
                    p.cargo,
                    r.nombre        AS recinto,
                    r.direccion     AS recinto_direccion,
                    ae.nombre       AS asiento_electoral,
                    m.nombre        AS municipio,
                    pr.nombre       AS provincia,
                    d.nombre        AS departamento
                FROM persona p
                JOIN recinto r            ON p.recinto_id = r.id
                JOIN asiento_electoral ae ON r.asiento_id = ae.id
                JOIN municipio m          ON ae.municipio_id = m.id
                JOIN provincia pr         ON m.provincia_id = pr.id
                JOIN departamento d       ON pr.departamento_id = d.id
                WHERE p.tipo = 'notario'
            """,

            'v_actas': """
                CREATE VIEW IF NOT EXISTS v_actas AS
                SELECT
                    a.id,
                    a.codigo,
                    p.nombre        AS operador,
                    p.ci            AS operador_ci,
                    p.celular       AS operador_celular,
                    c.nombre_grupo  AS grupo,
                    c.nombre        AS coordinador,
                    r.nombre        AS recinto,
                    r.direccion     AS recinto_direccion,
                    ae.nombre       AS asiento_electoral,
                    m.nombre        AS municipio,
                    pr.nombre       AS provincia,
                    d.nombre        AS departamento
                FROM acta a
                JOIN persona p            ON a.persona_id = p.id
                JOIN recinto r            ON p.recinto_id = r.id
                JOIN asiento_electoral ae ON r.asiento_id = ae.id
                JOIN municipio m          ON ae.municipio_id = m.id
                JOIN provincia pr         ON m.provincia_id = pr.id
                JOIN departamento d       ON pr.departamento_id = d.id
                LEFT JOIN coordinador c   ON p.coordinador_id = c.id
            """,

            'v_recintos': """
                CREATE VIEW IF NOT EXISTS v_recintos AS
                SELECT
                    r.id,
                    r.nombre,
                    r.direccion,
                    r.distrito,
                    ae.nombre       AS asiento_electoral,
                    m.nombre        AS municipio,
                    pr.nombre       AS provincia,
                    d.nombre        AS departamento,
                    CASE WHEN pr.es_urbano = 1 THEN 'urbano' ELSE 'rural' END AS tipo_zona
                FROM recinto r
                JOIN asiento_electoral ae ON r.asiento_id = ae.id
                JOIN municipio m          ON ae.municipio_id = m.id
                JOIN provincia pr         ON m.provincia_id = pr.id
                JOIN departamento d       ON pr.departamento_id = d.id
            """,

            'v_coordinadores': """
                CREATE VIEW IF NOT EXISTS v_coordinadores AS
                SELECT
                    c.id,
                    c.nombre,
                    c.ci,
                    c.celular,
                    c.correo,
                    c.cargo,
                    c.nombre_grupo  AS grupo,
                    j.nombre        AS jefe,
                    COUNT(p.id)     AS total_operadores
                FROM coordinador c
                LEFT JOIN jefe j    ON c.jefe_id = j.id
                LEFT JOIN persona p ON p.coordinador_id = c.id AND p.tipo = 'operador'
                GROUP BY c.id
            """,
        }

        with self.get_connection() as conn:
            for table_name, sql in tables_sql.items():
                conn.execute(sql)
                print(f"  ✅ Tabla '{table_name}' lista")
            for idx_sql in indexes_sql:
                conn.execute(idx_sql)
            print(f"  ✅ Índices creados")
            for view_name, sql in views_sql.items():
                conn.execute(sql)
                print(f"  ✅ Vista '{view_name}' lista")

        print("✅ Esquema listo")

    # ── HELPERS ───────────────────────────────────────────────────────

    def insert_or_update(self, table: str, data: Dict[str, Any], unique_field: str) -> int:
        if not data or unique_field not in data:
            raise ValueError(f"Campo único '{unique_field}' no en datos")

        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    f"SELECT id FROM {table} WHERE {unique_field} = ?",
                    (data[unique_field],)
                )
                existing = cursor.fetchone()

                if existing:
                    update_data = {k: v for k, v in data.items() if k != unique_field}
                    if update_data:
                        fields = ", ".join(f"{k} = ?" for k in update_data)
                        values = list(update_data.values()) + [data[unique_field]]
                        cursor.execute(
                            f"UPDATE {table} SET {fields} WHERE {unique_field} = ?",
                            values
                        )
                    return existing[0]
                else:
                    fields = ", ".join(data.keys())
                    placeholders = ", ".join("?" for _ in data)
                    cursor.execute(
                        f"INSERT INTO {table} ({fields}) VALUES ({placeholders})",
                        list(data.values())
                    )
                    return cursor.lastrowid

            except sqlite3.IntegrityError as e:
                print(f"  ⚠️  Integridad en {table}: {e}")
                raise
            except sqlite3.Error as e:
                print(f"  ⚠️  Error en {table}: {e}")
                raise

    def get_id_by_field(self, table: str, field: str, value: Union[str, int]) -> Optional[int]:
        if value is None:
            return None
        search = str(value).strip()
        if not search:
            return None
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT id FROM {table} WHERE {field} = ? LIMIT 1", (search,))
            result = cursor.fetchone()
            return result[0] if result else None

    def get_recinto_id_by_asiento_and_nombre(
        self, asiento_nombre: str, recinto_nombre: str
    ) -> Optional[int]:
        if not asiento_nombre or not recinto_nombre:
            return None
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.id
                FROM recinto r
                JOIN asiento_electoral ae ON r.asiento_id = ae.id
                WHERE ae.nombre = ? AND r.nombre = ?
                LIMIT 1
            """, (asiento_nombre.strip(), recinto_nombre.strip()))
            result = cursor.fetchone()
            return result[0] if result else None

    def insert_record(self, table: str, data: Dict[str, Any]) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            fields = ", ".join(data.keys())
            placeholders = ", ".join("?" for _ in data)
            cursor.execute(
                f"INSERT INTO {table} ({fields}) VALUES ({placeholders})",
                list(data.values())
            )
            return cursor.lastrowid

    def update_record(self, table: str, data: Dict[str, Any], record_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            fields = ", ".join(f"{k} = ?" for k in data)
            values = list(data.values()) + [record_id]
            cursor.execute(f"UPDATE {table} SET {fields} WHERE id = ?", values)
            return cursor.rowcount > 0

    def get_stats(self) -> Dict[str, int]:
        tables = [
            'jefe', 'coordinador',
            'departamento', 'provincia', 'municipio',
            'asiento_electoral', 'recinto',
            'persona', 'acta',
        ]
        stats = {}
        with self.get_connection() as conn:
            cursor = conn.cursor()
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                stats[table] = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM persona WHERE tipo = 'operador'")
            stats['operadores'] = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM persona WHERE tipo = 'notario'")
            stats['notarios'] = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM persona WHERE user IS NOT NULL")
            stats['cuentas'] = cursor.fetchone()[0]
        return stats
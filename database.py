# ============================================
# database.py - ESQUEMA MEJORADO
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
        return sqlite3.connect(self.db_path)
    
    def create_schema(self):
        """Esquema optimizado con restricciones de integridad"""
        
        tables_sql = {
            # ORGANIZACIÓN
            'jefe': """
                CREATE TABLE IF NOT EXISTS jefe (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    cargo TEXT,
                    celular TEXT
                )
            """,
            
            'coordinador': """
                CREATE TABLE IF NOT EXISTS coordinador (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    ci TEXT UNIQUE NOT NULL,
                    expedido TEXT,
                    celular TEXT,
                    correo TEXT,
                    cargo TEXT,
                    jefe_id INTEGER NOT NULL,
                    FOREIGN KEY (jefe_id) REFERENCES jefe(id)
                )
            """,
            
            'grupo': """
                CREATE TABLE IF NOT EXISTS grupo (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    coordinador_id INTEGER NOT NULL,
                    FOREIGN KEY (coordinador_id) REFERENCES coordinador(id)
                )
            """,

            # GEOGRAFÍA
            'departamento': """
                CREATE TABLE IF NOT EXISTS departamento (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE
                )
            """,
            
            'provincia': """
                CREATE TABLE IF NOT EXISTS provincia (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    departamento_id INTEGER NOT NULL,
                    es_urbano BOOLEAN DEFAULT 0,
                    UNIQUE(departamento_id, nombre),
                    FOREIGN KEY (departamento_id) REFERENCES departamento(id)
                )
            """,
            
            'municipio': """
                CREATE TABLE IF NOT EXISTS municipio (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    provincia_id INTEGER NOT NULL,
                    UNIQUE(provincia_id, nombre),
                    FOREIGN KEY (provincia_id) REFERENCES provincia(id)
                )
            """,
            
            'asiento_electoral': """
                CREATE TABLE IF NOT EXISTS asiento_electoral (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    municipio_id INTEGER NOT NULL,
                    UNIQUE(municipio_id, nombre),
                    FOREIGN KEY (municipio_id) REFERENCES municipio(id)
                )
            """,
            
            'recinto': """
                CREATE TABLE IF NOT EXISTS recinto (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    direccion TEXT,
                    distrito INTEGER DEFAULT 0,
                    asiento_id INTEGER NOT NULL,
                    -- Clave compuesta: asiento + nombre es único
                    UNIQUE(asiento_id, nombre),
                    FOREIGN KEY (asiento_id) REFERENCES asiento_electoral(id)
                )
            """,

            # PERSONAS (sin campo 'tipo')
            'operador': """
                CREATE TABLE IF NOT EXISTS operador (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    ci TEXT UNIQUE NOT NULL,
                    expedido TEXT,
                    celular TEXT,
                    correo TEXT,
                    cargo TEXT,
                    recinto_id INTEGER NOT NULL,
                    grupo_id INTEGER NOT NULL,
                    FOREIGN KEY (recinto_id) REFERENCES recinto(id),
                    FOREIGN KEY (grupo_id) REFERENCES grupo(id)
                )
            """,
            
            'notario': """
                CREATE TABLE IF NOT EXISTS notario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    ci TEXT UNIQUE NOT NULL,
                    expedido TEXT,
                    celular TEXT,
                    correo TEXT,
                    cargo TEXT,
                    recinto_id INTEGER NOT NULL,
                    FOREIGN KEY (recinto_id) REFERENCES recinto(id)
                )
            """,
            
            'acta': """
                CREATE TABLE IF NOT EXISTS acta (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT NOT NULL UNIQUE,
                    recinto_id INTEGER NOT NULL,
                    FOREIGN KEY (recinto_id) REFERENCES recinto(id)
                )
            """,

            'cuenta': """
                CREATE TABLE IF NOT EXISTS cuenta (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    operador_id INTEGER NOT NULL UNIQUE,
                    FOREIGN KEY (operador_id) REFERENCES operador(id)
                )
            """
        }
        
        # VISTAS PARA CONSULTAS COMUNES
        views_sql = {
            'v_operadores_completo': """
                CREATE VIEW IF NOT EXISTS v_operadores_completo AS
                SELECT 
                    o.id,
                    o.nombre,
                    o.ci,
                    o.celular,
                    o.correo,
                    g.nombre as grupo,
                    c.nombre as coordinador,
                    j.nombre as jefe,
                    r.nombre as recinto,
                    r.direccion as recinto_direccion,
                    a.nombre as asiento_electoral,
                    m.nombre as municipio,
                    p.nombre as provincia,
                    d.nombre as departamento,
                    CASE WHEN p.es_urbano = 1 THEN 'urbano' ELSE 'rural' END as tipo
                FROM operador o
                LEFT JOIN grupo g ON o.grupo_id = g.id
                LEFT JOIN coordinador c ON g.coordinador_id = c.id
                LEFT JOIN jefe j ON c.jefe_id = j.id
                LEFT JOIN recinto r ON o.recinto_id = r.id
                LEFT JOIN asiento_electoral a ON r.asiento_id = a.id
                LEFT JOIN municipio m ON a.municipio_id = m.id
                LEFT JOIN provincia p ON m.provincia_id = p.id
                LEFT JOIN departamento d ON p.departamento_id = d.id
            """,
            
            'v_recintos_completo': """
                CREATE VIEW IF NOT EXISTS v_recintos_completo AS
                SELECT 
                    r.id,
                    r.nombre,
                    r.direccion,
                    r.distrito,
                    a.nombre as asiento_electoral,
                    m.nombre as municipio,
                    p.nombre as provincia,
                    d.nombre as departamento,
                    CASE WHEN p.es_urbano = 1 THEN 'urbano' ELSE 'rural' END as tipo,
                    p.nombre || ' - ' || a.nombre || ' - ' || r.nombre as nombre_completo
                FROM recinto r
                JOIN asiento_electoral a ON r.asiento_id = a.id
                JOIN municipio m ON a.municipio_id = m.id
                JOIN provincia p ON m.provincia_id = p.id
                JOIN departamento d ON p.departamento_id = d.id
            """
        }
        
        with self.get_connection() as conn:
            for table_name, sql in tables_sql.items():
                conn.execute(sql)
                print(f"Tabla '{table_name}' OK")
            
            for view_name, sql in views_sql.items():
                conn.execute(sql)
                print(f"Vista '{view_name}' OK")
        
        print("Esquema de base de datos listo")
    
    def insert_or_update(self, table: str, data: Dict[str, Any], unique_field: str) -> int:
        """Inserta o actualiza basado en campo único"""
        if not data or unique_field not in data:
            raise ValueError(f"Datos inválidos o campo único '{unique_field}' no encontrado")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                cursor.execute(f"SELECT id FROM {table} WHERE {unique_field} = ?", 
                            (data[unique_field],))
                existing = cursor.fetchone()
                
                if existing:
                    update_data = {k: v for k, v in data.items() if k != unique_field}
                    
                    if update_data:
                        update_fields = ", ".join([f"{k} = ?" for k in update_data.keys()])
                        values = list(update_data.values())
                        values.append(data[unique_field])
                        
                        cursor.execute(f"UPDATE {table} SET {update_fields} WHERE {unique_field} = ?", values)
                    
                    return existing[0]
                else:
                    fields = ", ".join(data.keys())
                    placeholders = ", ".join(["?" for _ in data.keys()])
                    values = list(data.values())
                    
                    cursor.execute(f"INSERT INTO {table} ({fields}) VALUES ({placeholders})", values)
                    return cursor.lastrowid
                    
            except sqlite3.IntegrityError as e:
                print(f"   Error de integridad en {table}: {e}")
                raise
            except sqlite3.Error as e:
                print(f"   Error en {table}: {e}")
                raise
    
    def get_recinto_id_by_asiento_and_nombre(self, asiento_nombre: str, recinto_nombre: str) -> Optional[int]:
        """Busca recinto por asiento electoral + nombre"""
        if not asiento_nombre or not recinto_nombre:
            return None
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.id 
                FROM recinto r
                JOIN asiento_electoral a ON r.asiento_id = a.id
                WHERE a.nombre = ? AND r.nombre = ?
                LIMIT 1
            """, (asiento_nombre.strip(), recinto_nombre.strip()))
            
            result = cursor.fetchone()
            return result[0] if result else None
    
    def get_id_by_field(self, table: str, field: str, value: Union[str, int]) -> Optional[int]:
        """Busca ID por campo específico"""
        if value is None:
            return None
            
        search_value = str(value).strip() if isinstance(value, str) else str(value)
        if not search_value:
            return None
            
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT id FROM {table} WHERE {field} = ? LIMIT 1", (search_value,))
            result = cursor.fetchone()
            return result[0] if result else None
    
    def insert_record(self, table: str, data: Dict[str, Any]) -> int:
        """Inserta nuevo registro"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            fields = ", ".join(data.keys())
            placeholders = ", ".join(["?" for _ in data.keys()])
            values = list(data.values())
            
            cursor.execute(f"INSERT INTO {table} ({fields}) VALUES ({placeholders})", values)
            return cursor.lastrowid

    def update_record(self, table: str, data: Dict[str, Any], record_id: int) -> bool:
        """Actualiza registro por ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            update_fields = ", ".join([f"{k} = ?" for k in data.keys()])
            values = list(data.values())
            values.append(record_id)
            
            cursor.execute(f"UPDATE {table} SET {update_fields} WHERE id = ?", values)
            return cursor.rowcount > 0
    
    def get_stats(self) -> Dict[str, int]:
        """Estadísticas por tabla"""
        tables = [
            'jefe', 'coordinador', 'grupo',
            'departamento', 'provincia', 'municipio', 'asiento_electoral', 'recinto',
            'operador', 'notario', 'acta', 'cuenta'
        ]
        
        stats = {}
        with self.get_connection() as conn:
            cursor = conn.cursor()
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                stats[table] = cursor.fetchone()[0]
        
        return stats

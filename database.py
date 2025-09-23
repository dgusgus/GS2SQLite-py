# database.py - Manejo de la base de datos
import sqlite3
from pathlib import Path
from typing import Dict, List, Any, Optional
from config import DATABASE_PATH

class DatabaseManager:
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"💾 Base de datos: {self.db_path}")
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def create_schema(self):
        """Crea todas las tablas - FÁCIL DE MODIFICAR"""
        
        # Si quieres cambiar la estructura de tablas, modifica aquí
        tables_sql = {
            'jefe': """
                CREATE TABLE IF NOT EXISTS jefe (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    telefono TEXT,
                    email TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """,
            
            'coordinador': """
                CREATE TABLE IF NOT EXISTS coordinador (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jefe_id INTEGER,
                    nombre TEXT NOT NULL,
                    codigo_coordinador TEXT UNIQUE,
                    telefono TEXT,
                    email TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (jefe_id) REFERENCES jefe(id)
                )
            """,
            
            'grupo': """
                CREATE TABLE IF NOT EXISTS grupo (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    coordinador_id INTEGER,
                    nombre_grupo TEXT NOT NULL UNIQUE,
                    descripcion TEXT,
                    fecha_creacion DATE DEFAULT CURRENT_DATE,
                    FOREIGN KEY (coordinador_id) REFERENCES coordinador(id)
                )
            """,
            
            'departamento': """
                CREATE TABLE IF NOT EXISTS departamento (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    codigo TEXT UNIQUE NOT NULL
                )
            """,
            
            'provincia': """
                CREATE TABLE IF NOT EXISTS provincia (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    depto_id INTEGER,
                    nombre TEXT NOT NULL,
                    codigo TEXT UNIQUE,
                    FOREIGN KEY (depto_id) REFERENCES departamento(id)
                )
            """,
            
            'municipio': """
                CREATE TABLE IF NOT EXISTS municipio (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    provincia_id INTEGER,
                    nombre TEXT NOT NULL,
                    codigo TEXT UNIQUE,
                    FOREIGN KEY (provincia_id) REFERENCES provincia(id)
                )
            """,
            
            'asiento_electoral': """
                CREATE TABLE IF NOT EXISTS asiento_electoral (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    municipio_id INTEGER,
                    nombre TEXT NOT NULL,
                    codigo TEXT UNIQUE,
                    FOREIGN KEY (municipio_id) REFERENCES municipio(id)
                )
            """,
            
            'recinto': """
                CREATE TABLE IF NOT EXISTS recinto (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    asiento_id INTEGER,
                    nombre TEXT NOT NULL UNIQUE,
                    direccion TEXT,
                    tipo TEXT DEFAULT 'urbano',
                    latitud REAL DEFAULT 0.0,
                    longitud REAL DEFAULT 0.0,
                    FOREIGN KEY (asiento_id) REFERENCES asiento_electoral(id)
                )
            """,
            
            'vehiculo': """
                CREATE TABLE IF NOT EXISTS vehiculo (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    placa TEXT UNIQUE NOT NULL,
                    modelo TEXT,
                    marca TEXT,
                    anio INTEGER,
                    estado TEXT DEFAULT 'activo'
                )
            """,
            
            'chofer': """
                CREATE TABLE IF NOT EXISTS chofer (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehiculo_id INTEGER,
                    nombre TEXT NOT NULL,
                    cedula TEXT UNIQUE,
                    licencia TEXT,
                    telefono TEXT,
                    FOREIGN KEY (vehiculo_id) REFERENCES vehiculo(id)
                )
            """,
            
            'operador': """
                CREATE TABLE IF NOT EXISTS operador (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    grupo_id INTEGER,
                    recinto_id INTEGER,
                    vehiculo_id INTEGER,
                    nombre TEXT NOT NULL,
                    cedula TEXT UNIQUE,
                    telefono TEXT,
                    tipo_operador TEXT DEFAULT 'urbano',
                    fecha_inicio DATE,
                    fecha_fin DATE,
                    estado TEXT DEFAULT 'activo',
                    FOREIGN KEY (grupo_id) REFERENCES grupo(id),
                    FOREIGN KEY (recinto_id) REFERENCES recinto(id),
                    FOREIGN KEY (vehiculo_id) REFERENCES vehiculo(id)
                )
            """
        }
        
        with self.get_connection() as conn:
            for table_name, sql in tables_sql.items():
                conn.execute(sql)
                print(f"✅ Tabla '{table_name}' creada/verificada")
        
        print("✅ Esquema de base de datos listo")
    
    def insert_or_update(self, table: str, data: Dict[str, Any], unique_field: str) -> int:
        """Inserta o actualiza registro"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Verificar si existe
            cursor.execute(f"SELECT id FROM {table} WHERE {unique_field} = ?", 
                          (data[unique_field],))
            existing = cursor.fetchone()
            
            if existing:
                # Actualizar
                update_fields = ", ".join([f"{k} = ?" for k in data.keys() if k != unique_field])
                values = [v for k, v in data.items() if k != unique_field]
                values.append(data[unique_field])
                
                cursor.execute(f"UPDATE {table} SET {update_fields} WHERE {unique_field} = ?", values)
                return existing[0]
            else:
                # Insertar nuevo
                fields = ", ".join(data.keys())
                placeholders = ", ".join(["?" for _ in data.keys()])
                values = list(data.values())
                
                cursor.execute(f"INSERT INTO {table} ({fields}) VALUES ({placeholders})", values)
                return cursor.lastrowid
    
    def get_id_by_field(self, table: str, field: str, value: str) -> Optional[int]:
        """Busca ID por un campo específico"""
        if not value or not value.strip():
            return None
            
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT id FROM {table} WHERE {field} = ? LIMIT 1", (value.strip(),))
            result = cursor.fetchone()
            return result[0] if result else None
    
    def get_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de registros"""
        tables = ['jefe', 'coordinador', 'grupo', 'departamento', 'provincia', 
                 'municipio', 'asiento_electoral', 'recinto', 'vehiculo', 'chofer', 'operador']
        
        stats = {}
        with self.get_connection() as conn:
            cursor = conn.cursor()
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                stats[table] = cursor.fetchone()[0]
        
        return stats

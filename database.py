# database.py - Manejo de la base de datos
import sqlite3
from pathlib import Path
from typing import Dict, Any, Optional, Union
from config import DATABASE_PATH


class DatabaseManager:
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True) 
        print(f"💾 Base de datos: {self.db_path}")
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def create_schema(self):
        """Crea todas las tablas con relaciones - adaptado a tu modelo"""
        
        tables_sql = {
            # =============================
            # ORGANIZACIÓN
            # =============================
            'jefe': """
                CREATE TABLE IF NOT EXISTS jefe (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    cargo TEXT,
                    celular TEXT
                )
            """,
            'coordinador': """
                CREATE TABLE IF NOT EXISTS coordinador (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    ci TEXT,
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
                    nombre TEXT NOT NULL,
                    coordinador_id INTEGER NOT NULL,
                    FOREIGN KEY (coordinador_id) REFERENCES coordinador(id)
                )
            """,

            # =============================
            # GEOGRAFÍA
            # =============================
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
                    FOREIGN KEY (departamento_id) REFERENCES departamento(id)
                )
            """,
            'municipio': """
                CREATE TABLE IF NOT EXISTS municipio (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    provincia_id INTEGER NOT NULL,
                    FOREIGN KEY (provincia_id) REFERENCES provincia(id)
                )
            """,
            'asiento_electoral': """
                CREATE TABLE IF NOT EXISTS asiento_electoral (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    municipio_id INTEGER NOT NULL,
                    FOREIGN KEY (municipio_id) REFERENCES municipio(id)
                )
            """,
            'recinto': """
                CREATE TABLE IF NOT EXISTS recinto (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    direccion TEXT,
                    distrito INTEGER DEFAULT 0, -- 0 = rural, 1..n = urbano
                    asiento_id INTEGER NOT NULL,
                    FOREIGN KEY (asiento_id) REFERENCES asiento_electoral(id)
                )
            """,

            # =============================
            # PERSONAS
            # =============================
            'operador': """
                CREATE TABLE IF NOT EXISTS operador (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    ci TEXT,
                    expedido TEXT,
                    celular TEXT,
                    correo TEXT,
                    cargo TEXT,
                    tipo TEXT CHECK(tipo IN ('urbano','rural')) DEFAULT 'urbano',
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
                    ci TEXT,
                    expedido TEXT,
                    celular TEXT,
                    correo TEXT,
                    cargo TEXT,
                    tipo TEXT CHECK(tipo IN ('urbano','rural')) DEFAULT 'urbano',
                    recinto_id INTEGER NOT NULL,
                    FOREIGN KEY (recinto_id) REFERENCES recinto(id)
                )
            """,
            'acta': """
                CREATE TABLE IF NOT EXISTS acta (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT NOT NULL,
                    recinto_id  INTEGER NOT NULL,
                    FOREIGN KEY (recinto_id) REFERENCES recinto(id)
                )
            """,

            # =============================
            # CUENTAS DE USUARIO (1:1 con Operador)
            # =============================
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
        
        with self.get_connection() as conn:
            for table_name, sql in tables_sql.items():
                conn.execute(sql)
                print(f"✅ Tabla '{table_name}' creada/verificada")
        
        print("✅ Esquema de base de datos listo")
    
    def insert_or_update(self, table: str, data: Dict[str, Any], unique_field: str) -> int:
        """Inserta o actualiza un registro basado en un campo único"""
        if not data or unique_field not in data:
            raise ValueError(f"Datos inválidos o campo único '{unique_field}' no encontrado")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                # Verificar si ya existe
                cursor.execute(f"SELECT id FROM {table} WHERE {unique_field} = ?", 
                            (data[unique_field],))
                existing = cursor.fetchone()
                
                if existing:
                    # Preparar datos para UPDATE (excluyendo el campo único)
                    update_data = {}
                    for key, value in data.items():
                        if key != unique_field:
                            update_data[key] = value
                    
                    # Solo hacer UPDATE si hay campos para actualizar
                    if update_data:
                        update_fields = ", ".join([f"{k} = ?" for k in update_data.keys()])
                        values = list(update_data.values())
                        values.append(data[unique_field])  # Para el WHERE
                        
                        query = f"UPDATE {table} SET {update_fields} WHERE {unique_field} = ?"
                        cursor.execute(query, values)
                        print(f"   🔄 Actualizado {table} WHERE {unique_field} = {data[unique_field]}")
                    else:
                        print(f"   ℹ️  Registro existente en {table} WHERE {unique_field} = {data[unique_field]} (sin cambios)")
                    
                    return existing[0]
                else:
                    # INSERT nuevo registro
                    fields = ", ".join(data.keys())
                    placeholders = ", ".join(["?" for _ in data.keys()])
                    values = list(data.values())
                    
                    query = f"INSERT INTO {table} ({fields}) VALUES ({placeholders})"
                    cursor.execute(query, values)
                    print(f"   ✅ Insertado nuevo {table}: {unique_field} = {data[unique_field]}")
                    return cursor.lastrowid
                    
            except sqlite3.Error as e:
                print(f"   ❌ Error en {table} con {unique_field}={data[unique_field]}: {e}")
                raise
                
    def get_id_by_field(self, table: str, field: str, value: Union[str, int]) -> Optional[int]:
        """Busca ID por un campo específico, maneja strings e integers"""
        if value is None:
            return None
            
        # Convertir a string para la consulta si es necesario
        if isinstance(value, (int, float)):
            search_value = str(value)
        else:
            search_value = str(value).strip()
            if not search_value:
                return None
            
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Si el campo es numérico en la BD pero recibimos string, convertir
            if field == 'numero':  # Para mesas
                try:
                    cursor.execute(f"SELECT id FROM {table} WHERE {field} = ? LIMIT 1", (int(search_value),))
                except ValueError:
                    return None
            else:
                cursor.execute(f"SELECT id FROM {table} WHERE {field} = ? LIMIT 1", (search_value,))
                
            result = cursor.fetchone()
            return result[0] if result else None
    
    def get_stats(self) -> Dict[str, int]:
        """Devuelve el total de registros por tabla"""
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
    
    def insert_record(self, table: str, data: Dict[str, Any]) -> int:
        """Inserta un nuevo registro sin verificar duplicados"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            fields = ", ".join(data.keys())
            placeholders = ", ".join(["?" for _ in data.keys()])
            values = list(data.values())
            
            cursor.execute(f"INSERT INTO {table} ({fields}) VALUES ({placeholders})", values)
            return cursor.lastrowid

    def update_record(self, table: str, data: Dict[str, Any], record_id: int) -> bool:
        """Actualiza un registro existente por ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            update_fields = ", ".join([f"{k} = ?" for k in data.keys()])
            values = list(data.values())
            values.append(record_id)
            
            cursor.execute(f"UPDATE {table} SET {update_fields} WHERE id = ?", values)
            return cursor.rowcount > 0
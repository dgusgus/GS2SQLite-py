# main.py - Sistema 1: Conversión de Datos
import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import argparse
from pathlib import Path

# Google Sheets imports
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Configuración
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]

SPREADSHEET_ID = "1ehySw2tVI1l8INo4fgE7kEGFd0Kb2miPs7vCqsFZC8I"
DATABASE_PATH = "../database/operadores.db"
CREDENTIALS_PATH = "generador-docs-31f4b831a196.json"

# Esquemas de datos
@dataclass
class Jefe:
    id: Optional[int]
    nombre: str
    telefono: str = ""
    email: str = ""

@dataclass  
class Coordinador:
    id: Optional[int]
    jefe_id: int
    nombre: str
    codigo_coordinador: str
    telefono: str = ""
    email: str = ""

@dataclass
class Grupo:
    id: Optional[int] 
    coordinador_id: int
    nombre_grupo: str
    descripcion: str = ""
    fecha_creacion: str = ""

@dataclass
class Departamento:
    id: Optional[int]
    nombre: str
    codigo: str

@dataclass
class Provincia:
    id: Optional[int]
    depto_id: int
    nombre: str  
    codigo: str

@dataclass
class Municipio:
    id: Optional[int]
    provincia_id: int
    nombre: str
    codigo: str

@dataclass  
class AsientoElectoral:
    id: Optional[int]
    municipio_id: int
    nombre: str
    codigo: str

@dataclass
class Recinto:
    id: Optional[int]
    asiento_id: int
    nombre: str
    direccion: str
    tipo: str = "urbano"  # urbano/rural
    latitud: float = 0.0
    longitud: float = 0.0

@dataclass
class Vehiculo:
    id: Optional[int]
    placa: str
    modelo: str = ""
    marca: str = ""
    anio: int = 0
    estado: str = "activo"

@dataclass
class Chofer:
    id: Optional[int]
    vehiculo_id: int
    nombre: str
    cedula: str
    licencia: str = ""
    telefono: str = ""

@dataclass
class Operador:
    id: Optional[int]
    grupo_id: int
    recinto_id: int
    vehiculo_id: Optional[int]
    nombre: str
    cedula: str
    telefono: str = ""
    tipo_operador: str = "urbano"  # rural/urbano
    fecha_inicio: str = ""
    fecha_fin: str = ""
    estado: str = "activo"

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def create_database_schema(self):
        """Crea todas las tablas de la base de datos"""
        
        schema_sql = """
        -- Tabla Jefes
        CREATE TABLE IF NOT EXISTS jefe (
            jefe_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            email TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Tabla Coordinadores  
        CREATE TABLE IF NOT EXISTS coordinador (
            coordinador_id INTEGER PRIMARY KEY AUTOINCREMENT,
            jefe_id INTEGER,
            nombre TEXT NOT NULL,
            codigo_coordinador TEXT UNIQUE,
            telefono TEXT,
            email TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (jefe_id) REFERENCES jefe(jefe_id)
        );
        
        -- Tabla Grupos
        CREATE TABLE IF NOT EXISTS grupo (
            grupo_id INTEGER PRIMARY KEY AUTOINCREMENT,
            coordinador_id INTEGER,
            nombre_grupo TEXT NOT NULL,
            descripcion TEXT,
            fecha_creacion DATE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (coordinador_id) REFERENCES coordinador(coordinador_id)
        );
        
        -- Ubicaciones geográficas
        CREATE TABLE IF NOT EXISTS departamento (
            depto_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            codigo TEXT UNIQUE
        );
        
        CREATE TABLE IF NOT EXISTS provincia (
            provincia_id INTEGER PRIMARY KEY AUTOINCREMENT,
            depto_id INTEGER,
            nombre TEXT NOT NULL,
            codigo TEXT,
            FOREIGN KEY (depto_id) REFERENCES departamento(depto_id)
        );
        
        CREATE TABLE IF NOT EXISTS municipio (
            municipio_id INTEGER PRIMARY KEY AUTOINCREMENT,
            provincia_id INTEGER,
            nombre TEXT NOT NULL,
            codigo TEXT,
            FOREIGN KEY (provincia_id) REFERENCES provincia(provincia_id)
        );
        
        CREATE TABLE IF NOT EXISTS asiento_electoral (
            asiento_id INTEGER PRIMARY KEY AUTOINCREMENT,
            municipio_id INTEGER,
            nombre TEXT NOT NULL,
            codigo TEXT,
            FOREIGN KEY (municipio_id) REFERENCES municipio(municipio_id)
        );
        
        CREATE TABLE IF NOT EXISTS recinto (
            recinto_id INTEGER PRIMARY KEY AUTOINCREMENT,
            asiento_id INTEGER,
            nombre TEXT NOT NULL,
            direccion TEXT,
            tipo TEXT CHECK(tipo IN ('urbano', 'rural')) DEFAULT 'urbano',
            latitud REAL DEFAULT 0.0,
            longitud REAL DEFAULT 0.0,
            FOREIGN KEY (asiento_id) REFERENCES asiento_electoral(asiento_id)
        );
        
        -- Transporte
        CREATE TABLE IF NOT EXISTS vehiculo (
            vehiculo_id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT UNIQUE NOT NULL,
            modelo TEXT,
            marca TEXT,
            anio INTEGER,
            estado TEXT DEFAULT 'activo',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS chofer (
            chofer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehiculo_id INTEGER,
            nombre TEXT NOT NULL,
            cedula TEXT UNIQUE,
            licencia TEXT,
            telefono TEXT,
            FOREIGN KEY (vehiculo_id) REFERENCES vehiculo(vehiculo_id)
        );
        
        -- Operadores
        CREATE TABLE IF NOT EXISTS operador (
            operador_id INTEGER PRIMARY KEY AUTOINCREMENT,
            grupo_id INTEGER,
            recinto_id INTEGER,
            vehiculo_id INTEGER,
            nombre TEXT NOT NULL,
            cedula TEXT UNIQUE,
            telefono TEXT,
            tipo_operador TEXT CHECK(tipo_operador IN ('rural', 'urbano')) DEFAULT 'urbano',
            fecha_inicio DATE,
            fecha_fin DATE,
            estado TEXT DEFAULT 'activo',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (grupo_id) REFERENCES grupo(grupo_id),
            FOREIGN KEY (recinto_id) REFERENCES recinto(recinto_id),
            FOREIGN KEY (vehiculo_id) REFERENCES vehiculo(vehiculo_id)
        );
        
        -- Documentos
        CREATE TABLE IF NOT EXISTS documento (
            documento_id INTEGER PRIMARY KEY AUTOINCREMENT,
            operador_id INTEGER,
            tipo_documento TEXT NOT NULL,
            ruta_archivo TEXT,
            fecha_generacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            estado TEXT DEFAULT 'pendiente',
            formato TEXT,
            FOREIGN KEY (operador_id) REFERENCES operador(operador_id)
        );
        
        -- Asignaciones de transporte
        CREATE TABLE IF NOT EXISTS asignacion_transporte (
            asignacion_id INTEGER PRIMARY KEY AUTOINCREMENT,
            operador_id INTEGER,
            vehiculo_id INTEGER,
            fecha_asignacion DATE,
            hora_salida TIME,
            hora_retorno TIME,
            estado TEXT DEFAULT 'programado',
            observaciones TEXT,
            FOREIGN KEY (operador_id) REFERENCES operador(operador_id),
            FOREIGN KEY (vehiculo_id) REFERENCES vehiculo(vehiculo_id)
        );
        
        -- Índices para optimizar consultas
        CREATE INDEX IF NOT EXISTS idx_operador_cedula ON operador(cedula);
        CREATE INDEX IF NOT EXISTS idx_operador_grupo ON operador(grupo_id);
        CREATE INDEX IF NOT EXISTS idx_operador_recinto ON operador(recinto_id);
        CREATE INDEX IF NOT EXISTS idx_documento_operador ON documento(operador_id);
        CREATE INDEX IF NOT EXISTS idx_vehiculo_placa ON vehiculo(placa);
        """
        
        with self.get_connection() as conn:
            conn.executescript(schema_sql)
            print("✅ Base de datos creada exitosamente")
    
    def insert_or_update_record(self, table: str, data: Dict[str, Any], unique_field: str = None) -> int:
        """Inserta o actualiza un registro, retorna el ID"""
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Si hay campo único, verificar si existe
            if unique_field and unique_field in data:
                cursor.execute(f"SELECT rowid FROM {table} WHERE {unique_field} = ?", 
                             (data[unique_field],))
                existing = cursor.fetchone()
                
                if existing:
                    # Actualizar registro existente
                    update_fields = ", ".join([f"{k} = ?" for k in data.keys() if k != unique_field])
                    values = [v for k, v in data.items() if k != unique_field]
                    values.append(data[unique_field])
                    
                    cursor.execute(f"UPDATE {table} SET {update_fields} WHERE {unique_field} = ?", values)
                    return existing[0]
            
            # Insertar nuevo registro
            fields = ", ".join(data.keys())
            placeholders = ", ".join(["?" for _ in data.keys()])
            values = list(data.values())
            
            cursor.execute(f"INSERT INTO {table} ({fields}) VALUES ({placeholders})", values)
            return cursor.lastrowid

class GoogleSheetsManager:
    def __init__(self, credentials_path: str, spreadsheet_id: str):
        self.credentials_path = credentials_path
        self.spreadsheet_id = spreadsheet_id
        self.client = None
        self._authenticate()
    
    def _authenticate(self):
        """Autentica con Google Sheets API"""
        try:
            creds = Credentials.from_service_account_file(
                self.credentials_path, scopes=SCOPES
            )
            self.client = gspread.authorize(creds)
            print("✅ Autenticación con Google Sheets exitosa")
        except Exception as e:
            print(f"❌ Error de autenticación: {e}")
            raise
    
    def get_worksheet_data(self, sheet_name: str) -> List[Dict[str, str]]:
        """Obtiene datos de una hoja específica"""
        try:
            spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            worksheet = spreadsheet.worksheet(sheet_name)
            
            # Obtener todos los datos como lista de diccionarios
            data = worksheet.get_all_records()
            print(f"✅ Obtenidos {len(data)} registros de '{sheet_name}'")
            return data
            
        except Exception as e:
            print(f"❌ Error obteniendo datos de '{sheet_name}': {e}")
            return []
    
    def get_all_worksheet_names(self) -> List[str]:
        """Obtiene nombres de todas las hojas"""
        try:
            spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            return [ws.title for ws in spreadsheet.worksheets()]
        except Exception as e:
            print(f"❌ Error obteniendo nombres de hojas: {e}")
            return []

class DataConverter:
    def __init__(self, db_manager: DatabaseManager, sheets_manager: GoogleSheetsManager):
        self.db = db_manager
        self.sheets = sheets_manager
    
    def convert_all_data(self):
        """Convierte todos los datos desde Google Sheets a SQLite"""
        print("🚀 Iniciando conversión de datos...")
        
        # 1. Crear esquema de base de datos
        self.db.create_database_schema()
        
        # 2. Obtener nombres de hojas disponibles
        worksheets = self.sheets.get_all_worksheet_names()
        print(f"📊 Hojas disponibles: {worksheets}")
        
        # 3. Convertir cada tipo de dato
        conversion_map = {
            'jefes': self._convert_jefes,
            'coordinadores': self._convert_coordinadores, 
            'grupos': self._convert_grupos,
            'departamentos': self._convert_departamentos,
            'provincias': self._convert_provincias,
            'municipios': self._convert_municipios,
            'asientos_electorales': self._convert_asientos,
            'recintos': self._convert_recintos,
            'vehiculos': self._convert_vehiculos,
            'choferes': self._convert_choferes,
            'operadores': self._convert_operadores
        }
        
        for sheet_name, converter_func in conversion_map.items():
            if sheet_name in worksheets:
                print(f"\n📝 Procesando {sheet_name}...")
                converter_func(sheet_name)
            else:
                print(f"⚠️  Hoja '{sheet_name}' no encontrada, saltando...")
        
        print("\n✅ Conversión completada!")
    
    def _convert_jefes(self, sheet_name: str):
        data = self.sheets.get_worksheet_data(sheet_name)
        for row in data:
            if row.get('nombre'):  # Solo procesar si tiene nombre
                jefe_data = {
                    'nombre': row.get('nombre', '').strip(),
                    'telefono': row.get('telefono', '').strip(),
                    'email': row.get('email', '').strip()
                }
                self.db.insert_or_update_record('jefe', jefe_data, 'nombre')
    
    def _convert_coordinadores(self, sheet_name: str):
        data = self.sheets.get_worksheet_data(sheet_name)
        for row in data:
            if row.get('nombre') and row.get('codigo_coordinador'):
                # Buscar jefe_id por nombre
                jefe_nombre = row.get('jefe_nombre', '').strip()
                jefe_id = self._get_id_by_field('jefe', 'nombre', jefe_nombre) if jefe_nombre else None
                
                coord_data = {
                    'jefe_id': jefe_id,
                    'nombre': row.get('nombre', '').strip(),
                    'codigo_coordinador': row.get('codigo_coordinador', '').strip(),
                    'telefono': row.get('telefono', '').strip(),
                    'email': row.get('email', '').strip()
                }
                self.db.insert_or_update_record('coordinador', coord_data, 'codigo_coordinador')
    
    def _convert_grupos(self, sheet_name: str):
        data = self.sheets.get_worksheet_data(sheet_name)
        for row in data:
            if row.get('nombre_grupo'):
                # Buscar coordinador_id por código
                coord_codigo = row.get('coordinador_codigo', '').strip()
                coord_id = self._get_id_by_field('coordinador', 'codigo_coordinador', coord_codigo) if coord_codigo else None
                
                grupo_data = {
                    'coordinador_id': coord_id,
                    'nombre_grupo': row.get('nombre_grupo', '').strip(),
                    'descripcion': row.get('descripcion', '').strip(),
                    'fecha_creacion': row.get('fecha_creacion', datetime.now().strftime('%Y-%m-%d'))
                }
                self.db.insert_or_update_record('grupo', grupo_data, 'nombre_grupo')
    
    def _convert_departamentos(self, sheet_name: str):
        data = self.sheets.get_worksheet_data(sheet_name)
        for row in data:
            if row.get('nombre'):
                depto_data = {
                    'nombre': row.get('nombre', '').strip(),
                    'codigo': row.get('codigo', '').strip()
                }
                self.db.insert_or_update_record('departamento', depto_data, 'codigo')
    
    def _convert_provincias(self, sheet_name: str):
        data = self.sheets.get_worksheet_data(sheet_name)
        for row in data:
            if row.get('nombre'):
                depto_codigo = row.get('departamento_codigo', '').strip()
                depto_id = self._get_id_by_field('departamento', 'codigo', depto_codigo) if depto_codigo else None
                
                prov_data = {
                    'depto_id': depto_id,
                    'nombre': row.get('nombre', '').strip(),
                    'codigo': row.get('codigo', '').strip()
                }
                self.db.insert_or_update_record('provincia', prov_data, 'codigo')
    
    def _convert_municipios(self, sheet_name: str):
        data = self.sheets.get_worksheet_data(sheet_name)
        for row in data:
            if row.get('nombre'):
                prov_codigo = row.get('provincia_codigo', '').strip()
                prov_id = self._get_id_by_field('provincia', 'codigo', prov_codigo) if prov_codigo else None
                
                mun_data = {
                    'provincia_id': prov_id,
                    'nombre': row.get('nombre', '').strip(),
                    'codigo': row.get('codigo', '').strip()
                }
                self.db.insert_or_update_record('municipio', mun_data, 'codigo')
    
    def _convert_asientos(self, sheet_name: str):
        data = self.sheets.get_worksheet_data(sheet_name)
        for row in data:
            if row.get('nombre'):
                mun_codigo = row.get('municipio_codigo', '').strip()
                mun_id = self._get_id_by_field('municipio', 'codigo', mun_codigo) if mun_codigo else None
                
                asiento_data = {
                    'municipio_id': mun_id,
                    'nombre': row.get('nombre', '').strip(),
                    'codigo': row.get('codigo', '').strip()
                }
                self.db.insert_or_update_record('asiento_electoral', asiento_data, 'codigo')
    
    def _convert_recintos(self, sheet_name: str):
        data = self.sheets.get_worksheet_data(sheet_name)
        for row in data:
            if row.get('nombre'):
                asiento_codigo = row.get('asiento_codigo', '').strip()
                asiento_id = self._get_id_by_field('asiento_electoral', 'codigo', asiento_codigo) if asiento_codigo else None
                
                recinto_data = {
                    'asiento_id': asiento_id,
                    'nombre': row.get('nombre', '').strip(),
                    'direccion': row.get('direccion', '').strip(),
                    'tipo': row.get('tipo', 'urbano').lower(),
                    'latitud': float(row.get('latitud', 0) or 0),
                    'longitud': float(row.get('longitud', 0) or 0)
                }
                self.db.insert_or_update_record('recinto', recinto_data, 'nombre')
    
    def _convert_vehiculos(self, sheet_name: str):
        data = self.sheets.get_worksheet_data(sheet_name)
        for row in data:
            if row.get('placa'):
                vehiculo_data = {
                    'placa': row.get('placa', '').strip().upper(),
                    'modelo': row.get('modelo', '').strip(),
                    'marca': row.get('marca', '').strip(),
                    'anio': int(row.get('anio', 0) or 0),
                    'estado': row.get('estado', 'activo').lower()
                }
                self.db.insert_or_update_record('vehiculo', vehiculo_data, 'placa')
    
    def _convert_choferes(self, sheet_name: str):
        data = self.sheets.get_worksheet_data(sheet_name)
        for row in data:
            if row.get('cedula'):
                placa = row.get('vehiculo_placa', '').strip().upper()
                vehiculo_id = self._get_id_by_field('vehiculo', 'placa', placa) if placa else None
                
                chofer_data = {
                    'vehiculo_id': vehiculo_id,
                    'nombre': row.get('nombre', '').strip(),
                    'cedula': row.get('cedula', '').strip(),
                    'licencia': row.get('licencia', '').strip(),
                    'telefono': row.get('telefono', '').strip()
                }
                self.db.insert_or_update_record('chofer', chofer_data, 'cedula')
    
    def _convert_operadores(self, sheet_name: str):
        data = self.sheets.get_worksheet_data(sheet_name)
        for row in data:
            if row.get('cedula'):
                # Buscar IDs relacionados
                grupo_nombre = row.get('grupo_nombre', '').strip()
                grupo_id = self._get_id_by_field('grupo', 'nombre_grupo', grupo_nombre) if grupo_nombre else None
                
                recinto_nombre = row.get('recinto_nombre', '').strip()
                recinto_id = self._get_id_by_field('recinto', 'nombre', recinto_nombre) if recinto_nombre else None
                
                placa = row.get('vehiculo_placa', '').strip().upper()
                vehiculo_id = self._get_id_by_field('vehiculo', 'placa', placa) if placa else None
                
                operador_data = {
                    'grupo_id': grupo_id,
                    'recinto_id': recinto_id,
                    'vehiculo_id': vehiculo_id,
                    'nombre': row.get('nombre', '').strip(),
                    'cedula': row.get('cedula', '').strip(),
                    'telefono': row.get('telefono', '').strip(),
                    'tipo_operador': row.get('tipo_operador', 'urbano').lower(),
                    'fecha_inicio': row.get('fecha_inicio', ''),
                    'fecha_fin': row.get('fecha_fin', ''),
                    'estado': row.get('estado', 'activo').lower()
                }
                self.db.insert_or_update_record('operador', operador_data, 'cedula')
    
    def _get_id_by_field(self, table: str, field: str, value: str) -> Optional[int]:
        """Obtiene ID de una tabla por un campo específico"""
        if not value:
            return None
            
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT rowid FROM {table} WHERE {field} = ? LIMIT 1", (value,))
            result = cursor.fetchone()
            return result[0] if result else None
    
    def show_import_stats(self):
        """Muestra estadísticas de la importación"""
        print("\n📊 ESTADÍSTICAS DE IMPORTACIÓN")
        print("=" * 50)
        
        tables_to_check = [
            'jefe', 'coordinador', 'grupo', 'departamento', 'provincia', 
            'municipio', 'asiento_electoral', 'recinto', 'vehiculo', 
            'chofer', 'operador'
        ]
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            for table in tables_to_check:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"{table.ljust(20)}: {count:>5} registros")

def main():
    """Función principal con CLI"""
    parser = argparse.ArgumentParser(description="Sistema 1: Conversión de Datos Google Sheets → SQLite")
    parser.add_argument('--action', choices=['create', 'import', 'stats', 'all'], 
                       default='all', help='Acción a realizar')
    parser.add_argument('--credentials', default=CREDENTIALS_PATH, 
                       help='Ruta del archivo JSON de credenciales')
    parser.add_argument('--database', default=DATABASE_PATH, 
                       help='Ruta de la base de datos SQLite')
    
    args = parser.parse_args()
    
    try:
        # Inicializar componentes
        db_manager = DatabaseManager(args.database)
        
        if args.action in ['import', 'all']:
            sheets_manager = GoogleSheetsManager(args.credentials, SPREADSHEET_ID)
            converter = DataConverter(db_manager, sheets_manager)
        
        # Ejecutar acciones
        if args.action == 'create':
            db_manager.create_database_schema()
            
        elif args.action == 'import':
            converter.convert_all_data()
            
        elif args.action == 'stats':
            converter = DataConverter(db_manager, None)
            converter.show_import_stats()
            
        elif args.action == 'all':
            converter.convert_all_data()
            converter.show_import_stats()
        
        print("\n🎉 Proceso completado exitosamente!")
        
    except FileNotFoundError as e:
        print(f"❌ Archivo no encontrado: {e}")
        print("Asegúrate de que el archivo de credenciales esté en la ruta correcta")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    main()